"""Conformidade real SIMULADA em temporarios; sem HTTP/LLM ou chave real."""
import contextlib
import copy
import io
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import coletor_api as api
import revisao_conformidade as review
from test_coletor_api import resposta


class TestRevisaoConformidade(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.root = Path(cls.temp.name)
        cls.lote = cls.root / 'CONTROLE-ARTIFICIAL-lote'
        cls.avals = cls.root / 'CONTROLE-ARTIFICIAL-avaliados'
        counter = []
        def sender(*args):
            counter.append(1)
            return 200, resposta(id='resp-ARTIFICIAL-' + str(len(counter))), 'req-ARTIFICIAL'
        with patch.object(api.base, 'protegida', side_effect=lambda p, zona: Path(p)), \
                patch.dict(os.environ, OPENAI_API_KEY='FICTICIA-REVISAO'), contextlib.redirect_stdout(io.StringIO()):
            cls.plano = api.preparar(api.base.RAIZ / 'captura/planejamento-piloto-2026-11-07-D38/plano.json',
                                     cls.root / 'plano', 512, '1')
            assert api.capturar(cls.plano, cls.lote, 16, real=True, sender=sender) == 0
            cls.descriptive_status = api.base.avaliar_lote(cls.lote,
                api.base.RAIZ / 'materiais/modelos/referencia_candidata_NAO_ENVIAR_AO_LLM.json', cls.avals)
        cls.originals = {p: api.sha(p.read_bytes()) for folder in (cls.lote, cls.avals)
                         for p in folder.rglob('*') if p.is_file()}

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def setUp(self):
        self.case = tempfile.TemporaryDirectory(dir=self.root)
        self.addCleanup(self.case.cleanup)
        self.out = Path(self.case.name)
        self.scope = patch.object(api.base, 'protegida', side_effect=lambda p, zona: Path(p))
        self.scope.start()
        self.addCleanup(self.scope.stop)

    def tearDown(self):
        self.assertEqual(self.originals, {p: api.sha(p.read_bytes()) for p in self.originals})

    def decisions(self, decision='incluir'):
        path = review.modelo(self.lote, self.avals / 'lista.json', self.avals / 'observacoes.json', self.out / 'modelo.json')
        value = api.base.ler(path)
        value.update(responsavel='CONTROLE ARTIFICIAL de revisao, sem aprovacao de pesquisa',
                     data='2026-11-07T17:00:00-03:00')
        for row in value['observacoes']:
            row.update(decisao=decision, justificativa='CONTROLE: conferencia independente de formato ou pontuacao')
        return value

    def record(self, value):
        path = self.out / 'decisoes-preenchidas.json'
        api.salvar_json(path, value)
        return review.registrar(path, self.out / 'revisao.json')

    def test_descritiva_pendente_e_resumo_controlado_bloqueado(self):
        self.assertEqual(self.descriptive_status, 2)
        records = [api.base.ler(p) for p in self.avals.glob('PIL-*/T01/avaliacao.json')]
        self.assertEqual(len(records), 16)
        self.assertTrue(all(r['status_avaliacao'] == 'avaliada' for r in records))
        self.assertTrue(all(r['conformidade_protocolo'] == 'pendente' for r in records))
        summary = api.base.ler(self.avals / 'resumo/resumo.json')
        self.assertFalse(summary['completo'])
        self.assertTrue(any('pendente' in str(c['diagnosticos']) for c in summary['celulas']))

    def test_revisao_ainda_pendente_nao_libera_resumo(self):
        path = self.record(self.decisions('pendente'))
        self.assertEqual(review.resumir(path, self.out / 'resumo'), 2)
        summary = api.base.ler(self.out / 'resumo/resumo.json')
        self.assertEqual(len(summary['pendentes']), 16)
        self.assertFalse(summary['completo'])

    def test_revisao_explicita_inclui_e_preserva_originais(self):
        path = self.record(self.decisions())
        self.assertEqual(review.resumir(path, self.out / 'resumo'), 0)
        summary = api.base.ler(self.out / 'resumo/resumo.json')
        self.assertTrue(summary['completo'])
        self.assertEqual(summary['N_planejado_original'], 16)
        self.assertEqual(sum(g['contagens']['V'] for c in summary['celulas'] for g in c['grupos']), 16)
        self.assertEqual(sum(c['contagens_operacionais_originais']['N'] for c in summary['celulas']), 16)
        self.assertEqual(len(summary['avaliacoes_originais']), 16)

    def test_exclusao_nao_apaga_captura_ou_denominador(self):
        decisions = self.decisions()
        excluded = decisions['observacoes'][0]
        excluded.update(decisao='excluir', justificativa='CONTROLE ARTIFICIAL: excluir do resumo controlado')
        path = self.record(decisions)
        self.assertEqual(review.resumir(path, self.out / 'resumo'), 1)
        summary = api.base.ler(self.out / 'resumo/resumo.json')
        self.assertEqual(summary['N_planejado_original'], 16)
        self.assertEqual(sum(g['contagens']['N'] for c in summary['celulas'] for g in c['grupos']), 16)
        self.assertEqual(sum(g['contagens']['V'] for c in summary['celulas'] for g in c['grupos']), 15)
        self.assertEqual(sum(c['contagens_operacionais_originais']['V'] for c in summary['celulas']), 16)
        self.assertEqual(summary['excluidas'][0]['observacao_id'], excluded['observacao_id'])
        self.assertFalse(any(excluded['observacao_id'] in g['ausentes'] for c in summary['celulas'] for g in c['grupos']))
        self.assertTrue((self.lote / excluded['observacao_id'] / 'T01/resposta.bin').exists())

    def test_hash_responsavel_data_e_decisao_preservada(self):
        decisions = self.decisions()
        for field in ('responsavel', 'data', 'hash'):
            changed = copy.deepcopy(decisions)
            if field == 'hash':
                changed['observacoes'][0]['avaliacao_sha256'] = '0' * 64
            else:
                changed[field] = None
            path = self.out / (field + '.json')
            api.salvar_json(path, changed)
            with self.assertRaises(ValueError):
                review.registrar(path, self.out / ('revisao-' + field + '.json'))
        registered = self.record(decisions)
        changed = api.base.ler(registered)
        changed['decisoes']['observacoes'][0]['decisao'] = 'excluir'
        tampered = self.out / 'revisao-adulterada.json'
        api.salvar_json(tampered, changed)
        with self.assertRaisesRegex(ValueError, 'decisao original'):
            review.resumir(tampered, self.out / 'resumo-invalido')

    def test_desvio_nao_pode_ser_lavado_por_inclusao(self):
        decisions = self.decisions()
        meta, regs, _, signatures, _ = review.contexto(self.lote, self.avals / 'lista.json', self.avals / 'observacoes.json')
        fake = copy.deepcopy(regs)
        fake[0].update(conformidade_protocolo='desvio', desvios=['CONTROLE: ferramenta inesperada'])
        with self.assertRaisesRegex(ValueError, 'desvio registrado'):
            review.validar_decisoes(decisions, meta, signatures, fake)

    def test_lista_nao_pode_omitir_captura_para_ocultar_exclusao(self):
        entries = api.base.ler(self.avals / 'lista.json')
        # Lista na mesma pasta para preservar resolucao dos caminhos relativos;
        # e um controle novo, nao sobrescreve a lista do avaliador.
        path = self.avals / 'lista-incompleta-CONTROLE.json'
        api.salvar_json(path, entries[:-1])
        with self.assertRaisesRegex(ValueError, 'todas as capturas'):
            review.contexto(self.lote, path, self.avals / 'observacoes.json')


if __name__ == '__main__':
    unittest.main()
