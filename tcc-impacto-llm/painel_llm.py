"""Interface local para chamadas reais de demonstração, sem alterar as coortes.

O transporte e o cálculo são os existentes. Nenhuma chamada ao abrir a página.
Somente POST autenticado por token local e ação explícita inicia uma chamada.
"""
from __future__ import annotations

import copy
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import re
import secrets
from pathlib import Path
import threading
from urllib.parse import urlsplit
import uuid
import webbrowser

import apresentar as apoio
import coletor_api as api

ROOT = Path(__file__).resolve().parent
MODELS = ('gpt-6-sol', 'gpt-6-astra')
AUTHOR = 'Matheus Henrique Braun Nunes'
PLAN_HASHES = {'comparacao':'e00fd77c23e3b018cb3781e5ebee9b0d1b765e36e7c53fdf9eba8588e45c2e3e',
               'notas':'c8363eb2daaac2b1d1d1538470458356a29504cfc378d17cb35c2188d43dc1bd'}


class ErroPainel(ValueError):
    def __init__(self, message, code=400):
        super().__init__(message)
        self.code = code


def ler(path):
    return api.montagem._json(api.montagem.sem_links(Path(path)).read_bytes())


def perfis_preservados(root):
    """Só lê planos e requisições autorizadas; não abre a referência privada."""
    result = {}
    for cohort, (_, folder, _) in apoio.COHORTS.items():
        batch = apoio.arquivo(root, folder)
        plan_file = api.montagem.sem_links(batch / 'plano-original.json')
        if api.sha(plan_file.read_bytes()) != PLAN_HASHES[cohort]:
            raise ErroPainel('Plano de origem fora da versão preservada 0.3.')
        plan = ler(plan_file)
        for obs in plan['observacoes']:
            change, condition = obs['mudanca'], obs['condicao']
            note = obs.get('nota_id', 'original' if condition.endswith('1') else 'sem')
            identity = f'{change}:{condition}:{note}'
            source_id = obs['observacao_id']
            if not re.fullmatch(r'[A-Za-z0-9_-]+', source_id):
                raise ErroPainel('Identidade de origem inválida.')
            source = api.montagem.sem_links(batch / source_id / 'T01' / 'requisicao.json')
            raw = source.read_bytes()
            request = api.montagem._json(raw)
            if set(request) != {'input','model','reasoning','max_output_tokens','tools','tool_choice','store','stream'}:
                raise ErroPainel('Requisição de origem fora do contrato.')
            payload = request['input'].encode('utf-8')
            if api.sha(payload) != obs['payload_sha256'] or request['tools'] != [] or request['tool_choice'] != 'none':
                raise ErroPainel('Payload ou ferramentas divergentes da origem.')
            if request['reasoning'] != {'effort': 'medium'} or request['max_output_tokens'] != 4096:
                raise ErroPainel('Configuração de origem fora do recorte.')
            if identity in result:
                if result[identity]['payload'] != payload:
                    raise ErroPainel('Conteúdos distintos para o mesmo perfil.')
                continue
            result[identity] = {'id': identity, 'mudanca': change, 'condicao': condition,
                'nota_id': note, 'coorte_origem': cohort, 'payload': payload,
                'payload_sha256': obs['payload_sha256'], 'origem': source,
                'origem_sha256': api.sha(raw), 'referencia_sha256': plan['referencia_sha256']}
    return result


