"""Coleta pela Responses API. Preparar/simular/controle sao offline; iniciar exige --enviar-real.

Biblioteca padrao, HTTPS verificado, sem ferramentas, conversa anterior ou retries
automaticos. A chave e lida apenas de OPENAI_API_KEY no inicio de uma coleta real.
Nao importa o avaliador nem abre o gabarito durante a captura.
"""
import argparse
import http.client
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
import json
import os
from pathlib import Path
import ssl
import urllib.error
import urllib.request
import uuid

import coletor_piloto as base
import montagem_entradas as montagem

VERSAO = 'coletor-responses-v1.4-D47'
ENDPOINT = 'https://api.openai.com/v1/responses'
MODELO = 'gpt-6-sol'
MIN_OUTPUT_TOKENS = 16  # Restricao de formato da API, nao escolha do piloto.


def sha(data):
    return montagem.sha(data)


def bytes_json(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + '\n').encode('utf-8')


def agora():
    return datetime.now(timezone.utc).isoformat()


def chave_api():
    key = os.environ.get('OPENAI_API_KEY', '')
    if not key or key != key.strip() or any(not 33 <= ord(c) <= 126 for c in key):
        raise ValueError('OPENAI_API_KEY ausente ou malformada; nao informar chave no chat')
    return key


def salvar(path, value):
    path = montagem.sem_links(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('xb') as stream:
        stream.write(value)


def salvar_json(path, value):
    salvar(path, bytes_json(value))


def requisicao(payload, config):
    text = payload.decode('utf-8')
    if payload.startswith(b'\xef\xbb\xbf') or b'\r' in payload:
        raise ValueError('entrada deve preservar a politica UTF-8 sem BOM/LF')
    return bytes_json({'model': config['modelo_solicitado'], 'input': text,
                       'reasoning': {'effort': config['esforco_solicitado']},
                       'max_output_tokens': config['max_output_tokens'],
                       'tools': [], 'tool_choice': 'none', 'store': False, 'stream': False})


class SemRedirecionar(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


class FalhaTransporte(Exception):
    """Metadados seguros; nunca armazena str(exc), request ou Authorization."""
    def __init__(self, tipo, partial=b'', status=None, request_id=None, interrompida=False):
        super().__init__(tipo)
        self.tipo, self.partial = tipo, partial
        self.status, self.request_id = status, request_id
        self.interrompida = interrompida


def _parcial(error):
    value = getattr(error, 'partial', None)
    return value if isinstance(value, bytes) else b''


def headers_publicos(body):
    return {'Content-Type': 'application/json', 'Accept': 'application/json',
            'Content-Length': str(len(body)), 'Host': 'api.openai.com',
            'User-Agent': 'tcc-coletor-responses/1.1', 'Accept-Encoding': 'identity',
            'Connection': 'close'}


def enviar(body, key, timeout):
    """Uma tentativa HTTP; nunca persiste Authorization e nunca segue redirect."""
    req = urllib.request.Request(ENDPOINT, data=body, method='POST', headers={
        **headers_publicos(body), 'Authorization': 'Bearer ' + key})
    # Sem proxy herdado, auth handlers ou loop de retries. Certificados e nome
    # do host sao verificados pelo contexto padrao; redirects sao recusados.
    context = ssl.create_default_context()
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}),
                urllib.request.HTTPSHandler(context=context), SemRedirecionar())
    response = None
    chunks = []
    status, request_id = None, None
    try:
        try:
            response = opener.open(req, timeout=timeout)
        except urllib.error.HTTPError as error:
            response = error  # Corpo de HTTP 3xx/4xx/5xx tambem e evidencia.
        status = response.code if isinstance(response, urllib.error.HTTPError) else response.status
        request_id = response.headers.get('x-request-id')
        while True:
            chunk = response.read(65536)
            if not chunk:
                break
            chunks.append(chunk)
        raw = b''.join(chunks)
        length = response.headers.get('Content-Length')
        if length and length.isdecimal() and len(raw) < int(length):
            # read(amt) pode chegar a EOF sem levantar IncompleteRead por si.
            raise FalhaTransporte('IncompleteRead', raw, status, request_id)
        return status, raw, request_id
    except (http.client.HTTPException, OSError) as error:
        raise FalhaTransporte(type(error).__name__, b''.join(chunks) + _parcial(error),
                              status, request_id) from None
    except KeyboardInterrupt as error:
        raise FalhaTransporte('KeyboardInterrupt', b''.join(chunks) + _parcial(error),
                              status, request_id, interrompida=True) from None
    finally:
        if response is not None:
            response.close()


