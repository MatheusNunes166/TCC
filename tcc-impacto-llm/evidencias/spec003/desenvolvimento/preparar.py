"""Operação única T011–T015; quatro extrações independentes, nunca em execução da matriz."""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))  # Só ferramenta de preparação, não loader da bancada.
import verificacao_variantes as v

output = v.create_output(ROOT, ROOT / 'evidencias/spec003/procedencia')
git = v.GitSource(ROOT)
rules = {
    'MC-01': ("(('Consulta', 'visualizar'), ('Auditoria', 'exportar'))", "(('Consulta', 'visualizar'),)"),
    'MC-02': ("return {'Consulta', 'Auditoria'} <= papeis_efetivos", 'return False'),
    'MC-03': ("(('Consulta', 'visualizar'), ('Auditoria', 'exportar'))", "(('Auditoria', 'exportar'),)"),
    'MC-04-v2': ("return papeis | frozenset({'Consulta'} if 'Supervisão' in papeis else ())", 'return papeis')}
records = {}
for change, (old, new) in rules.items():
    base, blob = git.read('autorizacao.py')  # Extração nova de B para CADA variante.
    path = ROOT / v.VARIANTS[change]
    path.parent.mkdir(exist_ok=True)
    with path.open('xb') as stream:
        stream.write(base.replace(old.encode(), new.encode(), 1))
    record = v.audit_source(base, path.read_bytes(), change, v.BASELINE)
    diff = record.pop('diff')
    target = output / 'diffs' / f'{change}.diff'
    target.parent.mkdir(exist_ok=True)
    target.write_bytes(diff.encode('utf-8'))
    record.update(objeto_origem=blob, caminho=v.VARIANTS[change], diff=str(target), revisao=None)
    records[change] = record
v.save_json(output / 'manifesto.json', records)
v.save_json(ROOT / 'variantes/procedencia.json', records)
print(json.dumps(records, indent=2, ensure_ascii=False))
