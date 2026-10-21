# Tasks: Quatro mudanças controladas e verificação de efeitos

**Data**: 20/10/2026. **Feature ativa**: `specs/003-mudancas-controladas`.

**Revisão — 21/10/2026 (D-19)**: lista existente preservada, com 35 tarefas pendentes; somente T024 esclarecida para separar controles sintéticos e matriz real. Conferência documental de B realizada, sem concluir T001/T002, que exigem nova conferência na implementação. Revisão profissional, possíveis novos modelos e mudanças nas métricas aguardam a transcrição da orientação e decisão explícita; não são requisitos aprovados desta Spec.

**Input**: [Spec](spec.md), [plano](plan.md), [research](research.md), [modelo](data-model.md), [contrato](contracts/verificacao.md), [quickstart](quickstart.md), [checklist](checklists/requirements.md), governança e [referência candidata 0.2](../../materiais/modelos/referencia_candidata_NAO_ENVIAR_AO_LLM.json). Fluxo local: `.agents/skills/speckit-tasks/SKILL.md`, template resolvido por `setup-tasks.sh --json`.

**Estado desta entrega**: somente geração de tarefas e análise documental posterior, autorizadas pelo pesquisador em D-18. **Todas as 35 tarefas abaixo estão pendentes.** Nenhum código, variante, teste de aplicação ou execução sintética foi realizado. Sua execução depende de autorização própria; listar uma tarefa não a executa. Sem piloto/LLM experimental. Expectativas, conjuntos e revisões científicas preservados.

## Formato, caminhos e fontes

- IDs T001–T035 são tarefas locais; T01–T12 continuam sendo casos experimentais, sem novos IDs.
- `[US1]`, `[US2]`, `[US3]` correspondem às histórias/prioridades da Spec. `[P]` só indica arquivos distintos com pré-condições já atendidas; não autoriza delegação automática.
- Caminhos são relativos à raiz `tcc-impacto-llm`. `evidencias/spec003/<id_execucao>/` designa uma pasta nova por tentativa, nunca pasta existente a sobrescrever.
- B permanece **`aec474bcb54d6dae2afceff8e5b9226991386490`**. Extrair cada variante diretamente de B, nunca de outra variante ou do HEAD móvel. Fontes/esperados de B ficam intactos.
- Python + unittest e biblioteca padrão; nenhum banco, pacote extra, worktree, motor de políticas ou coletor experimental.
- Testes futuros são pedidos pela Spec/plano. Escrever os controles necessários antes da implementação correspondente, registrar falha inicial pertinente e verificar depois; não exigir falha artificial de comportamento que já esteja conforme. Fixtures sintéticas não integram os 48 pares reais.

## Phase 1: Setup — procedência e recorte

**Objetivo**: confirmar ambiente e fontes antes de qualquer nova implementação. Não instalar ferramentas ou refazer o projeto.

- [ ] T001 Confirmar `.specify/feature.json` → Spec 003, governança e autorização de implementação futura; conferir `git status`, HEAD, raiz/prefixo Git e disponibilidade de B, ler seus `autorizacao.py`, `tests/test_autorizacao.py` e JSON 0.2; informar alteração local relevante antes de incorporá-la, registrar inventário e procedência em `specs/003-mudancas-controladas/quickstart.md` sem declarar teste executado (FR-001/FR-003/FR-004).
- [ ] T002 Registrar inventário inicial de blobs/hashes e garantia de preservação de `autorizacao.py`, `tests/test_autorizacao.py`, materiais/referência e controles (18 métodos/T01–T12) em `specs/003-mudancas-controladas/quickstart.md`; delimitar arquivos futuros `variantes/`, `verificacao_variantes.py`, `tests/test_variantes.py` e saída `evidencias/spec003/`, sem alterar baseline, esperado ou seleção (FR-003/FR-004).

**Checkpoint**: B disponível, fontes necessárias identificadas, nenhuma alteração relevante local incorporada silenciosamente. Somente então iniciar a fundação.

## Phase 2: Foundational — fontes, referência e registros comuns

**Objetivo**: construir o suporte mínimo compartilhado às histórias, sem preparar políticas de variante nesta fase. Dependência: T001–T002.

