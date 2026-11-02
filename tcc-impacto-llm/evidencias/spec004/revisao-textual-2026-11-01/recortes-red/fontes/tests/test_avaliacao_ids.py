import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from unittest.mock import patch

from suporte_spec004 import ControleCase, ESPERADOS
import avaliacao_ids as a

def raw(obj): return json.dumps(obj).encode()
def sha(data): return hashlib.sha256(data).hexdigest()

def literal(rep=1, rf=None, tests=None, status='avaliada', obs=None, attempt=None):
    """Entrada artificial do resumo; nao produzida pelo avaliador."""
    zero = rf == []
    metric={k:{'fracao':'0' if zero else '1'} for k in ('precisao','revocacao','f1')}
    x={'avaliacao_id':f'ava-{rep}', 'observacao_id':obs or f'obs-{rep}',
       'tentativa_id':attempt or f'tent-{rep}', 'tentativa_anterior':None,
       'origem':'sintetica','modelo_reportado':None,'configuracao_id':'controle-local-v1',
       'mudanca':'MC-01','condicao':'D0','repeticao_sintetica':rep,
       'payload_sha256':'payload-controle','politica':{'versao':'ids-proposta-004-v2','sha256':'p1'},
       'referencia':{'versao':'sintetica-1','sha256':'r1'},'status_avaliacao':status,
       'completo':True,'somente_ids_conhecidos':True,
       'requisitos':{'S':['RF-02'] if rf is None else rf,'metricas_propostas':copy.deepcopy(metric)},
       'testes':{'S':['T04','T12'] if tests is None else tests,'metricas_propostas':copy.deepcopy(metric)}}
    if status!='avaliada': x['requisitos']=x['testes']=None; x['somente_ids_conhecidos']=None
    return x

def planned(*regs):
    return [{k:r[k] for k in ('observacao_id','configuracao_id','mudanca','condicao','repeticao_sintetica','payload_sha256')} for r in regs]

