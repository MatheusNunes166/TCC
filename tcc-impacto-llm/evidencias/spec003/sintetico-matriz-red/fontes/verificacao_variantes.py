"""Verificação local da Spec 003. Não coleta LLM nem altera a referência."""
from __future__ import annotations

import ast
import copy
import difflib
import hashlib
import importlib.machinery
import importlib.util
import json
import pathlib
import platform
import subprocess
import sys
import traceback
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
