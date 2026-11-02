"""Emite patch documental D-29/D-30, sem alterar fontes ou evidencias anteriores."""
import difflib
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
SPEC='specs/004-preparacao-avaliacao-ids/'
STAGE='evidencias/spec004/revisao-textual-2026-11-01/'
changes={}
def change(path,fn):
    old=(ROOT/path).read_text(encoding='utf-8');changes[path]=(old,fn(old))
def replace_once(text,old,new):
    assert text.count(old)==1,(old,text.count(old))
    return text.replace(old,new,1)

closing='''
## Verificação vigente — 01/11/2026 (D-30)

Engenharia offline do contrato D-29 concluída no alcance verificado: 49 tarefas vigentes atendidas; T014/T015 substituídas, não executadas/aprovadas. Recortes das seis fontes, autorização externa e montagem v3 produziram 16 pacotes; bytes, conteúdo, documentos comuns, notas D1/E1 e ausência de notas D0/E0 confrontados. Referência somente no avaliador separado; resposta de demonstração explicitamente sintética. As 16 famílias estão consolidadas com evidências anteriores preservadas e verificações necessárias das alterações; não se reexecutou pontuação inalterada nem se contou sintéticos como LLM.

RELATORIO inclui comandos, esperado/observado, hashes, matriz, caminhos suportados, limitação da criação de symlink e provas de SO substituídas. As seções de 27/10 são históricas; os gates atuais são D-29 e esta verificação, sem aprovação retroativa. Checklist é qualidade documental, preservada sem remarcação. Sem prova de entrega real ao modelo, modelo escolhido, chamada externa ou piloto. Revisão profissional/científica, notas definitivas, fundamentação das métricas, desenho final/congelamento do piloto e adoção constitucional permanecem pendentes.
'''
for name in ('spec.md','plan.md','research.md','data-model.md','contracts/preparacao-avaliacao.md','quickstart.md','tasks.md'):
    path=SPEC+name
    report=('../../../' if name.startswith('contracts/') else '../../')+STAGE+'relatorio.md'
    def transform(text,name=name,report=report):
        text=text.replace('Isolamento real não demonstrado; T014/T015 e dependentes permanecem pendentes.',
          'Registro de 27/10: isolamento por SO não demonstrado; exigência substituída por D-29, sem aprovação retroativa.')
        text=text.replace('## Estado técnico parcial — 27/10/2026','## Histórico técnico parcial — 27/10/2026 (substituído no alcance de D-29)')
        if name=='spec.md':
            text=replace_once(text,'**Status**: Rascunho revisado documentalmente; somente especificação, sem implementação ou execução.',
              '**Status**: Engenharia offline implementada/verificada sob D-29/D-30; protocolo científico permanece rascunho. O escopo de somente especificação abaixo é histórico da criação.')
            text=text.replace('Lista/recortes revisados e isolamento demonstrado são critérios futuros.',
              'Recortes e pacote textual têm conferência técnica D-30; revisão profissional/científica e entrega real sem acesso adicional continuam critérios futuros, sem gate de SO.')
        if name=='plan.md':
            text=text.replace('Gates de isolamento implementado, referência/notas revisadas e métricas fundamentadas continuam não atendidos para pesquisa;',
              'Gates de revisão profissional/científica, entrega textual efetiva sem ferramentas e desenho final do piloto continuam não atendidos para pesquisa;')
        if name=='quickstart.md':
            text=text.replace('# Guia de validação futura — Spec 004','# Guia de consulta e validação local — Spec 004')
            text=text.replace('## Pré-condições','## Histórico de planejamento e comandos v2 — 27/10/2026\n\nOs comandos desta seção pertencem ao contrato antigo. Não os reutilizar para montagem v3: a autorização externa agora é obrigatória. Comandos vigentes e evidências D-30 estão ao final.\n\n## Pré-condições',1)
        return text+'\n'+closing.replace('RELATORIO','[Relatório e limitações]('+report+')')
    change(path,transform)

