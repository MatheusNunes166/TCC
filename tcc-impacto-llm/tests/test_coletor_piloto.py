"""Controles offline: processos locais fixos, sem chamadas ao Codex/LLM/rede."""
import contextlib
import copy
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import coletor_piloto as c


class TestColetor(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Uma preparacao real textual e reutilizada; nenhuma resposta de modelo.
        cls.temp = tempfile.TemporaryDirectory(dir=c.RAIZ / 'saidas-locais')
        cls.root = Path(cls.temp.name)
        with patch.object(c, 'protegida', side_effect=lambda p, zona: c.montagem.sem_links(p)):
            cls.plan = c.preparar_plano(cls.root / 'planejamento')

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def setUp(self):
        self.temp_case = tempfile.TemporaryDirectory(dir=self.root)
        self.addCleanup(self.temp_case.cleanup)
        self.case = Path(self.temp_case.name)
        self.stub = [sys.executable, '-B', str(c.RAIZ / 'tests/substituto_coletor.py')]

    def run_capture(self, mode='valida', **kwargs):
        argv = self.stub if mode == 'valida' else self.stub + [mode]
        with contextlib.redirect_stdout(io.StringIO()):
            return c._capturar(self.plan, self.case / 'lote', argv, **kwargs)

    def attempts(self):
        return sorted((self.case / 'lote').glob('PIL-*/T*/tentativa.json'))

    def test_plano_simulacao_sem_invocacao_e_ordem_registrada(self):
        with patch.object(subprocess, 'Popen', side_effect=AssertionError('processo proibido')):
            report = c.simular(self.plan)
            self.assertEqual((report['observacoes'], report['payloads_unicos']), (16, 8))
            self.assertTrue(report['bloqueios_envio'])
            with contextlib.redirect_stdout(io.StringIO()), self.assertRaises(SystemExit) as exit_code:
                c.main(['--help'])
            self.assertEqual(exit_code.exception.code, 0)
        plan = c.conferir_plano(self.plan)
        self.assertEqual(plan['semente_ordem'], 20261106)
        self.assertIn('shuffle', plan['algoritmo_ordem'])
        for cmd in report['comandos']:
            self.assertIn('--model', cmd['argv'])
            self.assertIn('gpt-6-sol', cmd['argv'])
            self.assertNotIn('resume', cmd['argv'])
            self.assertNotIn('--output-schema', cmd['argv'])
        with patch.object(c, 'protegida', side_effect=lambda p, zona: c.montagem.sem_links(p)):
            new = c.preparar_plano(self.case / 'outro', self.plan)
        self.assertEqual([r['observacao_id'] for r in c.ler(new)['observacoes']],
                         [r['observacao_id'] for r in plan['observacoes']])

    def test_envio_real_sempre_bloqueado_inclusive_com_flag(self):
        with patch.object(subprocess, 'Popen', side_effect=AssertionError('modelo proibido')):
            for flag in (False, True):
                with self.assertRaisesRegex(ValueError, 'BLOQUEADO|--enviar-real'):
                    c.iniciar_real(self.plan, c.RAIZ / 'captura/NAO_CRIAR', flag)
        self.assertFalse((c.RAIZ / 'captura/NAO_CRIAR').exists())

    def test_16_capturas_bytes_repeticoes_e_continuacao_sem_reenvio(self):
        self.assertEqual(self.run_capture(limite=3), 0)
        first = {p: p.read_bytes() for p in self.attempts()}
        self.assertEqual(len(first), 3)
        self.assertEqual(self.run_capture(continuar=True), 0)
        self.assertEqual(len(self.attempts()), 16)
        for path, data in first.items():
            self.assertEqual(path.read_bytes(), data)
        sessions, inputs = [], {}
        for attempt in self.attempts():
            record = c.ler(attempt)
            self.assertEqual((record['origem'], record['fase']), ('sintetica', 'verificacao_sintetica'))
            self.assertIsNone(record['modelo_reportado'])
            folder = attempt.parent
            data = (folder / 'entrada.bin').read_bytes()
            self.assertEqual(data, (folder / 'ambiente/stdin-recebido.bin').read_bytes())
            self.assertEqual(data, (folder / 'preparacao/payload.txt').read_bytes())
            self.assertEqual((folder / 'resposta.bin').read_bytes(), b' \r\n{"requisitos":[],"testes":[]}\r\n ')
            sessions.append(record['sessao'])
            key = (record['mudanca'], record['condicao'])
            if key in inputs:
                self.assertEqual(data, inputs[key])
            inputs[key] = data
            c.conferir_fechamento(folder)
        self.assertEqual(len(set(sessions)), 16)
        with patch.object(subprocess, 'Popen', side_effect=AssertionError('nao reenviar')):
            self.assertEqual(self.run_capture(continuar=True), 0)

    def test_invalida_e_vazia_nao_geram_retry(self):
        for mode in ('invalida', 'vazia'):
            with self.subTest(mode=mode):
                previous_case = self.case
                self.case = previous_case / mode
                self.case.mkdir()
                self.assertEqual(self.run_capture(mode, limite=1), 0)
                record = c.ler(self.attempts()[0])
                self.assertEqual(record['estado_tecnico'], 'concluida')
                self.assertEqual(self.run_capture(mode, continuar=True, limite=0), 0)
                self.assertEqual(len(self.attempts()), 1)
                self.case = previous_case

    def test_falha_tecnica_so_uma_retentativa_vinculada(self):
        self.assertEqual(self.run_capture('tecnica'), 1)
        self.assertEqual(self.run_capture('tecnica', continuar=True), 1)
        paths = self.attempts()
        self.assertEqual(len(paths), 2)
        first, second = [c.ler(p) for p in paths]
        self.assertEqual(second['tentativa_anterior'], first['tentativa_id'])
        self.assertEqual(second['payload_sha256'], first['payload_sha256'])
        self.assertEqual(first['retorno_processo'], 7)
        self.assertTrue((paths[0].parent / 'stderr.bin').read_bytes())
        # Observacao encerrada apos T02; continua na proxima, sem T03.
        self.assertEqual(self.run_capture('tecnica', continuar=True), 1)
        self.assertFalse(list((self.case / 'lote').glob('PIL-*/T03')))
        self.assertEqual(len(self.attempts()), 3)

    def test_interrupcao_e_morte_apos_fechamento_sem_duplicacao(self):
        self.assertEqual(self.run_capture(limite=1), 0)
        first = self.attempts()[0]
        original = first.read_bytes()
        def interrupt(argv, payload, work, stdout, stderr):
            stdout.write_bytes(b'{"type":"turn.started"}\n')
            stderr.write_bytes(b'parcial\r\n')
            raise KeyboardInterrupt
        self.assertEqual(self.run_capture(continuar=True, executor=interrupt), 130)
        self.assertEqual(first.read_bytes(), original)
        with self.assertRaisesRegex(ValueError, 'interrompido'):
            self.run_capture(continuar=True)
        self.assertEqual(len(self.attempts()), 2)
        for attempt in self.attempts():
            c.conferir_fechamento(attempt.parent)

    def test_falha_antes_do_processo_e_recuperacao_sem_reenvio(self):
        def missing(*args):
            raise FileNotFoundError('CONTROLE: executavel indisponivel')
        self.assertEqual(self.run_capture(executor=missing), 1)
        self.assertEqual(self.run_capture(continuar=True, limite=1), 0)
        paths = self.attempts()
        self.assertEqual(len(paths), 2)
        self.assertEqual(c.ler(paths[1])['tentativa_anterior'], c.ler(paths[0])['tentativa_id'])
        (paths[1].parent / 'fechamento.json').unlink()  # Simula crash apos tentativa.json.
        with self.assertRaisesRegex(ValueError, 'interrompida/ambigua'):
            self.run_capture(continuar=True)
        self.assertEqual(c.recuperar(self.case / 'lote')['recuperados_sem_envio'], 1)
        self.assertEqual(self.run_capture(continuar=True, limite=0), 0)
        self.assertEqual(len(self.attempts()), 2)

    def test_ambiente_nao_herda_contexto_ou_credenciais(self):
        with patch.dict(c.os.environ, {'CODEX_THREAD_ID': 'CONTROLE', 'OPENAI_API_KEY': 'CONTROLE',
                                      'CODEX_CUSTOM_INSTRUCTIONS': 'CONTROLE'}):
            child_env = c.ambiente_filho()
            self.assertNotIn('CODEX_THREAD_ID', child_env)
            self.assertNotIn('OPENAI_API_KEY', child_env)
            self.assertNotIn('CODEX_CUSTOM_INSTRUCTIONS', child_env)

    def test_erro_de_cliente_com_final_nao_e_reenviado(self):
        def recovered(argv, payload, work, stdout, stderr):
            events = [{'type': 'thread.started', 'thread_id': 'CONTROLE-reconnect'},
                      {'type': 'turn.started'}, {'type': 'error', 'message': 'CONTROLE reconnect'},
                      {'type': 'item.completed', 'item': {'type': 'agent_message', 'text': 'INVALIDA preservada\r\n'}},
                      {'type': 'turn.completed'}]
            stdout.write_bytes(b''.join(json.dumps(e).encode() + b'\n' for e in events))
            stderr.write_bytes(b'CONTROLE sem transporte real')
            return 0
        self.assertEqual(self.run_capture(executor=recovered), 2)
        attempt = c.ler(self.attempts()[0])
        self.assertEqual(attempt['estado_tecnico'], 'concluida')
        self.assertEqual(attempt['transporte_observavel']['turnos_iniciados_observados'], 1)
        with self.assertRaisesRegex(ValueError, 'desvio previo'):
            self.run_capture(continuar=True)
        self.assertEqual(len(self.attempts()), 1)

    def test_integridade_tamper_configuracao_e_caminhos(self):
        self.assertEqual(self.run_capture(limite=1), 0)
        response = self.attempts()[0].parent / 'resposta.bin'
        response.write_bytes(b'alterada')
        with self.assertRaisesRegex(ValueError, 'captura alterada'):
            self.run_capture(continuar=True)
        plan = c.ler(self.plan)
        for mutation in ('modelo', 'ordem', 'payload', 'traversal'):
            changed = copy.deepcopy(plan)
            if mutation == 'modelo':
                changed['configuracao']['modelo_solicitado'] = 'gpt-6.1-sol'
            elif mutation == 'ordem':
                changed['observacoes'][0]['ordem'] = 2
            elif mutation == 'payload':
                changed['observacoes'][0]['payload_sha256'] = '0' * 64
            else:
                changed['observacoes'][0]['preparacao'] = '../privado.json'
            path = self.plan.parent / ('controle-' + mutation + '.json')
            c.salvar_json(path, changed)
            with self.assertRaises(ValueError):
                c.conferir_plano(path)
        with self.assertRaises(ValueError):
            c.protegida(c.RAIZ / 'saidas-locais/captura', 'captura')

    def test_ferramentas_modelo_e_turnos_como_desvios(self):
        self.assertEqual(self.run_capture('ferramenta'), 2)
        self.assertIn('ferramenta', c.ler(self.attempts()[0])['desvios'][0])
        with self.assertRaisesRegex(ValueError, 'desvio previo'):
            self.run_capture('ferramenta', continuar=True)
        parsed = c.extrair_eventos(b'{"type":"thread.started","thread_id":"x"}\n'
                                  b'{"type":"turn.started"}\n{"type":"turn.started"}\n'
                                  b'{"type":"metadata","model":"gpt-6.1-sol"}\n')
        self.assertTrue(any('turnos' in d for d in parsed['desvios']))
        self.assertTrue(any('modelo' in d for d in parsed['desvios']))

    def test_avaliacao_separada_pelos_arquivos(self):
        self.assertEqual(self.run_capture('invalida', limite=1), 0)
        with patch.object(c, 'protegida', side_effect=lambda p, zona: c.montagem.sem_links(p)):
            status = c.avaliar_lote(self.case / 'lote', c.RAIZ / 'materiais/modelos/referencia_candidata_NAO_ENVIAR_AO_LLM.json',
                                    self.case / 'avaliados')
        self.assertEqual(status, 1)
        results = list((self.case / 'avaliados').glob('PIL-*/T*/avaliacao.json'))
        result = c.ler(results[0])
        self.assertIsNone(result['testes'])
        self.assertEqual(result['status_avaliacao'], 'resposta_formato_invalido')
        self.assertEqual(result['origem'], 'sintetica')
        summary = c.ler(self.case / 'avaliados/resumo/resumo.json')
        self.assertTrue(summary['completo'])


if __name__ == '__main__':
    unittest.main()
