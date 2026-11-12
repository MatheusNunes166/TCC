"""Receita D-50 deste lote: conferencia e descricao offline, sem coleta.

Avaliacao e ficha sao produzidas separadamente pelas CLIs existentes.
Nao altera fontes, capturas, conformidade ou regras de pontuacao.
"""
from collections import Counter, defaultdict
from datetime import datetime
from fractions import Fraction
import csv
import io
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
EVID = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
sys.dont_write_bytecode = True


def offline(event, args):
    if event in ('socket.connect', 'socket.getaddrinfo', 'socket.gethostbyname'):
        raise RuntimeError('D-50: rede/DNS proibidos')


sys.addaudithook(offline)
import notas_exploratorias as n
import avaliacao_ids as a

api = n.api
LOTE = ROOT / 'captura/notas-mc04-real-001'
PLANO = ROOT / 'captura/notas-mc04-0.3-002/plano.json'
REF = ROOT / 'materiais/modelos/referencia_candidata_0.3_NAO_ENVIAR_AO_LLM.json'
AVAL = ROOT / 'avaliados/notas-mc04-real-001'
DIMS = ('requisitos', 'testes')


def exigir(ok, msg):
    if not ok: raise ValueError(msg)


def salvar(path, data):
    api.salvar_json(path, data)


