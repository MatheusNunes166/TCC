"""D-41: bancada real local e controles ARTIFICIAIS; nenhuma conexao ou chave."""
import contextlib
import copy
import io
import importlib.util
import json
from pathlib import Path
import socket
import tempfile
import unittest
from unittest.mock import patch

import autorizacao
import avaliacao_ids as a
import extensao_exploratoria as e
import revisao_conformidade as review
import verificacao_variantes as v
from variantes import mc01, mc02, mc03, mc04

ROOT = e.RAIZ
REF = ROOT / 'materiais/modelos/referencia_candidata_0.3_NAO_ENVIAR_AO_LLM.json'
OLD = ROOT / 'materiais/modelos/referencia_candidata_NAO_ENVIAR_AO_LLM.json'


def matriz():
    ref, old = a.json_estrito(REF.read_bytes()), a.json_estrito(OLD.read_bytes())
    assert ref['catalogo'][:12] == old['catalogo']
    functions = {'BASELINE': autorizacao.autorizar, 'MC-01': mc01.autorizar,
                 'MC-02': mc02.autorizar, 'MC-03': mc03.autorizar, 'MC-04-v2': mc04.autorizar}
    base = (ROOT / 'autorizacao.py').read_bytes()
    for change, source in v.VARIANTS.items():
        v.audit_source(base, (ROOT / source).read_bytes(), change, v.BASELINE)
    rows = []
    for name, function in functions.items():
        change = next((m for m in ref['mudancas'] if m['id'] == name), None)
        previous = next((m for m in old['mudancas'] if m['id'] == name), None)
        for case in ref['catalogo']:
            expected = case['esperado'] if change is None else change['expected'][case['id']]
            if previous is not None and case['id'] in previous['expected']:
                assert expected == previous['expected'][case['id']]
            observed = function(case['estado'], frozenset(case['papeis']), case['operacao'])
            rows.append({'versao': name, 'teste': case['id'], 'esperado': expected,
                         'observado': observed, 'conforme': expected == observed})
    return rows


class TestBancada03(unittest.TestCase):
    def test_75_decisoes_motivos_e_60_anteriores_preservados(self):
        rows = matriz()
        self.assertEqual(len(rows), 75)
        for row in rows:
            with self.subTest(versao=row['versao'], teste=row['teste']):
                self.assertTrue(row['conforme'], row)

    def test_politica_conservadora_e_particoes_60_pares(self):
        ref = a.json_estrito(REF.read_bytes())
        for change in ref['mudancas']:
            included = []
            for c in ref['catalogo']:
                roles = set(c['papeis']) | ({'Consulta'} if 'Supervisão' in c['papeis'] else set())
                applies = {'MC-01': c['operacao'] == 'exportar' and 'Auditoria' in roles,
                           'MC-02': {'Consulta', 'Auditoria'} <= roles,
                           'MC-03': c['operacao'] == 'visualizar' and 'Consulta' in roles,
                           'MC-04-v2': 'Supervisão' in c['papeis']}[change['id']]
                if applies:
                    included.append(c['id'])
                if c['id'] in change['tests']:
                    effect = 'preserved' if change['expected'][c['id']] == c['esperado'] else 'changed'
                    self.assertIn(c['id'], change[effect])
            self.assertEqual(included, change['tests'])
            self.assertFalse(set(change['changed']) & set(change['preserved']))
            self.assertEqual(set(change['tests']), set(change['changed']) | set(change['preserved']))

    def test_novos_ids_sao_conhecidos_so_na_referencia_03(self):
        data = b'{"requisitos":["RF-02"],"testes":["T13","T14","T15","T16"]}'
        for path, unknown in ((OLD, ['T13', 'T14', 'T15', 'T16']), (REF, ['T16'])):
            result = a.avaliar_resposta(data, a.json_estrito(path.read_bytes()))
            self.assertEqual(result['testes']['desconhecidos'], unknown)
            self.assertEqual(result['testes']['FP'], 2 if path == REF else 4)

    def test_piloto_16_mesma_interpretacao_no_avaliador_anterior(self):
        source = ROOT / 'evidencias/spec004/extensao-2026-11-09/fontes-anteriores/avaliacao_ids.py'
        spec = importlib.util.spec_from_file_location('avaliador_preservado_D40', source)
        previous = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(previous)
        reference = a.json_estrito(OLD.read_bytes())
        paths = list((ROOT / 'avaliados/piloto-api-001').glob('PIL-*/T01/resposta-original.bin'))
        self.assertEqual(len(paths), 16)
        for path in paths:
            reg = a.json_estrito((path.parent / 'avaliacao.json').read_bytes())
            self.assertEqual(a.avaliar_resposta(path.read_bytes(), reference, reg['mudanca']),
                             previous.avaliar_resposta(path.read_bytes(), reference, reg['mudanca']))


