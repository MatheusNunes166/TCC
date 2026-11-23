"""Controles SINTÉTICOS do bloco documental. Transporte externo proibido."""
import collections
import itertools
import json
import multiprocessing
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
import unittest
from unittest.mock import patch
import urllib.error
import urllib.request

import documentacao_operacional as doc
import painel_documental as painel
import painel_llm as antigo
import preparar_documentacao_operacional_v2 as prep
from test_painel_llm import envelope, KEY, TEXT


class TestPreparacao64(unittest.TestCase):
    def test_dezesseis_payloads_64_posicoes_32_celulas_dois_blocos(self):
        payloads, sources, docs = prep.montar()
        plan = prep.plano(payloads, sources)
        rows = plan['observacoes']
        self.assertEqual((len(payloads), len(set(payloads.values())), len(docs), len(rows)), (16, 16, 5, 64))
        self.assertEqual(len({r['observacao_id'] for r in rows}), 64)
        key = lambda r: tuple(r[k] for k in ('mudanca', 'modelo_solicitado', 'condicao', 'documentacao_id'))
        counts = collections.Counter(map(key, rows))
        self.assertEqual((len(counts), set(counts.values())), (32, {2}))
        self.assertEqual(collections.Counter(r['bloco'] for r in rows), {1: 32, 2: 32})
        self.assertEqual({key(r) for r in rows[:32]}, {key(r) for r in rows[32:]})
        self.assertEqual(rows, prep.plano(payloads, sources)['observacoes'])
        for r in rows:
            self.assertEqual(r['payload_sha256'], prep.sha(payloads[Path(r['payload']).stem]))
        self.assertEqual(prep.conferir(prep.ROOT/prep.PASTA)['posicoes'], 64)
        self.assertEqual(prep.anterior.conferir(prep.ROOT/prep.ANTECEDENTE)['observacoes_planejadas'], 32)

    def test_bloco_rf_unico_catalogo_politica_pedidos_notas_literais(self):
        payloads, _, _ = prep.montar()
        profiles = prep.anterior.perfis_preservados(prep.ROOT)
        notes = set()
        for change, cond in itertools.product(prep.MUDANCAS, prep.CONDICOES):
            note = 'sem' if cond.endswith('0') else 'original'
            original = profiles[f'{change}:{cond}:{note}']['payload']
            a = payloads[f'{change}-{cond}-CONSOLIDADA']
            b = payloads[f'{change}-{cond}-OPERACIONAL']
            self.assertEqual(original, a)
            self.assertEqual(prep.anterior.operacionalizar(a)[0], b)
            blocks = dict(prep.anterior.BLOCOS.findall(a.decode()))
            others = dict(prep.anterior.BLOCOS.findall(b.decode()))
            for key, raw in blocks.items():
                if key != 'requisitos-baseline':
                    self.assertEqual(others[key], raw)
            for data in (blocks, others):
                self.assertEqual('notas' in data, cond.endswith('1'))
                if 'notas' in data:
                    notes.add(data['notas'])
                catalog = [line for line in data['catalogo-baseline'].splitlines() if line.startswith('|')]
                self.assertEqual(len(catalog), 17)
                self.assertTrue(all(len(line.split('|')[1:-1]) == 6 for line in catalog))
            for label in ('DOCOP64-', 'CONSOLIDADA', 'OPERACIONAL', 'plano_sha256', 'NAO_ENVIAR_AO_LLM'):
                self.assertNotIn(label.encode(), b)
        self.assertEqual(len(notes), 1)

    def test_preparar_e_conferir_sem_referencia_chave_transporte(self):
        read = Path.read_bytes
        def guarded(path):
            self.assertNotIn('NAO_ENVIAR_AO_LLM', path.name)
            return read(path)
        with tempfile.TemporaryDirectory() as temp, patch.object(Path, 'read_bytes', guarded), \
             patch.object(doc.api, 'enviar', side_effect=AssertionError('API proibida')), \
             patch.object(doc.api, 'chave_api', side_effect=AssertionError('chave proibida')):
            folder = Path(temp)/'novo'
            prep.preparar(folder)
            with self.assertRaises(ValueError):
                prep.preparar(folder)
            file = folder/'payloads/MC-02-E0-OPERACIONAL.txt'
            file.write_bytes(file.read_bytes()+b'alteracao')
            with self.assertRaises(ValueError):
                prep.conferir(folder)


