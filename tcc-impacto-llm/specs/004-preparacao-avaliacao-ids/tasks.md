# Tasks: Preparação de entradas e avaliação separada de IDs

> Contrato vigente — 01/11/2026 (D-29): o modelo recebe somente texto preparado, sem ferramentas, repositório, código, comandos, gabarito, resultados de variantes ou histórico. Exigências de identidade/ACL do Windows de T014/T015 substituídas, sem execução ou aprovação retroativa. Permanecem validação de arquivos/caminhos, autorização de conteúdo, integridade, equivalência de condições e avaliação separada. Notas representam conhecimento de analista de testes; texto definitivo e revisão profissional pendentes. Não se avaliam juniores, novos testes ou defeitos reais. Sem modelo escolhido, envio, chamadas externas ou piloto; revisão científica pendente. Histórico preservado em evidencias/spec004/revisao-textual-2026-11-01/originais.

> Convenções vigentes — 27/10/2026, D-26/D-27: o pesquisador adotou PONT-01/PONT-02 como convenções técnicas candidatas, ainda sujeitas à revisão científica. Política `ids-proposta-004-v2`: célula base por configuração/mudança/condição; versões de política ou referência distintas impedem resultado combinado, com diagnóstico e grupos separados por versão. Identidade lógica única por configuração/mudança/condição/repetição; duplicidades bloqueiam o resumo afetado sem escolha automática. Tentativas técnicas vinculadas não são repetições. Jaccard somente entre repetições distintas elegíveis, com número de observações/pares; menos de duas: **não calculável**. I1 corrigido: rejeitar links simbólicos internos/externos, junctions e todos os reparse points. Implementação e controles independentes autorizados, sem LLM/piloto. Registro de 27/10: isolamento por SO não demonstrado; exigência substituída por D-29, sem aprovação retroativa. Textos datados de somente planejamento/sem tarefas abaixo são históricos; originais preservados em evidências.

**Input**: [Spec](spec.md), [plano](plan.md), [pesquisa](research.md), [modelo de dados](data-model.md), [contrato](contracts/preparacao-avaliacao.md), [quickstart](quickstart.md), checklist e governança.

**Data de criação**: 27/10/2026. **Estado vigente — 01/11/2026, D-29/D-30**: 49 tarefas vigentes concluídas no contrato de engenharia offline; 2 exigências históricas substituídas (T014/T015), mantidas desmarcadas e sem aprovação. Entrega real e pesquisa não executadas. Implementação autorizada em D-26/D-27 e revista em D-29.

**Autorização histórica da geração — 27/10/2026**: pedido atual do pesquisador para somente gerar tarefas e analisar consistência. Leitura/seleção confirmadas por `check-prerequisites.sh --json --paths-only` e `setup-tasks.sh --json`: FEATURE_DIR=`specs/004-preparacao-avaliacao-ids`, documentos de pesquisa/modelo/contrato/quickstart disponíveis; template core resolvido localmente. BRANCH do resolvedor é contexto, sem branch/commit criado. HEAD inicial `d64076af379b9b709bc1dc7a620bd06387ced912`. Não selecionar outra feature por aba aberta.

**Limite da etapa documental anterior**: somente este `tasks.md`; relatório de análise na resposta, em modo somente leitura. Governança e demais documentos são fontes preservadas. Suas declarações datadas de “sem tarefas” descrevem as entregas anteriores; o pedido atual supera esse alcance documental, sem autorizar implementação. Atualizações futuras de contexto estão previstas no fechamento, não realizadas agora.

**Tests**: requeridos pela Spec; escrever controles e esperados independentes antes da implementação correspondente. Implementação/verificações autorizadas posteriormente em D-26/D-29; resultados históricos e atuais vinculados ao final. Controles são `sintetica`, modelo nulo, sem fase piloto, sem resultados de LLM.

**Organization**: quatro histórias da Spec, por prioridade, com dependências explícitas e verificação independente. Sem SDK, rede, API, interface, infraestrutura genérica ou escolha de modelo.

## Format: `[ID] [P?] [Story] Description`

- Caixas pendentes não atestam execução. Marcar somente com evidência da aceitação correspondente.
- `[P]` indica arquivos distintos que podem ser editados em paralelo **após** suas pré-condições. Não autoriza agentes paralelos nem edições concorrentes do mesmo arquivo.
- `[US1]`–`[US4]` correspondem às histórias da Spec. Setup/fundação/fechamento não têm rótulo de história.
- IDs T001–T051 são locais desta Spec; não são T01–T12 da bancada nem S-01–S-16 dos controles.

## Path Conventions

Paths relativos a `D:\TCC-Projeto\TCC\tcc-impacto-llm`. Fontes futuras: `montagem_entradas.py`, `avaliacao_ids.py`; testes futuros: `tests/test_montagem_entradas.py`, `tests/test_avaliacao_ids.py`; fixtures: `tests/fixtures/spec004/`; evidências novas por tentativa: `evidencias/spec004/`. Não criar outro repositório. Na revisão D-29, exportador editorial local `fontes_autorizadas.py`, pacote plano e autorização externa; somente payload se destina ao modelo. Não criar zonas/contas/ACL para isolamento.

## Conferência prévia da pontuação

### Regras candidatas já explícitas — implementar com esse status

Fontes: Spec FR-007–FR-010, research R-06/R-07 e contrato §§4–7. Política identificada `ids-proposta-004-v2`; não recebe aprovação científica por implementação ou concordância sintética.

