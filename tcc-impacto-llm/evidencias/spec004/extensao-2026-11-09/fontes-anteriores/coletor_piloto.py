"""Coletor sequencial do piloto. Ajuda, preparacao e simulacao nunca enviam prompts.

A CLI instalada ainda nao demonstra a fronteira D-29; iniciar --enviar-real
permanece bloqueado. O mesmo motor de captura e exercitado com processo local.
Somente o comando avaliar importa o avaliador e abre a referencia privada.
"""
import argparse
from datetime import datetime, timezone
import importlib.util
import json
import os
from pathlib import Path, PureWindowsPath
import shutil
import subprocess
import sys
import uuid

import montagem_entradas as montagem

RAIZ = Path(__file__).resolve().parent
VERSAO = 'coletor-piloto-v1.1-D38'
MODELO = 'gpt-6-sol'
ESFORCO = 'medium'
CONFIG_ID = 'piloto-codex-gpt-6-sol-medium-D38'
BASE = RAIZ / 'evidencias/spec004/preparacao-piloto-2026-11-06-v2-lf/artefatos/preparados'
BLOQUEIOS = [
    'Fronteira D-29 nao demonstrada: sem inventario efetivo que comprove tools=[].',
    'Codex injeta instrucoes de agente (base_instructions no catalogo embutido); '
    'entrega somente do payload e ausencia de contexto adicional nao demonstradas.',
    'Disponibilidade remota de gpt-6-sol/medium, revisao dos materiais, orcamento '
    'e autorizacao operacional de inicio ainda pendentes.',
    'CLI 0.162.0-alpha.17.2 rejeita redefinir model_providers.openai: '
    'request_max_retries/stream_max_retries de provedor personalizado nao '
    'configuram a rota embutida com login ChatGPT. Unbounded=false nao significa zero retries.',
]
# Nomes observados em `codex features list` desta instalacao. Nao equivalem a
# inventario vazio de ferramentas nem removem instrucoes base do agente.
DESATIVAR = ('shell_tool', 'view_image', 'apps', 'plugins', 'multi_agent',
             'browser_use', 'computer_use', 'image_generation', 'goals', 'sleep_tool',
             'hooks', 'skill_search', 'workspace_dependencies', 'memories',
             'skill_mcp_dependency_install', 'remote_plugin', 'unbounded_connection_retries')
# Chaves documentadas e aceitas no parser nativo desta versao (D-38).
# Configuradas/desativadas nao significa tools indisponiveis na requisicao.
CONFIG_CLI = (
    ('model_provider', 'openai'),
    ('forced_login_method', 'chatgpt'),
    ('model_reasoning_effort', ESFORCO),
    ('web_search', 'disabled'),
    ('project_doc_max_bytes', 0),
    ('skills.include_instructions', False),
    ('memories.generate_memories', False),
    ('memories.use_memories', False),
)


def overrides_cli():
    # JSON escalares possuem a mesma representacao TOML para estes valores.
    return [key + '=' + json.dumps(value) for key, value in CONFIG_CLI]


def instante():
    return datetime.now(timezone.utc).isoformat()


def serial(obj):
    return (json.dumps(obj, ensure_ascii=True, sort_keys=True, indent=2) + '\n').encode()


