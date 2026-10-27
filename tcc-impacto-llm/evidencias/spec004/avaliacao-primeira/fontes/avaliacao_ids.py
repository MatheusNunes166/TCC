"""Avaliacao offline de IDs. Le referencia exclusivamente aqui; sem montagem ou LLM."""
import argparse
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
from itertools import combinations
import json
import os
from pathlib import Path
import stat
import sys
import uuid

POLITICA='ids-proposta-004-v2'
REGRAS={'versao':POLITICA,'status':'CANDIDATA_REVISAO_CIENTIFICA_PENDENTE',
        'PONT-01':'rejeitar mistura; preservar grupos por versao sem combinado',
        'PONT-02':'configuracao/mudanca/condicao/repeticao unicos; tentativas vinculadas',
        'desconhecidos':'FP unico','duplicatas':'conjunto unico','invalidas':'nulo; imputacao PRF opcional',
        'vazias':'PRF=0 com G nao vazio','jaccard_vazios':'1; nao e qualidade',
        'jaccard_insuficiente':'nao calculavel','json':'UTF8 estrito sem BOM; chaves unicas; sem NaN/Infinity'}
UNIVERSOS={'requisitos':{f'RF-{i:02}' for i in range(1,5)},'testes':{f'T{i:02}' for i in range(1,13)}}
MUDANCAS={'MC-01','MC-02','MC-03','MC-04-v2'}

def sha(data):return hashlib.sha256(data).hexdigest()
def serial(value):return (json.dumps(value,ensure_ascii=True,sort_keys=True,indent=2)+'\n').encode()
POLITICA_SHA=sha(serial(REGRAS))

class FormatoInvalido(ValueError):
    def __init__(self,msg,etapa='sintaxe'):
        super().__init__(msg);self.etapa=etapa

def pares_unicos(pairs):
    out={}
    for k,v in pairs:
        if k in out:raise ValueError('chave JSON repetida')
        out[k]=v
    return out

def constante_invalida(value):raise ValueError('constante JSON invalida: '+value)

def json_estrito(data):
    # decode() deliberately preserves BOM, which the JSON parser rejects.
    return json.loads(data.decode('utf-8'),object_pairs_hook=pares_unicos,parse_constant=constante_invalida)

def parse_resposta(data):
    try:obj=json_estrito(data)
    except (ValueError,UnicodeError,RecursionError) as e:raise FormatoInvalido(str(e)) from e
    if (not isinstance(obj,dict) or set(obj)!=set(UNIVERSOS) or
        any(not isinstance(obj[k],list) or any(not isinstance(v,str) for v in obj[k]) for k in UNIVERSOS)):
        raise FormatoInvalido('objeto deve ter exatamente requisitos/testes como listas de strings','contrato')
    return obj

def texto(v):return isinstance(v,str) and bool(v.strip())
def canonica(mudanca):return 'MC-04-v2' if mudanca=='MC-04' else mudanca

def referencia_da_mudanca(ref,mudanca):
    if not isinstance(ref,dict) or not texto(ref.get('versao')) or not texto(ref.get('status')):
        raise ValueError('referencia sem versao/status')
    changes=ref.get('mudancas')
    if not isinstance(changes,list) or any(not isinstance(c,dict) for c in changes):raise ValueError('mudancas invalidas')
    ids=[c.get('id') for c in changes]
    if any(not isinstance(i,str) for i in ids) or len(set(ids))!=len(ids):raise ValueError('mudanca duplicada/invalida')
    name=canonica(mudanca)
    if name not in MUDANCAS or ids.count(name)!=1:raise ValueError('mudanca ausente')
    c=changes[ids.index(name)];expected={}
    for dim,field in [('requisitos','rfs'),('testes','tests')]:
        values=c.get(field)
        if (not isinstance(values,list) or not values or any(not isinstance(v,str) for v in values)
            or len(set(values))!=len(values) or not set(values)<=UNIVERSOS[dim]):
            raise ValueError('conjunto esperado vazio/duplicado/desconhecido/tipo invalido: '+field)
        expected[dim]=set(values)
    return name,expected

