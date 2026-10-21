"""Verificação local da Spec 003. Não coleta LLM nem altera a referência."""
from __future__ import annotations

import ast
import copy
import difflib
import hashlib
import importlib.machinery
import importlib.util
import io
import json
import pathlib
import platform
import subprocess
import sys
import traceback
import unittest
import uuid
from datetime import datetime, timezone

BASELINE = 'aec474bcb54d6dae2afceff8e5b9226991386490'
REFERENCE = 'materiais/modelos/referencia_candidata_NAO_ENVIAR_AO_LLM.json'
VARIANTS = {'MC-01': 'variantes/mc01.py', 'MC-02': 'variantes/mc02.py',
            'MC-03': 'variantes/mc03.py', 'MC-04-v2': 'variantes/mc04.py'}
CASE_IDS = {f'T{i:02}' for i in range(1, 13)}
SOURCE_FILES = ('autorizacao.py', 'tests/test_autorizacao.py', REFERENCE,
                'documentacao/requisitos.md', 'documentacao/qualidade-e-testes.md',
                'documentacao/referencia-candidata-proxima-etapa.md',
                'documentacao/evidencias-t12.md', 'materiais/02_REQUISITOS_TESTES_E_REFERENCIA.md',
                'materiais/07_DEFINICOES_COMUNS.md')


class VerificationError(ValueError):
    """Falha de pré-condição, procedência ou integridade."""


def now():
    return datetime.now(timezone.utc).isoformat()


def sha256(data):
    return hashlib.sha256(data).hexdigest()


class GitSource:
    def __init__(self, project):
        self.project = pathlib.Path(project).resolve()
        self.root = pathlib.Path(self.command('rev-parse', '--show-toplevel').decode().strip())
        self.prefix = self.command('rev-parse', '--show-prefix').decode().strip()

    def command(self, *args):
        result = subprocess.run(['git', *args], cwd=self.project, capture_output=True)
        if result.returncode:
            raise VerificationError(result.stderr.decode('utf-8', errors='replace'))
        return result.stdout

    def read(self, relative, commit=BASELINE):
        if self.command('cat-file', '-t', commit).strip() != b'commit':
            raise VerificationError('Origem não é commit')
        key = f'{commit}:{self.prefix}{relative}'
        return self.command('show', key), self.command('rev-parse', key).decode().strip()


def valid_result(value):
    return (type(value) is dict and set(value) == {'decisao', 'motivo'}
            and type(value['decisao']) is str and value['decisao'] in {'permitir', 'negar'}
            and type(value['motivo']) is str and value['motivo'] in
            {'estado', 'conflito', 'sem_permissao', 'permissao_direta', 'permissao_herdada'})


def validate_reference(ref):
    """Valida estrutura e domínio, nunca deduz esperado com código executável."""
    try:
        assert ref['versao'] == '0.2' and ref['status'] == 'CANDIDATO_NAO_REVISADO'
        assert ref['revisor'] is None and ref['data_revisao'] is None
        catalog = ref['catalogo']
        assert type(catalog) is list and len(catalog) == 12
        assert {c['id'] for c in catalog} == CASE_IDS
        for case in catalog:
            assert set(case) == {'id', 'estado', 'papeis', 'operacao', 'esperado'}
            assert case['estado'] in {'ativa', 'suspensa', 'em_revisao'}
            assert type(case['papeis']) is list
            assert len(case['papeis']) == len(set(case['papeis']))
            assert set(case['papeis']) <= {'Consulta', 'Auditoria', 'Supervisão'}
            assert case['operacao'] in {'visualizar', 'exportar'}
            assert valid_result(case['esperado'])
        changes = ref['mudancas']
        assert type(changes) is list and len(changes) == 4
        assert {c['id'] for c in changes} == set(VARIANTS)
        for change, size in zip(changes, (2, 4, 8, 5)):
            assert type(change['expected']) is dict and set(change['expected']) == CASE_IDS
            assert all(valid_result(result) for result in change['expected'].values())
            for name in ('tests', 'changed', 'preserved'):
                assert type(change[name]) is list
                assert len(set(change[name])) == len(change[name])
                assert set(change[name]) <= CASE_IDS
            assert set(change['changed']).isdisjoint(change['preserved'])
            assert set(change['tests']) == set(change['changed']) | set(change['preserved'])
            assert len(change['tests']) == size
        return ref
    except (AssertionError, KeyError, TypeError, ValueError) as exc:
        raise VerificationError('Referência 0.2 inválida/incompleta; revisão necessária') from exc


