"""Controles SINTÉTICOS do verificador; não são os 48 pares reais."""
import copy
import json
import pathlib
import tempfile
import types
import unittest
from unittest import mock

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


class TestMatriz(unittest.TestCase):
    def setUp(self):
        self.ref = json.loads((ROOT / v.REFERENCE).read_text(encoding='utf-8-sig'))
        self.rows = v.make_records(self.ref, 'sintetico')

    def test_motivo_diferente_e_retorno_malformado(self):
        row = self.rows['variantes'][0]
        v.observe(row, lambda *args: {'decisao': 'negar', 'motivo': 'conflito'})
        self.assertEqual(row['estado'], 'divergente')
        self.assertEqual(row['diferencas'], ['motivo'])
        for result in (None, {'decisao': 'negar'}, {'decisao': 'negar', 'motivo': 'estado', 'extra': 1},
                       {'decisao': 'x', 'motivo': 'estado'}, object()):
            with self.subTest(result=result):
                v.observe(row, lambda *args: result)
                self.assertEqual(row['estado'], 'erro')
                self.assertIsNone(row['observado'])
                self.assertIsNotNone(row['observado_bruto'])

    def test_48_entradas_esperados_e_sem_filtro(self):
        calls = []
        def factory(change):
            # Instrumentação SINTÉTICA: respostas controladas, não política real.
            expected = next(m['expected'] for m in self.ref['mudancas'] if m['id'] == change)
            iterator = iter(self.ref['catalogo'])
            def controlled(*args):
                case = next(iterator)
                calls.append((change, case['id'], args))
                return copy.deepcopy(expected[case['id']])
            return controlled
        functions = {m: factory(m) for m in v.VARIANTS}
        baseline = {c['id']: c['esperado'] for c in self.ref['catalogo']}
        v.run_matrix(self.rows['variantes'], functions, baseline)
        self.assertEqual(len(calls), 48)
        self.assertIn(('MC-03', 'T12'), [(m, t) for m, t, args in calls])
        for change in v.VARIANTS:
            self.assertEqual([args for m, t, args in calls if m == change],
                             [(c['estado'], frozenset(c['papeis']), c['operacao']) for c in self.ref['catalogo']])
        self.assertEqual(v.summarize(self.rows['variantes'])['conformes'], 48)

    def test_fonte_invalida_e_erro_individual(self):
        count = 0
        def failing(*args):
            nonlocal count
            count += 1
            raise RuntimeError('falha sintética')
        v.run_matrix(self.rows['variantes'], {'MC-01': failing}, {})
        summary = v.summarize(self.rows['variantes'])
        self.assertEqual((count, summary['erros'], summary['nao_executados']), (12, 12, 36))
        self.assertTrue(all(r['observado'] is None for r in self.rows['variantes']))

    def test_baseline_invalida_bloqueia_todas(self):
        called = []
        v.run_matrix(self.rows['variantes'], {m: lambda *args: called.append(args) for m in v.VARIANTS}, {}, baseline_ok=False)
        self.assertEqual(called, [])
        self.assertEqual(v.summarize(self.rows['variantes'])['nao_executados'], 48)
        self.assertTrue(all(r['erro'] == 'baseline_invalida' for r in self.rows['variantes']))

    def test_efeitos_e_chaves_unicas(self):
        row = next(r for r in self.rows['variantes'] if (r['mudanca'], r['teste']) == ('MC-04-v2', 'T07'))
        v.observe(row, lambda *args: {'decisao': 'negar', 'motivo': 'sem_permissao'},
                  baseline={'decisao': 'negar', 'motivo': 'conflito'})
        self.assertEqual((row['efeito_esperado'], row['efeito_observado'], row['estado']), ('mudou', 'mudou', 'conforme'))
        for bad in (self.rows['variantes'] + [row], self.rows['variantes'][:-1]):
            with self.assertRaises(v.VerificationError):
                v.summarize(bad)
        self.rows['variantes'][0]['teste'] = 'T99'
        with self.assertRaises(v.VerificationError):
            v.summarize(self.rows['variantes'])