path=SPEC+'tasks.md';old,text=changes[path]
text=replace_once(text,'**Data**: 27/10/2026. **Estado vigente**: 39 tarefas independentes concluídas com evidências; 9 pendentes por isolamento e dependências de fechamento. Não há fechamento integral. A geração anterior foi somente documental; implementação posterior autorizada em D-26/D-27.',
  '**Data de criação**: 27/10/2026. **Estado vigente — 01/11/2026, D-29/D-30**: 49 tarefas vigentes concluídas no contrato de engenharia offline; 2 exigências históricas substituídas (T014/T015), mantidas desmarcadas e sem aprovação. Entrega real e pesquisa não executadas. Implementação autorizada em D-26/D-27 e revista em D-29.')
text=text.replace('**Autorização desta entrega**:', '**Autorização histórica da geração — 27/10/2026**:',1)
text=text.replace('Comandos/testes destas tarefas são futuros e dependem de pedido próprio de implementação/verificação.',
  'Implementação/verificações autorizadas posteriormente em D-26/D-29; resultados históricos e atuais vinculados ao final.')
text=text.replace('IDs T001–T048 são locais desta Spec','IDs T001–T051 são locais desta Spec')
text=text.replace('Zonas restritas reais ficam fora do contexto de desenvolvimento, com caminhos explicitamente registrados no futuro; não presumir ACL por nome de pasta.',
  'Na revisão D-29, exportador editorial local `fontes_autorizadas.py`, pacote plano e autorização externa; somente payload se destina ao modelo. Não criar zonas/contas/ACL para isolamento.')
text=text.replace('**Objetivo:** preparar futura execução autorizada sem perder contexto/artefatos. Ainda não executado.',
  '**Objetivo:** preservar contexto e artefatos; execução histórica e revisão atual registradas nas evidências.')
text=text.replace('**Goal:** montar entrada íntegra de uma mudança/condição, conferindo lista, revisão técnica, conteúdo/versões e isolamento.',
  '**Goal:** montar entrada íntegra de uma mudança/condição, conferindo fontes/recortes, autorização externa, conteúdo/versões e limite textual sem ferramentas.')
text=text.replace('**Independent Test:** usar pacotes fictícios e S-14, conferindo bytes esperados e recusas, sem avaliador/referência. Conclusão integral exige prova real de acesso; resultado lógico isolado não equivale a US1 concluída.',
  '**Independent Test:** S-14 textual, fontes reais autorizadas e negativos fictícios, conferindo bytes, recortes e recusas sem referência. T049/T050 substituem a prova por identidade; não demonstram envio remoto ou isolamento de SO.')
text=text.replace('com `--pacote`, `--manifesto`, `--saida` e códigos 0/2;',
  'com `--pacote`, `--manifesto`, `--autorizacao` externa obrigatória (v3), `--saida` e códigos 0/2;')
text=text.replace('em `evidencias/spec004/integracao/diagnostico.md`','em `'+STAGE+'diagnostico.md`')
text=text.replace('em `evidencias/spec004/fechamento/relatorio.md`','em `'+STAGE+'relatorio.md`')
text=text.replace('em `evidencias/spec004/fechamento/preservacao.json`','em `'+STAGE+'preservacao.json`')
text=text.replace('`plan.md`, `checklists/requirements.md` e `quickstart.md`, preservando histórico',
  '`plan.md` e `quickstart.md`, conferindo `checklists/requirements.md` como gate documental somente leitura, preservando histórico')
text=text.replace('                    │                                      └─ T014→T015 (acesso real)',
  '                    │                                      └─ T049→T050/T051 (contrato textual)')
text=text.replace('T013 + T015 + US2 + US3 + T041 → T042→T043→T044→T045→T046→T047→T048',
  'T013 + T049/T050/T051 + US2 + US3 + T041 → T042→T043→T044→T045→T046→T047→T048')