class TestAvaliacao(ControleCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)
        self.ref=copy.deepcopy(ESPERADOS['referencia'])

    def test_S01_a_S10_oraculos_literais(self):
        for case in ESPERADOS['casos']:
            with self.subTest(familia=case['familia']):
                r=a.avaliar_resposta(raw(case['resposta']),self.ref)
                for dim,k in [('requisitos','rf'),('testes','t')]:
                    d=r[dim]
                    self.checar(case['familia'],dim+'-contagens',[d['TP'],d['FP'],d['FN']],case[k])
                    self.checar(case['familia'],dim+'-prf',[d['metricas_propostas'][x]['fracao'] for x in ('precisao','revocacao','f1')],case['prf_'+k])
                self.assertEqual(r['status_avaliacao'],'avaliada')
                if case['familia']=='S-05':
                    self.checar('S-05','posicoes-repetidas',
                      [r['requisitos']['duplicatas'][0]['repeticoes'],r['testes']['duplicatas'][0]['repeticoes']],[[1],[2]])
                if case['familia']=='S-06':
                    self.checar('S-06','desconhecidos',[r['requisitos']['desconhecidos'],r['testes']['desconhecidos']],[['RF-99'],['T99']])

    def test_S07_espacos_vazio_caixa(self):
        for key in (' RF-02','RF-02 ','','rf-02'):
            r=a.avaliar_resposta(raw({'requisitos':[key],'testes':[]}),self.ref)
            self.checar('S-07','id-'+repr(key),[r['requisitos']['TP'],r['requisitos']['FP'],r['requisitos']['FN']],[0,1,1])

    def test_S09_invalida_sem_reparo(self):
        values=[b'',b'{}',b'{"requisitos":[]}',b'{"requisitos":[],"testes":[],"extra":[]}',
          b'{"requisitos":null,"testes":[]}',b'{"requisitos":{},"testes":[]}',
          b'{"requisitos":[2],"testes":[]}',b'{"requisitos":[true],"testes":[]}',
          b'{"requisitos":[{}],"testes":[]}',b'{"requisitos":[],"testes":[],"testes":[]}',
          b'```json\n{"requisitos":[],"testes":[]}\n```',b'nao posso',
          b'{"requisitos":[],"testes":[',b'\xef\xbb\xbf{"requisitos":[],"testes":[]}',
          b'\xff',b'{"requisitos":NaN,"testes":[]}',b'{"requisitos":[],"testes":Infinity}',
          b'{"requisitos":[],"testes":[]} trailing']
        for i,value in enumerate(values):
            r=a.avaliar_resposta(value,self.ref)
            self.checar('S-09',f'invalida-{i}',[r['status_avaliacao'],r['requisitos'],r['testes']],['resposta_formato_invalido',None,None])
        escaped=b' \n{"requisitos":["RF-\\u0030\\u0032"],"testes":["T04","T12"]} \r\n'
        r=a.avaliar_resposta(escaped,self.ref)
        self.checar('S-09','escape-legitimo-espacos',r['requisitos']['S'],['RF-02'])

    def test_S12_referencia_e_alias(self):
        def empty(r):r['mudancas'][0]['tests'].clear()
        mutators=[empty,lambda r:r.pop('versao'),lambda r:r.pop('status'),
          lambda r:r['mudancas'].clear(),lambda r:r['mudancas'].append(copy.deepcopy(r['mudancas'][0])),
          lambda r:r['mudancas'][0].update(rfs=['RF-02','RF-02']),
          lambda r:r['mudancas'][0].update(tests=['T99']),lambda r:r['mudancas'][0].update(tests=2)]
        for i,change in enumerate(mutators):
            ref=copy.deepcopy(self.ref);change(ref)
            r=a.avaliar_resposta(b'{}',ref)
            self.checar('S-12',str(i),[r['status_avaliacao'],r['requisitos']],['erro_referencia',None])
        ref=copy.deepcopy(self.ref);ref['mudancas'][0].update(changed=[],preserved=[],expected={})
        r=a.avaliar_resposta(raw(ESPERADOS['casos'][0]['resposta']),ref)
        self.checar('S-12','rfs-tests-sem-expected',r['testes']['G'],['T04','T12'])
        r=a.avaliar_resposta(raw(ESPERADOS['casos'][0]['resposta']),ref,'MC-04')
        self.checar('S-12','alias-documental',r['mudanca'],'MC-04-v2')

    def entrada(self,content=b'{"requisitos":["RF-02"],"testes":["T04","T12"]}',technical=False,fragment=False):
        self.prepdir=self.root/'prep'; self.prepdir.mkdir()
        payload=b'entrada sintetica exata\r\n'; (self.prepdir/'payload.txt').write_bytes(payload)
        prep={'preparacao_id':'prep-1','configuracao_id':'controle-local-v1','mudanca':'MC-01','condicao':'D0',
          'status':'PREPARADO_LOCAL_NAO_ENVIADO','completo':True,'liberado_para_pesquisa':False,
          'payload_sha256':sha(payload),'arquivos':[{'arquivo':'payload.txt','sha256':sha(payload)}]}
        self.prep=self.prepdir/'preparacao.json';self.prep.write_bytes(raw(prep))
        attempt={'observacao_id':'obs-1','tentativa_id':'tent-1','tentativa_anterior':None,
          'configuracao_id':'controle-local-v1','mudanca':'MC-01','condicao':'D0','repeticao_sintetica':1,
          'origem':'sintetica','modelo_reportado':None,'preparacao_id':'prep-1',
          'preparacao_sha256':sha(self.prep.read_bytes()),'payload_sha256':sha(payload),
          'estado_tecnico':'falha_tecnica' if technical else 'concluida','causa':'controle transporte' if technical else None,
          'fragmento':fragment,'resposta_arquivo':'resposta.bin' if content is not None else None,
          'resposta_sha256':sha(content) if content is not None else None,'resposta_tamanho':len(content) if content is not None else None}
        if content is not None:(self.root/'resposta.bin').write_bytes(content)
        self.attempt=self.root/'tentativa.json';self.attempt.write_bytes(raw(attempt))
        self.refpath=self.root/'referencia.json'; self.refpath.write_bytes(raw(self.ref))

    def evaluate(self,out='out'):
        return a.avaliar(self.prep,self.attempt,self.refpath,self.root/out)

    def test_S11_ausente_fragmento_original(self):
        for i,(content,frag) in enumerate([(None,False),(b'{"requisitos":',True),(b'{"requisitos":[],"testes":[]}',True)]):
            with self.subTest(caso=i):
                folder=self.root/f'case{i}';folder.mkdir(); oldroot=self.root;self.root=folder
                self.entrada(content,True,frag); r,code=self.evaluate()
                self.checar('S-11',str(i),[code,r['status_avaliacao'],r['requisitos']],[1,'falha_tecnica',None])
                self.assertEqual((folder/'out/resposta-original.bin').exists(),content is not None)
                if content is not None:self.assertEqual((folder/'out/resposta-original.bin').read_bytes(),content)
                self.root=oldroot

    def test_S13_originais_fechamento_reavaliacao(self):
        self.entrada(b'nao e JSON\r\n')
        r,code=self.evaluate(); self.assertEqual(code,1)
        self.checar('S-13','original-invalido-exato',(self.root/'out/resposta-original.bin').read_bytes().hex(),b'nao e JSON\r\n'.hex())
        r2,code=a.avaliar(self.prep,self.attempt,self.refpath,self.root/'novo',self.root/'out/avaliacao.json');self.assertEqual(code,1)
        self.checar('S-13','reavaliacao-vinculada',r2['avaliacao_anterior'],r['avaliacao_id'])
        self.assertNotEqual(r['avaliacao_id'],r2['avaliacao_id'])
        with self.assertRaises(ValueError):self.evaluate()
        original=a.revalidar
        def mutate(entries):
            (self.root/'resposta.bin').write_bytes(b'alterado'); return original(entries)
        with patch.object(a,'revalidar',side_effect=mutate):r3,code=self.evaluate('alterada')
        self.checar('S-13','rechecagem-final',[code,r3['completo'],r3['status_avaliacao']],[2,False,'erro_integridade'])

    def test_S13_falha_escrita_e_vinculo(self):
        self.entrada()
        old=a.salvar
        def failure(path,data,tracked):
            if path.name=='resposta-original.bin':path.write_bytes(b'parcial');raise OSError('controle escrita')
            return old(path,data,tracked)
        with patch.object(a,'salvar',side_effect=failure):r,code=self.evaluate()
        self.checar('S-13','escrita-parcial',[code,r['completo']],[2,False])
        attempt=json.loads(self.attempt.read_bytes());attempt['preparacao_sha256']='bad';self.attempt.write_bytes(raw(attempt))
        r,code=self.evaluate('vinculo');self.checar('S-13','vinculo-quebrado',code,2)
        for i,value in enumerate([[],None,1]):
            self.attempt.write_bytes(raw(value))
            r,code=self.evaluate('registro-tipo-'+str(i))
            self.checar('S-13','registro-nao-objeto-'+str(i),[code,r['completo']],[2,False])

    def test_S13_arquivo_removido_antes_fechamento(self):
        self.entrada();old=a.revalidar
        def remove(entries):
            (self.root/'out/resposta-original.bin').unlink()
            return old(entries)
        with patch.object(a,'revalidar',side_effect=remove):r,code=self.evaluate()
        self.checar('S-13','arquivo-removido',[code,r['completo'],r['requisitos']],[2,False,None])
        self.assertTrue((self.root/'resposta.bin').exists())

    def test_S01_S02_S09_cli(self):
        self.entrada(raw(ESPERADOS['casos'][1]['resposta']))
        root=Path(__file__).resolve().parents[1]
        cp=subprocess.run([sys.executable,'-B',str(root/'avaliacao_ids.py'),'avaliar','--preparacao',str(self.prep),
          '--tentativa',str(self.attempt),'--referencia',str(self.refpath),'--saida',str(self.root/'cli')],capture_output=True)
        self.checar('S-02','cli-incorreta-nao-falha',cp.returncode,0)
        loaded=json.loads((self.root/'cli/avaliacao.json').read_bytes())
        self.assertEqual(loaded['testes']['FN'],1)

    def test_S15_jaccard_observacoes_pares(self):
        regs=[literal(1),literal(2,tests=['T04']),literal(3,rf=[],tests=[])]
        r,code=a.resumir_registros(regs,planned(*regs))
        group=r['celulas'][0]['grupos'][0]
        for dim,val in [('requisitos','1/3'),('testes','1/6')]:
            self.checar('S-15','tres-'+dim,[group['jaccard'][dim]['valor']['fracao'],group['jaccard'][dim]['observacoes'],group['jaccard'][dim]['numero_pares']],[val,3,3])
        self.checar('S-15','pares-individuais',[p['valor']['fracao'] for p in group['jaccard']['testes']['pares']],['1/2','0','0'])
        extras=[literal(1,rf=['RF-02','RF-99'],tests=['T04','T99']),literal(2,rf=['RF-02'],tests=['T04'])]
        extras[0]['somente_ids_conhecidos']=False
        r,_=a.resumir_registros(extras,planned(*extras))
        self.checar('S-15','desconhecidos-no-Jaccard',[r['celulas'][0]['grupos'][0]['jaccard'][d]['valor']['fracao'] for d in ('requisitos','testes')],['1/2','1/2'])
        for n in (0,1):
            regs=[literal(1)][:n];r,_=a.resumir_registros(regs,planned(*regs))
            if n:
                j=r['celulas'][0]['grupos'][0]['jaccard']['testes']
                self.checar('S-15','menos-duas',[j['estado'],j['valor'],j['numero_pares']],['nao_calculavel',None,0])
        regs=[literal(1,rf=[],tests=[]),literal(2,rf=[],tests=[])]
        r,_=a.resumir_registros(regs,planned(*regs))
        self.checar('S-15','dois-vazios',r['celulas'][0]['grupos'][0]['jaccard']['testes']['valor']['fracao'],'1')

    def test_S16_resumo_A_B_ausencia(self):
        regs=[literal(1),literal(2,status='resposta_formato_invalido'),literal(3,status='falha_tecnica')]
        plans=planned(*regs)
        r,code=a.resumir_registros(regs,plans,True);g=r['celulas'][0]['grupos'][0]
        self.checar('S-16','A-contagens',g['contagens'],{k:ESPERADOS['resumo_A'][k] for k in ['N','A','C','V','I','T','K']})
        self.checar('S-16','A-escores',[g['validas']['testes']['precisao']['fracao'],g['operacional']['testes']['precisao']['fracao'],code],['1','1/2',1])
        self.assertIsNone(regs[1]['testes'])
        failure=literal(1,status='falha_tecnica',attempt='tent-primeira')
        good=literal(1);good['tentativa_anterior']='tent-primeira'
        failure['avaliacao_id']='ava-anterior'
        r,code=a.resumir_registros([failure,good],planned(good));g=r['celulas'][0]['grupos'][0]
        self.checar('S-16','B-contagens',g['contagens'],ESPERADOS['resumo_B'])
        self.assertEqual(code,0)
        bad2=copy.deepcopy(good);bad2['status_avaliacao']='falha_tecnica';bad2['testes']=bad2['requisitos']=None
        r,code=a.resumir_registros([failure,bad2],planned(good))
        self.checar('S-16','segunda-falha',[r['celulas'][0]['grupos'][0]['contagens']['T'],code],[1,1])
        single=literal(1)
        r,code=a.resumir_registros([single],planned(single,literal(2)))
        self.checar('S-16','planejada-ausente',[r['celulas'][0]['grupos'][0]['taxas']['completude']['fracao'],code],['1/2',1])

    def test_S16_PONT01_versoes_separadas(self):
        for component in ('referencia','politica'):
            regs=[literal(1),literal(2)];regs[1][component]['sha256']='outra-versao'
            r,code=a.resumir_registros(regs,planned(*regs))
            c=r['celulas'][0]
            self.checar('S-16','PONT01-'+component,[code,c['resultado_combinado'],len(c['grupos']),c['diagnosticos']],[2,None,2,['versoes_distintas']])

    def test_S16_PONT02_duplicidades_tentativas(self):
        for case in ('mesma-repeticao','duas-concluidas','duplicada-lista','payload-retentativa'):
            one=literal(1);two=literal(2)
            if case=='mesma-repeticao':two['repeticao_sintetica']=1
            if case=='duas-concluidas':two=literal(1,attempt='tent-extra');two['avaliacao_id']='ava-extra'
            if case=='duplicada-lista':two=copy.deepcopy(one)
            if case=='payload-retentativa':
                one=literal(1,status='falha_tecnica',attempt='primeira');two=literal(1);two['tentativa_anterior']='primeira';two['payload_sha256']='outro'
                one['avaliacao_id']='ava-anterior'
            r,code=a.resumir_registros([one,two],planned(one))
            self.checar('S-16','PONT02-'+case,[code,r['celulas'][0]['grupos']],[2,[]])

    def test_S16_cli_listas_hashed(self):
        regs=[literal(1)]; items=[]
        for i,r in enumerate(regs):
            p=self.root/f'a{i}.json';p.write_bytes(raw(r));items.append({'arquivo':p.name,'sha256':sha(p.read_bytes())})
        lista=self.root/'lista.json';lista.write_bytes(raw(items))
        planos=self.root/'planejadas.json';planos.write_bytes(raw(planned(*regs)))
        root=Path(__file__).resolve().parents[1]
        cmd=[sys.executable,'-B',str(root/'avaliacao_ids.py'),'resumir','--avaliacoes',str(lista),'--observacoes',str(planos),'--saida',str(self.root/'resumo')]
        cp=subprocess.run(cmd,capture_output=True)
        self.checar('S-16','cli-resumo-local',cp.returncode,0)
        (self.root/'a0.json').write_text('{}')
        cmd[-1]=str(self.root/'resumo-integro')
        cp=subprocess.run(cmd,capture_output=True)
        self.checar('S-13','cli-lista-hash',cp.returncode,2)