def create_output(root, requested):
    root = pathlib.Path(root).resolve()
    raw = pathlib.Path(requested)
    if '..' in raw.parts:
        raise VerificationError('Saída contém navegação relativa')
    output = (root / raw).resolve()
    area = root / 'evidencias' / 'spec003'
    if area.resolve() != area or output.parent != area:
        raise VerificationError('Saída deve ser pasta nova diretamente em evidencias/spec003')
    try:
        output.mkdir(parents=True, exist_ok=False)
    except FileExistsError as exc:
        raise VerificationError('Pasta já existe; preservar tentativa anterior') from exc
    return output


def save_json(path, value):
    """Substituição atômica apenas dentro da tentativa corrente."""
    path = pathlib.Path(path)
    temporary = path.with_name(path.name + '.tmp')
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    temporary.replace(path)


def make_records(ref, execution_id):
    def row(change, case, expected):
        return dict(id_execucao=execution_id, mudanca=change, teste=case['id'],
                    entrada={k: copy.deepcopy(case[k]) for k in ('estado', 'papeis', 'operacao')},
                    versao_executada=None,
                    referencia={'versao': '0.2', 'chave': f'{change}/{case["id"]}'},
                    esperado=copy.deepcopy(expected), observado=None, observado_bruto=None,
                    estado='nao_executado', comparacao='nao_comparavel', diferencas=[],
                    efeito_esperado='preservou' if expected == case['esperado'] else 'mudou',
                    efeito_observado='indisponivel', erro='ainda_nao_executado',
                    evidencia=None, diagnostico=None)
    return {'baseline': [row('BASELINE', c, c['esperado']) for c in ref['catalogo']],
            'variantes': [row(m['id'], c, m['expected'][c['id']])
                          for m in ref['mudancas'] for c in ref['catalogo']]}


def snapshot_baseline(git, output):
    inventory = {}
    for name in SOURCE_FILES:
        data, blob = git.read(name)
        target = output / 'fontes' / 'baseline' / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        inventory[name] = {'objeto_git': blob, 'sha256': sha256(data), 'caminho': str(target)}
    return inventory


def new_manifest(git, output, command):
    return dict(schema_version=1, id_execucao=output.name, inicio_utc=now(), fim_utc=None,
                tipo='bancada_real', comando=command, argumentos=sys.argv[1:], cwd=str(git.project),
                plataforma=platform.platform(), python={'executavel': sys.executable, 'versao': sys.version},
                baseline_commit=BASELINE, raiz_git=str(git.root), prefixo_git=git.prefix,
                commit_executor=git.command('rev-parse', 'HEAD').decode().strip(),
                estado_local=git.command('status', '--short').decode('utf-8'),
                estado='preparando', revisao_cientifica='pendente', piloto_liberado=False,
                fontes={}, variantes={}, logs={}, erros=[], retentativa_de=None)


def audit_source(base, candidate, change, origin):
    """Audita edição exata e AST; não produz fonte ou expectativa de execução."""
    if origin != BASELINE or change not in VARIANTS:
        raise VerificationError('Origem encadeada/desconhecida')
    rules = {
        'MC-01': ("(('Consulta', 'visualizar'), ('Auditoria', 'exportar'))", "(('Consulta', 'visualizar'),)"),
        'MC-02': ("return {'Consulta', 'Auditoria'} <= papeis_efetivos", 'return False'),
        'MC-03': ("(('Consulta', 'visualizar'), ('Auditoria', 'exportar'))", "(('Auditoria', 'exportar'),)"),
        'MC-04-v2': ("return papeis | frozenset({'Consulta'} if 'Supervisão' in papeis else ())", 'return papeis')}
    before, after = (s.encode('utf-8') for s in rules[change])
    if base.count(before) != 1 or candidate != base.replace(before, after, 1):
        raise VerificationError('Diff fora da única edição autorizada')
    expected_ast = ast.parse(base)
    actual_ast = ast.parse(candidate)
    function = {'MC-01': 'obter_permissoes_diretas', 'MC-03': 'obter_permissoes_diretas',
                'MC-02': 'ha_incompatibilidade', 'MC-04-v2': 'obter_papeis_efetivos'}[change]
    node = next(n for n in expected_ast.body if isinstance(n, ast.FunctionDef) and n.name == function)
    if change in ('MC-01', 'MC-03'):
        sequence = node.body[-1].value.args[0].generators[0].iter
        removed = 'Auditoria' if change == 'MC-01' else 'Consulta'
        sequence.elts = [e for e in sequence.elts if e.elts[0].value != removed]
    else:
        node.body[-1].value = ast.Constant(False) if change == 'MC-02' else ast.Name(id='papeis', ctx=ast.Load())
    if ast.dump(expected_ast) != ast.dump(actual_ast):
        raise VerificationError('AST/assinaturas fora do contrato')
    diff = ''.join(difflib.unified_diff(base.decode('utf-8-sig').splitlines(True),
                                      candidate.decode('utf-8-sig').splitlines(True),
                                      fromfile='B/autorizacao.py', tofile=VARIANTS[change]))
    return dict(origem=origin, ast_conforme=True, alteracao_unica=True, diff=diff,
                sha256=sha256(candidate), diff_sha256=sha256(diff.encode('utf-8')))