| Tema | Regra candidata existente | Tarefas correspondentes |
|---|---|---|
| Conjuntos esperados | G_RF=`rfs`, G_T=`tests` da mudança; nunca `changed`, `preserved` ou `expected`. MC-04 mapeia documentalmente para MC-04-v2, sem aliases para respostas. | T025, T028 |
| Formato | UTF-8 estrito, sem remover BOM; JSON integral, sem chave repetida/NaN/Infinity/texto residual; exatamente duas listas de strings. Espaços externos e escapes JSON legítimos aceitos; sem reparo/avaliação parcial. | T024, T027 |
| Duplicatas/desconhecidos | Duplicata exata conta uma vez, posições a partir de zero; desconhecido distinto é FP, inclusive string vazia/caixa/espaços/dimensão errada, sem normalização. | T026, T029–T030 |
| Comparação separada | TP=cardinalidade(S∩G), FP=cardinalidade(S−G), FN=cardinalidade(G−S), por RF/testes. Desconhecidos são subconjunto de FP, sem somá-los novamente. | T026, T029–T030 |
| Métricas | P=TP/(TP+FP), R=TP/(TP+FN), F1=2TP/(2TP+FP+FN). S vazio/G não vazio dá zero; G vazio bloqueia referência. Frações exatas e decimal derivado com seis casas, sem arredondamento intermediário. | T026, T028–T029 |
| Inválida/técnica/incorreta | Inválida: extração e escores observados nulos nas duas dimensões; técnica/fragmento: sem seleção/escore; formato válido com omissão/FP: avaliador pode retornar 0, sem significar resposta correta. | T016–T023, T024, T030–T032 |
| Imputação | Só visão operacional explicitamente solicitada com `--imputar-invalidas`, imputando P/R/F zero a inválidas, sem fabricar S/TP/FP/FN observados ou pontuar falhas técnicas. | T037–T041 |
| Jaccard | Pares de observações concluídas válidas da mesma mudança/condição e repetições distintas, por dimensão; desconhecidos permanecem. Dois vazios dão 1 acompanhado de omissões; menos de duas elegíveis informa não calculável. | T034–T035, T041 |
| Denominadores | N observações planejadas, A tentativas, C concluídas elegíveis, V válidas, I inválidas, T técnicas finais, K somente IDs conhecidos; V+I=C. V/C, K/V, C/N, zero denominador indisponível. P/R/F válido sobre V; operacional sobre V+I; sem resumo geral entre mudanças. | T037–T041 |
| Retentativas/retornos | No máximo uma retentativa técnica vinculada com mesmo payload; não nova repetição nem transporte implementado. Duas concluídas para a mesma observação bloqueiam resumo. Retornos candidatos 0/1/2 conforme contrato, com 2 prioritário sobre 1. | T018–T023, T031, T037–T041 |

### Convenções adotadas pelo pesquisador — sujeitas à revisão científica

As lacunas da análise foram resolvidas pelo pedido explícito do pesquisador, registrado em D-26. A adoção técnica não aprova cientificamente métricas ou resultados; a implementação preserva essa distinção.

| ID local | Decisão necessária e alternativas não escolhidas | Dependências/alcance |
|---|---|---|
| PONT-01 | Adotada em D-26: rejeitar agregação entre versões distintas de política/referência na mesma célula; preservar registros e informar grupos por versão, sem resultado combinado. | T036 resolvida documentalmente; T037–T041 podem avançar nas dependências independentes. |
| PONT-02 | Adotada em D-26: configuração/mudança/condição/repetição identificam uma observação; duplicidades bloqueiam célula afetada sem escolher resposta. Tentativas técnicas têm IDs/vínculos próprios. | T036 resolvida; refletir na importação, resumo e S-15/S-16. |

**Exigência substituída por D-29:** T014/T015 não foram executadas/aprovadas e deixam de bloquear o contrato textual. Seus registros permanecem históricos; T049–T051 substituem a garantia. Envio real ao modelo sem ferramentas permanece pendente antes do piloto.

**Pendências científicas preservadas**: revisão profissional/científica da referência/política/expectativas T12; notas definitivas, origem e neutralidade; fundamentação/revisão de P/R/F/Jaccard; piloto/configuração/orçamento/congelamento e adoção constitucional. Não bloqueiam geração desta lista ou verificação técnica de regras candidatas. Bloqueiam alegação de aprovação científica/liberação experimental. T12 já adotado em B; sem nova adoção.

## Phase 1: Setup — delimitação e preservação

**Objetivo:** preservar contexto e artefatos; execução histórica e revisão atual registradas nas evidências.

- [x] T001 Confirmar autorização futura, feature 004, Python 3.11+ e árvore local; registrar comando/cwd/versão/HEAD/alterações existentes e identidades de código, materiais, notas, referência e evidências em `evidencias/spec004/preparacao/inventario.json`, sem importar a bancada ou gerar variante.
- [x] T002 Conferir o quadro de pontuação deste `specs/004-preparacao-avaliacao-ids/tasks.md` contra Spec/research/contrato e registrar seu status candidato, PONT-01/PONT-02 e impedimentos de ambiente em `evidencias/spec004/preparacao/escopo-e-gates.md`; usar as convenções candidatas já adotadas em D-26, sem habilitar pesquisa pelo inventário.

## Phase 2: Foundational — contratos sintéticos e oráculos prévios

**Objetivo:** fixar evidências de entrada/esperados antes das funções sob teste. Depende de T001–T002. Nenhuma dependência de decisão de modelo ou ciência encerrada.

