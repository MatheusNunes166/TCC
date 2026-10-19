> Fechamento — 18/10/2026: T001–T022 concluídas. [Evidências por tarefa, comandos e relatório bruto](quickstart.md). T12 não adotado nem executado.

# Tasks: Herança de um nível e incompatibilidade efetiva

**Input**: [Spec](spec.md), [plano](plan.md), [research](research.md), [modelo](data-model.md), [contrato](contracts/autorizacao.md) e [guia](quickstart.md).
**Prerequisites**: Spec ativa confirmada em `specs/002-heranca-incompatibilidade` por `setup-tasks.sh --json`, em 16/10/2026. Histórico de 16/10: autorização limitada a tarefas/análise. Pedido de 18/10 autoriza implementação e testes locais (D-13).
**Tests**: exigidos pela Spec. As 22 tarefas estão concluídas com evidências reais em [quickstart.md](quickstart.md), seções identificadas por tarefa. Evidências do incremento 1 continuam históricas.
**Organization**: US1 = acesso herdado; US2 = incompatibilidade efetiva; US3 = preservação do primeiro incremento. Todas P1, executadas na ordem de dependência.

## Format: `[ID] [P?] [Story] Description`

T001–T022 são IDs locais de tarefas; T01–T11 são casos do catálogo. Caminhos partem da raiz `tcc-impacto-llm/`. Sem `[P]`: as histórias compartilham os mesmos dois arquivos e dependem da integração anterior.

## Phase 1: Setup

- [x] T001 Confirmar Spec ativa e Python 3.11+ antes da implementação autorizada; registrar data, comando, versão real e revisão inicial em `specs/002-heranca-incompatibilidade/quickstart.md`. Reaproveitar evidências do incremento 1 como histórico, sem afirmar que demonstram RF-03/RF-04 e sem instalar dependências externas.

## Phase 2: Foundational

- [x] T002 Confrontar `autorizacao.py` e `tests/test_autorizacao.py` com `specs/002-heranca-incompatibilidade/contracts/autorizacao.md`; registrar em `specs/002-heranca-incompatibilidade/quickstart.md` o inventário dos dez métodos existentes, sete IDs e controles preservados, assinaturas e domínio parcial atual. Fixar como precondições do desenho: estado str `ativa/suspensa/em_revisao`, papéis `frozenset[str]` de Consulta/Auditoria/Supervisão inclusive vazio, operação str `visualizar/exportar`, resultado `dict[str, str]` com exatamente `decisao` e `motivo`; sem novas guardas/erros para malformados. Não ampliar a garantia da função antes da integração.

## Phase 3: US1 — Reconhecer acesso herdado (P1)

**Goal**: RF-03, preservando concessões próprias e bloqueio de estado.
**Independent Test**: T05/T08, T10 e auxiliar de efetivos; sem depender de conflito para Supervisão isolada.

- [x] T003 [US1] Acrescentar em `tests/test_autorizacao.py` dois métodos identificados T05 (ativa, Supervisão, visualizar → permitir/permissao_herdada) e T08 (ativa, Supervisão, exportar → negar/sem_permissao); comparar dicionários completos, manter T10 esperando negar/estado. Cobrir SC-001 e parte de SC-003/SC-005.
- [x] T004 [US1] Escrever em `tests/test_autorizacao.py` verificação tabelada de `obter_papeis_efetivos` para os oito subconjuntos: preservar todos os atribuídos e acrescentar somente Consulta quando houver Supervisão; esperados explícitos independentes da implementação. Conferir retorno `frozenset[str]`, entrada intacta e chamadas repetidas; não criar IDs T adicionais.
- [x] T005 [US1] Executar seletivamente os testes US1 novos antes da implementação e registrar comando, métodos/subtestes, resultados e diagnóstico real em `specs/002-heranca-incompatibilidade/quickstart.md`. Distinguir interface ausente, divergência de motivo e erro de ambiente. T08 pode já passar incidentalmente; não exigir falha artificial nem tratar isso como prova de herança.
- [x] T006 [US1] Implementar em `autorizacao.py` a função pura `obter_papeis_efetivos(papeis)`: união imutável dos atribuídos com Consulta se Supervisão presente, sem recursão, Auditoria herdada, política mutável ou remoção de atribuídos. Preservar semântica e assinatura de `obter_permissoes_diretas`.
- [x] T007 [US1] Integrar RF-03 em `autorizar` de `autorizacao.py`: estado encerra primeiro; calcular diretas dos atribuídos e disponibilidade consultando as concessões dos efetivos; preferir motivo direto, depois herdado, depois ausência. Não classificar disponibilidade dos efetivos como origem direta. Documentar que US2 está pendente e não declarar garantia integrada para combinações com conflito.
- [x] T008 [US1] Executar a seleção US1 e os testes anteriores preservados de `tests/test_autorizacao.py`; registrar em `specs/002-heranca-incompatibilidade/quickstart.md` T05/T08/T10, oito subtestes de efetivos e regressão observada. Resolver falhas antes de avançar; comprovar SC-001 sem declarar RF-04 pronto.

