# Decisões, propostas e pendências

## Revisão das tarefas da Spec 003 — 21/10/2026

**D-19 — Autorização do pesquisador.** Responsável: usuário/pesquisador; evidência: pedido explícito nesta conversa para revisar tasks existente, completar apenas o necessário, analisar consistência e reconciliar estado. Somente documentação; sem variantes, testes ou chamadas ao LLM. Revisão profissional, possíveis novos modelos e mudanças nas métricas aguardam transcrição da orientação e decisão explícita.

Conferência pelo assistente: árvore inicialmente limpa; HEAD `8041b0b1deca09f13c8b95069699616c7a1a7a60`; Spec 003 em `.specify/feature.json`, confirmada por `check-prerequisites.sh --json --require-spec --require-tasks --include-tasks`. B disponível; blobs de código/testes/JSON coincidem com o plano. Diff contra B vazio para código, testes, JSON, requisitos, catálogo e evidências T12. Referência 0.2 candidata sem revisor/data; 12 casos, 48 expectativas e seleções 2/4/8/5 preservados.

35 tarefas mantidas pendentes; T024 esclarece controles sintéticos no teste novo e matriz real no verificador, sem depender da CLI futura T027. Nenhuma tarefa concluída por inspeção. Notas vigentes preservam os registros históricos. Análise posterior somente de leitura pela skill local speckit-analyze, com relatório na resposta; sem implementação ou execução da bancada. Pendências científicas e adoção constitucional preservadas.


## Tarefas e análise documental da Spec 003 — 20/10/2026

**D-18 — Autorização do pesquisador.** Responsável: usuário/pesquisador; evidência: pedido explícito nesta conversa para gerar tarefas da Spec 003 pelo fluxo local e analisar a consistência Spec/plano/tarefas, preservando expectativas, conjuntos e pendências científicas. Autoriza somente trabalho documental e reconciliação de contexto; não autoriza implementar variantes, executar testes, iniciar piloto ou chamadas ao LLM experimental. Não representa aprovação científica do orientador ou ratificação constitucional.

Execução documental pelo assistente em 20/10/2026: Spec ativa 003 em `.specify/feature.json`, confirmada por `setup-tasks.sh --json`; template local e research/data-model/contracts/quickstart disponíveis. Árvore inicialmente limpa, HEAD `53bbac223e17dd15516a6d0172275ed995b7dd46`. Leitura dos blobs de B `aec474bcb54d6dae2afceff8e5b9226991386490` confirmou 18 métodos/T12 e referência candidata 0.2 com 12 casos/48 expectativas/conjuntos 2/4/8/5; nenhum módulo da bancada importado ou teste executado.

Gerado [tasks.md](../specs/003-mudancas-controladas/tasks.md): **35 tarefas, todas pendentes**; Setup 2, Fundação 6, US1 9, US2 8, US3 6, Fechamento 4. Quatro tarefas paralelizáveis, somente fontes distintas das variantes após pré-condições. Formato/IDs/caminhos/links conferidos documentalmente; baseline, testes, materiais e referência intactos. Geração pela [skill tasks](../.agents/skills/speckit-tasks/SKILL.md); análise posterior pela [skill analyze](../.agents/skills/speckit-analyze/SKILL.md) em modo somente leitura, com relatório na resposta desta solicitação e sem corrigir silenciosamente achados. Sem arquivo de implementação criado.

Estado de engenharia: especificação, planejamento e tarefas documentados, ainda sem variantes ou teste novo executável. A análise não é teste da aplicação, validação científica ou autorização de implementação. P-01/P-02/P-03 e adoção constitucional continuam pendentes; T12 já adotado em B, expectativas das mudanças ainda candidatas sob P-02. Próxima ação: revisar tarefas e eventuais achados da análise; implementação exige pedido próprio. Registros anteriores mantêm o histórico das etapas, superados apenas no alcance autorizado por D-18.

## Planejamento da Spec 003 — 19/10/2026

**D-17 — Autorização do pesquisador e fechamento documental.** Responsável pela autorização: usuário/pesquisador; evidência: pedido explícito nesta conversa para planejar a Spec 003 pelo fluxo local, selecionar/confirmar a feature ativa, manter Python + unittest e preservar expectativas/conjuntos. Autoriza cinco artefatos de planejamento e reconciliação documental; não autoriza tarefas, variantes implementadas, teste de aplicação, piloto ou LLM experimental. Execução técnica documental: assistente, 19/10/2026. Não representa aprovação científica do orientador ou ratificação constitucional.

