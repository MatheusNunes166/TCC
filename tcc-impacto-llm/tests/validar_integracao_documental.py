"""Regressão técnica offline, sem DNS/rede externa. Grava logs novos de evidência."""
import argparse
import json
import os
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT/'tests'))
os.environ.pop('OPENAI_API_KEY', None)


def offline(event, args):
    if event in ('socket.connect', 'socket.getaddrinfo', 'socket.gethostbyname'):
        address = args[1] if event == 'socket.connect' else args[0]
        host = address[0] if isinstance(address, tuple) else address
        if host not in ('127.0.0.1', 'localhost', '::1'):
            raise AssertionError('Rede/DNS externo proibido nesta verificação')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--somente-novos', action='store_true')
    args = parser.parse_args()
    sys.addaudithook(offline)
    area = ROOT/'evidencias/spec004/integracao-documental-64-2026-11-22'
    area.mkdir(parents=True, exist_ok=True)
    pattern = 'test_documentacao_operacional_64.py' if args.somente_novos else 'test_*.py'
    suite = unittest.defaultTestLoader.discover(str(ROOT/'tests'), pattern=pattern)
    stem = 'testes-documentais-final' if args.somente_novos else 'testes-completos'
    with (area/(stem+'.txt')).open('w', encoding='utf-8') as stream:
        result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
    failed = {str(t) for t, _ in result.errors+result.failures}
    report = {'testes_descobertos': result.testsRun,
        'aprovados': result.testsRun-len(failed)-len(result.skipped),
        'falhas':len(result.failures), 'erros':len(result.errors),
        'ignorados':[{'teste':str(t),'motivo':why} for t,why in result.skipped],
        'origem': 'offline; HTTP artificial ou loopback; chave real removida', 'chamadas_reais':0}
    (area/(stem+'.json')).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2))
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    raise SystemExit(main())