def salvar(path, data):
    path = montagem.sem_links(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('xb') as stream:
        stream.write(data)


def salvar_json(path, obj):
    salvar(path, serial(obj))


def ler(path):
    return montagem._json(montagem.sem_links(path).read_bytes())


def relativo(root, name):
    if not isinstance(name, str) or not name:
        raise ValueError('caminho relativo ausente')
    win = PureWindowsPath(name)
    if win.drive or win.root or any(p in ('', '.', '..') for p in name.replace('\\', '/').split('/')):
        raise ValueError('caminho declarado deve ser relativo sem traversal')
    path = montagem.sem_links(root / name)
    if not path.is_relative_to(root):
        raise ValueError('caminho externo')
    return path


def protegida(path, zona):
    path = montagem.sem_links(path)
    root = montagem.sem_links(RAIZ / zona)
    if path == root or not path.is_relative_to(root):
        raise ValueError('usar diretorio novo dentro de ' + str(root))
    return path


def conferir_preparacao(path):
    """Valida snapshots, autorizacao e composicao sem consultar fontes privadas."""
    path = montagem.sem_links(path)
    prep = ler(path)
    root = path.parent
    if (prep.get('contrato') != montagem.CONTRATO or prep.get('completo') is not True
            or prep.get('status') != 'PREPARADO_LOCAL_NAO_ENVIADO'
            or prep.get('politica_bytes') != 'utf8-sem-bom-lf-v1'):
        raise ValueError('preparacao v2-LF incompleta/incompativel')
    entries = prep['arquivos']
    names = [item['arquivo'] for item in entries]
    docs = list(montagem.NOMES)
    if prep['condicao'] in ('D1', 'E1'):
        docs.insert(5, 'notas.md')
    expected = {'manifesto-original.json', 'autorizacao-original.json', 'payload.txt',
                'entrega-textual.json'} | {'documentos/' + name for name in docs}
    if len(names) != len(set(names)) or set(names) != expected:
        raise ValueError('arquivos extras/ausentes na preparacao')
    for item in entries:
        if montagem.sha(relativo(root, item['arquivo']).read_bytes()) != item['sha256']:
            raise ValueError('hash de arquivo divergente: ' + item['arquivo'])
    manifest_raw = (root / 'manifesto-original.json').read_bytes()
    auth_raw = (root / 'autorizacao-original.json').read_bytes()
    manifest, auth = montagem._json(manifest_raw), montagem._json(auth_raw)
    if (montagem.sha(manifest_raw) != prep['manifesto_sha256']
            or montagem.sha(auth_raw) != prep['autorizacao_sha256']
            or auth['manifesto_sha256'] != prep['manifesto_sha256']
            or auth.get('status') != 'CONFERIDO_TECNICAMENTE_RASCUNHO'
            or auth.get('documentos') != [{'arquivo': e['arquivo'], 'sha256': e['sha256']}
                                        for e in prep['documentos']]
            or manifest['documentos'] != prep['documentos']
            or [e['arquivo'] for e in prep['documentos']] != docs):
        raise ValueError('manifesto/autorizacao divergentes')
    for field in ('configuracao_id', 'mudanca', 'condicao', 'politica_bytes'):
        if manifest[field] != prep[field]:
            raise ValueError('identidade divergente: ' + field)
    blobs = []
    for entry in prep['documentos']:
        data = (root / 'documentos' / entry['arquivo']).read_bytes()
        data.decode('utf-8')
        if (montagem.sha(data) != entry['sha256'] or len(data) != entry['tamanho_bytes']
                or b'\r' in data or data.startswith(b'\xef\xbb\xbf')):
            raise ValueError('documento diverge da politica LF/hash')
        blobs.append(f'<<<inicio:{entry["papel"]}>>>\n'.encode() + data
                     + f'\n<<<fim:{entry["papel"]}>>>\n'.encode())
    payload = (root / 'payload.txt').read_bytes()
    if (payload != b''.join(blobs) or montagem.sha(payload) != prep['payload_sha256']
            or len(payload) != prep['payload_tamanho']):
        raise ValueError('payload/composicao divergentes')
    return prep


def configuracao_fixa():
    return {'id': CONFIG_ID, 'modelo_solicitado': MODELO, 'esforco_solicitado': ESFORCO,
            'interface': 'codex exec', 'saida_estruturada_forcada': False,
            'mensagem_usuario': 'payload completo via stdin; sem acrescimos',
            'modelo_reportado': None, 'temperatura': None, 'top_p': None,
            'seed_modelo': None, 'limite_saida': None, 'orcamento': None,
            'parametros_nao_verificados': ['modelo remoto', 'limite de saida', 'fronteira D-29', 'retentativas internas CLI'],
            'ferramentas_desativar_solicitadas': list(DESATIVAR),
            'ferramentas_desativadas_verificado': False,
            'configuracoes_cli_solicitadas': dict(CONFIG_CLI),
            'retentativas_cliente': {
                'provedor_solicitado': 'openai', 'request_max_retries': None,
                'stream_max_retries': None, 'garantia_zero_retries': False,
                'causa': 'provedor embutido reservado; zero aceito apenas em definicao personalizada testada',
            },
            'historico_sessao': 'novo codex exec; nunca resume/fork',
            'bloqueios_envio': BLOQUEIOS}


def preparar_plano(saida, ordem=None):
    out = protegida(saida, 'captura')
    if out.exists():
        raise ValueError('saida ja existe')
    if ordem is None:
        spec = importlib.util.spec_from_file_location('ordenador_piloto', RAIZ / 'materiais/modelos/ordenar_piloto.py')
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        plan = mod.ordenar(ler(RAIZ / 'materiais/modelos/plano_piloto.json'), 20261106)
    else:
        plan = ler(ordem)  # Ordem ja registrada nunca e embaralhada novamente.
    if any(row.get('ordem') is None for row in plan['observacoes']):
        raise ValueError('ordem registrada incompleta')
    out.mkdir(parents=True)
    if ordem is not None:
        salvar(out / 'ordem-original.json', Path(ordem).read_bytes())
    config = configuracao_fixa()
    plan.update(configuracao_id=CONFIG_ID, modelo=MODELO, configuracao=config,
                status='PREPARADO_OFFLINE_ENVIO_BLOQUEADO', coletor=VERSAO,
                coletor_sha256=montagem.sha(Path(__file__).read_bytes()),
                montador_sha256=montagem.sha(Path(montagem.__file__).read_bytes()))
    for change in ('MC-01', 'MC-03'):
        for condition in montagem.CONDICOES:
            key = change + '-' + condition
            source = BASE / key / 'preparacao.json'
            source_prep = conferir_preparacao(source)
            package = out / 'pacotes' / key
            package.mkdir(parents=True)
            manifest = ler(source.parent / 'manifesto-original.json')
            manifest['configuracao_id'] = CONFIG_ID
            raw = serial(manifest)
            salvar(package / 'manifesto.json', raw)
            for entry in manifest['documentos']:
                salvar(package / entry['arquivo'], (source.parent / 'documentos' / entry['arquivo']).read_bytes())
            auth = ler(source.parent / 'autorizacao-original.json')
            auth['manifesto_sha256'] = montagem.sha(raw)
            authpath = out / 'autorizacoes' / (key + '.json')
            salvar_json(authpath, auth)
            destination = out / 'preparados' / key
            prep = montagem.preparar(package, package / 'manifesto.json', destination, authpath)
            if prep['payload_sha256'] != source_prep['payload_sha256']:
                raise ValueError('remontagem alterou payload v2-LF')
            for row in plan['observacoes']:
                if (row['mudanca'], row['condicao']) == (change, condition):
                    row.update(configuracao_id=CONFIG_ID, payload_sha256=prep['payload_sha256'],
                               preparacao='preparados/' + key + '/preparacao.json',
                               preparacao_sha256=montagem.sha((destination / 'preparacao.json').read_bytes()),
                               fonte_v2_lf_sha256=montagem.sha(source.read_bytes()))
    salvar_json(out / 'plano.json', plan)
    conferir_plano(out / 'plano.json')
    return out / 'plano.json'


def conferir_plano(path):
    path = montagem.sem_links(path)
    plan = ler(path)
    if (plan.get('coletor') != VERSAO
            or plan.get('coletor_sha256') != montagem.sha(Path(__file__).read_bytes())
            or plan.get('montador_sha256') != montagem.sha(Path(montagem.__file__).read_bytes())):
        raise ValueError('versao/hash do coletor ou montador mudou; preparar novo plano')
    rows = plan['observacoes']
    expected = {(m, c, r) for m in ('MC-01', 'MC-03') for c in montagem.CONDICOES for r in (1, 2)}
    if (len(rows) != 16 or {(r['mudanca'], r['condicao'], r['repeticao']) for r in rows} != expected
            or [r['ordem'] for r in rows] != list(range(1, 17))
            or len({r['observacao_id'] for r in rows}) != 16):
        raise ValueError('plano exige 16 identidades/posicoes unicas na ordem registrada')
    config = plan['configuracao']
    if (config['modelo_solicitado'] != MODELO or config['esforco_solicitado'] != ESFORCO
            or config['id'] != plan['configuracao_id'] or config != configuracao_fixa()):
        raise ValueError('configuracao divergente; nunca substituir GPT-6 Sol')
    preps = {}
    for row in rows:
        m, c, r = row['mudanca'], row['condicao'], row['repeticao']
        if (row['observacao_id'] != f'PIL-{m}-{c}-R{r:02}' or row['bloco'] != r
                or r != (1 if row['ordem'] <= 8 else 2)
                or row['configuracao_id'] != config['id']
                or row['status'] != 'PLANEJADA_NAO_EXECUTADA'
                or row.get('origem') != 'real' or row.get('fase') != 'piloto'):
            raise ValueError('identidade/configuracao/bloco/fase divergente')
        source = relativo(path.parent, row['preparacao'])
        if montagem.sha(source.read_bytes()) != row['preparacao_sha256']:
            raise ValueError('hash da preparacao divergente')
        prep = conferir_preparacao(source)
        if any(prep[k] != row[k] for k in ('configuracao_id', 'mudanca', 'condicao', 'payload_sha256')):
            raise ValueError('preparacao de outra observacao/configuracao')
        preps[(m, c)] = prep
    if len({row['payload_sha256'] for row in rows}) != 8:
        raise ValueError('esperados oito payloads unicos')
    montagem.conferir_condicoes(list(preps.values()))
    return plan


def comando_codex(executable, work):
    """Somente flags vistas na ajuda local. Configuracoes nao provam tools=[]."""
    argv = [str(executable), '--no-daemon', 'exec', '--ignore-user-config', '--ignore-rules',
            '--ephemeral', '--strict-config', '--skip-git-repo-check', '--sandbox', 'read-only',
            '--model', MODELO,
            '--cd', str(work), '--json', '--color', 'never']
    for override in overrides_cli():
        argv.extend(['-c', override])
    for feature in DESATIVAR:
        argv.extend(['--disable', feature])
    return argv + ['-']


def simular(path):
    plan = conferir_plano(path)
    executable = shutil.which('codex') or 'codex'
    return {'modo': 'SIMULACAO_SEM_PROCESSO_LLM', 'observacoes': len(plan['observacoes']),
            'payloads_unicos': 8, 'plano_sha256': montagem.sha(Path(path).read_bytes()),
            'configuracao': plan['configuracao'], 'bloqueios_envio': BLOQUEIOS,
            'comandos': [{'observacao_id': row['observacao_id'], 'payload_sha256': row['payload_sha256'],
                          'stdin_arquivo': str(Path(path).parent / row['preparacao']).replace('preparacao.json', 'payload.txt'),
                          'argv': comando_codex(executable, '<diretorio-novo-sem-projeto>')}
                         for row in plan['observacoes']]}


def conferir_ambiente(saida):
    """Somente comandos locais de consulta. Nunca abre auth.json ou config.toml."""
    out = protegida(saida, 'captura')
    out.mkdir(parents=True, exist_ok=False)
    executable = shutil.which('codex')
    report = {'instante': instante(), 'executable': executable, 'modelo_solicitado': MODELO,
              'esforco_solicitado': ESFORCO, 'bloqueios_envio': BLOQUEIOS, 'consultas': []}
    if executable:
        for name, args in [('versao', ['--version']), ('ajuda', ['--help']),
                           ('exec-ajuda', ['exec', '--help']), ('autenticacao', ['login', 'status']),
                           ('catalogo-embutido', ['debug', 'models', '--bundled'])]:
            result = subprocess.run([executable, *args], capture_output=True, timeout=30)
            # Catalogo contem instrucoes extensas; preservar somente capacidades selecionadas.
            stdout = result.stdout
            if name == 'catalogo-embutido' and result.returncode == 0:
                models = montagem._json(stdout)['models']
                model = next((m for m in models if m['slug'] == MODELO), None)
                stdout = serial(None if model is None else {
                    **{k: model.get(k) for k in ('slug', 'supported_reasoning_levels', 'default_reasoning_level',
                                                'shell_type', 'apply_patch_tool_type', 'experimental_supported_tools', 'tool_mode')},
                    'base_instructions_presente': bool(model.get('base_instructions')),
                    'base_instructions_sha256': montagem.sha(model.get('base_instructions', '').encode())})
            salvar(out / (name + '-stdout.txt'), stdout)
            salvar(out / (name + '-stderr.txt'), result.stderr)
            report['consultas'].append({'consulta': name, 'argv': [executable, *args], 'retorno': result.returncode})
    salvar_json(out / 'ambiente.json', report)
    return report


def extrair_eventos(raw):
    """JSONL original permanece intocado; extracao nao limpa nem reserializa texto."""
    events, deviations, finals, sessions, models = [], [], [], [], []
    malformed = False
    for line in raw.splitlines():
        try:
            event = montagem._json(line)
            if not isinstance(event, dict):
                raise ValueError('evento nao e objeto')
        except (ValueError, UnicodeError):
            malformed = True
            continue
        events.append(event)
        kind = event.get('type')
        if kind not in ('thread.started', 'turn.started', 'turn.completed', 'turn.failed',
                        'error', 'item.started', 'item.updated', 'item.completed', 'metadata'):
            deviations.append('evento nao reconhecido: ' + str(kind))
        if kind == 'thread.started':
            sessions.append(event.get('thread_id'))
        if isinstance(event.get('model'), str):
            models.append(event['model'])
        item = event.get('item', {})
        if not isinstance(item, dict):
            malformed = True
            continue
        if kind in ('item.started', 'item.completed', 'item.updated'):
            if item.get('type') not in ('agent_message', 'reasoning'):
                deviations.append('ferramenta/evento adicional: ' + str(item.get('type')))
            if kind == 'item.completed' and item.get('type') == 'agent_message':
                text = item.get('text')
                if isinstance(text, str):
                    finals.append(text.encode('utf-8'))
    if len(finals) > 1:
        deviations.append('mensagens adicionais do agente: ' + str(len(finals)))
    if len(sessions) > 1 or (finals and (len(sessions) != 1 or not sessions[0])):
        deviations.append('sessao nova unica nao identificada')
    turns = sum(e.get('type') == 'turn.started' for e in events)
    if turns > 1 or (finals and turns != 1):
        deviations.append('quantidade de turnos diferente de um')
    if any(m != MODELO for m in models):
        deviations.append('modelo reportado difere do solicitado')
    errors = sum(e.get('type') == 'error' for e in events)
    failed = any(e.get('type') == 'turn.failed' for e in events)
    completed = sum(e.get('type') == 'turn.completed' for e in events)
    # Um erro/reconnect do cliente pode ser seguido de final integral no MESMO
    # turno. Preservar a conclusao evita nova geracao por retentativa do coletor.
    # O desvio bloqueia continuacao: nao inferir quantas requisicoes HTTP houve.
    if errors and completed:
        deviations.append('erro de cliente antes de conclusao; transporte interno a conferir')
    if failed and completed:
        deviations.append('eventos terminais conflitantes: turn.failed e turn.completed')
    complete = (not malformed and not failed and len(finals) > 0 and completed == 1)
    return {'resposta': finals[-1] if finals else None, 'mensagens': finals,
            'desvios': list(dict.fromkeys(deviations)), 'sessao': sessions[0] if len(sessions) == 1 else None,
            'modelo_reportado': models[-1] if models else None, 'completo': complete,
            'erros_cliente_observados': errors, 'turnos_iniciados_observados': turns,
            'retentativas_transporte_observadas': None,
            'jsonl_invalido': malformed}


def ambiente_filho():
    # Nao transportar IDs/contexto/overrides do agente de desenvolvimento nem
    # chaves de API. Autenticacao futura usa a conta local existente do Codex.
    names = {'systemroot', 'windir', 'path', 'pathext', 'temp', 'tmp', 'userprofile',
             'homedrive', 'homepath', 'appdata', 'localappdata', 'programdata', 'comspec', 'lang'}
    return {k: v for k, v in os.environ.items() if k.lower() in names}


def subprocesso(argv, payload, work, stdout, stderr):
    """Arquivos de eventos/erros abertos antes do filho; preservam captura parcial."""
    with stdout.open('xb') as out, stderr.open('xb') as err:
        child = subprocess.Popen(argv, stdin=subprocess.PIPE, stdout=out, stderr=err, cwd=work,
                                 env=ambiente_filho())
        try:
            child.communicate(input=payload)
            return child.returncode
        except BaseException:
            child.terminate()
            try:
                child.wait(timeout=5)
            except subprocess.TimeoutExpired:
                child.kill()
                child.wait()
            raise


def inventariar(root):
    records = []
    def visit(folder):
        for item in sorted(folder.iterdir()):
            p = montagem.sem_links(item)
            if p.is_dir():
                visit(p)
            elif p.is_file() and p != root / 'fechamento.json':
                records.append({'arquivo': p.relative_to(root).as_posix(), 'sha256': montagem.sha(p.read_bytes())})
    visit(root)
    return records


def identidade_adaptador(argv):
    records = []
    for arg in argv:
        path = Path(arg)
        if path.is_absolute() and path.is_file():
            path = montagem.sem_links(path)
            records.append({'arquivo': str(path), 'sha256': montagem.sha(path.read_bytes())})
    return records


def conferir_fechamento(root):
    closing = ler(root / 'fechamento.json')
    for item in closing['arquivos']:
        if montagem.sha(relativo(root, item['arquivo']).read_bytes()) != item['sha256']:
            raise ValueError('captura alterada: ' + item['arquivo'])
    if {i['arquivo'] for i in closing['arquivos']} != {i['arquivo'] for i in inventariar(root)}:
        raise ValueError('captura com arquivos extras/ausentes')
    return ler(root / 'tentativa.json')


def _capturar(path, lote, substituto, continuar=False, limite=None, executor=subprocesso, real=False):
    """Motor comum; adaptador real so e alcancavel apos o gate iniciar_real.

    Nao existe flag que promova controles a LLM/piloto. Nenhum retry por
    validade/qualidade. O caminho real permanece bloqueado no gate D-29.
    """
    path = montagem.sem_links(path)
    plan = conferir_plano(path)
    out = montagem.sem_links(lote)
    origin, phase = ('real', 'piloto') if real else ('sintetica', 'verificacao_sintetica')
    adapter = ['codex exec'] if real else list(substituto)
    binaries = identidade_adaptador([shutil.which('codex')]) if real else identidade_adaptador(adapter)
    if not continuar:
        out.mkdir(parents=True, exist_ok=False)
        salvar(out / 'plano-original.json', path.read_bytes())
        salvar_json(out / 'lote.json', {'origem': origin, 'fase': phase,
                    'plano_sha256': montagem.sha(path.read_bytes()), 'substituto': adapter,
                    'adaptador_arquivos': binaries,
                    'coletor_sha256': montagem.sha(Path(__file__).read_bytes()), 'versao': VERSAO})
    header = ler(out / 'lote.json')
    if (header['origem'] != origin or header['fase'] != phase
            or header['plano_sha256'] != montagem.sha(path.read_bytes())
            or (out / 'plano-original.json').read_bytes() != path.read_bytes()
            or header['coletor_sha256'] != montagem.sha(Path(__file__).read_bytes())
            or header['adaptador_arquivos'] != binaries
            or header['substituto'] != adapter):
        raise ValueError('plano/configuracao/versao/substituto mudou; continuacao bloqueada')
    # Lock exclusivo; nunca recuperar automaticamente um processo ainda ativo.
    lock = out / 'coletor.lock'
    with lock.open('x') as stream:
        stream.write(str(os.getpid()))
    count = 0
    sessions = set()
    try:
        for row in plan['observacoes']:
            obs = out / row['observacao_id']
            prior, final = None, False
            for number in (1, 2):
                attempt_dir = obs / f'T{number:02}'
                if not attempt_dir.exists():
                    break
                if not (attempt_dir / 'fechamento.json').exists():
                    raise ValueError('tentativa interrompida/ambigua: usar recuperar, sem reenvio automatico')
                prior = conferir_fechamento(attempt_dir)
                if prior.get('sessao'):
                    if prior['sessao'] in sessions:
                        raise ValueError('sessao compartilhada entre tentativas')
                    sessions.add(prior['sessao'])
                if prior.get('interrompida'):
                    raise ValueError('envio interrompido: estado remoto desconhecido; conferir antes de nova tentativa')
                if prior.get('desvios'):
                    raise ValueError('desvio previo preservado; continuacao bloqueada para conferencia')
                final = prior['estado_tecnico'] == 'concluida' or number == 2
                if final:
                    break
            if final:
                continue
            if limite is not None and count >= limite:
                break
            # Reconfere todos os bytes e configuracao imediatamente antes de cada tentativa.
            conferir_plano(path)
            current_binaries = identidade_adaptador([shutil.which('codex')]) if real else identidade_adaptador(adapter)
            if current_binaries != binaries:
                raise ValueError('executavel/substituto alterado durante lote')
            number = 1 if prior is None else 2
            attempt_dir = obs / f'T{number:02}'
            attempt_dir.mkdir(parents=True, exist_ok=False)
            prep_path = relativo(path.parent, row['preparacao'])
            prep = conferir_preparacao(prep_path)
            for name in ['preparacao.json'] + [e['arquivo'] for e in prep['arquivos']]:
                salvar(attempt_dir / 'preparacao' / name, (prep_path.parent / name).read_bytes())
            payload = (prep_path.parent / 'payload.txt').read_bytes()
            salvar(attempt_dir / 'entrada.bin', payload)
            work = attempt_dir / 'ambiente'
            work.mkdir()
            argv = comando_codex(shutil.which('codex'), work) if real else list(substituto)
            start = instante()
            salvar_json(attempt_dir / 'inicio.json', {'instante': start, 'argv': argv,
                        'cwd': str(work), 'origem': origin, 'fase': phase,
                        'ambiente_chaves_permitidas': sorted(ambiente_filho()),
                        'configuracao': plan['configuracao']})
            label = 'PILOTO' if real else 'CONTROLE'
            print(f"[{row['ordem']}/16] {label} {row['observacao_id']} T{number:02} -> {attempt_dir}", flush=True)
            interrupted, cause, code = False, None, None
            try:
                code = executor(argv, payload, work, attempt_dir / 'eventos.jsonl', attempt_dir / 'stderr.bin')
            except KeyboardInterrupt:
                interrupted, cause = True, 'interrupcao; processamento remoto nao pode ser presumido'
            except OSError as exc:
                cause = str(exc)
            events_path = attempt_dir / 'eventos.jsonl'
            parsed = extrair_eventos(events_path.read_bytes() if events_path.exists() else b'')
            response = parsed['resposta']
            for index, message in enumerate(parsed['mensagens'], 1):
                salvar(attempt_dir / f'mensagem-{index:02}.bin', message)
            if response is not None:
                salvar(attempt_dir / 'resposta.bin', response)
            # Final integral recebido nunca e repetido devido ao retorno do wrapper.
            complete = parsed['completo'] and not interrupted
            deviations = parsed['desvios']
            if complete and code != 0:
                deviations.append('processo com final integral e retorno diferente de zero')
            if parsed['sessao'] and parsed['sessao'] in sessions:
                deviations.append('sessao compartilhada entre tentativas/observacoes')
            if parsed['sessao']:
                sessions.add(parsed['sessao'])
            record = {k: row[k] for k in ('observacao_id', 'configuracao_id', 'mudanca', 'condicao', 'payload_sha256')}
            record.update(origem=origin, fase=phase,
                          tentativa_id=row['observacao_id'] + f'-T{number:02}',
                          tentativa_anterior=prior['tentativa_id'] if prior else None,
                          preparacao_id=prep['preparacao_id'], preparacao_sha256=row['preparacao_sha256'],
                          entrada_enviada_arquivo='entrada.bin', entrada_enviada_sha256=montagem.sha(payload),
                          resposta_arquivo='resposta.bin' if response is not None else None,
                          resposta_sha256=montagem.sha(response) if response is not None else None,
                          resposta_tamanho=len(response) if response is not None else None,
                          estado_tecnico='concluida' if complete else 'falha_tecnica', fragmento=not complete,
                          causa=None if complete else cause or f'processo/eventos incompletos; retorno={code}',
                          retorno_processo=code, instante_execucao=start, instante_fim=instante(),
                          origem_resposta='codex exec; eventos.jsonl; item.completed' if real else 'CONTROLE ARTIFICIAL; processo substituto local; sem LLM',
                          modelo_solicitado=MODELO, modelo_reportado=parsed['modelo_reportado'] if real else None,
                          modelo_reportado_indisponibilidade=(None if parsed['modelo_reportado'] else 'CLI nao expos modelo efetivo nos eventos') if real else 'controle local nao representa modelo',
                          sessao=parsed['sessao'],
                          transporte_observavel={k: parsed[k] for k in (
                              'erros_cliente_observados', 'turnos_iniciados_observados',
                              'retentativas_transporte_observadas')},
                          configuracao=plan['configuracao'],
                          versoes={'coletor': VERSAO, 'pacote': prep['versao_pacote'],
                                   'documentos': {e['arquivo']: {'versao': e['versao'], 'sha256': e['sha256']}
                                                 for e in prep['documentos']}},
                          conformidade_protocolo='desvio' if deviations else 'pendente', desvios=deviations,
                          interrompida=interrupted, texto_extraido_de='ultimo item.completed agent_message.text')
            record['repeticao' if real else 'repeticao_sintetica'] = row['repeticao']
            salvar_json(attempt_dir / 'tentativa.json', record)
            salvar_json(attempt_dir / 'fechamento.json', {'arquivos': inventariar(attempt_dir)})
            count += 1
            if interrupted:
                return 130
            if deviations:
                print('Desvio detectado; lote interrompido para conferencia.', flush=True)
                return 2
            if not complete:
                print('Falha tecnica preservada; corrigir indisponibilidade e continuar explicitamente.', flush=True)
                return 1
        return 0
    finally:
        lock.unlink()  # Somente o lock criado neste processo; evidencias nunca apagadas.


def recuperar(lote):
    """Fecha captura parcial sem reenviar. Estado ambiguo continua bloqueando retry."""
    out = montagem.sem_links(lote)
    if (out / 'coletor.lock').exists():
        raise ValueError('lock presente: conferir processo ativo antes de remover SOMENTE o lock')
    plan = ler(out / 'plano-original.json')
    recovered = 0
    for row in plan['observacoes']:
        for number in (1, 2):
            root = out / row['observacao_id'] / f'T{number:02}'
            if not root.exists() or (root / 'fechamento.json').exists():
                continue
            if not (root / 'tentativa.json').exists():
                raise ValueError('captura parcial preservada; sem registro final, estado ambiguo; nao reenviar')
            salvar_json(root / 'fechamento.json', {'arquivos': inventariar(root), 'recuperado_sem_envio': instante()})
            recovered += 1
    return {'recuperados_sem_envio': recovered}


def iniciar_real(path, lote, enviar_real=False, continuar=False, limite=None):
    conferir_plano(path)
    protegida(lote, 'captura')
    if not enviar_real:
        raise ValueError('envio exige --enviar-real; nenhuma chamada realizada')
    verificar_liberacao_real()
    return _capturar(path, lote, None, continuar=continuar, limite=limite, real=True)


def verificar_liberacao_real():
    # Nao ha opcao --ignorar-bloqueios ou declaracao humana que simule prova tecnica.
    # Remover este gate exige novo incremento com evidencia dos controles D-29.
    raise ValueError('ENVIO REAL BLOQUEADO: ' + ' '.join(BLOQUEIOS))


def avaliar_lote(lote, referencia, saida):
    # Importacao tardia: o caminho de captura nao importa nem consulta o gabarito.
    import avaliacao_ids as avaliador
    out = protegida(saida, 'avaliados')
    root = montagem.sem_links(lote)
    header = ler(root / 'lote.json')
    origin, phase = header['origem'], header['fase']
    if (origin, phase) not in (('sintetica', 'verificacao_sintetica'), ('real', 'piloto')):
        raise ValueError('origem/fase do lote incompativeis')
    plan = ler(root / 'plano-original.json')
    out.mkdir(parents=True, exist_ok=False)
    selected, observations = [], []
    code = 0
    for row in plan['observacoes']:
        observations.append({**{k: row[k] for k in ('observacao_id', 'configuracao_id', 'mudanca', 'condicao', 'payload_sha256')},
                             'origem': origin, 'fase': phase,
                             'repeticao' if origin == 'real' else 'repeticao_sintetica': row['repeticao']})
        for number in (1, 2):
            attempt = root / row['observacao_id'] / f'T{number:02}'
            if not attempt.exists():
                continue
            conferir_fechamento(attempt)
            target = out / row['observacao_id'] / f'T{number:02}'
            result, status = avaliador.avaliar(attempt / 'preparacao/preparacao.json', attempt / 'tentativa.json',
                                               referencia, target, origem=origin, fase=phase)
            code = max(code, status)
            selected.append({'arquivo': (target / 'avaliacao.json').relative_to(out).as_posix(),
                             'sha256': montagem.sha((target / 'avaliacao.json').read_bytes())})
    salvar_json(out / 'lista.json', selected)
    salvar_json(out / 'observacoes.json', observations)
    _, status = avaliador.resumir(out / 'lista.json', out / 'observacoes.json', out / 'resumo', origem=origin, fase=phase)
    return max(code, status)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='comando', required=True)
    p = sub.add_parser('ambiente', help='consultas locais; nunca envia prompts')
    p.add_argument('--saida', required=True, type=Path)
    p = sub.add_parser('preparar', help='registra ordem e remonta oito pacotes v2-LF')
    p.add_argument('--saida', required=True, type=Path)
    p.add_argument('--ordem-registrada', type=Path)
    p = sub.add_parser('simular', help='confere bytes e mostra argv; nenhum modelo/processo iniciado')
    p.add_argument('--plano', required=True, type=Path)
    p = sub.add_parser('iniciar', help='futuro piloto; BLOQUEADO pelos controles D-29 pendentes')
    p.add_argument('--plano', required=True, type=Path)
    p.add_argument('--lote', required=True, type=Path)
    p.add_argument('--enviar-real', action='store_true')
    p.add_argument('--continuar', action='store_true')
    p.add_argument('--limite', type=int, help='pausar entre observacoes apos N tentativas; nao muda a configuracao')
    p = sub.add_parser('controle', help='APENAS processo substituto fixo, sintetico, local e sem rede')
    p.add_argument('--plano', required=True, type=Path)
    p.add_argument('--lote', required=True, type=Path)
    p.add_argument('--continuar', action='store_true')
    p.add_argument('--limite', type=int)
    p = sub.add_parser('recuperar', help='recupera arquivos locais sem enviar ou retomar conversa')
    p.add_argument('--lote', required=True, type=Path)
    p = sub.add_parser('avaliar', help='etapa separada; importa respostas preservadas e chama avaliador existente')
    p.add_argument('--lote', required=True, type=Path)
    p.add_argument('--referencia', required=True, type=Path)
    p.add_argument('--saida', required=True, type=Path)
    args = parser.parse_args(argv)
    try:
        if args.comando == 'ambiente':
            print(json.dumps(conferir_ambiente(args.saida), ensure_ascii=True))
        elif args.comando == 'preparar':
            print(preparar_plano(args.saida, args.ordem_registrada))
        elif args.comando == 'simular':
            print(serial(simular(args.plano)).decode('ascii'), end='')
        elif args.comando == 'iniciar':
            iniciar_real(args.plano, args.lote, args.enviar_real, args.continuar, args.limite)
        elif args.comando == 'controle':
            protegida(args.lote, 'captura')
            return _capturar(args.plano, args.lote, [sys.executable, '-B', str(RAIZ / 'tests/substituto_coletor.py')],
                             args.continuar, args.limite)
        elif args.comando == 'recuperar':
            protegida(args.lote, 'captura')
            print(recuperar(args.lote))
        elif args.comando == 'avaliar':
            return avaliar_lote(args.lote, args.referencia, args.saida)
        return 0
    except (ValueError, OSError, KeyError, TypeError, subprocess.TimeoutExpired) as exc:
        print(str(exc), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
