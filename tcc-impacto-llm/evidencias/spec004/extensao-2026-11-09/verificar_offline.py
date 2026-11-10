"""Executa suites existentes e D-41 com rede bloqueada; conserva logs e matriz 75.

Uso na raiz: python -B evidencias/spec004/extensao-2026-11-09/verificar_offline.py
Use --saida com diretorio NOVO para repetir sem sobrescrever evidencias.
"""
import argparse
import contextlib
import io
import json
from pathlib import Path
import sys
import time
import unittest

ROOT = Path(__file__).resolve().parents[3]
EVIDENCE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / 'tests'))


def block_network(event, args):
    if event in ('socket.connect', 'socket.getaddrinfo', 'socket.gethostbyname'):
        raise AssertionError('D-41: rede proibida na verificacao offline')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--saida', type=Path, default=EVIDENCE / 'verificacao-final')
    args = parser.parse_args()
    args.saida.mkdir(parents=True, exist_ok=False)
    sys.addaudithook(block_network)
    import avaliacao_ids as a
    from test_extensao_exploratoria import matriz, REF
    expected = a.json_estrito((EVIDENCE / 'expectativas-antes-execucao.json').read_bytes())
    if a.sha(REF.read_bytes()) != expected['sha256']:
        raise ValueError('expectativas mudaram apos registro anterior a execucao')
    log = io.StringIO()
    start = time.monotonic()
    suite = unittest.defaultTestLoader.discover(str(ROOT / 'tests'))
    with contextlib.redirect_stdout(log), contextlib.redirect_stderr(log):
        result = unittest.TextTestRunner(stream=log, verbosity=2).run(suite)
    (args.saida / 'unittest.txt').write_bytes(log.getvalue().encode('utf-8'))
    rows = matriz()
    (args.saida / 'bancada-75.json').write_bytes(a.serial({'referencia_sha256': expected['sha256'],
        'tipo': 'execucao_local_bancada_sem_LLM', 'resultados': rows}))
    summary = {'comando': [sys.executable, '-B', *sys.argv], 'python': sys.version,
               'rede_bloqueada_por_audit_hook': True, 'chave_real_utilizada': False,
               'duracao_segundos': round(time.monotonic() - start, 3),
               'metodos': result.testsRun, 'falhas': len(result.failures), 'erros': len(result.errors),
               'ignorados': [{'teste': str(t), 'motivo': reason} for t, reason in result.skipped],
               'sucesso': result.wasSuccessful(),
               'baseline': 15, 'variantes': 60, 'comparacoes': len(rows),
               'conformes': sum(r['conforme'] for r in rows),
               'fontes_sha256': {name: a.sha((ROOT / name).read_bytes()) for name in (
                   'coletor_api.py', 'avaliacao_ids.py', 'extensao_exploratoria.py',
                   'montagem_entradas.py', 'tests/test_extensao_exploratoria.py', 'autorizacao.py',
                   'variantes/mc01.py', 'variantes/mc02.py', 'variantes/mc03.py', 'variantes/mc04.py')}}
    (args.saida / 'resultado.json').write_bytes(a.serial(summary))
    print(json.dumps(summary, ensure_ascii=True, indent=2))
    return 0 if result.wasSuccessful() and summary['conformes'] == 75 else 1


if __name__ == '__main__':
    raise SystemExit(main())