## Phase 4: US2 — Bloquear incompatibilidade efetiva (P1)

**Goal**: RF-04 sobre efetivos, antes de decidir pela permissão.
**Independent Test**: T06 verifica conflito direto; T07 integra herança; T11 preserva estado. Depende de US1 para integração herdada.

- [x] T009 [US2] Acrescentar em `tests/test_autorizacao.py` métodos T06 (ativa, Consulta+Auditoria, visualizar → negar/conflito) e T07 (ativa, Supervisão+Auditoria, visualizar → negar/conflito), com dicionários completos; conservar T11 negar/estado. Cobrir SC-002 e parte de SC-003/SC-005.
- [x] T010 [US2] Escrever em `tests/test_autorizacao.py` verificação de `ha_incompatibilidade` nos oito subconjuntos recebidos como papéis efetivos; retorno bool verdadeiro somente quando Consulta e Auditoria coexistem. Esperados independentes; não expandir herança no predicado. Conferir entradas intactas e repetição. Não executar autorização exportar de Supervisão+Auditoria (T12).
- [x] T011 [US2] Executar seletivamente os testes US2 novos antes de implementar conflito; registrar em `specs/002-heranca-incompatibilidade/quickstart.md` capacidades ausentes e resultados reais, separando preparação/importação de divergência funcional. Não converter descoberta vazia em sucesso.
- [x] T012 [US2] Implementar em `autorizacao.py` a função pura `ha_incompatibilidade(papeis_efetivos)`, verificando presença conjunta de Consulta e Auditoria, independentemente da operação e sem expandir herança ou introduzir outros conflitos.
- [x] T013 [US2] Integrar em `autorizacao.py` a incompatibilidade após calcular os efetivos e antes das decisões por permissão, retornando negar/conflito mesmo com concessão; preservar estado primeiro, direta antes de herdada e ausência por último. Manter exatamente duas strings nas chaves `decisao`/`motivo` e nenhuma operação externa.
- [x] T014 [US2] Executar testes US2 e regressão US1/primeiro incremento de `tests/test_autorizacao.py`; registrar resultados em `specs/002-heranca-incompatibilidade/quickstart.md`, incluindo T06/T07/T11 e oito subtestes do predicado. Revisar em `autorizacao.py` estado → conflito → decisão de permissão; resolver falhas antes de avançar.

## Phase 5: US3 — Preservar o primeiro incremento (P1)

**Goal**: completar integração com regressão e domínio ampliado explícito.
**Independent Test**: sete casos anteriores, controles originais e bordas da Spec; integração completa depende de US1/US2.

- [x] T015 [US3] Preservar em `tests/test_autorizacao.py` os dez métodos existentes e suas expectativas: sete casos T01/T02/T03/T04/T09/T10/T11, 32 combinações não ativas, três concessões próprias (Consulta visualizar, Auditoria exportar, Supervisão vazio) e Auditoria/visualizar negar/sem_permissao. Acrescentar quatro combinações auxiliares: ativa sem papéis nas duas operações → negar/sem_permissao; ativa Supervisão+Consulta visualizar → permitir/permissao_direta e exportar → negar/sem_permissao. Conferir entradas intactas e repetição, sem novos IDs T. SC-004/SC-006 e preservação SC-003.
- [x] T016 [US3] Executar os controles de `tests/test_autorizacao.py` e diagnosticar resultados em `specs/002-heranca-incompatibilidade/quickstart.md`; se falharem, corrigir somente desvios do contrato em `autorizacao.py` e repetir as verificações afetadas. Se já passarem, registrar conformidade sem inventar nova mudança funcional. Asserções novas podem passar por comportamento integrado anterior.
- [x] T017 [US3] Atualizar documentação do domínio em `autorizacao.py` e revisar `specs/002-heranca-incompatibilidade/contracts/autorizacao.md`: futuro suporte integrado aos três estados, oito subconjuntos e duas operações; conservar assinaturas anteriores, funções puras, retornos imutáveis e vocabulário de cinco motivos. Não preservar resultados incidentais fora do domínio antigo nem adicionar política para entradas inválidas. Só declarar capacidade verificada depois de T018.
- [x] T018 [US3] Executar `python -m unittest discover -s tests -p 'test_*.py' -v` e registrar relatório bruto, versão/data/revisão/comando e contagens reais em `specs/002-heranca-incompatibilidade/quickstart.md`. Exigir T01–T11 presentes, 11/11 dicionários conformes, controles e auxiliares conformes, nenhum erro/falha/ignorado e descoberta não vazia; conferir SC-001–SC-006. Separar métodos, casos e subtestes: dez métodos preservados + quatro IDs novos, além dos controles novos. Não executar matriz de autorizar que inclua T12, variantes ou piloto.

## Phase 6: Polish & Cross-Cutting Concerns