def avaliar_depois_da_captura(root, capture, assessed, record, expected_hash):
    """A referência só é aberta após o fechamento da captura, fora do input."""
    import avaliacao_ids as evaluator
    reference_file = apoio.arquivo(root, apoio.REFERENCE)
    reference_raw = reference_file.read_bytes()
    if api.sha(reference_raw) != expected_hash:
        raise ErroPainel('A captura foi preservada, mas a referência mudou; avaliação interrompida.')
    reference = evaluator.json_estrito(reference_raw)
    text_file = capture / 'resposta.bin'
    text = text_file.read_bytes() if text_file.exists() else b''
    result = evaluator.avaliar_resposta(text, reference, record['mudanca'], record['estado_tecnico'])
    result.update(tipo='demonstracao_interface', origem=record['origem'], fase=record['fase'],
        incluida_pesquisa=False, observacao_id=record['observacao_id'], nota_id=record['nota_id'],
        modelo_solicitado=record['modelo_solicitado'], referencia_sha256=expected_hash,
        conformidade_protocolo='pendente')
    api.salvar_json(assessed / 'avaliacao.json', result)
    if text_file.exists():
        api.salvar(assessed / 'resposta-original.bin', text)
    api.salvar_json(assessed / 'fechamento.json', {'arquivos': api.base.inventariar(assessed),
        'captura_resultado_sha256': api.sha((capture / 'resultado.json').read_bytes()),
        'referencia_sha256': expected_hash, 'avaliador_sha256': api.sha(Path(evaluator.__file__).read_bytes())})
    return result


