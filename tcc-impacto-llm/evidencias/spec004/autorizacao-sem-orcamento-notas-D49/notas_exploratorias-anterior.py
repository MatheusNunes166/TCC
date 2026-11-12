"""D-47: adaptador do bloco de notas; transporte e metricas sao os existentes.

O envio exige flag E autorizacao humana separada ligada ao hash do plano.
Preparacao, simulacao, controle, avaliacao e revisao sao comandos distintos.
"""
import argparse
import copy
from datetime import datetime
from decimal import Decimal, InvalidOperation
import json
from pathlib import Path
import sys

import coletor_api as api

ROOT = Path(__file__).resolve().parent
BASE = ROOT / 'captura/notas-mc04-0.3-001'
HASH_BASE = 'f4b2cbf4bbeabd4fc199e9e29084956761279e70aeb3f35ddeb4e2f0b45d89a8'
ETAPA = 'notas-mc04-0.3-D46'
VERSAO = 'integracao-notas-v1-D47'
ARQUIVADAS = ROOT / 'evidencias/spec004/integracao-notas-0.3-D47/fontes-anteriores'
FONTES = ('notas_exploratorias.py', 'coletor_api.py', 'avaliacao_ids.py',
          'revisao_conformidade.py', 'coletor_piloto.py', 'montagem_entradas.py')
IDENTIDADE = ('observacao_id','modelo','mudanca','condicao','nota_id','repeticao','bloco','ordem',
              'configuracao_id','payload_sha256','preparacao_sha256','requisicao_sha256')


def exigir(ok, msg):
    if not ok: raise ValueError(msg)


def base_preparada():
    raw = (BASE / 'plano.json').read_bytes()
    exigir(api.sha(raw) == HASH_BASE, 'plano preparado original alterado')
    plan = api.montagem._json(raw)
    manifest = api.base.ler(BASE / 'manifesto-bloco.json')['arquivos']
    exigir({p.relative_to(BASE).as_posix() for p in BASE.rglob('*') if p.is_file()}
           == {e['arquivo'] for e in manifest} | {'manifesto-bloco.json'}, 'arquivo extra/ausente na preparacao original')
    for e in manifest:
        exigir(api.sha(api.base.relativo(BASE,e['arquivo']).read_bytes()) == e['sha256'], 'hash original divergente')
    for name, digest in plan['fontes_sha256'].items():
        candidates = (ROOT / name, ARQUIVADAS / name)
        exigir(any(p.is_file() and api.sha(p.read_bytes()) == digest for p in candidates),
               'fonte original sem versao preservada: ' + name)
    return plan


def validar_plano(plan):
    original = base_preparada()
    exigir(plan.get('integracao') == VERSAO and plan.get('etapa') == ETAPA
           and plan.get('envio_autorizado') is False and plan.get('revisao_humana') == 'pendente', 'plano de outra etapa/autorizacao')
    exigir(plan.get('plano_base_sha256') == HASH_BASE and plan.get('bloco_exploratorio') == original['versao'], 'bloco/base divergente')
    exigir(plan['configuracoes'] == original['configuracoes'] and plan['referencia_sha256'] == original['referencia_sha256']
           and plan['referencia_versao'] == '0.3' and plan['catalogo_versao'] == '0.3', 'configuracao/referencia alterada')
    exigir(plan.get('orcamento_novo_declarado_usd') is None, 'orcamento historico nao e autorizacao')
    rows = plan['observacoes']
    exigir(len(rows) == len({r['observacao_id'] for r in rows}) == 16, 'preservar 16 identidades')
    for r, old in zip(rows,original['observacoes']):
        exigir(all(r.get(k) == old[k] for k in IDENTIDADE), 'identidade/nota/ordem/payload alterado')
        exigir(r.get('bloco_exploratorio') == original['versao']
               and r['status'] == 'PLANEJADA_NAO_EXECUTADA' and r['conformidade_protocolo'] == 'pendente'
               and r['origem'] == 'real' and r['fase'] == 'exploratoria', 'estado/bloco divergente')
    return original