- [ ] T003 Escrever em `tests/test_variantes.py` controles sintéticos de extração/identidade, referência inválida e diretório repetido; verificar rejeição de commit ausente, ID duplicado/inexistente, `expected` incompleto, saída fora da área e interceptação de código/referência; registrar execução inicial pertinente antes de implementar T004–T007 em `evidencias/spec003/<id_execucao>/`, identificada como sintética (FR-001/FR-004/FR-007).
- [ ] T004 Implementar em `verificacao_variantes.py` leitura Git em bytes com argumentos separados e raiz/prefixo reais, B fixo e objetos/SHA-256; materializar snapshot exclusivo de B, testes, fundamentos, variantes quando disponíveis e executor; recusar pasta existente/perigosa, sem remoção recursiva, normalização textual de BOM/CRLF ou dependência de HEAD como origem (FR-001/FR-003).
- [ ] T005 Implementar em `verificacao_variantes.py` validação do JSON de B: `versao = 0.2`, `status = CANDIDATO_NAO_REVISADO`, revisor/data nulos; “ID T01–T12 único”, estados ativa/suspensa/em_revisao, papéis canônicos sem duplicação e operação visualizar/exportar; “Exatamente quatro variantes com 12 expectativas cada” nos IDs MC-01/MC-02/MC-03/MC-04-v2; chaves/tipos/vocabulário e fundamentos documentais coerentes, sem editar referência, gerar esperado com o núcleo ou filtrar por `tests/changed/preserved` (FR-004/FR-005).
- [ ] T006 Implementar em `verificacao_variantes.py` o manifesto de `evidencias/spec003/<id_execucao>/manifesto.json` com `schema_version = 1`, ID/início/fim UTC, comando/argumentos/cwd/plataforma/Python, commit/estado/hashes e snapshot do executor/testes novos, fontes de B e variantes, objetos/hashes antes/depois, logs e revisão científica pendente; estados “preparando/em_execucao/concluida/invalida/interrompida”, conforme `data-model.md` (FR-001/FR-007/FR-010).
- [ ] T007 Implementar em `verificacao_variantes.py` o registro/persistência de `evidencias/spec003/<id_execucao>/resultados.json`, listas `baseline`/`variantes` separadas e chave única `(id_execucao, mudanca, teste)`, usando BASELINE para inicial; campos entrada/versao_executada/referencia/esperado/observado/observado_bruto/estado/comparacao/efeitos/erro/evidencia/diagnostico do modelo; estados “conforme/divergente/erro/nao_executado”, comparação “igual/diferente/nao_comparavel”, observado “null se indisponível ou malformado”, bruto com tipo/repr se necessário; inicializar registros conhecidos não executados, preservar escrita em falha/interrupção e não fabricar esperado em erro global de referência (FR-007/FR-008).
- [ ] T008 Executar futuramente os controles T003 após T004–T007 em `tests/test_variantes.py`, conferir persistência e integridade sem depender de variantes reais, registrar resultados identificados como sintéticos em `evidencias/spec003/<id_execucao>/` e corrigir defeitos do mecanismo no escopo, sem alterar materiais/JSON de referência (FR-001/FR-004/FR-007).

**Checkpoint**: suporte comum verificável, referência identificada/imutável e registro mínimo utilizável. T003–T008 são código/testes futuros, não realizados nesta geração.

## Phase 3: User Story 1 — origem comum e alteração única (P1, MVP)

**Objetivo**: quatro fontes autônomas, origem comprovada e política única auditada, sem depender dos resultados dos 48 pares.

**Teste independente**: para cada fonte, diff contra B e AST/revisão com responsável/data, preservando baseline. Isso verifica US1 sem exigir US2/US3 completas.