- [x] T003 Definir em `tests/fixtures/spec004/matriz-controles.json` o índice S-01–S-16 e todos os subcasos do contrato §7, vinculando requisitos, regra candidata, fixtures e resultado esperado; indexar também subcasos de PONT-01/PONT-02 conforme D-26 em `tests/fixtures/spec004/subcasos-previstos.json`, sem derivar esperado do observado.
- [x] T004 [P] Preparar em `tests/fixtures/spec004/` referência sintética de versão própria com G_RF={RF-02}/G_T={T04,T12}, pacotes fictícios D0/D1/E0/E1, bytes de respostas e registros de tentativas com `origem=sintetica` e `modelo_reportado=null`; nenhum gabarito, resultado ou fonte mista real no pacote permitido. Depende de T003.
- [x] T005 [P] Escrever em `tests/fixtures/spec004/esperados.json` estados, listas, TP/FP/FN, frações, nulidades, códigos e denominadores literais dos subcasos já definidos, conferidos manualmente pelo contrato; não calcular esperados com parser/avaliador de produção nem derivá-los da candidata. Registrar a revisão técnica prévia e incluir casos PONT-01/PONT-02 conforme decisões D-26. Depende de T003, independente da geração de T004.

**Checkpoint:** referência sintética e oráculos identificados; ausência de decisão para agregação não autoriza preenchimento automático. Após T003–T005, US1 e a importação independente de US2 podem avançar com arquivos separados, sob futura autorização.

## Phase 3: US1 — montar somente documentos permitidos (Priority: P1, MVP técnico)

**Goal:** montar entrada íntegra de uma mudança/condição, conferindo fontes/recortes, autorização externa, conteúdo/versões e limite textual sem ferramentas.

**Independent Test:** S-14 textual, fontes reais autorizadas e negativos fictícios, conferindo bytes, recortes e recusas sem referência. T049/T050 substituem a prova por identidade; não demonstram envio remoto ou isolamento de SO.

### Tests for US1 — antes da implementação correspondente

- [x] T006 [P] [US1] Escrever em `tests/test_montagem_entradas.py` os controles de manifesto de uma mudança/condição, oito nomes lógicos, status/revisão, duplicidade de papéis/caminhos e notas rascunho; exigir `status=RASCUNHO_PREPARACAO`, `liberado_para_pesquisa=false`, documentos `conferido_tecnicamente`, bloqueando `pendente`/`reprovado`; S-14 com esperados de T005. Depende de T004/T005; paralelo apenas à importação US2 em arquivo distinto.
- [x] T007 [US1] Completar S-14 e a parte de preservação S-13 em `tests/test_montagem_entradas.py`: extra/ausente, absoluto/../subdiretório/link interno/externo, junction/reparse point, hash diferente, saída sobreposta/repetida, nota em condição errada, gabarito fictício com revisão reprovada; controles positivos de quatro condições, documentos originais e payload esperado literal.

### Implementation for US1 — futura

- [x] T008 [US1] Implementar manifesto e lista fechada em `montagem_entradas.py`, incluindo `versao_contrato`, IDs/versões/hashes/tamanhos, mudança canônica e condições D0/D1/E0/E1, revisão técnica e `status_notas=RASCUNHO_NAO_REVISADO` ou `ausentes`; rejeitar formato/status indevidos sem ler documento adicional. Depende de T006/T007 escritos.
- [x] T009 [US1] Implementar em `montagem_entradas.py` confinamento de manifesto/documentos e saída nova: apenas filhos diretos com nomes exatos, sem glob/recursão/resolução de dependências, links internos/externos, junctions e reparse points, paths sobrepostos ou fallback; verificar hashes antes de usar e ao consolidar. Não importar avaliador ou aceitar referência.
- [x] T010 [US1] Implementar composição em `montagem_entradas.py` na ordem do contrato, delimitadores/LF fixos e bytes dos documentos preservados: comuns idênticos por mudança, pedido igual D0/D1 e E0/E1, mesmas notas D1/E1 entre mudanças; omitir integralmente bloco/delimitadores/notas em D0/E0, sem abrir `notas.md` ou acrescentar texto compensatório.
- [x] T011 [US1] Persistir em `montagem_entradas.py` `payload.txt`, `manifesto-original.json`, `documentos/` e `preparacao.json` com conteúdo integral, instante UTC, versões/hashes/IDs, metadados de rascunho e `PREPARADO_LOCAL_NAO_ENVIADO`; bloqueio/causa explícitos sem payload parcial utilizável, sem sobrescrever tentativa anterior.
- [x] T012 [US1] Implementar CLI local de montagem em `montagem_entradas.py` conforme contrato §2, com `--pacote`, `--manifesto`, `--autorizacao` externa obrigatória (v3), `--saida` e códigos 0/2; recusar argumentos de referência/modelo/provedor e não acessar rede, desenvolvimento, avaliador ou material privado.
- [x] T013 [US1] Executar futuramente controles lógicos/positivos da montagem e composição literal das quatro condições; guardar comando/retorno/stdout/stderr, versões, esperado/observado e casos negativos em `evidencias/spec004/us1-logica/`, usando diretórios novos; não declarar isolamento ou ciência aprovados pelo resultado lógico.
- [ ] T014 [US1] Preparar e registrar em `evidencias/spec004/isolamento/preparacao.md` a identidade Windows restrita, raízes de leitura/escrita e permissões do desenho, com disponibilidade/autorização operacional e runner identificado; se indisponível, registrar impedimento concreto e manter T015/fechamento pendentes. Sem infraestrutura genérica, novo repositório ou acesso ao gabarito pelo runner. **[SUBSTITUÍDA D-29, NÃO EXECUTADA/APROVADA; ver T049–T051].**
- [ ] T015 [US1] Verificar S-14 sob a identidade de T014, demonstrando leitura permitida só do pacote/runner e leitura negada de sentinelas fictícias nas zonas de desenvolvimento/referência/avaliação; inspecionar integralmente o payload permitido e preservar provas em `evidencias/spec004/isolamento/`. Não substituir acesso real por mocks, nome de pasta ou hashes. **[SUBSTITUÍDA D-29, NÃO EXECUTADA/APROVADA; ver T049–T051].**

## Phase 4: US2 — preservar entrada e resposta original (Priority: P1)