Árvore inicialmente limpa; HEAD `3cdff8ec1c82b4919bce3761364364754863ca81`. B permanece `aec474bcb54d6dae2afceff8e5b9226991386490`, já fixado na Spec. Leitura Git/AST confirmou RF-01–RF-04, 18 métodos/T01–T12, controles e JSON 0.2 com 48 expectativas e seleções 2/4/8/5. Código, testes, referência, requisitos, catálogo e evidências T12 sem diferença entre B e HEAD; nenhuma alteração relevante não commitada na inspeção inicial. Nenhum teste repetido nesta etapa.

Feature ativa persistida em `.specify/feature.json`: `specs/003-mudancas-controladas`. `check-prerequisites.sh --json --paths-only` confirmou destino de FEATURE_SPEC/IMPL_PLAN antes de `setup-plan.sh --json`; template copiado em 003. Setup e criação de contracts inicialmente negados pelo sandbox e repetidos com autorização técnica. BRANCH no JSON é contexto, sem branch/commit criado. Fluxo [speckit-plan](../.agents/skills/speckit-plan/SKILL.md), sem hooks de extensão; pesquisa técnica local e revisão auxiliar de leitura previstas pela skill, sem chamadas experimentais.

Artefatos: [plan](../specs/003-mudancas-controladas/plan.md), [research](../specs/003-mudancas-controladas/research.md), [data-model](../specs/003-mudancas-controladas/data-model.md), [contrato](../specs/003-mudancas-controladas/contracts/verificacao.md) e [quickstart](../specs/003-mudancas-controladas/quickstart.md). Desenho escolhido: quatro módulos independentes copiados diretamente de B, edição mínima e diff/AST; verificador local com snapshot/hashes e registros esperado/observado por par; 12 casos em cada variante, sem filtro de seleção. Suíte inicial preservada. Representação e comandos estão planejados, não implementados ou executados.

Constituição conferida antes/depois do desenho, sem violação ou dúvida técnica bloqueante. P-01/P-02/P-03 e adoção formal continuam pendentes; P-04 já tem T12 adotado/verificado em B, expectativas das mudanças permanecem candidatas. Gabarito/seleções não alterados. Próxima ação: revisão do planejamento e solicitação de tarefas quando desejado; nenhuma etapa seguinte iniciada automaticamente. Registros anteriores abaixo são históricos nos alcances superados por D-17.

## Adoção de T12 e fechamento técnico — 19/10/2026

**D-15 — Autorização do pesquisador.** Responsável: usuário/pesquisador. Evidência: pedido explícito nesta conversa, “Confirmo a adoção de T12 no catálogo da bancada”, com entrada ativa, Supervisão + Auditoria, exportar e resultado inicial negar/conflito. Autoriza acrescentar o teste, executar isolado e suíte integrada, atualizar catálogo, rastreabilidade, referência candidata/JSON e artefatos dependentes, preservar histórico e reconciliar estado/handoff/pendências. Justificativa: acrescentar a operação exportar sob conflito herdado, complementando T07. Não atribui aprovação científica ao orientador nem adota formalmente a constituição. Não autoriza implementar/executar variantes, piloto ou chamadas ao LLM experimental.

Expectativas candidatas autorizadas para registro: MC-01 negar/conflito, preservação selecionada; MC-02 permitir/permissao_direta, mudança selecionada; MC-03 negar/conflito, excluído pela política; MC-04 permitir/permissao_direta, mudança selecionada. MC-04 aqui é a retirada de herança já identificada como **MC-04-v2**; mantém-se esse ID no JSON para evitar ambiguidade com a antiga mudança de estado. Não há acumulação: cada mudança parte da mesma versão inicial.

**D-16 — Fechamento de engenharia sob D-15.** Responsável pela execução: assistente, 19/10/2026. Evidências em [evidencias-t12.md](evidencias-t12.md): Python 3.13.3; T12 isolado OK; suíte integrada com 18 métodos OK, sem falhas/erros/ignorados. T01–T11, seis métodos auxiliares, controles e regras preservados; somente T12 foi acrescentado ao código de testes. Nenhuma divergência na versão inicial; resultado negar/conflito conforme RF-03/RF-04, prevalecendo sobre exportar direto de RF-02.