class Aplicacao:
    def __init__(self, root=ROOT, sender=None, chave=None, origem='real', area_captura=None, area_avaliacao=None):
        self.root = Path(root).resolve()
        self.sender = sender or api.enviar
        self.chave = chave or api.chave_api
        self.origem = origem
        self.capture_root = api.montagem.sem_links(area_captura or self.root / 'captura/demonstracoes-painel')
        self.assessed_root = api.montagem.sem_links(area_avaliacao or self.root / 'avaliados/demonstracoes-painel')
        self.profiles = perfis_preservados(self.root)
        self.token = secrets.token_urlsafe(32)
        self.lock = threading.RLock()
        self.jobs, self.clicks, self.worker = {}, {}, None
        self._history = None
        self._recuperar()

    def _recuperar(self):
        if not self.capture_root.exists():
            return
        for folder in self.capture_root.iterdir():
            api.montagem.sem_links(folder)
            if not folder.is_dir() or not re.fullmatch(r'DEMO-[A-Za-z0-9-]+', folder.name):
                continue
            initial = folder / 'inicio.json'
            if not initial.exists():
                continue
            info = ler(initial)
            self.clicks[info['acao_id']] = {'id': folder.name, 'modelo': info['modelo_solicitado'], 'perfil_id': info['perfil_id']}
            # Um início interrompido nunca é reenviado ao reiniciar o painel.
            self.jobs[folder.name] = {'id': folder.name, 'etapa': 'encerrada', 'finalizado': True,
                'mensagem': 'Registro preservado de outra sessão; consulte os detalhes. Sem reenvio automático.'}

    def chave_pronta(self):
        try:
            self.chave()
            return True
        except (ValueError, KeyError):
            return False

    def opcoes(self):
        with self.lock:
            current = next((copy.deepcopy(j) for j in self.jobs.values() if not j['finalizado']), None)
        return {'modelos': list(MODELS), 'perfis': [
            {k:p[k] for k in ('id','mudanca','condicao','nota_id')} for p in self.profiles.values()],
            'chave_disponivel': self.chave_pronta(), 'job_atual': current, 'modo': self.origem,
            'esforco': 'medium', 'limite_saida': 4096}

    def perfil(self, identity):
        if identity not in self.profiles:
            raise ErroPainel('Perfil não encontrado.', 404)
        p = self.profiles[identity]
        return {'id': identity, 'payload': p['payload'].decode('utf-8'), 'sha256': p['payload_sha256']}

    def iniciar(self, choice):
        if not isinstance(choice, dict) or set(choice) != {'modelo','perfil_id','acao_id'}:
            raise ErroPainel('Seleção inválida: use somente modelo, perfil e identificador da ação.')
        model, profile_id, click = choice['modelo'], choice['perfil_id'], choice['acao_id']
        if not all(isinstance(v,str) for v in (model,profile_id,click)):
            raise ErroPainel('Campos da seleção devem ser textos.')
        if model not in MODELS or profile_id not in self.profiles:
            raise ErroPainel('Modelo ou combinação não permitida.')
        if not isinstance(click, str) or not re.fullmatch(r'[A-Za-z0-9_-]{12,80}', click):
            raise ErroPainel('Identificador da ação inválido.')
        with self.lock:
            if click in self.clicks:
                existing = self.clicks[click]
                if (existing['modelo'], existing['perfil_id']) != (model, profile_id):
                    raise ErroPainel('Ação já usada com outra seleção.', 409)
                return copy.deepcopy(self.jobs[existing['id']])
            if any(not job['finalizado'] for job in self.jobs.values()):
                raise ErroPainel('Já há uma chamada em andamento. Aguarde a conclusão.', 409)
            try:
                key = self.chave()
            except (ValueError, KeyError):
                raise ErroPainel('Configure OPENAI_API_KEY no terminal e reinicie o painel. A chave não é informada na página.') from None
            profile = self.profiles[profile_id]
            if api.sha(api.montagem.sem_links(profile['origem']).read_bytes()) != profile['origem_sha256']:
                raise ErroPainel('A requisição de origem mudou. Reinicie e confira os materiais.')
            identity = 'DEMO-' + datetime.now().strftime('%Y%m%dT%H%M%S') + '-' + uuid.uuid4().hex[:12]
            job = {'id': identity, 'etapa': 'preparando', 'finalizado': False,
                'mensagem': 'Preparando o pacote autorizado.', 'eventos': []}
            self.jobs[identity] = job
            self.clicks[click] = {'id': identity, 'modelo': model, 'perfil_id': profile_id}
            self.worker = threading.Thread(target=self._executar, args=(identity, choice.copy(), key), daemon=False)
            self.worker.start()
            return copy.deepcopy(job)

    def _etapa(self, identity, name, message, done=False):
        with self.lock:
            job = self.jobs[identity]
            job.update(etapa=name, mensagem=message, finalizado=done)
            job['eventos'].append({'etapa': name, 'instante': api.agora()})

    def _executar(self, identity, choice, key):
        capture = self.capture_root / identity
        assessed = self.assessed_root / identity
        sent = False
        try:
            profile = self.profiles[choice['perfil_id']]
            config = {'modelo_solicitado': choice['modelo'], 'esforco_solicitado': 'medium',
                'max_output_tokens': 4096, 'timeout_segundos': 120, 'endpoint':api.ENDPOINT,
                'tools':[], 'tool_choice':'none', 'store':False, 'stream':False, 'retries_automaticos_cliente':0}
            payload = profile['payload']
            body = api.requisicao(payload, config)
            api.montagem.sem_links(capture)
            capture.mkdir(parents=True, exist_ok=False)
            initial = {'observacao_id': identity, 'perfil_id': profile['id'], 'acao_id': choice['acao_id'],
                'modelo_solicitado': choice['modelo'], 'mudanca': profile['mudanca'],
                'condicao': profile['condicao'], 'nota_id': profile['nota_id'],
                'origem': self.origem, 'fase': 'demonstracao' if self.origem == 'real' else 'verificacao_sintetica',
                'incluida_pesquisa': False, 'instante': api.agora(), 'configuracao':config,
                'payload_sha256': api.sha(payload), 'requisicao_sha256': api.sha(body),
                'referencia_sha256': profile['referencia_sha256'],
                'autorizacao': {'origem': 'clique_explicito_na_interface_local',
                    'responsavel_informado': AUTHOR, 'uma_chamada': True, 'orcamento_declarado_usd': None,
                    'credenciais_persistidas': False},
                'fontes_sha256': {'painel_llm.py': api.sha(Path(__file__).read_bytes()),
                    'coletor_api.py': api.sha(Path(api.__file__).read_bytes()),
                    'requisicao_origem': profile['origem_sha256']}}
            api.salvar_json(capture / 'inicio.json', initial)
            api.salvar(capture / 'entrada.bin', payload)
            api.guardar_requisicao(capture, body)
            self._etapa(identity, 'enviando', 'Aguardando a resposta do modelo. Uma chamada, sem reenvio automático.')
            sent = True
            status, raw, request_id, failure = api.obter_http(self.sender, body, key, 120)
            api.guardar_http(capture, status, raw, request_id, failure)
            parsed = api.falha_interpretada(failure) if failure else api.interpretar(raw, status, config)
            if parsed['texto'] is not None:
                api.salvar(capture / 'resposta.bin', parsed['texto'])
            record = {**initial, 'estado_tecnico': 'concluida' if parsed['concluida'] else 'falha_tecnica',
                'instante_fim': api.agora(), 'http_status': status, 'request_id': request_id,
                'response_id': parsed['response_id'], 'modelo_reportado': parsed['modelo_reportado'],
                'usage': parsed['usage'], 'desvios': parsed['desvios'], 'causa': parsed['causa'],
                'falha_transporte': failure, 'estado_remoto': 'desconhecido' if failure else 'resposta_http_recebida',
                'retentativas_cliente': 0, 'conformidade_protocolo': 'pendente',
                'resposta_sha256': api.sha(parsed['texto']) if parsed['texto'] is not None else None}
            api.salvar_json(capture / 'resultado.json', record)
            api.salvar_json(capture / 'fechamento.json', {'arquivos': api.base.inventariar(capture)})
            self._etapa(identity, 'avaliando', 'Resposta preservada. Comparando os IDs offline com a referência.')
            result = avaliar_depois_da_captura(self.root, capture, assessed, record, profile['referencia_sha256'])
            if failure or not parsed['concluida']:
                message = 'Falha técnica registrada. Originais preservados; sem reenvio automático.'
            elif result['status_avaliacao'] != 'avaliada':
                message = 'Resposta recebida, mas o formato não é válido. O original foi preservado.'
            elif parsed['desvios']:
                message = 'Resposta avaliada com desvio técnico reportado; confira os detalhes.'
            else:
                message = 'Chamada concluída e avaliada. Resultado disponível.'
            self._etapa(identity, 'concluida', message, True)
        except Exception as error:
            # Nunca serializar str(error) de transporte: pode conter dados sensíveis.
            message = str(error) if isinstance(error, ErroPainel) else 'Falha de execução (' + type(error).__name__ + '). Consulte os arquivos preservados.'
            if capture.exists():
                api.salvar_json(capture / 'erro-painel.json', {'tipo': type(error).__name__,
                    'mensagem': message, 'envio_iniciado': sent, 'estado_remoto': 'desconhecido' if sent else 'nao_enviado',
                    'retentativas_automaticas': 0, 'instante': api.agora()})
            self._etapa(identity, 'falha', message, True)

    def job(self, identity):
        with self.lock:
            if identity not in self.jobs:
                raise ErroPainel('Execução não encontrada.', 404)
            return copy.deepcopy(self.jobs[identity])

    def _historico(self):
        if self._history is None:
            self._history = apoio.ler_capturas(self.root)[0]
            for record in self._history:
                record['origem'] = 'real'
                record['modelo_reportado'] = record['modelo']
                record['nota'] = record.get('nota') or ('original' if record['condicao'].endswith('1') else 'sem')
        return self._history

    def _demo(self, identity):
        folder = api.montagem.sem_links(self.capture_root / identity)
        initial = ler(folder / 'inicio.json')
        result_file = folder / 'resultado.json'
        record = ler(result_file) if result_file.exists() else initial
        assessment = self.assessed_root / identity / 'avaliacao.json'
        evaluation = ler(assessment) if assessment.exists() else {}
        response = folder / 'resposta.bin'
        error_file = folder / 'erro-painel.json'
        cause = record.get('causa') or (ler(error_file)['mensagem'] if error_file.exists() else None)
        return {'coorte': 'demonstracao', 'id': identity, 'modelo': initial['modelo_solicitado'],
            'modelo_reportado': record.get('modelo_reportado'), 'mudanca': initial['mudanca'],
            'condicao': initial['condicao'], 'nota': initial['nota_id'], 'repeticao': None,
            'instante': initial['instante'], 'estado': record.get('estado_tecnico','interrompida'),
            'conformidade_original': 'pendente', 'origem': initial['origem'],
            'payload': (folder / 'entrada.bin').read_text(encoding='utf-8'),
            'resposta': response.read_text(encoding='utf-8') if response.exists() else '',
            'requisitos': evaluation.get('requisitos'), 'testes': evaluation.get('testes'),
            'formato': evaluation.get('formato_contrato','indisponivel'), 'tokens': record.get('usage'),
            'causa': cause, 'desvios': record.get('desvios',[]), 'estado_remoto': record.get('estado_remoto','desconhecido'),
            'http_status': record.get('http_status'), 'request_id': record.get('request_id'),
            'response_id': record.get('response_id'), 'payload_sha256': record.get('payload_sha256'),
            'resposta_sha256': record.get('resposta_sha256'), 'fase': initial['fase'], 'configuracao':initial['configuracao'],
            'pasta': folder.as_uri(), 'avaliacao': assessment.as_uri()}

    def _todos(self):
        records = list(self._historico())
        with self.lock:
            identities = [identity for identity,job in self.jobs.items() if job['finalizado']]
        for identity in identities:
            folder = self.capture_root / identity
            if (folder / 'inicio.json').exists() and (folder / 'entrada.bin').exists():
                records.append(self._demo(identity))
        return sorted(records, key=lambda r:r['instante'], reverse=True)

    def resultados(self):
        fields = ('coorte','id','modelo','modelo_reportado','mudanca','condicao','nota','repeticao',
                  'instante','estado','formato','causa','origem','desvios')
        rows = []
        for record in self._todos():
            row = {k:record.get(k) for k in fields}
            for dim in ('requisitos','testes'):
                result = record.get(dim)
                row[dim] = None if not result else {k:result.get(k) for k in ('TP','FP','FN')}
                if result:
                    row[dim]['esperados'] = len(result['G'])
                    row[dim]['ids_esperados'] = result['G']
                    row[dim]['ids_selecionados'] = result['S']
                    row[dim]['exata'] = result['metricas_propostas']['correspondencia_exata'] == 1
            rows.append(row)
        return rows

    def detalhe(self, identity):
        record = next((r for r in self._todos() if r['id'] == identity), None)
        if record is None:
            raise ErroPainel('Observação não encontrada.', 404)
        reference_path = apoio.arquivo(self.root, apoio.REFERENCE)
        if api.sha(reference_path.read_bytes()) != next(iter(self.profiles.values()))['referencia_sha256']:
            raise ErroPainel('Referência atual fora da versão 0.3; não exibir comparação com outra versão.')
        reference = ler(reference_path)
        change = next(c for c in reference['mudancas'] if c['id'] == record['mudanca'])
        return {**record, 'mudanca_texto': change['text'], 'casos': reference['catalogo'],
                'esperado_requisitos':change['rfs'], 'esperado_testes':change['tests'],
                'mudaram': change['changed'], 'preservaram': change['preserved'],
                'regras': {'RF-01':'Estado da conta','RF-02':'Permissões diretas',
                           'RF-03':'Herança entre papéis','RF-04':'Incompatibilidade entre papéis'}}

    def pasta(self, identity, side):
        if side not in ('captura','avaliacao'):
            raise ErroPainel('Pasta não permitida.')
        record = next((r for r in self._todos() if r['id'] == identity), None)
        if record is None:
            raise ErroPainel('Observação não encontrada.', 404)
        if record['coorte'] == 'demonstracao':
            path = (self.capture_root if side == 'captura' else self.assessed_root) / identity
        else:
            config = apoio.COHORTS[record['coorte']]
            path = apoio.arquivo(self.root, config[1 if side == 'captura' else 2]) / identity / 'T01'
        if not path.is_dir():
            raise ErroPainel('A pasta ainda não foi criada.')
        apoio.abrir_pasta(path)