def obter_http(sender, body, key, timeout):
    """Captura so falhas de transporte/interrupcao, inclusive sender simulado."""
    try:
        status, raw, request_id = sender(body, key, timeout)
        return status, raw, request_id, None
    except FalhaTransporte as error:
        return error.status, error.partial, error.request_id, {
            'tipo': error.tipo, 'estado_remoto': 'desconhecido',
            'interrompida': error.interrompida, 'retentativas_automaticas': 0}
    except (http.client.HTTPException, OSError, KeyboardInterrupt) as error:
        return None, _parcial(error), None, {
            'tipo': type(error).__name__, 'estado_remoto': 'desconhecido',
            'interrompida': isinstance(error, KeyboardInterrupt), 'retentativas_automaticas': 0}


def guardar_http(out, status, raw, request_id, failure):
    salvar(out / ('resposta-http-parcial.bin' if failure else 'resposta-http.bin'), raw)
    salvar_json(out / 'transporte.json', {'http_status': status, 'request_id': request_id,
        'corpo_sha256': sha(raw), 'corpo_tamanho': len(raw), 'falha': failure,
        'retentativas_cliente': 0})


def falha_interpretada(failure):
    return {'concluida': False, 'texto': None, 'modelo_reportado': None,
            'response_id': None, 'usage': None, 'desvios': [],
            'causa': failure['tipo'] + '; estado remoto desconhecido; nao reenviar'}


def guardar_requisicao(out, body):
    salvar(out / 'requisicao.json', body)
    salvar_json(out / 'http-requisicao.json', {'metodo': 'POST', 'url': ENDPOINT,
        'headers': headers_publicos(body), 'corpo_arquivo': 'requisicao.json',
        'corpo_sha256': sha(body), 'corpo_tamanho': len(body)})


def interpretar(raw, http_status, config):
    """Preserva texto do assistente, inclusive recusa, cercas e JSON invalido."""
    result = {'concluida': False, 'texto': None, 'modelo_reportado': None,
              'response_id': None, 'usage': None, 'desvios': [], 'causa': None}
    if not 200 <= http_status < 300:
        result['causa'] = 'HTTP ' + str(http_status) + '; original preservado; sem retry automatico'
        return result
    try:
        data = montagem._json(raw)
        if not isinstance(data, dict) or not isinstance(data.get('output'), list):
            raise ValueError('envelope sem output')
        result.update(modelo_reportado=data.get('model'), response_id=data.get('id'), usage=data.get('usage'))
        messages = []
        for item in data['output']:
            if not isinstance(item, dict):
                raise ValueError('item de output invalido')
            if item.get('type') == 'reasoning':
                continue
            if item.get('type') != 'message' or item.get('role') != 'assistant':
                result['desvios'].append('output contem item adicional: ' + str(item.get('type')))
                continue
            parts = []
            content_list = item.get('content')
            if not isinstance(content_list, list) or any(not isinstance(part, dict) for part in content_list):
                raise ValueError('content deve ser lista de objetos')
            for content in content_list:
                if content.get('type') == 'output_text' and isinstance(content.get('text'), str):
                    parts.append(content['text'])
                elif content.get('type') == 'refusal' and isinstance(content.get('refusal'), str):
                    parts.append(content['refusal'])
                else:
                    result['desvios'].append('conteudo de mensagem nao textual')
            messages.append(''.join(parts))
            if item.get('status') != 'completed':
                result['desvios'].append('mensagem nao concluida')
        if messages:
            result['texto'] = ''.join(messages).encode('utf-8')
        if len(messages) != 1:
            result['desvios'].append('esperada exatamente uma mensagem de assistente')
        if not isinstance(result['response_id'], str) or not result['response_id']:
            result['desvios'].append('response_id ausente')
        if result['modelo_reportado'] != config['modelo_solicitado']:
            result['desvios'].append('modelo reportado diferente/ausente; conferir alias e versao')
        if data.get('tools') != [] or data.get('tool_choice') != 'none':
            result['desvios'].append('envelope nao confirma tools=[] e tool_choice=none')
        if data.get('instructions') is not None or data.get('previous_response_id') is not None:
            result['desvios'].append('envelope reporta instrucoes/historico adicionais')
        result['concluida'] = data.get('status') == 'completed' and len(messages) == 1
        if not result['concluida']:
            result['causa'] = 'resposta incompleta/incompativel: ' + str(data.get('status'))
    except (ValueError, UnicodeError, RecursionError) as error:
        result['causa'] = 'envelope invalido: ' + type(error).__name__
    return result