def preparar(saida):
    out = api.base.protegida(saida,'captura')
    exigir(not out.exists(), 'saida existente; usar destino novo')
    original = base_preparada()
    out.mkdir(parents=True)
    # Snapshots literais necessarios aos caminhos relativos e hashes do motor.
    paths = set()
    for r in original['observacoes']:
        p = api.base.relativo(BASE,r['preparacao'])
        prep = api.base.conferir_preparacao(p)
        for name in ['preparacao.json'] + [e['arquivo'] for e in prep['arquivos']]:
            paths.add((p.parent / name).relative_to(BASE).as_posix())
        paths.add(r['requisicao'])
    for name in sorted(paths): api.salvar(out / name,api.base.relativo(BASE,name).read_bytes())
    api.salvar(out / 'ordem.json',(BASE / 'ordem.json').read_bytes())
    api.salvar(out / 'plano-base-original.json',(BASE / 'plano.json').read_bytes())
    plan = copy.deepcopy(original)
    plan.update(versao=VERSAO,integracao=VERSAO,etapa=ETAPA,plano_base_sha256=HASH_BASE,
                bloco_exploratorio=original['versao'],envio_autorizado=False,revisao_humana='pendente',
                fontes_integracao_sha256={n:api.sha((ROOT / n).read_bytes()) for n in FONTES})
    for r in plan['observacoes']:r['bloco_exploratorio'] = original['versao']
    api.salvar_json(out / 'plano.json',plan)
    api.salvar_json(out / 'autorizacao-modelo.json',{
        'versao':'autorizacao-envio-notas-v1','plano_sha256':api.sha((out / 'plano.json').read_bytes()),
        'responsavel':None,'data':None,'revisao_par_pacotes_ordem':False,'autoriza_envio_real':False,
        'orcamento_usd':None,'justificativa':None,
        'limite':'USD 2 nas configuracoes e historico; orcamento declarado nao e teto automatico'})
    files=[{'arquivo':p.relative_to(out).as_posix(),'sha256':api.sha(p.read_bytes())}
           for p in sorted(out.rglob('*')) if p.is_file()]
    api.salvar_json(out / 'manifesto-integracao.json',{'integracao':VERSAO,'arquivos':files})
    conferir(out / 'plano.json')
    return out / 'plano.json'


def conferir(path):
    path = api.montagem.sem_links(path)
    out = path.parent
    plan = api.base.ler(path)
    original = validar_plano(plan)
    exigir(plan['fontes_integracao_sha256'] == {n:api.sha((ROOT / n).read_bytes()) for n in FONTES}, 'fontes da integracao mudaram')
    inventory = api.base.ler(out / 'manifesto-integracao.json')['arquivos']
    names=[e['arquivo'] for e in inventory]
    exigir(len(names)==len(set(names)) and {p.relative_to(out).as_posix() for p in out.rglob('*') if p.is_file()}
           == set(names)|{'manifesto-integracao.json'}, 'arquivos extras/ausentes no plano integrado')
    for e in inventory:exigir(api.sha(api.base.relativo(out,e['arquivo']).read_bytes())==e['sha256'], 'hash da integracao divergente')
    exigir((out/'ordem.json').read_bytes()==(BASE/'ordem.json').read_bytes()
           and (out/'plano-base-original.json').read_bytes()==(BASE/'plano.json').read_bytes(), 'ordem/base nao literal')
    for r,old in zip(plan['observacoes'],original['observacoes']):
        p=api.base.relativo(out,r['preparacao']);source=api.base.relativo(BASE,old['preparacao'])
        prep=api.base.conferir_preparacao(p)
        exigir(p.read_bytes()==source.read_bytes() and api.sha(p.read_bytes())==r['preparacao_sha256'], 'preparacao alterada')
        for e in prep['arquivos']:
            exigir(api.base.relativo(p.parent,e['arquivo']).read_bytes()==api.base.relativo(source.parent,e['arquivo']).read_bytes(), 'snapshot alterado')
        exigir(all(prep[k]==r[k] for k in ('nota_id','bloco_exploratorio','configuracao_id','payload_sha256')), 'preparacao de outra nota')
        payload=(p.parent/'payload.txt').read_bytes()
        req=api.base.relativo(out,r['requisicao']).read_bytes()
        exigir(req==api.base.relativo(BASE,old['requisicao']).read_bytes()
               ==api.requisicao(payload,plan['configuracoes'][r['configuracao_id']]), 'requisicao alterada')
    return plan


