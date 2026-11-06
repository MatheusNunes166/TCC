"""Descriptive scoring of recovered literal finals. No synthetic CLI, model calls or repair."""
import sys, json, hashlib
from pathlib import Path
from datetime import datetime, timezone

ROOT=Path(__file__).resolve().parents[4]
OUT=Path(__file__).resolve().parent
TRIAL=OUT.parent
sys.path.insert(0,str(ROOT))
from avaliacao_ids import avaliar_resposta, POLITICA, POLITICA_SHA

def sha(b):return hashlib.sha256(b).hexdigest()
def save(p,v):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('x',encoding='utf-8',newline='\n') as f:
        json.dump(v,f,ensure_ascii=True,indent=2);f.write('\n')
def rawsave(p,b):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('xb') as f:f.write(b)

if __name__=='__main__':
    identified=json.loads((OUT/'identificacao.json').read_bytes())
    previous=json.loads((OUT/'inventario-anterior.json').read_bytes())
    sources=identified['fonte_sha256']
    for group in (previous['arquivos_ensaio_sha256'],previous['fontes_sha256']):
        assert all(sha((ROOT/p).read_bytes())==h for p,h in group.items())
    assert all(sha(Path(p).read_bytes())==h for p,h in sources.items())
    versions=json.loads((TRIAL/'versoes.json').read_bytes())
    refraw=(ROOT/versions['referencia']['arquivo']).read_bytes()
    assert sha(refraw)==versions['referencia']['sha256']
    assert sha((ROOT/'avaliacao_ids.py').read_bytes())==versions['avaliador']['sha256']
    rawsave(OUT/'avaliacao/referencia-privada-original.json',refraw)
    rawsave(OUT/'avaliacao/avaliador-fonte.py',(ROOT/'avaliacao_ids.py').read_bytes())
    results=[]
    for cond in ('D0','D1','E0','E1'):
        record=json.loads((OUT/cond/'registro-recuperado.json').read_bytes())
        raw=(OUT/cond/'resposta-final.txt').read_bytes()
        assert sha(raw)==record['resposta_sha256']
        assert sha((OUT/cond/'mensagem-enviada.txt').read_bytes())==record['mensagem_sha256']
        assert sha((OUT/cond/'payload-enviado.txt').read_bytes())==record['payload_enviado_sha256']
        result=avaliar_resposta(raw,json.loads(refraw),'MC-04-v2','concluida')
        output={'fase':'exploratorio','origem':'llm_exploratoria','condicao':cond,'sessao_id':record['sessao_id'],'turn_id':record['turn_id'],
          'instante_avaliacao_utc':datetime.now(timezone.utc).isoformat(),'resposta_sha256':sha(raw),'registro_sha256':sha((OUT/cond/'registro-recuperado.json').read_bytes()),
          'mensagem_sha256':record['mensagem_sha256'],'payload_enviado_sha256':record['payload_enviado_sha256'],
          'referencia':versions['referencia'],'avaliador_sha256':sha((ROOT/'avaliacao_ids.py').read_bytes()),'politica':{'versao':POLITICA,'sha256':POLITICA_SHA,'status':'CANDIDATA_REVISAO_CIENTIFICA_PENDENTE'},
          'resultado':result,'avaliacao':'descritiva do final ligado ao envio textual integral, sem atestar conformidade do protocolo',
          'regra_vinculo':'turno da mensagem com blocos completos identificado antes de consultar gabarito; nunca escolha pela pontuacao',
          'igualdade_bytes_preparado_enviado':False,'desvios_registrados':True,'resumo_controlado_D0_bloqueado':bool(record['finais_anteriores']),
          'incluido_piloto':False,'incluido_coleta_principal':False,'consistencia_entre_repeticoes_calculada':False}
        save(OUT/cond/'avaliacao-descritiva-001.json',output);results.append(output)
    raw=(OUT/'D0/preliminar/resposta-final.txt').read_bytes()
    preliminary=avaliar_resposta(raw,json.loads(refraw),'MC-04-v2','concluida')
    save(OUT/'D0/preliminar/avaliacao-descritiva-001.json',{'fase':'exploratorio','origem':'llm_exploratoria','tipo':'retorno preliminar adicional; preservado, sem substituicao pelo posterior',
      'resultado':preliminary,'resposta_sha256':sha(raw),'referencia':versions['referencia'],'avaliador_sha256':versions['avaliador']['sha256'],
      'politica':POLITICA,'imputacao':False,'incluido_piloto':False,'incluido_coleta_principal':False})
    save(OUT/'avaliacao/resumo-descritivo.json',{'fase':'exploratorio','resultados':results,'retorno_preliminar_D0':preliminary,
      'resumo_controlado_ou_agregado_produzido':False,'D0_uma_observacao_unica':'bloqueado por dois retornos e contexto anterior; sem selecao automatica',
      'comparacao_entre_condicoes':'descricao dos finais recuperados; sem inferir efeito de notas/estrutura','consistencia_calculada':False,'novas_chamadas_modelo':0})
    for group in (previous['arquivos_ensaio_sha256'],previous['fontes_sha256']):
        assert all(sha((ROOT/p).read_bytes())==h for p,h in group.items())
    assert all(sha(Path(p).read_bytes())==h for p,h in sources.items())
    save(OUT/'preservacao.json',{'anteriores_ensaio_sha256':previous['arquivos_ensaio_sha256'],'fontes_protegidas_sha256':previous['fontes_sha256'],
      'origens_sessoes_e_anexo_sha256':sources,'divergencias':[],'fontes_originais_somente_leitura':True,'registros_origem_sem_alteracao':True,
      'outras_conversas_lidas':False,'cli_sintetica_chamada':False,'novas_chamadas_modelo':0})
    print(json.dumps({'resultados':[{ 'condicao':r['condicao'],'status':r['resultado']['status_avaliacao'],
        'requisitos':{k:r['resultado']['requisitos'][k] for k in ('TP','FP','FN')},'testes':{k:r['resultado']['testes'][k] for k in ('TP','FP','FN')}} for r in results],
        'preliminar_D0':preliminary['status_avaliacao'],'D0_resumo_controlado':'bloqueado','origens_preservadas':True}))