def preparar(origem, saida, limite_saida, orcamento, timeout=120):
    original = base.conferir_plano(origem)
    if type(limite_saida) is not int or limite_saida < MIN_OUTPUT_TOKENS or type(timeout) is not int or timeout < 1:
        raise ValueError('limite de saida deve ser inteiro >=16; timeout inteiro positivo; nao escolhe limite cientifico')
    try:
        budget = Decimal(str(orcamento))
        if not budget.is_finite() or budget <= 0:
            raise ValueError('orcamento declarado deve ser positivo')
    except InvalidOperation as error:
        raise ValueError('orcamento invalido') from error
    out = base.protegida(saida, 'captura')
    if out.exists():
        raise ValueError('saida existente; preservar plano anterior')
    config = {'modelo_solicitado': MODELO, 'esforco_solicitado': 'medium',
              'interface': 'Responses API HTTP direto', 'endpoint': ENDPOINT,
              'max_output_tokens': limite_saida, 'timeout_segundos': timeout,
              'orcamento_declarado_usd': str(budget), 'retries_automaticos_cliente': 0,
              'tools': [], 'tool_choice': 'none', 'store': False, 'stream': False,
              'limite_garantia': 'requisicao do cliente; nao controla instrucoes ou transporte internos do provedor',
              'limite_orcamento': 'declaracao do pesquisador; nao e teto monetario imposto pelo script'}
    config['id'] = 'piloto-api-' + sha(bytes_json(config))[:16]
    out.mkdir(parents=True)
    salvar(out / 'plano-cli-original.json', Path(origem).read_bytes())
    plan = {k: v for k, v in original.items() if k not in ('configuracao', 'observacoes')}
    plan.update(coletor=VERSAO, coletor_sha256=sha(Path(__file__).read_bytes()),
                montador_sha256=sha(Path(montagem.__file__).read_bytes()),
                auxiliar_sha256=sha(Path(base.__file__).read_bytes()),
                ordem_origem_sha256=sha(Path(origem).read_bytes()),
                configuracao_id=config['id'], configuracao=config, modelo=MODELO,
                status='PREPARADO_API_NAO_ENVIADO', observacoes=[])
    prepared = {}
    for row in original['observacoes']:
        key = row['mudanca'] + '-' + row['condicao']
        if key not in prepared:
            source = base.relativo(Path(origem).parent, row['preparacao'])
            old = base.conferir_preparacao(source)
            package = out / 'pacotes' / key
            package.mkdir(parents=True)
            for e in old['documentos']:
                salvar(package / e['arquivo'], (source.parent / 'documentos' / e['arquivo']).read_bytes())
            manifest = base.ler(source.parent / 'manifesto-original.json')
            manifest['configuracao_id'] = config['id']
            salvar_json(package / 'manifesto.json', manifest)
            auth = base.ler(source.parent / 'autorizacao-original.json')
            auth['manifesto_sha256'] = sha((package / 'manifesto.json').read_bytes())
            authpath = out / 'autorizacoes' / (key + '.json')
            salvar_json(authpath, auth)
            dest = out / 'preparados' / key
            new = montagem.preparar(package, package / 'manifesto.json', dest, authpath)
            if new['payload_sha256'] != old['payload_sha256']:
                raise ValueError('transporte API alterou o texto experimental')
            prepared[key] = dest / 'preparacao.json'
        prep = prepared[key]
        plan['observacoes'].append({**row, 'configuracao_id': config['id'],
                                   'preparacao': prep.relative_to(out).as_posix(),
                                   'preparacao_sha256': sha(prep.read_bytes())})
    salvar_json(out / 'plano.json', plan)
    return out / 'plano.json'


