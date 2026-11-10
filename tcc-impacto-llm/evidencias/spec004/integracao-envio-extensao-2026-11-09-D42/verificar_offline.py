"""D-42: regressao local da integracao; rede bloqueada, sem chave real.

Executar na raiz do projeto com Python -B. --saida deve ser pasta nova.
"""
import argparse
import contextlib
import io
import json
from pathlib import Path
import subprocess
import sys
import time
import unittest

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(ROOT), str(ROOT / 'tests')]


def sem_rede(event, args):
    if event in ('socket.connect', 'socket.getaddrinfo', 'socket.gethostbyname'):
        raise AssertionError('D-42: rede proibida nesta verificacao offline')


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--saida', type=Path, default=HERE / 'verificacao-001')
    args = p.parse_args()
    args.saida.mkdir(parents=True, exist_ok=False)
    sys.addaudithook(sem_rede)
    import extensao_exploratoria as e
    modules = ['test_envio_extensao', 'test_extensao_exploratoria', 'test_coletor_api',
               'test_transporte_api', 'test_revisao_conformidade', 'test_controles_cli']
    suite = unittest.defaultTestLoader.loadTestsFromNames(modules)
    log = io.StringIO()
    start = time.monotonic()
    with contextlib.redirect_stdout(log), contextlib.redirect_stderr(log):
        result = unittest.TextTestRunner(stream=log, verbosity=2).run(suite)
    (args.saida / 'unittest.txt').write_bytes(log.getvalue().encode())
    planpath = ROOT / 'captura/extensao-20261109-003/plano.json'
    plan = e.conferir(planpath)
    oldpath = ROOT / 'captura/extensao-20261109-002/plano.json'
    old = e.api.base.ler(oldpath)
    fields = ('observacao_id', 'ordem', 'bloco', 'repeticao', 'mudanca', 'condicao', 'modelo', 'payload_sha256')
    same_rows = len(plan['observacoes']) == len(old['observacoes']) == 64 and all(
        all(new[k] == previous[k] for k in fields) for new, previous in zip(plan['observacoes'], old['observacoes']))
    initial = e.api.base.ler(HERE / 'estado-inicial.json')['sha256_anteriores']
    replaced = {'coletor_api.py', 'extensao_exploratoria.py', 'revisao_conformidade.py', 'tests/test_extensao_exploratoria.py'}
    missing = []
    for name, h in initial.items():
        source = HERE / 'fontes-anteriores' / name if name in replaced else ROOT / name
        if not source.is_file() or e.api.sha(source.read_bytes()) != h:
            missing.append(name)
    summary = {'comando': [sys.executable, '-B', *sys.argv], 'python': sys.version,
        'modulos': modules, 'metodos': result.testsRun, 'falhas': len(result.failures),
        'erros': len(result.errors), 'ignorados': len(result.skipped),
        'duracao_segundos': round(time.monotonic() - start, 3),
        'rede_bloqueada_por_audit_hook': True, 'chave_real_utilizada': False,
        'envios_api_reais': 0, 'captura_real_exercitada_somente_com_substituto_em_temporarios': True,
        'ordem_e_64_itens_payloads_preservados': same_rows,
        'ordem_json_literal_preservada': (planpath.parent / 'ordem.json').read_bytes() == (oldpath.parent / 'ordem.json').read_bytes(),
        'referencia_sha256_preservada': plan['referencia_sha256'] == old['referencia_sha256'],
        'orcamento_declarado_usd': plan['orcamento_declarado_usd'], 'teto_monetario_implementado': False,
        'arquivos_anteriores_conferidos': len(initial), 'divergencias_anteriores': missing,
        'plano_vigente_sha256': e.api.sha(planpath.read_bytes()),
        'fontes_testadas_sha256': {name: e.api.sha((ROOT / name).read_bytes()) for name in (
            'coletor_api.py', 'extensao_exploratoria.py', 'coletor_piloto.py', 'revisao_conformidade.py',
            'tests/test_envio_extensao.py', 'tests/test_extensao_exploratoria.py')}}
    summary['conforme'] = result.wasSuccessful() and not missing and same_rows and summary['ordem_json_literal_preservada']
    (args.saida / 'resultado.json').write_bytes(e.api.bytes_json(summary))
    print(json.dumps(summary, indent=2))
    return 0 if summary['conforme'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
