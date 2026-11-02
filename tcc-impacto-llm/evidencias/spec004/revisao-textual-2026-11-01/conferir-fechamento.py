"""Conferencia final de preservacao/rastreabilidade, sem executar testes."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT=Path(__file__).resolve().parents[3]
STAGE=Path(__file__).resolve().parent
SPEC=ROOT/'specs/004-preparacao-avaliacao-ids'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(path,value):
    with path.open('x',encoding='utf-8',newline='\n') as out:
        json.dump(value,out,ensure_ascii=True,indent=2);out.write('\n')

if __name__=='__main__':
    initial=json.loads((STAGE/'inventario-inicial.json').read_bytes())
    controls=json.loads((STAGE/'controles-originais.json').read_bytes())
    expected=initial['protegidos_sha256']|controls
    errors=[p for p,h in expected.items() if not (ROOT/p).is_file() or sha(ROOT/p)!=h]
    assert not errors,errors
    text=(SPEC/'tasks.md').read_text(encoding='utf-8')
    tasks=re.findall(r'^- \[([xX ])\] (T\d{3}) (.+)$',text,re.M)
    assert len(tasks)==51 and {i for _,i,_ in tasks}=={f'T{i:03}' for i in range(1,52)}
    retired={i for mark,i,line in tasks if mark==' '}
    assert retired=={'T014','T015'}
    assert all('SUBSTITUÍDA D-29' in line for mark,i,line in tasks if i in retired)
    task_records=[]
    for mark,ident,line in tasks:
        proof=('contrato_antigo_substituido_D29_nao_executado' if ident in retired else
               'relatorio.md; matriz.json; preservacao.json' if int(ident[1:])>=42 else
               '../revisao-parcial/estado-tarefas.json; matriz.json')
        task_records.append({'id':ident,'estado':'substituida_nao_executada_nao_aprovada' if ident in retired else 'concluida_engenharia_offline',
                             'evidencia':proof,'texto_sha256':hashlib.sha256(line.encode()).hexdigest()})
    checklist=SPEC/'checklists/requirements.md'
    assert sha(checklist)==sha(STAGE/'originais'/checklist.relative_to(ROOT))
    assert len(re.findall(r'^- \[[xX]\]',checklist.read_text(encoding='utf-8'),re.M))==26
    assert not re.search(r'^- \[ \]',checklist.read_text(encoding='utf-8'),re.M)
    index=json.loads((STAGE/'demonstracao-textual-001/editorial/indice.json').read_bytes())
    # Freeze provenance against the current actual six source files, after all doc edits.
    for item in index['pacotes']:
        auth=json.loads((STAGE/'demonstracao-textual-001/editorial'/item['autorizacao']).read_bytes())
        for source in auth['fontes']:assert sha(ROOT/source['arquivo'])==source['sha256']
    docs=[SPEC/p for p in ('spec.md','plan.md','research.md','data-model.md','quickstart.md','tasks.md','contracts/preparacao-avaliacao.md')]
    docs += [ROOT/p for p in ('AGENTS.md','ESTADO_ATUAL.md','BLOQUEIOS.md','HANDOFF.md','documentacao/decisoes.md','documentacao/arquitetura.md')]
    docs += [STAGE/'relatorio.md',STAGE/'diagnostico.md']
    missing=[]
    for doc in docs:
        for target in re.findall(r'\]\(([^)]+)\)',doc.read_text(encoding='utf-8')):
            if '://' in target or target.startswith('#'):continue
            path=target.split('#')[0]
            if path and not (doc.parent/path).exists():missing.append({'documento':str(doc.relative_to(ROOT)),'destino':target})
    assert not missing,missing
    # No semantic proof is inferred from these link/count checks.
    diff=subprocess.run(['git','diff','--check'],cwd=ROOT,capture_output=True)
    assert diff.returncode==0,diff.stdout.decode(errors='replace')
    assert not (ROOT/'.specify/extensions.yml').exists()
    save(STAGE/'estado-tarefas.json',{'data':'2026-11-01','spec':'004-preparacao-avaliacao-ids',
        'vigentes_concluidas':49,'substituidas_nao_aprovadas':2,'tarefas':task_records,
        'limite':'Fechamento de engenharia offline D29; entrega real, revisao cientifica e piloto pendentes.'})
    save(STAGE/'conferencia-final.json',{'data':'2026-11-01','protegidos_preservados':len(expected),
        'divergencias':errors,'fontes_editoriais_iguais_as_preparadas':True,'checklist_preservada_26_marcas':True,
        'tarefas_vigentes_concluidas':49,'tarefas_substituidas_desmarcadas':sorted(retired),
        'documentos_sha256':{p.relative_to(ROOT).as_posix():sha(p) for p in docs},
        'links_inexistentes':missing,'links_nao_sao_prova_funcional':True,
        'git_diff_check':{'retorno':diff.returncode,'stdout':diff.stdout.decode(errors='replace'),
                          'stderr':diff.stderr.decode(errors='replace')},
        'hooks_ausentes':True,'LLM':False,'envio_realizado':False,'piloto':False,'isolamento_SO_alegado':False,
        'evidencia_funcional':'matriz.json; demonstracao-textual-001/confrontos.json; comandos e confrontos das execucoes vinculadas'})
    print('49 tarefas vigentes/2 substituidas; fontes protegidas/editoriais e checklist preservadas; documentos conferidos. Sem teste adicional/LLM/envio/piloto.')