**Goal:** importar registros/respostas locais e produzir evidência íntegra antes da interpretação.

**Independent Test:** preparação literal de T004 e respostas sintéticas, sem precisar executar US1 ou pontuador; S-11/S-13 verificam originais, ausências e falhas. A CLI final de avaliação só fica pronta em US3.

### Tests for US2 — antes da implementação correspondente

- [x] T016 [P] [US2] Escrever em `tests/test_avaliacao_ids.py` S-11 e preservação de resposta malformada/vazia recebida: `estado_tecnico` exatamente `concluida`/`falha_tecnica`, causa obrigatória na falha, resposta ausente com arquivo/hash/tamanho nulos, fragmento não promovido a concluído; originais íntegros antes/depois, `origem=sintetica` e modelo nulo. Depende de T004/T005; não depende de completar US1.
- [x] T017 [US2] Acrescentar S-13 em `tests/test_avaliacao_ids.py` para vínculo/hash de preparação quebrado, alteração/remoção de fonte após importação e antes de fechamento, escrita parcial, pasta repetida, reavaliação nova vinculada e originais não sobrescritos; erro técnico do mecanismo não vira escore zero do conteúdo.

### Implementation for US2 — futura

- [x] T018 [US2] Implementar em `avaliacao_ids.py` importação explícita da preparação e tentativa com `observacao_id`, `tentativa_id`, `tentativa_anterior`, origem/mudança/condição/`repeticao_sintetica`, hashes/vínculos/causas; confinar caminhos à raiz de importação e distinguir tentativa de observação, sem montar pedidos ou ler referência nesta função.
- [x] T019 [US2] Copiar em bytes os originais de preparação/registro e resposta/fragmento quando existentes em `avaliacao_ids.py` antes de parsear; manter ausência nula e arquivo recebido vazio como presente, preservar erros disponíveis e separar integridade/estado técnico sem fabricar resposta/seleção.
- [x] T020 [US2] Implementar em `avaliacao_ids.py` diretório exclusivo por avaliação, versão/hash do avaliador/contrato, instante UTC, vínculos de reavaliação e log; impedir sobrescrita e manter causas de falha de persistência sem declarar registro completo.
- [x] T021 [US2] Implementar em `avaliacao_ids.py` revalidação de integridade na consolidação de originais/copias/logs, com `completo=true` somente quando íntegros; erro de mecanismo tem código 2 prioritário e falha técnica importada mantém diagnóstico próprio, sem escore.
- [x] T022 [US2] Executar futuramente os controles de importação/preservação sem pontuação de `tests/test_avaliacao_ids.py`, com preparação sintética literal; conservar resultado esperado/observado e tentativas originais em `evidencias/spec004/us2-preservacao/`, sem executar testes de US3/US4 ainda não implementadas.
- [x] T023 [US2] Conferir independente do importador a recuperação byte a byte e semântica de ausente/vazia/fragmento/reavaliação nas evidências de `evidencias/spec004/us2-preservacao/relatorio.md`; explicitar erros/lacunas e impedir confundir persistência íntegra com seleção correta.

## Phase 5: US3 — validar e comparar listas separadamente (Priority: P2)

**Goal:** separar validade, IDs conhecidos e correção da seleção; usar referência apenas no avaliador.

**Independent Test:** entrada/resposta/referência sintéticas fixas, S-01–S-12 e S-13 aplicável; operação de conjuntos e frações conferidas por esperados prévios, sem montagem ao vivo ou LLM.

### Tests for US3 — antes da implementação correspondente

- [x] T024 [US3] Escrever em `tests/test_avaliacao_ids.py` todos os subcasos S-09 e fronteira S-10: bytes UTF-8/BOM, JSON integral, chaves repetidas, NaN/Infinity, item numérico/bool/objeto/null, chave ausente/extra, truncamento/recusa/cercas, original recebido vazio; positivos de espaços/escapes legítimos. Formato inválido deixa ambas as dimensões sem extração/escores observados, sem reparo/avaliação parcial.
- [x] T025 [US3] Escrever em `tests/test_avaliacao_ids.py` S-12 para referência ausente/incompleta, versão/status, mudança ausente/duplicada, G vazio/duplicado/desconhecido/tipo errado, alias documental MC-04 e ausência de dependência de `expected`; prova positiva usa apenas rfs/tests e não filtra preservações.
- [x] T026 [US3] Escrever em `tests/test_avaliacao_ids.py` S-01–S-08/S-10 com contagens/listas/frações literais de T005: exata, parcial, todos, vazias, ordem/duplicatas com posições desde zero, desconhecidos conhecidos-excedentes separados, caixa/espaço/string vazia e dimensão trocada; P/R/F, completa/exata por dimensão, sem escore conjunto.

### Implementation for US3 — futura

