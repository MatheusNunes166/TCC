"""Verificacoes do coletor D-38 exclusivamente offline; nao executa Codex."""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
import coletor_piloto as c


def run(name, args, expected):
    argv = [sys.executable, '-B', *args]
    cp = subprocess.run(argv, cwd=ROOT, capture_output=True)
    c.salvar(OUT / (name + '-stdout.bin'), cp.stdout)
    c.salvar(OUT / (name + '-stderr.bin'), cp.stderr)
    print(name, cp.returncode, flush=True)
    assert cp.returncode == expected
    return {'argv': argv, 'retorno': cp.returncode, 'esperado': expected}


def main():
    records = []
    for name in ('test_controles_cli.py', 'test_coletor_piloto.py'):
        records.append(run(name[:-3], ['-m', 'unittest', 'discover', '-s', 'tests', '-p', name, '-v'], 0))
    original = ROOT / 'captura/planejamento-piloto-2026-11-07/plano.json'
    plan = c.preparar_plano(ROOT / 'captura/planejamento-piloto-2026-11-07-D38', original)
    old, new = c.ler(original), c.ler(plan)
    assert [r['observacao_id'] for r in old['observacoes']] == [r['observacao_id'] for r in new['observacoes']]
    assert [r['payload_sha256'] for r in old['observacoes']] == [r['payload_sha256'] for r in new['observacoes']]
    records.append(run('simulacao-D38', ['coletor_piloto.py', 'simular', '--plano', str(plan)], 0))
    records.append(run('trava-real-D38', ['coletor_piloto.py', 'iniciar', '--plano', str(plan),
                                       '--lote', 'captura/piloto/D38-NAO-CRIAR', '--enviar-real'], 2))
    assert not (ROOT / 'captura/piloto/D38-NAO-CRIAR').exists()
    sources = []
    for name in ('coletor_piloto.py', 'tests/test_controles_cli.py', 'tests/test_coletor_piloto.py'):
        data = (ROOT / name).read_bytes()
        c.salvar(OUT / 'fontes-D38' / name, data)
        sources.append({'arquivo': name, 'sha256': c.montagem.sha(data)})
    c.salvar_json(OUT / 'validacao-offline.json', {'tipo': 'CONTROLES_ARTIFICIAIS_SEM_LLM',
                   'consultas': records, 'fontes': sources, 'ordem_anterior_preservada': True,
                   'payloads_anteriores_preservados': True, 'envio_real_bloqueado': True,
                   'plano_arquivo': plan.relative_to(ROOT).as_posix(),
                   'plano_sha256': c.montagem.sha(plan.read_bytes())})


if __name__ == '__main__':
    main()
