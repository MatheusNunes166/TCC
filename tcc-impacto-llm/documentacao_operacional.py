"""Adaptador documental: plano fixo, captura API existente e avaliação posterior.

Sem transporte ao construir/consultar. Um clique persistido libera um limite
explícito. Posições iniciadas, inclusive desconhecidas, nunca são reenviadas.
"""
from __future__ import annotations

import copy
import os
from pathlib import Path
import re
import threading

import coletor_api as api
import preparar_documentacao_operacional_v2 as prep
from painel_llm import ErroPainel

COORTE = 'documentacao_operacional_64'
COORTE_SINTETICA = 'documentacao_operacional_64_sintetica'
CAPTURA = 'captura/documentacao-operacional-64-real-001'
AVALIACAO = 'avaliados/documentacao-operacional-64-real-001'
FIELDS = ('documentacao_id', 'condicao', 'nota_id', 'mudanca', 'modelo_solicitado',
          'repeticao', 'bloco', 'ordem', 'payload_sha256')


class TravaLote:
    """Trava do SO, liberada também ao encerrar processo; arquivo não é apagado."""
    def __init__(self, path):
        self.path, self.stream = api.montagem.sem_links(path), None

    def adquirir(self, criar=True):
        if not criar and not self.path.exists():
            return True
        if criar:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            try:
                with self.path.open('xb') as stream:
                    stream.write(b'0')
            except FileExistsError:
                pass
        self.stream = self.path.open('r+b')
        try:
            if os.name == 'nt':
                import msvcrt
                msvcrt.locking(self.stream.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl
                fcntl.flock(self.stream, fcntl.LOCK_EX | fcntl.LOCK_NB)
            return True
        except OSError:
            self.stream.close()
            self.stream = None
            return False

    def liberar(self):
        if self.stream is not None:
            self.stream.seek(0)
            if os.name == 'nt':
                import msvcrt
                msvcrt.locking(self.stream.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                import fcntl
                fcntl.flock(self.stream, fcntl.LOCK_UN)
            self.stream.close()
            self.stream = None


class BlocoDocumental:
    def __init__(self, root, sender, chave, origem='real', captura=None, avaliacao=None):
        if origem not in ('real', 'sintetica'):
            raise ValueError('Origem inválida.')
        if origem == 'sintetica' and (captura is None or avaliacao is None):
            raise ValueError('Controles sintéticos exigem áreas separadas explícitas.')
        self.root = Path(root)
        self.pasta = self.root / prep.PASTA
        self.sender, self.chave, self.origem = sender, chave, origem
        self.capture = api.montagem.sem_links(Path(captura) if captura else self.root / CAPTURA)
        self.assessed = api.montagem.sem_links(Path(avaliacao) if avaliacao else self.root / AVALIACAO)
        if self.capture == self.assessed or (origem == 'sintetica' and (
                self.capture == self.root / CAPTURA or self.assessed == self.root / AVALIACAO)):
            raise ValueError('Áreas sintéticas/reais devem permanecer separadas.')
        prep.conferir(self.pasta, self.root)
        self.plan_raw = (self.pasta / 'plano.json').read_bytes()
        self.plan = api.montagem._json(self.plan_raw)
        self.plan_hash = api.sha(self.plan_raw)
        self.manifest_hash = api.sha((self.pasta / 'manifesto.json').read_bytes())
        self.rows = self.plan['observacoes']
        self.cohort = COORTE if origem == 'real' else COORTE_SINTETICA
        self.phase = 'exploratoria_documental' if origem == 'real' else 'verificacao_sintetica'
        self.lock, self.jobs, self.worker = threading.RLock(), {}, None

    def conferir(self, completa=True):
        if completa:
            prep.conferir(self.pasta, self.root)
        if api.sha((self.pasta / 'plano.json').read_bytes()) != self.plan_hash:
            raise ErroPainel('Plano mudou; envio recusado.')
        if api.sha((self.pasta / 'manifesto.json').read_bytes()) != self.manifest_hash:
            raise ErroPainel('Manifesto mudou; envio recusado.')
        if self.capture.exists():
            header = self.capture / 'lote.json'
            if header.exists():
                info = prep.ler(header)
                if any(info.get(k) != v for k, v in self.identidade().items()):
                    raise ErroPainel('Lote de outro plano, fase ou coorte.')
                if (self.capture / 'plano-original.json').read_bytes() != self.plan_raw:
                    raise ErroPainel('Cópia do plano no lote foi alterada.')

    def identidade(self):
        return {'coorte': self.cohort, 'origem': self.origem, 'fase': self.phase,
                'plano': prep.PASTA + '/plano.json',
                'plano_sha256': self.plan_hash, 'manifesto_sha256': self.manifest_hash}

    def ocupada(self):
        lock = TravaLote(self.capture / '.execucao.lock')
        available = lock.adquirir(criar=False)
        lock.liberar()
        return not available

    def pasta_observacao(self, row):
        return api.montagem.sem_links(self.capture / row['observacao_id'] / 'T01')

    def pendentes(self):
        return [r for r in self.rows if not self.pasta_observacao(r).exists()]

    def estado(self):
        positions, counts = [], {'concluidas': 0, 'falhas': 0, 'interrompidas': 0,
                                 'invalidas': 0, 'avaliadas': 0, 'desvios': 0}
        for row in self.rows:
            folder = self.pasta_observacao(row)
            result = folder / 'tentativa.json'
            evaluation = self.assessed / row['observacao_id'] / 'T01/avaliacao.json'
            state = 'pendente'
            if folder.exists():
                state = 'interrompida'
                if result.exists() and (folder / 'fechamento.json').exists():
                    record = prep.ler(result)
                    state = record['estado_tecnico']
                    counts['concluidas' if state == 'concluida' else 'falhas'] += 1
                    counts['desvios'] += bool(record['desvios'])
                else:
                    counts['interrompidas'] += 1
                if evaluation.exists():
                    ev = prep.ler(evaluation)
                    counts['avaliadas'] += 1
                    if ev['formato_contrato'] == 'invalido':
                        counts['invalidas'] += 1
                        state = 'invalida'
            positions.append({**row, 'situacao': state})
        pending = [r for r in positions if r['situacao'] == 'pendente']
        busy = self.ocupada()
        active = next((copy.deepcopy(j) for j in self.jobs.values() if not j['finalizado']), None)
        return {**self.identidade(), 'plano': prep.PASTA + '/plano.json',
            'quantidade_planejada': 64, 'payloads_unicos': 16, 'celulas': 32, 'N': 2,
            'configuracao': self.plan['configuracao'], 'posicoes': positions,
            **counts, 'iniciadas': 64 - len(pending), 'pendentes': len(pending),
            'proxima': pending[0] if pending else None, 'ocupada': busy, 'job_atual': active,
            'continuar_disponivel': bool(len(pending) < 64 and pending and not busy),
            'conformidade': 'pendente_revisao_humana_separada'}

    def previa(self):
        rows = self.pendentes()
        if not rows:
            raise ErroPainel('Não há posições pendentes.', 409)
        row = rows[0]
        raw = api.montagem.sem_links(self.pasta / row['payload']).read_bytes()
        if api.sha(raw) != row['payload_sha256']:
            raise ErroPainel('Payload alterado.')
        return {**row, 'payload': raw.decode(), 'sha256': row['payload_sha256'],
                **self.identidade()}

    def job(self, identity):
        with self.lock:
            if identity in self.jobs:
                result = copy.deepcopy(self.jobs[identity])
            elif re.fullmatch(r'DOCOP64-ACAO-[A-Za-z0-9_-]{12,80}', identity):
                path = self.capture / 'acoes' / (identity + '.json')
                if not path.exists():
                    raise ErroPainel('Ação não encontrada.', 404)
                final = path.with_suffix('.fim.json')
                result = prep.ler(final) if final.exists() else {
                    'id': identity, 'finalizado': not self.ocupada(), 'etapa': 'interrompida',
                    'mensagem': 'Ação de outra sessão. Consulte posições preservadas; nenhum reenvio automático.'}
            else:
                raise ErroPainel('Ação não encontrada.', 404)
        return {**result, 'documental': self.estado()}

    def iniciar(self, choice, demo_ocupada=False):
        if not isinstance(choice, dict) or set(choice) != {'bloco', 'acao_id', 'limite', 'plano_sha256', 'manifesto_sha256'}:
            raise ErroPainel('Use somente bloco, ação, limite e hashes do plano/manifesto.')
        click, limit = choice['acao_id'], choice['limite']
        if (choice['bloco'] != COORTE or not isinstance(click, str)
                or not re.fullmatch(r'[A-Za-z0-9_-]{12,80}', click)
                or type(limit) is not int or not 1 <= limit <= 64
                or choice['plano_sha256'] != self.plan_hash
                or choice['manifesto_sha256'] != self.manifest_hash):
            raise ErroPainel('Ação, limite ou plano divergente.')
        identity = 'DOCOP64-ACAO-' + click
        action_file = self.capture / 'acoes' / (identity + '.json')
        with self.lock:
            if action_file.exists():
                if prep.ler(action_file)['solicitacao'] != choice:
                    raise ErroPainel('Ação já usada com outra seleção.', 409)
                return self.job(identity)
            if demo_ocupada:
                raise ErroPainel('Há demonstração em andamento.', 409)
            process_lock = TravaLote(self.capture / '.execucao.lock')
            if not process_lock.adquirir():
                raise ErroPainel('Lote em andamento em outra ação ou processo.', 409)
            try:
                self.conferir()
                if action_file.exists():
                    if prep.ler(action_file)['solicitacao'] != choice:
                        raise ErroPainel('Ação já usada com outra seleção.', 409)
                    return self.job(identity)
                pending = self.pendentes()
                if not pending or limit > len(pending):
                    raise ErroPainel('Limite excede posições pendentes.', 409)
                if len(pending) == 64 and limit != 1:
                    raise ErroPainel('Primeira ação exige somente uma chamada.', 409)
                try:
                    key = self.chave()
                except (ValueError, KeyError):
                    raise ErroPainel('Configure OPENAI_API_KEY somente no ambiente do servidor.') from None
                if not (self.capture / 'lote.json').exists():
                    api.salvar_json(self.capture / 'lote.json', {**self.identidade(), 'instante': api.agora(),
                        'tipo': 'pesquisa_documental' if self.origem == 'real' else 'controle_sintetico'})
                    api.salvar(self.capture / 'plano-original.json', self.plan_raw)
                selected = pending[:limit]
                api.salvar_json(action_file, {**self.identidade(), 'id': identity,
                    'instante_clique_servidor': api.agora(), 'solicitacao': choice,
                    'limite_solicitado': limit, 'chamadas_pagas_solicitadas': limit if self.origem == 'real' else 0,
                    'posicoes_previstas': [r['observacao_id'] for r in selected],
                    'payloads_sha256': [r['payload_sha256'] for r in selected],
                    'origem_acao': 'clique_explicito_interface', 'conformidade_aprovada': False})
                self.jobs[identity] = {'id': identity, 'etapa': 'preparando', 'finalizado': False,
                    'limite': limit, 'enviadas': 0, 'mensagem': 'Preparando a execução sequencial.', 'eventos': []}
                self.worker = threading.Thread(target=self._executar,
                    args=(identity, selected, key, process_lock), daemon=False)
                self.worker.start()
                process_lock = None  # A thread mantém a trava até terminar a captura/avaliação.
                return self.job(identity)
            finally:
                if process_lock is not None:
                    process_lock.liberar()

    def _etapa(self, identity, etapa, mensagem, **extra):
        with self.lock:
            self.jobs[identity].update(etapa=etapa, mensagem=mensagem, **extra)
            self.jobs[identity]['eventos'].append({'etapa': etapa, 'instante': api.agora()})

    def _executar(self, identity, selected, key, process_lock):
        try:
            for row in selected:
                self.conferir(completa=False)
                self._etapa(identity, 'preparando', f"Posição {row['ordem']}/64: {row['observacao_id']}")
                record, evaluation = self._capturar(identity, row, key)
                if (record['estado_tecnico'] != 'concluida' or record['desvios']
                        or evaluation['status_avaliacao'] != 'avaliada'):
                    self._etapa(identity, 'concluida', 'Lote interrompido por ocorrência técnica ou formato inválido. '
                        'Originais preservados. Consulte os detalhes antes de continuar pendentes.', finalizado=True)
                    break
            else:
                self._etapa(identity, 'concluida', 'Limite solicitado concluído. Capturas e avaliações preservadas.', finalizado=True)
        except BaseException as error:
            # Nunca persistir mensagem arbitrária: transporte pode carregar credencial.
            self._etapa(identity, 'falha', 'Execução interrompida (' + type(error).__name__ +
                '). Consulte os registros. Posições iniciadas não serão reenviadas.', finalizado=True)
        finally:
            with self.lock:
                final = copy.deepcopy(self.jobs[identity])
            try:
                api.salvar_json(self.capture / 'acoes' / (identity + '.fim.json'), final)
            finally:
                process_lock.liberar()

    def _capturar(self, identity, row, key):
        folder = self.pasta_observacao(row)
        folder.mkdir(parents=True, exist_ok=False)  # Reserva durável antes de qualquer envio.
        payload = api.montagem.sem_links(self.pasta / row['payload']).read_bytes()
        if api.sha(payload) != row['payload_sha256']:
            raise ErroPainel('Payload divergente.')
        config = {**self.plan['configuracao'], 'modelo_solicitado': row['modelo_solicitado']}
        body = api.requisicao(payload, config)
        sources = self.plan['fontes'][row['mudanca'] + ':' + row['condicao']]
        initial = {**self.identidade(), **row, 'acao_id': identity, 'tentativa_id': 'T01',
            'instante_execucao': api.agora(), 'configuracao': config,
            'referencia_sha256': sources['referencia_sha256'], 'origem_payload': sources,
            'requisicao_sha256': api.sha(body), 'retentativas_cliente': 0,
            'fontes_sha256': {p.name: api.sha(p.read_bytes()) for p in (
                Path(__file__), Path(api.__file__), Path(prep.__file__))}}
        api.salvar_json(folder / 'inicio.json', initial)
        api.salvar(folder / 'entrada.bin', payload)
        api.guardar_requisicao(folder, body)
        api.salvar_json(folder / 'envio-iniciado.json', {'instante': api.agora(), 'acao_id': identity,
            'estado_remoto': 'desconhecido', 'requisicao_sha256': api.sha(body), **self.identidade()})
        self._etapa(identity, 'enviando', f"Enviando posição {row['ordem']}/64, uma chamada sem retry.",
                    ultima_observacao=row['observacao_id'])
        with self.lock:
            self.jobs[identity]['enviadas'] += 1
        status, raw, request_id, failure = api.obter_http(self.sender, body, key, config['timeout_segundos'])
        api.guardar_http(folder, status, raw, request_id, failure)
        parsed = api.falha_interpretada(failure) if failure else api.interpretar(raw, status, config)
        if parsed['texto'] is not None:
            api.salvar(folder / 'resposta.bin', parsed['texto'])
        record = {**initial, 'estado_tecnico': 'concluida' if parsed['concluida'] else 'falha_tecnica',
            'instante_fim': api.agora(), 'http_status': status, 'request_id': request_id,
            'response_id': parsed['response_id'], 'modelo_reportado': parsed['modelo_reportado'],
            'usage': parsed['usage'], 'desvios': parsed['desvios'], 'causa': parsed['causa'],
            'falha_transporte': failure, 'estado_remoto': 'desconhecido' if failure else 'resposta_http_recebida',
            'resposta_sha256': api.sha(parsed['texto']) if parsed['texto'] is not None else None,
            'conformidade_protocolo': 'pendente'}
        api.salvar_json(folder / 'tentativa.json', record)
        api.salvar_json(folder / 'fechamento.json', {'arquivos': api.base.inventariar(folder)})
        self._etapa(identity, 'avaliando', 'Captura fechada e preservada. Avaliação offline posterior.')
        return record, self.avaliar(row)

    def avaliar(self, row):
        """Pode ser retomada offline, sem tocar na captura ou chamar o transporte."""
        import avaliacao_ids as evaluator
        import apresentar as apoio
        capture = self.pasta_observacao(row)
        record = api.base.conferir_fechamento(capture)
        if any(record[k] != row[k] for k in FIELDS) or record['plano_sha256'] != self.plan_hash:
            raise ErroPainel('Identidade da captura divergente.')
        reference_raw = (self.root / apoio.REFERENCE).read_bytes()
        if api.sha(reference_raw) != record['referencia_sha256']:
            raise ErroPainel('Referência mudou; captura preservada e avaliação interrompida.')
        out = api.montagem.sem_links(self.assessed / row['observacao_id'] / 'T01')
        if (out / 'fechamento.json').exists():
            closing = prep.ler(out / 'fechamento.json')
            if closing['arquivos'] != api.base.inventariar(out):
                raise ErroPainel('Avaliação anterior alterada.')
            return prep.ler(out / 'avaliacao.json')
        if out.exists():
            raise ErroPainel('Avaliação parcial preservada; usar revisão offline em novo destino.')
        response = capture / 'resposta.bin'
        text = response.read_bytes() if response.exists() else b''
        result = evaluator.avaliar_resposta(text, evaluator.json_estrito(reference_raw),
                                          row['mudanca'], record['estado_tecnico'])
        result.update(**self.identidade(), **{k: record[k] for k in FIELDS},
            observacao_id=row['observacao_id'], tentativa_id='T01',
            modelo_reportado=record['modelo_reportado'], referencia_sha256=record['referencia_sha256'],
            resposta_sha256=record['resposta_sha256'], requisicao_sha256=record['requisicao_sha256'],
            captura_fechamento_sha256=api.sha((capture / 'fechamento.json').read_bytes()),
            politica=evaluator.POLITICA, avaliador_sha256=api.sha(Path(evaluator.__file__).read_bytes()),
            instante_avaliacao=api.agora(), conformidade_protocolo='pendente')
        api.salvar_json(out / 'avaliacao.json', result)
        api.salvar(out / 'tentativa-original.json', (capture / 'tentativa.json').read_bytes())
        if response.exists():
            api.salvar(out / 'resposta-original.bin', text)
        api.salvar_json(out / 'fechamento.json', {'arquivos': api.base.inventariar(out)})
        # Ficha separada, com hashes, sem editar registro bruto ou avaliação.
        review = self.assessed / 'conformidade' / (row['observacao_id'] + '.pendente.json')
        if not review.exists():
            api.salvar_json(review, {'versao': 'decisoes-conformidade-v1', 'responsavel': None,
                'data': None, 'fontes': self.identidade(), 'observacoes': [{
                    **{k: row[k] for k in FIELDS}, 'observacao_id': row['observacao_id'],
                    'plano_sha256': self.plan_hash, 'payload_sha256': row['payload_sha256'],
                    'tentativa_sha256': api.sha((capture / 'tentativa.json').read_bytes()),
                    'fechamento_sha256': api.sha((capture / 'fechamento.json').read_bytes()),
                    'avaliacao_sha256': api.sha((out / 'avaliacao.json').read_bytes()),
                    'resposta_sha256': record['resposta_sha256'], 'decisao': 'pendente',
                    'justificativa': None}]})
        return result

    def registros(self):
        result = []
        for row in self.rows:
            folder = self.pasta_observacao(row)
            if not folder.exists():
                continue
            initial_path, final = folder / 'inicio.json', folder / 'tentativa.json'
            initial = prep.ler(initial_path) if initial_path.exists() else {
                **row, **self.identidade(), 'instante_execucao': None, 'configuracao': self.plan['configuracao']}
            record = api.base.conferir_fechamento(folder) if (folder / 'fechamento.json').exists() else initial
            if final.exists() and not (folder / 'fechamento.json').exists():
                record = {**prep.ler(final), 'estado_tecnico': 'interrompida',
                          'causa': 'Captura sem fechamento; métricas indisponíveis.'}
            out = self.assessed / row['observacao_id'] / 'T01'
            ev = {}
            if (out / 'fechamento.json').exists() and (folder / 'fechamento.json').exists():
                if prep.ler(out / 'fechamento.json')['arquivos'] != api.base.inventariar(out):
                    raise ErroPainel('Avaliação alterada; consulta interrompida.')
                ev = prep.ler(out / 'avaliacao.json')
            response, payload = folder / 'resposta.bin', folder / 'entrada.bin'
            result.append({**record, 'id': row['observacao_id'], 'modelo': row['modelo_solicitado'],
                'nota': row['nota_id'], 'instante': initial['instante_execucao'] or '',
                'estado': record.get('estado_tecnico', 'interrompida'),
                'conformidade_original': 'pendente', 'requisitos': ev.get('requisitos'),
                'testes': ev.get('testes'), 'formato': ev.get('formato_contrato', 'indisponivel'),
                'status_avaliacao': ev.get('status_avaliacao', 'pendente'),
                'estado_remoto': record.get('estado_remoto', 'desconhecido'),
                'tokens': record.get('usage'), 'resposta': response.read_text(encoding='utf-8') if response.exists() else '',
                'payload': payload.read_text(encoding='utf-8') if payload.exists() else '',
                'pasta': folder.as_uri(), 'avaliacao': (out / 'avaliacao.json').as_uri()})
        return result

    def celulas(self):
        """Agrupa explicitamente todos os fatores antes de reutilizar Jaccard."""
        import avaliacao_ids as evaluator
        records = {r['id']: r for r in self.registros()}
        cells = {}
        for row in self.rows:
            key = (self.cohort, self.origem, self.phase, self.plan_hash, row['documentacao_id'],
                   row['modelo_solicitado'], row['mudanca'], row['condicao'], row['nota_id'])
            cell = cells.setdefault(key, {'coorte': self.cohort, 'documentacao_id': row['documentacao_id'],
                'modelo': row['modelo_solicitado'], 'mudanca': row['mudanca'], 'condicao': row['condicao'],
                'nota_id': row['nota_id'], 'plano_sha256': self.plan_hash, 'N_planejado': 2,
                'observacoes': [], 'avaliaveis': [], 'falhas_ou_invalidas': []})
            cell['observacoes'].append(row['observacao_id'])
            reg = records.get(row['observacao_id'])
            if reg:
                cell['avaliaveis' if reg['status_avaliacao'] == 'avaliada' else 'falhas_ou_invalidas'].append(reg['id'])
        for cell in cells.values():
            eligible = [records[oid] for oid in cell['avaliaveis']]
            # Projeção mínima; os fatores completos já foram conferidos acima.
            regs = [{'observacao_id': r['id'], 'origem': 'real', 'repeticao': r['repeticao'],
                     'requisitos': r['requisitos'], 'testes': r['testes']} for r in eligible]
            cell['consistencia_descritiva_pendente'] = {d: evaluator.jaccard(regs, d) for d in ('requisitos', 'testes')}
            cell['N_valido'] = len(eligible)
            cell['N_iniciado'] = sum(oid in records for oid in cell['observacoes'])
            cell['conformidade'] = 'pendente; descrição não aprova inclusão'
        return list(cells.values())