def conferir():
    exigir(not AVAL.exists(), 'avaliacao existente: conferir sem sobrescrever')
    inventory = {}
    for folder in ('captura', 'avaliados', 'materiais', 'variantes', 'evidencias'):
        for p in sorted((ROOT / folder).rglob('*')):
            if p.is_file() and EVID not in p.parents and '__pycache__' not in p.parts:
                api.montagem.sem_links(p)
                inventory[p.relative_to(ROOT).as_posix()] = api.sha(p.read_bytes())
    for name in n.FONTES + ('preparar_bloco_notas.py', 'fontes_autorizadas.py'):
        inventory[name] = api.sha((ROOT / name).read_bytes())
    salvar(EVID / 'estado-inicial.json', {
        'head': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT).decode().strip(),
        'status': subprocess.check_output(['git', 'status', '--short'], cwd=ROOT).decode(),
        'sha256_originais': inventory, 'rede': False})
    plan = n.conferir(PLANO)
    header, copied = n.conferir_lote(LOTE)
    exigir(copied == plan and (LOTE/'plano-original.json').read_bytes() == PLANO.read_bytes(), 'plano copiado divergente')
    auth = n.validar_autorizacao(PLANO, LOTE/'autorizacao-envio-original.json')
    exigir((LOTE/'autorizacao-envio-original.json').read_bytes() == (ROOT/'captura/autorizacao-notas-mc04-001.json').read_bytes(), 'autorizacao divergente')
    exigir(auth['orcamento_usd'] is None and header['orcamento_novo_declarado_usd'] is None, 'orcamento alterado')
    exigir(header['coletor_sha256'] == api.sha((ROOT/'coletor_api.py').read_bytes()), 'coletor divergente')
    exigir(api.sha(REF.read_bytes()) == plan['referencia_sha256'] == header['referencia_sha256'], 'referencia divergente')
    a.referencia_da_mudanca(a.json_estrito(REF.read_bytes()), 'MC-04-v2')
    rows = plan['observacoes'];ids = {r['observacao_id'] for r in rows}
    exigir(len(rows) == len(ids) == 16, '16 identidades requeridas')
    exigir({p.name for p in LOTE.iterdir() if p.is_dir()} == ids, 'observacoes extras/ausentes')
    exigir({p.name for p in LOTE.iterdir() if p.is_file()} == {'lote.json','plano-original.json','autorizacao-envio-original.json'}, 'arquivos extras/lock no lote')
    counts = Counter((r['modelo'],r['condicao'],r['nota_id']) for r in rows)
    exigir(len(counts) == 8 and set(counts.values()) == {2}, 'oito celulas N=2 requeridas')
    records = [];remote = defaultdict(set);closing_links = 0;last_end = None
    for row in rows:
        root = LOTE/row['observacao_id']/'T01'
        t = api.base.conferir_fechamento(root)
        links = api.base.ler(root/'fechamento.json')['arquivos']
        exigir(len(links) == len({x['arquivo'] for x in links}), 'fechamento duplicado')
        closing_links += len(links)
        exigir(t['repeticao'] == row['repeticao'] and t['tentativa_anterior'] is None, 'repeticao/tentativa divergente')
        config = plan['configuracoes'][row['configuracao_id']]
        exigir(config['esforco_solicitado'] == 'medium' and config['max_output_tokens'] == 4096, 'configuracao alterada')
        body = (root/'requisicao.json').read_bytes();payload = (root/'entrada.bin').read_bytes()
        exigir(body == api.base.relativo(PLANO.parent,row['requisicao']).read_bytes(), 'corpo difere do planejado')
        exigir(payload == (root/'preparacao/payload.txt').read_bytes(), 'input difere do preparado')
        http = api.base.ler(root/'http-requisicao.json')
        exigir(http['metodo'] == 'POST' and http['url'] == api.ENDPOINT
               and http['headers'] == api.headers_publicos(body)
               and http['corpo_sha256'] == api.sha(body) and http['corpo_tamanho'] == len(body), 'metadados HTTP divergentes')
        raw = (root/'resposta-http.bin').read_bytes();env = api.montagem._json(raw)
        transport = api.base.ler(root/'transporte.json')
        exigir(transport['corpo_sha256'] == api.sha(raw) and transport['corpo_tamanho'] == len(raw)
               and transport['request_id'] == t['request_id'] and transport['http_status'] == t['http_status'], 'transporte divergente')
        parsed = api.interpretar(raw,t['http_status'],config)
        exigir(parsed['texto'] == (root/'resposta.bin').read_bytes()
               and parsed['usage'] == t['usage'] and parsed['response_id'] == t['response_id']
               and parsed['modelo_reportado'] == t['modelo_reportado'] == row['modelo']
               and parsed['desvios'] == t['desvios'], 'extracao/envelope/registro divergente')
        exigir(parsed['concluida'] and t['estado_tecnico'] == 'concluida' and t['fragmento'] is False
               and t['http_status'] == 200 and transport['falha'] is None and t['falha_transporte'] is None, 'captura nao concluida/falha')
        exigir(env.get('reasoning',{}).get('effort') == 'medium' and env.get('max_output_tokens') == 4096
               and env.get('status') == 'completed', 'configuracao/completude reportada divergente')
        exigir(env.get('tools') == [] and env.get('tool_choice') == 'none'
               and env.get('previous_response_id') is None and env.get('instructions') is None, 'ferramentas/historico/instrucoes adicionais')
        exigir(t['retentativas_cliente'] == transport['retentativas_cliente'] == 0, 'retry registrado')
        inicio = api.base.ler(root/'inicio.json')
        exigir(inicio['nota_id'] == row['nota_id'] and inicio['bloco_exploratorio'] == row['bloco_exploratorio']
               and inicio['requisicao_sha256'] == api.sha(body) and inicio['credenciais_persistidas'] is False, 'inicio divergente')
        for key in ('request_id','response_id','tentativa_id'):
            exigir(isinstance(t[key],str) and t[key] and t[key] not in remote[key], 'ID duplicado/ausente')
            remote[key].add(t[key])
        start,end = map(datetime.fromisoformat,(t['instante_execucao'],t['instante_fim']))
        exigir(start.tzinfo and end.tzinfo and end >= start and (last_end is None or start >= last_end), 'ordem temporal divergente')
        last_end = end
        usage = t['usage']
        exigir(all(type(usage.get(k)) is int and usage[k] >= 0 for k in ('input_tokens','output_tokens','total_tokens'))
               and usage['input_tokens'] + usage['output_tokens'] == usage['total_tokens'], 'tokens incoerentes')
        exigir(0 <= usage['output_tokens_details']['reasoning_tokens'] <= usage['output_tokens'], 'raciocinio fora da saida')
        records.append({k:t[k] for k in ('observacao_id','modelo','nota_id','condicao','repeticao','ordem','estado_tecnico',
                       'conformidade_protocolo','desvios','instante_execucao','instante_fim','usage')})
    result = {'observacoes':len(records),'celulas':8,'N_por_celula':2,'plano_sha256':header['plano_sha256'],
        'referencia_sha256':header['referencia_sha256'],'autorizacao_sha256':header['autorizacao_sha256'],
        'conformidade':dict(Counter(t['conformidade_protocolo'] for t in records)),
        'desvios':sum(bool(t['desvios']) for t in records),'vinculos_fechamentos':closing_links,
        'IDs_unicos':{k:len(v) for k,v in remote.items()},'tentativas_por_observacao':1,'retentativas_registradas':0,
        'ordem_temporal_conforme':True,'configuracao_reportada_medium_4096':True,'modelos':dict(Counter(t['modelo'] for t in records)),
        'primeira_execucao':records[0]['instante_execucao'],'ultima_conclusao':records[-1]['instante_fim'],
        'originais_inventariados':len(inventory),'rede':False,'conformidade_humana_aprovada':False,'registros':records}
    salvar(EVID/'integridade.json',result)
    print(json.dumps({k:v for k,v in result.items() if k!='registros'},indent=2))


