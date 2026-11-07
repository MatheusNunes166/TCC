"""Fechamento offline D-38 e preservacao D-37. Nenhum comando Codex/modelo."""
from datetime import datetime, timezone
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
import coletor_piloto as c


def main():
    plan_path = ROOT / 'captura/planejamento-piloto-2026-11-07-D38/plano.json'
    plan = c.conferir_plano(plan_path)
    previous_path = ROOT / 'captura/planejamento-piloto-2026-11-07/plano.json'
    previous = c.ler(previous_path)
    previous_source = (OUT / 'coletor-antes-D38.py').read_bytes()
    assert previous['coletor_sha256'] == c.montagem.sha(previous_source)
    assert previous_source == (ROOT / 'captura/controles-coletor-2026-11-07/fontes/coletor_piloto.py').read_bytes()
    assert [r['observacao_id'] for r in plan['observacoes']] == [r['observacao_id'] for r in previous['observacoes']]
    assert [r['payload_sha256'] for r in plan['observacoes']] == [r['payload_sha256'] for r in previous['observacoes']]
    for row in previous['observacoes']:
        assert c.montagem.sha((previous_path.parent / row['preparacao']).read_bytes()) == row['preparacao_sha256']
    old_attempts = list((ROOT / 'captura/controles-cli-2026-11-07').glob('PIL-*/T*/tentativa.json'))
    assert len(old_attempts) == 16
    for attempt in old_attempts:
        c.conferir_fechamento(attempt.parent)
    for manifest_path in (ROOT / 'avaliados/controles-cli-2026-11-07').rglob('manifesto.json'):
        for item in c.ler(manifest_path)['arquivos']:
            assert c.montagem.sha(c.relativo(manifest_path.parent, item['arquivo']).read_bytes()) == item['sha256']
    for name, expected in [('custom-zero', 0), ('custom-one', 0), ('custom-negative', 1),
                           ('custom-stream-negative', 1), ('custom-string', 1),
                           ('builtin-zero', 1), ('unknown-key', 1), ('ajustes-aplicados', 0)]:
        assert c.ler(OUT / ('config-' + name + '.json'))['retorno'] == expected
    assert 'reserved built-in provider IDs' in c.ler(OUT / 'config-builtin-zero.json')['stderr']
    context = c.ler(OUT / 'contexto-ajustes-aplicados.json')
    assert context['partes_developer'] == 4 and context['environment_context_presente']
    assert not context['sentinela_agents_presente']
    validation = c.ler(OUT / 'validacao-offline.json')
    for source in validation['fontes']:
        assert c.montagem.sha((ROOT / source['arquivo']).read_bytes()) == source['sha256']
    schemas = []
    for name in ('v2/ConfigReadParams.json', 'v2/ConfigReadResponse.json', 'InitializeParams.json'):
        source = ROOT / 'saidas-locais/schema-codex-D38-001' / name
        if source.is_file():
            raw = source.read_bytes()
            c.salvar(OUT / 'schema-instalado' / name, raw)
            schemas.append({'arquivo': name, 'sha256': c.montagem.sha(raw)})
    missing = []
    for target in re.findall(r'\]\(([^)]+)\)', (OUT / 'RELATORIO.md').read_text(encoding='utf-8')):
        if target.startswith(('https://', 'http://')):
            continue
        if not (OUT / target.split('#')[0]).exists():
            missing.append(target)
    assert not missing, missing
    cp = subprocess.run(['git', 'diff', '--check'], cwd=ROOT, capture_output=True)
    c.salvar(OUT / 'diff-check-stdout.bin', cp.stdout)
    c.salvar(OUT / 'diff-check-stderr.bin', cp.stderr)
    assert cp.returncode == 0
    c.salvar_json(OUT / 'revisao-final.json', {
        'instante': datetime.now(timezone.utc).isoformat(), 'escopo': 'D38_OFFLINE_SEM_LLM',
        'testes_aprovados': 16, 'falhas': 0, 'erros': 0,
        'fonte_D37_preservada': True, 'capturas_D37_revalidadas': 16,
        'avaliacoes_D37_revalidadas': True, 'plano_D37_hashes_preservados': True,
        'ordem_e_payloads_preservados': True,
        'configuracoes_nativas_conferidas': True, 'schemas_nativos_preservados': schemas,
        'bloqueio_ferramentas_contexto': 'PENDENTE', 'bloqueio_retentativas_cli': 'PENDENTE',
        'trava_incondicional_preservada': True, 'exec_modelo_iniciado': False,
        'alternativa_API_implementada': False, 'diff_check_retorno': cp.returncode,
        'links_relatorio_validos': True,
    })
    print('Revisao D-38 concluida; ambos os bloqueios pendentes; evidencias D-37 preservadas.')


if __name__ == '__main__':
    main()