def conferir(path):
    path = montagem.sem_links(path)
    plan = base.ler(path)
    if (plan.get('coletor') != VERSAO or plan.get('coletor_sha256') != sha(Path(__file__).read_bytes())
            or plan.get('montador_sha256') != sha(Path(montagem.__file__).read_bytes())
            or plan.get('auxiliar_sha256') != sha(Path(base.__file__).read_bytes())):
        raise ValueError('versao/hash mudou; preparar novo plano API')
    config = plan['configuracao']
    signature = {k: v for k, v in config.items() if k != 'id'}
    if (config['id'] != 'piloto-api-' + sha(bytes_json(signature))[:16]
            or config['modelo_solicitado'] != MODELO or config['endpoint'] != ENDPOINT
            or config['esforco_solicitado'] != 'medium' or config['tools'] != []
            or config['tool_choice'] != 'none' or config['store'] is not False
            or config['stream'] is not False or config['retries_automaticos_cliente'] != 0):
        raise ValueError('configuracao API divergente')
    rows = plan['observacoes']
    oldraw = (path.parent / 'plano-cli-original.json').read_bytes()
    original_rows = montagem._json(oldraw)['observacoes']
    if (sha(oldraw) != plan['ordem_origem_sha256']
            or [(r['observacao_id'], r['payload_sha256']) for r in rows]
            != [(r['observacao_id'], r['payload_sha256']) for r in original_rows]):
        raise ValueError('ordem/textos diferem do planejamento preservado')
    if (plan['configuracao_id'] != config['id'] or type(config['max_output_tokens']) is not int
            or config['max_output_tokens'] < MIN_OUTPUT_TOKENS or type(config['timeout_segundos']) is not int
            or config['timeout_segundos'] < 1):
        raise ValueError('limites/configuracao invalidos')
    expected = {(m, c, r) for m in ('MC-01', 'MC-03') for c in montagem.CONDICOES for r in (1, 2)}
    if (len(rows) != 16 or {(r['mudanca'], r['condicao'], r['repeticao']) for r in rows} != expected
            or [r['ordem'] for r in rows] != list(range(1, 17))
            or len({r['observacao_id'] for r in rows}) != 16):
        raise ValueError('ordem/identidades do piloto divergentes')
    preps = {}
    for row in rows:
        if (row['observacao_id'] != f"PIL-{row['mudanca']}-{row['condicao']}-R{row['repeticao']:02}"
                or row['bloco'] != row['repeticao']
                or row['repeticao'] != (1 if row['ordem'] <= 8 else 2)
                or row['status'] != 'PLANEJADA_NAO_EXECUTADA'):
            raise ValueError('identidade/bloco/fase divergente')
        p = base.relativo(path.parent, row['preparacao'])
        if sha(p.read_bytes()) != row['preparacao_sha256']:
            raise ValueError('hash da preparacao divergente')
        prep = base.conferir_preparacao(p)
        if any(row[k] != prep[k] for k in ('configuracao_id', 'mudanca', 'condicao', 'payload_sha256')):
            raise ValueError('preparacao/configuracao divergente')
        if row['configuracao_id'] != config['id'] or row['origem'] != 'real' or row['fase'] != 'piloto':
            raise ValueError('origem/fase/configuracao divergente')
        preps[(row['mudanca'], row['condicao'])] = prep
    if len(preps) != 8 or not montagem.conferir_condicoes(list(preps.values())):
        raise ValueError('condicoes divergentes')
    return plan


