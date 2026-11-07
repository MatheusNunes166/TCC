"""Confirma somente parsing/contexto locais dos ajustes D-38. Sem modelo."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tomllib

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
import coletor_piloto as c
import inspecionar_config as native


def main():
    native.KEYS = (*native.KEYS, 'forced_login_method')
    config = native.consultar([*c.overrides_cli(), 'model="gpt-6-sol"', 'sandbox_mode="read-only"'])
    c.salvar_json(OUT / 'config-ajustes-aplicados.json', config)
    assert config['retorno'] == 0 and config['resultado']
    effective = config['resultado']['config']
    assert effective['model'] == 'gpt-6-sol' and effective['model_reasoning_effort'] == 'medium'
    assert effective['model_provider'] == 'openai' and effective['forced_login_method'] == 'chatgpt'
    assert effective['skills']['include_instructions'] is False
    assert effective['memories']['use_memories'] is False
    assert effective['memories']['generate_memories'] is False
    work = OUT / 'ambiente-sentinela'
    argv = [shutil.which('codex'), 'debug', 'prompt-input']
    for override in [*c.overrides_cli(), 'model="gpt-6-sol"', 'sandbox_mode="read-only"', 'analytics.enabled=false']:
        argv.extend(['-c', override])
    for feature in c.DESATIVAR:
        argv.extend(['--disable', feature])
    argv.append('D38_SENTINELA_PAYLOAD_ARTIFICIAL')
    cp = subprocess.run(argv, cwd=work, env=c.ambiente_filho(), capture_output=True, timeout=30)
    c.salvar(OUT / 'contexto-ajustes-aplicados-stdout.json', cp.stdout)
    c.salvar(OUT / 'contexto-ajustes-aplicados-stderr.bin', cp.stderr)
    assert cp.returncode == 0
    messages = json.loads(cp.stdout)
    texts = [part['text'] for message in messages for part in message.get('content', []) if 'text' in part]
    text = '\n'.join(texts)
    assert 'D38_SENTINELA_AGENTS_NAO_CARREGAR' not in text
    assert 'D38_SENTINELA_PAYLOAD_ARTIFICIAL' in text
    c.salvar_json(OUT / 'contexto-ajustes-aplicados.json', {
        'argv': argv, 'retorno': cp.returncode, 'stdout_sha256': c.montagem.sha(cp.stdout),
        'papeis': [message.get('role') for message in messages],
        'partes_developer': sum(len(m.get('content', [])) for m in messages if m.get('role') == 'developer'),
        'sentinela_agents_presente': False, 'sentinela_payload_presente': True,
        'environment_context_presente': '<environment_context>' in text,
        'instrucoes_skills_automaticas_presentes': '<skills_instructions>' in text,
        'tem_tools_ou_instructions_no_envelope': False,
        'limite': 'render de input; nao inventario tools nem instructions do request; debug nao aceita ignore-user-config'})
    sources = []
    for path in [Path('C:/ProgramData/OpenAI/Codex/config.toml'),
                 Path('C:/ProgramData/OpenAI/Codex/requirements.toml'),
                 Path('C:/Users/User/.codex/config.toml'),
                 ROOT / '.codex/config.toml', ROOT.parent / '.codex/config.toml']:
        record = {'arquivo': str(path), 'existe': path.is_file()}
        if path.is_file():
            raw = path.read_bytes()
            obj = tomllib.loads(raw.decode('utf-8-sig'))
            record.update(sha256=c.montagem.sha(raw), chaves_raiz=sorted(obj))
            record['instrucoes'] = {key: {'presente': bool(obj.get(key)),
                                          'sha256': c.montagem.sha(c.serial(obj[key])) if obj.get(key) else None}
                                    for key in ('developer_instructions', 'additional_developer_instructions',
                                                'model_instructions_file', 'instructions')}
        sources.append(record)
    c.salvar_json(OUT / 'fontes-configuracao-metadados.json', sources)
    c.salvar_json(OUT / 'subprocesso-solicitado.json', {
        'argv': c.comando_codex(shutil.which('codex'), '<ambiente-novo>'),
        'ambiente_chaves': sorted(c.ambiente_filho()), 'configuracao': c.configuracao_fixa(),
        'exec_iniciado': False, 'llm_chamado': False,
        'limite': 'argv/env na fronteira do coletor; configuracao runtime de exec ainda nao observada'})
    print('Parsing aceito; contexto adicional permanece; nenhum exec/LLM.')


if __name__ == '__main__':
    main()