def numero(value):
    f=Fraction(value)
    return {'numerador':f.numerator,'denominador':f.denominator,'fracao':str(f),'decimal':format(float(f),'.6f')}

def quociente(n,d):return numero(Fraction(n,d)) if d else None

def comparar(lista,g,dim):
    selected=set(lista);positions={}
    for i,value in enumerate(lista):positions.setdefault(value,[]).append(i)
    tp=len(selected & g);fp=len(selected-g);fn=len(g-selected)
    return {'lista_original':lista,'S':sorted(selected),'G':sorted(g),
        'acertos':sorted(selected & g),'excedentes':sorted(selected-g),'omissoes':sorted(g-selected),
        'desconhecidos':sorted(selected-UNIVERSOS[dim]),
        'duplicatas':[{'id':k,'posicoes':p,'repeticoes':p[1:]} for k,p in positions.items() if len(p)>1],
        'TP':tp,'FP':fp,'FN':fn,'metricas_propostas':{
          'precisao':numero(Fraction(tp,tp+fp) if selected else 0),
          'revocacao':numero(Fraction(tp,tp+fn)),
          'f1':numero(Fraction(2*tp,2*tp+fp+fn)),
          'selecao_completa':int(fn==0),'correspondencia_exata':int(selected==g)}}

def avaliar_resposta(data,referencia,mudanca='MC-01',estado_tecnico='concluida'):
    result={'mudanca_pedida':mudanca,'mudanca':canonica(mudanca),'status_avaliacao':None,
      'json_sintatico':'nao_analisado','formato_contrato':'nao_analisado',
      'somente_ids_conhecidos':None,'requisitos':None,'testes':None,'causa':None}
    try:name,g=referencia_da_mudanca(referencia,mudanca);result['mudanca']=name
    except (ValueError,TypeError) as e:
        result.update(status_avaliacao='erro_referencia',causa=str(e));return result
    if estado_tecnico=='falha_tecnica':result['status_avaliacao']='falha_tecnica';return result
    if estado_tecnico!='concluida':raise ValueError('estado tecnico invalido')
    try:obj=parse_resposta(data)
    except FormatoInvalido as e:
        result.update(status_avaliacao='resposta_formato_invalido',causa=str(e),
            json_sintatico='valido' if e.etapa=='contrato' else 'invalido',formato_contrato='invalido')
        return result
    result.update(status_avaliacao='avaliada',json_sintatico='valido',formato_contrato='valido')
    for dim in UNIVERSOS:result[dim]=comparar(obj[dim],g[dim],dim)
    result['somente_ids_conhecidos']=all(not result[d]['desconhecidos'] for d in UNIVERSOS)
    result['ids_conhecidos_por_dimensao']={d:not result[d]['desconhecidos'] for d in UNIVERSOS}
    return result

def caminho_seguro(path):
    p=Path(os.path.abspath(path))
    for item in (p,*p.parents):
        if item.exists() or item.is_symlink():
            info=item.lstat()
            if stat.S_ISLNK(info.st_mode) or getattr(info,'st_file_attributes',0)&0x400:
                raise ValueError('link/junction/reparse proibido: '+str(item))
    return p

def relativo(root,name):
    if not isinstance(name,str) or not name or Path(name).is_absolute() or '..' in Path(name).parts:
        raise ValueError('caminho relativo invalido')
    path=caminho_seguro(root/name)
    if not path.is_relative_to(root):raise ValueError('caminho externo')
    return path

def ler(path,tracked):
    path=caminho_seguro(path);data=path.read_bytes();tracked.append((path,sha(data)));return data

def salvar(path,data,tracked):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('xb') as stream:stream.write(data)
    tracked.append((path,sha(data)))

def revalidar(entries):
    for path,digest in entries:
        caminho_seguro(path)
        if sha(path.read_bytes())!=digest:raise ValueError('integridade alterada: '+str(path))

def nova_saida(path,inputs):
    out=caminho_seguro(path)
    if out.exists():raise ValueError('saida ja existe')
    for inp in inputs:
        p=caminho_seguro(inp)
        if p.is_relative_to(out) or out==p or out.is_relative_to(p.parent):
            raise ValueError('saida sobreposta a raiz de importacao')
    out.mkdir(parents=True,exist_ok=False);return out