def validar_autorizacao(plano, arquivo):
    conferir(plano)
    exigir(arquivo is not None, 'envio bloqueado: revisao e autorizacao especificas pendentes')
    data=api.base.ler(arquivo)
    exigir(data.get('versao')=='autorizacao-envio-notas-v1'
           and data.get('plano_sha256')==api.sha(Path(plano).read_bytes())
           and data.get('revisao_par_pacotes_ordem') is True and data.get('autoriza_envio_real') is True,
           'envio bloqueado: autorizacao/revisao ausente ou de outro plano')
    exigir(all(isinstance(data.get(k),str) and data[k].strip() for k in ('responsavel','data','justificativa')), 'autorizacao exige responsavel/data/justificativa')
    try:
        moment=datetime.fromisoformat(data['data'])
        budget=Decimal(str(data['orcamento_usd']))
        exigir(moment.tzinfo is not None and moment.utcoffset() is not None
               and budget.is_finite() and budget>0, 'data com fuso e orcamento proprio positivo requeridos')
    except (ValueError,TypeError,InvalidOperation,KeyError) as error:
        raise ValueError('autorizacao com data/orcamento invalido') from error
    return data


def iniciar(plano,lote,limite,enviar_real=False,continuar=False,autorizacao=None):
    exigir(enviar_real, 'envio bloqueado: --enviar-real obrigatorio; nenhuma chave foi lida')
    return api.capturar(plano,lote,limite,continuar,True,conferidor=conferir,autorizacao=autorizacao)


def controle(plano,lote,limite=16,continuar=False,controle_http=None):
    return api.capturar(plano,lote,limite,continuar,False,conferidor=conferir,controle_http=controle_http)


def conferir_lote(lote):
    root=api.montagem.sem_links(lote)
    header=api.base.ler(root/'lote.json');raw=(root/'plano-original.json').read_bytes();plan=api.montagem._json(raw)
    validar_plano(plan)
    exigir(header.get('etapa')==ETAPA and header.get('integracao')==VERSAO
           and header.get('bloco_exploratorio')==plan['bloco_exploratorio']
           and header.get('referencia_sha256')==plan['referencia_sha256']
           and header.get('plano_sha256')==api.sha(raw), 'lote de outro plano/bloco')
    exigir((header['origem'],header['fase']) in (('real','exploratoria'),('sintetica','verificacao_sintetica')), 'origem/fase indevida')
    exigir(header.get('coletor_sha256')==plan['fontes_integracao_sha256']['coletor_api.py'], 'fonte do coletor nao corresponde ao plano')
    if header['origem']=='real':
        rawauth=(root/'autorizacao-envio-original.json').read_bytes()
        auth=api.montagem._json(rawauth)
        exigir(api.sha(rawauth)==header.get('autorizacao_sha256') and auth.get('plano_sha256')==header['plano_sha256']
               and auth.get('autoriza_envio_real') is True and auth.get('revisao_par_pacotes_ordem') is True
               and auth.get('orcamento_usd')==header.get('orcamento_novo_declarado_usd'), 'autorizacao original divergente')
    expected={r['observacao_id'] for r in plan['observacoes']}
    exigir({p.name for p in root.iterdir() if p.is_dir()}<=expected, 'captura extra ou de outra coorte')
    exigir(not (root/'coletor.lock').exists(), 'lote em captura ou com lock pendente')
    for r in plan['observacoes']:
        p=root/r['observacao_id']/'T01'
        if not p.exists():continue
        exigir({q.name for q in p.parent.iterdir()}=={'T01'}, 'tentativa extra nao prevista')
        t=api.base.conferir_fechamento(p)
        exigir(all(t.get(k)==r[k] for k in ('observacao_id','configuracao_id','mudanca','condicao','payload_sha256',
                                           'preparacao_sha256','nota_id','bloco_exploratorio','modelo','bloco','ordem'))
               and t.get('plano_sha256')==header['plano_sha256'] and t['origem']==header['origem']
               and t['fase']==header['fase'] and t.get('etapa')==ETAPA
               and t.get('integracao')==VERSAO and t.get('referencia_sha256')==plan['referencia_sha256']
               and t.get('versoes',{}).get('coletor_sha256')==header['coletor_sha256']
               and t['configuracao']==plan['configuracoes'][r['configuracao_id']], 'captura de outra nota/bloco/configuracao')
        if header['origem']=='real':exigir(t.get('autorizacao_sha256')==header['autorizacao_sha256'], 'tentativa de outra autorizacao')
        repeat='repeticao' if header['origem']=='real' else 'repeticao_sintetica'
        exigir(t[repeat]==r['repeticao'], 'repeticao divergente')
        prep=api.base.conferir_preparacao(p/'preparacao/preparacao.json')
        exigir(prep['nota_id']==r['nota_id'] and prep['bloco_exploratorio']==r['bloco_exploratorio']
               and api.sha((p/'preparacao/preparacao.json').read_bytes())==r['preparacao_sha256'], 'snapshot de outra nota')
        payload=(p/'entrada.bin').read_bytes()
        exigir(api.sha(payload)==r['payload_sha256'] and (p/'requisicao.json').read_bytes()
               ==api.requisicao(payload,t['configuracao']), 'entrada/requisicao divergente')
    return header,plan