- [x] T019 Revisar alterações de `autorizacao.py` e `tests/test_autorizacao.py` contra `specs/002-heranca-incompatibilidade/spec.md`, `plan.md` e `contracts/autorizacao.md`: expansão de um nível, preservação dos atribuídos, conflito efetivo, precedência, origem direta prioritária, saída exata, pureza, domínio e ausência de T12/variantes. Registrar revisão/diff e lacunas em `specs/002-heranca-incompatibilidade/quickstart.md`; não redefinir contrato ou gabarito silenciosamente.
- [x] T020 Consolidar em `specs/002-heranca-incompatibilidade/quickstart.md` evidências de T005/T008/T011/T014/T016/T018/T019 e vínculos com SC-001–SC-006; registrar falhas/resoluções e resultados observados separadamente das metas. Repetir testes somente por alteração ou dúvida concreta. Não marcar tarefas sem prova correspondente nem afirmar cobertura total da bancada.
- [x] T021 Atualizar `documentacao/arquitetura.md`, `documentacao/qualidade-e-testes.md` e `documentacao/decisoes.md` com implementação versus planejamento e evidências da integração; preservar catálogo/gabarito e D-09/P-01/P-02/P-03/P-04 como aplicáveis. Registrar T12 somente proposto; eventual adoção exige relevância nas quatro mudanças e recálculo de tamanho/denominadores, não aprovação por consequência dos testes.
- [x] T022 Reconciliar `ESTADO_ATUAL.md`, `HANDOFF.md`, `BLOQUEIOS.md`, `documentacao/roadmap.md` e `specs/002-heranca-incompatibilidade/tasks.md` após revisão e evidências: marcar apenas concluídas comprovadas, declarar domínio real e pendências restantes; nenhuma nova etapa, variante, piloto ou coleta iniciada automaticamente. Incremento só fecha se onze casos e controles realmente conformes.

## Dependencies & Execution Order

Sequência deliberadamente linear: T001 → T002 → T003–T008 (US1) → T009–T014 (US2) → T015–T018 (US3) → T019–T022. Dentro de cada intervalo, seguir numeração. Testes antes da implementação correspondente, diagnóstico real, implementação, verificação e só depois integração/fechamento.

US1 é demonstrável isoladamente com Supervisão sem conflito, mas não encerra o incremento. US2 usa a expansão de US1 para T07. US3 preserva a base durante toda a implementação e finaliza aceitação integrada; não adiar a preservação das expectativas até sua fase.

### Parallel Opportunities / Examples

US1: T003/T004 compartilham testes, T006/T007 compartilham produção; manter sequencial. US2: T009/T010 e T012/T013 têm a mesma limitação. US3: escrita, execução e registro dependem dos resultados anteriores. Não há marcador `[P]` nem divisão de escrita paralela segura neste recorte. Uma revisão independente pode ser somente leitura, sem alterar a ordem de evidências.

## Implementation Strategy

MVP demonstrável: RF-03 com T05/T08 e estado preservado. Sem publicação ou garantia de conflito até US2. Entrega solicitada da Spec 002 exige US1/US2/US3, onze casos integrados, controles, evidências, revisão e atualização documental. Implementação autorizada em 18/10 por D-13 e concluída conforme evidências no quickstart.

T12 permanece proposta fora da aceitação e da execução planejada. As regras gerais do domínio o abrangem semanticamente, sem adotá-lo como cenário. Manter 11 casos/44 pares de variantes planejados na referência original; nenhuma variante será implementada aqui.

## Coverage Summary

| Critério/regra | Tarefas | Evidência futura |
|---|---|---|
| SC-001 / RF-03 herança | T003–T008, T018–T020 | T05/T08, efetivos imutáveis |
| SC-002 / RF-04 conflito efetivo | T009–T014, T018–T020 | T06/T07, predicado |
| SC-003 / regressão e integração | T002, T003, T008, T009, T014–T020 | Sete pares preservados e 11/11 |
| SC-004 / controles anteriores | T002, T008, T014–T016, T018–T020 | 32 estados, três concessões, Auditoria/visualizar |
| SC-005 / saída decisão e motivo | T003, T009, T013, T015, T018–T020 | Onze dicionários completos |
| SC-006 / vazio e origem direta prioritária | T007, T015–T020 | Quatro bordas, repetição e entradas intactas |
| RF-01/RF-04 precedência | T007–T014, T018–T020 | T10/T11, 32 estados e inspeção de ordem |
| RF-01–RF-04 domínio/pureza | T002, T006, T007, T012, T013, T017–T020 | Contrato ampliado sem novos erros ou política |
| Governança e limites | T001, T019–T022 | Evidências, documentação, T12 separado |

Contagem: 22 tarefas, todas concluídas com evidências em quickstart.md. Setup/fundação 2; US1 6; US2 6; US3 4; fechamento 4. A matriz mantém a rastreabilidade planejada; os resultados executados e SC-001–SC-006 estão no quickstart.