Catálogo vigente T01–T12; 48 pares teste × mudança e 60 expectativas com a versão inicial. Referência candidata 0.2, seleções 2/4/8/5; conjuntos de RFs intactos. Histórico anterior preservado literalmente com hashes em [pré-T12](historico/pre-t12-2026-10-19/LEIA_PRIMEIRO.md). Foram harmonizados requisitos, testes, documento de revisão, materiais 01–06 e guia, JSON, estado, governança operacional e handoff. Bloco de definições comuns em `materiais/07_DEFINICOES_COMUNS.md`, obrigatório e igual às quatro condições, sem respostas; notas candidatas intactas. Schema sem restrição de IDs não exigiu alteração; manifesto continua não congelado. Artefatos das Specs são históricos do incremento e recebem aviso de complemento em D-15, preservando evidências antigas.

P-04: **adoção e engenharia concluídas**, expectativas das mudanças ainda candidatas e sujeitas à revisão humana em P-02. P-01/P-02/P-03 e adoção constitucional permanecem abertas nos seus demais alcances. Próxima ação: revisão humana da referência 0.2, notas, política e medidas; revisor/data a combinar. Variantes não implementadas nem executadas; sem piloto/LLM experimental. Registros abaixo são históricos e seus limites não revogam D-15.

## Fechamento anterior — 18/10/2026

D-14 — Execução técnica pelo assistente sob autorização D-13, em 18/10/2026. Evidências: [quickstart da Spec 002](../specs/002-heranca-incompatibilidade/quickstart.md), relatório bruto final e revisão do diff. T001–T022 concluídas; RF-01–RF-04 integrados, 17 métodos OK, onze casos com decisão/motivo conformes e 55 subtestes. Dez métodos originais e expectativas preservados. Estado precede conflito, direta precede herdada. Domínio válido ampliado; verificação dirigida sem T12. Sem alteração de gabarito, materiais, variantes, piloto ou chamadas experimentais. D-09 e P-01/P-02/P-03/P-04 preservados; engenharia não equivale a validação científica. Nenhuma pendência funcional bloqueante no incremento; próxima etapa exige autorização própria.

## Autorização anterior — 18/10/2026

D-13 — Responsável: usuário/responsável do projeto; evidência: pedido explícito nesta conversa para implementar a Spec 002 seguindo suas 22 tarefas com Python e unittest. Autoriza implementação, testes locais e reconciliação documental; preserva gabarito e T12 como proposta. Não autoriza variantes, piloto ou LLM experimental nem representa aprovação científica ou adoção formal da constituição.

Reconciliação prévia: tasks, estado e handoff já registravam geração de 22 tarefas e análise em 16/10, posteriores ao planejamento D-12. BLOQUEIOS e a próxima ação de D-12 estavam desatualizados. Esses limites são históricos, superados pelo pedido atual apenas no alcance de engenharia. Nenhuma divergência funcional bloqueante identificada.

## Planejamento da Spec 002 — 16/10/2026

D-12 — Responsável pela autorização: usuário/responsável do projeto; evidência: solicitação explícita desta conversa para selecionar Spec 002 e preparar planejamento técnico com Python + unittest, aproveitando organização existente. Autoriza somente cinco artefatos de planejamento, seleção local e reconciliação de estado/handoff/bloqueios/decisões. Sem geração de tarefas, código, testes de aplicação, variantes, piloto ou LLM experimental; não registra aprovação científica.

Seleção pelo mecanismo local documentado em common.sh: .specify/feature.json → specs/002-heranca-incompatibilidade. Destino confirmado por check-prerequisites.sh --json --paths-only antes de setup-plan.sh --json, que copiou o template no destino certo. BRANCH no JSON é identificador de contexto; nenhuma branch criada. Sandbox inicialmente negou escrita do setup e criação de contracts; repetições com permissão técnica concluídas. O apontador é estado local ignorado pelo Git.

Desenho em [plan.md](../specs/002-heranca-incompatibilidade/plan.md): funções puras de efetivos e incompatibilidade; consulta direta preservada; estado → conflito → decisão por permissão, com direta antes de herdada e ausência por último. Interface existente conservada; domínio ativo ampliado apenas na implementação futura. Nenhuma nova decisão funcional necessária ou contradição bloqueante identificada; preferência direta/herdada já consta no contrato completo.