class TestExecucaoDocumental64(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.area = Path(self.temp.name)
        self.calls = []
        guard = patch.object(doc.api, 'enviar', side_effect=AssertionError('API real proibida'))
        guard.start()
        self.addCleanup(guard.stop)

    def sender(self, body, key, timeout):
        self.calls.append((body, key, timeout))
        request = json.loads(body)
        return 200, envelope(model=request['model']), 'req-SINTETICA'

    def app(self, sender=None, chave=None):
        return painel.Aplicacao(sender=sender or self.sender, chave=chave or (lambda: KEY), origem='sintetica',
            area_captura=self.area/'demo', area_avaliacao=self.area/'demo-avaliados',
            area_documental_captura=self.area/'documental', area_documental_avaliacao=self.area/'doc-avaliados')

    def choice(self, app, limit=1, action='acao-sintetica-0001'):
        return {'bloco': doc.COORTE, 'acao_id': action, 'limite': limit,
            'plano_sha256': app.documental.plan_hash, 'manifesto_sha256': app.documental.manifest_hash}

    def finish(self, app, job):
        app.documental.worker.join(60)
        self.assertFalse(app.documental.worker.is_alive())
        return app.job(job['id'])

    def test_abertura_previa_filtros_sem_envio_e_primeira_acao_restrita(self):
        app = self.app()
        self.assertEqual(app.opcoes()['documental']['pendentes'], 64)
        self.assertEqual(len(app.opcoes()['documental']['celulas']), 32)
        self.assertEqual(len(app.resultados()), 80)
        self.assertIn('<<<inicio:sistema>>>', app.perfil('documental-proxima')['payload'])
        self.assertFalse(app.documental.capture.exists())
        with self.assertRaisesRegex(antigo.ErroPainel, 'Primeira'):
            app.iniciar(self.choice(app, 2))
        self.assertFalse(self.calls)
        for extra in ({'modelo': 'outro'}, {'limite': True}, {'plano_sha256': '0'*64}):
            with self.assertRaises(antigo.ErroPainel):
                app.iniciar({**self.choice(app), **extra})

    def test_primeira_captura_depois_avaliacao_e_metadados(self):
        app = self.app()
        evaluate = app.documental.avaliar
        def checked(row):
            folder = app.documental.pasta_observacao(row)
            self.assertTrue((folder/'fechamento.json').exists())
            self.assertTrue((folder/'resposta-http.bin').exists())
            return evaluate(row)
        with patch.object(app.documental, 'avaliar', side_effect=checked):
            job = app.iniciar(self.choice(app))
            done = self.finish(app, job)
        self.assertEqual(done['enviadas'], 1)
        self.assertEqual(len(self.calls), 1)
        row = app.documental.rows[0]
        detail = app.detalhe(row['observacao_id'])
        self.assertEqual(detail['coorte'], doc.COORTE_SINTETICA)
        self.assertEqual(detail['fase'], 'verificacao_sintetica')
        self.assertFalse(detail['id'].startswith('DEMO'))
        for k in doc.FIELDS:
            self.assertEqual(detail[k], row[k])
        self.assertEqual(detail['conformidade_original'], 'pendente')
        request = json.loads(self.calls[0][0])
        self.assertEqual(request['reasoning'], {'effort': 'medium'})
        self.assertEqual(request['max_output_tokens'], 4096)
        self.assertEqual(request['tools'], [])
        self.assertEqual(app.documental.estado()['pendentes'], 63)
        audit = prep.ler(app.documental.capture/'acoes'/(job['id']+'.json'))
        self.assertEqual(audit['limite_solicitado'], 1)
        self.assertFalse(audit['conformidade_aprovada'])
        self.assertIn('+00:00', audit['instante_clique_servidor'])
        for p in self.area.rglob('*'):
            if p.is_file():
                self.assertNotIn(KEY.encode(), p.read_bytes())

    def test_continuidade_reinicio_ordem_64_e_consistencia_sem_mistura(self):
        app = self.app()
        self.finish(app, app.iniciar(self.choice(app)))
        again = self.app()
        self.assertTrue(again.iniciar(self.choice(again))['finalizado'])
        self.assertEqual(len(self.calls), 1)
        done = self.finish(again, again.iniciar(self.choice(again, 63, 'acao-sintetica-restantes')))
        self.assertEqual(done['enviadas'], 63)
        self.assertEqual(len(self.calls), 64)
        self.assertEqual(again.documental.estado()['pendentes'], 0)
        for row, (raw, _, _) in zip(again.documental.rows, self.calls):
            request = json.loads(raw)
            self.assertEqual(request['model'], row['modelo_solicitado'])
            self.assertEqual(prep.sha(request['input'].encode()), row['payload_sha256'])
        cells = again.documental.celulas()
        self.assertEqual(len(cells), 32)
        for cell in cells:
            self.assertEqual(cell['N_planejado'], 2)
            self.assertEqual(cell['N_valido'], 2)
            for dim in ('requisitos', 'testes'):
                self.assertEqual(cell['consistencia_descritiva_pendente'][dim]['numero_pares'], 1)
        self.assertEqual(collections.Counter(r['coorte'] for r in again.resultados()),
                         {'comparacao':64, 'notas':16, doc.COORTE_SINTETICA:64})

    def test_clique_duplicado_concorrencia_entre_instancias_e_processos(self):
        entered, release = threading.Event(), threading.Event()
        def blocked(*args):
            entered.set()
            release.wait(10)
            return self.sender(*args)
        app = self.app(blocked)
        job = app.iniciar(self.choice(app))
        try:
            self.assertTrue(entered.wait(5))
            self.assertEqual(app.iniciar(self.choice(app))['id'], job['id'])
            other = self.app()
            with self.assertRaisesRegex(antigo.ErroPainel, 'andamento'):
                other.iniciar(self.choice(other, action='acao-sintetica-outra'))
            with self.assertRaises(antigo.ErroPainel):
                app.iniciar({'modelo':'gpt-6-sol','perfil_id':'MC-01:D0:sem','acao_id':'acao-demo-sintetica'})
            code = ('from pathlib import Path; from documentacao_operacional import TravaLote; '
                    't=TravaLote(Path(__import__("sys").argv[1])); '
                    'print(t.adquirir(criar=False)); t.liberar()')
            result = subprocess.run([sys.executable, '-B', '-c', code,
                str(app.documental.capture/'.execucao.lock')], capture_output=True, timeout=10)
            self.assertEqual(result.stdout.strip(), b'False', result.stderr)
        finally:
            release.set()
        self.finish(app, job)
        self.assertEqual(len(self.calls), 1)

    def test_fragmento_desconhecido_invalida_divergencia_sem_retry_ou_imputacao(self):
        responses = [lambda: (_ for _ in ()).throw(doc.api.FalhaTransporte('IncompleteRead',
                        partial=b'fragmento SINTETICO', status=200)),
                     lambda: (200, envelope('```json\n'+TEXT+'\n```'), 'req-invalida'),
                     lambda: (200, envelope(model='modelo-reportado-diferente'), 'req-divergente')]
        def sender(*args):
            self.calls.append(args)
            return responses[len(self.calls)-1]()
        app = self.app(sender)
        self.finish(app, app.iniciar(self.choice(app)))
        self.finish(app, app.iniciar(self.choice(app, 5, 'acao-sintetica-invalida')))
        self.assertEqual(len(self.calls), 2)  # Para no formato inválido, não preenche o limite.
        self.finish(app, app.iniciar(self.choice(app, 4, 'acao-sintetica-divergente')))
        self.assertEqual(len(self.calls), 3)
        records = app.documental.registros()
        self.assertEqual(records[0]['estado_remoto'], 'desconhecido')
        self.assertEqual(records[1]['formato'], 'invalido')
        self.assertEqual(records[2]['modelo_reportado'], 'modelo-reportado-diferente')
        self.assertTrue(records[2]['desvios'])
        for r in records[:2]:
            self.assertIsNone(r['requisitos'])
            self.assertIsNone(r['testes'])
        self.assertEqual(app.documental.estado()['pendentes'], 61)
        folder = app.documental.pasta_observacao(app.documental.rows[0])
        self.assertEqual((folder/'resposta-http-parcial.bin').read_bytes(), b'fragmento SINTETICO')

    def test_interrupcao_e_avaliacao_falha_preservam_captura_e_retomada_offline(self):
        app = self.app()
        with patch.object(app.documental, 'avaliar', side_effect=RuntimeError('falha offline')):
            self.finish(app, app.iniciar(self.choice(app)))
        row = app.documental.rows[0]
        self.assertTrue((app.documental.pasta_observacao(row)/'fechamento.json').exists())
        app.documental.avaliar(row)
        self.assertEqual(app.documental.registros()[0]['status_avaliacao'], 'avaliada')
        self.assertEqual(len(self.calls), 1)
        # Reserva interrompida não é pendente e nunca pode ser reenviada.
        app.documental.pasta_observacao(app.documental.rows[1]).mkdir(parents=True)
        self.assertEqual(self.app().documental.previa()['ordem'], 3)
        self.assertEqual(self.app().documental.estado()['interrompidas'], 1)

    def test_tentativa_sem_fechamento_nao_promove_conclusao_ou_pontuacao(self):
        app = self.app()
        self.finish(app, app.iniciar(self.choice(app)))
        row = app.documental.rows[0]
        (app.documental.pasta_observacao(row)/'fechamento.json').unlink()
        state = app.documental.estado()
        self.assertEqual(state['interrompidas'], 1)
        self.assertEqual(state['concluidas'], 0)
        record = app.documental.registros()[0]
        self.assertEqual(record['estado'], 'interrompida')
        self.assertIsNone(record['requisitos'])
        self.assertEqual(app.documental.previa()['ordem'], 2)

    def test_http_interface_fluxo_completo_artificial_e_post_perdido(self):
        app = self.app()
        server = antigo.ThreadingHTTPServer(('127.0.0.1', 0), antigo.handler(app))
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        def shutdown():
            server.shutdown();server.server_close();thread.join(3)
        self.addCleanup(shutdown)
        url = 'http://127.0.0.1:' + str(server.server_address[1])
        headers = {'X-TCC-Token': app.token, 'Content-Type':'application/json'}
        def call(path, data=None):
            req = urllib.request.Request(url+path, headers=headers,
                data=doc.api.bytes_json(data) if data is not None else None)
            with urllib.request.urlopen(req, timeout=10) as response:
                return json.load(response)
        with urllib.request.urlopen(url+'/', timeout=5) as response:
            html = response.read().decode()
            self.assertIn('Pesquisa documental', html)
            self.assertNotIn(KEY, html)
        call('/api/opcoes');call('/api/perfil/documental-proxima');call('/api/resultados')
        self.assertFalse(self.calls)
        choice = self.choice(app)
        job = call('/api/executar', choice)  # Resposta do POST considerada perdida pelo navegador.
        self.finish(app, job)
        self.assertEqual(call('/api/executar', choice)['id'], job['id'])
        self.assertEqual(call('/api/opcoes')['documental']['pendentes'], 63)
        job = call('/api/executar', self.choice(app, 2, 'acao-sintetica-http-2'))
        self.finish(app, job)
        self.assertEqual(len(self.calls), 3)
        rows = call('/api/resultados')
        new = [r for r in rows if r['coorte'] == doc.COORTE_SINTETICA]
        self.assertEqual(len(new), 3)
        for r in new:
            detail = call('/api/resultado/'+r['id'])
            self.assertEqual(detail['documentacao_id'], r['documentacao_id'])
            self.assertEqual(detail['plano_sha256'], app.documental.plan_hash)
        self.assertEqual(call('/api/job/'+job['id'])['documental']['pendentes'], 61)


if __name__ == '__main__':
    unittest.main()
