"""D-46: controles offline de separacao dos fatores, integridade e fronteira."""
import contextlib
import copy
import io
from pathlib import Path
import shutil
import socket
import tempfile
import unittest
from unittest.mock import patch

import preparar_bloco_notas as b


class TestBlocoNotas(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.root = Path(cls.temp.name)
        with (patch.object(b.api.base, 'protegida', side_effect=lambda p, z: Path(p)),
              patch.object(b.api, 'chave_api', side_effect=AssertionError('chave proibida')),
              patch.object(b.api, 'enviar', side_effect=AssertionError('envio proibido')),
              patch.object(socket, 'create_connection', side_effect=AssertionError('rede proibida')),
              patch.object(socket, 'getaddrinfo', side_effect=AssertionError('DNS proibido'))):
            cls.plan = b.preparar(cls.root / 'preparacao')

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def setUp(self):
        self.case = tempfile.TemporaryDirectory(dir=self.root)
        self.addCleanup(self.case.cleanup)
        self.out = Path(self.case.name) / 'bloco'
        shutil.copytree(self.plan.parent, self.out)
        self.path = self.out / 'plano.json'

    def reassinar(self, changed):
        manifest = b.api.base.ler(self.out / 'manifesto-bloco.json')
        for e in manifest['arquivos']:
            if e['arquivo'] in changed:
                e['sha256'] = b.api.sha((self.out / e['arquivo']).read_bytes())
        (self.out / 'manifesto-bloco.json').write_bytes(b.api.bytes_json(manifest))

    def test_desenho_16_8_celulas_e_texto_igual_entre_modelos(self):
        result = b.conferir(self.path)
        self.assertEqual((result['N_planejado'], result['celulas'], result['repeticoes_por_celula']), (16, 8, 2))
        self.assertEqual((result['preparacoes'], result['payloads_unicos'], result['executadas']), (8, 4, 0))
        self.assertFalse(result['envio_autorizado'])
        plan = b.api.base.ler(self.path)
        for bloco in (1, 2):
            cells = {(r['modelo'], r['condicao'], r['nota_id']) for r in plan['observacoes'] if r['bloco'] == bloco}
            self.assertEqual(cells, {(m, c, n) for m in b.MODELOS for c in b.CONDICOES for n in b.NOTAS})

    def test_par_preserva_base_e_diferenca_somente_na_afirmacao(self):
        _, originals, _, notes = b.fontes_base()
        baseline = originals[b.MODELOS[0], 'D1']['notas.md']
        for n in b.NOTAS:
            self.assertEqual(notes[n], baseline[:-1] + b' ' + b.FRASES[n].encode() + b'\n')
        diffs = b.api.base.ler(self.out / 'diferencas-payloads.json')['comparacoes']
        self.assertEqual(len(diffs), 8)
        self.assertEqual([d['documentos_diferentes'] for d in diffs if d['tipo'] == 'nota'], [['notas.md']] * 4)
        self.assertEqual([d['documentos_diferentes'] for d in diffs if d['tipo'] == 'estrutura'], [['pedido.txt']] * 4)

    def test_requisicoes_sem_rotulos_historico_gabarito_ou_ferramentas(self):
        for cond in b.CONDICOES:
            for note in b.NOTAS:
                reqs = [b.api.base.ler(self.out / 'requisicoes' / m / f'{cond}-{note}.json') for m in b.MODELOS]
                for req in reqs:
                    self.assertEqual(set(req), {'model', 'input', 'reasoning', 'max_output_tokens', 'tools', 'tool_choice', 'store', 'stream'})
                    self.assertEqual(req['tools'], [])
                    self.assertEqual(req['tool_choice'], 'none')
                    self.assertEqual(req['reasoning'], {'effort': 'medium'})
                    self.assertEqual(req['max_output_tokens'], 4096)
                    self.assertNotIn(note, req['input'])
                    self.assertNotIn(b.REFHASH, req['input'])
                    self.assertNotIn('mapa_notas_privado', req['input'])
                left, right = (copy.deepcopy(r) for r in reqs)
                left.pop('model'); right.pop('model')
                self.assertEqual(left, right)

    def test_recusa_input_adicional_mesmo_com_hash_externo_recalculado(self):
        path = self.out / 'requisicoes' / b.MODELOS[0] / 'D1-N01.json'
        req = b.api.base.ler(path)
        req['input'] += '\nAVISO EXCLUSIVO ARTIFICIAL'
        path.write_bytes(b.api.bytes_json(req))
        self.reassinar([path.relative_to(self.out).as_posix()])
        with self.assertRaisesRegex(ValueError, 'requisicao divergente'):
            b.conferir(self.path)

    def test_recusa_mistura_de_notas_nas_repeticoes(self):
        plan = b.api.base.ler(self.path)
        plan['observacoes'][0]['nota_id'] = 'N02' if plan['observacoes'][0]['nota_id'] == 'N01' else 'N01'
        self.path.write_bytes(b.api.bytes_json(plan))
        self.reassinar(['plano.json'])
        with self.assertRaisesRegex(ValueError, 'identidade/fator/repeticao alterado'):
            b.conferir(self.path)

    def test_recusa_pacote_alterado_mesmo_com_hash_externo_recalculado(self):
        path = self.out / 'pacotes' / b.MODELOS[0] / 'D1-N01/notas.md'
        path.write_bytes(path.read_bytes() + b'AVISO ARTIFICIAL\n')
        self.reassinar([path.relative_to(self.out).as_posix()])
        with self.assertRaisesRegex(ValueError, 'pacote/autorizacao diferente'):
            b.conferir(self.path)

    def test_nao_sobrescreve_saida_e_nao_herda_autorizacao(self):
        before = self.path.read_bytes()
        with patch.object(b.api.base, 'protegida', side_effect=lambda p, z: Path(p)):
            with self.assertRaisesRegex(ValueError, 'saida existente'):
                b.preparar(self.out)
        self.assertEqual(self.path.read_bytes(), before)
        with self.assertRaises(SystemExit) as error, contextlib.redirect_stderr(io.StringIO()):
            b.main(['iniciar'])
        self.assertEqual(error.exception.code, 2)
        with self.assertRaises(ValueError):
            b.ext.conferir(self.path)


if __name__ == '__main__':
    unittest.main()