Cinco artefatos produzidos: plan, research, data-model, contracts/autorizacao e quickstart. Revisão documental pré/pós-desenho conforme constituição, sem exceções identificadas. Testes antigos não repetidos e testes novos não executados; RF-03/RF-04 continuam não implementados. T12 fora dos critérios; gabarito e catálogo intactos. Adoção formal da constituição, P-01 parcialmente atendida e P-02/P-03/P-04 continuam pendentes. Próxima ação: revisão e solicitação de tarefas.

Registros anteriores abaixo preservam o histórico; seus limites temporais não revogam D-12.

## Fechamento de engenharia — 16/10/2026

D-11: execução técnica pelo assistente sob autorização D-10; evidências observadas em [evidencias.md](../specs/001-autorizacao-direta/evidencias.md). Python 3.13.3; 10 métodos unittest OK; SC-001–SC-004 atendidos no domínio parcial. T001–T017 concluídas com revisão código/contrato/documentação. RF-03/RF-04 futuros, sem alteração de contrato ou expectativas T05–T08; referência original preservada. Sem piloto ou LLM experimental. Retorno científico permanece limitado a D-09 e proposta P-04.

## Registro vigente — 16/10/2026

D-09: orientador, conforme relato explícito do usuário nesta conversa (data do registro; data da manifestação não informada): recorte da bancada aceito, autorizado prosseguir. Gabarito, notas, prompts, métricas e piloto ainda serão revisados. P-01 parcialmente atendida quanto ao recorte; demais detalhes não recebem aprovação científica por consequência. P-02/P-03 continuam pendentes.

Ajuste solicitado: retirar a herança em MC-04 elimina o conflito em Supervisão + Auditoria, pois Consulta deixa de ser papel efetivo, e pode liberar exportar pela concessão direta de Auditoria. T07 continua correto para visualizar: baseline negar/conflito; sem herança negar/sem_permissao.

P-04: proposta do usuário, ainda não adotada nem executada: T12, ativa, Supervisão + Auditoria, exportar. Baseline negar/conflito; MC-04 sem herança permitir/permissao_direta. Antes de adotar, revisar relevância nas quatro mudanças, inclusões/exclusões, expectativas, conjuntos candidatos, notas/prompts, tamanho da suíte e cálculos/denominadores. Seriam 12 casos e 48 pares teste × mudança em vez de 11/44, sem alterar por si o número de chamadas. Catálogo e referência JSON permanecem preservados.

D-10: usuário, pedido explícito desta conversa em 16/10/2026: implementação da Spec 001, 17 tarefas, Python + unittest e testes locais autorizados. Supera restrições temporais anteriores somente nesse alcance. Sem RF-03/RF-04, piloto ou LLM experimental. Adoção formal da constituição pendente.

Conferência prévia de Spec/plano/tasks/modelo/contrato: sete casos coerentes, concessões próprias distintas da autorização final, estado primeiro e domínio parcial sem guarda adicional. Nenhuma contradição funcional bloqueante identificada; nenhum contrato alterado. Registros abaixo descrevem etapas históricas.

Registro inicial: 14/10/2026. Fontes: solicitação do usuário nesta conversa e [fontes e decisões](../materiais/06_FONTES_E_DECISOES.md). Não há aprovação do orientador registrada nos materiais consultados. Ausência de resposta ou aprovação parcial não aprova os demais pontos.

## Diretrizes com autorização registrada

| ID | Diretriz | Origem e alcance |
|---|---|---|
| D-01 | Preparar somente os seis documentos da baseline, preservando materiais. | Usuário, 14/10/2026; autorização documental, sem implementação ou abertura de Spec. |
| D-02 | Distinguir propostas, pendências e evidências; não declarar gabarito validado ou testes executados. | Usuário, 14/10/2026; vale para toda a baseline. |
| D-03 | Exigir resposta válida, seleção completa e IDs existentes para interpretar redução favoravelmente. | Usuário, 14/10/2026; harmonização com o protocolo candidato. |
| D-04 | Fazer o número de blocos depender das repetições finalmente definidas. | Usuário, 14/10/2026; cinco blocos não são quantidade fixa aprovada. |
| D-05 | Distinguir documentação preparada de liberação para piloto. | Usuário, 14/10/2026; condições de entrada permanecem obrigatórias. |