- [ ] T009 [US1] Escrever em `tests/test_variantes.py` controles sintéticos de diff/AST e carregamento: rejeitar edição adicional, assinatura/nó externo alterado, origem encadeada e módulo/caminho errado; aceitar somente as quatro expressões do plano; registrar resultado inicial pertinente em `evidencias/spec003/<id_execucao>/`, antes da implementação T010/T016 (FR-001/FR-002).
- [ ] T010 [US1] Implementar em `verificacao_variantes.py` auditor de diff textual contra o blob B e AST com igualdade fora da expressão autorizada, assinatura preservada e remoção/substituição exata dentro dela; manter diff/hash e revisão “responsável/data/resultado/observação”; auditoria inválida ou pendente bloqueia os 12 pares da fonte sem bloquear variantes independentes válidas; AST não gera código ou esperado (FR-001/FR-002).
- [ ] T011 [P] [US1] Preparar `variantes/mc01.py` extraindo novamente `autorizacao.py` diretamente de B e retirando só `('Auditoria', 'exportar')` da sequência de concessões; preservar tupla unitária válida, assinaturas e demais funções; registrar origem para auditoria sem importar outra variante ou alterar baseline (FR-001/FR-002).
- [ ] T012 [P] [US1] Preparar `variantes/mc02.py` extraindo novamente a fonte diretamente de B e trocando só o retorno de `ha_incompatibilidade` por `False`; manter concessões, herança, estado e demais nós executáveis de B (FR-001/FR-002).
- [ ] T013 [P] [US1] Preparar `variantes/mc03.py` extraindo novamente a fonte diretamente de B e retirando só `('Consulta', 'visualizar')` da sequência de concessões; preservar tupla unitária válida, relação de herança, incompatibilidade e demais funções (FR-001/FR-002).
- [ ] T014 [P] [US1] Preparar `variantes/mc04.py` extraindo novamente a fonte diretamente de B e trocando só o retorno de `obter_papeis_efetivos` pelos papéis atribuídos sem expansão; conservar concessões/conflito/estado e ID canônico MC-04-v2 no registro, sem renomear JSON (FR-001/FR-002).
- [ ] T015 [US1] Conferir os quatro diffs contra B, estrutura AST e independência de `variantes/mc01.py` a `variantes/mc04.py`; registrar fonte/revisão/autor/data/resultado, diff e hashes em `evidencias/spec003/<id_execucao>/manifesto.json` e `diffs/`; comprovar `autorizacao.py`, `tests/test_autorizacao.py` e referência intactos; alteração extra não pode ser relevada por coincidência de saídas (FR-001/FR-002/FR-003).
- [ ] T016 [US1] Implementar em `verificacao_variantes.py` carregamento de B e variantes por `importlib.util.spec_from_file_location`, caminhos absolutos do snapshot e nomes exclusivos por tentativa/variante, Python `-B` e pasta sem cache; conferir `module.__file__`, loader, SHA-256 e B + ID + hash como versão executada, sem mudar `sys.path`/`sys.modules['autorizacao']` ou compartilhar implementação entre variantes (FR-001/FR-002).
- [ ] T017 [US1] Executar futuramente os controles T009 com T010/T016 e a auditoria das quatro fontes, consolidar checkpoint de US1 em `evidencias/spec003/<id_execucao>/` e `specs/003-mudancas-controladas/quickstart.md`; fonte inválida permanece bloqueada, baseline preservada e nenhuma conformidade comportamental é inferida apenas do diff (FR-001–FR-003; SC-001).

**Checkpoint**: MVP de procedência/isolamento utilizável. Não declara US2 conforme, gabarito revisado ou piloto liberado.

## Phase 4: User Story 2 — matriz completa por decisão e motivo (P2)

**Objetivo**: conferir B e depois os 48 pares distintos, incluindo selecionados/excluídos da política.

**Teste independente**: uma variante com procedência válida deve produzir 12 registros comparados; o consolidado das quatro deve produzir 48 chaves, com observado válido ou ausência/erro explícito. Dependência real: fundação + procedência/carregamento US1.

