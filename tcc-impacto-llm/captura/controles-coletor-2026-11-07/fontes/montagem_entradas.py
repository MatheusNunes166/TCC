"""Montagem local por lista fechada. Sem referencia, rede ou envio de mensagens."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path, PureWindowsPath
import stat
import sys
import uuid

CONTRATO = 'spec004-v3'
NOMES = ('sistema.txt','definicoes-comuns.md','requisitos-baseline.md',
         'catalogo-baseline.md','mudanca.md','pedido.txt','schema_saida.json')
CONDICOES = ('D0','D1','E0','E1')
MUDANCAS = ('MC-01','MC-02','MC-03','MC-04-v2')

def sha(data):
    return hashlib.sha256(data).hexdigest()

def reparse(path):
    try:s=path.lstat()
    except FileNotFoundError:return False
    return stat.S_ISLNK(s.st_mode) or bool(getattr(s,'st_file_attributes',0) & 0x400)

def sem_links(path):
    """Valida caminho local; nao e mecanismo de isolamento por SO."""
    w=PureWindowsPath(os.fspath(path))
    if w.drive.startswith('\\\\') or (w.drive and not w.root):
        raise ValueError('UNC/dispositivo/drive relativo nao suportado')
    if os.name=='nt' and w.root and not w.drive:raise ValueError('raiz sem drive nao suportada')
    parts=[p for p in w.parts if p!=w.anchor and p not in ('.','..')]
    if any(':' in p or p.endswith(('.', ' ')) for p in parts):raise ValueError('fluxo alternativo/alias de caminho nao suportado')
    devices={'CON','PRN','AUX','NUL'}|{f'{p}{i}' for p in ('COM','LPT') for i in range(1,10)}
    if any(p.split('.')[0].upper() in devices for p in parts):raise ValueError('dispositivo nao suportado')
    p=Path(os.path.abspath(path))
    for item in (p,*p.parents):
        if reparse(item):
            raise ValueError(f'link/junction/reparse point proibido: {item}')
    return p

def _pairs(pairs):
    out={}
    for k,v in pairs:
        if k in out:raise ValueError('chave JSON repetida')
        out[k]=v
    return out

def _invalid_constant(value):
    raise ValueError('constante fora de JSON: '+value)

def _json(data):
    return json.loads(data.decode('utf-8'),object_pairs_hook=_pairs,parse_constant=_invalid_constant)

def _text(value):
    return isinstance(value,str) and bool(value.strip())

def _dump(path,value):
    with path.open('x',encoding='utf-8',newline='\n') as stream:
        json.dump(value,stream,ensure_ascii=True,indent=2,sort_keys=True)
        stream.write('\n')

def revalidar(entries):
    for p,digest in entries:
        sem_links(p)
        if sha(p.read_bytes())!=digest:raise ValueError(f'integridade alterada: {p}')

def preparar(pacote,manifesto,saida,autorizacao=None):
    root=sem_links(pacote);manifesto=sem_links(manifesto);out=sem_links(saida)
    if not root.is_dir() or manifesto!=root/'manifesto.json':raise ValueError('manifesto fora da raiz permitida')
    if out==root or out.is_relative_to(root) or root.is_relative_to(out):raise ValueError('saida sobreposta a entrada')
    if out.exists():raise ValueError('saida ja existe')
    if autorizacao is None:raise ValueError('autorizacao externa explicita obrigatoria')
    autorizacao=sem_links(autorizacao)
    if autorizacao.is_relative_to(root) or autorizacao.is_relative_to(out):
        raise ValueError('autorizacao deve ficar fora do pacote/saida')
    out.mkdir(parents=True,exist_ok=False)
    base={'preparacao_id':uuid.uuid4().hex,'contrato':CONTRATO,'instante_utc':datetime.now(timezone.utc).isoformat(),
          'liberado_para_pesquisa':False,'completo':False,'status':'BLOQUEADO',
          'montador_sha256':sha(Path(__file__).read_bytes())}
    tracked=[];artifacts=[]
    try:
        raw=manifesto.read_bytes();tracked.append((manifesto,sha(raw)));m=_json(raw)
        if not isinstance(m,dict):raise ValueError('manifesto deve ser objeto')
        for field in ('versao_contrato','pacote_id','versao_pacote','configuracao_id'):
            if not _text(m.get(field)):raise ValueError('campo obrigatorio: '+field)
        if m['versao_contrato']!=CONTRATO:raise ValueError('versao de contrato incompativel')
        if m.get('politica_bytes') not in (None,'utf8-sem-bom-lf-v1'):
            raise ValueError('politica de bytes incompativel')
        if 'politica_bytes' in m:base['politica_bytes']=m['politica_bytes']
        if m.get('mudanca') not in MUDANCAS or m.get('condicao') not in CONDICOES:raise ValueError('mudanca/condicao invalida')
        if m.get('status')!='RASCUNHO_PREPARACAO' or m.get('liberado_para_pesquisa') is not False:
            raise ValueError('pacote nao e preparacao local em rascunho')
        names=list(NOMES);notes=m['condicao'] in ('D1','E1')
        if notes:names.insert(5,'notas.md')
        if m.get('status_notas')!=('RASCUNHO_NAO_REVISADO' if notes else 'ausentes'):
            raise ValueError('estado das notas incompativel')
        entries=m.get('documentos')
        if not isinstance(entries,list) or any(not isinstance(e,dict) for e in entries):raise ValueError('lista de documentos invalida')
        if [e.get('arquivo') for e in entries]!=names:raise ValueError('lista/ordem de arquivos nao permitida')
        # Only this explicitly supplied flat package is enumerated, never the repository.
        for p in root.iterdir():sem_links(p)
        if {p.name for p in root.iterdir()}!=set(names)|{'manifesto.json'}:raise ValueError('arquivo extra/ausente no pacote')
        authorization_raw=autorizacao.read_bytes();a=_json(authorization_raw)
        tracked.append((autorizacao,sha(authorization_raw)))
        if (not isinstance(a,dict) or a.get('versao')!='autorizacao-textual-v1'
            or a.get('status')!='CONFERIDO_TECNICAMENTE_RASCUNHO'
            or a.get('manifesto_sha256')!=sha(raw)
            or a.get('documentos')!=[{'arquivo':e.get('arquivo'),'sha256':e.get('sha256')} for e in entries]):
            raise ValueError('pacote/manifesto diverge da autorizacao externa')
        blobs=[]
        for e in entries:
            name=e['arquivo'];p=sem_links(root/name)
            if not p.is_file() or e.get('papel')!=name.split('.')[0]:raise ValueError('papel/arquivo invalido')
            revision=e.get('revisao_conteudo',{})
            if not isinstance(revision,dict) or revision.get('estado')!='conferido_tecnicamente':raise ValueError('conteudo pendente/reprovado')
            if not all(_text(revision.get(k)) for k in ('responsavel','data')):raise ValueError('revisao sem responsavel/data')
            if not _text(e.get('versao')):raise ValueError('documento sem versao')
            blob=p.read_bytes();blob.decode('utf-8')
            if m.get('politica_bytes')=='utf8-sem-bom-lf-v1' and (blob.startswith(b'\xef\xbb\xbf') or b'\r' in blob):
                raise ValueError('documento diverge da politica UTF-8 sem BOM/LF')
            if e.get('sha256')!=sha(blob) or type(e.get('tamanho_bytes')) is not int or e['tamanho_bytes']!=len(blob):
                raise ValueError('hash/tamanho divergente')
            tracked.append((p,sha(blob)));blobs.append((e,blob))
        payload=b''.join(f'<<<inicio:{e["papel"]}>>>\n'.encode()+b+f'\n<<<fim:{e["papel"]}>>>\n'.encode() for e,b in blobs)
        def save(relative,data):
            p=out/relative;p.parent.mkdir(parents=True,exist_ok=True)
            with p.open('xb') as f:f.write(data)
            tracked.append((p,sha(data)));artifacts.append({'arquivo':relative,'sha256':sha(data)})
        save('manifesto-original.json',raw)
        save('autorizacao-original.json',authorization_raw)
        for e,b in blobs:save('documentos/'+e['arquivo'],b)
        save('payload.txt',payload)
        delivery={'contrato':'texto-apenas-D29','payload_arquivo':'payload.txt','payload_sha256':sha(payload),
                  'ferramentas':[],'anexos_ambiente':[],'historico_conversa':False,
                  'envio_realizado':False,'isolamento_por_SO_alegado':False,
                  'limite':'Somente este texto e destinado ao modelo. Entrega real nao exercitada; sem acesso adicional.'}
        save('entrega-textual.json',(json.dumps(delivery,ensure_ascii=True,sort_keys=True,indent=2)+'\n').encode())
        base.update({k:m[k] for k in ('configuracao_id','mudanca','condicao','status_notas','versao_pacote','pacote_id')})
        base.update(payload_sha256=sha(payload),payload_tamanho=len(payload),manifesto_sha256=sha(raw),
                    documentos=entries,arquivos=artifacts,status='PREPARADO_LOCAL_NAO_ENVIADO',
                    autorizacao_sha256=sha(authorization_raw),fronteira='conteudo_textual_sem_ferramentas',isolamento_por_SO_alegado=False)
        revalidar(tracked)
        base['completo']=True
        _dump(out/'preparacao.json',base)
        return base
    except (OSError,ValueError,KeyError,TypeError,RecursionError) as exc:
        base.update(completo=False,status='BLOQUEADO',causa=str(exc))
        diagnostic=out/('erro.json' if (out/'preparacao.json').exists() else 'preparacao.json')
        try:_dump(diagnostic,base)
        except OSError:pass
        raise ValueError(str(exc)) from exc

def conferir_condicoes(preparacoes):
    """Confronta metadados das preparacoes locais; nao abre fontes privadas."""
    if not preparacoes:raise ValueError('nenhuma preparacao')
    for r in preparacoes:
        if r.get('completo') is not True:raise ValueError('preparacao incompleta')
    by_change={}
    note_hash=None
    for r in preparacoes:
        group=by_change.setdefault((r['configuracao_id'],r['mudanca']),{})
        if r['condicao'] in group:raise ValueError('condicao duplicada')
        docs={e['arquivo']:e['sha256'] for e in r['documentos']}
        group[r['condicao']]=docs
        if 'notas.md' in docs:
            if note_hash is not None and note_hash!=docs['notas.md']:raise ValueError('notas diferentes')
            note_hash=docs['notas.md']
    for group in by_change.values():
        if set(group)!=set(CONDICOES):raise ValueError('quatro condicoes requeridas')
        for name in NOMES:
            if name=='pedido.txt':
                for x,y in [('D0','D1'),('E0','E1')]:
                    if group[x][name]!=group[y][name]:raise ValueError('pedido diferente')
            elif len({d[name] for d in group.values()})!=1:raise ValueError('documentos comuns diferentes')
    return True

def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ('pacote','manifesto','saida','autorizacao'):parser.add_argument('--'+name,required=True)
    args=parser.parse_args(argv)
    try:
        r=preparar(args.pacote,args.manifesto,args.saida,args.autorizacao)
        print(json.dumps({'preparacao_id':r['preparacao_id'],'status':r['status']}));return 0
    except (ValueError,OSError) as exc:
        print(str(exc),file=sys.stderr);return 2

if __name__=='__main__':raise SystemExit(main())
