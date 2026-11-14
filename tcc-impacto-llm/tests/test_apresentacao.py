"""Controles locais da apresentação. Fixtures artificiais; nenhuma chamada à API."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

import apresentar as demo


def serial(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False), encoding='utf-8')


class TestLeituraApresentacao(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        reference = self.root / demo.REFERENCE
        serial(reference, {'versao': 'ARTIFICIAL', 'catalogo': []})
        self.reference_hash = hashlib.sha256(reference.read_bytes()).hexdigest()
        self.evaluations = []
        for cohort, (_, batch_name, evaluation_name) in demo.COHORTS.items():
            batch, evaluated = self.root / batch_name, self.root / evaluation_name
            identity = 'ARTIFICIAL-' + cohort
            note = 'N02' if cohort == 'notas' else None
            payload = 'ARTIFICIAL: tarefa sem respostas.'
            response = b'{"requisitos":[],"testes":[]}'
            obs = {'observacao_id': identity, 'payload_sha256': demo.sha(payload.encode()),
                   'mudanca': 'MC-04-v2', 'condicao': 'D1', 'repeticao': 1}
            if note:
                obs['nota_id'] = note
            serial(batch / 'plano-original.json', {'referencia_sha256': self.reference_hash, 'observacoes': [obs]})
            serial(evaluated / 'descritivo-pendente.json', {'origem': 'ARTIFICIAL'})
            attempt = batch / identity / 'T01'
            assessment = evaluated / identity / 'T01'
            serial(attempt / 'tentativa.json', {'observacao_id': identity,
                'resposta_sha256': demo.sha(response), 'modelo_reportado': 'MODELO_FICTICIO',
                'estado_tecnico': 'concluida', 'instante_execucao': 'DATA_ARTIFICIAL'})
            serial(attempt / 'requisicao.json', {'input': payload, 'tools': [], 'tool_choice': 'none'})
            (attempt / 'resposta.bin').write_bytes(response)
            serial(assessment / 'avaliacao.json', {'observacao_id': identity, 'nota_id': note,
                'referencia': {'sha256': self.reference_hash}, 'requisitos': {}, 'testes': {},
                'formato_contrato': 'valido'})
            (assessment / 'resposta-original.bin').write_bytes(response)
            self.evaluations.append(assessment / 'avaliacao.json')

    def test_preserva_coorte_nota_e_resposta_original_sem_reavaliar(self):
        records, hashes, reports = demo.ler_capturas(self.root)
        self.assertEqual([r['coorte'] for r in records], ['comparacao', 'notas'])
        self.assertEqual([r['nota'] for r in records], [None, 'N02'])
        self.assertEqual(records[1]['resposta'], '{"requisitos":[],"testes":[]}')
        self.assertEqual(set(reports), {'comparacao', 'notas'})
        self.assertGreater(len(hashes), 8)

    def test_recusa_nota_trocada_na_avaliacao(self):
        path = self.evaluations[1]
        value = json.loads(path.read_text())
        value['nota_id'] = 'N01'
        serial(path, value)
        with self.assertRaisesRegex(ValueError, 'nota divergente'):
            demo.ler_capturas(self.root)

    def test_recusa_referencia_alterada(self):
        (self.root / demo.REFERENCE).write_text('{}')
        with self.assertRaisesRegex(ValueError, 'Referência atual difere'):
            demo.ler_capturas(self.root)

    def test_recusa_resposta_original_alterada(self):
        path = self.evaluations[0].with_name('resposta-original.bin')
        path.write_bytes(b'ARTIFICIAL: resposta diferente')
        with self.assertRaisesRegex(ValueError, 'Resposta original divergente'):
            demo.ler_capturas(self.root)

    def test_caminho_fora_do_projeto_e_recusado(self):
        with self.assertRaisesRegex(ValueError, 'fora do projeto'):
            demo.arquivo(self.root, '../fora')


class TestLimpezaApresentacao(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        subprocess.run(['git', 'init', '-q', str(self.root)], check=True, capture_output=True)
        (self.root / '__pycache__').mkdir()
        (self.root / '__pycache__/ARTIFICIAL.pyc').write_bytes(b'ARTIFICIAL')
        (self.root / 'captura').mkdir()
        (self.root / 'captura/registro.json').write_bytes(b'{"origem":"ARTIFICIAL"}')

    def test_previa_nao_remove_e_aplicacao_preserva_capturas(self):
        preview = demo.limpar_caches(self.root)
        self.assertEqual(preview['removidos'], [])
        self.assertTrue((self.root / '__pycache__').exists())
        applied = demo.limpar_caches(self.root, True)
        self.assertEqual(applied['removidos'], ['__pycache__'])
        self.assertEqual((self.root / 'captura/registro.json').read_bytes(), b'{"origem":"ARTIFICIAL"}')

    def test_cache_rastreado_nao_e_removido(self):
        subprocess.run(['git', 'add', '__pycache__/ARTIFICIAL.pyc'], cwd=self.root, check=True, capture_output=True)
        with self.assertRaisesRegex(ValueError, 'não rastreado'):
            demo.limpar_caches(self.root, True)
        self.assertTrue((self.root / '__pycache__/ARTIFICIAL.pyc').exists())

    def test_link_de_cache_nao_e_seguido(self):
        target = self.root / '.ruff_cache'
        try:
            target.symlink_to(self.root / 'captura', target_is_directory=True)
        except OSError as exc:
            self.skipTest('Ambiente não permite criar symlink: ' + str(exc))
        with self.assertRaisesRegex(ValueError, 'link/junction'):
            demo.limpar_caches(self.root, True)
        self.assertTrue((self.root / 'captura/registro.json').exists())


class TestExecucaoOffline(unittest.TestCase):
    def test_comando_verificar_nao_gera_painel_ou_arquivos(self):
        before = sorted(p.relative_to(demo.ROOT).as_posix()
                        for p in (demo.ROOT / 'apresentacao').rglob('*'))
        result = demo.executar_local(demo.ROOT,
            "import runpy; sys.argv=['apresentar.py','verificar']; "
            "runpy.run_path('apresentar.py',run_name='__main__')")
        self.assertEqual(result.returncode, 0, result.stderr.decode('utf-8'))
        output = result.stdout.decode('utf-8')
        self.assertIn('75/75', output)
        self.assertIn('64 + 16', output)
        after = sorted(p.relative_to(demo.ROOT).as_posix()
                       for p in (demo.ROOT / 'apresentacao').rglob('*'))
        self.assertEqual(before, after)

    def test_subprocesso_bloqueia_rede(self):
        result = demo.executar_local(demo.ROOT, "import socket; socket.create_connection(('127.0.0.1',9))")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('rede bloqueada', result.stderr.decode('utf-8'))

    def test_chave_nao_e_repassada_ao_subprocesso(self):
        with patch.dict(os.environ, {'OPENAI_API_KEY': 'FICTICIA_NAO_REAL'}):
            result = demo.executar_local(demo.ROOT, "import os; print('OPENAI_API_KEY' in os.environ)")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout.strip(), b'False')


if __name__ == '__main__':
    unittest.main()