def load_source(path, expected_hash, execution_id):
    path = pathlib.Path(path).resolve()
    if not sys.dont_write_bytecode:
        raise VerificationError('Executar Python com -B')
    if (path.parent / '__pycache__').exists() or sha256(path.read_bytes()) != expected_hash:
        raise VerificationError('Fonte/cache não corresponde ao snapshot')
    name = f'_spec003_{execution_id.replace("-", "_")}_{uuid.uuid4().hex}'
    spec = importlib.util.spec_from_file_location(name, path)
    if (spec is None or not isinstance(spec.loader, importlib.machinery.SourceFileLoader)
            or pathlib.Path(spec.origin).resolve() != path):
        raise VerificationError('Loader/caminho inválido')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if pathlib.Path(module.__file__).resolve() != path or sha256(path.read_bytes()) != expected_hash:
        raise VerificationError('Fonte mudou durante carregamento')
    return module


def observe(row, function, baseline=None):
    row.update(observado=None, observado_bruto=None, erro=None, diferencas=[],
               comparacao='nao_comparavel', efeito_observado='indisponivel')
    try:
        entry = row['entrada']
        result = function(entry['estado'], frozenset(entry['papeis']), entry['operacao'])
        if not valid_result(result):
            row['observado_bruto'] = {'tipo': type(result).__name__, 'repr': repr(result)}
            raise VerificationError('Retorno fora do contrato decisao/motivo')
        row['observado'] = copy.deepcopy(result)
        row['diferencas'] = [k for k in ('decisao', 'motivo') if result[k] != row['esperado'][k]]
        row['comparacao'] = 'diferente' if row['diferencas'] else 'igual'
        row['estado'] = 'divergente' if row['diferencas'] else 'conforme'
        if baseline is not None:
            row['efeito_observado'] = 'preservou' if result == baseline else 'mudou'
    except Exception as exc:
        row.update(estado='erro', erro={'tipo': type(exc).__name__, 'mensagem': str(exc),
                                      'traceback': traceback.format_exc()})
    return row


def summarize(rows):
    keys = [(r['mudanca'], r['teste']) for r in rows]
    if len(set(keys)) != len(keys) or set(keys) != {(m, t) for m in VARIANTS for t in CASE_IDS}:
        raise VerificationError('Matriz deve conter exatamente 48 chaves únicas conhecidas')
    labels = {'conforme': 'conformes', 'divergente': 'divergentes',
              'erro': 'erros', 'nao_executado': 'nao_executados'}
    counts = {name: 0 for name in labels.values()}
    for row in rows:
        if row['estado'] not in labels:
            raise VerificationError('Estado desconhecido')
        counts[labels[row['estado']]] += 1
    counts.update(previstos=48, tentados=48-counts['nao_executados'],
                  comparados=counts['conformes']+counts['divergentes'])
    return counts


def run_matrix(rows, functions, baseline, baseline_ok=True, persist=lambda: None, stream=None):
    """Matriz real usa funções reais; fixtures controladas ficam só nos testes sintéticos."""
    class Matrix(unittest.TestCase):
        def runTest(self):
            for row in rows:
                with self.subTest(mudanca=row['mudanca'], teste=row['teste']):
                    if not baseline_ok or row['mudanca'] not in functions:
                        row['erro'] = 'baseline_invalida' if not baseline_ok else 'fonte_invalida_ou_revisao_pendente'
                        persist()
                        continue
                    observe(row, functions[row['mudanca']], baseline.get(row['teste']))
                    # Persistência ANTES da asserção garante manutenção de cada ocorrência.
                    persist()
                    self.assertEqual(row['estado'], 'conforme', repr(row))
    stream = stream if stream is not None else io.StringIO()
    return unittest.TextTestRunner(stream=stream, verbosity=2).run(Matrix())