- [x] T027 [US3] Implementar em `avaliacao_ids.py` decodificação/parser estritos e contrato específico de `materiais/modelos/schema_saida.json`, com hooks de chave repetida/constantes, rejeição de BOM/UTF-8 inválido/texto residual e exatamente `requisitos`/`testes` como listas de strings; preservar bytes antes do parser, sem biblioteca/schema genérico ou normalização.
- [x] T028 [US3] Implementar em `avaliacao_ids.py` adaptador de referência exclusiva do avaliador: registrar caminho/hash/versão/status, validar universos RF-01–RF-04/T01–T12 e G não vazio/único/conhecido em rfs/tests; alias exato MC-04→MC-04-v2 registrado, sem ler `changed`/`preserved`/`expected` para pontuar ou modificar candidata.
- [x] T029 [US3] Implementar em `avaliacao_ids.py` conjuntos S/G e listas de acertos/omissões/excedentes/IDs inexistentes, TP/FP/FN independentes, desconhecidos únicos incluídos em FP uma vez e duplicatas registradas; P/R/F/completa/exata da política candidata, frações exatas e decimal só derivado. G vazio bloqueia; S vazio válido não é erro técnico.
- [x] T030 [US3] Emitir `avaliacao.json` em `avaliacao_ids.py` com sintaxe/formato/IDs conhecidos/integridade/estado técnico separados e por dimensão, origem sintética/modelo nulo, listas originais/duplicatas/status da referência/versão `ids-proposta-004-v2`; invalidade e falha técnica mantêm valores observados nulos, com causas e sem aprovação científica.
- [x] T031 [US3] Integrar CLI `avaliar` em `avaliacao_ids.py` com importação/persistência US2, comparação e referência explícita, retornos 0 para avaliação válida mesmo com erro de seleção, 1 para invalidade de conteúdo/falha técnica importada bem registrada e 2 para infraestrutura/referência/integridade; sem transporte ou retentativa de conteúdo.
- [x] T032 [US3] Executar futuramente controles S-01–S-13 aplicáveis de `tests/test_avaliacao_ids.py`, preservando esperado/observado, logs e retorno em `evidencias/spec004/us3-avaliacao/`; demonstrar que uma seleção parcial pode ter retorno 0, enquanto falha de mecanismo não vira omissão do LLM.
- [x] T033 [US3] Inspecionar em `evidencias/spec004/us3-avaliacao/relatorio.md` a separação efetiva das duas listas, referência/hash, originais e causas das recusas; verificar fronteira de dependências nos módulos sem importar núcleo/variantes/verificador, sem contar casos sintéticos como bancada ou LLM. Não ajustar gabarito ao observado.

## Phase 6: US4 — conferir consistência/resumos e 16 famílias (Priority: P2)

**Goal:** comprovar comportamento do mecanismo com controles pré-definidos e evidências próprias; nenhuma avaliação experimental.

**Independent Test:** S-15/S-16 sobre avaliações sintéticas literais, sem LLM ou necessidade de rodar bancada; cobertura completa S-01–S-16 na integração futura. T036 é gate apenas das partes dependentes de política de agregação.

### Tests e decisões antes das partes correspondentes

- [x] T034 [US4] Escrever em `tests/test_avaliacao_ids.py` S-15 com referência/política homogêneas e repetições distintas: Jaccard RF=1 e testes=1/2 no primeiro par, dois vazios=1 com omissões, três pares/médias literais 1/3 RF e 1/6 testes, exclusões por inválida/tentativa e insuficiência de pares; não fixar regras de PONT-01/PONT-02 nestes testes.
- [x] T035 [US4] Implementar em `avaliacao_ids.py` cálculo de Jaccard por dimensão para pares já elegíveis da mesma célula com repetições distintas, todos os pares/IDs e frações exatas, dois vazios=1 e sem par=não calculável, sem nota de qualidade presumida. O filtro de entradas conflitantes e agregação completa dependem de T036–T038.
- [x] T036 [US4] Obter e registrar decisões explícitas para PONT-01/PONT-02 antes de implementar a seleção final das células/pares: responsável, data, evidência, justificativa e impacto de versão em `documentacao/decisoes.md`, reconciliando `specs/004-preparacao-avaliacao-ids/research.md`, `data-model.md` e `contracts/preparacao-avaliacao.md`; sem escolha automática de rejeição/estratificação/deduplicação ou aprovação científica presumida. Se decisão ausente, manter T037–T041 pendentes.
- [x] T037 [US4] Escrever em `tests/test_avaliacao_ids.py` S-16 e esperados independentes em `tests/fixtures/spec004/esperados.json`: cenários A/B, segunda falha, payload diferente, duas concluídas, planejada ausente, imputação opcional, denominadores zero e subcasos de versões misturadas/repetições repetidas conforme decisões registradas em T036; conservar esperados anteriores e versionar mudanças.

### Implementation e verificação de US4 — futuras

- [x] T038 [US4] Implementar em `avaliacao_ids.py` listas explícitas de avaliações/observações planejadas, identidade/vínculos/integridade e agrupamento conforme T036, sem glob, tentativas adicionais como observações ou escolha de melhor resposta; N/A/C/V/I/T/K, taxas V/C, K/V e C/N, elegibilidade final de pares e médias por célula, sem resumo entre mudanças. Depende de T037 escrito.
- [x] T039 [US4] Implementar em `avaliacao_ids.py` visão operacional só com `--imputar-invalidas`: P/R/F zero identificado apenas em I, denominador V+I; conservar resumo válido sobre V e nulos originais, sem imputar falha técnica nem fabricar conjuntos/TP/FP/FN/seleção completa/Jaccard observados.
- [x] T040 [US4] Integrar CLI `resumir` e persistência nova em `avaliacao_ids.py`, com hashes/versões/IDs/exclusões/pares e códigos do contrato, diagnósticos de completude/conflitos e rechecagem de integridade; decisões T036 explícitas, sem rede, modelo ou transporte.
- [x] T041 [US4] Executar futuramente S-15/S-16 e subcasos dependentes de T036, preservando contagens/taxas/frações/ausências e retornos em `evidencias/spec004/us4-resumos/`; comparar cenários literais sem invocar produção para gerar esperados, sem transformar tentativas ou pares em respostas LLM.
- [x] T042 [US4] Consolidar verificações necessárias do contrato textual em `evidencias/spec004/revisao-textual-2026-11-01/`, confrontando fontes, recortes, condições, caminhos, bytes e avaliação separada; reutilizar controles de métricas inalterados com versões/fontes identificadas, sem aprovar prova de SO substituída.
- [x] T043 [US4] Investigar divergências em `evidencias/spec004/revisao-textual-2026-11-01/diagnostico.md`, preservando esperado/observado, hipóteses/causas/evidências e responsável/resolução ou pendência; correção do mecanismo exige nova tentativa identificada, sem substituir expectativa pelo observado ou modificar candidata/notas para obter aprovação.

