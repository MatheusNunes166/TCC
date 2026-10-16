import itertools
import unittest

import autorizacao


class TestEstado(unittest.TestCase):
    def conferir_estado(self, estado, papeis):
        self.assertEqual(autorizacao.autorizar(estado, frozenset(papeis), 'visualizar'),
                         {'decisao': 'negar', 'motivo': 'estado'})

    def test_T01(self):
        self.conferir_estado('suspensa', {'Consulta'})

    def test_T09(self):
        self.conferir_estado('em_revisao', {'Consulta'})

    def test_T10(self):
        self.conferir_estado('em_revisao', {'Supervisão'})

    def test_T11(self):
        self.conferir_estado('em_revisao', {'Consulta', 'Auditoria'})

    def test_estados_32_combinacoes(self):
        nomes = ('Consulta', 'Auditoria', 'Supervisão')
        for estado, bits, operacao in itertools.product(
                ('suspensa', 'em_revisao'), itertools.product((False, True), repeat=3),
                ('visualizar', 'exportar')):
            papeis = frozenset(p for p, inclui in zip(nomes, bits) if inclui)
            entrada = (estado, papeis, operacao)
            with self.subTest(estado=estado, papeis=papeis, operacao=operacao):
                self.assertEqual(autorizacao.autorizar(*entrada),
                                 {'decisao': 'negar', 'motivo': 'estado'})
                self.assertEqual(entrada, (estado, frozenset(p for p, inclui in zip(nomes, bits) if inclui), operacao))


class TestDiretas(unittest.TestCase):
    def test_T02(self):
        self.assertEqual(autorizacao.autorizar('ativa', frozenset({'Consulta'}), 'visualizar'),
                         {'decisao': 'permitir', 'motivo': 'permissao_direta'})

    def test_T03(self):
        self.assertEqual(autorizacao.autorizar('ativa', frozenset({'Consulta'}), 'exportar'),
                         {'decisao': 'negar', 'motivo': 'sem_permissao'})

    def test_T04(self):
        self.assertEqual(autorizacao.autorizar('ativa', frozenset({'Auditoria'}), 'exportar'),
                         {'decisao': 'permitir', 'motivo': 'permissao_direta'})

    def test_auditoria_visualizar(self):
        self.assertEqual(autorizacao.autorizar('ativa', frozenset({'Auditoria'}), 'visualizar'),
                         {'decisao': 'negar', 'motivo': 'sem_permissao'})

    def test_concessoes_proprias(self):
        for papel, esperado in (
                ('Consulta', frozenset({'visualizar'})),
                ('Auditoria', frozenset({'exportar'})),
                ('Supervisão', frozenset())):
            with self.subTest(papel=papel):
                papeis = frozenset({papel})
                resultado = autorizacao.obter_permissoes_diretas(papeis)
                self.assertIsInstance(resultado, frozenset)
                self.assertEqual(resultado, esperado)
                self.assertEqual(papeis, frozenset({papel}))
                self.assertEqual(autorizacao.obter_permissoes_diretas(papeis), esperado)