text=replace_once(text,'T014/T015 podem ser preparados após T012; requerem identidade/autorização operacional e execução externa ao contexto amplo. Falta de ambiente não bloqueia US2/US3 com preparação literal, mas impede concluir US1/S-14/integração completa.',
  'T014/T015 foram substituídas por D-29 e não integram o caminho ativo: não criar identidade nem retomar a prova de SO. T049/T050/T051 verificam recortes, montagem, caminhos e avaliação separada; envio real permanece fora desta etapa.')
text=text.replace('**MVP primeiro:** fundação e US1, com pacote fictício, conteúdo exato e prova de isolamento. Se só controles lógicos passarem, denominar resultado parcial; não chamar MVP integral nem liberar envio.',
  '**MVP primeiro:** fundação e US1, com recortes reais, negativos fictícios, conteúdo exato e contrato textual D-29. Aceitação local não libera envio ou pesquisa.')
text=text.replace('| FR-002 | T009, T012, T014–T015, T028, T033 | Isolamento real ainda sem evidência |',
  '| FR-002 | T009, T012, T028, T033, T049–T051 | Referência separada; limite textual local, envio não exercitado |')
text=text.replace('| FR-003 | T002, T006–T009, T014–T015 |', '| FR-003 | T002, T006–T009, T049–T050 |')
text=text.replace('| FR-012 | Escopo desta entrega, T001–T002, T044–T048 | Limites temporais da Spec superados apenas pelo pedido atual de tarefas/análise |',
  '| FR-012 | T001–T002, T044–T051 | Limites temporais superados apenas pelas autorizações D-26/D-29; sem pesquisa |')
text=text.replace('| SC-001 | T006–T015, T042, T044 | Sem prova real não concluir isolamento |',
  '| SC-001 | T006–T013, T042, T044, T049–T051 | Recortes/bytes/caminhos/condições/recibo local; nenhuma alegação de SO |')
text=text.replace('| SC-006 | T003–T005, T015, T042–T044 |','| SC-006 | T003–T005, T042–T044, T049–T051 |')
text=text.replace('**48 tarefas: 39 concluídas e 9 pendentes**',
  '**48 IDs originais (situação histórica: 39 concluídos/9 pendentes em 27/10); revisão D-29 acrescenta T049–T051: 51 IDs, 49 vigentes concluídos e 2 substituídos sem aprovação**')
text=text.replace('**Pendentes:** T014/T015', '**Pendentes à data de 27/10 (histórico, substituído por D-29/D-30):** T014/T015')
text=text.replace('**Testes atuais:** 14 métodos', '**Testes à data de 27/10 (histórico):** 14 métodos')
for number in (*range(42,49),49,50,51):
    text=replace_once(text,f'- [ ] T{number:03}',f'- [x] T{number:03}')
text+='''
Aceitação das tarefas atuais: T049/T050 — recortes-primeira, montagem-revisada e demonstracao-textual-001; T051 — entrada-avaliador e demonstração separada; T042/T044 — matriz.json e relatório critério a critério; T043 — diagnostico.md; T045 — preservacao.json; T046 — reconciliação e checklist intacta; T047 — D-30/governança; T048 — estado-tarefas.json e limites do relatório. Todos os caminhos de evidência são relativos a `evidencias/spec004/revisao-textual-2026-11-01/`. T014/T015 permanecem desmarcadas exclusivamente como exigências substituídas, não pendências para provisionamento.
'''
changes[path]=(old,text)

