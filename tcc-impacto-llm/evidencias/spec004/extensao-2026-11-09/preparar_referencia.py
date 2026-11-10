"""Receita documental D-41: escreve expectativas ANTES de executar a bancada.

Nao importa autorizacao, variantes ou avaliador. Deduz os tres casos novos dos
RFs e conserva literalmente as 60 expectativas anteriores em nova referencia.
Executar uma unica vez, a partir da raiz do projeto, com Python -B.
"""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent


def sha(blob):
    return hashlib.sha256(blob).hexdigest()


def save(path, value):
    with path.open('xb') as f:
        f.write((json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode())


def main():
    # Inventario inclui ignorados, materiais e todas as fontes/capturas antigas.
    inventory = {}
    for area in ('captura', 'avaliados', 'evidencias', 'materiais', 'variantes'):
        for path in sorted((ROOT / area).rglob('*')):
            if path.is_file() and not path.is_relative_to(OUT):
                inventory[path.relative_to(ROOT).as_posix()] = sha(path.read_bytes())
    sources = ('coletor_api.py', 'coletor_piloto.py', 'montagem_entradas.py',
               'avaliacao_ids.py', 'revisao_conformidade.py', 'fontes_autorizadas.py',
               'verificacao_variantes.py', 'autorizacao.py')
    for name in sources:
        data = (ROOT / name).read_bytes()
        inventory[name] = sha(data)
        folder = OUT / 'fontes-anteriores'
        folder.mkdir(exist_ok=True)
        with (folder / name).open('xb') as f:
            f.write(data)
    save(OUT / 'estado-inicial.json', {
        'data': '2026-11-09', 'python': sys.version,
        'head': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT).decode().strip(),
        'status_antes': subprocess.check_output(['git', 'status', '--short'], cwd=ROOT).decode(),
        'sha256_anteriores': inventory})
    oldpath = ROOT / 'materiais/modelos/referencia_candidata_NAO_ENVIAR_AO_LLM.json'
    ref = json.loads(oldpath.read_bytes())
    ref.update(versao='0.3', status='CANDIDATO_NAO_REVISADO', revisor=None,
               data_revisao=None, catalogo_versao='0.3',
               observacao='D-41, 09/11/2026. Expectativas deduzidas dos contratos antes da execucao local; '
               'T01-T12 preservados. Referencia para revisao do pesquisador; sem aprovacao externa.',
               historico_anterior=oldpath.name,
               origem_sha256=sha(oldpath.read_bytes()),
               quantidades={'testes_baseline': 15, 'pares_teste_mudanca': 60,
                            'expectativas_com_baseline': 75})
    def result(decision, reason):
        return {'decisao': decision, 'motivo': reason}
    direct = result('permitir', 'permissao_direta')
    conflict = result('negar', 'conflito')
    state = result('negar', 'estado')
    absent = result('negar', 'sem_permissao')
    ref['catalogo'] += [
        dict(id='T13', estado='ativa', papeis=['Consulta', 'Supervisão'],
             operacao='visualizar', esperado=direct),
        dict(id='T14', estado='ativa', papeis=['Consulta', 'Auditoria', 'Supervisão'],
             operacao='exportar', esperado=conflict),
        dict(id='T15', estado='em_revisao', papeis=['Consulta', 'Auditoria', 'Supervisão'],
             operacao='exportar', esperado=state)]
    # RF-02 direta prevalece sobre RF-03; RF-01 > RF-04 > concessao.
    expectations = {
        'MC-01': [direct, conflict, state],
        'MC-02': [direct, direct, state],
        'MC-03': [absent, conflict, state],
        'MC-04-v2': [direct, conflict, state]}
    selections = {
        'MC-01': ([], ['T14', 'T15']),
        'MC-02': (['T14'], ['T15']),
        'MC-03': (['T13'], []),
        'MC-04-v2': ([], ['T13', 'T14', 'T15'])}
    reasons = {
        'MC-01': {'T13': 'Excluir: visualizar, nao exportar.',
                  'T14': 'Preservacao: exportar/Auditoria efetivo; conflito precede permissao removida.',
                  'T15': 'Preservacao: exportar/Auditoria efetivo; estado mascara conflito e concessao.'},
        'MC-02': {'T13': 'Excluir: falta Auditoria no par efetivo.',
                  'T14': 'Mudanca: retirado conflito, Auditoria concede exportar diretamente.',
                  'T15': 'Preservacao: par efetivo presente; estado prevalece mesmo sem conflito.'},
        'MC-03': {'T13': 'Mudanca: visualizar/Consulta efetivo; perde concessoes direta e herdada.',
                  'T14': 'Excluir: exportar, nao visualizar; conflito intacto.',
                  'T15': 'Excluir: exportar, nao visualizar; estado prevalece.'},
        'MC-04-v2': {'T13': 'Preservacao: Supervisao atribuida; Consulta direto conserva visualizar.',
                     'T14': 'Preservacao: Supervisao atribuida; Consulta direto conserva conflito com Auditoria.',
                     'T15': 'Preservacao: Supervisao atribuida; estado mascara conflito e concessao.'}}
    for change in ref['mudancas']:
        name = change['id']
        change['expected'].update(dict(zip(('T13', 'T14', 'T15'), expectations[name])))
        changed, preserved = selections[name]
        change['changed'] += changed
        change['preserved'] += preserved
        change['tests'] = sorted(change['tests'] + changed + preserved)
        change['justificativas_adicionais'] = reasons[name]
    dest = ROOT / 'materiais/modelos/referencia_candidata_0.3_NAO_ENVIAR_AO_LLM.json'
    save(dest, ref)
    save(ROOT / 'materiais/modelos/catalogo_baseline_0.3.json', {
        'versao': '0.3', 'referencia_versao': '0.3',
        'referencia_sha256': sha(dest.read_bytes()), 'catalogo': ref['catalogo']})
    # Catálogo publico: somente entrada e expectativa da BASELINE.
    lines = ['| ID | Estado | Papéis | Operação | Decisão esperada | Motivo esperado |\n',
             '| --- | --- | --- | --- | --- | --- |\n']
    for c in ref['catalogo']:
        lines.append('| ' + ' | '.join([c['id'], c['estado'], ' + '.join(c['papeis']),
                     c['operacao'], c['esperado']['decisao'], c['esperado']['motivo']]) + ' |\n')
    with (ROOT / 'materiais/modelos/catalogo_baseline_0.3.md').open('xb') as f:
        f.write(''.join(lines).encode())
    save(OUT / 'expectativas-antes-execucao.json', {
        'derivacao': 'contratos RF-01 a RF-04; precedencia de documentacao/requisitos.md; politica conservadora 0.2',
        'referencia': dest.relative_to(ROOT).as_posix(), 'sha256': sha(dest.read_bytes()),
        'codigo_bancada_executado_nesta_receita': False,
        'matriz': {m['id']: m['expected'] for m in ref['mudancas']},
        'baseline': {c['id']: c['esperado'] for c in ref['catalogo']}})


if __name__ == '__main__':
    main()