- [ ] T018 [US2] Escrever em `tests/test_variantes.py` controles de contrato/matriz que verifiquem 12 entradas idênticas por variante, esperado específico de `expected`, diferença só de motivo, T12/MC-03 executado apesar de excluído, fonte inválida com 12 não executados, erro individual sem interromper demais pares e bloqueio global se B falhar; registrar resultado inicial pertinente antes de T019–T023, usando fixtures sintéticas separadas (FR-003–FR-007/FR-009).
- [ ] T019 [US2] Implementar em `verificacao_variantes.py` execução da suíte original de `tests/test_autorizacao.py` no snapshot B via `sys.executable -B -m unittest discover -s tests -p test_autorizacao.py -v`, cwd do snapshot, descoberta não vazia, 18 métodos/controles, comando/retorno/stdout/stderr em `evidencias/spec003/<id_execucao>/baseline-unittest.txt`; não modificar a suíte nem aplicar seus esperados às variantes (FR-003).
- [ ] T020 [US2] Implementar em `verificacao_variantes.py` as 12 chamadas de referência inicial pelo catálogo e comparação com `catalogo[].esperado`, registros BASELINE separados em `evidencias/spec003/<id_execucao>/resultados.json`; erro/divergência da suíte/B bloqueia os 48 pares por pré-condição inválida, preservando causa e sem qualificar variantes (FR-003/FR-004/FR-009).
- [ ] T021 [US2] Implementar em `verificacao_variantes.py` suíte unittest com `subTest(mudanca, teste)` para cada variante válida × 12 itens de `catalogo`, papéis convertidos para frozenset, chamada real `autorizar` sem mocks e esperado `mudancas[id].expected[teste]`; registrar antes da asserção e continuar após falha individual, nunca filtrar pelos conjuntos selecionados de 2/4/8/5 (FR-005/FR-007).
- [ ] T022 [US2] Implementar em `verificacao_variantes.py` comparação do dict com exatamente `decisao`/`motivo`, strings do contrato, distinguindo retorno válido diferente como divergente e exceção/retorno malformado como erro com bruto preservado; calcular contagens “conformes + divergentes + erros + nao_executados = 48”, tentados = conformes + divergentes + erros, comparados = conformes + divergentes; rejeitar duplicatas/IDs desconhecidos como integridade, sem criar pares adicionais (FR-006/FR-007).
- [ ] T023 [US2] Implementar em `verificacao_variantes.py` efeitos “mudou/preservou” esperados contra o esperado inicial e “mudou/preservou/indisponivel” observados contra observado de B da mesma rodada, diferenças por campo, fonte/versão/referência e evidência por par; persistir em `evidencias/spec003/<id_execucao>/resultados.json` sem confundir efeito, relevância e conformidade (FR-007/FR-009).
- [ ] T024 [US2] Executar futuramente os controles sintéticos T018 de `tests/test_variantes.py` separadamente da matriz real implementada em `verificacao_variantes.py` após T019–T023/US1; acionar essa matriz por integração local dos componentes já disponíveis, sem depender da CLI ainda futura de T027. Guardar a tentativa real exclusiva em `evidencias/spec003/<id_execucao>/`, com comandos/retornos/logs; conferir 12 pares iniciais e os 48 pares de variantes, T07/MC-04 por motivo e T12 nas quatro mudanças; registrar divergências/lacunas reais sem alterar esperado ou proclamar sucesso se houver falha (FR-003–FR-007/FR-009; SC-002/SC-003/SC-006).
- [ ] T025 [US2] Conferir em `evidencias/spec003/<id_execucao>/manifesto.json` e `resultados.json` as 48 chaves distintas e identificação executada por par, contagens disjuntas e preservação de `autorizacao.py`, `tests/test_autorizacao.py`, catálogo/referência/conjuntos; confirmar snapshot sem contaminação e hashes antes/depois, registrando impedimento se falhar (FR-001/FR-003/FR-004/FR-007; SC-004).

**Checkpoint**: relatório de US2 completo somente se os 48 pares forem tentados e a integridade for válida; conformidade integral exige 48 conformes. Erros, não execução ou divergências permanecem visíveis e seguem para investigação; não induzem ajuste de referência.

## Phase 5: User Story 3 — diagnóstico, interface e conclusão restrita (P3)

**Objetivo**: preservar falhas e explicar efeitos, distinguindo registro utilizável, conformidade técnica e aprovação científica.

**Teste independente**: rever registro de divergência e contrato da interface com fixtures sintéticas, sem precisar produzir falha real nas variantes. Integração real usa US2.

