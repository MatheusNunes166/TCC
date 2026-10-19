import itertools
import unittest

import autorizacao


class TestHeranca(unittest.TestCase):
    def test_T05(self):
        self.assertEqual(autorizacao.autorizar('ativa', frozenset({'Supervisão'}), 'visualizar'),
                         {'decisao': 'permitir', 'motivo': 'permissao_herdada'})

    def test_T08(self):
        self.assertEqual(autorizacao.autorizar('ativa', frozenset({'Supervisão'}), 'exportar'),
                         {'decisao': 'negar', 'motivo': 'sem_permissao'})

    def test_efetivos_oito_subconjuntos(self):
        for atribuidos, esperado in (
                ((), ()),
                (('Consulta',), ('Consulta',)),
                (('Auditoria',), ('Auditoria',)),
                (('Supervisão',), ('Supervisão', 'Consulta')),
                (('Consulta', 'Auditoria'), ('Consulta', 'Auditoria')),
                (('Consulta', 'Supervisão'), ('Consulta', 'Supervisão')),
                (('Auditoria', 'Supervisão'), ('Consulta', 'Auditoria', 'Supervisão')),
                (('Consulta', 'Auditoria', 'Supervisão'), ('Consulta', 'Auditoria', 'Supervisão'))):
            with self.subTest(atribuidos=atribuidos):
                papeis = frozenset(atribuidos)
                resultado = autorizacao.obter_papeis_efetivos(papeis)
                self.assertIsInstance(resultado, frozenset)
                self.assertEqual(resultado, frozenset(esperado))
                self.assertEqual(papeis, frozenset(atribuidos))
                self.assertEqual(autorizacao.obter_papeis_efetivos(papeis), resultado)


class TestConflito(unittest.TestCase):
    def test_T12(self):
        # RF-03 inclui Consulta efetivo; RF-04 supera exportar direto de RF-02.
        self.assertEqual(autorizacao.autorizar('ativa', frozenset({'Supervisão', 'Auditoria'}), 'exportar'),
                         {'decisao': 'negar', 'motivo': 'conflito'})

    def test_T06(self):
        self.assertEqual(autorizacao.autorizar('ativa', frozenset({'Consulta', 'Auditoria'}), 'visualizar'),
                         {'decisao': 'negar', 'motivo': 'conflito'})

    def test_T07(self):
        self.assertEqual(autorizacao.autorizar('ativa', frozenset({'Supervisão', 'Auditoria'}), 'visualizar'),
                         {'decisao': 'negar', 'motivo': 'conflito'})

    def test_incompatibilidade_oito_subconjuntos(self):
        for nomes, esperado in (
                ((), False),
                (('Consulta',), False),
                (('Auditoria',), False),
                (('Supervisão',), False),
                (('Consulta', 'Auditoria'), True),
                (('Consulta', 'Supervisão'), False),
                (('Auditoria', 'Supervisão'), False),
                (('Consulta', 'Auditoria', 'Supervisão'), True)):
            with self.subTest(efetivos=nomes):
                efetivos = frozenset(nomes)
                resultado = autorizacao.ha_incompatibilidade(efetivos)
                self.assertIs(type(resultado), bool)
                self.assertEqual(resultado, esperado)
                self.assertEqual(efetivos, frozenset(nomes))
                self.assertEqual(autorizacao.ha_incompatibilidade(efetivos), esperado)


class TestBordas(unittest.TestCase):
    def test_vazio_e_prioridade_direta(self):
        for nomes, operacao, esperado in (
                ((), 'visualizar', {'decisao': 'negar', 'motivo': 'sem_permissao'}),
                ((), 'exportar', {'decisao': 'negar', 'motivo': 'sem_permissao'}),
                (('Supervisão', 'Consulta'), 'visualizar',
                 {'decisao': 'permitir', 'motivo': 'permissao_direta'}),
                (('Supervisão', 'Consulta'), 'exportar',
                 {'decisao': 'negar', 'motivo': 'sem_permissao'})):
            with self.subTest(papeis=nomes, operacao=operacao):
                entrada = ('ativa', frozenset(nomes), operacao)
                self.assertEqual(autorizacao.autorizar(*entrada), esperado)
                self.assertEqual(autorizacao.autorizar(*entrada), esperado)
                self.assertEqual(entrada, ('ativa', frozenset(nomes), operacao))


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