def finalizar(out,result,code,tracked,filename):
    try:revalidar(tracked)
    except (OSError,ValueError) as e:
        result.update(completo=False,status_avaliacao='erro_integridade',causa=str(e))
        if 'requisitos' in result:result['requisitos']=result['testes']=None
        code=2
    try:
        salvar(out/filename,serial(result),tracked)
        manifest={'completo':result.get('completo',False),'retorno':code,
          'origem':'sintetica','arquivos':[{'arquivo':str(p.relative_to(out)),'sha256':h} for p,h in tracked if p.is_relative_to(out)],
          'fontes':[{'arquivo':str(p),'sha256':h} for p,h in tracked if not p.is_relative_to(out)]}
        revalidar(tracked)
        salvar(out/'manifesto.json',serial(manifest),[])
    except (OSError,ValueError) as e:
        result.update(completo=False,status_avaliacao='erro_integridade',causa=str(e));code=2
        # Preserve partial files; a separate diagnostic cannot certify completeness.
        try:salvar(out/'erro-fechamento.json',serial(result),[])
        except OSError:pass
    return result,code

def identidade(record):
    for field in ('configuracao_id','observacao_id'):
        if not texto(record.get(field)):raise ValueError('identidade sem '+field)
    repeat=record.get('repeticao_sintetica')
    if type(repeat) is not int or repeat<1:raise ValueError('repeticao deve ser inteiro positivo')
    change=canonica(record.get('mudanca'))
    if change not in MUDANCAS or record.get('condicao') not in ('D0','D1','E0','E1'):raise ValueError('celula invalida')
    return (record['configuracao_id'],change,record['condicao'],repeat)

