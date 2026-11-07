"""Preparacao LF e prova de transporte Git local D36; sem LLM ou bancada.

gerar cria uma versao nova; verificar confere bytes e recompoe pelo montador;
transporte inclui os arquivos novos num Git temporario e verifica quatro checkouts.
Stage/commit sao exclusivos desse repositorio temporario, nunca do projeto.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import uuid

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
import fontes_autorizadas as f
import montagem_entradas as m

EVIDENCIA = Path(__file__).resolve().parent
ANTERIOR = Path('evidencias/spec004/preparacao-piloto-2026-11-06/artefatos')


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read(path):
    return json.loads(path.read_bytes())


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('xb') as stream:
        stream.write((json.dumps(value, ensure_ascii=True, sort_keys=True, indent=2)+'\n').encode())


def require(condition, message):
    if not condition:
        raise ValueError(message)


def gerar(out):
    require(not out.exists(), 'saida ja existe')
    out.mkdir(parents=True)
    records = f.exportar(ROOT, out/'recortes')
    for record in records:
        package = out/'recortes'/record['pacote']
        auth = out/'recortes'/record['autorizacao']
        m.preparar(package, package/'manifesto.json', out/'preparados'/record['id'], auth)
        # Igualdade textual com D35, inclusive espacos e delimitadores; so BOM/EOL.
        previous = ROOT/ANTERIOR/'preparados'/record['id']
        for name in ['payload.txt', *['documentos/'+e['arquivo'] for e in read(package/'manifesto.json')['documentos']]]:
            require((out/'preparados'/record['id']/name).read_bytes() ==
                    f.normalizar_documento((previous/name).read_bytes()), 'conteudo D35 alterado: '+record['id']+'/'+name)
    for name in ('fontes_autorizadas.py', 'montagem_entradas.py'):
        path = out/'fontes-ferramentas'/name
        path.parent.mkdir(exist_ok=True)
        path.write_bytes((ROOT/name).read_bytes())
    inventory = [{'arquivo':p.relative_to(out).as_posix(), 'sha256':sha(p.read_bytes()),
                  'tamanho_bytes':p.stat().st_size}
                 for p in sorted(out.rglob('*')) if p.is_file()]
    save(out/'inventario.json', {'politica_bytes':f.POLITICA_BYTES, 'arquivos':inventory,
        'conteudo_D35_preservado_apos_normalizacao':True,
        'limite':'fontes-originais e fontes-ferramentas sao capturas literais; documentos exportados e payloads sao LF'})
    print(json.dumps({'gerados':16,'arquivos_inventariados':len(inventory)}), flush=True)


def verificar(out, flow):
    require(not flow.exists(), 'saida de recomposicao ja existe')
    inventory = read(out/'inventario.json')['arquivos']
    expected_files = {e['arquivo'] for e in inventory} | {'inventario.json'}
    require({p.relative_to(out).as_posix() for p in out.rglob('*') if p.is_file()} == expected_files,
            'arquivos ausentes/extras no inventario')
    for entry in inventory:
        data = (out/entry['arquivo']).read_bytes()
        require(sha(data)==entry['sha256'] and len(data)==entry['tamanho_bytes'], 'inventario: '+entry['arquivo'])
    index = read(out/'recortes/indice.json')
    records = index['pacotes']
    require({r['id'] for r in records} == {c+'-'+k for c in m.MUDANCAS for k in m.CONDICOES}
            and len(records)==16, 'matriz incompleta/duplicada')
    sources = out/'recortes/fontes-originais'
    require([e['arquivo'] for e in index['fontes_originais']]==list(f.FONTES), 'fontes inesperadas')
    for entry in index['fontes_originais']:
        data = (sources/entry['arquivo']).read_bytes()
        require(sha(data)==entry['sha256'] and len(data)==entry['tamanho_bytes'], 'fonte original divergente')
    results = []
    global_common = {}
    note_hashes = set()
    doc_count = 0
    for record in records:
        package = out/'recortes'/record['pacote']
        prepared = out/'preparados'/record['id']
        authpath = out/'recortes'/record['autorizacao']
        manifest_raw = (package/'manifesto.json').read_bytes()
        auth_raw = authpath.read_bytes()
        manifest, auth, prep = json.loads(manifest_raw), json.loads(auth_raw), read(prepared/'preparacao.json')
        require((prepared/'manifesto-original.json').read_bytes()==manifest_raw and
                (prepared/'autorizacao-original.json').read_bytes()==auth_raw, 'copias de manifesto/autorizacao')
        require(auth['manifesto_sha256']==sha(manifest_raw)==prep['manifesto_sha256'], 'vinculo manifesto')
        require(prep['autorizacao_sha256']==sha(auth_raw), 'vinculo autorizacao')
        require(auth['politica_bytes']==manifest['politica_bytes']==prep['politica_bytes']==f.POLITICA_BYTES,
                'politica divergente')
        require(prep['documentos']==manifest['documentos'], 'documentos da preparacao')
        for name in ('pacote_id','versao_pacote','configuracao_id','mudanca','condicao','status_notas'):
            require(prep[name]==manifest[name], 'identidade: '+name)
        require(prep['completo'] is True and prep['status']=='PREPARADO_LOCAL_NAO_ENVIADO' and
                prep['liberado_para_pesquisa'] is False, 'estado de preparacao')
        require(prep['montador_sha256']==sha((out/'fontes-ferramentas/montagem_entradas.py').read_bytes()),
                'hash do montador produtor')
        names = list(m.NOMES)
        notes = manifest['condicao'] in ('D1','E1')
        if notes:
            names.insert(5,'notas.md')
        require([e['arquivo'] for e in manifest['documentos']]==names, 'lista/ordem dos documentos')
        require({p.name for p in package.iterdir()}==set(names)|{'manifesto.json'}, 'extras no pacote')
        require({p.name for p in (prepared/'documentos').iterdir()}==set(names), 'extras nos documentos preparados')
        require(auth['documentos']==[{'arquivo':e['arquivo'],'sha256':e['sha256']} for e in manifest['documentos']],
                'documentos autorizados')
        originals, provenance = f.reunir_fontes(sources, manifest['mudanca'], manifest['condicao'])
        require(auth['fontes']==provenance==index['fontes_originais'], 'proveniencia das fontes')
        payload_parts = []
        for entry in manifest['documentos']:
            name = entry['arquivo']
            data = (package/name).read_bytes()
            raw = originals[name]
            require((prepared/'documentos'/name).read_bytes()==data, 'documento copiado')
            require(sha(data)==entry['sha256'] and len(data)==entry['tamanho_bytes'], 'hash/tamanho documento')
            require(entry['recorte_antes_normalizacao']=={'sha256':sha(raw),'tamanho_bytes':len(raw)},
                    'recorte anterior a normalizacao')
            require(data==f.normalizar_documento(raw) and not data.startswith(b'\xef\xbb\xbf') and b'\r' not in data,
                    'transformacao ou UTF-8/LF divergente')
            payload_parts.append(f'<<<inicio:{entry["papel"]}>>>\n'.encode()+data+f'\n<<<fim:{entry["papel"]}>>>\n'.encode())
            if name not in ('mudanca.md','pedido.txt','notas.md'):
                global_common.setdefault(name,set()).add(sha(data))
            if name=='notas.md':
                note_hashes.add(sha(data))
            doc_count += 1
        payload = (prepared/'payload.txt').read_bytes()
        require(payload==b''.join(payload_parts), 'composicao payload')
        require(sha(payload)==prep['payload_sha256'] and len(payload)==prep['payload_tamanho'], 'hash/tamanho payload')
        delivery = read(prepared/'entrega-textual.json')
        require(delivery['payload_sha256']==sha(payload) and delivery['envio_realizado'] is False, 'entrega textual')
        require((b'<<<inicio:notas>>>' in payload)==notes, 'presenca/ausencia notas')
        require(all(token not in payload for token in (b'"expected"',b'"changed"',b'G_RF',b'D-34',
                b'def autorizar',b'recuperacao-sessoes',b'TP/FP/FN')), 'conteudo nao permitido')
        for entry in prep['arquivos']:
            require(sha((prepared/entry['arquivo']).read_bytes())==entry['sha256'], 'arquivo vinculado na preparacao')
        # Exercita o fluxo existente com os arquivos efetivamente recuperados do checkout.
        recomposed = m.preparar(package, package/'manifesto.json', flow/record['id'], authpath)
        require((flow/record['id']/'payload.txt').read_bytes()==payload and
                recomposed['payload_sha256']==prep['payload_sha256'], 'fluxo offline divergiu')
        results.append(prep)
    require(m.conferir_condicoes(results), 'condicoes divergentes')
    require(len(note_hashes)==1 and all(len(v)==1 for v in global_common.values()), 'equivalencia entre mudancas')
    return {'status':'CONFERIDO','arquivos_hash_tamanho':len(inventory), 'arquivo_inventario_adicional':1,
        'documentos_exportados':doc_count,'copias_documentos':doc_count,'payloads':len(results),
        'fluxo_offline_pacotes':len(results),'divergencias':[],
        'fontes_originais':len(index['fontes_originais']), 'hash_inventario':sha((out/'inventario.json').read_bytes()),
        'limite_vazamento':'recortes fixos rederivados das seis fontes e negativos; sem detector semantico universal',
        'python':sys.version,'plataforma':sys.platform,'ferramentas_modelo_exercitadas':False}


def transporte(temp_base, report):
    require(not temp_base.exists(), 'diretorio temporario deve ser novo')
    require(temp_base.resolve().is_relative_to((ROOT/'saidas-locais').resolve()), 'temporario fora da saida local')
    temp_base.mkdir(parents=True)
    snapshot = temp_base/'snapshot'
    project = snapshot/'tcc-impacto-llm'
    project.mkdir(parents=True)
    relative = EVIDENCIA.relative_to(ROOT)
    shutil.copytree(EVIDENCIA, project/relative)
    for name in ('.gitattributes','fontes_autorizadas.py','montagem_entradas.py'):
        shutil.copyfile(ROOT/name, project/name)
    controls = {'captura/controle-artificial-entrada.bin':b'\xef\xbb\xbfentrada sintetica\r\nlinha\rfim\n',
                'avaliados/controle-artificial-resposta.bin':b'controle sintetico\r\n\xff\n'}
    for name,data in controls.items():
        path = project/name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    transcript = []
    env = os.environ.copy()
    env.update(GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL=os.devnull,GIT_ATTR_NOSYSTEM='1')
    def run(args, cwd, check=True):
        cp = subprocess.run(args,cwd=cwd,env=env,capture_output=True)
        transcript.append({'cwd':str(cwd),'comando':list(map(str,args)),'retorno':cp.returncode,
                           'stdout':cp.stdout.decode('utf-8',errors='replace'),
                           'stderr':cp.stderr.decode('utf-8',errors='replace')})
        if check and cp.returncode:
            save(report/'comandos-falha.json',transcript)
            raise ValueError('comando falhou: '+str(args))
        return cp.stdout
    run(['git','init','--template='],snapshot)
    for key,value in [('core.autocrlf','true'),('user.name','Verificacao offline D36'),
                      ('user.email','verificacao@local.invalid'),('commit.gpgsign','false')]:
        run(['git','config','--local',key,value],snapshot)
    # Assercao antes das unicas mutacoes Git: este .git e o temporario criado acima.
    require((snapshot/'.git').is_dir() and snapshot.resolve().is_relative_to(temp_base.resolve()),
            'repositorio temporario invalido')
    run(['git','add','--all','--','tcc-impacto-llm'],snapshot)
    run(['git','commit','-m','Snapshot artificial D36 para verificar transporte de bytes'],snapshot)
    commit = run(['git','rev-parse','HEAD'],snapshot).decode().strip()
    require(not run(['git','status','--porcelain'],snapshot).strip(),'snapshot sujo')
    results = []
    for label,autocrlf,eol in [('false-lf','false','lf'),('true-crlf','true','crlf'),
                              ('input-lf','input','lf'),('false-crlf','false','crlf')]:
        checkout = temp_base/label
        run(['git','clone','--no-hardlinks','--no-checkout',str(snapshot),str(checkout)],temp_base)
        for key,value in [('core.autocrlf',autocrlf),('core.eol',eol)]:
            run(['git','config','--local',key,value],checkout)
        run(['git','checkout','--detach',commit],checkout)
        require(not run(['git','status','--porcelain'],checkout).strip(),'checkout inicial sujo')
        dest = checkout/'tcc-impacto-llm'
        script = dest/relative/Path(__file__).name
        result_path = checkout/'resultado.json'
        run([sys.executable,'-B',str(script),'verificar','--artefatos',str(dest/relative/'artefatos'),
             '--recompor-em',str(checkout/'fluxo-offline'),'--relatorio',str(result_path)],dest)
        result = read(result_path)
        for name,data in controls.items():
            require((dest/name).read_bytes()==data,'captura bruta modificada pelo Git')
        attrs = run(['git','check-attr','text','eol','filter','ident','--',
                     'tcc-impacto-llm/'+(relative/'artefatos/preparados/MC-01-D0/payload.txt').as_posix(),
                     'tcc-impacto-llm/captura/controle-artificial-entrada.bin',
                     'tcc-impacto-llm/avaliados/controle-artificial-resposta.bin',
                     'tcc-impacto-llm/evidencias/spec004/preparacao-piloto-2026-11-06/artefatos/preparados/MC-01-D0/payload.txt'],checkout)
        run(['git','ls-files','--eol','--','tcc-impacto-llm/'+(relative/'artefatos').as_posix()],checkout)
        result.update(ambiente=label,core_autocrlf=autocrlf,core_eol=eol,commit_snapshot=commit,
                      checkout_limpo_antes_verificacao=True,controles_brutos_artificiais_preservados=2,
                      atributos=attrs.decode())
        save(report/'checkouts'/(label+'.json'),result)
        results.append(result)
        print(json.dumps({'checkout':label,'arquivos':result['arquivos_hash_tamanho'],'payloads':16,'divergencias':0}),flush=True)
    save(report/'comandos-transporte.json',transcript)
    save(report/'transporte.json',{'commit_snapshot_temporario':commit,'repositorio_temporario':str(snapshot),
        'configuracao_global_e_sistema_inalterada':True,'commit_no_projeto':False,'chamadas_externas':0,
        'inventario_snapshot_sha256':results[0]['hash_inventario'],
        'checkouts':[{'ambiente':r['ambiente'],'arquivos_hash_tamanho':r['arquivos_hash_tamanho'],
                     'payloads':r['payloads'],'divergencias':r['divergencias']} for r in results],
        'nao_verificados':['Linux','macOS','transporte remoto GitHub; prova local de blobs/checkouts Git'],
        'controles_brutos':'dois arquivos artificiais em captura/avaliados; nenhuma resposta de modelo'})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='comando',required=True)
    generate = commands.add_parser('gerar')
    generate.add_argument('--saida',type=Path,required=True)
    verify = commands.add_parser('verificar')
    for name in ('artefatos','recompor-em','relatorio'):
        verify.add_argument('--'+name,type=Path,required=True)
    transport = commands.add_parser('transporte')
    transport.add_argument('--temporario',type=Path,required=True)
    transport.add_argument('--relatorios',type=Path,default=EVIDENCIA)
    args = parser.parse_args()
    if args.comando=='gerar':
        gerar(args.saida.resolve())
    elif args.comando=='verificar':
        result = verificar(args.artefatos.resolve(),args.recompor_em.resolve())
        save(args.relatorio.resolve(),result)
        print(json.dumps(result))
    else:
        transporte(args.temporario.resolve(),args.relatorios.resolve())


if __name__=='__main__':
    main()