class TestExtensao(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.root = Path(cls.temp.name)
        with patch.object(e.api.base, 'protegida', side_effect=lambda p, z: Path(p)):
            cls.plan = e.preparar(cls.root / 'preparacao')
        cls.original = e.conferir(cls.plan)

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def setUp(self):
        self.case = tempfile.TemporaryDirectory(dir=self.root)
        self.addCleanup(self.case.cleanup)
        self.out = Path(self.case.name)
        for target, attr in ((socket, 'create_connection'), (socket, 'getaddrinfo'), (e.api, 'chave_api'), (e.api, 'enviar')):
            guard = patch.object(target, attr, side_effect=AssertionError('rede/chave real proibida'))
            guard.start()
            self.addCleanup(guard.stop)
        scope = patch.object(e.api.base, 'protegida', side_effect=lambda p, z: Path(p))
        scope.start()
        self.addCleanup(scope.stop)
        self.output = contextlib.redirect_stdout(io.StringIO())
        self.output.__enter__()
        self.addCleanup(self.output.__exit__, None, None, None)

    def test_64_ordem_blocos_modelos_identidades_e_payloads(self):
        plan = e.conferir(self.plan)
        self.assertEqual(len(plan['observacoes']), 64)
        self.assertEqual(len({r['observacao_id'] for r in plan['observacoes']}), 64)
        for block in (1, 2):
            rows = [r for r in plan['observacoes'] if r['bloco'] == block]
            self.assertEqual(len(rows), 32)
            self.assertEqual({(r['mudanca'], r['condicao'], r['modelo']) for r in rows},
                             {(m, c, model) for m in e.montagem.MUDANCAS for c in e.montagem.CONDICOES for model in e.MODELOS})
        for config in plan['configuracoes'].values():
            self.assertEqual(config['max_output_tokens'], 4096)
            self.assertEqual(config['esforco_solicitado'], 'medium')
        self.assertEqual([r['observacao_id'] for r in plan['observacoes']], [r['observacao_id'] for r in e.ordem()])

    def test_textos_anteriores_preservados_e_catalogo_igual_nos_32(self):
        for model in e.MODELOS:
            for change in e.montagem.MUDANCAS:
                for cond in e.montagem.CONDICOES:
                    p = self.plan.parent / 'preparados' / model / (change + '-' + cond) / 'documentos'
                    docs, _ = e.fontes.reunir_fontes(ROOT, change, cond)
                    for name, old in docs.items():
                        if name == 'catalogo-baseline.md':
                            current = (p / name).read_bytes()
                            self.assertTrue(current.startswith(e.fontes.normalizar_documento(old)))
                            self.assertEqual(current.count(b'| T'), 15)
                        else:
                            self.assertEqual((p / name).read_bytes(), e.fontes.normalizar_documento(old))
                    self.assertEqual((p / 'notas.md').exists(), cond in ('D1', 'E1'))

    def test_64_capturas_retomada_e_avaliacao_separadas(self):
        batch = self.out / 'ARTIFICIAL-lote'
        self.assertEqual(e.controle(self.plan, batch, 17), 0)
        original = {p: a.sha(p.read_bytes()) for p in batch.rglob('*') if p.is_file()}
        self.assertEqual(e.controle(self.plan, batch, 47, continuar=True), 0)
        self.assertEqual(e.controle(self.plan, batch, 64, continuar=True), 0)
        self.assertEqual(len(list(batch.glob('EXT03-*/T01/tentativa.json'))), 64)
        for p, h in original.items():
            self.assertEqual(a.sha(p.read_bytes()), h)
        for row in self.original['observacoes']:
            attempt = batch / row['observacao_id'] / 'T01'
            reg = e.api.base.conferir_fechamento(attempt)
            req = a.json_estrito((attempt / 'requisicao.json').read_bytes())
            self.assertEqual(req['model'], row['modelo'])
            self.assertEqual(reg['configuracao']['modelo_solicitado'], row['modelo'])
            self.assertIsNone(reg['modelo_reportado'])
            self.assertEqual(reg['origem'], 'sintetica')
        dest = self.out / 'ARTIFICIAL-avaliacoes'
        self.assertEqual(e.api.base.avaliar_lote(batch, REF, dest), 0)
        for path in dest.glob('EXT03-*/T01/avaliacao.json'):
            reg = a.json_estrito(path.read_bytes())
            self.assertEqual(reg['testes']['desconhecidos'], [])
        model = review.modelo(batch, dest / 'lista.json', dest / 'observacoes.json', self.out / 'revisao.json')
        decisions = a.json_estrito(model.read_bytes())
        self.assertEqual(len(decisions['observacoes']), 64)
        self.assertTrue(all(r['decisao'] == 'pendente' for r in decisions['observacoes']))
        decisions.update(responsavel='CONTROLE ARTIFICIAL; nenhuma aprovacao de pesquisa',
                         data='2026-11-09T12:00:00-03:00')
        for row in decisions['observacoes']:
            row.update(decisao='pendente', justificativa='ARTIFICIAL: ainda sem revisao')
        e.api.salvar_json(self.out / 'pendentes.json', decisions)
        reviewed = review.registrar(self.out / 'pendentes.json', self.out / 'revisao-pendente.json')
        self.assertEqual(review.resumir(reviewed, self.out / 'resumo-pendente'), 2)
        for row in decisions['observacoes']:
            row.update(decisao='incluir', justificativa='ARTIFICIAL: conferencia separada da pontuacao')
        decisions['observacoes'][0].update(decisao='excluir', justificativa='ARTIFICIAL: exercitar exclusao conservando N')
        e.api.salvar_json(self.out / 'decisoes.json', decisions)
        reviewed = review.registrar(self.out / 'decisoes.json', self.out / 'revisao-artificial.json')
        self.assertEqual(review.resumir(reviewed, self.out / 'resumo-revisado'), 1)
        summary = a.json_estrito((self.out / 'resumo-revisado/resumo.json').read_bytes())
        self.assertEqual(summary['N_planejado_original'], 64)
        self.assertEqual(len(summary['excluidas']), 1)
        self.assertEqual(len(summary['avaliacoes_originais']), 64)

    def test_versoes_e_configuracoes_nao_podem_ser_misturadas(self):
        plan = copy.deepcopy(self.original)
        for mutate in (lambda p: p.update(catalogo_versao='0.2'),
                       lambda p: p['observacoes'][0].update(configuracao_id=p['observacoes'][1]['configuracao_id'] + '-OUTRA'),
                       lambda p: p['observacoes'][0].update(preparacao=p['observacoes'][2]['preparacao']),
                       lambda p: p['observacoes'].reverse(),
                       lambda p: p['observacoes'].pop(),
                       lambda p: next(iter(p['configuracoes'].values())).update(modelo_solicitado='outro'),
                       lambda p: next(iter(p['configuracoes'].values())).update(max_output_tokens=8192)):
            changed = copy.deepcopy(plan)
            mutate(changed)
            # Mantem caminhos relativos das preparacoes sem copiar os milhares de bytes.
            testfile = self.plan.parent / ('mutacao-' + str(id(changed)) + '.json')
            testfile.write_bytes(e.api.bytes_json(changed))
            with self.assertRaises(ValueError):
                e.conferir(testfile)

    def test_avaliador_rejeita_referencia_antiga_para_preparacao_nova_e_inverso(self):
        batch = self.out / 'ARTIFICIAL-lote'
        e.controle(self.plan, batch, 1)
        attempt = next(batch.glob('EXT03-*/T01'))
        result, code = a.avaliar(attempt / 'preparacao/preparacao.json', attempt / 'tentativa.json', OLD, self.out / 'avaliacao-errada')
        self.assertEqual(code, 2)
        self.assertEqual(result['status_avaliacao'], 'erro_integridade')
        # Controle anterior construido pelo mesmo motor continua na versao 0.2.
        oldplan = e.api.preparar(ROOT / 'captura/planejamento-piloto-2026-11-07-D38/plano.json', self.out / 'plano-antigo', 512, '1')
        e.api.capturar(oldplan, self.out / 'lote-antigo', 1)
        attempt = next((self.out / 'lote-antigo').glob('PIL-*/T01'))
        result, code = a.avaliar(attempt / 'preparacao/preparacao.json', attempt / 'tentativa.json', REF, self.out / 'avaliacao-errada-inversa')
        self.assertEqual((code, result['status_avaliacao']), (2, 'erro_integridade'))

    def test_invalida_preserva_bytes_e_nao_repete(self):
        count = []
        def invalid(body, key, timeout):
            count.append(1)
            status, raw, rid = e.artificial(body, key, timeout)
            data = a.json_estrito(raw)
            data['output'][0]['content'][0]['text'] = ' ```json\nINVALIDO\n```\r\n'
            return status, e.api.bytes_json(data), rid
        batch = self.out / 'ARTIFICIAL-invalida'
        self.assertEqual(e.controle(self.plan, batch, 1, resposta=invalid), 0)
        self.assertEqual(e.controle(self.plan, batch, 1, continuar=True, resposta=invalid), 0)
        self.assertEqual(len(count), 2)
        attempt = next(batch.glob('EXT03-*/T01'))
        self.assertEqual((attempt / 'resposta.bin').read_bytes(), b' ```json\nINVALIDO\n```\r\n')
        result, code = a.avaliar(attempt / 'preparacao/preparacao.json', attempt / 'tentativa.json', REF, self.out / 'invalida-avaliada')
        self.assertEqual((code, result['status_avaliacao']), (1, 'resposta_formato_invalido'))

    def test_falha_parcial_e_modelo_divergente_bloqueiam_reenvio(self):
        for mode in ('timeout', 'modelo', 'incomplete', 'http'):
            count = []
            def response(body, key, timeout):
                count.append(1)
                if mode == 'timeout':
                    raise e.api.FalhaTransporte('TimeoutError', b'PARCIAL-ARTIFICIAL')
                status, raw, rid = e.artificial(body, key, timeout)
                data = a.json_estrito(raw)
                if mode == 'modelo':
                    data['model'] = 'outro-sem-fallback'
                if mode == 'incomplete':
                    data['status'] = 'incomplete'
                return 429 if mode == 'http' else status, e.api.bytes_json(data), rid
            batch = self.out / ('ARTIFICIAL-' + mode)
            self.assertEqual(e.controle(self.plan, batch, 1, resposta=response), 2)
            with self.assertRaises(ValueError):
                e.controle(self.plan, batch, 1, continuar=True, resposta=response)
            self.assertEqual(len(count), 1)
            attempt = next(batch.glob('EXT03-*/T01'))
            self.assertTrue((attempt / 'fechamento.json').exists())

    def test_envio_real_extensao_exige_flag_antes_da_chave(self):
        with self.assertRaisesRegex(ValueError, '--enviar-real'):
            e.iniciar(self.plan, self.out / 'proibido', 1)
        self.assertFalse((self.out / 'proibido').exists())


if __name__ == '__main__':
    unittest.main()
