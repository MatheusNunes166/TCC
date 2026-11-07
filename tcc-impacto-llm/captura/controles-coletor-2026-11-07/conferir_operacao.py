"""Smoke offline da CLI do coletor; nenhum comando Codex/LLM e executado."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
PLAN = 'captura/planejamento-piloto-2026-11-07/plano.json'
LOT = 'captura/controles-cli-2026-11-07'
EVAL = 'avaliados/controles-cli-2026-11-07'


def main():
    checks = [
        ('ajuda', ['--help'], 0),
        ('simulacao', ['simular', '--plano', PLAN], 0),
        ('envio-sem-flag', ['iniciar', '--plano', PLAN, '--lote', 'captura/piloto/NAO_CRIAR'], 2),
        ('envio-com-flag', ['iniciar', '--plano', PLAN, '--lote', 'captura/piloto/NAO_CRIAR', '--enviar-real'], 2),
        ('controle-parcial', ['controle', '--plano', PLAN, '--lote', LOT, '--limite', '3'], 0),
        ('controle-continuacao', ['controle', '--plano', PLAN, '--lote', LOT, '--continuar'], 0),
        ('avaliacao-sintetica', ['avaliar', '--lote', LOT, '--referencia',
         'materiais/modelos/referencia_candidata_NAO_ENVIAR_AO_LLM.json', '--saida', EVAL], 0),
    ]
    records = []
    for name, args, expected in checks:
        argv = [sys.executable, '-B', 'coletor_piloto.py', *args]
        result = subprocess.run(argv, cwd=ROOT, capture_output=True)
        for suffix, data in [('stdout.bin', result.stdout), ('stderr.bin', result.stderr)]:
            with (OUT / (name + '-' + suffix)).open('xb') as stream:
                stream.write(data)
        records.append({'argv': argv, 'retorno': result.returncode, 'esperado': expected})
        print(name, result.returncode, flush=True)
        if result.returncode != expected:
            raise RuntimeError(name + ': retorno inesperado; consultar logs')
    attempts = list((ROOT / LOT).glob('PIL-*/T*/tentativa.json'))
    rows = [json.loads(p.read_bytes()) for p in attempts]
    assert len(rows) == 16
    assert all(r['origem'] == 'sintetica' and r['fase'] == 'verificacao_sintetica' for r in rows)
    assert len({r['sessao'] for r in rows}) == 16
    assert not (ROOT / 'captura/piloto/NAO_CRIAR').exists()
    summary = json.loads((ROOT / EVAL / 'resumo/resumo.json').read_bytes())
    assert summary['origem'] == 'sintetica'
    with (OUT / 'operacao.json').open('x', encoding='utf-8', newline='\n') as stream:
        json.dump({'tipo': 'CONTROLE_ARTIFICIAL_SEM_LLM', 'consultas': records,
                   'capturas_sinteticas': len(rows), 'sessoes_substituto_distintas': 16,
                   'plano_sha256': hashlib.sha256((ROOT / PLAN).read_bytes()).hexdigest()}, stream, indent=2)
        stream.write('\n')


if __name__ == '__main__':
    main()