def avaliar(preparacao,tentativa,referencia,saida,avaliacao_anterior=None):
    inputs=[Path(preparacao),Path(tentativa),Path(referencia)]
    if avaliacao_anterior:inputs.append(Path(avaliacao_anterior))
    out=nova_saida(saida,inputs);tracked=[]
    result={'avaliacao_id':uuid.uuid4().hex,'instante_utc':datetime.now(timezone.utc).isoformat(),
      'completo':False,'origem':'sintetica','modelo_reportado':None,
      'politica':{'versao':POLITICA,'sha256':POLITICA_SHA,'status':'CANDIDATA_REVISAO_CIENTIFICA_PENDENTE'},
      'avaliador_sha256':sha(Path(__file__).read_bytes()),'requisitos':None,'testes':None}
    code=2
    try:
        preparacao=caminho_seguro(preparacao);tentativa=caminho_seguro(tentativa)
        prepraw=ler(preparacao,tracked);traw=ler(tentativa,tracked)
        salvar(out/'preparacao-original.json',prepraw,tracked);salvar(out/'tentativa-original.json',traw,tracked)
        prep=json_estrito(prepraw);t=json_estrito(traw);identidade(t)
        if (t.get('origem')!='sintetica' or t.get('modelo_reportado') is not None
            or not texto(t.get('tentativa_id')) or t.get('estado_tecnico') not in ('concluida','falha_tecnica')):
            raise ValueError('registro sintetico/estado tecnico invalido')
        if t['estado_tecnico']=='falha_tecnica' and not texto(t.get('causa')):raise ValueError('falha sem causa')
        if prep.get('completo') is not True or prep.get('status')!='PREPARADO_LOCAL_NAO_ENVIADO':raise ValueError('preparacao nao utilizavel')
        if (t.get('preparacao_sha256')!=sha(prepraw) or t.get('preparacao_id')!=prep.get('preparacao_id')
            or t.get('payload_sha256')!=prep.get('payload_sha256')
            or any(t.get(k)!=prep.get(k) for k in ('configuracao_id','mudanca','condicao'))):
            raise ValueError('vinculo com preparacao divergente')
        arquivos=prep.get('arquivos')
        if not isinstance(arquivos,list) or not arquivos:raise ValueError('preparacao sem arquivos')
        names=set()
        for item in arquivos:
            p=relativo(preparacao.parent,item['arquivo'])
            if item['arquivo'] in names:raise ValueError('arquivo duplicado na preparacao')
            names.add(item['arquivo']);blob=ler(p,tracked)
            if sha(blob)!=item.get('sha256'):raise ValueError('arquivo de preparacao alterado')
            salvar(out/'entrada'/item['arquivo'],blob,tracked)
            if item['arquivo']=='payload.txt' and sha(blob)!=prep['payload_sha256']:raise ValueError('payload divergente')
        if 'payload.txt' not in names:raise ValueError('payload ausente')
        response=None
        if t.get('resposta_arquivo') is not None:
            response=ler(relativo(tentativa.parent,t['resposta_arquivo']),tracked)
            salvar(out/'resposta-original.bin',response,tracked)
            if t.get('resposta_sha256')!=sha(response) or type(t.get('resposta_tamanho')) is not int or t['resposta_tamanho']!=len(response):
                raise ValueError('hash/tamanho da resposta divergente')
        elif any(t.get(k) is not None for k in ('resposta_sha256','resposta_tamanho')):raise ValueError('ausencia inconsistente')
        if t['estado_tecnico']=='concluida' and (response is None or t.get('fragmento')):raise ValueError('concluida sem resposta integral')
        for k in ('observacao_id','tentativa_id','tentativa_anterior','configuracao_id','mudanca','condicao',
                  'repeticao_sintetica','payload_sha256','estado_tecnico','fragmento'):
            result[k]=t.get(k)
        result['causa_tecnica']=t.get('causa');result['resposta_sha256']=t.get('resposta_sha256')
        if avaliacao_anterior:
            prevraw=ler(avaliacao_anterior,tracked);prev=json_estrito(prevraw)
            if any(prev.get(k)!=result.get(k) for k in ('observacao_id','tentativa_id','payload_sha256','resposta_sha256')):
                raise ValueError('reavaliacao anterior de outra tentativa/resposta')
            salvar(out/'avaliacao-anterior.json',prevraw,tracked);result['avaliacao_anterior']=prev['avaliacao_id']
        else:result['avaliacao_anterior']=None
        refraw=ler(referencia,tracked);salvar(out/'referencia-privada.json',refraw,tracked)
        try:ref=json_estrito(refraw)
        except (ValueError,UnicodeError):ref=None
        result.update(avaliar_resposta(response,ref,t['mudanca'],t['estado_tecnico']))
        result['referencia']={'sha256':sha(refraw),'versao':ref.get('versao') if isinstance(ref,dict) else None,
            'status':ref.get('status') if isinstance(ref,dict) else None}
        salvar(out/'politica-candidata.json',serial(REGRAS),tracked)
        result['completo']=True
        code=0 if result['status_avaliacao']=='avaliada' else 2 if result['status_avaliacao']=='erro_referencia' else 1
    except (OSError,ValueError,TypeError,KeyError,RecursionError) as e:
        result.update(status_avaliacao='erro_integridade',causa=str(e),completo=False);code=2
    return finalizar(out,result,code,tracked,'avaliacao.json')

def _versao(record):
    p=record['politica'];r=record['referencia']
    signature=(p['versao'],p['sha256'],r['versao'],r['sha256'])
    if any(not texto(s) for s in signature):raise ValueError('versao/hash ausente')
    return signature

def _celula(key):return {'configuracao_id':key[0],'mudanca':key[1],'condicao':key[2]}

def jaccard(regs,dim):
    pairs=[]
    for x,y in combinations(regs,2):
        if x['repeticao_sintetica']==y['repeticao_sintetica']:raise ValueError('repeticao duplicada nao adjudicada')
        s=set(x[dim]['S']);t=set(y[dim]['S']);u=s|t
        pairs.append({'observacoes':[x['observacao_id'],y['observacao_id']],
          'intersecao':len(s&t),'uniao':len(u),'valor':numero(Fraction(len(s&t),len(u)) if u else 1)})
    return {'estado':'calculavel' if pairs else 'nao_calculavel',
      'motivo':None if pairs else 'não calculável','observacoes':len(regs),'numero_pares':len(pairs),
      'pares':pairs,'valor':numero(sum(Fraction(p['valor']['fracao']) for p in pairs)/len(pairs)) if pairs else None}