Estas autorizações não equivalem à aprovação científica do desenho pelo orientador.

## Três grupos de alinhamento com o orientador

| ID | Proposta submetida / decisão necessária | Situação e responsável esperado |
|---|---|---|
| P-01 — Objeto e casos | Manter seleção de IDs no módulo, impacto funcional em dependências, entrega sem framework geral e substituição da antiga MC-04 por retirada da herança (MC-04-v2). | Pendente de alinhamento com orientador; pesquisador registra resposta e ajustes. |
| P-02 — Referência e medidas | Confirmar política conservadora incluindo preservação; precisão, revocação e F1 separados para RF/testes, consistência e redução condicionada. Definir revisor do gabarito e das notas. | Pendente de alinhamento com orientador; revisão humana ainda não concluída. |
| P-03 — Execução | Confirmar D0/D1/E0/E1, uma chamada independente, piloto de 16, proposta de 80 chamadas principais, análise descritiva e congelamento após piloto. | Pendente de alinhamento com orientador; quantidade final depende da viabilidade. |

## Outras propostas e pendências

- Contrato de decisão/motivo, precedência e critérios dos RFs: revisão conforme [requisitos.md](requisitos.md), especialmente antes da implementação correspondente.
- Referência: revisor e data a combinar; registrar divergências e resolução antes do piloto. Notas também exigem revisão de origem e neutralidade.
- Tecnologias, modelo/configuração, isolamento e formatos: escolhas do pesquisador a registrar antes dos respectivos incrementos; sugestões em [arquitetura.md](arquitetura.md).
- Repetições, orçamento e ordem: fixar após avaliação de viabilidade e antes dos resultados principais. Para r repetições, planejar r blocos de 16 combinações; 80 chamadas correspondem somente à proposta r = 5.
- Avanço de etapa: esta entrega não autoriza implementação, abertura de Spec, piloto ou coleta. Futuras ações dependem de autorização no respectivo escopo e dos critérios do [roadmap.md](roadmap.md).

## Como atualizar

Para cada decisão futura, registrar ID, data, responsável pela aprovação, evidência da resposta, decisão e justificativa, ajustes solicitados, documentos/versões afetados e próxima ação. Enquanto não houver esse registro, manter o item como proposta ou pendência. Materiais históricos não são decisões simultaneamente vigentes; a substituição de MC-04 continua candidata.

## Atualização de engenharia — especificação e tarefas (14/10/2026)

| ID | Decisão e evidência | Alcance e efeito |
|---|---|---|
| D-06 | Usuário forneceu o contrato RF-01/RF-02 e solicitou `$speckit-specify` nesta conversa. | Base de engenharia para a Spec 001: estado, concessões próprias e decisão/motivo; RF-03/RF-04 ficam para o próximo incremento. Sem aprovação do orientador ou validação científica. |
| D-07 | Usuário declarou: “Confirmo Python + unittest e a organização mínima proposta como escolhas técnicas para o primeiro incremento.” | Python + biblioteca padrão unittest, sem terceiros; `autorizacao.py` e `tests/test_autorizacao.py`. Versão exata do interpretador a conferir no ambiente; 3.11+ é a compatibilidade proposta no plano. |
| D-08 | Usuário solicitou planejamento e, depois, geração de tarefas e análise de consistência nesta conversa. | Spec e plano existentes; tarefas documentadas, todas pendentes. Não autoriza implementação, execução de testes da aplicação, piloto ou coleta. Substitui as restrições temporais das entregas anteriores apenas nesse alcance. |

Responsável pelas confirmações acima: usuário/responsável do projeto; evidência: solicitações explícitas desta conversa em 14/10/2026. Justificativa técnica e desenho em [plano da Spec 001](../specs/001-autorizacao-direta/plan.md). Assinaturas e representações do contrato são desenho de implementação, sem alegar confirmação específica além da linguagem, ferramenta e organização declaradas pelo usuário.

P-01/P-02/P-03, adoção formal da constituição e revisão humana da referência/notas permanecem pendentes. O contrato completo RF-01–RF-04 não foi reduzido. Próxima ação: revisar tasks e, quando solicitado implementar, cumprir verificações e atualizar evidências reais.