def avaliar_lote(lote,referencia,saida):
    # So este comando abre a referencia; captura nao importa avaliador/gabarito.
    import avaliacao_ids as a
    header,plan=conferir_lote(lote)
    exigir(api.sha(Path(referencia).read_bytes())==plan['referencia_sha256'], 'referencia diferente da preparada')
    root=api.montagem.sem_links(lote);out=api.base.protegida(saida,'avaliados');out.mkdir(parents=True,exist_ok=False)
    entries=[];observations=[];code=0
    for r in plan['observacoes']:
        planned={k:r[k] for k in ('observacao_id','configuracao_id','mudanca','condicao','payload_sha256','nota_id','bloco_exploratorio','modelo')}
        planned.update(origem=header['origem'],fase=header['fase'],plano_sha256=header['plano_sha256'])
        planned['repeticao' if header['origem']=='real' else 'repeticao_sintetica']=r['repeticao']
        observations.append(planned)
        attempt=root/r['observacao_id']/'T01'
        if not attempt.exists():continue
        target=out/r['observacao_id']/'T01'
        reg,status=a.avaliar(attempt/'preparacao/preparacao.json',attempt/'tentativa.json',referencia,target,
                             origem=header['origem'],fase=header['fase'])
        exigir(reg['completo'], 'avaliacao incompleta; preservar diagnostico e interromper')
        code=max(code,status)
        entries.append({'arquivo':(target/'avaliacao.json').relative_to(out).as_posix(),'sha256':api.sha((target/'avaliacao.json').read_bytes())})
    api.salvar_json(out/'lista.json',entries);api.salvar_json(out/'observacoes.json',observations)
    _,status=a.resumir(out/'lista.json',out/'observacoes.json',out/'resumo',origem=header['origem'],fase=header['fase'])
    return max(code,status)


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__);sub=p.add_subparsers(dest='comando',required=True)
    sub.add_parser('preparar').add_argument('--saida',required=True)
    sub.add_parser('simular').add_argument('--plano',required=True)
    for name in ('controle','iniciar'):
        q=sub.add_parser(name)
        for arg in ('plano','lote'):q.add_argument('--'+arg,required=True)
        q.add_argument('--limite',type=int,required=True);q.add_argument('--continuar',action='store_true')
        if name=='iniciar':
            q.add_argument('--enviar-real',action='store_true');q.add_argument('--autorizacao')
    q=sub.add_parser('avaliar')
    for arg in ('lote','referencia','saida'):q.add_argument('--'+arg,required=True)
    args=p.parse_args(argv)
    if args.comando!='iniciar':
        def offline(event,values):
            if event in ('socket.connect','socket.getaddrinfo','socket.gethostbyname'):
                raise RuntimeError('D-47: comando offline; rede proibida')
        sys.addaudithook(offline)
    try:
        if args.comando=='preparar':print(preparar(args.saida));return 0
        if args.comando=='simular':
            plan=conferir(args.plano)
            print(json.dumps({'N':len(plan['observacoes']),'celulas':8,'primeira':plan['observacoes'][0],
                              'envio_autorizado':False,'revisao_humana':'pendente'},ensure_ascii=True,indent=2));return 0
        if args.comando=='controle':return controle(args.plano,args.lote,args.limite,args.continuar)
        if args.comando=='iniciar':return iniciar(args.plano,args.lote,args.limite,args.enviar_real,args.continuar,args.autorizacao)
        return avaliar_lote(args.lote,args.referencia,args.saida)
    except (OSError,ValueError,KeyError) as error:
        print(str(error),file=sys.stderr);return 2


if __name__=='__main__':raise SystemExit(main())
