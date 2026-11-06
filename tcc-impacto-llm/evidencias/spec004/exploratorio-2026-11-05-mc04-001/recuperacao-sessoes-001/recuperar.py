"""One-off evidence recovery: four explicit Codex sessions, read-only sources. No model calls."""
import json, hashlib, sqlite3, re
from pathlib import Path
from datetime import datetime, timezone, timedelta

TARGETS=json.loads(r'''[{"id":"01a1aeb3-83c5-7f20-b121-c20efd4d2a6e","rollout_path":"C:\\Users\\User\\.codex\\sessions\\2026\\11\\05\\rollout-2026-11-05T23-32-42-01a1aeb3-83c5-7f20-b121-c20efd4d2a6e.jsonl","cwd":"\\\\?\\D:\\Tcc-ensaio","model":"gpt-6-astra","reasoning_effort":"medium","created_at_ms":1793932362714,"updated_at_ms":1793932675174},{"id":"01a1aeba-14c8-7121-903e-99a6d6a054ae","rollout_path":"C:\\Users\\User\\.codex\\sessions\\2026\\11\\05\\rollout-2026-11-05T23-39-53-01a1aeba-14c8-7121-903e-99a6d6a054ae.jsonl","cwd":"\\\\?\\D:\\Tcc-ensaio","model":"gpt-6-astra","reasoning_effort":"medium","created_at_ms":1793932793036,"updated_at_ms":1793932799116},{"id":"01a1aebb-667a-7623-b559-1fdaa6091f35","rollout_path":"C:\\Users\\User\\.codex\\sessions\\2026\\11\\05\\rollout-2026-11-05T23-41-19-01a1aebb-667a-7623-b559-1fdaa6091f35.jsonl","cwd":"\\\\?\\D:\\Tcc-ensaio","model":"gpt-6-astra","reasoning_effort":"medium","created_at_ms":1793932879485,"updated_at_ms":1793932885729},{"id":"01a1aebc-26c9-7702-9200-143d39f2c127","rollout_path":"C:\\Users\\User\\.codex\\sessions\\2026\\11\\05\\rollout-2026-11-05T23-42-08-01a1aebc-26c9-7702-9200-143d39f2c127.jsonl","cwd":"\\\\?\\D:\\Tcc-ensaio","model":"gpt-6-astra","reasoning_effort":"medium","created_at_ms":1793932928716,"updated_at_ms":1793932934083}]''')
ROOT=Path(__file__).resolve().parents[4]
TRIAL=Path(__file__).resolve().parent.parent
OUT=Path(__file__).resolve().parent
ATTACHMENT=Path('C:/Users/User/.codex/attachments/05541469-7056-4824-8035-e4b8c0e4d3ca/Pasted text.txt')
def sha(b):return hashlib.sha256(b).hexdigest()
def norm(s):return s.replace('\r\n','\n').replace('\r','\n')
def cwd(s):return s.removeprefix('\\\\?\\').replace('\\','/').rstrip('/').lower()
def save(p,v):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('x',encoding='utf-8',newline='\n') as f:
        json.dump(v,f,ensure_ascii=True,indent=2);f.write('\n')
def rawsave(p,b):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('xb') as f:f.write(b)
def text(event):
    parts=event['payload'].get('content',[])
    assert all(p.get('type') in ('input_text','output_text') for p in parts)
    return ''.join(p['text'] for p in parts)
def iso(epoch):return datetime.fromtimestamp(epoch,timezone.utc).isoformat()
def local(ts):return datetime.fromisoformat(ts.replace('Z','+00:00')).astimezone(timezone(timedelta(hours=-3))).isoformat()
def block_parts(s):
    matches=list(re.finditer(r'<<<inicio:([^>]+)>>>\n(.*?)\n<<<fim:\1>>>\n',s,re.S))
    assert matches and len({m[1] for m in matches})==len(matches)
    return {m[1]:m[2] for m in matches}