class TestInterface(unittest.TestCase):
    """Falhas injetadas somente em cópias temporárias e respostas controladas."""
    @classmethod
    def setUpClass(cls):
        git = v.GitSource(ROOT)
        cls.sources = {name: git.read(name) for name in v.SOURCE_FILES}

    def fixture(self, root, mode='ok', name='tentativa', previous=None):
        for relative, (data, blob) in self.sources.items():
            path = root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
        for relative in (*v.VARIANTS.values(), 'variantes/procedencia.json',
                         'verificacao_variantes.py', 'tests/test_variantes.py'):
            path = root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes((ROOT / relative).read_bytes())
        reference = json.loads(self.sources[v.REFERENCE][0])
        sources = copy.deepcopy(self.sources)
        if mode == 'referencia_invalida':
            broken = copy.deepcopy(reference)
            broken['mudancas'][0]['expected'].pop('T12')
            sources[v.REFERENCE] = (json.dumps(broken).encode(), 'blob_sintetico')
        if mode == 'fonte_invalida':
            path = root / 'variantes/mc01.py'
            path.write_bytes(path.read_bytes() + b'\n# alteracao sintetica extra\n')
        class FakeGit:
            project = root
            prefix = 'tcc-impacto-llm/'
            def __init__(self):
                self.root = root.parent
            def read(self, name):
                return sources[name]
            def command(self, *args):
                return b'commit_sintetico\n' if args == ('rev-parse', 'HEAD') else b''
        def loader(path, digest, execution_id):
            change = next((m for m, rel in v.VARIANTS.items() if path.name == pathlib.Path(rel).name), 'BASELINE')
            def controlled(state, roles, operation):
                case = next(c for c in reference['catalogo'] if (c['estado'], frozenset(c['papeis']), c['operacao']) == (state, roles, operation))
                if mode == 'interrupcao' and change == 'MC-01' and case['id'] == 'T02':
                    raise KeyboardInterrupt()
                if mode == 'erro_par' and change == 'MC-01' and case['id'] == 'T01':
                    raise RuntimeError('erro sintético')
                if mode == 'retorno_invalido' and change == 'MC-01' and case['id'] == 'T01':
                    return object()
                if mode == 'baseline_divergente' and change == 'BASELINE' and case['id'] == 'T01':
                    return {'decisao': 'negar', 'motivo': 'conflito'}
                if mode == 'divergente' and change == 'MC-01' and case['id'] == 'T01':
                    return {'decisao': 'negar', 'motivo': 'conflito'}
                if change == 'BASELINE':
                    return copy.deepcopy(case['esperado'])
                return copy.deepcopy(next(m for m in reference['mudancas'] if m['id'] == change)['expected'][case['id']])
            return types.SimpleNamespace(autorizar=controlled, __file__=str(path), __loader__=object())
        suite = dict(conforme=mode != 'suite_invalida', retorno=0, metodos_descobertos=18)
        def baseline_suite(snapshot, output):
            for name in ('baseline-unittest.txt', 'baseline-stdout.txt', 'baseline-stderr.txt'):
                (output / name).write_text('CONTROLE SINTÉTICO, não execução real\n', encoding='utf-8')
            return suite
        original_manifest = v.new_manifest
        def manifest(*args):
            result = original_manifest(*args)
            result['tipo'] = 'controle_sintetico'
            return result
        with mock.patch.object(v, 'GitSource', return_value=FakeGit()), \
             mock.patch.object(v, 'load_source', side_effect=loader), \
             mock.patch.object(v, 'run_baseline_suite', side_effect=baseline_suite), \
             mock.patch.object(v, 'new_manifest', side_effect=manifest):
            return v.execute_attempt(root, root / f'evidencias/spec003/{name}',
                                     command=['SINTETICO', mode], retentativa_de=previous)

    def test_codigos_0_1_2_e_prioridade(self):
        for mode, code in (('ok', 0), ('divergente', 1), ('erro_par', 2), ('retorno_invalido', 2),
                           ('fonte_invalida', 2), ('baseline_divergente', 2), ('suite_invalida', 2),
                           ('referencia_invalida', 2), ('interrupcao', 2)):
            with self.subTest(mode=mode), tempfile.TemporaryDirectory() as temp:
                root = pathlib.Path(temp)
                manifest, rows = self.fixture(root, mode)
                self.assertEqual(v.result_code(manifest, rows), code)
                output = root / 'evidencias/spec003/tentativa'
                v.finalize_attempt(output, manifest, rows)
                self.assertEqual(json.loads((output / 'manifesto.json').read_text(encoding='utf-8'))['codigo_saida'], code)
                self.assertTrue((output / 'resultados-originais.json').exists())
                self.assertEqual(manifest['revisao_cientifica'], 'pendente')
                self.assertFalse(manifest['piloto_liberado'])
                if mode in ('baseline_divergente', 'suite_invalida'):
                    self.assertEqual(manifest['resumo']['nao_executados'], 48)
                if mode == 'fonte_invalida':
                    self.assertEqual(manifest['resumo']['nao_executados'], 12)
                if mode == 'referencia_invalida':
                    self.assertEqual(rows['variantes'], [])
                if mode == 'interrupcao':
                    self.assertEqual(manifest['estado'], 'interrompida')
                    self.assertEqual(manifest['resumo']['conformes'], 1)

    def test_retentar_preserva_primeira_e_diagnostico(self):
        with tempfile.TemporaryDirectory() as temp:
            root = pathlib.Path(temp)
            manifest, rows = self.fixture(root, 'divergente')
            output = root / 'evidencias/spec003/tentativa'
            v.finalize_attempt(output, manifest, rows)
            original = (output / 'resultados-originais.json').read_bytes()
            original_rows = json.loads(original)
            divergent = next(r for r in rows['variantes'] if r['estado'] == 'divergente')
            self.assertEqual(divergent['diagnostico']['estado'], 'pendente')
            self.assertEqual(divergent['esperado'], original_rows['variantes'][0]['esperado'])
            self.assertEqual(divergent['observado'], original_rows['variantes'][0]['observado'])
            new_manifest, new_rows = self.fixture(root, 'ok', 'nova', 'tentativa')
            v.finalize_attempt(root / 'evidencias/spec003/nova', new_manifest, new_rows)
            self.assertEqual(new_manifest['retentativa_de'], 'tentativa')
            self.assertEqual((output / 'resultados-originais.json').read_bytes(), original)
            with self.assertRaises(v.VerificationError):
                v.create_output(root, output)

    def test_falha_de_escrita_nao_pode_retornar_sucesso(self):
        with tempfile.TemporaryDirectory() as temp:
            root = pathlib.Path(temp)
            manifest, rows = self.fixture(root)
            with mock.patch.object(v, 'save_json', side_effect=OSError('disco sintético indisponível')):
                with self.assertRaises(OSError):
                    v.finalize_attempt(root / 'evidencias/spec003/tentativa', manifest, rows)
            target = root / 'atomico.json'
            target.write_text('original', encoding='utf-8')
            with mock.patch.object(pathlib.Path, 'replace', side_effect=OSError('falha de rename')):
                with self.assertRaises(OSError):
                    v.save_json(target, {'novo': True})
            self.assertEqual(target.read_text(), 'original')

    def test_duplicata_integridade_e_cli_restrita(self):
        with tempfile.TemporaryDirectory() as temp:
            manifest, rows = self.fixture(pathlib.Path(temp))
            rows['variantes'].append(copy.deepcopy(rows['variantes'][0]))
            self.assertEqual(v.result_code(manifest, rows), 2)
        for args in ([], ['--saida', 'x', '--baseline', 'HEAD'], ['--saida', 'x', '--atualizar-gabarito']):
            with self.subTest(args=args), mock.patch('sys.stderr', new=__import__('io').StringIO()):
                self.assertEqual(v.main(args), 2)

    def test_log_ausente_impede_fechamento_conforme(self):
        with tempfile.TemporaryDirectory() as temp:
            root = pathlib.Path(temp)
            manifest, rows = self.fixture(root)
            output = root / 'evidencias/spec003/tentativa'
            (output / 'baseline-unittest.txt').unlink()
            self.assertEqual(v.finalize_attempt(output, manifest, rows), 2)
            self.assertFalse(manifest['conclusao']['conforme'])

    def test_fonte_alterada_apos_execucao_impede_fechamento(self):
        with tempfile.TemporaryDirectory() as temp:
            root = pathlib.Path(temp)
            manifest, rows = self.fixture(root)
            path = root / 'evidencias/spec003/tentativa/fontes/variantes/mc04.py'
            path.write_bytes(path.read_bytes() + b'\n# adulteracao sintetica\n')
            self.assertEqual(v.finalize_attempt(path.parents[2], manifest, rows), 2)
            self.assertFalse(manifest['integridade'])


if __name__ == '__main__':
    unittest.main()
