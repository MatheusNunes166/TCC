"""Inspecao local do parser/configuracao por IPC stdio, sem criar thread/turno.

Metodos permitidos: initialize, initialized, config/read. Nenhum prompt, modelo,
MCP ou servidor HTTP e iniciado pelo script. Nao grava configuracao completa.
"""
import json
from pathlib import Path
import queue
import shutil
import subprocess
import sys
import threading

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
import coletor_piloto as c

KEYS = ('model', 'model_provider', 'model_reasoning_effort', 'web_search',
        'project_doc_max_bytes', 'skills', 'memories', 'features', 'sandbox_mode')


def resumo(config):
    result = {k: config[k] for k in KEYS if k in config}
    result['instrucoes_configuradas'] = {
        k: {'presente': bool(config.get(k)), 'sha256': c.montagem.sha(str(config[k]).encode()) if config.get(k) else None}
        for k in ('developer_instructions', 'model_instructions_file', 'instructions')}
    result['mcp'] = {name: {'enabled': server.get('enabled', True)}
                     for name, server in config.get('mcp_servers', {}).items()}
    result['plugins_configurados'] = sorted(config.get('plugins', {}))
    result['providers'] = {name: {k: provider[k] for k in (
        'name', 'request_max_retries', 'stream_max_retries', 'requires_openai_auth', 'wire_api') if k in provider}
        for name, provider in config.get('model_providers', {}).items()}
    return result


def consultar(values):
    binary = shutil.which('codex')
    argv = [binary, 'app-server', '--strict-config', '--listen', 'stdio://']
    for value in ['analytics.enabled=false', 'web_search="disabled"', 'project_doc_max_bytes=0', *values]:
        argv.extend(['-c', value])
    for feature in c.DESATIVAR:
        argv.extend(['--disable', feature])
    child = subprocess.Popen(argv, cwd=ROOT, env=c.ambiente_filho(),
                             stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    messages, errors, q = [], [], queue.Queue()
    def reader(stream, target, is_out):
        for line in stream:
            target.append(line)
            if is_out:
                q.put(line)
        if is_out:
            q.put(None)
    readers = [threading.Thread(target=reader, args=(child.stdout, messages, True), daemon=True),
               threading.Thread(target=reader, args=(child.stderr, errors, False), daemon=True)]
    for thread in readers:
        thread.start()
    def send(message):
        assert message['method'] in ('initialize', 'initialized', 'config/read')
        child.stdin.write((json.dumps(message) + '\n').encode())
        child.stdin.flush()
    def response(identifier):
        while True:
            line = q.get(timeout=15)
            if line is None:
                return None
            value = json.loads(line)
            if value.get('id') == identifier:
                return value
    result, diagnostic = None, None
    try:
        send({'id': 1, 'method': 'initialize', 'params': {'clientInfo': {'name': 'D38_inspecao_offline', 'version': '1'},
              'capabilities': {'experimentalApi': True}}})
        init = response(1)
        if init and 'result' in init:
            send({'method': 'initialized'})
            send({'id': 2, 'method': 'config/read', 'params': {'includeLayers': True, 'cwd': str(ROOT)}})
            value = response(2)
            if value and 'result' in value:
                data = value['result']
                result = {'config': resumo(data['config']),
                          'layers': [{'source': layer.get('name', layer.get('source')), 'disabledReason': layer.get('disabledReason')}
                                     for layer in data.get('layers') or []],
                          'origins': {k: v for k, v in data.get('origins', {}).items() if k in KEYS}}
            else:
                diagnostic = value
        else:
            diagnostic = init
    except (BrokenPipeError, queue.Empty, ValueError) as exc:
        diagnostic = type(exc).__name__
    finally:
        child.stdin.close()
        try:
            child.wait(timeout=5)
        except subprocess.TimeoutExpired:
            child.terminate()
            child.wait(timeout=5)
        for thread in readers:
            thread.join(timeout=2)
    return {'argv': argv, 'retorno': child.returncode, 'resultado': result,
            'diagnostico': diagnostic, 'stderr': b''.join(errors).decode('utf-8', errors='replace'),
            'limite': 'config/read de app-server; nao e exec --ignore-user-config nem prova do transporte'}


def main():
    probes = {
        'base': [],
        'custom-zero': ['model_providers.controle.name="Controle sem chamadas"',
                        'model_providers.controle.request_max_retries=0', 'model_providers.controle.stream_max_retries=0'],
        'custom-negative': ['model_providers.controle.name="Controle sem chamadas"',
                            'model_providers.controle.request_max_retries=-1'],
        'custom-stream-negative': ['model_providers.controle.name="Controle sem chamadas"',
                                   'model_providers.controle.stream_max_retries=-1'],
        'builtin-zero': ['model_providers.openai.name="Controle sem chamadas"',
                        'model_providers.openai.request_max_retries=0', 'model_providers.openai.stream_max_retries=0'],
        'context-controls': ['skills.include_instructions=false', 'memories.generate_memories=false',
                             'memories.use_memories=false', 'model_provider="openai"'],
        'unknown-key': ['D38_chave_deliberadamente_inexistente=true'],
    }
    for name, values in probes.items():
        record = consultar(values)
        c.salvar_json(OUT / ('config-' + name + '.json'), record)
        print(name, record['retorno'], bool(record['resultado']), record['diagnostico'], flush=True)


if __name__ == '__main__':
    main()