## Phase 7: Polish & Cross-Cutting Concerns — fechamento futuro

**Pré-condição vigente:** convenções D-26/D-29 e verificações textuais T049–T051 evidenciadas. Não há gate de identidade do Windows. Fechamento somente de engenharia offline; envio real/piloto/revisão científica continuam pendentes.

- [x] T044 Revisar semanticamente critério por critério, positivos/negativos, fronteira de acesso, integridade dos originais e regras candidatas em `evidencias/spec004/revisao-textual-2026-11-01/relatorio.md`; registrar conformidade/divergências/erros/ausências por FR/SC/subcaso, sem tratar quantidade de arquivos/links como prova de correção funcional.
- [x] T045 Confrontar fonte/referência/notas/materiais/evidências da bancada com inventário T001 e registrar preservação/versões/limites em `evidencias/spec004/revisao-textual-2026-11-01/preservacao.json`; confirmar nenhuma chamada/modelo/piloto, notas ainda rascunho e revisão científica/profissional pendente, sem inferir aprovação da concordância sintética.
- [x] T046 Reconciliar realizado/planejado em `specs/004-preparacao-avaliacao-ids/spec.md`, `plan.md` e `quickstart.md`, conferindo `checklists/requirements.md` como gate documental somente leitura, preservando histórico e substituindo referências a capacidades futuras somente com evidências reais; comandos de documentação conferidos não equivalem a controles executados.
- [x] T047 Atualizar com acréscimos datados `documentacao/decisoes.md`, `AGENTS.md`, `ESTADO_ATUAL.md`, `BLOQUEIOS.md` e `HANDOFF.md`, ligando evidências, decisões T036 e lacunas remanescentes; manter revisão profissional, notas definitivas, fundamentação/revisão de métricas, piloto final e adoção constitucional pendentes no alcance não resolvido.
- [x] T048 Revisar `specs/004-preparacao-avaliacao-ids/tasks.md` e relatório atual, marcar aceitação evidenciada, manter T014/T015 como substituídas não executadas e registrar revisão humana/científica, notas definitivas, entrega real e piloto pendentes antes da pesquisa.

## Dependencies & Execution Order

### Fases e histórias

```text
T001–T002 → T003 → {T004, T005}
                    ├─ US1: T006→T007→T008→T009→T010→T011→T012→T013
                    │                                      └─ T049→T050/T051 (contrato textual)
                    └─ US2: T016→T017→T018→T019→T020→T021→T022→T023
                              → US3: T024→T025→T026→T027→T028→T029→T030→T031→T032→T033
                              → US4: T034→T035; T036→T037→T038→T039→T040→T041
T013 + T049/T050/T051 + US2 + US3 + T041 → T042→T043→T044→T045→T046→T047→T048
```

T014/T015 foram substituídas por D-29 e não integram o caminho ativo: não criar identidade nem retomar a prova de SO. T049/T050/T051 verificam recortes, montagem, caminhos e avaliação separada; envio real permanece fora desta etapa. T036 pode ser discutida desde T002; sua posição na US4 não obriga aguardar implementação para decidir. T037–T041 dependem também de US2/US3 e dos cálculos de T034/T035; ambos os ramos se unem antes da integração. Nenhum caminho dispensa pedido de implementação.

### Dentro de cada história

Testes/esperados escritos antes da implementação correspondente; executar checkpoints somente no escopo autorizado e depois da capacidade necessária. Mesmos módulos e mesmos arquivos de testes são editados sequencialmente. Testes de importação não dependem da CLI final; testes de comparação não dependem do resumo futuro. Não executar suíte que invoque capacidade ainda ausente como se fosse critério já satisfeito.

### Oportunidades de paralelo e exemplos por história

- Fundação: T004 (fixtures de entrada/referência) e T005 (oráculos literais) podem ser preparados em arquivos distintos após T003; nenhum gera valores usando o outro como saída de produção.
- US1: T006, no teste de montagem, pode coexistir com T016, no teste de importação, após fundação. T007–T012 compartilham arquivos e ficam sequenciais.
- US2: somente o exemplo T016/T006 acima é independente; T017–T023 compartilham avaliador/teste/evidência ou dependem de conteúdo anterior.
- US3: sem paralelismo interno sinalizado; teste e implementação reutilizam `tests/test_avaliacao_ids.py`/`avaliacao_ids.py`, incluindo funções US2.
- US4: sem paralelismo interno sinalizado; decisões, testes, filtro/resumo e integração têm dependências; T036 pode ser tratada antecipadamente, sem editar artefatos compartilhados em concorrência.

## Implementation Strategy

**MVP primeiro:** fundação e US1, com recortes reais, negativos fictícios, conteúdo exato e contrato textual D-29. Aceitação local não libera envio ou pesquisa. Não criar interface para demonstrar a bancada.

**Entrega incremental:** US2 funciona com preparação literal independente; US3 agrega parser/referência e seleção por IDs; US4 acrescenta Jaccard/resumos após decisões necessárias. Esperados ficam identificados/versionados antes das funções correspondentes; nenhuma execução nesta geração.

**Fechamento:** cruzar esperado/observado e causas em todas as famílias/subcasos, revisar limites e pendências, atualizar documentação futura e só então avaliar conclusão técnica. Aprovação científica, notas definitivas e piloto são etapas separadas. Não selecionar modelos nem acrescentar cliente de provedor para completar este incremento.

## Rastreabilidade e contagens documentais

