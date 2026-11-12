"""D-47: somente HTTP ARTIFICIAL/chave ficticia em temporarios; sem chamadas."""
import contextlib
import copy
import http.client
import io
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import uuid

import avaliacao_ids as a
import notas_exploratorias as n
import revisao_conformidade as review

REF=n.ROOT/'materiais/modelos/referencia_candidata_0.3_NAO_ENVIAR_AO_LLM.json'


class TestIntegracaoNotas(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp=tempfile.TemporaryDirectory();cls.root=Path(cls.temp.name)
        with patch.object(n.api.base,'protegida',side_effect=lambda p,z:Path(p)):
            cls.path=n.preparar(cls.root/'plano')
        cls.plan=n.conferir(cls.path)

    @classmethod
    def tearDownClass(cls):cls.temp.cleanup()

    def setUp(self):
        self.case=tempfile.TemporaryDirectory(dir=self.root);self.addCleanup(self.case.cleanup)
        self.out=Path(self.case.name);self.calls=[]
        guard=patch.object(n.api.base,'protegida',side_effect=lambda p,z:Path(p));guard.start();self.addCleanup(guard.stop)
        self.redirect=contextlib.redirect_stdout(io.StringIO());self.redirect.__enter__();self.addCleanup(self.redirect.__exit__,None,None,None)
        guard=patch.object(n.api,'chave_api',side_effect=AssertionError('chave real proibida'));guard.start();self.addCleanup(guard.stop)

    def http(self,body,key,timeout):
        self.calls.append(body)
        req=n.api.montagem._json(body)
        # Resultados ARTIFICIAIS distintos: prova de separacao, nao resultado de LLM.
        coherent=n.api.montagem._json(body)['input'].find('nunca altera um conflito')<0
        answer={'requisitos':['RF-03','RF-04'] if coherent else ['RF-03'],
                'testes':['T05','T07','T08','T10','T12','T13','T14','T15'] if coherent else ['T05']}
        uid=uuid.uuid4().hex
        raw=n.api.bytes_json({'id':'ARTIFICIAL-'+uid,'model':req['model'],'status':'completed',
            'tools':[],'tool_choice':'none','output':[{'type':'message','role':'assistant','status':'completed',
            'content':[{'type':'output_text','text':n.api.bytes_json(answer).decode()}]}]})
        return 200,raw,'ARTIFICIAL-REQ-'+uid

    def capture(self,limit=16,continuar=False,http=None):
        return n.controle(self.path,self.out/'lote',limit,continuar,http or self.http)

    def evaluate(self,name='avaliacao'):
        code=n.avaliar_lote(self.out/'lote',REF,self.out/name)
        records=[a.json_estrito((self.out/name/e['arquivo']).read_bytes()) for e in n.api.base.ler(self.out/name/'lista.json')]
        return code,records,n.api.base.ler(self.out/name/'resumo/resumo.json')

    def test_preserva_original_16_ordem_textos_configuracoes(self):
        old=n.base_preparada();new=n.conferir(self.path)
        self.assertEqual(new['configuracoes'],old['configuracoes'])
        self.assertFalse(new['envio_autorizado'])
        for x,y in zip(new['observacoes'],old['observacoes']):
            self.assertEqual({k:x[k] for k in n.IDENTIDADE},{k:y[k] for k in n.IDENTIDADE})
        self.assertEqual((self.path.parent/'ordem.json').read_bytes(),(n.BASE/'ordem.json').read_bytes())

    def test_captura_retomada_16_sem_reenvio_e_8_celulas(self):
        self.assertEqual(self.capture(5),0)
        before={p:n.api.sha(p.read_bytes()) for p in (self.out/'lote').rglob('*') if p.is_file()}
        self.assertEqual(self.capture(11,True),0)
        self.assertEqual(self.capture(16,True),0)
        self.assertEqual(len(self.calls),16)
        for p,h in before.items():self.assertEqual(n.api.sha(p.read_bytes()),h)
        code,regs,summary=self.evaluate()
        self.assertEqual(code,0);self.assertEqual(len(regs),16);self.assertEqual(len(summary['celulas']),8)
        for cell in summary['celulas']:
            group=cell['grupos'][0]
            self.assertEqual((group['contagens']['N'],group['contagens']['V']),(2,2))
            self.assertEqual(group['jaccard']['requisitos']['numero_pares'],1)
            self.assertEqual(group['validas']['requisitos']['revocacao']['fracao'],'1' if cell['nota_id']=='N01' else '1/2')
            self.assertEqual(group['validas']['testes']['revocacao']['fracao'],'1' if cell['nota_id']=='N01' else '1/8')
            self.assertIn(cell['modelo'],('gpt-6-sol','gpt-6-astra'))
        for r in regs:
            capture=n.api.base.ler(self.out/'lote'/r['observacao_id']/'T01/tentativa.json')
            self.assertEqual(r['nota_id'],capture['nota_id'])
            self.assertEqual(n.api.base.ler(self.out/'lote'/r['observacao_id']/'T01/inicio.json')['nota_id'],r['nota_id'])
            self.assertEqual(r['conformidade_protocolo'],'pendente')
            self.assertEqual((self.out/'lote'/r['observacao_id']/'T01/resposta.bin').read_bytes(),
                             (self.out/'avaliacao'/r['observacao_id']/'T01/resposta-original.bin').read_bytes())

    def test_falha_parcial_preservada_sem_retry_na_retomada(self):
        def broken(body,key,timeout):
            self.calls.append(body);raise http.client.IncompleteRead(b'PREFIXO-ARTIFICIAL',40)
        self.assertEqual(self.capture(1,http=broken),2)
        with self.assertRaisesRegex(ValueError,'sem reenvio'):self.capture(16,True)
        self.assertEqual(len(self.calls),1)
        first=self.plan['observacoes'][0]
        p=self.out/'lote'/first['observacao_id']/'T01'
        self.assertEqual((p/'resposta-http-parcial.bin').read_bytes(),b'PREFIXO-ARTIFICIAL')
        self.assertEqual(n.api.base.ler(p/'tentativa.json')['nota_id'],first['nota_id'])
        code,regs,summary=self.evaluate();self.assertEqual(code,1)
        self.assertEqual(regs[0]['status_avaliacao'],'falha_tecnica')
        self.assertIsNone(regs[0]['requisitos']);self.assertIsNone(regs[0]['testes'])
        self.assertEqual(len(summary['celulas']),8)

    def test_formato_invalido_nao_reparado_e_sem_novas_tentativas(self):
        def invalid(body,key,timeout):
            status,raw,rid=self.http(body,key,timeout);env=n.api.montagem._json(raw)
            env['output'][0]['content'][0]['text']='JSON ARTIFICIAL INVALIDO'
            return status,n.api.bytes_json(env),rid
        self.assertEqual(self.capture(http=invalid),0)
        self.assertEqual(self.capture(16,True,http=invalid),0)
        self.assertEqual(len(self.calls),16)
        code,regs,summary=self.evaluate();self.assertEqual(code,1)
        self.assertTrue(all(r['status_avaliacao']=='resposta_formato_invalido' and r['requisitos'] is None for r in regs))
        self.assertTrue(all(c['grupos'][0]['contagens']['I']==2 for c in summary['celulas']))

    def test_recusa_nota_trocada_mesmo_com_fechamento_recalculado(self):
        self.capture(1);row=self.plan['observacoes'][0];p=self.out/'lote'/row['observacao_id']/'T01'
        t=n.api.base.ler(p/'tentativa.json');t['nota_id']='N01' if t['nota_id']=='N02' else 'N02'
        (p/'tentativa.json').write_bytes(n.api.bytes_json(t))
        (p/'fechamento.json').write_bytes(n.api.bytes_json({'arquivos':n.api.base.inventariar(p)}))
        with self.assertRaisesRegex(ValueError,'nota/bloco divergente'):self.capture(16,True)
        with self.assertRaises(ValueError):self.evaluate()
        self.assertEqual(len(self.calls),1)

    def test_resumo_recusa_coorte_antiga_nota_ausente_ou_plano_misto(self):
        self.capture();_,regs,_=self.evaluate();plans=n.api.base.ler(self.out/'avaliacao/observacoes.json')
        old=copy.deepcopy(regs[0]);old['observacao_id']='EXT03-ARTIFICIAL'
        old.pop('nota_id');old.pop('bloco_exploratorio')
        with self.assertRaisesRegex(ValueError,'outras coortes'):a.resumir_registros(regs+[old],plans)
        bad=copy.deepcopy(regs);bad[0]['plano_sha256']='a'*64
        with self.assertRaisesRegex(ValueError,'planos/blocos'):a.resumir_registros(bad,plans)
        bad=copy.deepcopy(regs);bad[0].pop('nota_id')
        with self.assertRaises(ValueError):a.resumir_registros(bad,plans)
        with self.assertRaisesRegex(ValueError,'grupo deve preservar'):a._grupo(regs,plans,False)
        with self.assertRaisesRegex(ValueError,'mesma celula'):a.jaccard(regs,'requisitos')

    def test_trava_antes_da_chave_ignora_usd2_historicos(self):
        self.assertTrue(all(c['orcamento_declarado_usd']=='2' for c in self.plan['configuracoes'].values()))
        with self.assertRaises(ValueError):n.iniciar(self.path,self.out/'real',1)
        with self.assertRaisesRegex(ValueError,'autorizacao especificas'):n.iniciar(self.path,self.out/'real',1,True)
        with self.assertRaises(ValueError):n.iniciar(self.path,self.out/'real',1,True,autorizacao=self.path.parent/'autorizacao-modelo.json')
        self.assertFalse((self.out/'real').exists())

    def test_autorizacao_alterada_durante_validacao_recusada_antes_da_chave(self):
        file=self.out/'auth.json';file.write_bytes(n.api.bytes_json({'autoriza_envio_real':False}))
        with patch.object(n,'validar_autorizacao',return_value={'autoriza_envio_real':True}):
            with self.assertRaisesRegex(ValueError,'mudou durante'):
                n.iniciar(self.path,self.out/'real',1,True,autorizacao=file)
        self.assertFalse((self.out/'real').exists())

    def test_autorizacao_outro_plano_sem_orcamento_ou_data_sem_fuso_recusada(self):
        auth=n.api.base.ler(self.path.parent/'autorizacao-modelo.json')
        auth.update(responsavel='CONTROLE ARTIFICIAL',data='2026-11-11T12:00:00-03:00',justificativa='TESTE; nenhuma aprovacao humana',
                    revisao_par_pacotes_ordem=True,autoriza_envio_real=True,orcamento_usd='0.01')
        file=self.out/'auth.json'
        for field,value in [('plano_sha256','0'*64),('orcamento_usd',None),('data','2026-11-11T12:00:00')]:
            bad={**auth,field:value};file.write_bytes(n.api.bytes_json(bad))
            with self.assertRaises(ValueError):n.validar_autorizacao(self.path,file)

    def test_ramo_real_http_simulado_revisao_pendente_exclusao_por_nota(self):
        auth=n.api.base.ler(self.path.parent/'autorizacao-modelo.json')
        auth.update(responsavel='CONTROLE ARTIFICIAL',data='2026-11-11T12:00:00-03:00',justificativa='CONTROLE: nao e aprovacao humana',
                    revisao_par_pacotes_ordem=True,autoriza_envio_real=True,orcamento_usd='0.01')
        file=self.out/'auth.json';file.write_bytes(n.api.bytes_json(auth))
        def fake(sender,body,key,timeout):return (*self.http(body,key,timeout),None)
        with patch.object(n.api,'chave_api',return_value='CHAVE-FICTICIA'),patch.object(n.api,'obter_http',side_effect=fake):
            self.assertEqual(n.iniciar(self.path,self.out/'lote',1,True,autorizacao=file),0)
            self.assertEqual(n.iniciar(self.path,self.out/'lote',15,True,True,file),0)
            self.assertEqual(n.iniciar(self.path,self.out/'lote',16,True,True,file),0)
        self.assertEqual(len(self.calls),16)
        self.assertEqual(n.api.base.ler(self.out/'lote/lote.json')['orcamento_novo_declarado_usd'],'0.01')
        self.assertEqual((self.out/'lote/autorizacao-envio-original.json').read_bytes(),file.read_bytes())
        code,regs,summary=self.evaluate();self.assertEqual(code,2)
        self.assertEqual(len(summary['celulas']),8)
        template=review.modelo(self.out/'lote',self.out/'avaliacao/lista.json',self.out/'avaliacao/observacoes.json',self.out/'ficha.json')
        d=n.api.base.ler(template);self.assertIsNone(d['responsavel'])
        self.assertTrue(all(r['decisao']=='pendente' and r['nota_id'] in ('N01','N02') for r in d['observacoes']))
        d.update(responsavel='CONTROLE ARTIFICIAL',data='2026-11-11T12:00:00-03:00')
        for r in d['observacoes']:r.update(decisao='incluir',justificativa='SOMENTE CONTROLE ARTIFICIAL EM TEMPORARIO')
        excluded=d['observacoes'][0];excluded['decisao']='excluir'
        filled=self.out/'decisoes.json';filled.write_bytes(n.api.bytes_json(d))
        recorded=review.registrar(filled,self.out/'revisao.json')
        self.assertEqual(review.resumir(recorded,self.out/'resumo-revisado'),1)
        revised=n.api.base.ler(self.out/'resumo-revisado/resumo.json')
        self.assertEqual(revised['N_planejado_original'],16)
        self.assertEqual(len(revised['celulas']),8)
        for cell in revised['celulas']:
            group=cell['grupos'][0];self.assertEqual(group['N_planejado_original'],2)
            for ex in group['exclusoes_conformidade']:self.assertEqual(ex['nota_id'],cell['nota_id'])
        self.assertTrue(all(n.api.base.ler(self.out/'lote'/r['observacao_id']/'T01/tentativa.json')['conformidade_protocolo']=='pendente' for r in regs))


if __name__=='__main__':unittest.main()
