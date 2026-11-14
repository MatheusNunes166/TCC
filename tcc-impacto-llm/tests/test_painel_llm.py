"""Interface local: HTTP e respostas artificiais; nenhum envio à OpenAI."""
import json
from pathlib import Path
import tempfile
import threading
import unittest
from unittest.mock import patch
import urllib.error
import urllib.request

import painel_llm as painel


KEY = 'CREDENCIAL-ARTIFICIAL-NAO-PERSISTIR'
TEXT = '{"requisitos":["RF-02"],"testes":["T04","T12","T14","T15"]}'


def envelope(text=TEXT, model='gpt-6-sol', **extras):
    return painel.api.bytes_json({'id':'resp-artificial','model':model,'status':'completed',
        'tools':[], 'tool_choice':'none', 'usage':{'input_tokens':8,'output_tokens':9},
        'output':[{'type':'message','role':'assistant','status':'completed',
                   'content':[{'type':'output_text','text':text}]}], **extras})


class TestPainelLLM(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.area = Path(self.tmp.name)
        self.calls = []
        self.no_network = patch.object(painel.api, 'enviar', side_effect=AssertionError('rede real proibida'))
        self.no_network.start()
        self.addCleanup(self.no_network.stop)

    def sender(self, body, key, timeout):
        self.calls.append((body,key,timeout))
        return 200,envelope(model=json.loads(body)['model']),'req-artificial'

    def app(self, sender=None, chave=None):
        return painel.Aplicacao(sender=sender or self.sender, chave=chave or (lambda:KEY),
            origem='sintetica', area_captura=self.area/'captura', area_avaliacao=self.area/'avaliados')

    def choice(self, **extras):
        return {'modelo':'gpt-6-sol','perfil_id':'MC-01:D0:sem','acao_id':'clique-artificial-001',**extras}

    def finish(self, app, job):
        app.worker.join(5)
        self.assertFalse(app.worker.is_alive())
        value = app.job(job['id'])
        self.assertTrue(value['finalizado'])
        self.assertEqual(value['etapa'],'concluida', value)
        return app.detalhe(job['id'])

    def test_leitura_das_coortes_e_preview_sem_chamada(self):
        app=self.app()
        self.assertEqual(len(app.opcoes()['perfis']),20)
        self.assertEqual(len(app.resultados()),80)
        self.assertEqual({r['coorte'] for r in app.resultados()},{'comparacao','notas'})
        self.assertIn('<<<inicio:sistema>>>', app.perfil('MC-01:D0:sem')['payload'])
        self.assertEqual(self.calls,[])
        self.assertFalse((self.area/'captura').exists())

    def test_envio_uma_vez_e_avaliacao_somente_apos_captura(self):
        app=self.app()
        original=painel.avaliar_depois_da_captura
        def evaluate(root,capture,*args):
            self.assertTrue((capture/'fechamento.json').is_file())
            self.assertTrue((capture/'resposta.bin').is_file())
            self.assertEqual(len(self.calls),1)
            return original(root,capture,*args)
        with patch.object(painel,'avaliar_depois_da_captura',side_effect=evaluate):
            job=app.iniciar(self.choice()); record=self.finish(app,job)
        self.assertEqual(len(self.calls),1)
        body,key,timeout=self.calls[0]; request=json.loads(body)
        self.assertEqual(set(request),{'model','input','reasoning','max_output_tokens','tools','tool_choice','store','stream'})
        self.assertEqual(request['input'],app.perfil('MC-01:D0:sem')['payload'])
        self.assertEqual(request['tools'],[])
        self.assertEqual(request['tool_choice'],'none')
        self.assertEqual(request['reasoning'],{'effort':'medium'})
        self.assertEqual((timeout,request['max_output_tokens']),(120,4096))
        self.assertFalse(request['store']);self.assertFalse(request['stream'])
        self.assertEqual((record['coorte'],record['origem']),('demonstracao','sintetica'))
        self.assertEqual(record['conformidade_original'],'pendente')
        self.assertEqual(record['testes']['TP'],4)
        self.assertEqual(record['testes']['FP'],0)
        for path in self.area.rglob('*'):
            if path.is_file(): self.assertNotIn(KEY.encode(),path.read_bytes(),str(path))

    def test_acoes_repetidas_e_concorrentes_nao_reenviam(self):
        entered,release=threading.Event(),threading.Event()
        def blocked(*args):
            entered.set();release.wait(5);return self.sender(*args)
        app=self.app(sender=blocked)
        job=app.iniciar(self.choice())
        try:
            self.assertTrue(entered.wait(2))
            self.assertEqual(app.iniciar(self.choice())['id'],job['id'])
            with self.assertRaisesRegex(painel.ErroPainel,'andamento'):
                app.iniciar(self.choice(acao_id='clique-artificial-002'))
            with self.assertRaisesRegex(painel.ErroPainel,'outra seleção'):
                app.iniciar(self.choice(modelo='gpt-6-astra'))
        finally: release.set()
        self.finish(app,job)
        self.assertEqual(app.iniciar(self.choice())['id'],job['id'])
        self.assertEqual(len(self.calls),1)

    def test_recusa_modelo_conteudo_adicional_e_chave_ausente(self):
        app=self.app()
        for value in (self.choice(modelo='arbitrario'),self.choice(perfil_id='../../fora'),
                      self.choice(input='gabarito'),self.choice(acao_id='curto')):
            with self.assertRaises(painel.ErroPainel): app.iniciar(value)
        def absent(): raise ValueError('sem chave')
        app=self.app(chave=absent)
        self.assertFalse(app.opcoes()['chave_disponivel'])
        with self.assertRaisesRegex(painel.ErroPainel,'OPENAI_API_KEY'): app.iniciar(self.choice())
        self.assertFalse(self.calls)

    def test_fragmento_preservado_sem_metricas_ou_retry(self):
        def failed(*args):
            self.calls.append(args)
            raise painel.api.FalhaTransporte('IncompleteRead',partial=b'fragmento artificial',status=200)
        app=self.app(sender=failed);job=app.iniciar(self.choice());record=self.finish(app,job)
        self.assertEqual(record['estado_remoto'],'desconhecido')
        self.assertIsNone(record['requisitos']);self.assertIsNone(record['testes'])
        self.assertEqual((app.capture_root/job['id']/'resposta-http-parcial.bin').read_bytes(),b'fragmento artificial')
        self.assertEqual(len(self.calls),1)

    def test_resposta_invalida_nao_e_reparada_ou_imputada(self):
        text='```json\n{"requisitos":[],"testes":[]}\n```'
        app=self.app(sender=lambda *args:(200,envelope(text),'req-artificial'))
        record=self.finish(app,app.iniciar(self.choice()))
        self.assertEqual(record['resposta'],text)
        self.assertEqual(record['formato'],'invalido')
        self.assertIsNone(record['requisitos'])

    def test_modelo_reportado_divergente_preservado(self):
        app=self.app(sender=lambda *args:(200,envelope(model='modelo-diferente'),'req-artificial'))
        record=self.finish(app,app.iniciar(self.choice()))
        self.assertEqual(record['modelo_reportado'],'modelo-diferente')
        self.assertTrue(record['desvios'])

    def test_nota_e_modelo_selecionados_chegam_ao_envio(self):
        app=self.app();choice=self.choice(modelo='gpt-6-astra',perfil_id='MC-04-v2:E1:N02')
        record=self.finish(app,app.iniciar(choice))
        self.assertEqual(record['nota'],'N02')
        body=json.loads(self.calls[0][0]);self.assertEqual(body['model'],'gpt-6-astra')
        self.assertIn('nunca altera um conflito',body['input'])
        self.assertNotIn('rótulo privado',body['input'])

    def test_reinicio_nao_reenvia_registro_interrompido(self):
        app=self.app();job=app.iniciar(self.choice());self.finish(app,job)
        (app.capture_root/job['id']/'resultado.json').unlink()
        again=self.app()
        self.assertTrue(again.iniciar(self.choice())['finalizado'])
        self.assertEqual(len(self.calls),1)
        self.assertEqual(again.detalhe(job['id'])['estado'],'interrompida')

    def test_falha_de_avaliacao_preserva_original(self):
        app=self.app()
        with patch.object(painel,'avaliar_depois_da_captura',side_effect=painel.ErroPainel('Referência mudou')):
            job=app.iniciar(self.choice());app.worker.join(5)
        self.assertEqual(app.job(job['id'])['etapa'],'falha')
        self.assertTrue((app.capture_root/job['id']/'resposta-http.bin').is_file())
        self.assertIsNone(app.detalhe(job['id'])['requisitos'])
        self.assertEqual(len(self.calls),1)

    def test_http_local_protege_execucao_e_serve_interface(self):
        app=self.app()
        server=painel.ThreadingHTTPServer(('127.0.0.1',0),painel.handler(app))
        thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
        def shutdown():
            server.shutdown();server.server_close();thread.join(3)
        self.addCleanup(shutdown)
        url='http://127.0.0.1:'+str(server.server_address[1])
        def get(path,headers=None,data=None):
            req=urllib.request.Request(url+path,data=data,headers=headers or {})
            return urllib.request.urlopen(req,timeout=5)
        with get('/') as response:
            html=response.read().decode()
            self.assertIn('Executar chamada real',html)
            self.assertNotIn('__TOKEN_TCC__',html)
            self.assertNotIn(KEY,html)
        with self.assertRaises(urllib.error.HTTPError) as bad: get('/api/opcoes')
        self.assertEqual(bad.exception.code,403)
        headers={'X-TCC-Token':app.token,'Content-Type':'application/json'}
        with get('/api/opcoes',headers) as response:
            self.assertEqual(len(json.load(response)['perfis']),20)
        for extra in ({'Origin':'https://externo.invalid'},{'Host':'externo.invalid'}):
            with self.assertRaises(urllib.error.HTTPError) as bad:
                get('/api/opcoes',{**headers,**extra})
            self.assertEqual(bad.exception.code,403)
        with self.assertRaises(urllib.error.HTTPError) as bad:
            get('/api/executar',headers,painel.api.bytes_json(self.choice(input='extra')))
        self.assertEqual(bad.exception.code,400)
        self.assertEqual(len(self.calls),0)
        with get('/api/executar',headers,painel.api.bytes_json(self.choice())) as response:
            self.assertEqual(response.status,202);job=json.load(response)
        self.finish(app,job)
        with get('/api/resultado/'+job['id'],headers) as response:
            self.assertEqual(json.load(response)['coorte'],'demonstracao')
        self.assertEqual(len(self.calls),1)

    def test_abrir_somente_pastas_de_registros_conhecidos(self):
        app=self.app();identity=app.resultados()[0]['id']
        with patch.object(painel.apoio,'abrir_pasta') as opening:
            app.pasta(identity,'captura')
            self.assertTrue(opening.call_args.args[0].is_dir())
            with self.assertRaises(painel.ErroPainel): app.pasta('../../fora','captura')
            with self.assertRaises(painel.ErroPainel): app.pasta(identity,'../../fora')
            self.assertEqual(opening.call_count,1)


if __name__ == '__main__':
    unittest.main()
