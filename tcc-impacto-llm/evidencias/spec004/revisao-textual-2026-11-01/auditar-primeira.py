"""Consolida evidencias locais D-29; nao executa testes, LLM ou piloto."""
import ast
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
STAGE=Path(__file__).resolve().parent

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_bytes())
def save(p,value):
    with p.open('x',encoding='utf-8',newline='\n') as out:
        json.dump(value,out,ensure_ascii=True,indent=2);out.write('\n')
def functions(path):
    return {n.name:ast.dump(n,include_attributes=False) for n in ast.parse(path.read_bytes()).body if isinstance(n,ast.FunctionDef)}

if __name__=='__main__':
    inv=load(STAGE/'inventario-inicial.json')
    protected=inv['protegidos_sha256']
    controls=load(STAGE/'controles-originais.json')
    checked={p:{'anterior':digest,'atual':sha(ROOT/p)} for p,digest in (protected|controls).items()}
    changed=[p for p,r in checked.items() if r['anterior']!=r['atual']]
    assert not changed,changed
    checklist='specs/004-preparacao-avaliacao-ids/checklists/requirements.md'
    # Originais are stored with their original relative paths.
    assert sha(ROOT/checklist)==sha(STAGE/'originais'/checklist)
    before=functions(STAGE/'originais/avaliacao_ids.py');after=functions(ROOT/'avaliacao_ids.py')
    differences=[name for name in before if before[name]!=after.get(name)]
    assert set(differences)=={'caminho_seguro','relativo','ler'},differences
    old_test=ast.parse((STAGE/'originais/tests/test_avaliacao_ids.py').read_bytes())
    new_test=ast.parse((ROOT/'tests/test_avaliacao_ids.py').read_bytes())
    methods=lambda tree:{n.name:ast.dump(n,include_attributes=False) for n in ast.walk(tree) if isinstance(n,ast.FunctionDef) and n.name.startswith('test_')}
    old_methods=methods(old_test);new_methods=methods(new_test)
    assert all(new_methods.get(k)==v for k,v in old_methods.items())
    runs={}
    snapshots=['montagem_entradas.py','avaliacao_ids.py','fontes_autorizadas.py',
               'tests/test_montagem_entradas.py','tests/test_avaliacao_ids.py','tests/test_fontes_autorizadas.py']
    for run in ('recortes-primeira','montagem-revisada','entrada-avaliador','prova-comando'):
        record=load(STAGE/run/'comando.json');assert record['retorno']==0
        for path in snapshots:assert record['fontes_sha256'][path]==sha(ROOT/path),(run,path)
        runs[run]={'retorno':record['retorno'],'comando':record['comando'],
                   'comando_sha256':sha(STAGE/run/'comando.json')}
    proof=load(STAGE/'demonstracao-textual-001/confrontos.json')
    assert len(proof['pacotes'])==16 and proof['comuns_equivalentes'] and proof['referencia_apenas_avaliador']
    assert all(x['conteudo_exato_confrontado'] and x['sentinelas_proibidas_ausentes'] for x in proof['pacotes'])
    assert proof['mesmas_notas_oito_condicoes_com_notas'] and not proof['envio_realizado']
    old_matrix=ROOT/'evidencias/spec004/revisao-parcial/matriz.json'
    previous=load(old_matrix)
    fresh=[]
    for run in ('recortes-primeira','montagem-revisada','entrada-avaliador'):
        rows=[json.loads(line) for line in (STAGE/run/'controles.jsonl').read_text(encoding='utf-8').splitlines() if line]
        assert rows and all(x['conforme'] and x['esperado']==x['observado'] for x in rows),run
        fresh.extend({'execucao':run,**x} for x in rows)
    matrix=[]
    for family in previous['familias']:
        ident=family['familia']
        if ident!='S-14':
            assert all(r['conforme'] and r['esperado']==r['observado'] for r in family['registros_de_confronto'])
        current=[r for r in fresh if r['familia']==ident]
        matrix.append({'familia':ident,'estado':'conforme_no_escopo_offline_D29',
          'evidencia_anterior':{'arquivo':'../revisao-parcial/matriz.json','sha256':sha(old_matrix),
             'estado_na_epoca':family['estado'],'nao_reexecutada':True},
          'registros_atuais':current,
          'fundamento':'Recortes/fontes, autorizacao, caminhos, byte a byte e demonstracao persistente' if ident=='S-14'
             else 'Oraculos/controles anteriores preservados; AST de pontuacao inalterada; alteracoes de importacao/caminhos reconferidas',
          'limite':'Sem resultado de LLM. Identidade Windows/symlink privilegiado substituidos, nao aprovados.'})
    save(STAGE/'preservacao.json',{'data_local':'2026-11-01','arquivos':checked,'divergencias':changed,
         'checklist_byte_identica':True,'funcoes_avaliador_alteradas':differences,
         'demais_funcoes_avaliador_AST_identico':True,'metodos_anteriores_avaliador_AST_identico':True,
         'limite':'Hashes/AST provam preservacao delimitada, nao aprovacao cientifica nem garantia universal.'})
    save(STAGE/'matriz.json',{'origem':'sintetica','contrato_montagem':'spec004-v3',
         'politica':'ids-proposta-004-v2','familias':matrix,'execucoes_atuais':runs,
         'prova_textual':'demonstracao-textual-001/confrontos.json',
         'fechamento':'engenharia_offline_D29','envio_realizado':False,'isolamento_SO':False,
         'provas_substituidas_nao_aprovadas':['T014','T015','criacao_privilegiada_symlink']})
    print(json.dumps({'protegidos_preservados':len(checked),'funcoes_avaliador_alteradas':differences,
         'familias_consolidadas':len(matrix),'confrontos_atuais':len(fresh),
         'limite':'Verificacao local delimitada; sem envio/LLM/piloto/aprovacao cientifica.'}))