def run_baseline_suite(snapshot, output):
    command = [sys.executable, '-B', '-m', 'unittest', 'discover', '-s', 'tests', '-p', 'test_autorizacao.py', '-v']
    result = subprocess.run(command, cwd=snapshot, capture_output=True)
    (output / 'baseline-stdout.txt').write_bytes(result.stdout)
    (output / 'baseline-stderr.txt').write_bytes(result.stderr)
    log = result.stdout + result.stderr
    (output / 'baseline-unittest.txt').write_bytes(log)
    tree = ast.parse((snapshot / 'tests/test_autorizacao.py').read_bytes())
    methods = sum(isinstance(n, ast.FunctionDef) and n.name.startswith('test_') for n in ast.walk(tree))
    import re
    match = re.search(rb'Ran (\d+) tests? in ', log)
    count = int(match.group(1)) if match else 0
    ok = result.returncode == 0 and methods == count == 18 and b'\nOK' in log and b'skipped=' not in log
    return dict(comando=command, cwd=str(snapshot), retorno=result.returncode,
                metodos_descobertos=count, metodos_fonte=methods, conforme=ok,
                stdout='baseline-stdout.txt', stderr='baseline-stderr.txt', log='baseline-unittest.txt')


def execute_attempt(root, requested, command=None, retentativa_de=None):
    """Integração local; toda tentativa é nova e conserva originais mesmo em erro."""
    root = pathlib.Path(root).resolve()
    output = create_output(root, requested)
    git = GitSource(root)
    manifest = new_manifest(git, output, command or [sys.executable, '-B', *sys.argv])
    manifest['retentativa_de'] = retentativa_de
    rows = {'baseline': [], 'variantes': []}
    guarded = {}
    matrix_stream = io.StringIO()

    def persist():
        save_json(output / 'resultados.json', rows)
        save_json(output / 'manifesto.json', manifest)

    def guard(path):
        guarded[str(path)] = sha256(path.read_bytes())

    try:
        manifest['fontes'] = snapshot_baseline(git, output)
        for info in manifest['fontes'].values():
            guard(pathlib.Path(info['caminho']))
        # A baseline de trabalho não é executada; ainda assim, deve permanecer intacta.
        for name in ('autorizacao.py', 'tests/test_autorizacao.py', REFERENCE):
            guard(root / name)
        for path in (root / 'materiais').rglob('*'):
            if path.is_file():
                guard(path)
        if git.command('diff', BASELINE, '--', 'autorizacao.py', 'tests/test_autorizacao.py', REFERENCE).strip():
            raise VerificationError('Baseline de trabalho difere de B')
        for name in ('verificacao_variantes.py', 'tests/test_variantes.py', 'variantes/procedencia.json'):
            source = root / name
            data = source.read_bytes()
            target = output / 'fontes' / 'executor' / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
            guard(source)
            guard(target)
            manifest.setdefault('executor', {})[name] = {'sha256': sha256(data), 'snapshot': str(target)}
        baseline_path = output / 'fontes/baseline'
        reference_bytes = (baseline_path / REFERENCE).read_bytes()
        ref = validate_reference(json.loads(reference_bytes.decode('utf-8-sig')))
        rows = make_records(ref, output.name)
        reference_info = {'versao': '0.2', 'caminho': str(baseline_path / REFERENCE),
                          'sha256': sha256(reference_bytes), 'status': ref['status']}
        base = (baseline_path / 'autorizacao.py').read_bytes()
        metadata = json.loads((root / 'variantes/procedencia.json').read_text(encoding='utf-8'))
        functions = {}
        for change, relative in VARIANTS.items():
            info = {'valida': False, 'origem': BASELINE, 'erro': None}
            manifest['variantes'][change] = info
            try:
                source = root / relative
                data = source.read_bytes()
                target = output / 'fontes' / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(data)
                guard(source)
                guard(target)
                meta = metadata[change]
                audit = audit_source(base, data, change, meta['origem'])
                review = meta['revisao']
                if (meta['caminho'] != relative or meta['sha256'] != sha256(data)
                        or meta['objeto_origem'] != manifest['fontes']['autorizacao.py']['objeto_git']
                        or meta['diff_sha256'] != audit['diff_sha256']
                        or not review or review['resultado'] != 'aprovada'
                        or not review['responsavel'] or not review['data']):
                    raise VerificationError('Revisão/origem não corresponde aos bytes da fonte')
                diff = audit.pop('diff')
                diff_path = output / 'diffs' / f'{change}.diff'
                diff_path.parent.mkdir(exist_ok=True)
                diff_path.write_bytes(diff.encode('utf-8'))
                guard(diff_path)
                info.update(audit, revisao=review, caminho=str(target), diff=str(diff_path),
                            objeto_origem=meta['objeto_origem'])
                module = load_source(target, audit['sha256'], output.name)
                info.update(valida=True, loader=type(module.__loader__).__name__, module_file=module.__file__)
                functions[change] = module.autorizar
            except (Exception,) as exc:
                info['erro'] = {'tipo': type(exc).__name__, 'mensagem': str(exc), 'traceback': traceback.format_exc()}
        for row in rows['baseline'] + rows['variantes']:
            info = manifest['fontes']['autorizacao.py'] if row['mudanca'] == 'BASELINE' else manifest['variantes'][row['mudanca']]
            row['referencia'].update(reference_info)
            row['versao_executada'] = {'B': BASELINE, 'id': row['mudanca'],
                                       'caminho': info.get('caminho'), 'sha256': info.get('sha256'),
                                       'manifesto': 'fontes/autorizacao.py' if row['mudanca'] == 'BASELINE' else f'variantes/{row["mudanca"]}'}
            row['evidencia'] = {'log': 'baseline-pares.jsonl' if row['mudanca'] == 'BASELINE' else 'variantes-unittest.txt',
                                'subteste': f'{row["mudanca"]}/{row["teste"]}'}
        manifest['estado'] = 'em_execucao'
        persist()
        suite = run_baseline_suite(baseline_path, output)
        manifest['suite_baseline'] = suite
        module = load_source(baseline_path / 'autorizacao.py', sha256(base), output.name)
        with (output / 'baseline-pares.jsonl').open('x', encoding='utf-8') as stream:
            for row in rows['baseline']:
                observe(row, module.autorizar)
                stream.write(json.dumps(row, ensure_ascii=False) + '\n')
                stream.flush()
                persist()
        baseline_ok = suite['conforme'] and all(r['estado'] == 'conforme' for r in rows['baseline'])
        manifest['baseline_conforme'] = baseline_ok
        observed_baseline = {r['teste']: r['observado'] for r in rows['baseline']}
        run_matrix(rows['variantes'], functions, observed_baseline, baseline_ok, persist, matrix_stream)
        manifest['resumo'] = summarize(rows['variantes'])
        manifest['estado'] = 'concluida'
    except KeyboardInterrupt:
        manifest.update(estado='interrompida')
        manifest['erros'].append({'tipo': 'KeyboardInterrupt', 'mensagem': 'Execução interrompida; repetir em pasta nova'})
    except Exception as exc:
        manifest.update(estado='invalida')
        manifest['erros'].append({'tipo': type(exc).__name__, 'mensagem': str(exc), 'traceback': traceback.format_exc()})
    finally:
        for row in rows['baseline'] + rows['variantes']:
            if row['estado'] == 'nao_executado' and row['erro'] == 'ainda_nao_executado':
                row['erro'] = f'tentativa_{manifest["estado"]}'
        (output / 'variantes-unittest.txt').write_text(matrix_stream.getvalue(), encoding='utf-8')
        final_hashes = {name: sha256(pathlib.Path(name).read_bytes()) if pathlib.Path(name).is_file() else None
                        for name in guarded}
        manifest['hashes_antes'] = guarded
        manifest['hashes_depois'] = final_hashes
        manifest['integridade'] = guarded == final_hashes
        manifest['fim_utc'] = now()
        manifest['logs'] = {p.name: sha256(p.read_bytes()) for p in output.iterdir() if p.is_file() and p.suffix in ('.txt', '.jsonl')}
        if rows['variantes']:
            manifest['resumo'] = summarize(rows['variantes'])
        persist()
    return manifest, rows