prefix='''> Estado vigente — 01/11/2026 (D-29/D-30): Spec 004 confirmada ativa; contrato de texto preparado sem ferramentas/acesso adicional do modelo. Engenharia offline verificada: 49 tarefas vigentes concluídas; T014/T015 substituídas, não executadas/aprovadas. [Evidências, comandos e limites](evidencias/spec004/revisao-textual-2026-11-01/relatorio.md). Fontes/recortes autorizados, 16 pacotes, condições/notas equivalentes, bytes exatos e avaliação separada conferidos; resposta de demonstração sintética, sem resultado de LLM. Não se alega isolamento por SO. Gabarito, notas e evidências anteriores preservados.

Próxima ação: revisão humana/profissional/científica da referência, notas/prompts, métricas e desenho final do piloto. Entrega real dos bytes ao modelo e ausência efetiva de ferramentas na plataforma ainda não exercitadas; conferir antes de qualquer piloto, sob autorização própria. Sem escolha de modelo, chamada externa ou piloto nesta etapa. Notas definitivas e adoção constitucional continuam pendentes. Runner restrito/ACL do Windows deixaram de ser exigência por D-29; não criar contas/permissões. PONT-01/PONT-02 continuam convenções candidatas, sem revisão científica presumida.

## Histórico preservado (afirmações de estado abaixo valem nas respectivas datas)

'''
for path in ('AGENTS.md','ESTADO_ATUAL.md','BLOQUEIOS.md','HANDOFF.md'):
    change(path,lambda text:prefix+text)
decision='''
## Verificação de engenharia do contrato textual — 01/11/2026

**D-30 — Registro técnico do assistente sob autorização D-29, sem decisão científica.** Preparação editorial por seis fontes/recortes fixos e montagem v3 com autorização externa; 16 pacotes das quatro mudanças/condições confrontados byte a byte, documentos comuns equivalentes, mesmas notas literais D1/E1 e nenhum bloco de notas D0/E0. Inspeção dos recortes/campos exclui código, histórico, referência de seleção e resultados de variantes; saídas esperadas da baseline são parte do catálogo permitido. Referência acessada apenas no avaliador separado; resposta demonstrativa sintética preservada. [Relatório](../evidencias/spec004/revisao-textual-2026-11-01/relatorio.md), [matriz](../evidencias/spec004/revisao-textual-2026-11-01/matriz.json), [preservação](../evidencias/spec004/revisao-textual-2026-11-01/preservacao.json).

Verificações necessárias: quatro métodos de recortes aprovados; montagem sete aprovados e um ignorado por WinError1314 (symlink real); sete métodos dirigidos de caminhos/importação/CLI aprovados. Junctions reais recusadas. Sem conta, ACL, elevação ou contorno de restrição. Pontuação/PONT-01/PONT-02 inalteradas por comparação de AST; controles/esperados anteriores mantidos com versões/hashes, sem reexecutar suíte inalterada. 49 tarefas vigentes concluídas no alcance offline, 2 substituídas mantidas desmarcadas. O contrato antigo não foi satisfeito retroativamente; nenhuma prova de identidade ou symlink ignorada virou aprovada.

Envelope local registra somente payload, ferramentas/anexos vazios e envio não realizado. Não é prova de configuração/entrega em plataforma externa; não há modelo selecionado, chamada ao LLM ou piloto. Referência candidata e todas as notas permanecem intactas; notas atuais representam conhecimento de analista, ainda rascunho. Revisão profissional/científica, fundamentação de métricas, notas definitivas, desenho final/congelamento do piloto e adoção constitucional continuam pendentes. As afirmações de bloqueio Windows em D-28 abaixo descrevem o contrato histórico, substituído por D-29.

'''
change('documentacao/decisoes.md',lambda text:replace_once(text,'## Revisão parcial de engenharia da Spec 004 — 27/10/2026',decision+'## Revisão parcial de engenharia da Spec 004 — 27/10/2026'))

print('*** Begin Patch')
for path,(old,new) in changes.items():
    if old==new:continue
    print('*** Update File: '+str(ROOT/path))
    for line in list(difflib.unified_diff(old.splitlines(),new.splitlines(),n=3))[2:]:
        print('@@' if line.startswith('@@') else line)
print('*** End Patch')
