"""Prova local do texto autorizado; sem chamada a modelo, conta ou permissao."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT))
import fontes_autorizadas as f
import montagem_entradas as m

OUT=Path(__file__).parent/'demonstracao-textual-001'

def sha(data):return hashlib.sha256(data).hexdigest()
def dump(path,obj):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('x',encoding='utf-8') as stream:json.dump(obj,stream,ensure_ascii=True,indent=2);stream.write('\n')

def run(label,args,expected=0):
    folder=OUT/'comandos'/label;folder.mkdir(parents=True,exist_ok=False)
    command=[sys.executable,'-B',*map(str,args)]
    p=subprocess.run(command,cwd=ROOT,capture_output=True)
    (folder/'stdout.txt').write_bytes(p.stdout);(folder/'stderr.txt').write_bytes(p.stderr)
    dump(folder/'comando.json',{'comando':command,'cwd':str(ROOT),'retorno':p.returncode,'esperado':expected,
         'origem':'verificacao_local','LLM':False})
    if p.returncode!=expected:raise RuntimeError(f'{label}: {p.returncode} != {expected}')

if __name__=='__main__':
    OUT.mkdir(exist_ok=False)
    run('fontes',['fontes_autorizadas.py','--raiz',ROOT,'--saida',OUT/'editorial'])
    index=json.loads((OUT/'editorial/indice.json').read_bytes())['pacotes']
    preparations=[];proofs=[];notes=[];groups={}
    forbidden=[b'G_RF',b'G_T',b'CANDIDATO_NAO_REVISADO',b'resultados-originais.json',
               b'referencia_candidata_NAO_ENVIAR_AO_LLM.json',b'RFs candidatos',b'Testes pela pol']
    note_original=next(l for l in (ROOT/'materiais/04_NOTAS_E_PROMPTS.md').read_bytes().splitlines(keepends=True)
                       if l.startswith('> Observações do analista de testes:'.encode()))
    for record in index:
        ident=record['id'];package=OUT/'editorial'/record['pacote'];auth=OUT/'editorial'/record['autorizacao'];output=OUT/'preparados'/ident
        run('montagem-'+ident,['montagem_entradas.py','--pacote',package,'--manifesto',package/'manifesto.json',
            '--autorizacao',auth,'--saida',output])
        prep=json.loads((output/'preparacao.json').read_bytes());preparations.append(prep)
        manifest=json.loads((package/'manifesto.json').read_bytes());expected=b''
        for d in manifest['documentos']:
            blob=(package/d['arquivo']).read_bytes()
            assert (output/'documentos'/d['arquivo']).read_bytes()==blob
            expected+=f'<<<inicio:{d["papel"]}>>>\n'.encode()+blob+f'\n<<<fim:{d["papel"]}>>>\n'.encode()
        payload=(output/'payload.txt').read_bytes();delivery=json.loads((output/'entrega-textual.json').read_bytes())
        assert payload==expected and prep['payload_sha256']==sha(payload)==delivery['payload_sha256']
        assert delivery['ferramentas']==[] and delivery['anexos_ambiente']==[] and delivery['envio_realizado'] is False
        assert delivery['isolamento_por_SO_alegado'] is False
        assert not any(b in payload for b in forbidden)
        if prep['condicao'] in ('D1','E1'):
            actual=(package/'notas.md').read_bytes();assert actual==note_original;notes.append(sha(actual))
        else:assert not (package/'notas.md').exists() and b'<<<inicio:notas>>>' not in payload
        catalog=(package/'catalogo-baseline.md').read_text(encoding='utf-8')
        ids=[line.split('|')[1].strip() for line in catalog.splitlines() if line.startswith('| T')]
        assert ids==[f'T{i:02}' for i in range(1,13)]
        groups.setdefault(prep['mudanca'],[]).append(prep)
        proofs.append({'id':ident,'payload_sha256':sha(payload),'conteudo_exato_confrontado':True,
          'sentinelas_proibidas_ausentes':True,'nota_literal_preservada':prep['condicao'] in ('D1','E1'),
          'doze_testes_baseline':ids,'entrega_realizada':False})
    assert len(index)==16 and len(set(notes))==1 and m.conferir_condicoes(preparations)
    # Trace actual reads of the preparation roles, with no reference supplied to them.
    original=Path.read_bytes;reads=[]
    def spy(path):reads.append(str(path.absolute()));return original(path)
    with patch.object(Path,'read_bytes',spy):f.reunir_fontes(ROOT,'MC-01','D1')
    assert set(reads)=={str((ROOT/n).absolute()) for n in f.FONTES}
    dump(OUT/'leituras-editoriais.json',{'fontes_lidas':reads,'fontes_extras':[],
      'limite':'Edicao local le seis documentos mistos e exporta somente recortes; nao le referencia de selecao.'})
    reads=[];one=index[0];package=OUT/'editorial'/one['pacote'];auth=OUT/'editorial'/one['autorizacao']
    with patch.object(Path,'read_bytes',spy):
        m.preparar(package,package/'manifesto.json',OUT/'auditoria-montagem',auth)
    allowed=[package.absolute(),auth.absolute(),(ROOT/'montagem_entradas.py').absolute(),(OUT/'auditoria-montagem').absolute()]
    assert all(any(Path(p)==q or Path(p).is_relative_to(q) for q in allowed) for p in reads)
    dump(OUT/'leituras-montador.json',{'arquivos_lidos':reads,'referencia_lida':False,'nenhuma_fonte_extra_aberta':True})
    # Only now create a synthetic response and invoke the separated evaluator with the real candidate.
    prepfile=OUT/'preparados/MC-01-D0/preparacao.json';prep=json.loads(prepfile.read_bytes())
    response=b'{"requisitos":["RF-02"],"testes":["T04","T12"]}\r\n'
    inputdir=OUT/'entrada-avaliacao';inputdir.mkdir();(inputdir/'resposta.bin').write_bytes(response)
    attempt={'observacao_id':'controle-D29','tentativa_id':'tentativa-D29','tentativa_anterior':None,
      'origem':'sintetica','modelo_reportado':None,'configuracao_id':prep['configuracao_id'],
      'mudanca':'MC-01','condicao':'D0','repeticao_sintetica':1,'estado_tecnico':'concluida','fragmento':False,
      'preparacao_id':prep['preparacao_id'],'preparacao_sha256':sha(prepfile.read_bytes()),'payload_sha256':prep['payload_sha256'],
      'resposta_arquivo':'resposta.bin','resposta_sha256':sha(response),'resposta_tamanho':len(response)}
    dump(inputdir/'tentativa.json',attempt)
    run('avaliacao-separada',['avaliacao_ids.py','avaliar','--preparacao',prepfile,'--tentativa',inputdir/'tentativa.json',
      '--referencia',ROOT/'materiais/modelos/referencia_candidata_NAO_ENVIAR_AO_LLM.json','--saida',OUT/'avaliacao'])
    result=json.loads((OUT/'avaliacao/avaliacao.json').read_bytes())
    assert [result['requisitos'][k] for k in ('TP','FP','FN')]==[1,0,0]
    assert [result['testes'][k] for k in ('TP','FP','FN')]==[2,0,0]
    assert (OUT/'avaliacao/resposta-original.bin').read_bytes()==response
    assert (OUT/'avaliacao/entrada/payload.txt').read_bytes()==(prepfile.parent/'payload.txt').read_bytes()
    dump(OUT/'confrontos.json',{'origem':'verificacao_local_com_resposta_sintetica','pacotes':proofs,
      'comuns_equivalentes':True,'mesmas_notas_oito_condicoes_com_notas':True,'conteudo_notas_nao_alterado':True,
      'referencia_apenas_avaliador':True,'referencia_status':result['referencia']['status'],
      'inspecao':'Recortes/hashes/bytes e sentinelas conferidos; nao e detector semantico universal, revisao profissional pendente.',
      'chamadas_LLM':0,'envio_realizado':False,'piloto':False,'isolamento_por_SO_alegado':False})
    print('16 pacotes autorizados, comuns/notas/bytes e avaliacao separada conferidos. Sem envio, LLM ou isolamento por SO.')