def capturar(path, lote, limite, continuar=False, real=False, sender=enviar, *, conferidor=None, controle_http=None, autorizacao=None):
    check = conferir if conferidor is None else conferidor
    plan = check(path)
    total = len(plan['observacoes'])
    notas = plan.get('etapa') == 'notas-mc04-0.3-D46'
    extension = notas or plan.get('etapa') == 'extensao-0.3-D41'
    authorization_raw = None
    authorization_data = None
    if notas and real:
        # Antes de chave, lock, criacao do lote ou transporte.
        from notas_exploratorias import validar_autorizacao
        authorization_data = validar_autorizacao(path, autorizacao)
        authorization_raw = Path(autorizacao).read_bytes()
        if montagem._json(authorization_raw) != authorization_data:
            raise ValueError('autorizacao mudou durante a validacao')
    if extension and not notas and real and (plan.get('integracao') != 'envio-extensao-D42-v1'
                               or plan.get('envio_autorizado') is not True):
        raise ValueError('plano da extensao sem integracao de envio D-42')
    if type(limite) is not int or not 1 <= limite <= total:
        raise ValueError('--limite deve estar entre 1 e ' + str(total))
    key = None
    if real:
        key = chave_api()
    out = base.protegida(lote, 'captura')
    origin, phase = ('real', 'exploratoria' if extension else 'piloto') if real else ('sintetica', 'verificacao_sintetica')
    header = {'origem': origin, 'fase': phase, 'interface': 'Responses API',
              'plano_sha256': sha(Path(path).read_bytes()), 'coletor_sha256': sha(Path(__file__).read_bytes())}
    if extension:
        header.update(etapa=plan['etapa'], integracao=plan['integracao'],
                      catalogo_versao=plan['catalogo_versao'], referencia_sha256=plan['referencia_sha256'])
    if notas:
        header['bloco_exploratorio'] = plan['bloco_exploratorio']
        if real:
            header.update(autorizacao_sha256=sha(authorization_raw),
                          orcamento_novo_declarado_usd=authorization_data['orcamento_usd'])
    if not continuar:
        out.mkdir(parents=True, exist_ok=False)
        salvar(out / 'plano-original.json', Path(path).read_bytes())
        salvar_json(out / 'lote.json', header)
        if notas and real:salvar(out / 'autorizacao-envio-original.json',authorization_raw)
    if (base.ler(out / 'lote.json') != header or (out / 'plano-original.json').read_bytes() != Path(path).read_bytes()):
        raise ValueError('configuracao/origem/plano mudou; nao continuar este lote')
    if notas and real and sha((out/'autorizacao-envio-original.json').read_bytes())!=header['autorizacao_sha256']:
        raise ValueError('autorizacao original do lote divergente')
    lock = out / 'coletor.lock'
    with lock.open('x') as f:
        f.write(str(os.getpid()))
    count = 0
    response_ids = set()
    try:
        for row in plan['observacoes']:
            attempt = out / row['observacao_id'] / 'T01'
            if attempt.exists():
                previous = base.conferir_fechamento(attempt)
                if extension and (any(previous[k] != row[k] for k in (
                    'observacao_id', 'configuracao_id', 'payload_sha256', 'preparacao_sha256', 'mudanca', 'condicao'))
                    or previous['origem'] != origin or previous['fase'] != phase
                    or previous.get('etapa') != plan['etapa']
                    or previous.get('configuracao') != plan['configuracoes'][row['configuracao_id']]):
                    raise ValueError('captura de outra observacao/configuracao/origem; nao continuar')
                if notas and any(previous.get(k) != row[k] for k in ('nota_id', 'bloco_exploratorio')):
                    raise ValueError('nota/bloco divergente na retomada')
                if previous['estado_tecnico'] != 'concluida' or previous['desvios']:
                    raise ValueError('tentativa incompleta/ambigua/com desvio; conferir sem reenvio automatico')
                if previous['response_id'] in response_ids:
                    raise ValueError('response_id repetido entre observacoes')
                response_ids.add(previous['response_id'])
                continue
            if count >= limite:
                break
            check(path)
            config = plan['configuracoes'][row['configuracao_id']] if extension else plan['configuracao']
            prepfile = base.relativo(Path(path).parent, row['preparacao'])
            prep = base.conferir_preparacao(prepfile)
            if notas and any(prep.get(k) != row[k] for k in ('nota_id', 'bloco_exploratorio')):
                raise ValueError('nota/bloco diverge da preparacao')
            attempt.mkdir(parents=True)
            for name in ['preparacao.json'] + [x['arquivo'] for x in prep['arquivos']]:
                salvar(attempt / 'preparacao' / name, (prepfile.parent / name).read_bytes())
            payload = (prepfile.parent / 'payload.txt').read_bytes()
            body = requisicao(payload, config)
            salvar(attempt / 'entrada.bin', payload)
            guardar_requisicao(attempt, body)
            start = agora()
            salvar_json(attempt / 'inicio.json', {'instante': start, 'origem': origin,
                        'endpoint': ENDPOINT, 'requisicao_sha256': sha(body), 'credenciais_persistidas': False,
                        **({'nota_id':row['nota_id'],'bloco_exploratorio':row['bloco_exploratorio']} if notas else {})})
            parsed = None
            request_id = None
            status = None
            failure = None
            if real:
                status, raw, request_id, failure = obter_http(sender, body, key, config['timeout_segundos'])
            elif controle_http is not None:
                status, raw, request_id, failure = obter_http(controle_http, body, None, config['timeout_segundos'])
            else:
                status, raw = 200, bytes_json({'id': 'controle-' + uuid.uuid4().hex,
                        'model': config['modelo_solicitado'], 'status': 'completed', 'tools': [], 'tool_choice': 'none',
                        'output': [{'type': 'message', 'role': 'assistant', 'status': 'completed',
                                    'content': [{'type': 'output_text', 'text': '{"requisitos":[],"testes":[]}'}]}]})
            guardar_http(attempt, status, raw, request_id, failure)
            parsed = falha_interpretada(failure) if failure else interpretar(raw, status, config)
            text = parsed['texto']
            if parsed['response_id'] in response_ids:
                parsed['desvios'].append('response_id repetido entre observacoes')
            if parsed['response_id'] is not None:
                response_ids.add(parsed['response_id'])
            if text is not None:
                salvar(attempt / 'resposta.bin', text)
            record = {k: row[k] for k in ('observacao_id', 'configuracao_id', 'mudanca', 'condicao', 'payload_sha256')}
            record.update(origem=origin, fase=phase, tentativa_id=row['observacao_id'] + '-T01', tentativa_anterior=None,
                preparacao_id=prep['preparacao_id'], preparacao_sha256=row['preparacao_sha256'],
                entrada_enviada_arquivo='entrada.bin', entrada_enviada_sha256=sha(payload),
                resposta_arquivo='resposta.bin' if text is not None else None,
                resposta_sha256=sha(text) if text is not None else None, resposta_tamanho=len(text) if text is not None else None,
                estado_tecnico='concluida' if parsed['concluida'] else 'falha_tecnica', fragmento=not parsed['concluida'],
                causa=parsed['causa'], instante_execucao=start, instante_fim=agora(),
                origem_resposta='Responses API; envelope bruto preservado' if real else 'CONTROLE ARTIFICIAL; sem rede/modelo',
                modelo_reportado=parsed['modelo_reportado'] if real else None,
                modelo_reportado_indisponibilidade=None if real and parsed['modelo_reportado'] else 'nao reportado; controle ou falha',
                configuracao=config, versoes={'coletor': VERSAO, 'coletor_sha256': header['coletor_sha256']},
                conformidade_protocolo='desvio' if parsed['desvios'] else 'pendente', desvios=parsed['desvios'],
                http_status=status, request_id=request_id, response_id=parsed['response_id'], usage=parsed['usage'],
                falha_transporte=failure, estado_remoto='desconhecido' if failure else 'resposta_http_recebida',
                requisicao_sha256=sha(body), retentativas_cliente=0,
                texto_extraido_de='output/message/content/output_text ou refusal; sem trim ou reparo')
            record['repeticao' if real else 'repeticao_sintetica'] = row['repeticao']
            if extension:
                record.update(etapa=plan['etapa'], integracao=plan['integracao'],
                              bloco=row['bloco'], ordem=row['ordem'], plano_sha256=header['plano_sha256'],
                              catalogo_versao=plan['catalogo_versao'], referencia_sha256=plan['referencia_sha256'])
            if notas:
                record.update(nota_id=row['nota_id'], bloco_exploratorio=row['bloco_exploratorio'], modelo=row['modelo'])
                if real:record['autorizacao_sha256'] = header['autorizacao_sha256']
            salvar_json(attempt / 'tentativa.json', record)
            salvar_json(attempt / 'fechamento.json', {'arquivos': base.inventariar(attempt)})
            count += 1
            print(row['observacao_id'], record['estado_tecnico'], flush=True)
            if failure and failure['interrompida']:
                return 130
            if not parsed['concluida'] or parsed['desvios']:
                return 2
        return 0
    finally:
        lock.unlink()


