"""Reconciliação documental T030–T035, condicionada a evidências reais já salvas."""
import hashlib
import json
import pathlib
import re
import subprocess

ROOT = pathlib.Path(__file__).resolve().parents[3]
AREA = ROOT / 'evidencias/spec003'
FINAL = AREA / 'rodada-final'
manifest = json.loads((FINAL / 'manifesto.json').read_text(encoding='utf-8'))
rows = json.loads((FINAL / 'resultados.json').read_text(encoding='utf-8'))
synthetic = json.loads((AREA / 'sintetico-final-green/comando.json').read_text(encoding='utf-8'))
assert manifest['codigo_saida'] == 0 and manifest['resumo']['conformes'] == 48
assert len(rows['baseline']) == 12 and len(rows['variantes']) == 48
assert all(r['estado'] == 'conforme' for r in rows['baseline'] + rows['variantes'])
assert manifest['integridade'] and synthetic['retorno'] == 0
assert manifest['suite_baseline']['metodos_descobertos'] == 18
assert manifest['diagnostico']['total'] == 0
for name, digest in manifest['hashes_fechamento'].items():
    assert hashlib.sha256(pathlib.Path(name).read_bytes()).hexdigest() == digest, name
for name, digest in manifest['logs'].items():
    assert hashlib.sha256((FINAL / name).read_bytes()).hexdigest() == digest, name
subprocess.run(['git', 'diff', '--exit-code', manifest['baseline_commit'], '--',
                'autorizacao.py', 'tests/test_autorizacao.py',
                'materiais/modelos/referencia_candidata_NAO_ENVIAR_AO_LLM.json'], cwd=ROOT, check=True)

note = ('> Estado vigente — 21/10/2026 (D-20/D-21): Spec 003 implementada e verificada; '
        '35/35 tarefas concluídas com evidências. Quatro variantes independentes de B '
        '`aec474bcb54d6dae2afceff8e5b9226991386490`, uma edição por fonte, diffs/AST e revisão registrados. '
        'Python 3.13.3: suíte original 18 métodos OK, baseline 12/12 pares e variantes 48/48 conformes '
        'por decisão/motivo, zero divergências/erros/lacunas; 17 métodos sintéticos separados da bancada. '
        'Baseline, testes, materiais, referência candidata 0.2 e seleções 2/4/8/5 preservados. '
        'Evidências e diagnóstico do mecanismo: `specs/003-mudancas-controladas/evidencias.md` (desde a raiz). '
        'P-01/P-02/P-03, revisão das expectativas T12 e adoção constitucional pendentes; '
        'T12 já adotado/verificado em B. Revisão profissional, possíveis novos modelos e métricas '
        'aguardam transcrição da orientação e decisão explícita. Sem piloto, coleta ou LLM. '
        'Próxima ação: revisão humana das evidências e da referência candidata, seguida de detalhamento '
        'da orientação; nenhuma etapa experimental liberada. Registros anteriores abaixo são históricos.')

files = ['AGENTS.md', 'ESTADO_ATUAL.md', 'HANDOFF.md', 'BLOQUEIOS.md',
         'documentacao/contexto-e-escopo.md', 'documentacao/arquitetura.md',
         'documentacao/qualidade-e-testes.md', 'documentacao/roadmap.md',
         'specs/003-mudancas-controladas/spec.md', 'specs/003-mudancas-controladas/plan.md',
         'specs/003-mudancas-controladas/data-model.md',
         'specs/003-mudancas-controladas/contracts/verificacao.md',
         'specs/003-mudancas-controladas/quickstart.md']
for relative in files:
    path = ROOT / relative
    old = path.read_text(encoding='utf-8')
    assert not old.startswith(note), 'Fechamento documental já aplicado'
    path.write_text(note + '\n\n' + old, encoding='utf-8')

# T034 pede atualização das notas da checklist; seus 23 marcadores de qualidade não mudam.
checklist = ROOT / 'specs/003-mudancas-controladas/checklists/requirements.md'
old = checklist.read_text(encoding='utf-8')
markers = re.findall(r'^- \[[ xX]\].*', old, re.M)
new = ('> Complemento de execução — 21/10/2026, D-20/D-21: implementação autorizada e concluída. '
       'Baseline 18 métodos/12 pares e variantes 48 pares conformes; 17 métodos sintéticos separados. '
       'Evidências em [evidencias.md](../evidencias.md). Marcadores abaixo conservam sua semântica '
       'de qualidade da especificação; não representam aprovação científica. Descrições de etapa '
       'somente documental abaixo são históricas.\n\n' + old)
assert re.findall(r'^- \[[ xX]\].*', new, re.M) == markers
checklist.write_text(new, encoding='utf-8')