def _grupo(regs,plans,imputar):
    obs={}
    for r in regs:obs.setdefault(r['observacao_id'],[]).append(r)
    finals=[]
    for oid,rs in obs.items():
        byid={r['tentativa_id']:r for r in rs}
        if len(byid)!=len(rs) or len(rs)>2:raise ValueError('tentativa duplicada/limite excedido')
        first=[r for r in rs if r.get('tentativa_anterior') is None]
        if len(first)!=1:raise ValueError('cadeia de tentativas invalida')
        first=first[0]
        if len(rs)==2:
            second=next(r for r in rs if r is not first)
            if (first['status_avaliacao']!='falha_tecnica' or second.get('tentativa_anterior')!=first['tentativa_id']
                or second['payload_sha256']!=first['payload_sha256']):raise ValueError('retentativa invalida')
            finals.append(second)
        else:finals.append(first)
    valid=[r for r in finals if r['status_avaliacao']=='avaliada']
    invalid=[r for r in finals if r['status_avaliacao']=='resposta_formato_invalido']
    technical=[r for r in finals if r['status_avaliacao']=='falha_tecnica']
    if len(valid)+len(invalid)+len(technical)!=len(finals):raise ValueError('avaliacao com erro de mecanismo/referencia')
    n=len(plans);v=len(valid);i=len(invalid);c=v+i;t=len(technical)
    counts={'N':n,'A':len(regs),'C':c,'V':v,'I':i,'T':t,'K':sum(r['somente_ids_conhecidos'] is True for r in valid)}
    def means(denom):
        return {dim:{metric:numero(sum(Fraction(r[dim]['metricas_propostas'][metric]['fracao']) for r in valid)/denom)
                if denom else None for metric in ('precisao','revocacao','f1')} for dim in UNIVERSOS}
    group={'contagens':counts,'taxas':{'validade':quociente(v,c),'ids_conhecidos':quociente(counts['K'],v),'completude':quociente(c,n)},
      'validas':means(v),'jaccard':{d:jaccard(valid,d) for d in UNIVERSOS},
      'ausentes':[p['observacao_id'] for p in plans if p['observacao_id'] not in obs],
      'exclusoes':[{'observacao_id':r['observacao_id'],'motivo':r['status_avaliacao']} for r in finals if r not in valid],
      'avaliacoes':[r['avaliacao_id'] for r in regs]}
    if imputar:
        group['operacional']=means(v+i)
        group['imputacoes']=[{'observacao_id':r['observacao_id'],'P_RF_T':0,'R_RF_T':0,'F1_RF_T':0,'origem':'imputacao_nao_observacao'} for r in invalid]
    return group,1 if i or t or len(finals)<n else 0