def avaliar_lote(lote, referencia, saida):
    """Adapta somente a fase exploratoria; reusa avaliacao/resumo, sem coleta.

    A rota historica e delegada literalmente ao auxiliar anterior, cuja fonte
    e trava Codex permanecem intactas.
    """
    root = montagem.sem_links(lote)
    header = base.ler(root / 'lote.json')
    if header.get('etapa') == 'notas-mc04-0.3-D46':
        from notas_exploratorias import avaliar_lote as avaliar_notas
        return avaliar_notas(lote, referencia, saida)
    if (header['origem'], header['fase']) != ('real', 'exploratoria'):
        return base.avaliar_lote(lote, referencia, saida)
    import avaliacao_ids as avaliador
    raw = (root / 'plano-original.json').read_bytes()
    plan = montagem._json(raw)
    if (sha(raw) != header['plano_sha256'] or plan.get('etapa') != 'extensao-0.3-D41'
        or header.get('etapa') != plan['etapa'] or header.get('referencia_sha256') != plan['referencia_sha256']
        or sha(Path(referencia).read_bytes()) != plan['referencia_sha256']):
        raise ValueError('lote/plano/referencia nao correspondem a extensao')
    out = base.protegida(saida, 'avaliados')
    out.mkdir(parents=True, exist_ok=False)
    selected, observations = [], []
    code = 0
    for row in plan['observacoes']:
        observations.append({**{k: row[k] for k in ('observacao_id', 'configuracao_id', 'mudanca', 'condicao', 'payload_sha256')},
                             'origem': 'real', 'fase': 'exploratoria', 'repeticao': row['repeticao']})
        attempt = root / row['observacao_id'] / 'T01'
        if not attempt.exists():
            continue
        reg = base.conferir_fechamento(attempt)
        if (reg['origem'] != 'real' or reg['fase'] != 'exploratoria' or reg.get('etapa') != plan['etapa']
            or any(reg[k] != row[k] for k in ('observacao_id', 'configuracao_id', 'payload_sha256'))):
            raise ValueError('captura de outra fase/observacao/configuracao')
        target = out / row['observacao_id'] / 'T01'
        _, status = avaliador.avaliar(attempt / 'preparacao/preparacao.json', attempt / 'tentativa.json',
                                     referencia, target, origem='real', fase='exploratoria')
        code = max(code, status)
        selected.append({'arquivo': (target / 'avaliacao.json').relative_to(out).as_posix(),
                         'sha256': sha((target / 'avaliacao.json').read_bytes())})
    salvar_json(out / 'lista.json', selected)
    salvar_json(out / 'observacoes.json', observations)
    _, status = avaliador.resumir(out / 'lista.json', out / 'observacoes.json', out / 'resumo', origem='real', fase='exploratoria')
    return max(code, status)


