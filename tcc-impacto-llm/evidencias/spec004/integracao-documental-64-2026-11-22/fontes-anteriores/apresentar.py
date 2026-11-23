"""Painel local de demonstração e verificação offline da bancada.

python apresentar.py                 abre o painel, sem envio automático
python apresentar.py --sem-abrir     inicia somente o servidor local
python apresentar.py verificar       testes originais, matriz e leitura offline
python apresentar.py limpar          lista caches descartáveis da raiz
python apresentar.py limpar --aplicar remove somente caches não rastreados

Uma chamada real só começa por clique explícito. Demonstrações permanecem
separadas das coortes científicas. Verificar não gera painel ou relatório.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
REFERENCE = 'materiais/modelos/referencia_candidata_0.3_NAO_ENVIAR_AO_LLM.json'
COHORTS = {
    'comparacao': ('Comparação de 64 respostas', 'captura/extensao-real-0.3-001',
                  'avaliados/extensao-real-0.3-001-avaliacao-001'),
    'notas': ('Bloco de 16 respostas de notas', 'captura/notas-mc04-real-001',
              'avaliados/notas-mc04-real-001'),
}
GUARD = """
import sys
def sem_rede(evento, argumentos):
    if evento.startswith('socket.'):
        raise RuntimeError('Demonstração offline: rede bloqueada no processo de testes')
