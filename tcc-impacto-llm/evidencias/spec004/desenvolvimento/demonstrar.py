"""Execucao local pela CLI; preserva cada entrada, resposta e resultado original."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[3]
FIX=ROOT/'tests/fixtures/spec004'
OUT=ROOT/'evidencias/spec004/demonstracao-001'

def sha(data):return hashlib.sha256(data).hexdigest()
def dump(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('x',encoding='utf-8',newline='\n') as f:json.dump(value,f,indent=2,ensure_ascii=True);f.write('\n')

def run(label,args,expected):
    record=OUT/'comandos'/label;record.mkdir(parents=True,exist_ok=False)
    cmd=[sys.executable,'-B',*map(str,args)]
    p=subprocess.run(cmd,cwd=ROOT,capture_output=True)
    (record/'stdout.txt').write_bytes(p.stdout);(record/'stderr.txt').write_bytes(p.stderr)
    dump(record/'comando.json',{'comando':cmd,'cwd':str(ROOT),'retorno':p.returncode,'esperado':expected,'origem':'sintetica'})
    if p.returncode!=expected:raise RuntimeError(f'{label}: {p.returncode} != {expected}')

if __name__=='__main__':
    OUT.mkdir(exist_ok=False)
    preparations=[]
    for cond in ['D0','D1','E0','E1']:
        output=OUT/'preparacoes'/cond
        run('montagem-'+cond,['montagem_entradas.py','--pacote',FIX/'pacotes'/cond,
          '--manifesto',FIX/'pacotes'/cond/'manifesto.json','--saida',output],0)
        preparations.append(json.loads((output/'preparacao.json').read_bytes()))
    # Independent confrontation of hashes in saved artifacts (not a fabricated response).
    common=['sistema.txt','definicoes-comuns.md','requisitos-baseline.md','catalogo-baseline.md','mudanca.md','schema_saida.json']
    maps=[{d['arquivo']:d['sha256'] for d in p['documentos']} for p in preparations]
    assert all(len({m[n] for m in maps})==1 for n in common)
    assert maps[1]['notas.md']==maps[3]['notas.md']
    dump(OUT/'controles-condicoes.json',{'comuns_identicos':True,'notas_D1_E1_identicas':True,
      'notas_D0_E0_ausentes':all('notas.md' not in maps[i] for i in [0,2]),'origem':'sintetica'})
    prepfile=OUT/'preparacoes/D0/preparacao.json';prep=json.loads(prepfile.read_bytes())
    cases=json.loads((FIX/'esperados.json').read_bytes())['casos']
    results=[];inputs=[]
    def attempt(label,repeat,content,technical=False,previous=None,oid=None):
        folder=OUT/'entradas-avaliacao'/label;folder.mkdir(parents=True,exist_ok=False)
        if content is not None:(folder/'resposta.bin').write_bytes(content)
        t={'observacao_id':oid or 'obs-'+label,'tentativa_id':'tent-'+label,'tentativa_anterior':previous,
          'configuracao_id':'controle-local-v1','mudanca':'MC-01','condicao':'D0','repeticao_sintetica':repeat,
          'origem':'sintetica','modelo_reportado':None,'preparacao_id':prep['preparacao_id'],
          'preparacao_sha256':sha(prepfile.read_bytes()),'payload_sha256':prep['payload_sha256'],
          'estado_tecnico':'falha_tecnica' if technical else 'concluida','causa':'falha artificial de transporte' if technical else None,
          'fragmento':technical and content is not None,'resposta_arquivo':'resposta.bin' if content is not None else None,
          'resposta_sha256':sha(content) if content is not None else None,'resposta_tamanho':len(content) if content is not None else None}
        dump(folder/'tentativa.json',t)
        output=OUT/'avaliacoes'/label
        code=1 if technical or label=='invalida' else 0
        run('avaliacao-'+label,['avaliacao_ids.py','avaliar','--preparacao',prepfile,'--tentativa',folder/'tentativa.json',
          '--referencia',FIX/'referencia-sintetica.json','--saida',output],code)
        result=json.loads((output/'avaliacao.json').read_bytes())
        results.append((output/'avaliacao.json',result));inputs.append(t)
        return t,result,output/'avaliacao.json'
    for i,case in enumerate(cases,1):
        _,r,_=attempt(case['familia'],i,(json.dumps(case['resposta'])+'\n').encode())
        for dim,k in [('requisitos','rf'),('testes','t')]:
            assert [r[dim][n] for n in ('TP','FP','FN')]==case[k]
    inv=attempt('invalida',10,b'```json\n{}\n```\r\n')
    tech=attempt('tecnica',11,None,True)
    fragment=attempt('fragmento',12,b'{"requisitos":',True)
    first=attempt('ret-1',100,None,True,oid='obs-retentativa')
    second=attempt('ret-2',100,(json.dumps(cases[0]['resposta'])+'\n').encode(),previous=first[0]['tentativa_id'],oid='obs-retentativa')
    def summary(label,selected,plans,impute=False,expected=0):
        folder=OUT/'listas'/label;folder.mkdir(parents=True,exist_ok=False)
        # Explicit paths relative to the list; imports stay within the demonstration root.
        entries=[]
        for i,(file,result) in enumerate(selected):
            data=file.read_bytes();copyfile=folder/f'avaliacao-{i}.json';copyfile.write_bytes(data)
            entries.append({'arquivo':copyfile.name,'sha256':sha(data)})
        dump(folder/'avaliacoes.json',entries)
        keys=['observacao_id','configuracao_id','mudanca','condicao','repeticao_sintetica','payload_sha256']
        dump(folder/'planejadas.json',[{k:t[k] for k in keys} for t in plans])
        args=['avaliacao_ids.py','resumir','--avaliacoes',folder/'avaliacoes.json','--observacoes',folder/'planejadas.json','--saida',OUT/'resumos'/label]
        if impute:args.append('--imputar-invalidas')
        run('resumo-'+label,args,expected)
    exact=results[0]
    summary('A',[exact,(inv[2],inv[1]),(tech[2],tech[1])],[inputs[0],inv[0],tech[0]],True,1)
    summary('B',[(first[2],first[1]),(second[2],second[1])],[second[0]],False,0)
    summary('todas-validas',results[:len(cases)],inputs[:len(cases)],False,0)
    dump(OUT/'manifesto.json',{'origem':'sintetica','completo_no_escopo_offline':True,'isolamento_real_demonstrado':False,
      'modelos':None,'llm_chamadas':0,'piloto':False,'limite':'Nao e fechamento integral; T014/T015 e dependentes pendentes.'})
    print('Demonstracao offline concluida, originais e comandos preservados; isolamento nao demonstrado.')