def conexao(saida, limite_saida, timeout=120, sender=enviar):
    """Uma chamada paga neutra, separada de qualquer observacao do piloto."""
    if type(limite_saida) is not int or limite_saida < MIN_OUTPUT_TOKENS or type(timeout) is not int or timeout < 1:
        raise ValueError('limite deve ser >=16 e timeout positivo; valor cientifico ainda deve ser escolhido')
    key = chave_api()
    out = base.protegida(saida, 'captura')
    if out.exists():
        raise ValueError('saida existente; nao sobrescrever teste de conexao')
    config = {'modelo_solicitado': MODELO, 'esforco_solicitado': 'medium', 'max_output_tokens': limite_saida}
    payload = b'Responda apenas OK.\n'
    body = requisicao(payload, config)
    out.mkdir(parents=True)
    salvar(out / 'entrada.bin', payload)
    guardar_requisicao(out, body)
    salvar_json(out / 'inicio.json', {'fase': 'verificacao_conexao', 'instante': agora(),
                                     'configuracao': config, 'endpoint': ENDPOINT, 'credenciais_persistidas': False})
    status, raw, request_id, failure = obter_http(sender, body, key, timeout)
    guardar_http(out, status, raw, request_id, failure)
    result = falha_interpretada(failure) if failure else interpretar(raw, status, config)
    if result['texto'] is not None:
        salvar(out / 'resposta.bin', result['texto'])
    summary = {k: v for k, v in result.items() if k != 'texto'}
    summary.update(fase='verificacao_conexao', http_status=status, request_id=request_id,
                       incluido_piloto=False, incluido_coleta_principal=False,
                       falha_transporte=failure, estado_remoto='desconhecido' if failure else 'resposta_http_recebida',
                       orcamento='chamada paga isolada; uso em usage quando reportado')
    salvar_json(out / 'resultado.json', summary)
    salvar_json(out / 'fechamento.json', {'arquivos': base.inventariar(out)})
    if failure and failure['interrompida']:
        return 130
    return 0 if summary.get('concluida') and not summary.get('desvios') else 2


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='comando', required=True)
    p = sub.add_parser('preparar', help='offline: copia ordem e bytes para novo plano API')
    p.add_argument('--ordem', required=True, type=Path)
    p.add_argument('--saida', required=True, type=Path)
    p.add_argument('--limite-saida', required=True, type=int)
    p.add_argument('--orcamento-usd', required=True)
    p.add_argument('--timeout', type=int, default=120)
    p = sub.add_parser('simular', help='offline: valida entradas, sem chave/rede')
    p.add_argument('--plano', required=True, type=Path)
    p = sub.add_parser('conexao', help='UMA chamada paga neutra, fora do piloto; exige --enviar-real')
    p.add_argument('--saida', required=True, type=Path)
    p.add_argument('--limite-saida', required=True, type=int)
    p.add_argument('--timeout', type=int, default=120)
    p.add_argument('--enviar-real', action='store_true')
    for name in ('controle', 'iniciar'):
        p = sub.add_parser(name, help='offline sintetico' if name == 'controle' else 'chamadas pagas; requer --enviar-real')
        p.add_argument('--plano', required=True, type=Path)
        p.add_argument('--lote', required=True, type=Path)
        p.add_argument('--limite', required=True, type=int)
        p.add_argument('--continuar', action='store_true')
        if name == 'iniciar':
            p.add_argument('--enviar-real', action='store_true')
    p = sub.add_parser('avaliar', help='offline: mesma avaliacao existente em etapa separada')
    p.add_argument('--lote', required=True, type=Path)
    p.add_argument('--referencia', required=True, type=Path)
    p.add_argument('--saida', required=True, type=Path)
    p = sub.add_parser('revisao-modelo', help='offline: modelo pendente com hashes, sem aprovar observacoes')
    for field in ('lote', 'avaliacoes', 'observacoes', 'saida'):
        p.add_argument('--' + field, required=True, type=Path)
    p = sub.add_parser('revisar', help='offline: registra decisao humana externa sem alterar brutos')
    p.add_argument('--decisoes', required=True, type=Path)
    p.add_argument('--saida', required=True, type=Path)
    p = sub.add_parser('resumir-revisado', help='offline: resumo controlado apenas apos revisao explicita')
    p.add_argument('--revisao', required=True, type=Path)
    p.add_argument('--saida', required=True, type=Path)
    args = parser.parse_args(argv)
    try:
        if args.comando == 'preparar':
            print(preparar(args.ordem, args.saida, args.limite_saida, args.orcamento_usd, args.timeout))
        elif args.comando == 'simular':
            plan = conferir(args.plano)
            print(json.dumps({'observacoes': len(plan['observacoes']), 'configuracao': plan['configuracao'],
                              'rede_utilizada': False, 'fase': 'preparacao_offline'}, ensure_ascii=False, indent=2))
        elif args.comando == 'conexao':
            if not args.enviar_real:
                raise ValueError('conexao gera custo; exige --enviar-real')
            return conexao(args.saida, args.limite_saida, args.timeout)
        elif args.comando in ('controle', 'iniciar'):
            real = args.comando == 'iniciar'
            if real and not args.enviar_real:
                raise ValueError('envio exige --enviar-real; nenhuma chamada realizada')
            return capturar(args.plano, args.lote, args.limite, args.continuar, real)
        elif args.comando == 'avaliar':
            return avaliar_lote(args.lote, args.referencia, args.saida)
        elif args.comando in ('revisao-modelo', 'revisar', 'resumir-revisado'):
            import revisao_conformidade as revisao
            if args.comando == 'revisao-modelo':
                print(revisao.modelo(args.lote, args.avaliacoes, args.observacoes, args.saida))
            elif args.comando == 'revisar':
                print(revisao.registrar(args.decisoes, args.saida))
            else:
                return revisao.resumir(args.revisao, args.saida)
        return 0
    except (ValueError, OSError) as error:
        print(str(error), file=__import__('sys').stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