def main():
    assert OUT==TRIAL/'recuperacao-sessoes-001'
    assert not (OUT/'identificacao.json').exists()
    previous={p.relative_to(ROOT).as_posix():sha(p.read_bytes()) for p in TRIAL.rglob('*') if p.is_file() and not p.is_relative_to(OUT)}
    protected={p:sha((ROOT/p).read_bytes()) for p in ('materiais/04_NOTAS_E_PROMPTS.md','materiais/07_DEFINICOES_COMUNS.md','materiais/modelos/referencia_candidata_NAO_ENVIAR_AO_LLM.json','avaliacao_ids.py','fontes_autorizadas.py','montagem_entradas.py')}
    save(OUT/'inventario-anterior.json',{'arquivos_ensaio_sha256':previous,'fontes_sha256':protected})
    # Metadata selection only; no thread bodies outside the four explicit IDs are opened.
    conn=sqlite3.connect(Path('C:/Users/User/.codex/state_5.sqlite').as_uri()+'?mode=ro',uri=True)
    conn.execute('PRAGMA query_only=ON');conn.row_factory=sqlite3.Row
    ids=[t['id'] for t in TARGETS]
    query="SELECT id,rollout_path,cwd,model,reasoning_effort,created_at_ms,updated_at_ms,cli_version,source FROM threads WHERE id IN ("+','.join('?' for _ in ids)+")"
    rows=[dict(r) for r in conn.execute(query,ids)];conn.close()
    assert set(r['id'] for r in rows)==set(ids)
    assert all(cwd(r['cwd'])=='d:/tcc-ensaio' and r['model']=='gpt-6-astra' and r['reasoning_effort']=='medium' for r in rows)
    save(OUT/'indice-sessoes-filtrado.json',{'modo_sqlite':'mode=ro; query_only=ON','filtro':'quatro IDs selecionados por cwd D:/Tcc-ensaio, modelo e effort; sem leitura de outras conversas','sessoes':rows})
    prepared={c:(TRIAL/'preparados'/c/'payload.txt').read_bytes() for c in ('D0','D1','E0','E1')}
    found={};sources={};extras=[]
    for target in TARGETS:
        source=Path(target['rollout_path']);data=source.read_bytes();sources[str(source)]=sha(data)
        lines=data.splitlines(keepends=True)
        events=[(i,json.loads(line)) for i,line in enumerate(lines) if line.strip()]
        meta=next(e['payload'] for _,e in events if e['type']=='session_meta')
        assert meta['id']==target['id'] and cwd(meta['cwd'])=='d:/tcc-ensaio'
        rawsave(OUT/'origens'/(target['id']+'.jsonl'),data)
        finals=[(i,e) for i,e in events if e['type']=='response_item' and e['payload'].get('type')=='message' and e['payload'].get('role')=='assistant' and e['payload'].get('phase') in ('final','final_answer')]
        for i,e in finals:
            rawsave(OUT/'todos-os-finais'/target['id']/('linha-'+str(i+1)+'.txt'),text(e).encode('utf-8'))
            rawsave(OUT/'todos-os-finais'/target['id']/('linha-'+str(i+1)+'.jsonl'),lines[i])
        candidates=[]
        for i,e in events:
            b=e.get('payload',{})
            if e['type']!='response_item' or b.get('type')!='message' or b.get('role')!='user':continue
            s=text(e);start=s.find('<<<inicio:sistema>>>')
            if start<0:continue
            offered=s[start:]
            matches=[c for c,p in prepared.items() if norm(p.decode('utf-8')).rstrip('\n')==norm(offered).rstrip('\n')]
            if len(matches)==1:candidates.append((matches[0],i,e,s,start,offered))
        assert len(candidates)==1,('ambiguous or missing complete payload',target['id'])
        cond,i,e,s,start,offered=candidates[0]
        assert cond not in found
        ctxline,ctx=next((j,v['payload']) for j,v in reversed(events) if j<i and v['type']=='turn_context')
        turn=ctx['turn_id'];assert ctx['model']=='gpt-6-astra' and ctx['effort']=='medium'
        complete=[(j,v) for j,v in events if j>i and v['type']=='event_msg' and v['payload'].get('type')=='task_complete' and v['payload'].get('turn_id')==turn]
        assert len(complete)==1
        endline,end=complete[0]
        final=[(j,v) for j,v in finals if i<j<endline];assert len(final)==1
        fi,fe=final[0];answer=text(fe)
        assert answer==end['payload']['last_agent_message']
        parts=block_parts(offered)
        pparts=block_parts(norm(prepared[cond].decode('utf-8')))
        assert parts==pparts
        folder=OUT/cond
        rawsave(folder/'mensagem-enviada.txt',s.encode('utf-8'))
        rawsave(folder/'payload-enviado.txt',offered.encode('utf-8'))
        rawsave(folder/'resposta-final.txt',answer.encode('utf-8'))
        rawsave(folder/'mensagem-enviada.origem.jsonl',lines[i])
        rawsave(folder/'resposta-final.origem.jsonl',lines[fi])
        tool_events=[{'linha':j+1,**v} for j,v in events if v['type']=='response_item' and v['payload'].get('type') in ('custom_tool_call','custom_tool_call_output','function_call','function_call_output')]
        runtime_events=[{'linha':j+1,**v} for j,v in events if v['type']=='turn_context' or v['type']=='token_usage_record' or (v['type']=='event_msg' and v['payload'].get('type') in ('task_started','task_complete','thread_settings_applied','mcp_tool_call_end'))]
        save(folder/'eventos-metadados.json',runtime_events)
        save(folder/'eventos-ferramentas.json',tool_events)
        usage=[{'linha':j+1,'timestamp':v['timestamp'],'payload':v['payload']} for j,v in events if v['type']=='token_usage_record' and v['payload'].get('turn_id')==turn]
        prior=[(j,v) for j,v in finals if j<i]
        prelim=[]
        for j,v in prior:
            earlier=[(k,w) for k,w in events if k<j and w['type']=='response_item' and w['payload'].get('role')=='user' and 'Pasted text contains' in text(w)]
            assert cond=='D0' and len(earlier)==1
            k,w=earlier[0]
            rawsave(folder/'preliminar'/'mensagem-enviada.txt',text(w).encode('utf-8'))
            rawsave(folder/'preliminar'/'resposta-final.txt',text(v).encode('utf-8'))
            rawsave(folder/'preliminar'/'mensagem-enviada.origem.jsonl',lines[k])
            rawsave(folder/'preliminar'/'resposta-final.origem.jsonl',lines[j])
            preliminary={'entrada_linha':k+1,'resposta_linha':j+1,'timestamp_entrada':w['timestamp'],'timestamp_resposta':v['timestamp'],'entrada_tipo':'referencia a anexo, sem texto integral no corpo do pedido','resposta_arquivo':'D0/preliminar/resposta-final.txt','historia_anterior_ao_payload_completo':True}
            prelim.append(preliminary);extras.append(preliminary)
        metadata={'condicao':cond,'fase':'exploratorio','origem':'llm_exploratoria','incluido_piloto':False,'incluido_coleta_principal':False,
          'sessao_id':target['id'],'turn_id':turn,'cwd_registrado':ctx['cwd'],'modelo_registrado':ctx['model'],'effort_registrado':ctx['effort'],
          'origem_sessao_arquivo':str(source),'origem_sessao_sha256':sha(data),'origem_sessao_snapshot':'origens/'+target['id']+'.jsonl',
          'mensagem_linha':i+1,'resposta_linha':fi+1,'contexto_linha':ctxline+1,'task_complete_linha':endline+1,
          'timestamp_mensagem_utc':e['timestamp'],'timestamp_resposta_utc':fe['timestamp'],
          'timestamp_mensagem_local_UTC_menos_03':local(e['timestamp']),'timestamp_resposta_local_UTC_menos_03':local(fe['timestamp']),
          'inicio_tarefa_utc':iso(end['payload']['started_at']),'fim_tarefa_utc':iso(end['payload']['completed_at']),
          'duration_ms_registrada_tarefa':end['payload']['duration_ms'],'time_to_first_token_ms_registrada':end['payload'].get('time_to_first_token_ms'),
          'usage_registrado_turno':usage,'custo':None,'temperatura':None,'top_p':None,'seed':None,
          'representacao':'Texto decodificado dos campos text do registro, salvo UTF-8 sem acrescentar/remover caracteres; linhas JSONL originais e snapshot integral preservados. Nao e captura de bytes HTTP.',
          'mensagem_sha256':sha(s.encode()),'payload_enviado_sha256':sha(offered.encode()),'resposta_sha256':sha(answer.encode()),'resposta_bytes':len(answer.encode()),
          'payload_preparado_sha256':sha(prepared[cond]),'payload_preparado_bytes':len(prepared[cond]),'payload_enviado_bytes':len(offered.encode()),
          'igualdade_literal_preparado_enviado':offered.encode()==prepared[cond],'identificacao_por_conteudo':True,
          'regra_identificacao':'correspondencia unica das quatro entradas apos equivalencia CRLF/LF e desconsideracao de LF terminais somente para identificar; originais nunca normalizados',
          'blocos_textuais_conferem_apos_EOL':parts==pparts,'CRLF_preparado':prepared[cond].count(b'\r\n'),'CRLF_enviado':offered.count('\r\n'),
          'LF_terminais_preparado':len(prepared[cond])-len(prepared[cond].rstrip(b'\n')),'LF_terminais_enviado':len(offered)-len(offered.rstrip('\n')),
          'prefixo_ide_literal':s[:start],'prefixo_ide_bytes':len(s[:start].encode()),
          'ferramentas_invocadas_sessao':[v for v in tool_events if v['payload'].get('type') in ('custom_tool_call','function_call')],
          'ferramentas_invocadas_turno_payload':sum(i<v['linha']-1<endline for v in tool_events if v['payload'].get('type') in ('custom_tool_call','function_call')),
          'ausencia_de_ferramentas_disponiveis_comprovada':False,'acesso_a_repositorio_alheio_comprovado':False,
          'finais_anteriores':prelim,'numero_task_complete_sessao':sum(v['type']=='event_msg' and v['payload'].get('type')=='task_complete' for _,v in events),
          'conformidade_texto_apenas_sem_contexto_adicional':False,
          'resumo_controlado_D0_bloqueado':bool(prelim),'motivo_bloqueio_D0':'dois retornos concluidos e historia anterior; nao escolher silenciosamente uma resposta como unica execucao' if prelim else None}
        save(folder/'registro-recuperado.json',metadata)
        found[cond]={'registro':metadata,'partes':parts}
        assert sha(source.read_bytes())==sha(data),('source changed during read',str(source))
    assert set(found)==set(prepared)
    if ATTACHMENT.is_file():
        blob=ATTACHMENT.read_bytes();rawsave(OUT/'D0/preliminar/anexo-original.txt',blob)
        amatches=[c for c,p in prepared.items() if norm(p.decode()).rstrip('\n')==norm(blob.decode()).rstrip('\n')]
        assert amatches==['D0']
        save(OUT/'D0/preliminar/anexo-proveniencia.json',{'origem':str(ATTACHMENT),'sha256':sha(blob),'bytes':len(blob),'identificacao_conteudo':['D0'],'conteudo_lido_pelo_modelo':'nao comprovado; primeiro final declara que so recebeu caminho','copia_literal':True})
        sources[str(ATTACHMENT)]=sha(blob)
    save(OUT/'identificacao.json',{'data_recuperacao_local':'2026-11-06','metodo':'cwd+modelo+effort nos metadados; condicao identificada unicamente pelo conteudo enviado, nao ordem/titulo',
       'conversas_lidas':ids,'outras_conversas_lidas':False,'condicoes':{c:{k:v for k,v in x['registro'].items() if k not in ('ferramentas_invocadas_sessao','usage_registrado_turno')} for c,x in found.items()},
       'ordem_observada_payloads':sorted(found,key=lambda c:found[c]['registro']['timestamp_mensagem_utc']),
       'retornos_finais_texto_integral':4,'retorno_preliminar_adicional_D0':len(extras),'sem_normalizar_copias':True,'fonte_sha256':sources})
    common=set(found['D0']['partes'])-{'pedido','notas'}
    assert all(len({x['partes'][n] for x in found.values()})==1 for n in common)
    assert found['D1']['partes']['notas']==found['E1']['partes']['notas']
    assert 'notas' not in found['D0']['partes'] and 'notas' not in found['E0']['partes']
    assert found['D0']['partes']['pedido']==found['D1']['partes']['pedido']
    assert found['E0']['partes']['pedido']==found['E1']['partes']['pedido']
    save(OUT/'confronto-entradas-reais.json',{'comuns_textuais_iguais':sorted(common),'mesmas_notas_D1_E1':True,'notas_ausentes_D0_E0':True,'pedidos_pares_iguais':True,'igualdade_literal_com_preparados':False,'identificacao_segura_das_condicoes':True,'desvios':'CRLF/LF, LF terminal extra e prefixo IDE nos quatro; historia/retorno anterior e ferramentas em D0','limite':'igualdade dos blocos nao demonstra igualdade de todo contexto da plataforma ou ausencia de ferramentas'})
    # Only after identification and preservation, read the candidate for descriptive scoring.
    from avaliacao_ids import avaliar_resposta, POLITICA, POLITICA_SHA
    versions=json.loads((TRIAL/'versoes.json').read_bytes())
    refraw=(ROOT/versions['referencia']['arquivo']).read_bytes()
    assert sha(refraw)==versions['referencia']['sha256']
    assert sha((ROOT/'avaliacao_ids.py').read_bytes())==versions['avaliador']['sha256']
    rawsave(OUT/'avaliacao/referencia-privada-original.json',refraw)
    rawsave(OUT/'avaliacao/avaliador-fonte.py',(ROOT/'avaliacao_ids.py').read_bytes())
    results=[]
    for cond,item in found.items():
        raw=(OUT/cond/'resposta-final.txt').read_bytes()
        result=avaliar_resposta(raw,json.loads(refraw),'MC-04-v2','concluida')
        record=item['registro']
        output={'fase':'exploratorio','origem':'llm_exploratoria','condicao':cond,'sessao_id':record['sessao_id'],'turn_id':record['turn_id'],
          'instante_avaliacao_utc':datetime.now(timezone.utc).isoformat(),'resposta_sha256':sha(raw),'registro_sha256':sha((OUT/cond/'registro-recuperado.json').read_bytes()),
          'mensagem_sha256':record['mensagem_sha256'],'payload_enviado_sha256':record['payload_enviado_sha256'],
          'referencia':versions['referencia'],'avaliador_sha256':sha((ROOT/'avaliacao_ids.py').read_bytes()),'politica':{'versao':POLITICA,'sha256':POLITICA_SHA,'status':'CANDIDATA_REVISAO_CIENTIFICA_PENDENTE'},
          'resultado':result,'avaliacao':'descritiva do final ligado ao envio textual integral, sem atestar conformidade do protocolo',
          'regra_vinculo':'turno da mensagem que contem os blocos completos identificados, antes de consultar gabarito; nao selecao pela pontuacao',
          'igualdade_bytes_preparado_enviado':False,'desvios_registrados':True,'resumo_controlado_D0_bloqueado':bool(record['finais_anteriores']),
          'incluido_piloto':False,'incluido_coleta_principal':False,'consistencia_entre_repeticoes_calculada':False}
        save(OUT/cond/'avaliacao-descritiva-001.json',output)
        results.append(output)
    if extras:
        raw=(OUT/'D0/preliminar/resposta-final.txt').read_bytes()
        result=avaliar_resposta(raw,json.loads(refraw),'MC-04-v2','concluida')
        save(OUT/'D0/preliminar/avaliacao-descritiva-001.json',{'fase':'exploratorio','origem':'llm_exploratoria','tipo':'retorno preliminar adicional; nunca substituido pelo final posterior','resultado':result,'resposta_sha256':sha(raw),'ref_sha256':sha(refraw),'imputacao':False,'incluido_piloto':False,'incluido_coleta_principal':False})
    save(OUT/'avaliacao/resumo-descritivo.json',{'fase':'exploratorio','resultados':results,'retorno_preliminar_D0':'avaliado separadamente; formato invalido e escores nulos',
       'resumo_controlado_ou_agregado_produzido':False,'D0_uma_observacao_unica':'bloqueado por dois retornos e contexto anterior','comparacao_entre_condicoes':'somente descricao dos finais recuperados; sem inferir efeito de notas/estrutura','consistencia_calculada':False,'novas_chamadas_modelo':0})
    assert all(sha((ROOT/p).read_bytes())==h for p,h in previous.items())
    assert all(sha((ROOT/p).read_bytes())==h for p,h in protected.items())
    assert all(sha(Path(p).read_bytes())==h for p,h in sources.items())
    save(OUT/'preservacao.json',{'anteriores_ensaio_sha256':previous,'fontes_protegidas_sha256':protected,'origens_sessoes_e_anexo_sha256':sources,'divergencias':[],
      'fontes_originais_somente_leitura':True,'registros_origem_sem_alteracao':True,'outras_conversas_lidas':False,'cli_sintetica_chamada':False,'novas_chamadas_modelo':0})
    print(json.dumps({'condicoes':list(found),'respostas_texto_integral':4,'preliminar_D0':len(extras),'ordem':sorted(found,key=lambda c:found[c]['registro']['timestamp_mensagem_utc']),
      'respostas_validas_texto_integral':sum(x['resultado']['formato_contrato']=='valido' for x in results),'resumo_controlado_D0':'bloqueado','origens_preservadas':True}))

if __name__=='__main__':main()
