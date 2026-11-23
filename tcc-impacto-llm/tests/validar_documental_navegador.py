"""Chrome real via CDP local, sem driver/download. Todos os envios são SINTÉTICOS.

Execute da raiz: python -B tests/validar_documental_navegador.py
Não equivale a testar a API nem o processo de revisão humana.
"""
import base64
import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import tempfile
import threading
import time
import urllib.request

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import websocket
import coletor_api as api
import painel_documental as painel
import painel_llm as base
from test_painel_llm import envelope, KEY, TEXT

ROOT = Path(__file__).resolve().parents[1]
AREA = ROOT/'evidencias/spec004/integracao-documental-64-2026-11-22/navegador-sintetico'


def main():
    AREA.mkdir(parents=True, exist_ok=True)
    calls, modes, checks = [], [], []
    os.environ.pop('OPENAI_API_KEY', None)
    api.enviar = lambda *_: (_ for _ in ()).throw(AssertionError('API real proibida'))
    def offline(event, args):
        if event == 'socket.connect' and isinstance(args[1], tuple):
            if args[1][0] not in ('127.0.0.1', '::1', 'localhost'):
                raise AssertionError('Conexão externa proibida')
    sys.addaudithook(offline)

    def sender(body, key, timeout):
        calls.append(json.loads(body))
        mode = modes.pop(0) if modes else 'valida'
        if mode == 'fragmento':
            raise api.FalhaTransporte('IncompleteRead', partial=b'FRAGMENTO SINTETICO', status=200)
        text = '```json\n'+TEXT+'\n```' if mode == 'invalida' else TEXT
        model = 'modelo-reportado-SINTETICO' if mode == 'divergente' else json.loads(body)['model']
        return 200, envelope(text, model), 'req-SINTETICA-'+str(len(calls))

    # Destino novo por execução, preserva capturas artificiais anteriores.
    run = AREA/('execucao-'+str(time.time_ns()))
    app = painel.Aplicacao(sender=sender, chave=lambda: KEY, origem='sintetica',
        area_captura=run/'demonstracoes', area_avaliacao=run/'demonstracoes-avaliadas',
        area_documental_captura=run/'capturas-SINTETICAS',
        area_documental_avaliacao=run/'avaliacoes-SINTETICAS')
    server = base.ThreadingHTTPServer(('127.0.0.1', 0), base.handler(app))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    url = 'http://127.0.0.1:'+str(server.server_address[1])+'/'
    chrome = Path(os.environ.get('TCC_TEST_BROWSER', 'C:/Program Files/Google/Chrome/Application/chrome.exe'))
    assert chrome.exists(), 'Chrome local indisponível'
    process, ws = None, None
    temp = tempfile.TemporaryDirectory(prefix='tcc-cdp-')
    try:
        process = subprocess.Popen([str(chrome), '--headless=new', '--remote-debugging-port=0',
            '--remote-allow-origins=http://localhost', '--user-data-dir='+temp.name,
            '--no-first-run', '--no-default-browser-check', '--disable-background-networking',
            '--disable-component-update', '--disable-sync', '--disable-default-apps',
            '--proxy-server=http://127.0.0.1:9', '--proxy-bypass-list=127.0.0.1;localhost',
            '--window-size=1366,900', 'about:blank'], stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL, creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
        active = Path(temp.name)/'DevToolsActivePort'
        ready_port = []
        def port_ready():
            try:
                lines = active.read_text().splitlines()
                if len(lines) < 2:
                    return False
                ready_port.append(lines[0])
                return True
            except (OSError, IndexError):
                return False
        until(port_ready, timeout=20)
        port = ready_port[0]
        opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
        with opener.open('http://127.0.0.1:'+port+'/json', timeout=15) as response:
            pages = json.load(response)
        ws = websocket.create_connection(next(p['webSocketDebuggerUrl'] for p in pages if p['type']=='page'),
            timeout=15, origin='http://localhost', http_proxy_host=None)
        sequence = 0
        def cdp(method, params=None):
            nonlocal sequence
            sequence += 1
            ws.send(json.dumps({'id': sequence, 'method': method, 'params':params or {}}))
            while True:
                reply = json.loads(ws.recv())
                if reply.get('id') == sequence:
                    assert 'error' not in reply, reply
                    return reply.get('result', {})
        def js(code):
            result = cdp('Runtime.evaluate', {'expression':code, 'returnByValue':True, 'awaitPromise':True})
            assert 'exceptionDetails' not in result, result
            return result['result'].get('value')
        def click(identity):
            rect = js("(()=>{const e=document.getElementById("+json.dumps(identity)+
                ");e.scrollIntoView({block:'center'});const r=e.getBoundingClientRect();return {x:r.x+r.width/2,y:r.y+r.height/2,disabled:e.disabled};})()")
            assert not rect['disabled'], identity+' desabilitado'
            for action in ('mousePressed', 'mouseReleased'):
                cdp('Input.dispatchMouseEvent', {'type':action, 'x':rect['x'], 'y':rect['y'], 'button':'left', 'clickCount':1})
        def select(identity, value):
            js(f"document.getElementById({json.dumps(identity)}).value={json.dumps(value)};document.getElementById({json.dumps(identity)}).dispatchEvent(new Event('change'))")
        def shot(name):
            raw = cdp('Page.captureScreenshot', {'format':'png', 'captureBeyondViewport':False})
            (AREA/name).write_bytes(base64.b64decode(raw['data']))
        cdp('Page.enable');cdp('Runtime.enable')
        cdp('Emulation.setDeviceMetricsOverride', {'width':1366,'height':768,'deviceScaleFactor':1,'mobile':False})
        cdp('Page.navigate', {'url':url})
        until(lambda: js("!!state.options?.documental&&state.rows.length===80"))
        assert not calls
        assert js("document.getElementById('execution-mode').value") == 'documental'
        assert js('state.options.documental.celulas.length') == 32
        shot('01-executar-1366.png')
        click('doc-preview')
        until(lambda: js("document.getElementById('doc-payload').textContent.includes('<<<inicio:sistema>>>')"))
        assert not calls
        checks.append('Abertura, plano e prévia sem envio; 32 células e 64 posições renderizadas.')
        click('doc-run')
        # Segundo evento artificial de clique ainda passa pelo bloqueio do navegador.
        js("document.getElementById('doc-run').dispatchEvent(new Event('click'))")
        until(lambda: js('state.options.documental.pendentes===63&&!state.busy'))
        assert len(calls) == 1
        assert js("!document.getElementById('doc-batch').classList.contains('hidden')")
        assert '63 respostas sintéticas' in js("document.getElementById('doc-continue').textContent")
        shot('02-primeira-capturada.png')
        checks.append('Primeira observação e clique duplicado: somente um envio artificial.')
        js("document.getElementById('doc-limit').value='2';document.getElementById('doc-limit').dispatchEvent(new Event('input'))")
        assert '2 respostas sintéticas' in js("document.getElementById('doc-continue').textContent")
        click('doc-continue')
        until(lambda: js('state.options.documental.pendentes===61&&!state.busy'))
        assert len(calls) == 3
        checks.append('Continuidade com limite explícito de duas, ordem preservada.')
        modes.append('invalida')
        click('doc-run')
        until(lambda: js('state.options.documental.pendentes===60&&!state.busy'))
        modes.append('fragmento')
        click('doc-run')
        until(lambda: js('state.options.documental.pendentes===59&&!state.busy'))
        modes.append('divergente')
        click('doc-run')
        until(lambda: js('state.options.documental.pendentes===58&&!state.busy'))
        checks.append('Inválida, fragmento/estado desconhecido e divergência reportada, sem reparo/retry.')
        # POST recebido no servidor, resposta perdida somente no cliente.
        js("window.originalFetch=window.fetch;window.fetch=async(...args)=>{const r=await window.originalFetch(...args);if(args[0]==='/api/executar')throw new Error('PERDA SINTÉTICA DA CONFIRMAÇÃO');return r}")
        click('doc-run')
        until(lambda: len(calls)==7)
        until(lambda: js("document.getElementById('progress-text').textContent.includes('Consultar estado')"))
        assert js("document.getElementById('doc-run').disabled")
        js('window.fetch=window.originalFetch')
        until(lambda: app.documental.worker is not None and not app.documental.worker.is_alive())
        click('doc-refresh')
        until(lambda: js('state.options.documental.pendentes===57&&!state.busy&&state.rows.length===87'))
        assert len(calls) == 7
        cdp('Page.reload')
        until(lambda: js('!!state.options?.documental&&state.options.documental.pendentes===57&&state.rows.length===87'))
        assert len(calls) == 7
        checks.append('POST sem confirmação: bloqueio, consulta e recarga sem reenvio das sete posições iniciadas.')
        js("view('resultados')")
        select('filter-cohort', 'documentacao_operacional_64_sintetica')
        assert js("document.getElementById('result-rows').children.length") == 7
        assert js("document.getElementById('doc-cell-rows').children.length") == 32
        shot('03-resultados-1366.png')
        first = app.documental.rows[0]
        for identity, value in (('filter-documentation', first['documentacao_id']),
            ('filter-model', first['modelo_solicitado']), ('filter-change', first['mudanca']),
            ('filter-condition', first['condicao']), ('filter-note', first['nota_id']),
            ('filter-repetition', str(first['repeticao']))):
            select(identity, value)
        assert js("document.getElementById('result-rows').children.length") == 1
        assert js("document.getElementById('doc-cell-rows').children.length") == 1
        click_id = first['observacao_id']
        js('openDetail('+json.dumps(click_id)+')')
        until(lambda: js("document.getElementById('detail').open"))
        assert js("state.detail.documentacao_id") == first['documentacao_id']
        assert js("state.detail.celula.N_planejado") == 2
        click('dim-tests')
        assert js("document.getElementById('detail-rows').children.length") > 0
        shot('04-detalhes-1366.png')
        click('close-detail')
        for identity in ('filter-documentation', 'filter-model', 'filter-change', 'filter-condition',
                         'filter-note', 'filter-repetition'):
            select(identity, '')
        for status, expected in (('invalida',1),('falha',1),('desvio',1)):
            select('filter-status', status)
            assert js("document.getElementById('result-rows').children.length") == expected
        select('filter-status','')
        select('filter-rf','RF-02');select('filter-test','T04')
        assert js("document.getElementById('result-rows').children.length") > 0
        checks.append('Filtros de coorte/documentação/modelo/mudança/condição/nota/repetição/situação/RF/teste e detalhes separados.')
        select('filter-rf','');select('filter-test','')
        js("view('executar')")
        assert '57 respostas sintéticas' in js("document.getElementById('doc-continue').textContent")
        click('doc-continue')
        until(lambda: js('state.options.documental.pendentes===0&&!state.busy&&state.rows.length===144'), timeout=90)
        assert len(calls)==64
        assert js("document.getElementById('doc-run').disabled")
        js("view('resultados')")
        assert js("document.getElementById('result-rows').children.length") == 64
        cells = js('state.options.documental.celulas')
        assert len(cells)==32
        assert sum(c['N_valido'] for c in cells)==62
        assert sum(c['consistencia_descritiva_pendente']['requisitos']['numero_pares'] for c in cells)==30
        shot('06-consistencia-64.png')
        checks.append('Lote completo pela interface: 64 capturas artificiais; 62 válidas, uma inválida, uma falha, 32 células N=2 e 30 pares válidos por dimensão.')
        js("view('executar')")
        select('execution-mode','demonstracao')
        assert js("!document.getElementById('demo-config').classList.contains('hidden')")
        assert js("document.getElementById('documental-card').classList.contains('hidden')")
        select('condition','E0')
        click('preview')
        until(lambda: js("document.getElementById('preview-text').textContent.includes('<<<inicio:pedido>>>')"))
        assert '<<<inicio:notas>>>' not in js("document.getElementById('preview-text').textContent")
        assert len(calls)==64
        select('execution-mode','documental')
        def absent():
            raise ValueError('Chave fictícia retirada')
        app.chave=absent;app.documental.chave=absent
        click('doc-refresh')
        until(lambda: js('!state.options.chave_disponivel&&state.rows.length===144'))
        checks.append('Demonstração livre permanece separada; prévia E0 sem notas e retirada da chave não enviam chamadas.')
        cdp('Emulation.setDeviceMetricsOverride', {'width':390,'height':844,'deviceScaleFactor':1,'mobile':True})
        js("view('executar');window.scrollTo(0,0)")
        shot('05-executar-390.png')
        assert js('document.documentElement.scrollWidth<=window.innerWidth+1')
        assert len(calls)==64
        assert KEY not in js('document.documentElement.outerHTML')
        for p in run.rglob('*'):
            if p.is_file():
                assert KEY.encode() not in p.read_bytes(), str(p)
        checks.append('Sem credencial no navegador/arquivos. Tela estreita sem transbordamento horizontal da página.')
        logs = cdp('Runtime.evaluate', {'expression':'document.title','returnByValue':True})
        report = {'tipo':'VALIDACAO_SINTETICA_EM_CHROME_RENDERIZADO', 'chamadas_reais':0,
            'envios_artificiais':len(calls), 'checks':checks,
            'navegador':cdp('Browser.getVersion'), 'execucao':run.relative_to(ROOT).as_posix(),
            'pendentes':app.documental.estado()['pendentes'], 'inspecao_visual_assistente':'registrar após leitura dos PNGs; não é revisão humana de conformidade'}
        (AREA/'verificacao.json').write_bytes(api.bytes_json(report))
        print(json.dumps(report, ensure_ascii=False, indent=2))
    finally:
        if ws is not None:
            ws.close()
        if process is not None:
            process.terminate()
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                process.kill();process.wait(timeout=5)
        server.shutdown();server.server_close()
        try:
            temp.cleanup()
        except PermissionError:
            pass


def until(condition, timeout=35):
    deadline = time.monotonic()+timeout
    while time.monotonic() < deadline:
        if condition():
            return
        time.sleep(.1)
    raise AssertionError('Condição não atingida no navegador')


if __name__ == '__main__':
    main()