sys.addaudithook(sem_rede)
"""


def sha(data):
    return hashlib.sha256(data).hexdigest()


def ler_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def arquivo(root, relative):
    path = (root / relative).resolve()
    if not path.is_relative_to(root.resolve()):
        raise ValueError('Caminho fora do projeto: ' + str(relative))
    return path


def executar_local(root, code, timeout=120):
    env = os.environ.copy()
    env.pop('OPENAI_API_KEY', None)
    env.update(PYTHONIOENCODING='utf-8', PYTHONDONTWRITEBYTECODE='1')
    return subprocess.run([sys.executable, '-B', '-c', GUARD + '\n' + code],
                          cwd=root, env=env, capture_output=True, timeout=timeout)


def ler_capturas(root):
    """Mostra originais e pontuações existentes, sem chamar o avaliador ou LLM."""
    records, hashes, reports = [], {}, {}
    reference_hash = sha(arquivo(root, REFERENCE).read_bytes())
    for cohort, (label, batch_name, evaluation_name) in COHORTS.items():
        batch, evaluation = arquivo(root, batch_name), arquivo(root, evaluation_name)
        plan_path = batch / 'plano-original.json'
        plan = ler_json(plan_path)
        hashes[plan_path.relative_to(root).as_posix()] = sha(plan_path.read_bytes())
        report_path = evaluation / 'descritivo-pendente.json'
        reports[cohort] = ler_json(report_path)
        hashes[report_path.relative_to(root).as_posix()] = sha(report_path.read_bytes())
        if plan['referencia_sha256'] != reference_hash:
            raise ValueError('Referência atual difere da versão usada em ' + label)
        for observation in plan['observacoes']:
            identity = observation['observacao_id']
            if not re.fullmatch(r'[A-Za-z0-9_-]+', identity):
                raise ValueError('Identificador de observação inválido')
            capture = batch / identity / 'T01'
            assessed = evaluation / identity / 'T01'
            record = ler_json(capture / 'tentativa.json')
            request = ler_json(capture / 'requisicao.json')
            result = ler_json(assessed / 'avaliacao.json')
            original = (capture / 'resposta.bin').read_bytes()
            if sha(original) != record['resposta_sha256'] or original != (assessed / 'resposta-original.bin').read_bytes():
                raise ValueError('Resposta original divergente em ' + identity)
            if sha(request['input'].encode('utf-8')) != observation['payload_sha256']:
                raise ValueError('Payload divergente do plano em ' + identity)
            if result['referencia']['sha256'] != reference_hash:
                raise ValueError('Avaliação de outra referência em ' + identity)
            if result['observacao_id'] != identity or record['observacao_id'] != identity:
                raise ValueError('Identidade divergente em ' + identity)
            if result.get('nota_id') != observation.get('nota_id'):
                raise ValueError('Fator nota divergente em ' + identity)
            for path in (capture / 'tentativa.json', capture / 'requisicao.json',
                         capture / 'resposta.bin', assessed / 'avaliacao.json'):
                hashes[path.relative_to(root).as_posix()] = sha(path.read_bytes())
            records.append({
                'coorte': cohort, 'id': identity, 'modelo': record['modelo_reportado'],
                'mudanca': observation['mudanca'], 'condicao': observation['condicao'],
                'nota': observation.get('nota_id'), 'repeticao': observation['repeticao'],
                'instante': record['instante_execucao'], 'estado': record['estado_tecnico'],
                'conformidade_original': record.get('conformidade_protocolo', 'indisponível'),
                'payload': request['input'], 'resposta': original.decode('utf-8'),
                'requisitos': result['requisitos'], 'testes': result['testes'],
                'formato': result['formato_contrato'], 'tokens': record.get('usage'),
                'ferramentas': request.get('tools'), 'tool_choice': request.get('tool_choice'),
                'modelo_solicitado': request.get('model'),
                'configuracao': {k: request.get(k) for k in (
                    'model', 'reasoning', 'max_output_tokens', 'tools', 'tool_choice', 'store', 'stream')},
                'causa': record.get('causa'), 'desvios': record.get('desvios', []),
                'http_status': record.get('http_status'), 'request_id': record.get('request_id'),
                'response_id': record.get('response_id'), 'fase': record.get('fase'),
                'payload_sha256': observation['payload_sha256'],
                'resposta_sha256': record['resposta_sha256'],
                'pasta': capture.as_uri(), 'avaliacao': (assessed / 'avaliacao.json').as_uri(),
            })
    return records, hashes, reports


def abrir_pasta(path):
    if sys.platform == 'win32':
        os.startfile(str(path))
    else:
        opener = shutil.which('open' if sys.platform == 'darwin' else 'xdg-open')
        if opener:
            subprocess.Popen([opener, str(path)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def limpar_caches(root, aplicar=False):
    """Somente três diretórios de cache na raiz; nunca percorre evidências."""
    removed, candidates = [], []
    for name in ('__pycache__', '.pytest_cache', '.ruff_cache'):
        path = root / name
        if not path.exists() and not path.is_symlink():
            continue
        if path.is_symlink() or getattr(path, 'is_junction', lambda: False)():
            raise ValueError('Cache é link/junction; preservado: ' + name)
        if not path.is_dir():
            raise ValueError('Candidato não é diretório de cache: ' + name)
        result = subprocess.run(['git', 'ls-files', '-z', '--', name], cwd=root, capture_output=True)
        if result.returncode or result.stdout:
            raise ValueError('Não foi comprovado que o cache é não rastreado: ' + name)
        # Não segue links internos; rmtree remove o link, não o destino.
        candidates.append(name)
        if aplicar:
            shutil.rmtree(path)
            removed.append(name)
    return {'modo': 'aplicado' if aplicar else 'prévia', 'candidatos': candidates, 'removidos': removed,
            'preservados': ['captura', 'avaliados', 'evidencias', 'materiais', 'specs', 'documentacao']}


def verificar(root=ROOT):
    """Executa a bancada sem rede/chave, sem gerar arquivos de apresentação."""
    root = Path(root).resolve()
    print('1/3 Executando os 18 testes originais da autorização...', flush=True)
    unit = executar_local(root, "import runpy; sys.argv=['unittest','discover','-s','tests','-p','test_autorizacao.py','-v']; runpy.run_module('unittest',run_name='__main__')")
    log = (unit.stdout + unit.stderr).decode('utf-8', errors='replace')
    print(log, end='')
    match = re.search(r'Ran (\d+) tests? in ', log)
    unit_ok = unit.returncode == 0 and match is not None and int(match.group(1)) == 18
    print('2/3 Conferindo os 15 casos nas cinco versões...', flush=True)
    matrix = executar_local(root, "import json; sys.path.insert(0,'tests'); from test_extensao_exploratoria import matriz; print(json.dumps(matriz(),ensure_ascii=False))")
    rows = json.loads(matrix.stdout.decode('utf-8')) if matrix.returncode == 0 else []
    passed = sum(r['conforme'] for r in rows)
    matrix_ok = matrix.returncode == 0 and len(rows) == 75 and passed == 75
    print(f'Bancada: {passed}/{len(rows)} comparações conformes')
    if matrix.stderr:
        print(matrix.stderr.decode('utf-8', errors='replace'), file=sys.stderr)
    print('3/3 Conferindo as 64 + 16 respostas preservadas, sem reavaliar...', flush=True)
    records, hashes, _ = ler_capturas(root)
    counts = {cohort: sum(r['coorte'] == cohort for r in records) for cohort in COHORTS}
    for name, original_hash in hashes.items():
        if sha(arquivo(root, name).read_bytes()) != original_hash:
            raise ValueError('Fonte alterada durante a verificação: ' + name)
    print(f"Originais: {counts['comparacao']} + {counts['notas']}; {len(hashes)} hashes conferidos.")
    print('Nenhuma chamada à API, relatório HTML ou alteração de conformidade.')
    return 0 if unit_ok and matrix_ok and counts == {'comparacao': 64, 'notas': 16} else 1


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('acao', choices=('painel', 'verificar', 'limpar'), nargs='?', default='painel')
    parser.add_argument('--sem-abrir', action='store_true', help='Inicia o servidor sem abrir navegador')
    parser.add_argument('--porta', type=int, default=8765, help='Porta local do painel (padrão: 8765)')
    parser.add_argument('--aplicar', action='store_true', help='Somente em limpar: remove os caches listados')
    args = parser.parse_args(argv)
    if args.aplicar and args.acao != 'limpar':
        parser.error('--aplicar só é usado com limpar')
    if args.acao != 'painel' and (args.sem_abrir or args.porta != 8765):
        parser.error('--sem-abrir e --porta só são usados com painel')
    try:
        if args.acao == 'limpar':
            print(json.dumps(limpar_caches(ROOT, args.aplicar), ensure_ascii=False, indent=2))
            return 0
        if args.acao == 'verificar':
            return verificar()
        if not 1 <= args.porta <= 65535:
            parser.error('Escolha uma porta de 1 a 65535')
        from painel_llm import servir
        servir(ROOT, porta=args.porta, sem_abrir=args.sem_abrir)
        return 0
    except (Exception, KeyboardInterrupt) as exc:
        print(f'Apresentação interrompida: {type(exc).__name__}: {exc}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
