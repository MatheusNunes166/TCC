"""Inspeção de fechamento, sem executar novamente a bancada."""
import hashlib
import json
import pathlib
import re
import subprocess

ROOT = pathlib.Path(__file__).resolve().parents[3]
FINAL = ROOT / 'evidencias/spec003/rodada-final'
output = ROOT / 'evidencias/spec003/revisao-final'
output.mkdir(exist_ok=False)
m = json.loads((FINAL / 'manifesto.json').read_text(encoding='utf-8'))
r = json.loads((FINAL / 'resultados.json').read_text(encoding='utf-8'))
original = json.loads((FINAL / 'resultados-originais.json').read_text(encoding='utf-8'))
ref = json.loads((ROOT / 'materiais/modelos/referencia_candidata_NAO_ENVIAR_AO_LLM.json').read_text(encoding='utf-8'))
assert len({(x['mudanca'], x['teste']) for x in r['variantes']}) == 48
assert len(r['baseline']) == 12 and all(x['estado'] == 'conforme' for x in r['baseline'] + r['variantes'])
assert all(x['esperado'] == x['observado'] for x in r['baseline'] + r['variantes'])
assert all(x['versao_executada']['executada'] for x in r['baseline'] + r['variantes'])
assert r == original  # Nenhuma ocorrência exigiu acrescentar diagnóstico aos pares reais.
assert ref['versao'] == '0.2' and ref['status'] == 'CANDIDATO_NAO_REVISADO'
assert ref['revisor'] is None and ref['data_revisao'] is None
assert [len(x['tests']) for x in ref['mudancas']] == [2, 4, 8, 5]
assert m['codigo_saida'] == 0 and m['integridade'] and m['diagnostico']['total'] == 0
hashes = {}
for name, expected in m['hashes_fechamento'].items():
    actual = hashlib.sha256(pathlib.Path(name).read_bytes()).hexdigest()
    assert expected == actual, name
    hashes[name] = actual
for name, expected in m['logs'].items():
    assert hashlib.sha256((FINAL / name).read_bytes()).hexdigest() == expected, name
tasks = (ROOT / 'specs/003-mudancas-controladas/tasks.md').read_text(encoding='utf-8')
assert len(re.findall(r'^- \[x\] T\d{3}\b', tasks, re.M)) == 35
assert not re.findall(r'^- \[ \] T\d{3}\b', tasks, re.M)
checklist = (ROOT / 'specs/003-mudancas-controladas/checklists/requirements.md').read_text(encoding='utf-8')
assert len(re.findall(r'^- \[x\]', checklist, re.M)) == 23
report = ROOT / 'specs/003-mudancas-controladas/evidencias.md'
links = re.findall(r'\[[^\]]+\]\(([^)]+)\)', report.read_text(encoding='utf-8'))
for link in links:
    assert (report.parent / link).resolve().exists(), link
commands = []
for args in (['git', 'diff', '--exit-code', m['baseline_commit'], '--', 'autorizacao.py',
              'tests/test_autorizacao.py', 'materiais/'],
             ['git', '-c', 'core.safecrlf=false', 'diff', '--check'],
             ['git', 'status', '--short'], ['git', 'diff', '--stat']):
    result = subprocess.run(args, cwd=ROOT, capture_output=True)
    commands.append(dict(comando=args, retorno=result.returncode,
                         stdout=result.stdout.decode('utf-8', errors='replace'),
                         stderr=result.stderr.decode('utf-8', errors='replace')))
    assert result.returncode == 0, commands[-1]
audit = dict(tipo='inspecao_sem_nova_execucao_da_bancada', tarefas_concluidas=35,
             checklist_qualidade_preservada=23, pares_baseline=12, pares_variantes=48,
             referencia='0.2 candidata, sem revisor/data', links_validos=len(links),
             hashes_conferidos=hashes, comandos=commands, revisao_cientifica='pendente')
(output / 'auditoria.json').write_text(json.dumps(audit, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({k: v for k, v in audit.items() if k not in ('hashes_conferidos', 'comandos')}, ensure_ascii=False, indent=2))
