"""Controles D-38 offline: nunca inicia Codex, HTTP ou modelo."""
import contextlib
import io
from pathlib import Path
import subprocess
import unittest
from unittest.mock import patch

import coletor_piloto as c


class TestControlesCLI(unittest.TestCase):
    def test_argv_configura_somente_chaves_conferidas_sem_prompts_extras(self):
        argv = c.comando_codex('codex', 'ambiente-vazio')
        overrides = [argv[i+1] for i, word in enumerate(argv[:-1]) if word == '-c']
        self.assertEqual(overrides, c.overrides_cli())
        config = dict(c.CONFIG_CLI)
        self.assertEqual(config['model_provider'], 'openai')
        self.assertEqual(config['forced_login_method'], 'chatgpt')
        self.assertFalse(config['skills.include_instructions'])
        self.assertFalse(config['memories.use_memories'])
        self.assertFalse(config['memories.generate_memories'])
        self.assertIn('--strict-config', argv)
        self.assertIn('--ignore-user-config', argv)
        self.assertIn('--ignore-rules', argv)
        self.assertEqual(argv[-1], '-')
        self.assertEqual(argv[argv.index('--model')+1], 'gpt-6-sol')
        self.assertNotIn('resume', argv)
        self.assertNotIn('fork', argv)
        self.assertFalse(any('request_max_retries=' in s or 'stream_max_retries=' in s for s in argv))

    def test_configuracao_nao_promove_false_a_indisponibilidade(self):
        config = c.configuracao_fixa()
        self.assertFalse(config['ferramentas_desativadas_verificado'])
        self.assertFalse(config['retentativas_cliente']['garantia_zero_retries'])
        self.assertIsNone(config['retentativas_cliente']['request_max_retries'])
        self.assertIsNone(config['retentativas_cliente']['stream_max_retries'])
        self.assertEqual(config['configuracoes_cli_solicitadas'], dict(c.CONFIG_CLI))

    def test_trava_nao_e_liberada_esvaziando_lista_de_bloqueios(self):
        with patch.object(c, 'BLOQUEIOS', []), patch.object(subprocess, 'Popen', side_effect=AssertionError('proibido')):
            with self.assertRaisesRegex(ValueError, 'ENVIO REAL BLOQUEADO'):
                c.verificar_liberacao_real()

    def test_erro_recuperado_nao_cria_turno_ou_gera_retry_de_final(self):
        events = [
            {'type': 'thread.started', 'thread_id': 'CONTROLE-LOCAL'},
            {'type': 'turn.started'},
            {'type': 'error', 'message': 'CONTROLE reconectando; sem HTTP/modelo'},
            {'type': 'item.completed', 'item': {'type': 'agent_message', 'text': ' \r\n{"requisitos":[],"testes":[]}\r\n'}},
            {'type': 'turn.completed'},
        ]
        parsed = c.extrair_eventos(b''.join(c.serial(e).replace(b'\n', b'') + b'\n' for e in events))
        self.assertTrue(parsed['completo'])
        self.assertEqual(parsed['turnos_iniciados_observados'], 1)
        self.assertEqual(parsed['erros_cliente_observados'], 1)
        self.assertIsNone(parsed['retentativas_transporte_observadas'])
        self.assertEqual(parsed['resposta'], b' \r\n{"requisitos":[],"testes":[]}\r\n')
        self.assertTrue(parsed['desvios'])


if __name__ == '__main__':
    unittest.main()
