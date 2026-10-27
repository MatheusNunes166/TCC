"""Registro local de preparação; não integra montagem ou avaliação."""
from pathlib import Path
import ctypes
import hashlib
import json
import platform
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'evidencias/spec004/preparacao'

def dump(path, value):
    with path.open('x', encoding='utf-8', newline='\n') as stream:
        json.dump(value, stream, ensure_ascii=True, indent=2)
        stream.write('\n')

def run(*args):
    p = subprocess.run(args, cwd=ROOT, capture_output=True)
    return {'comando': list(args), 'retorno': p.returncode,
            'stdout': p.stdout.decode('utf-8', 'replace'),
            'stderr': p.stderr.decode('utf-8', 'replace')}

if __name__ == '__main__':
    protected = {}
    for folder in ['materiais', 'evidencias/spec003', 'variantes', 'tests',
                   'specs/001-autorizacao-direta', 'specs/002-heranca-incompatibilidade',
                   'specs/003-mudancas-controladas']:
        for p in (ROOT / folder).rglob('*'):
            if p.is_file() and '__pycache__' not in p.parts and 'spec004' not in p.parts:
                protected[p.relative_to(ROOT).as_posix()] = hashlib.sha256(p.read_bytes()).hexdigest()
    for name in ['autorizacao.py', 'verificacao_variantes.py', '.specify/memory/constitution.md',
                 'documentacao/21-10-2026.txt']:
        protected[name] = hashlib.sha256((ROOT/name).read_bytes()).hexdigest()
    initial = OUT / 'arquivos-iniciais'
    initial.mkdir(exist_ok=False)
    docs = list((ROOT/'specs/004-preparacao-avaliacao-ids').rglob('*.md'))
    docs += [ROOT/p for p in ['documentacao/decisoes.md', 'AGENTS.md',
                              'ESTADO_ATUAL.md', 'BLOQUEIOS.md', 'HANDOFF.md']]
    for p in docs:
        target = initial/p.relative_to(ROOT)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(p, target)
    dump(OUT/'inventario.json', {'python': sys.version, 'executavel': sys.executable,
         'cwd': str(ROOT), 'plataforma': platform.platform(),
         'git': [run('git','rev-parse','HEAD'), run('git','status','--short')],
         'protegidos_sha256': protected, 'originais_documentais': str(initial)})
    identity = run('whoami')
    dump(ROOT/'evidencias/spec004/isolamento/ambiente.json', {
        'identidade': identity, 'elevada': bool(ctypes.windll.shell32.IsUserAnAdmin()),
        'referencia_legivel_pelo_token_atual': bool((ROOT/'materiais/modelos/referencia_candidata_NAO_ENVIAR_AO_LLM.json').read_bytes()),
        'contrato_cumprido': False,
        'capacidade_ausente': 'Runner provisionado sob identidade separada sem leitura de desenvolvimento/referencia/avaliacao, com raizes e permissoes verificaveis. O token atual le a referencia; nao serve como prova de negacao.',
        'limite': 'Nao foram criadas contas, alteradas ACLs, usados privilegios alternativos ou simulada prova de isolamento. T014/T015 pendentes; controles logicos independentes autorizados.'})
    print('Inventario e originais preservados; isolamento real nao demonstrado.')