- [ ] T026 [US3] Escrever em `tests/test_variantes.py` controles da interface/registrador para códigos 0/1/2, decisão igual com motivo diferente, exceção/saída inválida, duplicatas, referência global inválida, B divergente, fonte inválida, interrupção, falha de escrita e pasta repetida; provar preservação das tentativas/esperado e campos de diagnóstico/revisão científica, registrando resultado inicial pertinente antes de T027/T028 em evidências sintéticas separadas (FR-006–FR-010).
- [ ] T027 [US3] Integrar em `verificacao_variantes.py` comando `python -B verificacao_variantes.py --saida evidencias/spec003/<id-novo>` e resumo: 0 somente com 48 conformes/B/controles/procedência/registros íntegros; 1 somente matriz completa sem erros/lacunas com divergência em variante; 2 para erro/interrupção/incompletude com prioridade sobre 1, inclusive B divergente com variantes bloqueadas; persistir antes de sair e não oferecer atualização de gabarito, origem móvel ou filtro de testes (FR-007/FR-010).
- [ ] T028 [US3] Integrar em `verificacao_variantes.py` diagnóstico por par em `evidencias/spec003/<id_execucao>/resultados.json`, separando causa confirmada/hipótese/pendência, RFs/evidências/responsável/data/resolução, esperado/observado originais e revisão científica pendente; estado de conclusão distingue especificado/implementado/executado/conforme, sem concluir aprovação de orientador, referência ou piloto (FR-008/FR-010).
- [ ] T029 [US3] Executar futuramente T026 após T027/T028 em `tests/test_variantes.py` e inspecionar evidências sintéticas em `evidencias/spec003/<id_execucao>/`, validando salvamento em falha, códigos prioritários, logs e retentativa com pasta/ID novos e vínculo `retentativa_de`; não misturar fixtures com os 48 pares reais (FR-007/FR-008/FR-010).
- [ ] T030 [US3] Investigar cada divergência/erro real de T024/T025 ou rodada posterior em `evidencias/spec003/<id_execucao>/resultados.json` e `specs/003-mudancas-controladas/quickstart.md`: conferir commit/isolamento/entrada/esperado, depois RF-01–RF-04/dependências/precedência; registrar causa ou pendência e evidência, inclusive suspeita de referência, sem trocar esperado por observado; se não houver ocorrências, registrar zero, sem inventar investigação (FR-008; SC-005).
- [ ] T031 [US3] Registrar em `documentacao/decisoes.md` pendência humana de qualquer suspeita de erro na referência, com fonte/responsável/data/próxima ação, preservando candidata 0.2 e conjuntos; correção de engenharia no escopo deve gerar tentativa nova em `evidencias/spec003/<id_execucao>/`, ligada à anterior, sem apagar diagnóstico; aprovação científica e alterações de gabarito dependem de revisão/autorização próprias (FR-004/FR-008/FR-010).

**Checkpoint**: mecanismo de falha/diagnóstico verificado e ocorrência real investigada ou pendente explicitamente. Resultado divergente não equivale a conformidade; código de saída 0 não equivale a aprovação científica.

## Phase 6: Polish — evidências e fechamento transversal

**Dependências**: US1–US3 e suas verificações, mantendo pendências funcionais visíveis.

- [ ] T032 Executar futuramente o quickstart integrado após a interface/diagnóstico de US3, em nova pasta `evidencias/spec003/<id_execucao>/`, conservando comando completo/Python/cwd/retornos/stdout/stderr e resultado; confirmar suíte inicial e controles, 12 pares B e 48 pares reais sem filtro, sem repetir apenas casos ruins ou substituir registros anteriores (FR-003/FR-005/FR-007/FR-010; SC-002/SC-003).
- [ ] T033 Consolidar e revisar `evidencias/spec003/<id_execucao>/manifesto.json`, `resultados.json`, logs, diffs e snapshots: versões/hash efetivamente executados, 48 chaves, contagens e conformidade/pendência, hashes finais e revisão de cada fonte; comprovar ausência de alteração em `autorizacao.py`, `tests/test_autorizacao.py` e referência/conjuntos, com relatório de completude separado da conformidade científica (FR-001–FR-010; SC-001–SC-007).
- [ ] T034 Atualizar `specs/003-mudancas-controladas/quickstart.md`, notas de estado de `spec.md`/`plan.md`/`checklists/requirements.md` e documentação afetada em `documentacao/arquitetura.md`/`qualidade-e-testes.md`, vinculando apenas evidências reais, descrevendo limites/divergências e preservando catálogo, gabarito e histórico; não marcar planejado como executado nem alterar critérios para coincidir com implementação (FR-003/FR-004/FR-008/FR-010).
- [ ] T035 Atualizar `documentacao/decisoes.md`, `ESTADO_ATUAL.md`, `HANDOFF.md`, `BLOQUEIOS.md` e `AGENTS.md` no fechamento futuro, distinguindo conformidade executável e revisão científica; manter P-01/P-02/P-03, revisão das expectativas T12 em P-02 e adoção constitucional, com responsáveis/pendências; T12 já adotado em B, sem novo pedido de adoção. Marcar tarefas somente com evidência própria; sem iniciar piloto/LLM/coleta (FR-010; SC-007).

## Dependencies & Execution Order

Ordem de fases: Setup → Fundação → US1 (P1) → US2 (P2) → US3 (P3) → Fechamento. Não há dependência de aprovação científica para gerar esta lista; implementação exige autorização própria e experimento mantém seus critérios de entrada.

