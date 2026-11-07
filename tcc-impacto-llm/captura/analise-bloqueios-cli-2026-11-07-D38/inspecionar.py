"""Consulta local delimitada da CLI instalada; NUNCA executa exec/turn/start.

Todos os subprocessos recebem o mesmo ambiente filtrado do coletor.
Nao le auth.json, nao inicia MCP, nao atualiza catalogos e nao envia prompts.
"""
from datetime import datetime, timezone
import json
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
import coletor_piloto as c


def main():
    binary = shutil.which('codex')
    records = []
    queries = [('versao', ['--version']), ('exec-ajuda', ['exec', '--help']),
               ('autenticacao', ['login', 'status']), ('features', ['features', 'list'])]
    probes = {
        'builtin-retries-zero': ['model_providers.openai.request_max_retries=0', 'model_providers.openai.stream_max_retries=0'],
        'custom-zero': ['model_providers.controle.name="Controle local sem chamadas"',
                        'model_providers.controle.base_url="http://127.0.0.1:1/v1"',
                        'model_providers.controle.request_max_retries=0', 'model_providers.controle.stream_max_retries=0'],
        'custom-one': ['model_providers.controle.name="Controle local sem chamadas"',
                      'model_providers.controle.request_max_retries=1', 'model_providers.controle.stream_max_retries=1'],
        'custom-negative': ['model_providers.controle.name="Controle local sem chamadas"',
                           'model_providers.controle.request_max_retries=-1'],
        'custom-stream-negative': ['model_providers.controle.name="Controle local sem chamadas"',
                                  'model_providers.controle.stream_max_retries=-1'],
        'custom-string': ['model_providers.controle.name="Controle local sem chamadas"',
                         'model_providers.controle.request_max_retries="zero"'],
        'controle-chave-inexistente': ['D38_chave_deliberadamente_inexistente=true'],
        'skills-instructions': ['skills.include_instructions=false'],
        'memory-controls': ['memories.generate_memories=false', 'memories.use_memories=false'],
        'provider-openai': ['model_provider="openai"'],
    }
    for name, values in probes.items():
        argv = ['--strict-config']
        for value in values:
            argv.extend(['-c', value])
        queries.append((name, argv + ['features', 'list']))
    for name, args in queries:
        cp = subprocess.run([binary, *args], env=c.ambiente_filho(), cwd=ROOT,
                            capture_output=True, timeout=30)
        c.salvar(OUT / (name + '-stdout.bin'), cp.stdout)
        c.salvar(OUT / (name + '-stderr.bin'), cp.stderr)
        records.append({'nome': name, 'argv': [binary, *args], 'retorno': cp.returncode,
                        'stdout_sha256': c.montagem.sha(cp.stdout), 'stderr_sha256': c.montagem.sha(cp.stderr)})
        print(name, cp.returncode, flush=True)
    c.salvar(OUT / 'coletor-antes-D38.py', (ROOT / 'coletor_piloto.py').read_bytes())
    c.salvar_json(OUT / 'inspecao.json', {'instante': datetime.now(timezone.utc).isoformat(),
                   'python': sys.version, 'binary': binary, 'binary_sha256': c.montagem.sha(Path(binary).read_bytes()),
                   'ambiente_chaves': sorted(c.ambiente_filho()), 'consultas': records,
                   'limite': 'features list valida parsing, nao prova aplicacao na rota exec nem semantica de transporte'})


if __name__ == '__main__':
    main()
