"""Fixtures sinteticas e oraculos editoriais; nao importa codigo de producao."""
from pathlib import Path
import hashlib
import json

ROOT=Path(__file__).resolve().parents[3]
FIX=ROOT/'tests/fixtures/spec004'

def dump(path,x):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('x',encoding='utf-8',newline='\n') as f:json.dump(x,f,indent=2,ensure_ascii=True);f.write('\n')

if __name__=='__main__':
    expected=json.loads((FIX/'esperados.json').read_bytes())
    dump(FIX/'referencia-sintetica.json',expected['referencia'])
    names=['sistema.txt','definicoes-comuns.md','requisitos-baseline.md','catalogo-baseline.md','mudanca.md','pedido.txt','schema_saida.json']
    for cond in ['D0','D1','E0','E1']:
        p=FIX/'pacotes'/cond;p.mkdir(parents=True,exist_ok=False)
        ns=names.copy()
        if cond in ('D1','E1'):ns.insert(5,'notas.md')
        entries=[]
        for name in ns:
            text={'sistema.txt':'Use somente este material ficticio. Retorne JSON de IDs.',
                  'definicoes-comuns.md':'Definicoes ficticias comuns; sem selecao resolvida.',
                  'requisitos-baseline.md':'RF-01 a RF-04 identificam regras ficticias.',
                  'catalogo-baseline.md':'T01 a T12 identificam casos ficticios; sem selecao apos mudanca.',
                  'mudanca.md':'Retirar uma concessao ficticia, isoladamente.',
                  'notas.md':'Observacoes ficticias para controle de composicao; rascunho.',
                  'pedido.txt':'Selecione IDs.' if cond[0]=='D' else 'Examine a mudanca e dependencias; selecione IDs.',
                  'schema_saida.json':'{"type":"object","required":["requisitos","testes"],"additionalProperties":false,"properties":{"requisitos":{"type":"array","items":{"type":"string"}},"testes":{"type":"array","items":{"type":"string"}}}}'}[name]
            data=(text+'\r\n').encode();(p/name).write_bytes(data)
            entries.append({'papel':name.split('.')[0],'arquivo':name,'versao':'sintetica-1',
              'sha256':hashlib.sha256(data).hexdigest(),'tamanho_bytes':len(data),
              'revisao_conteudo':{'estado':'conferido_tecnicamente','responsavel':'assistente; controle sintetico','data':'2026-10-27'}})
        dump(p/'manifesto.json',{'versao_contrato':'spec004-v2','pacote_id':'controle-'+cond,'versao_pacote':'sintetica-1',
          'configuracao_id':'controle-local-v1','mudanca':'MC-01','condicao':cond,
          'status':'RASCUNHO_PREPARACAO','liberado_para_pesquisa':False,'documentos':entries,
          'status_notas':'RASCUNHO_NAO_REVISADO' if cond in ('D1','E1') else 'ausentes',
          'origem_notas':'ficticia, nao sao as notas reais do pesquisador' if cond in ('D1','E1') else 'ausentes'})
    matrix=[]
    for i,title in enumerate(['exata','parcial','todos','vazias','duplicatas e ordem','desconhecidos','sem normalizacao',
         'dimensoes trocadas','JSON estrito','independencia','falhas tecnicas','referencia','integridade',
         'montagem e acesso','Jaccard','resumos e convencoes'],1):
        family=f'S-{i:02}'
        matrix.append({'familia':family,'objetivo':title,'origem':'sintetica',
          'oraculo':'esperados.json e literais nos testes, definidos antes da implementacao',
          'fonte_contrato':'specs/004-preparacao-avaliacao-ids/contracts/preparacao-avaliacao.md, secao 7',
          'isolamento_identidade':'PENDENTE, ver isolamento/ambiente.json' if i==14 else 'nao aplicavel'})
    dump(FIX/'matriz-controles.json',{'politica':'ids-proposta-004-v2','familias':matrix})
    print('Quatro pacotes ficticios sem referencia, fonte privada ou evidencias; notas reais preservadas.')