| Requisito/critério | Tarefas previstas | Limite |
|---|---|---|
| FR-001 | T004, T006–T009, T012–T013 | Lista/manifesto e recusas, não descoberta de contexto |
| FR-002 | T009, T012, T028, T033, T049–T051 | Referência separada; limite textual local, envio não exercitado |
| FR-003 | T002, T006–T009, T049–T050 | Conteúdo/neutralidade revisados antes do uso experimental |
| FR-004 | T010–T011, T017–T023 | Preparado local não significa enviado |
| FR-005 | T016–T023, T030–T032 | Ausente/fragmento/técnica não viram seleção |
| FR-006 | T001, T011, T017–T023, T040, T043–T045 | Derivados novos, originais preservados |
| FR-007 | T024, T027, T030–T032 | Parser e contrato distintos de acerto |
| FR-008 | T025–T030, T033 | RF/testes independentes |
| FR-009 | T005, T025–T030, T032 | G de rfs/tests, nunca observado |
| FR-010 | T002, T005, T026, T029–T041 | Candidatas; T036 é gate de agregação |
| FR-011 | T003–T007, T016–T017, T024–T026, T034–T043 | 16 famílias com subcasos e oráculos prévios |
| FR-012 | T001–T002, T044–T051 | Limites temporais superados apenas pelas autorizações D-26/D-29; sem pesquisa |
| SC-001 | T006–T013, T042, T044, T049–T051 | Recortes/bytes/caminhos/condições/recibo local; nenhuma alegação de SO |
| SC-002 | T011, T016–T023, T040, T045 | Integridade e preservação observáveis |
| SC-003 | T024–T032, T042 | Valores esperados, não contagem de testes |
| SC-004 | T016–T023, T024, T030–T032, T037–T042 | Estados, nulidades e denominadores |
| SC-005 | T005, T026, T029, T034–T041 | Frações/convenções candidatas |
| SC-006 | T003–T005, T042–T044, T049–T051 | Nenhum sintético contabilizado como experimento |
| SC-007 | Escopo desta entrega, T044–T048 | Exatamente dois arquivos era condição histórica da criação da Spec; não limitar artefatos hoje autorizados |

Distribuição: Setup 2; Fundação 3; US1 10; US2 8; US3 10; US4 10; Fechamento 5 = **48 IDs originais (situação histórica: 39 concluídos/9 pendentes em 27/10); revisão D-29 acrescenta T049–T051: 51 IDs, 49 vigentes concluídos e 2 substituídos sem aprovação**. Quatro `[P]` (T004/T005/T006/T016), com pré-condições acima. Essas contagens verificam organização, não correção funcional, execução ou aprovação científica.

## Notes

Não há hooks de extensão registrados (`.specify/extensions.yml` ausente na geração). Template/estrutura e destino confirmados pelo fluxo local, sem novos artefatos além de tasks.md. Análise posterior por `speckit-analyze` estritamente de leitura, com achados apresentados na resposta, sem corrigir silenciosamente fontes ou completar decisões PONT-01/PONT-02. Constituição preparada 1.0.0 continua sem ratificação; pendências científicas e fontes preservadas.

## Evidências da implementação parcial — 27/10/2026

Convenções do pesquisador em D-26, execução técnica D-27 e revisão parcial D-28. [Relatório](../../evidencias/spec004/revisao-parcial/relatorio.md), [matriz de confrontos](../../evidencias/spec004/revisao-parcial/matriz.json) e [estado por tarefa](../../evidencias/spec004/revisao-parcial/estado-tarefas.json). Originais documentais anteriores à adoção estão arquivados em preparacao/arquivos-iniciais; respostas e execuções anteriores não foram sobrescritas.

| Tarefas marcadas | Aceitação observada/evidência |
|---|---|
| T001–T002 | Inventário, hashes, escopo-e-gates e ambiente original |
| T003–T005 | Oráculos literais e código dos controles anteriores à implementação nos snapshots red; matriz/subcasos previstos e quatro pacotes fictícios |
| T006–T013 | montagem-final, casos positivos/negativos e bytes de payload; demonstracao-001 com quatro preparações originais. Um teste real de symlink ignorado, explicitamente pendente em S-14 |
| T016–T023 | avaliacao-confirmacao, S-11/S-13, originais/copias temporárias, falhas de persistência/fechamento e reavaliação vinculada; us2-preservacao/relatorio.md |
| T024–T033 | avaliacao-confirmacao e saídas CLI da demonstracao-001; referência exclusiva do avaliador, contagens/frações/status por dimensão; us3-avaliacao/relatorio.md |
| T034–T035 | Pares individuais, médias exatas, desconhecidos e não calculável em S-15 |
| T036 | Decisões explícitas D-26 já registradas; sem escolha automática do implementador |
| T037–T041 | PONT-01/PONT-02 e S-16 em avaliacao-confirmacao; cenários A/B persistentes, us4-resumos/relatorio.md |

**Pendentes à data de 27/10 (histórico, substituído por D-29/D-30):** T014/T015 (runner sob identidade separada sem leitura das zonas proibidas não provisionado; token atual lê referência) e T042–T048, cujas dependências integrais não foram satisfeitas. Documentação e revisão parciais foram atualizadas, mas não concluem essas tarefas de fechamento. S-14 também registra criação de symlink real negada pelo Windows, WinError1314; junctions reais foram verificadas, sem simulação apresentada como isolamento. As 15 outras famílias estão conformes no escopo offline descrito pelos confrontos; não são resultados de LLM.

**Testes à data de 27/10 (histórico):** 14 métodos do avaliador aprovados; montagem com 5 aprovados e 1 ignorado por capacidade ausente. Valores esperados e observados, não contagens de arquivos/links, sustentam as conclusões técnicas limitadas. Nenhum modelo, chamada ao LLM, piloto ou alteração de candidata/notas reais.

## Contrato textual verificável — D-29