def resumir_registros(avaliacoes,planejadas,imputar=False):
    result={'origem':'sintetica','politica':POLITICA,'completo':True,'celulas':[]}
    if not isinstance(avaliacoes,list) or not isinstance(planejadas,list):raise ValueError('listas explicitas requeridas')
    cells={};global_obs={};global_attempt={};bad_cells=set()
    for kind,entries in [('plans',planejadas),('regs',avaliacoes)]:
        for r in entries:
            key=identidade(r);cell=key[:3]
            node=cells.setdefault(cell,{'plans':[],'regs':[]});node[kind].append(r)
            if r['observacao_id'] in global_obs and global_obs[r['observacao_id']]!=key:
                bad_cells.update([cell,global_obs[r['observacao_id']][:3]])
            global_obs[r['observacao_id']]=key
            if kind=='regs':
                tid=r.get('tentativa_id')
                if not texto(tid):bad_cells.add(cell)
                if tid in global_attempt:bad_cells.update([cell,global_attempt[tid]])
                global_attempt[tid]=cell
    code=0
    for key,node in cells.items():
        cell={**_celula(key),'resultado_combinado':None,'grupos':[],'diagnosticos':[]}
        result['celulas'].append(cell);regs=node['regs'];plans=node['plans']
        try:
            if key in bad_cells:raise ValueError('identidade/tentativa duplicada')
            planids=[r['observacao_id'] for r in plans];plankeys=[identidade(r) for r in plans]
            if len(set(planids))!=len(planids) or len(set(plankeys))!=len(plankeys):raise ValueError('observacao planejada duplicada')
            observed={}
            for r in regs:
                if (r.get('origem')!='sintetica' or r.get('modelo_reportado') is not None or r.get('completo') is not True):
                    raise ValueError('registro nao sintetico ou incompleto')
                if r['observacao_id'] not in planids:raise ValueError('observacao nao planejada')
                plan=plans[planids.index(r['observacao_id'])]
                if identidade(plan)!=identidade(r) or plan.get('payload_sha256')!=r.get('payload_sha256'):raise ValueError('identidade/payload divergente')
                k=identidade(r)
                if k in observed and observed[k]!=r['observacao_id']:raise ValueError('repeticao duplicada')
                observed[k]=r['observacao_id']
            signatures={_versao(r) for r in regs}
            if len(signatures)>1:
                cell['diagnosticos']=['versoes_distintas']
                # Separate inventories, without inventing planned denominators per version.
                for signature in sorted(signatures):
                    cell['grupos'].append({'versoes':list(signature),'avaliacoes':[r['avaliacao_id'] for r in regs if _versao(r)==signature],
                        'resumo':None,'motivo':'Rejeitada agregacao mista; solicitar lista explicita homogenea para novo resumo.'})
                code=2;continue
            group,groupcode=_grupo(regs,plans,imputar)
            group['versoes']=list(next(iter(signatures))) if signatures else None
            cell['grupos']=[group];code=max(code,groupcode)
        except (ValueError,KeyError,TypeError,ZeroDivisionError) as e:
            cell['diagnosticos']=[str(e)];cell['grupos']=[];code=2
    result['completo']=code!=2
    return result,code

def resumir(avaliacoes,observacoes,saida,imputar=False):
    out=nova_saida(saida,[Path(avaliacoes),Path(observacoes)]);tracked=[]
    result={'completo':False,'origem':'sintetica','celulas':[]};code=2
    try:
        path=caminho_seguro(avaliacoes)
        lraw=ler(path,tracked);praw=ler(observacoes,tracked)
        salvar(out/'lista-original.json',lraw,tracked);salvar(out/'planejadas-original.json',praw,tracked)
        lista=json_estrito(lraw);plans=json_estrito(praw)
        if not isinstance(lista,list):raise ValueError('lista explicita requerida')
        regs=[]
        for i,entry in enumerate(lista):
            data=ler(relativo(path.parent,entry['arquivo']),tracked)
            salvar(out/f'avaliacoes/{i:04}.json',data,tracked)
            if sha(data)!=entry.get('sha256'):raise ValueError('hash de avaliacao divergente')
            regs.append(json_estrito(data))
        result,code=resumir_registros(regs,plans,imputar)
        result.update(resumo_id=uuid.uuid4().hex,instante_utc=datetime.now(timezone.utc).isoformat(),avaliador_sha256=sha(Path(__file__).read_bytes()))
    except (OSError,ValueError,TypeError,KeyError) as e:
        result.update(completo=False,causa=str(e));code=2
    return finalizar(out,result,code,tracked,'resumo.json')

def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__);commands=parser.add_subparsers(dest='comando',required=True)
    ev=commands.add_parser('avaliar')
    for k in ('preparacao','tentativa','referencia','saida'):ev.add_argument('--'+k,required=True)
    ev.add_argument('--avaliacao-anterior')
    su=commands.add_parser('resumir')
    for k in ('avaliacoes','observacoes','saida'):su.add_argument('--'+k,required=True)
    su.add_argument('--imputar-invalidas',action='store_true')
    args=parser.parse_args(argv)
    try:
        if args.comando=='avaliar':r,code=avaliar(args.preparacao,args.tentativa,args.referencia,args.saida,args.avaliacao_anterior)
        else:r,code=resumir(args.avaliacoes,args.observacoes,args.saida,args.imputar_invalidas)
        print(json.dumps({'retorno':code,'completo':r['completo']}));return code
    except (OSError,ValueError) as e:print(str(e),file=sys.stderr);return 2

if __name__=='__main__':raise SystemExit(main())
