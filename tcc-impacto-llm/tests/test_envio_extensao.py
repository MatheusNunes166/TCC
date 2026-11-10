"""D-42: envio REAL SIMULADO em temporarios, chave ficticia e HTTP substituido.

Nenhuma captura deste teste constitui dado da pesquisa ou chamada externa.
"""
import contextlib
import io
import json
from pathlib import Path
import socket
import tempfile
import unittest
from unittest.mock import patch

import extensao_exploratoria as e
import revisao_conformidade as review

ROOT = e.RAIZ
ORIGEM = ROOT / 'captura/extensao-20261109-002/plano.json'
REF = ROOT / 'materiais/modelos/referencia_candidata_0.3_NAO_ENVIAR_AO_LLM.json'


class TestEnvioExtensao(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.root = Path(cls.temp.name)
        with patch.object(e.api.base, 'protegida', side_effect=lambda p, zona: Path(p)):
            cls.plano = e.preparar(cls.root / 'preparacao', ORIGEM)
        cls.plan = e.conferir(cls.plano)

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def setUp(self):
        temp = tempfile.TemporaryDirectory(dir=self.root)
        self.addCleanup(temp.cleanup)
        self.out = Path(temp.name)
        self.sent = []
        for obj, name, kwargs in (
            (e.api.base, 'protegida', {'side_effect': lambda p, zona: Path(p)}),
            (e.api, 'chave_api', {'return_value': 'CHAVE-FICTICIA-D42'}),
            (e.api, 'enviar', {'side_effect': AssertionError('HTTP real proibido')}),
            (socket, 'create_connection', {'side_effect': AssertionError('rede proibida')}),
            (socket, 'getaddrinfo', {'side_effect': AssertionError('DNS proibido')})):
            mock = patch.object(obj, name, **kwargs)
            mock.start()
            self.addCleanup(mock.stop)
        stream = contextlib.redirect_stdout(io.StringIO())
        stream.__enter__()
        self.addCleanup(stream.__exit__, None, None, None)

    def sender(self, body, key, timeout):
        self.assertEqual(key, 'CHAVE-FICTICIA-D42')
        req = json.loads(body)
        self.sent.append(req)
        return e.artificial(body, None, timeout)

    def iniciar(self, **kwargs):
        return e.iniciar(self.plano, self.out / 'REAL-SIMULADA', 1,
                          enviar_real=True, sender=self.sender, **kwargs)

    def test_nova_versao_preserva_64_ordem_payloads_referencia_e_orcamento(self):
        previous = e.api.base.ler(ORIGEM)
        fields = ('observacao_id', 'ordem', 'bloco', 'repeticao', 'mudanca', 'condicao', 'modelo', 'payload_sha256')
        self.assertEqual(len(self.plan['observacoes']), 64)
        for old, new in zip(previous['observacoes'], self.plan['observacoes']):
            self.assertEqual({k: old[k] for k in fields}, {k: new[k] for k in fields})
            self.assertNotEqual(old['configuracao_id'], new['configuracao_id'])
            self.assertEqual(new['status'], 'PLANEJADA_NAO_EXECUTADA')
        self.assertEqual(self.plan['referencia_sha256'], previous['referencia_sha256'])
        self.assertEqual((self.plano.parent / 'ordem.json').read_bytes(), (ORIGEM.parent / 'ordem.json').read_bytes())
        self.assertEqual((self.plano.parent / 'plano-anterior.json').read_bytes(), ORIGEM.read_bytes())
        self.assertEqual(self.plan['orcamento_declarado_usd'], '2')
        for config in self.plan['configuracoes'].values():
            self.assertEqual(config['orcamento_declarado_usd'], '2')
            self.assertEqual(config['max_output_tokens'], 4096)
            self.assertEqual(config['esforco_solicitado'], 'medium')

    def test_comando_sem_flag_nao_le_chave_nem_envia(self):
        with patch.object(e.api, 'chave_api', side_effect=AssertionError('chave nao deve ser lida')):
            self.assertEqual(e.main(['iniciar', '--plano', str(self.plano), '--lote', str(self.out / 'proibido'), '--limite', '1']), 2)
        self.assertFalse((self.out / 'proibido').exists())
        self.assertEqual(self.sent, [])

    def test_64_envios_simulados_configuracao_por_item_retomada_e_avaliacao(self):
        batch = self.out / 'REAL-SIMULADA'
        def run(limit, resume=False):
            return e.iniciar(self.plano, batch, limit, continuar=resume, enviar_real=True, sender=self.sender)
        self.assertEqual(run(1), 0)
        first = self.plan['observacoes'][0]
        self.assertEqual(first['observacao_id'], 'EXT03-MC-04-v2-E1-SOL-R01')
        firstfiles = {p: e.api.sha(p.read_bytes()) for p in batch.rglob('*') if p.is_file()}
        self.assertEqual(len(self.sent), 1)
        self.assertEqual(run(2, True), 0)  # Posicoes 2 e 3 exercitam Sol e Astra.
        self.assertEqual(len(self.sent), 3)
        self.assertEqual(run(61, True), 0)
        self.assertEqual(run(64, True), 0)
        self.assertEqual(len(self.sent), 64)
        for p, h in firstfiles.items():
            self.assertEqual(e.api.sha(p.read_bytes()), h)
        self.assertEqual({r['model'] for r in self.sent}, set(e.MODELOS))
        header = e.api.base.ler(batch / 'lote.json')
        self.assertEqual((header['origem'], header['fase'], header['etapa']), ('real', 'exploratoria', e.ETAPA))
        for row, sent in zip(self.plan['observacoes'], self.sent):
            attempt = batch / row['observacao_id'] / 'T01'
            reg = e.api.base.conferir_fechamento(attempt)
            self.assertEqual(sent['model'], row['modelo'])
            self.assertEqual(sent['reasoning'], {'effort': 'medium'})
            self.assertEqual(sent['max_output_tokens'], 4096)
            self.assertEqual((sent['tools'], sent['tool_choice']), ([], 'none'))
            self.assertEqual(sent['input'].encode(), (attempt / 'entrada.bin').read_bytes())
            self.assertEqual(reg['modelo_reportado'], row['modelo'])
            self.assertEqual(reg['configuracao'], self.plan['configuracoes'][row['configuracao_id']])
            self.assertEqual((reg['fase'], reg['etapa']), ('exploratoria', e.ETAPA))
            self.assertEqual(reg['retentativas_cliente'], 0)
            self.assertNotIn(b'CHAVE-FICTICIA-D42', (attempt / 'tentativa.json').read_bytes())
        dest = self.out / 'AVALIACOES-REAIS-SIMULADAS'
        # Descricao permitida; resumo controlado segue bloqueado por revisao pendente.
        self.assertEqual(e.api.avaliar_lote(batch, REF, dest), 2)
        entries = e.api.base.ler(dest / 'lista.json')
        self.assertEqual(len(entries), 64)
        self.assertEqual(len(e.api.base.ler(dest / 'observacoes.json')), 64)
        for entry in entries:
            reg = e.api.base.ler(dest / entry['arquivo'])
            self.assertEqual(reg['status_avaliacao'], 'avaliada')
            self.assertEqual((reg['origem'], reg['fase']), ('real', 'exploratoria'))
            self.assertEqual(reg['testes']['desconhecidos'], [])
            self.assertEqual(reg['conformidade_protocolo'], 'pendente')
        model = review.modelo(batch, dest / 'lista.json', dest / 'observacoes.json', self.out / 'revisao.json')
        self.assertEqual(len(e.api.base.ler(model)['observacoes']), 64)

    def test_limites_invalidos_nao_leem_chave(self):
        for limit in (0, 65, True):
            with patch.object(e.api, 'chave_api', side_effect=AssertionError('chave nao deve ser lida')):
                with self.assertRaises(ValueError):
                    e.iniciar(self.plano, self.out / 'invalido', limit, enviar_real=True)

    def test_plano_anterior_recusado_sem_atualizar_seus_hashes(self):
        with patch.object(e.api, 'chave_api', side_effect=AssertionError('chave nao deve ser lida')):
            with self.assertRaises(ValueError):
                e.iniciar(ORIGEM, self.out / 'anterior', 1, enviar_real=True)

    def test_retomada_nao_mistura_controle_sintetico_com_real(self):
        e.controle(self.plano, self.out / 'REAL-SIMULADA', 1)
        with self.assertRaisesRegex(ValueError, 'configuracao/origem/plano'):
            self.iniciar(continuar=True)
        self.assertEqual(self.sent, [])

    def test_falha_e_modelo_divergente_sem_retry_ou_fallback(self):
        for mode in ('timeout', 'modelo'):
            calls = []
            def sender(body, key, timeout):
                calls.append(1)
                if mode == 'timeout':
                    raise e.api.FalhaTransporte('TimeoutError', b'PARCIAL-ARTIFICIAL')
                status, raw, rid = e.artificial(body, None, timeout)
                envelope = json.loads(raw)
                envelope['model'] = 'gpt-6-astra'  # Primeira observacao exige Sol.
                return status, e.api.bytes_json(envelope), rid
            batch = self.out / mode
            self.assertEqual(e.iniciar(self.plano, batch, 1, enviar_real=True, sender=sender), 2)
            with self.assertRaises(ValueError):
                e.iniciar(self.plano, batch, 1, continuar=True, enviar_real=True, sender=sender)
            self.assertEqual(len(calls), 1)
            reg = e.api.base.conferir_fechamento(batch / self.plan['observacoes'][0]['observacao_id'] / 'T01')
            self.assertEqual(reg['fase'], 'exploratoria')
            self.assertEqual(reg['configuracao']['modelo_solicitado'], 'gpt-6-sol')


if __name__ == '__main__':
    unittest.main()
