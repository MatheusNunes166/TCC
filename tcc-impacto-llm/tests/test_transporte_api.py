"""HTTP inteiramente simulado e chave ficticia; nunca consulta a conta/LLM."""
import contextlib
import http.client
import io
import os
from pathlib import Path
import ssl
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch
import urllib.error

import coletor_api as api

KEY = 'CHAVE-FICTICIA-NAO-PERSISTIR'


class TestTransporteAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.root = Path(cls.temp.name)
        with patch.object(api.base, 'protegida', side_effect=lambda p, zona: Path(p)):
            cls.plano = api.preparar(api.base.RAIZ / 'captura/planejamento-piloto-2026-11-07-D38/plano.json',
                                     cls.root / 'plano', 512, '1')

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def setUp(self):
        self.case = tempfile.TemporaryDirectory(dir=self.root)
        self.addCleanup(self.case.cleanup)
        self.out = Path(self.case.name)

    def capture(self, sender, continuar=False):
        with patch.dict(os.environ, OPENAI_API_KEY=KEY), contextlib.redirect_stdout(io.StringIO()), \
                patch.object(api.base, 'protegida', side_effect=lambda p, zona: Path(p)):
            return api.capturar(self.plano, self.out / 'lote', 1, real=True, sender=sender, continuar=continuar)

    def attempt(self):
        return next((self.out / 'lote').glob('PIL-*/T01'))

    def assert_no_key(self, root):
        for path in root.rglob('*'):
            if path.is_file():
                self.assertNotIn(KEY.encode(), path.read_bytes(), str(path))

    def test_incomplete_read_200_com_prefixo_fecha_e_nao_reenvia(self):
        response = Mock(status=200, headers={'x-request-id': 'req-ficticio'})
        response.read.side_effect = [b'prefixo-', http.client.IncompleteRead(b'parcial', 10)]
        with patch.object(api.urllib.request, 'build_opener') as factory:
            factory.return_value.open.return_value = response
            self.assertEqual(self.capture(api.enviar), 2)
            self.assertEqual(factory.return_value.open.call_count, 1)
            with self.assertRaises(ValueError):
                self.capture(api.enviar, continuar=True)
            self.assertEqual(factory.return_value.open.call_count, 1)
        root = self.attempt()
        self.assertEqual((root / 'resposta-http-parcial.bin').read_bytes(), b'prefixo-parcial')
        record = api.base.conferir_fechamento(root)
        self.assertEqual(record['falha_transporte']['tipo'], 'IncompleteRead')
        self.assertEqual(record['http_status'], 200)
        self.assertEqual(record['request_id'], 'req-ficticio')
        self.assertEqual(record['estado_remoto'], 'desconhecido')
        self.assert_no_key(root)

    def test_corpo_http_error_tambem_preserva_incomplete_read(self):
        fp = Mock()
        fp.read.side_effect = [b'erro-', http.client.IncompleteRead(b'cortado', 3)]
        error = urllib.error.HTTPError(api.ENDPOINT, 503, KEY, {'x-request-id': 'req-503'}, fp)
        with patch.object(api.urllib.request, 'build_opener') as factory:
            factory.return_value.open.side_effect = error
            self.assertEqual(self.capture(api.enviar), 2)
            self.assertEqual(factory.return_value.open.call_count, 1)
        record = api.base.conferir_fechamento(self.attempt())
        self.assertEqual(record['http_status'], 503)
        self.assertEqual((self.attempt() / 'resposta-http-parcial.bin').read_bytes(), b'erro-cortado')
        self.assert_no_key(self.attempt())

    def test_eof_antes_de_content_length_e_falha_tecnica(self):
        response = Mock(status=200, headers={'Content-Length': '100'})
        response.read.side_effect = [b'curto', b'']
        with patch.object(api.urllib.request, 'build_opener') as factory:
            factory.return_value.open.return_value = response
            with self.assertRaises(api.FalhaTransporte) as failure:
                api.enviar(b'{}', KEY, 1)
        self.assertEqual(failure.exception.partial, b'curto')
        self.assertEqual(failure.exception.tipo, 'IncompleteRead')

    def test_excecoes_http_oserror_sem_texto_segredo_ou_retry(self):
        errors = [http.client.IncompleteRead(b'fragmento', 8), http.client.RemoteDisconnected(KEY),
                  http.client.BadStatusLine(KEY), ConnectionResetError(KEY), TimeoutError(KEY),
                  ssl.SSLError(KEY), urllib.error.URLError(KEY)]
        original = self.out
        for index, error in enumerate(errors):
            with self.subTest(tipo=type(error).__name__):
                self.out = original / str(index)
                sender = Mock(side_effect=error)
                self.assertEqual(self.capture(sender), 2)
                self.assertEqual(sender.call_count, 1)
                self.assertEqual(api.base.ler(self.attempt() / 'tentativa.json')['falha_transporte']['tipo'], type(error).__name__)
                self.assert_no_key(self.out)
        self.out = original

    def test_conexao_incomplete_read_preserva_fragmento_e_fechamento(self):
        sender = Mock(side_effect=http.client.IncompleteRead(b'conexao-cortada', 5))
        with patch.dict(os.environ, OPENAI_API_KEY=KEY), \
                patch.object(api.base, 'protegida', side_effect=lambda p, zona: Path(p)):
            self.assertEqual(api.conexao(self.out / 'conexao', 512, sender=sender), 2)
        self.assertEqual(sender.call_count, 1)
        self.assertEqual((self.out / 'conexao/resposta-http-parcial.bin').read_bytes(), b'conexao-cortada')
        result = api.base.ler(self.out / 'conexao/resultado.json')
        self.assertEqual(result['estado_remoto'], 'desconhecido')
        self.assertFalse(result['incluido_piloto'])
        for entry in api.base.ler(self.out / 'conexao/fechamento.json')['arquivos']:
            self.assertEqual(api.sha((self.out / 'conexao' / entry['arquivo']).read_bytes()), entry['sha256'])
        self.assert_no_key(self.out)

    def test_interrupcao_com_fragmento_em_captura_e_conexao(self):
        interrupt = KeyboardInterrupt(KEY)
        interrupt.partial = b'antes-do-ctrl-c'
        sender = Mock(side_effect=interrupt)
        self.assertEqual(self.capture(sender), 130)
        self.assertTrue(api.base.conferir_fechamento(self.attempt())['falha_transporte']['interrompida'])
        with self.assertRaises(ValueError):
            self.capture(sender, continuar=True)
        self.assertEqual(sender.call_count, 1)
        with patch.dict(os.environ, OPENAI_API_KEY=KEY), \
                patch.object(api.base, 'protegida', side_effect=lambda p, zona: Path(p)):
            self.assertEqual(api.conexao(self.out / 'conexao', 512, sender=sender), 130)
        self.assertEqual((self.out / 'conexao/resposta-http-parcial.bin').read_bytes(), interrupt.partial)
        self.assert_no_key(self.out)

    def test_tls_verificado_headers_sem_segredo_e_um_unico_open(self):
        response = SimpleNamespace(status=200, headers={}, read=io.BytesIO(b'corpo original\r\n').read, close=lambda: None)
        with patch.object(api.urllib.request, 'build_opener') as factory:
            factory.return_value.open.return_value = response
            self.assertEqual(api.enviar(b'{}', KEY, 1), (200, b'corpo original\r\n', None))
            handlers = factory.call_args.args
            https = next(h for h in handlers if isinstance(h, api.urllib.request.HTTPSHandler))
            self.assertTrue(https._context.check_hostname)
            self.assertEqual(https._context.verify_mode, ssl.CERT_REQUIRED)
            self.assertTrue(any(isinstance(h, api.SemRedirecionar) for h in handlers))
            self.assertEqual(next(h for h in handlers if isinstance(h, api.urllib.request.ProxyHandler)).proxies, {})
            request = factory.return_value.open.call_args.args[0]
            self.assertEqual(request.data, b'{}')
            self.assertEqual(request.get_header('Authorization'), 'Bearer ' + KEY)
            self.assertEqual(factory.return_value.open.call_count, 1)
        api.guardar_requisicao(self.out, b'{}')
        saved = api.base.ler(self.out / 'http-requisicao.json')
        self.assertFalse(any(k.lower() == 'authorization' for k in saved['headers']))
        self.assertEqual((self.out / 'requisicao.json').read_bytes(), b'{}')
        self.assert_no_key(self.out)

    def test_defeito_de_programacao_nao_vira_falha_de_transporte(self):
        for error in (TypeError('CONTROLE defeito'), ValueError('CONTROLE defeito')):
            with self.assertRaises(type(error)):
                api.obter_http(Mock(side_effect=error), b'{}', KEY, 1)

    def test_ajuda_simulacao_preparacao_nao_leem_chave_ou_enviam(self):
        with patch.object(api, 'chave_api', side_effect=AssertionError('chave proibida')), \
                patch.object(api.urllib.request, 'build_opener', side_effect=AssertionError('rede proibida')), \
                contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(api.main(['simular', '--plano', str(self.plano)]), 0)
            with self.assertRaises(SystemExit) as code:
                api.main(['--help'])
            self.assertEqual(code.exception.code, 0)
            with patch.object(api.base, 'protegida', side_effect=lambda p, zona: Path(p)):
                api.preparar(api.base.RAIZ / 'captura/planejamento-piloto-2026-11-07-D38/plano.json',
                             self.out / 'plano-offline', 512, '1')


if __name__ == '__main__':
    unittest.main()
