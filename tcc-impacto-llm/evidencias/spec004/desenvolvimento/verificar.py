"""Auditoria documental/integridade posterior aos controles; nao substitui testes."""
from pathlib import Path
import hashlib
import json
import re
import subprocess

ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/'evidencias/spec004/revisao-parcial'

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

if __name__=='__main__':
    errors=[]
    inventory=json.loads((ROOT/'evidencias/spec004/preparacao/inventario.json').read_bytes())
    for name,digest in inventory['protegidos_sha256'].items():
        if sha(ROOT/name)!=digest:errors.append('protegido alterado: '+name)
    checks=ROOT/'specs/004-preparacao-avaliacao-ids/checklists/requirements.md'
    old=ROOT/'evidencias/spec004/preparacao/arquivos-iniciais/specs/004-preparacao-avaliacao-ids/checklists/requirements.md'
    if checks.read_bytes()!=old.read_bytes():errors.append('checklist foi alterada')
    tasks=(ROOT/'specs/004-preparacao-avaliacao-ids/tasks.md').read_text(encoding='utf-8')
    rows=re.findall(r'^- \[([ xX])\] (T\d{3})',tasks,re.M)
    completed=[t for flag,t in rows if flag.lower()=='x'];pending=[t for flag,t in rows if flag==' ']
    if len(completed)!=39 or pending!=['T014','T015']+[f'T{i:03}' for i in range(42,49)]:errors.append('estado das tarefas divergente')
    controls=[]
    for phase,source in [('montagem-final','montagem_entradas.py'),('avaliacao-importacao-final','avaliacao_ids.py')]:
        p=ROOT/'evidencias/spec004'/phase
        cmd=json.loads((p/'comando.json').read_bytes())
        if cmd['retorno']!=0 or cmd['fontes_sha256'][source]!=sha(ROOT/source):errors.append('checkpoint difere da fonte atual: '+source)
        controls += [json.loads(l) for l in (p/'controles.jsonl').read_text(encoding='utf-8').splitlines()]
    if any(r['conforme'] is not True for r in controls):errors.append('confronto divergente no checkpoint atual')
    matrix={'origem':'sintetica','politica':'ids-proposta-004-v2','fechamento_integral':False,'familias':[]}
    for i in range(1,17):
        fam=f'S-{i:02}';rs=[r for r in controls if r['familia']==fam]
        if not rs:errors.append('familia sem confronto: '+fam)
        matrix['familias'].append({'familia':fam,'estado':'parcial' if i==14 else 'conforme_no_escopo_offline','confrontos':rs})
    with (OUT/'matriz-atual.json').open('x',encoding='utf-8') as f:json.dump(matrix,f,indent=2,ensure_ascii=True)
    # Check original/snapshot hashes declared by evaluation manifests in the persistent demonstration.
    audited=0
    for manifest in (ROOT/'evidencias/spec004/demonstracao-001').rglob('manifesto.json'):
        m=json.loads(manifest.read_bytes())
        if 'arquivos' in m:
            for item in m['arquivos']:
                if sha(manifest.parent/item['arquivo'])!=item['sha256']:errors.append('snapshot alterado: '+str(manifest))
            audited+=1
    files=list((ROOT/'specs/004-preparacao-avaliacao-ids').rglob('*.md'))
    files += [ROOT/p for p in ['AGENTS.md','ESTADO_ATUAL.md','BLOQUEIOS.md','HANDOFF.md','documentacao/decisoes.md']]
    for p in files:
        text=p.read_text(encoding='utf-8-sig')
        for label,link in re.findall(r'\[([^\]]+)\]\(([^)]+)\)',text):
            if not link.startswith(('https:','http:','#')) and not (p.parent/link.split('#')[0]).exists():errors.append('link ausente: '+str(p)+': '+link)
    diff=subprocess.run(['git','diff','--check'],cwd=ROOT,capture_output=True)
    if diff.returncode:errors.append(diff.stdout.decode('utf-8','replace')+diff.stderr.decode('utf-8','replace'))
    record={'erros':errors,'tarefas_concluidas':completed,'tarefas_pendentes':pending,
      'originais_protegidos_preservados':not any('protegido' in e for e in errors),
      'checklist_preservada':checks.read_bytes()==old.read_bytes(),'snapshots_demonstracao_auditados':audited,
      'escopo':'Links/hashes conferem documentos e preservacao; correcao limitada aos confrontos funcionais nas evidencias sinteticas. Sem isolamento real ou fechamento integral.'}
    with (OUT/'verificacao-final.json').open('x',encoding='utf-8') as f:json.dump(record,f,indent=2,ensure_ascii=True)
    print(json.dumps({'erros':errors,'concluidas':len(completed),'pendentes':pending,'fechamento_integral':False}))
    raise SystemExit(bool(errors))
