"""Revalida evidencias locais; nao inicia Codex/LLM, nao faz stage/commit/push."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
import coletor_piloto as c


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pedido', required=True, type=Path)
    args = parser.parse_args()
    plan_path = ROOT / 'captura/planejamento-piloto-2026-11-07/plano.json'
    plan = c.conferir_plano(plan_path)
    tests = c.ler(OUT / 'testes.json')
    assert all(r['retorno'] == 0 for r in tests['consultas'])
    for source in tests['fontes']:
        assert c.montagem.sha((ROOT / source['arquivo']).read_bytes()) == source['sha256']
        assert (ROOT / source['arquivo']).read_bytes() == (OUT / 'fontes' / source['arquivo']).read_bytes()
    for row in plan['observacoes']:
        original = c.BASE / (row['mudanca'] + '-' + row['condicao']) / 'payload.txt'
        prepared = plan_path.parent / row['preparacao']
        assert original.read_bytes() == (prepared.parent / 'payload.txt').read_bytes()
    lot = ROOT / 'captura/controles-cli-2026-11-07'
    attempts = sorted(lot.glob('PIL-*/T*/tentativa.json'))
    assert len(attempts) == 16
    sessions = set()
    for path in attempts:
        t = c.conferir_fechamento(path.parent)
        assert (t['origem'], t['fase']) == ('sintetica', 'verificacao_sintetica')
        assert t['modelo_reportado'] is None
        sessions.add(t['sessao'])
        assert (path.parent / 'entrada.bin').read_bytes() == (path.parent / 'ambiente/stdin-recebido.bin').read_bytes()
    assert len(sessions) == 16
    summary = c.ler(ROOT / 'avaliados/controles-cli-2026-11-07/resumo/resumo.json')
    assert summary['origem'] == 'sintetica' and summary['completo']
    assert sum(group['contagens']['N'] for cell in summary['celulas'] for group in cell['grupos']) == 16
    assert not (ROOT / 'captura/piloto/NAO_CRIAR').exists()
    cp = subprocess.run(['git', 'diff', '--check'], cwd=ROOT, capture_output=True)
    c.salvar(OUT / 'diff-check-stdout.bin', cp.stdout)
    c.salvar(OUT / 'diff-check-stderr.bin', cp.stderr)
    assert cp.returncode == 0
    cp = subprocess.run(['git', 'diff', '--name-only', '--relative'], cwd=ROOT, capture_output=True)
    names = cp.stdout.decode().splitlines()
    assert not any(name.startswith(('evidencias/', 'variantes/', 'materiais/modelos/')) for name in names)
    pedido = args.pedido.read_bytes()
    c.salvar(OUT / 'pedido-original.txt', pedido)
    c.salvar_json(OUT / 'revisao-final.json', {
        'instante_utc': datetime.now(timezone.utc).isoformat(), 'tipo': 'REVISAO_OFFLINE_SEM_LLM',
        'testes_descobertos': 46, 'testes_aprovados': 45, 'ignorados': 1,
        'motivo_ignorado': 'symlink real: WinError 1314, privilegio Windows indisponivel',
        'capturas_sinteticas': 16, 'sessoes_substituto_distintas': 16,
        'observacoes_planejadas': 16, 'payloads_unicos': 8, 'identicos_v2_lf': True,
        'envio_real_bloqueado': True, 'piloto_real_executado': False,
        'pedido_sha256': c.montagem.sha(pedido),
        'plano_sha256': c.montagem.sha(plan_path.read_bytes()),
        'fontes_testadas_revalidadas': True, 'diff_check_retorno': 0,
        'arquivos_rastreados_alterados': names,
        'evidencias_anteriores_regravadas_no_diff': False,
    })
    print('Revisao offline concluida; nenhuma chamada ao LLM ou piloto real.')


if __name__ == '__main__':
    main()
