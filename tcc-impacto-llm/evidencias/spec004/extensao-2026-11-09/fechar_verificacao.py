"""Confere conservacao integral anterior, plano atual e bytes que Git preservara.

Sem stage/commit/transporte remoto. Nao regrava manifestos antigos.
"""
import argparse
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
import avaliacao_ids as a
import extensao_exploratoria as e


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--saida', type=Path, default=OUT / 'preservacao-final-002.json')
    args = p.parse_args()
    old = a.json_estrito((OUT / 'estado-inicial.json').read_bytes())['sha256_anteriores']
    functional = {'coletor_api.py', 'avaliacao_ids.py'}
    mismatches = []
    preserved = 0
    for name, h in old.items():
        path = ROOT / name
        if name in functional:
            path = OUT / 'fontes-anteriores' / name
        if not path.is_file() or a.sha(path.read_bytes()) != h:
            mismatches.append(name)
        else:
            preserved += 1
    plan = ROOT / 'captura/extensao-20261109-002/plano.json'
    checked = e.conferir(plan)
    preps = {r['preparacao']: r for r in checked['observacoes']}
    links = 0
    for name in preps:
        prep = e.api.base.conferir_preparacao(plan.parent / name)
        links += len(prep['arquivos']) + len(prep['documentos']) + 3
    # Verifica todos os novos arquivos com bytes vinculados: Git filtrado deve
    # produzir o mesmo objeto que bytes literais, sem escrever objetos ou index.
    bound = [ROOT / name for name in ('coletor_api.py', 'avaliacao_ids.py', 'extensao_exploratoria.py',
             'tests/test_extensao_exploratoria.py', 'materiais/modelos/catalogo_baseline_0.3.json',
             'materiais/modelos/catalogo_baseline_0.3.md', 'materiais/modelos/referencia_candidata_0.3_NAO_ENVIAR_AO_LLM.json')]
    bound += [f for folder in (plan.parent, OUT) for f in folder.rglob('*') if f.is_file() and f != args.saida]
    names = [f.relative_to(ROOT).as_posix() for f in bound]
    gitroot = Path(subprocess.check_output(['git', 'rev-parse', '--show-toplevel'], cwd=ROOT).decode().strip())
    filenames = ('\n'.join(f.relative_to(gitroot).as_posix() for f in bound) + '\n').encode()
    literal = subprocess.check_output(['git', 'hash-object', '--stdin-paths', '--no-filters'], input=filenames, cwd=gitroot).splitlines()
    filtered = subprocess.check_output(['git', 'hash-object', '--stdin-paths'], input=filenames, cwd=gitroot).splitlines()
    if len(literal) != len(filtered) or len(literal) != len(names):
        raise ValueError('inventario Git incompleto')
    byte_errors = [name for name, before, after in zip(names, literal, filtered) if before != after]
    docs = ['README.md', 'ESTADO_ATUAL.md', 'documentacao/contexto-e-escopo.md',
            'documentacao/arquitetura.md', 'documentacao/roadmap.md', 'documentacao/decisoes.md',
            'documentacao/operacao-api.md', 'documentacao/referencia-candidata-0.3.md',
            'evidencias/spec004/extensao-2026-11-09/RELATORIO.md']
    missing, inherited = [], []
    link_count = 0
    for name in docs:
        file = ROOT / name
        original = subprocess.run(['git', 'show', 'HEAD:' + file.relative_to(gitroot).as_posix()],
                                  cwd=gitroot, capture_output=True)
        previous = original.stdout.decode('utf-8-sig') if original.returncode == 0 else ''
        for href in re.findall(r'\]\(([^)]+)\)', file.read_text(encoding='utf-8-sig')):
            href = href.split('#')[0]
            if not href or '://' in href:
                continue
            link_count += 1
            target = (file.parent / href).resolve()
            if target == args.saida.resolve():
                continue  # O proprio fechamento sera gravado apos a conferencia.
            if not target.exists():
                (inherited if '](' + href + ')' in previous else missing).append([name, href])
    pilot = [a.json_estrito(p.read_bytes()) for p in (ROOT / 'avaliados/piloto-api-001').glob('PIL-*/T01/avaliacao.json')]
    exact = sum(all(r[d]['metricas_propostas']['correspondencia_exata'] == 1 for d in ('requisitos', 'testes')) for r in pilot)
    result = {'arquivos_anteriores_conferidos': len(old), 'preservados': preserved,
        'divergencias_anteriores': mismatches, 'fontes_funcionais_atuais_alteradas_com_originais_preservados': sorted(functional),
        'preparacoes_atuais': len(preps), 'vinculos_preparacoes_conferidos': links,
        'textos_unicos': len({r['payload_sha256'] for r in checked['observacoes']}),
        'posicoes_planejadas_nao_executadas': len(checked['observacoes']),
        'arquivos_com_bytes_git_conferidos': len(bound), 'divergencias_bytes_git': byte_errors,
        'links_locais_conferidos': link_count, 'links_ausentes_novos': missing,
        'links_ausentes_preexistentes_no_HEAD_preservados': inherited,
        'piloto_avaliacoes': len(pilot), 'piloto_correspondencia_integral': exact,
        'manifesto_novos_sha256': {f.relative_to(ROOT).as_posix(): a.sha(f.read_bytes()) for f in bound},
        'sem_commit_stage_ou_push': True, 'hash_object_sem_escrita_de_objetos': True}
    result['conforme'] = not (mismatches or byte_errors or missing) and exact == len(pilot) == 16
    with args.saida.open('xb') as f:
        f.write(a.serial(result))
    print(json.dumps({k: v for k, v in result.items() if k != 'manifesto_novos_sha256'}, indent=2))
    return 0 if result['conforme'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
