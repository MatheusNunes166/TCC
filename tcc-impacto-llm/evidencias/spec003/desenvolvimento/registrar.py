"""Capture comandos de desenvolvimento em pastas novas, sem sobrescrever logs."""
import hashlib
import json
import pathlib
import subprocess
import sys
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).resolve().parents[3]


def main():
    label, *command = sys.argv[1:]
    output = ROOT / 'evidencias' / 'spec003' / label
    output.mkdir(parents=True, exist_ok=False)
    if command == ['inventario']:
        paths = subprocess.check_output(['git', 'diff', '--name-only'], cwd=ROOT).decode().splitlines()
        prefix = subprocess.check_output(['git', 'rev-parse', '--show-prefix'], cwd=ROOT).decode().strip()
        local = {}
        for path in paths:
            relative = path.removeprefix(prefix)
            data = (ROOT / relative).read_bytes()
            target = output / 'alteracoes-locais-iniciais' / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
            local[relative] = hashlib.sha256(data).hexdigest()
        result = {'tipo': 'inventario_sem_execucao_da_bancada', 'locais': local}
        for args in (['status', '--short'], ['rev-parse', 'HEAD'], ['rev-parse', '--show-toplevel'],
                     ['rev-parse', '--show-prefix'], ['cat-file', '-t', 'aec474bcb54d6dae2afceff8e5b9226991386490']):
            result['git ' + ' '.join(args)] = subprocess.check_output(['git', *args], cwd=ROOT).decode()
        result['python'] = sys.version
        result['executable'] = sys.executable
        (output / 'inventario.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    completed = subprocess.run(command, cwd=ROOT, capture_output=True)
    (output / 'stdout.txt').write_bytes(completed.stdout)
    (output / 'stderr.txt').write_bytes(completed.stderr)
    # Snapshot the exact new sources for each red/green checkpoint.
    for name in ('verificacao_variantes.py', 'tests/test_variantes.py'):
        path = ROOT / name
        if path.exists():
            target = output / 'fontes' / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(path.read_bytes())
    record = dict(tipo='controle_sintetico' if 'sintetico' in label else 'comando_real',
                  comando=command, cwd=str(ROOT), retorno=completed.returncode,
                  python=sys.version, instante_utc=datetime.now(timezone.utc).isoformat())
    (output / 'comando.json').write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(record, ensure_ascii=False))
    print(completed.stdout.decode('utf-8', errors='replace'))
    print(completed.stderr.decode('utf-8', errors='replace'))
    return completed.returncode


if __name__ == '__main__':
    raise SystemExit(main())
