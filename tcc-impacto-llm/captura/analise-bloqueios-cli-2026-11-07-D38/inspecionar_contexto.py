"""Renderiza contexto local com debug prompt-input; nenhum exec/turno/LLM.

Somente sentinelas artificiais. Saidas ficam locais; nao e prova da requisicao
de exec --ignore-user-config nem inventario de ferramentas do provedor.
"""
import json
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
import coletor_piloto as c


def main():
    work = OUT / 'ambiente-sentinela'
    work.mkdir(exist_ok=False)
    c.salvar(work / 'AGENTS.md', b'D38_SENTINELA_AGENTS_NAO_CARREGAR\n')
    records = []
    for name, additional in [('anterior', []), ('controles-explicitos', [
            'skills.include_instructions=false', 'memories.generate_memories=false',
            'memories.use_memories=false', 'model_provider="openai"'])]:
        argv = [shutil.which('codex'), 'debug', 'prompt-input']
        for value in ['model="gpt-6-sol"', 'model_reasoning_effort="medium"',
                      'web_search="disabled"', 'project_doc_max_bytes=0', 'analytics.enabled=false', *additional]:
            argv.extend(['-c', value])
        for feature in c.DESATIVAR:
            argv.extend(['--disable', feature])
        argv.append('D38_SENTINELA_PAYLOAD_ARTIFICIAL')
        cp = subprocess.run(argv, cwd=work, env=c.ambiente_filho(), capture_output=True, timeout=30)
        c.salvar(OUT / ('contexto-' + name + '-stdout.json'), cp.stdout)
        c.salvar(OUT / ('contexto-' + name + '-stderr.bin'), cp.stderr)
        # O JSON usa escapes; procurar na representacao decodificada, sem imprimir conteudo.
        try:
            parsed = json.loads(cp.stdout)
            text = json.dumps(parsed, ensure_ascii=False)
            fields = sorted(parsed) if isinstance(parsed, dict) else None
        except ValueError:
            text, fields = '', None
        records.append({'nome': name, 'argv': argv, 'retorno': cp.returncode,
                        'stdout_sha256': c.montagem.sha(cp.stdout), 'campos_raiz': fields,
                        'sentinela_payload_presente': 'D38_SENTINELA_PAYLOAD_ARTIFICIAL' in text,
                        'sentinela_agents_presente': 'D38_SENTINELA_AGENTS_NAO_CARREGAR' in text,
                        'tamanho_stdout': len(cp.stdout)})
        print(name, cp.returncode, len(cp.stdout), fields, flush=True)
    c.salvar_json(OUT / 'contexto-renderizado.json', {'consultas': records,
                   'limite': 'debug prompt-input nao expõe obrigatoriamente instructions/tools nem reproduz flags exclusivas de exec'})


if __name__ == '__main__':
    main()