task_path = ROOT / 'specs/003-mudancas-controladas/tasks.md'
tasks = task_path.read_text(encoding='utf-8')
tasks = re.sub(r'^- \[ \] (T\d{3})\b', r'- [x] \1', tasks, flags=re.M)
tasks = tasks.replace('## Estado da geração', '## Estado histórico da geração')
tasks = ('> Fechamento vigente — 21/10/2026 (D-20/D-21): 35/35 tarefas concluídas. '
         'Evidência por grupo em [evidencias.md](evidencias.md); código, testes e registros reais '
         'conferidos. Zero pendências funcionais identificadas. Referência candidata e pendências '
         'científicas preservadas; estados de geração/revisão abaixo são históricos.\n\n' + tasks)
task_path.write_text(tasks, encoding='utf-8')
assert len(re.findall(r'^- \[x\] T\d{3}\b', tasks, re.M)) == 35

decisions = ROOT / 'documentacao/decisoes.md'
old = decisions.read_text(encoding='utf-8')
entry = '''## Implementação e verificação da Spec 003 — 21/10/2026

**D-20 — Autorização do pesquisador.** Responsável: usuário/pesquisador; evidência: pedido explícito nesta conversa para implementar as 35 tarefas, preservar alterações locais/B/T01–T12, executar baseline e 48 comparações por decisão/motivo, investigar divergências sem ajustar automaticamente expectativas e reconciliar documentação. Não autoriza piloto, LLM, novos modelos ou alterações nas métricas; não aprova cientificamente a referência nem ratifica a constituição.

**D-21 — Fechamento de engenharia pelo assistente.** Spec 003 confirmada pelo resolvedor; checklist 23/23 satisfeita. HEAD inicial `8041b0b1deca09f13c8b95069699616c7a1a7a60`; sete alterações documentais locais preservadas e arquivadas com hashes em `evidencias/spec003/preparacao/`. B confirmado, sem redefinição por HEAD. Quatro extrações independentes do mesmo blob; cada fonte possui só a edição do plano, diff/AST/revisão e hashes. Manifestos identificam HEAD, estado local e snapshots dos arquivos novos executados, sem pressupor commit da implementação.

Execução Python 3.13.3: primeira integração US2 e rodada final em pastas distintas; cada uma com 18 métodos originais OK, 12/12 pares B e 48/48 pares reais de variantes conformes. Zero divergências/erros/lacunas na bancada. T07/MC-04 muda apenas motivo; T12/MC-03 executado sem filtro. Controles sintéticos separados, 17 métodos finais OK, sem compor os 48 pares. Originais, comandos/retornos/stdout/stderr, fontes, hashes e diffs preservados. [Relatório e rastreabilidade](../specs/003-mudancas-controladas/evidencias.md).

Desvio de engenharia M-01 encontrado em controles adicionais: o fechamento não revalidava fonte/log entre execução e consolidação. Dois testes sintéticos reproduziram código 0 indevido. Correção: revalidar hashes/arquivos no fechamento e retornar 2 com integridade inválida. Falhas originais e versão corrigida arquivadas em `sintetico-integridade-final-red/` e `sintetico-final-green/`; rodada final posterior integral conforme. Não houve alteração no gabarito, na política ou nas variantes para acomodar resultados. Nenhuma suspeita de erro na referência foi identificada; T031 concluída pela conferência de ausência de ocorrência, sem inventar revisão/resolução.

35 tarefas concluídas com vínculos a evidências; baseline/testes/materiais/referência 0.2 e conjuntos 2/4/8/5 preservados. P-01/P-02/P-03, expectativas T12 e adoção constitucional continuam pendentes. T12 já adotado em B; não pedir nova adoção. Revisão profissional, possíveis novos modelos e mudanças nas métricas aguardam transcrição da orientação e decisão explícita. Textos datados da referência de B são preservados como fonte histórica; observações novas ficam nas evidências externas à referência. Próxima ação: revisão humana, sem liberar etapas experimentais.

'''
decisions.write_text(old.replace('# Decisões, propostas e pendências\n', '# Decisões, propostas e pendências\n\n' + entry, 1), encoding='utf-8')

quickstart = ROOT / 'specs/003-mudancas-controladas/quickstart.md'
with quickstart.open('a', encoding='utf-8') as stream:
    stream.write('''

## Execução concluída — 21/10/2026

Comando final: `python -B verificacao_variantes.py --saida evidencias/spec003/rodada-final`, na raiz do projeto, Python 3.13.3. Código 0; baseline 18 métodos/12 pares conformes, variantes 48/48 conformes; zero divergências/erros/lacunas, hashes intactos. Para repetir, usar outro nome de pasta; uma tentativa existente é recusada.

Controles sintéticos: `python -B -m unittest discover -s tests -p test_variantes.py -v`, 17 métodos OK em `evidencias/spec003/sintetico-final-green/`. Não compõem os 48 pares. [Relatório completo](evidencias.md) registra fases, versões, M-01 e resolução, diffs e evidências originais. Sem suspeita de erro de expectativa; revisão científica pendente. Comandos e descrições futuras datadas acima documentam o planejamento anterior.
''')

print('Documentação reconciliada; 35 tarefas marcadas com evidências verificadas.')
