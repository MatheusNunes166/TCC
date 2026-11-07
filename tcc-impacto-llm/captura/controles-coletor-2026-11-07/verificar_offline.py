"""Registra somente controles artificiais locais; nao executa Codex ou LLM."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent


def main():
    records = []
    for pattern in ('test_coletor_piloto.py', 'test_avaliacao*.py',
                    'test_montagem_entradas.py', 'test_fontes_autorizadas.py'):
        argv = [sys.executable, '-B', '-m', 'unittest', 'discover', '-s', 'tests', '-p', pattern, '-v']
        result = subprocess.run(argv, cwd=ROOT, capture_output=True)
        name = pattern.replace('*', '-todos-').replace('.py', '')
        for suffix, data in [('stdout.bin', result.stdout), ('stderr.bin', result.stderr)]:
            with (OUT / (name + '-' + suffix)).open('xb') as stream:
                stream.write(data)
        records.append({'argv': argv, 'retorno': result.returncode,
                        'stdout_sha256': hashlib.sha256(result.stdout).hexdigest(),
                        'stderr_sha256': hashlib.sha256(result.stderr).hexdigest()})
        print(pattern, result.returncode, flush=True)
    sources = []
    for name in ('coletor_piloto.py', 'avaliacao_ids.py', 'montagem_entradas.py',
                 'tests/test_coletor_piloto.py', 'tests/substituto_coletor.py', 'tests/test_avaliacao_real.py'):
        data = (ROOT / name).read_bytes()
        destination = OUT / 'fontes' / name
        destination.parent.mkdir(parents=True, exist_ok=True)
        with destination.open('xb') as stream:
            stream.write(data)
        sources.append({'arquivo': name, 'sha256': hashlib.sha256(data).hexdigest()})
    with (OUT / 'testes.json').open('x', encoding='utf-8', newline='\n') as stream:
        json.dump({'tipo': 'CONTROLES_ARTIFICIAIS_SEM_LLM', 'python': sys.version,
                   'consultas': records, 'fontes': sources}, stream, indent=2)
        stream.write('\n')
    return max(r['retorno'] for r in records)


if __name__ == '__main__':
    raise SystemExit(main())
