"""Respostas artificiais; nunca abrem a rede ou leem chave real."""
import copy
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import urllib.error

import coletor_api as api


def resposta(text=' {"requisitos":[],"testes":[]}\r\n', **extras):
    data = {'id': 'resp-controle', 'model': 'gpt-6-sol', 'status': 'completed',
            'tools': [], 'tool_choice': 'none', 'usage': {'input_tokens': 10, 'output_tokens': 5},
            'output': [{'type': 'message', 'role': 'assistant', 'status': 'completed',
                        'content': [{'type': 'output_text', 'text': text}]}]}
    data.update(extras)
    return api.bytes_json(data)


class TestAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.root = Path(cls.temp.name)
        cls.origem = api.base.RAIZ / 'captura/planejamento-piloto-2026-11-07-D38/plano.json'
        with patch.object(api.base, 'protegida', side_effect=lambda p, zona: Path(p)):
            cls.plano = api.preparar(cls.origem, cls.root / 'plano', 512, '1')
        cls.config = api.conferir(cls.plano)['configuracao']

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def setUp(self):
        self.temp_case = tempfile.TemporaryDirectory(dir=self.root)
        self.addCleanup(self.temp_case.cleanup)
        self.out = Path(self.temp_case.name)

    def capturar(self, **kwargs):
        with patch.object(api.base, 'protegida', side_effect=lambda p, zona: Path(p)):
            return api.capturar(self.plano, self.out / 'lote', 1, **kwargs)

    def tentativa(self):
        return next((self.out / 'lote').glob('PIL-*/T01'))

    def test_ordem_textos_configuracao_e_fase_separados(self):
        old = api.base.conferir_plano(self.origem)
        new = api.conferir(self.plano)
        self.assertEqual([r['observacao_id'] for r in old['observacoes']], [r['observacao_id'] for r in new['observacoes']])
        self.assertEqual([r['payload_sha256'] for r in old['observacoes']], [r['payload_sha256'] for r in new['observacoes']])
        self.assertNotEqual(old['configuracao_id'], new['configuracao_id'])
        self.assertEqual(new['configuracao']['retries_automaticos_cliente'], 0)

    def test_requisicao_so_texto_sem_historico_ferramentas_ou_segredo(self):
        raw = 'ação\ntexto integral\n'.encode()
        body = api.requisicao(raw, self.config)
        value = json.loads(body)
        self.assertEqual(value['input'].encode(), raw)
        self.assertEqual(set(value), {'model','input','reasoning','max_output_tokens','tools','tool_choice','store','stream'})
        self.assertEqual(value['tools'], [])
        self.assertEqual(value['tool_choice'], 'none')
        self.assertFalse(value['store'])
        self.assertFalse(value['stream'])

    def test_parse_preserva_texto_recusa_invalida_e_incompleta(self):
        for text in ('', 'nao posso responder', '```json\n{}\n```', ' \r\n{"requisitos":[],"testes":[]}\r\n '):
            r = api.interpretar(resposta(text), 200, self.config)
            self.assertTrue(r['concluida'])
            self.assertEqual(r['texto'], text.encode())
        refused = json.loads(resposta())
        refused['output'][0]['content'] = [{'type': 'refusal', 'refusal': 'recusa literal'}]
        self.assertEqual(api.interpretar(api.bytes_json(refused),200,self.config)['texto'], b'recusa literal')
        self.assertFalse(api.interpretar(resposta(status='incomplete'),200,self.config)['concluida'])
        self.assertFalse(api.interpretar(b'nao e JSON',200,self.config)['concluida'])
        self.assertFalse(api.interpretar(resposta(),429,self.config)['concluida'])

    def test_output_tools_modelo_historico_e_mensagens_extras_sao_desvios(self):
        for extra in ({'model':'outro'}, {'tools':[{'type':'function'}]}, {'instructions':'extra'},
                      {'previous_response_id':'outra'}, {'tool_choice':'auto'}):
            self.assertTrue(api.interpretar(resposta(**extra),200,self.config)['desvios'])
        raw = json.loads(resposta())
        raw['output'].append(copy.deepcopy(raw['output'][0]))
        self.assertFalse(api.interpretar(api.bytes_json(raw),200,self.config)['concluida'])

    def test_controle_sem_rede_credencial_e_avaliacao_separada(self):
        with patch.object(api, 'enviar', side_effect=AssertionError('rede proibida')):
            self.assertEqual(self.capturar(), 0)
        record = api.base.ler(self.tentativa() / 'tentativa.json')
        self.assertEqual((record['origem'],record['fase']), ('sintetica','verificacao_sintetica'))
        self.assertIsNone(record['modelo_reportado'])
        with patch.object(api.base, 'protegida', side_effect=lambda p, zona: Path(p)):
            api.base.avaliar_lote(self.out/'lote',api.base.RAIZ/'materiais/modelos/referencia_candidata_NAO_ENVIAR_AO_LLM.json', self.out/'avaliados')
        self.assertEqual(len(list((self.out/'avaliados').glob('PIL-*/T*/avaliacao.json'))),1)

    def test_real_simulada_uma_chamada_chave_nao_persistida_e_sem_reenvio(self):
        sent=[]
        def sender(body, key, timeout):
            sent.append(body)
            self.assertEqual(key,'SEGREDO-FICTICIO')
            return 200,resposta('JSON INVALIDO preservado',id='resp-controle-'+str(len(sent))), 'req-controle'
        with patch.dict(os.environ,OPENAI_API_KEY='SEGREDO-FICTICIO'):
            self.assertEqual(self.capturar(real=True,sender=sender),0)
            self.assertEqual(self.capturar(real=True,sender=sender,continuar=True),0)
        self.assertEqual(len(sent),2)  # primeira + proxima observacao; nao reenviou a primeira
        for p in (self.out/'lote').rglob('*'):
            if p.is_file():self.assertNotIn(b'SEGREDO-FICTICIO',p.read_bytes())
        self.assertEqual((self.tentativa()/'resposta.bin').read_bytes(),b'JSON INVALIDO preservado')

    def test_timeout_preservado_e_continuacao_bloqueada(self):
        count=[]
        def timeout(*args):
            count.append(1)
            raise TimeoutError('SEGREDO-FICTICIO')
        with patch.dict(os.environ,OPENAI_API_KEY='SEGREDO-FICTICIO'):
            self.assertEqual(self.capturar(real=True,sender=timeout),2)
            with self.assertRaises(ValueError):self.capturar(real=True,sender=timeout,continuar=True)
        self.assertEqual(len(count),1)
        self.assertTrue((self.tentativa()/'requisicao.json').exists())
        self.assertNotIn('SEGREDO-FICTICIO',(self.tentativa()/'tentativa.json').read_text())

    def test_hash_tamper_retomada_e_orcamento(self):
        self.assertEqual(self.capturar(),0)
        (self.tentativa()/'resposta.bin').write_bytes(b'alterada')
        with self.assertRaises(ValueError):self.capturar(continuar=True)
        for value in ('0','-1','NaN','Infinity','x'):
            with patch.object(api.base,'protegida',side_effect=lambda p,z:Path(p)):
                with self.assertRaises(ValueError):api.preparar(self.origem,self.out/'invalido',512,value)

    def test_iniciar_sem_flag_ou_chave_nao_chama_rede(self):
        with patch.object(api,'enviar',side_effect=AssertionError('rede proibida')):
            self.assertEqual(api.main(['iniciar','--plano',str(self.plano),'--lote',str(self.out/'x'),'--limite','1']),2)
            with patch.dict(os.environ,OPENAI_API_KEY=''):
                with self.assertRaises(ValueError):self.capturar(real=True)
        self.assertFalse((self.out/'lote').exists())

    def test_redirect_e_http_error_sem_retry(self):
        self.assertIsNone(api.SemRedirecionar().redirect_request(None,None,302,'',{},'https://outro'))
        import io
        err=urllib.error.HTTPError(api.ENDPOINT,429,'limited',{'x-request-id':'controle'},io.BytesIO(b'{"error":{}}'))
        with patch.object(api.urllib.request,'build_opener') as factory:
            factory.return_value.open.side_effect=err
            status,body,request_id=api.enviar(b'{}','SEGREDO-FICTICIO',1)
            self.assertEqual((status,body,request_id),(429,b'{"error":{}}','controle'))
            self.assertEqual(factory.return_value.open.call_count,1)

    def test_conexao_neutra_separada_e_explicita(self):
        sent=[]
        def sender(body,key,timeout):
            data=json.loads(body)
            self.assertEqual(data['input'],'Responda apenas OK.\n')
            self.assertNotIn('RF-',data['input'])
            sent.append(body)
            return 200,resposta('OK'),'req-conexao-controle'
        with patch.dict(os.environ,OPENAI_API_KEY='SEGREDO-FICTICIO'):
            with patch.object(api.base,'protegida',side_effect=lambda p,z:Path(p)):
                self.assertEqual(api.conexao(self.out/'conexao',512,sender=sender),0)
                with self.assertRaises(ValueError):api.conexao(self.out/'conexao',512,sender=sender)
        result=api.base.ler(self.out/'conexao/resultado.json')
        self.assertFalse(result['incluido_piloto'])
        self.assertEqual(len(sent),1)
        self.assertEqual(api.main(['conexao','--saida',str(self.out/'nao-criar'),'--limite-saida','512']),2)
        self.assertFalse((self.out/'nao-criar').exists())

    def test_response_id_duplicado_interrompe_sem_escolher_resultado(self):
        def sender(*args):return 200,resposta(),'req-controle'
        with patch.dict(os.environ,OPENAI_API_KEY='SEGREDO-FICTICIO'):
            self.assertEqual(self.capturar(real=True,sender=sender),0)
            self.assertEqual(self.capturar(real=True,sender=sender,continuar=True),2)
            with self.assertRaises(ValueError):self.capturar(real=True,sender=sender,continuar=True)
        self.assertEqual(len(list((self.out/'lote').glob('PIL-*/T01/tentativa.json'))),2)

    def test_lote_sintetico_16_e_avaliacao_integrada_sem_rede(self):
        with patch.object(api.base,'protegida',side_effect=lambda p,z:Path(p)):
            self.assertEqual(api.capturar(self.plano,self.out/'lote',16),0)
            originals={p:p.read_bytes() for p in (self.out/'lote').glob('PIL-*/T01/tentativa.json')}
            self.assertEqual(len(originals),16)
            self.assertEqual(api.capturar(self.plano,self.out/'lote',16,continuar=True),0)
            self.assertEqual(originals,{p:p.read_bytes() for p in originals})
            status=api.base.avaliar_lote(self.out/'lote',api.base.RAIZ/'materiais/modelos/referencia_candidata_NAO_ENVIAR_AO_LLM.json',self.out/'avaliados')
        self.assertEqual(status,0)
        evaluations=list((self.out/'avaliados').glob('PIL-*/T*/avaliacao.json'))
        self.assertEqual(len(evaluations),16)
        self.assertTrue(all(api.base.ler(p)['origem']=='sintetica' for p in evaluations))