def relatar():
    entries = api.base.ler(AVAL/'lista.json');planned = api.base.ler(AVAL/'observacoes.json')
    ficha = api.base.ler(AVAL/'revisao-conformidade-pendente.json')
    exigir(ficha['responsavel'] is None and ficha['data'] is None
           and len(ficha['observacoes']) == 16 and all(x['decisao'] == 'pendente' and x['justificativa'] is None for x in ficha['observacoes']), 'ficha preenchida inesperadamente')
    records = []
    for e in entries:
        raw = api.base.relativo(AVAL,e['arquivo']).read_bytes()
        exigir(api.sha(raw) == e['sha256'], 'avaliacao alterada')
        r = a.json_estrito(raw)
        exigir(r['completo'] and r['politica']['sha256'] == a.POLITICA_SHA
               and r['referencia']['sha256'] == api.sha(REF.read_bytes())
               and r['conformidade_protocolo'] == 'pendente', 'avaliacao/politica/referencia/conformidade divergente')
        records.append(r)
    exigir(len(records) == len(planned) == 16 and {r['observacao_id'] for r in records} == {r['observacao_id'] for r in planned}, 'inventario divergente')
    cells = [];table = [];differences = [];pairs = [];comparisons = [];individual = []
    for model in ('gpt-6-sol','gpt-6-astra'):
        for cond in ('D1','E1'):
            by_note = {}
            for note in ('N01','N02'):
                rs = sorted([r for r in records if (r['modelo'],r['condicao'],r['nota_id']) == (model,cond,note)],key=lambda r:r['repeticao'])
                ps = [p for p in planned if (p['modelo'],p['condicao'],p['nota_id']) == (model,cond,note)]
                exigir(len(rs) == len(ps) == 2 and {r['repeticao'] for r in rs} == {1,2}, 'celula incompleta')
                group,code = a._grupo(rs,ps,False)  # Descritivo: nao passa pelo gate humano nem altera registros.
                row = {'modelo':model,'estrutura':cond,'nota_id':note,**group['contagens']}
                totals = {}
                for dim in DIMS:
                    valid = [r for r in rs if r['status_avaliacao'] == 'avaliada']
                    totals[dim] = {k:sum(r[dim][k] for r in valid) for k in ('TP','FN','FP')}
                    totals[dim].update(exatas=sum(r[dim]['metricas_propostas']['correspondencia_exata'] for r in valid),denominador=len(valid))
                    row.update({dim+'_'+k:v for k,v in totals[dim].items()})
                    row.update({dim+'_'+k:v['fracao'] if v else None for k,v in group['validas'][dim].items()})
                    row[dim+'_jaccard'] = group['jaccard'][dim]['valor']['fracao'] if group['jaccard'][dim]['valor'] else None
                    comparable = all(r['status_avaliacao'] == 'avaliada' for r in rs)
                    s,t = (set(r[dim]['S']) for r in rs) if comparable else (None,None)
                    pairs.append({'modelo':model,'estrutura':cond,'nota_id':note,'dimensao':dim,
                        'observacoes':[r['observacao_id'] for r in rs],'comparavel':comparable,
                        'apenas_R01':sorted(s-t) if comparable else None,'apenas_R02':sorted(t-s) if comparable else None})
                cells.append({'modelo':model,'estrutura':cond,'nota_id':note,'descritivo':group,'contagens_ids':totals,
                              'observacoes':[r['observacao_id'] for r in rs]})
                table.append(row);by_note[note] = rs
                for r in rs:
                    item = {k:r[k] for k in ('observacao_id','modelo','condicao','nota_id','repeticao','status_avaliacao','causa')}
                    for dim in DIMS:
                        item[dim] = r[dim]
                        if r[dim] is not None and (r[dim]['omissoes'] or r[dim]['excedentes']):
                            differences.append({'observacao_id':r['observacao_id'],'dimensao':dim,**r[dim]})
                    individual.append(item)
            for x,y in zip(by_note['N01'],by_note['N02']):
                for dim in DIMS:
                    comparable = x['status_avaliacao'] == y['status_avaliacao'] == 'avaliada'
                    s,t = (set(x[dim]['S']),set(y[dim]['S'])) if comparable else (None,None)
                    comparisons.append({'modelo':model,'estrutura':cond,'repeticao':x['repeticao'],'dimensao':dim,
                        'N01_observacao':x['observacao_id'],'N02_observacao':y['observacao_id'],'comparavel':comparable,
                        'apenas_N01':sorted(s-t) if comparable else None,'apenas_N02':sorted(t-s) if comparable else None})
    tokens = {}
    for model in ('gpt-6-sol','gpt-6-astra'):
        captures = [x for x in api.base.ler(EVID/'integridade.json')['registros'] if x['modelo'] == model]
        tokens[model] = {'observacoes':len(captures),**{k:sum(x['usage'][k] for x in captures) for k in ('input_tokens','output_tokens','total_tokens')},
                        'reasoning_tokens_incluidos_na_saida':sum(x['usage']['output_tokens_details']['reasoning_tokens'] for x in captures)}
    result = {'status':'DESCRITIVO_COM_CONFORMIDADE_PENDENTE','N':16,'celulas':cells,
        'invalidas':[r['observacao_id'] for r in records if r['status_avaliacao'] == 'resposta_formato_invalido'],
        'falhas_tecnicas':[r['observacao_id'] for r in records if r['status_avaliacao'] == 'falha_tecnica'],
        'divergencias_referencia':differences,'diferencas_entre_repeticoes':pairs,'comparacoes_N01_N02':comparisons,
        'observacoes':individual,'tokens_reportados':tokens,'politica_sha256':a.POLITICA_SHA,
        'referencia_sha256':api.sha(REF.read_bytes()),'revisao_humana_pendente':True}
    salvar(AVAL/'descritivo-pendente.json',result)
    stream = io.StringIO(newline='');writer = csv.DictWriter(stream,fieldnames=list(table[0]))
    writer.writeheader();writer.writerows(table)
    api.salvar(AVAL/'tabelas-descritivas.csv',stream.getvalue().encode('utf-8'))
    print(json.dumps({'celulas':table,'divergencias_referencia':differences,'tokens':tokens},indent=2))