| Grupo | Dependências e restrições |
|---|---|
| T001 → T002 | Sem edição prévia do núcleo; conferir status antes de fixar fontes |
| T003 → T004 → T005 → T006 → T007 → T008 | Mesmo verificador/teste, execução sequencial; não paralelizar edições concorrentes |
| T009 → T010 | Controles de auditoria antes do auditor |
| T011/T012/T013/T014 | Após T010 e fundação; independentes entre si, arquivos distintos e cópia nova de B |
| T015 → T016 → T017 | T015 depende das quatro fontes; T016/T017 de T009/T010/T015 |
| T018 → T019 → T020 → T021 → T022 → T023 → T024 → T025 | Após US1; implementações no mesmo arquivo sequenciais, observados de B antes das variantes |
| T026 → T027 → T028 → T029 → T030 → T031 | T026/T027 dependem da integração US2; T030 depende das ocorrências reais, zero é resultado legítimo |
| T032 → T033 → T034 → T035 | Rodada nova após integração final; revisão antes de comunicar fechamento |

A independência das histórias é de aceitação: US1 pode ser demonstrada por procedência/diff sem matriz, US2 por 12 casos de uma fonte válida, US3 por registros/fixtures. O fluxo real usa componentes anteriores compartilhados, sem alegar paralelismo irrestrito entre histórias. T032 é rodada final justificada pela integração de interface/diagnóstico após T024; não uma repetição para obter resultado favorável.

## Parallel Examples

- **US1**: após T010, T011–T014 podem preparar quatro arquivos separados em paralelo; nenhum escreve no manifesto compartilhado. Integração/revisão em T015 é sequencial.
- **US2**: não há tarefas `[P]` de edição, pois T018–T025 usam verificador/teste/registro compartilhados. Inspeções de logs por variante podem ser distribuídas somente para leitura, com consolidação única; a rodada permanece sequencial.
- **US3**: não há paralelismo seguro de edição em T026–T031. A inspeção de registros distintos pode ser independente, mas gravação/consolidação e decisões são sequenciais.

## Implementation Strategy

MVP: T001–T017, demonstrando quatro fontes com origem/alteração única e baseline preservada. Não inclui declaração de efeitos conformes ou pesquisa liberada.

Depois, US2 entrega os 12 pares por variante e 48 registros completos quando possível; US3 acrescenta interface final e diagnóstico auditável. Fechamento transversal consolida evidências reais, sem ampliar o recorte. Dados sintéticos permanecem separados, não representam resultados experimentais. Pausar em cada checkpoint para revisar evidências, sem iniciar a próxima etapa por inferência.

## Rastreabilidade Spec → tarefas

| Requisito / critério | Tarefas |
|---|---|
| FR-001 | T001, T004, T006, T009–T017, T025, T033 |
| FR-002 | T009–T017, T033 |
| FR-003 | T001/T002, T004, T015, T019/T020, T024/T025, T032–T034 |
| FR-004 | T001/T002, T005, T008, T020, T025, T031, T033/T034 |
| FR-005 | T005, T018, T021, T024, T032/T033 |
| FR-006 | T018, T022, T024, T026, T033 |
| FR-007 | T003, T005–T008, T018–T029, T032/T033 |
| FR-008 | T007, T026, T028–T031, T033/T034 |
| FR-009 | T018, T020, T023/T024, T033 |
| FR-010 | T006, T026–T035 |
| SC-001 | T009–T017, T033 |
| SC-002 | T019/T020, T024/T025, T032/T033 |
| SC-003 | T021/T022, T024/T025, T027, T032/T033 |
| SC-004 | T006/T007, T022/T023, T025, T033 |
| SC-005 | T026, T028–T031, T033/T034 |
| SC-006 | T018, T021–T024, T033 |
| SC-007 | T027/T028, T031, T033–T035 |

## Estado da geração

35 tarefas: Setup 2, Fundação 6, US1 9, US2 8, US3 6, Fechamento 4. Quatro tarefas `[P]` (somente fontes independentes). Todas pendentes, sem execução. Spec ativa confirmada por setup-tasks; template local resolvido, artefatos opcionais lidos, sem hooks de extensão na conferência. A análise Spec/plano/tarefas é etapa de leitura posterior à geração e seu relatório é apresentado na resposta, sem editar fontes para ocultar achados.
