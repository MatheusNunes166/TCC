"""Controles SINTÉTICOS do verificador; não são os 48 pares reais."""
import copy
import json
import pathlib
import tempfile
import unittest

import verificacao_variantes as v


ROOT = pathlib.Path(__file__).resolve().parents[1]


class TestFundacao(unittest.TestCase):
    def setUp(self):
        self.reference = json.loads((ROOT / v.REFERENCE).read_text(encoding='utf-8-sig'))

    def test_git_bytes_e_commit_ausente(self):
        git = v.GitSource(ROOT)
        data, blob = git.read('autorizacao.py')
        self.assertIsInstance(data, bytes)
        self.assertEqual(blob, 'c219b9ab1f2ed75a92664c79009a1a417e75ef11')
        with self.assertRaises(v.VerificationError):
            git.read('autorizacao.py', '0' * 40)

    def test_referencia_invalida(self):
        v.validate_reference(self.reference)
        mutations = [lambda r: r.update(versao='0.1'),
                     lambda r: r['catalogo'].append(copy.deepcopy(r['catalogo'][0])),
                     lambda r: r['catalogo'][0].update(id='T99'),
                     lambda r: r['mudancas'][0]['expected'].pop('T12'),
                     lambda r: r['mudancas'][0]['expected']['T01'].update(motivo='inventado'),
                     lambda r: r['catalogo'][0]['papeis'].append(r['catalogo'][0]['papeis'][0])]
        for change in mutations:
            with self.subTest(change=change):
                ref = copy.deepcopy(self.reference)
                change(ref)
                with self.assertRaises(v.VerificationError):
                    v.validate_reference(ref)

    def test_pasta_repetida_e_interceptacao(self):
        with tempfile.TemporaryDirectory() as temp:
            root = pathlib.Path(temp)
            out = v.create_output(root, root / 'evidencias/spec003/nova')
            (out / 'original').write_bytes(b'preservar')
            for path in (out, root / 'fora', root / 'autorizacao.py', root / v.REFERENCE,
                         root / 'evidencias/spec003', root / 'evidencias/spec003/../escape'):
                with self.subTest(path=path), self.assertRaises(v.VerificationError):
                    v.create_output(root, path)
            self.assertEqual((out / 'original').read_bytes(), b'preservar')

    def test_registros_ausentes_e_persistencia(self):
        rows = v.make_records(self.reference, 'sintetico')
        self.assertEqual(len(rows['baseline']), 12)
        self.assertEqual(len(rows['variantes']), 48)
        self.assertTrue(all(r['observado'] is None and r['estado'] == 'nao_executado'
                            for r in rows['variantes']))
        with tempfile.TemporaryDirectory() as temp:
            path = pathlib.Path(temp) / 'resultados.json'
            v.save_json(path, rows)
            self.assertEqual(json.loads(path.read_text(encoding='utf-8')), rows)


class TestProcedencia(unittest.TestCase):
    def setUp(self):
        self.base, _ = v.GitSource(ROOT).read('autorizacao.py')
        self.sources = {
            'MC-01': self.base.replace(b"(('Consulta', 'visualizar'), ('Auditoria', 'exportar'))",
                                       b"(('Consulta', 'visualizar'),)"),
            'MC-02': self.base.replace(b"return {'Consulta', 'Auditoria'} <= papeis_efetivos", b'return False'),
            'MC-03': self.base.replace(b"(('Consulta', 'visualizar'), ('Auditoria', 'exportar'))",
                                       b"(('Auditoria', 'exportar'),)"),
            'MC-04-v2': self.base.replace("return papeis | frozenset({'Consulta'} if 'Supervisão' in papeis else ())".encode(),
                                          b'return papeis')}

    def test_quatro_edicoes_e_rejeicao_de_extra(self):
        for change, source in self.sources.items():
            with self.subTest(change=change):
                report = v.audit_source(self.base, source, change, v.BASELINE)
                self.assertTrue(report['ast_conforme'])
                self.assertIn('--- B/autorizacao.py', report['diff'])
                for bad in (source + b'\n# extra\n', source.replace(b'operacao: str', b'operacao: int'),
                            self.base, source.replace(b'return papeis', b'return frozenset()')):
                    if bad != source:
                        with self.assertRaises(v.VerificationError):
                            v.audit_source(self.base, bad, change, v.BASELINE)
                with self.assertRaises(v.VerificationError):
                    v.audit_source(self.base, source, change, 'MC-01')
        chained = self.sources['MC-01'].replace(b"return {'Consulta', 'Auditoria'} <= papeis_efetivos", b'return False')
        with self.assertRaises(v.VerificationError):
            v.audit_source(self.base, chained, 'MC-02', v.BASELINE)

    def test_loader_confere_caminho_hash_e_cache(self):
        with tempfile.TemporaryDirectory() as temp:
            path = pathlib.Path(temp) / 'fonte.py'
            path.write_bytes(self.base)
            original = __import__('sys').modules.get('autorizacao')
            module = v.load_source(path, v.sha256(self.base), 'sintetico')
            self.assertEqual(path.resolve(), pathlib.Path(module.__file__))
            self.assertEqual(module.autorizar('ativa', frozenset({'Auditoria'}), 'exportar'),
                             {'decisao': 'permitir', 'motivo': 'permissao_direta'})
            self.assertIs(__import__('sys').modules.get('autorizacao'), original)
            with self.assertRaises(v.VerificationError):
                v.load_source(path, '0' * 64, 'sintetico')
            with self.assertRaises((v.VerificationError, FileNotFoundError)):
                v.load_source(path.with_name('ausente.py'), v.sha256(self.base), 'sintetico')
            (path.parent / '__pycache__').mkdir()
            with self.assertRaises(v.VerificationError):
                v.load_source(path, v.sha256(self.base), 'sintetico')


if __name__ == '__main__':
    unittest.main()