Preparação editorial local em `fontes_autorizadas.py`, com seis caminhos fixos e recortes enumerados: instrução/notas/pedidos de materiais/04; definições integrais de materiais/07; contrato inicial de documentacao/requisitos; seis primeiras colunas da tabela T01–T12 de documentacao/qualidade-e-testes (sem coluna de destaques de RF); somente descrição de uma remoção na tabela da Spec 003; schema existente. Documentos mistos são lidos nessa edição local para selecionar os trechos, nunca enviados inteiros. A referência candidata não é lida nessa etapa.

`montagem_entradas.py`, contrato `spec004-v3`, lê pacote plano e `--autorizacao` externa explícita, fixando hashes de manifesto/documentos. Atualizar apenas seu próprio manifesto não autoriza texto alterado. A autorização é registro técnico controlado, não assinatura de autoridade ou detector semântico de qualquer gabarito: confrontar fontes, recortes, conteúdo e bytes. Mudança de fonte/recorte requer nova conferência; revisão profissional continua pendente. Fixtures v2 e comandos anteriores são históricos, preservados e não reexecutados como prova do contrato atual.

Somente `payload.txt` se destina ao modelo. Manifesto, autorização, cópias de documentos, fontes/hashes e `entrega-textual.json` são registros locais; não anexar diretório, código, fontes mistas ou referência. O recibo fixa texto/hash, `ferramentas=[]`, `anexos_ambiente=[]`, sem histórico e `envio_realizado=false`. Entrega real e ausência de ferramentas na plataforma serão conferidas antes do piloto; não foram exercitadas aqui, pois não há chamadas externas. Não se alega isolamento por SO.

Caminhos suportados: CLI com caminho local absoluto com drive ou relativo ao cwd; documentos do pacote filhos diretos com nomes enumerados; avaliador admite subdiretórios relativos declarados com separadores `/` ou `\`, confinados à raiz. Recusar drive relativo, raiz sem drive no Windows, UNC/dispositivos, streams `arquivo:fluxo`, dispositivos reservados, ponto/espaço final, componentes declarados vazios/`.`/`..` e links/junctions/reparse points. São controles de inclusão indevida, sem contas/permissões ou alegação de isolamento.

S-14 vigente verifica recortes/fontes, autorização independente, conteúdo proibido fictício em negativos, 16 combinações (quatro mudanças × quatro condições), texto exato e notas iguais D1/E1/ausentes D0/E0. Criação de symlink e negação de leitura por identidade são exigências antigas substituídas: não foram aprovadas. Esses objetos não pertencem às entradas suportadas; permanecem controles de recusa, sem exigir criação privilegiada para aceitar o contrato textual. PONT-01/PONT-02 e fórmulas candidatas não mudaram.

## Tarefas de substituição — D-29 (IDs anteriores preservados)

- [x] T049 [US1] Materializar apenas seis fontes/recortes enumerados em `fontes_autorizadas.py`, mantendo notas literais, proveniência e autorização externa; verificar 16 pacotes sem resultados de variantes, gabarito, código ou histórico.
- [x] T050 [US1] Verificar `payload.txt`/`entrega-textual.json`, bytes/versões, ferramentas/anexos vazios e envio não realizado; demonstrar recusa de conteúdo alterado mesmo com manifesto atualizado em `tests/test_fontes_autorizadas.py` e `tests/test_montagem_entradas.py`.
- [x] T051 [US4] Verificar caminhos locais suportados e recusas de inclusão indevida e demonstrar avaliação pela CLI separada, referência apenas nessa etapa e originais preservados em `evidencias/spec004/revisao-textual-2026-11-01/`.

Dependência vigente: T049 → T050/T051 → T042 → T043–T048. T014/T015 são exigências históricas substituídas, não provas aprovadas. Total: 51 IDs, 49 tarefas vigentes e 2 substituídas. Fechamento técnico não conclui revisão científica nem entrega real/piloto.



## Verificação vigente — 01/11/2026 (D-30)

Engenharia offline do contrato D-29 concluída no alcance verificado: 49 tarefas vigentes atendidas; T014/T015 substituídas, não executadas/aprovadas. Recortes das seis fontes, autorização externa e montagem v3 produziram 16 pacotes; bytes, conteúdo, documentos comuns, notas D1/E1 e ausência de notas D0/E0 confrontados. Referência somente no avaliador separado; resposta de demonstração explicitamente sintética. As 16 famílias estão consolidadas com evidências anteriores preservadas e verificações necessárias das alterações; não se reexecutou pontuação inalterada nem se contou sintéticos como LLM.

[Relatório e limitações](../../evidencias/spec004/revisao-textual-2026-11-01/relatorio.md) inclui comandos, esperado/observado, hashes, matriz, caminhos suportados, limitação da criação de symlink e provas de SO substituídas. As seções de 27/10 são históricas; os gates atuais são D-29 e esta verificação, sem aprovação retroativa. Checklist é qualidade documental, preservada sem remarcação. Sem prova de entrega real ao modelo, modelo escolhido, chamada externa ou piloto. Revisão profissional/científica, notas definitivas, fundamentação das métricas, desenho final/congelamento do piloto e adoção constitucional permanecem pendentes.

Aceitação das tarefas atuais: T049/T050 — recortes-primeira, montagem-revisada e demonstracao-textual-001; T051 — entrada-avaliador e demonstração separada; T042/T044 — matriz.json e relatório critério a critério; T043 — diagnostico.md; T045 — preservacao.json; T046 — reconciliação e checklist intacta; T047 — D-30/governança; T048 — estado-tarefas.json e limites do relatório. Todos os caminhos de evidência são relativos a `evidencias/spec004/revisao-textual-2026-11-01/`. T014/T015 permanecem desmarcadas exclusivamente como exigências substituídas, não pendências para provisionamento.