def handler(app):
    class Handler(BaseHTTPRequestHandler):
        server_version = 'TCC-Local/2'

        def log_message(self, *_):
            pass

        def _guard(self, protected=True):
            expected = f'127.0.0.1:{self.server.server_address[1]}'
            if self.headers.get('Host') != expected:
                raise ErroPainel('Host local inválido.', 403)
            origin = self.headers.get('Origin')
            if origin not in (None, 'http://' + expected) or self.headers.get('Sec-Fetch-Site') == 'cross-site':
                raise ErroPainel('Origem não permitida.', 403)
            if protected and not secrets.compare_digest(self.headers.get('X-TCC-Token',''), app.token):
                raise ErroPainel('Sessão local inválida; recarregue o painel.', 403)

        def _reply(self, data, status=200, kind='application/json; charset=utf-8'):
            raw = data if isinstance(data, bytes) else api.bytes_json(data)
            self.send_response(status)
            for k,v in {'Content-Type':kind,'Content-Length':str(len(raw)),'Cache-Control':'no-store',
                'X-Content-Type-Options':'nosniff','Referrer-Policy':'no-referrer',
                'Content-Security-Policy':"default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; connect-src 'self'; frame-ancestors 'none'; base-uri 'none'"}.items():
                self.send_header(k,v)
            self.end_headers()
            self.wfile.write(raw)

        def do_GET(self):
            try:
                path = urlsplit(self.path).path
                self._guard(path != '/')
                if path == '/':
                    html = (app.root / 'apresentacao/interface.html').read_text(encoding='utf-8')
                    self._reply(html.replace('__TOKEN_TCC__', json.dumps(app.token)).encode('utf-8'), kind='text/html; charset=utf-8')
                elif path == '/api/opcoes': self._reply(app.opcoes())
                elif path == '/api/resultados': self._reply(app.resultados())
                elif path.startswith('/api/perfil/'):
                    from urllib.parse import unquote
                    self._reply(app.perfil(unquote(path.removeprefix('/api/perfil/'))))
                elif path.startswith('/api/job/'): self._reply(app.job(path.removeprefix('/api/job/')))
                elif path.startswith('/api/resultado/'): self._reply(app.detalhe(path.removeprefix('/api/resultado/')))
                else: raise ErroPainel('Recurso não encontrado.',404)
            except ErroPainel as error: self._reply({'erro':str(error)},error.code)
            except Exception: self._reply({'erro':'Falha ao ler os registros. Confira os arquivos locais.'},500)

        def do_POST(self):
            try:
                self._guard()
                if self.headers.get('Content-Type','').split(';')[0] != 'application/json':
                    raise ErroPainel('JSON obrigatório.',415)
                size = int(self.headers.get('Content-Length','0'))
                if not 0 < size <= 2048: raise ErroPainel('Tamanho de solicitação inválido.',413)
                data = api.montagem._json(self.rfile.read(size))
                if self.path == '/api/executar': self._reply(app.iniciar(data),202)
                elif self.path == '/api/abrir-pasta':
                    if not isinstance(data,dict) or set(data) != {'id','lado'}: raise ErroPainel('Pasta não permitida.')
                    app.pasta(data['id'],data['lado']);self._reply({'aberta':True})
                else: raise ErroPainel('Ação não encontrada.',404)
            except ErroPainel as error: self._reply({'erro':str(error)},error.code)
            except (ValueError,TypeError,KeyError): self._reply({'erro':'Solicitação inválida.'},400)
            except Exception: self._reply({'erro':'Falha local; não reenvie automaticamente.'},500)

        def do_OPTIONS(self):
            self._reply({'erro':'Requisição entre origens não permitida.'},403)
    return Handler


def servir(root=ROOT, porta=8765, sem_abrir=False, app=None):
    app = app or Aplicacao(root)
    server = ThreadingHTTPServer(('127.0.0.1',porta),handler(app))
    url = 'http://127.0.0.1:' + str(server.server_address[1]) + '/'
    print('Painel local:',url,flush=True)
    print('Nenhuma chamada foi enviada. Use Executar na interface. Ctrl+C encerra o painel.',flush=True)
    if not sem_abrir:
        webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\nPainel encerrado. Uma chamada já iniciada conserva seus registros ao terminar.')
    finally:
        server.server_close()


if __name__ == '__main__':
    servir()
