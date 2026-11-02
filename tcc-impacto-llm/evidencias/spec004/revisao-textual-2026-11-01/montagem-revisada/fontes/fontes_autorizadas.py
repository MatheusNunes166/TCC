"""Preparacao editorial local de recortes enumerados. Sem gabarito/avaliador/rede."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys

from montagem_entradas import CONTRATO, NOMES, MUDANCAS, CONDICOES, sem_links

FONTES=(
    'materiais/04_NOTAS_E_PROMPTS.md',
    'materiais/07_DEFINICOES_COMUNS.md',
    'documentacao/requisitos.md',
    'documentacao/qualidade-e-testes.md',
    'specs/003-mudancas-controladas/spec.md',
    'materiais/modelos/schema_saida.json',
)

def sha(data):return hashlib.sha256(data).hexdigest()

def secao(data,inicio,fim):
    lines=data.splitlines(keepends=True)
    begins=[i for i,l in enumerate(lines) if l.decode('utf-8').strip()==inicio]
    ends=[i for i,l in enumerate(lines) if l.decode('utf-8').strip()==fim]
    if len(begins)!=1 or len(ends)!=1 or ends[0]<=begins[0]:
        raise ValueError('marcador ausente/duplicado/fora de ordem: '+inicio)
    return b''.join(lines[begins[0]:ends[0]])

def quote(data):
    lines=[l for l in data.splitlines(keepends=True) if l.startswith(b'> ')]
    if len(lines)!=1:raise ValueError('bloco literal de nota/pedido ambiguo')
    return lines[0]  # Preserve the exact note, including Markdown prefix and line ending.

def reunir_fontes(raiz,mudanca,condicao):
    if mudanca not in MUDANCAS or condicao not in CONDICOES:raise ValueError('mudanca/condicao invalida')
    root=sem_links(raiz);data={};provenance=[]
    for name in FONTES:
        p=sem_links(root/name)
        blob=p.read_bytes();blob.decode('utf-8');data[name]=blob
        provenance.append({'arquivo':name,'sha256':sha(blob),'tamanho_bytes':len(blob)})
    prompts=data[FONTES[0]]
    system=secao(prompts,'## 4.4 Pacote comum — montagem futura','## 4.5 Pedido direto — D0 e D1')
    prefix='1. Mensagem de sistema: '.encode()
    instructions=[l for l in system.splitlines(keepends=True) if l.startswith(prefix)]
    if len(instructions)!=1:raise ValueError('instrucao de sistema ausente/ambigua')
    catalog=secao(data[FONTES[3]],'## Doze casos da baseline','## Variantes e avaliação futura')
    rows=[]
    for line in catalog.decode('utf-8').splitlines():
        if line.startswith('|'):
            columns=[v.strip() for v in line.strip().strip('|').split('|')]
            if len(columns)<6:raise ValueError('catalogo sem campos esperados')
            rows.append('| '+' | '.join(columns[:6])+' |\n')
    if len(rows)<3:raise ValueError('catalogo sem testes')
    changes=secao(data[FONTES[4]],'### Mudanças e regras de origem','### Fontes de aceitação e rastreabilidade')
    selected=[]
    for line in changes.decode('utf-8').splitlines():
        if line.startswith('|'):
            cols=[v.strip() for v in line.strip().strip('|').split('|')]
            if len(cols)==4 and cols[1]==mudanca:selected.append(cols[2])
    if len(selected)!=1:raise ValueError('descricao da mudanca ausente/duplicada')
    pedido=secao(prompts, '## 4.5 Pedido direto — D0 e D1' if condicao[0]=='D' else '## 4.6 Pedido estruturado — E0 e E1',
                         '## 4.6 Pedido estruturado — E0 e E1' if condicao[0]=='D' else '## 4.7 Contrato de saída')
    docs={
        'sistema.txt':instructions[0][len(prefix):],
        'definicoes-comuns.md':data[FONTES[1]],
        'requisitos-baseline.md':secao(data[FONTES[2]],'## Entradas e saídas','## Situação da baseline completa e do incremento 1'),
        'catalogo-baseline.md':''.join(rows).encode(),
        'mudanca.md':(selected[0]+'\n').encode(),
        'pedido.txt':quote(pedido),
        'schema_saida.json':data[FONTES[5]],
    }
    if condicao in ('D1','E1'):
        docs['notas.md']=quote(secao(prompts,'## 4.2 Nota candidata única, comum a todas as mudanças','## 4.3 Como preparar e revisar as notas'))
    return docs,provenance

def gravar(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('x',encoding='utf-8',newline='\n') as f:
        json.dump(value,f,ensure_ascii=True,sort_keys=True,indent=2);f.write('\n')

def exportar(raiz,saida):
    root=sem_links(raiz);out=sem_links(saida)
    if out==root or root.is_relative_to(out):raise ValueError('saida sobreposta as fontes')
    if out.exists():raise ValueError('saida existente')
    # Output may be in the workspace, but never in any of the declared source directories.
    if any(out.is_relative_to((root/p).parent) for p in FONTES):raise ValueError('saida dentro de fonte autorizada')
    out.mkdir(parents=True,exist_ok=False);records=[]
    for change in sorted(MUDANCAS):
        for cond in CONDICOES:
            docs,provenance=reunir_fontes(root,change,cond)
            ident=change+'-'+cond;folder=out/'pacotes'/ident;folder.mkdir(parents=True)
            names=list(NOMES)
            if cond in ('D1','E1'):names.insert(5,'notas.md')
            entries=[]
            for name in names:
                blob=docs[name];(folder/name).write_bytes(blob)
                entries.append({'papel':name.split('.')[0],'arquivo':name,'versao':'recorte-D29-2026-11-01',
                  'sha256':sha(blob),'tamanho_bytes':len(blob),'revisao_conteudo':{
                    'estado':'conferido_tecnicamente','responsavel':'assistente; recorte editorial autorizado D29',
                    'data':'2026-11-01','alcance':'rastreabilidade do recorte; revisao profissional/cientifica pendente'}})
            manifest={'versao_contrato':CONTRATO,'pacote_id':ident,'versao_pacote':'D29-2026-11-01',
              'configuracao_id':'texto-autorizado-D29','mudanca':change,'condicao':cond,
              'status':'RASCUNHO_PREPARACAO','liberado_para_pesquisa':False,'documentos':entries,
              'status_notas':'RASCUNHO_NAO_REVISADO' if cond in ('D1','E1') else 'ausentes',
              'origem_notas':'pesquisador, representa conhecimento de analista; revisao profissional pendente' if cond in ('D1','E1') else 'ausentes'}
            gravar(folder/'manifesto.json',manifest)
            auth=out/'autorizacoes'/(ident+'.json')
            gravar(auth,{'versao':'autorizacao-textual-v1','status':'CONFERIDO_TECNICAMENTE_RASCUNHO',
              'manifesto_sha256':sha((folder/'manifesto.json').read_bytes()),
              'documentos':[{'arquivo':e['arquivo'],'sha256':e['sha256']} for e in entries],
              'fontes':provenance,'receita':'recortes-D29-v1','revisao_cientifica':'pendente',
              'regras_de_recorte':'sistema/pedido/nota: blocos literais; requisitos: contrato inicial; catalogo: seis primeiras colunas da baseline; mudanca: somente descricao; definicoes/schema integrais'})
            records.append({'id':ident,'pacote':folder.relative_to(out).as_posix(),'autorizacao':auth.relative_to(out).as_posix()})
    gravar(out/'indice.json',{'contrato':CONTRATO,'origem':'preparacao_local_nao_enviada','pacotes':records,
      'instante_utc':datetime.now(timezone.utc).isoformat(),'envio_realizado':False})
    return records

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--raiz',required=True);p.add_argument('--saida',required=True)
    args=p.parse_args(argv)
    try:records=exportar(args.raiz,args.saida);print(json.dumps({'pacotes':len(records),'envio_realizado':False}));return 0
    except (OSError,ValueError) as exc:print(str(exc),file=sys.stderr);return 2

if __name__=='__main__':raise SystemExit(main())