def fechar():
    initial = api.base.ler(EVID/'estado-inicial.json')['sha256_originais']
    changed = [name for name,sha in initial.items() if not (ROOT/name).is_file() or api.sha((ROOT/name).read_bytes()) != sha]
    exigir(not changed,'originais alterados: '+str(changed))
    desc = api.base.ler(AVAL/'descritivo-pendente.json')
    manifest_links = 0
    for path in AVAL.rglob('manifesto.json'):
        manifest = api.base.ler(path)
        for item in manifest['arquivos'] + manifest['fontes']:
            source = Path(item['arquivo'])
            source = source if source.is_absolute() else path.parent/source
            exigir(api.sha(source.read_bytes()) == item['sha256'], 'manifesto divergente: '+str(source))
            manifest_links += 1
    import revisao_conformidade as review
    meta,regs,plans,signatures,tracked = review.contexto(LOTE,AVAL/'lista.json',AVAL/'observacoes.json')
    ficha = api.base.ler(AVAL/'revisao-conformidade-pendente.json')
    exigir(ficha['fontes'] == meta and ficha['responsavel'] is None and ficha['data'] is None, 'ficha divergente')
    exigir(ficha['observacoes'] == [{**s,'decisao':'pendente','justificativa':None} for s in signatures], 'decisao humana indevida')
    a.revalidar(tracked)
    for item in desc['observacoes']:
        for dim in DIMS:
            d = item[dim]
            if d is None:continue
            s,g = set(d['S']),set(d['G'])
            exigir(d['TP'] == len(s&g) and d['FN'] == len(g-s) and d['FP'] == len(s-g), 'contagens incoerentes')
            exigir(d['metricas_propostas']['correspondencia_exata'] == int(s == g), 'exatas incoerentes')
            if s:
                exigir(Fraction(d['metricas_propostas']['precisao']['fracao']) == Fraction(len(s&g),len(s)), 'precisao incoerente')
            exigir(Fraction(d['metricas_propostas']['revocacao']['fracao']) == Fraction(len(s&g),len(g)), 'revocacao incoerente')
            exigir(Fraction(d['metricas_propostas']['f1']['fracao']) == Fraction(2*len(s&g),len(s)+len(g)), 'F1 incoerente')
    for cell in desc['celulas']:
        exigir(cell['descritivo']['contagens']['N'] == 2,'denominador alterado')
        for dim in DIMS:
            pair = cell['descritivo']['jaccard'][dim]
            if pair['estado'] != 'calculavel':continue
            rs = [r for r in desc['observacoes'] if r['observacao_id'] in cell['observacoes']]
            s,t = (set(r[dim]['S']) for r in rs)
            exigir(Fraction(pair['valor']['fracao']) == (Fraction(len(s&t),len(s|t)) if s|t else 1), 'Jaccard incoerente')
    controlled = api.base.ler(AVAL/'resumo/resumo.json')
    exigir(controlled['completo'] is False and len(controlled['celulas']) == 8,'gate humano indevidamente liberado')
    exigir(api.base.ler(AVAL/'resumo/manifesto.json')['retorno'] == 2, 'retorno do gate divergente')
    with (AVAL/'tabelas-descritivas.csv').open(encoding='utf-8',newline='') as stream:
        rows = list(csv.DictReader(stream))
    exigir(len(rows) == len(desc['celulas']) == 8,'CSV nao preserva oito celulas')
    for row,cell in zip(rows,desc['celulas']):
        exigir(all(row[k] == cell[k] for k in ('modelo','estrutura','nota_id')), 'CSV mistura notas')
        for k,v in cell['descritivo']['contagens'].items():exigir(int(row[k]) == v,'CSV contagens divergentes')
        for dim in DIMS:
            for k,v in cell['contagens_ids'][dim].items():exigir(int(row[dim+'_'+k]) == v,'CSV contagens IDs divergentes')
            for k,v in cell['descritivo']['validas'][dim].items():
                exigir(row[dim+'_'+k] == (v['fracao'] if v else ''),'CSV metrica divergente')
    samples = [LOTE/'NOTA03-MC-04-v2-D1-N02-ASTRA-R01/T01/resposta.bin',PLANO,AVAL/'RELATORIO.md',
               AVAL/'tabelas-descritivas.csv',EVID/'conferir_relatar.py']
    for sample in samples:
        rel = sample.relative_to(ROOT).as_posix()
        raw = subprocess.check_output(['git','hash-object','--no-filters',str(sample)],cwd=ROOT)
        filtered = subprocess.check_output(['git','hash-object','--path='+rel,str(sample)],cwd=ROOT)
        exigir(raw == filtered,'filtro Git alteraria bytes: '+rel)
    preservation = {'arquivos_anteriores':len(initial),'identicos':len(initial),'alterados':changed,'rede':False}
    salvar(EVID/'preservacao.json',preservation)
    files = ['RELATORIO.md','descritivo-pendente.json','tabelas-descritivas.csv']
    salvar(AVAL/'manifesto-descritivo.json',{'status':'DESCRITIVO_COM_CONFORMIDADE_PENDENTE',
        'arquivos':[{'arquivo':f,'sha256':api.sha((AVAL/f).read_bytes())} for f in files]})
    salvar(EVID/'conferencia-final.json',{'originais_identicos':len(initial),'observacoes':16,'celulas':8,
        'avaliacoes_conferidas_por_conjuntos':len(desc['observacoes']),'formula_P_R_F1_conferida':True,
        'consistencia_conferida_por_conjuntos':True,'resumo_controlado_bloqueado':True,
        'vinculos_manifestos_avaliador_conferidos':manifest_links,'amostras_bytes_Git':len(samples),
        'ficha_16_pendentes_reconferida':True,'CSV_conferido_com_avaliacoes':True,
        'ficha_pendente_sha256':api.sha((AVAL/'revisao-conformidade-pendente.json').read_bytes()),
        'politica_preservada_sha256':a.POLITICA_SHA,'rede':False,'chamadas_executadas':0,
        'manifesto_descritivo_sha256':api.sha((AVAL/'manifesto-descritivo.json').read_bytes())})
    print(json.dumps(preservation))


if __name__ == '__main__':
    {'conferir':conferir,'relatar':relatar,'fechar':fechar}[sys.argv[1]]()
