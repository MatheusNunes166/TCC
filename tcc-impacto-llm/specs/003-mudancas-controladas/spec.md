> Estado vigente — 21/10/2026 (D-20/D-21): Spec 003 implementada e verificada; 35/35 tarefas concluídas com evidências. Quatro variantes independentes de B `aec474bcb54d6dae2afceff8e5b9226991386490`, uma edição por fonte, diffs/AST e revisão registrados. Python 3.13.3: suíte original 18 métodos OK, baseline 12/12 pares e variantes 48/48 conformes por decisão/motivo, zero divergências/erros/lacunas; 17 métodos sintéticos separados da bancada. Baseline, testes, materiais, referência candidata 0.2 e seleções 2/4/8/5 preservados. Evidências e diagnóstico do mecanismo: `specs/003-mudancas-controladas/evidencias.md` (desde a raiz). P-01/P-02/P-03, revisão das expectativas T12 e adoção constitucional pendentes; T12 já adotado/verificado em B. Revisão profissional, possíveis novos modelos e métricas aguardam transcrição da orientação e decisão explícita. Sem piloto, coleta ou LLM. Próxima ação: revisão humana das evidências e da referência candidata, seguida de detalhamento da orientação; nenhuma etapa experimental liberada. Registros anteriores abaixo são históricos.

# Feature Specification: Quatro mudanças controladas e verificação de efeitos

**Feature Directory**: `specs/003-mudancas-controladas`

**Created**: 2026-10-19

**Status**: Draft — revisada documentalmente; implementação e execução não iniciadas.

Atualização de etapa — 20/10/2026, D-18: [tasks.md](tasks.md) gerado com 35 tarefas, todas pendentes, seguido de análise somente documental. Nenhuma tarefa foi executada; sem variantes ou testes nesta etapa. As restrições temporais anteriores abaixo descrevem suas etapas, superadas apenas para geração/análise documental; requisitos, expectativas e conjuntos preservados.

Atualização de etapa — 19/10/2026, D-17: planejamento autorizado posteriormente, concluído em [plan.md](plan.md) e artefatos vinculados. Spec 003 selecionada/confirmada como ativa. Nenhuma tarefa, implementação ou execução de variante iniciada; expectativas e requisitos abaixo preservados. Menções a “somente Spec/checklist” em Assumptions descrevem a autorização da etapa de especificação.

**Input**: solicitação explícita do pesquisador nesta conversa para preparar somente Spec e checklist pelo fluxo do Spec Kit, especificando quatro mudanças independentes, preservação da versão inicial e comparação futura dos 12 casos por variante, sem ajustar automaticamente o gabarito ao código.

**Versão inicial B**: commit `aec474bcb54d6dae2afceff8e5b9226991386490` (`adicionando cenario de testes T12`). Identificado em leitura do repositório, inicialmente com árvore limpa; contém T12 e a referência candidata 0.2. Nenhum commit ou branch foi criado nesta etapa.

## User Scenarios & Testing *(mandatory)*

Os cenários são critérios para execução futura sob autorização própria. Revisar esta Spec não executa esses cenários nem valida cientificamente a referência.

### User Story 1 - Comparar mudanças com origem comum (Priority: P1)

Como pesquisador, quero preservar uma versão inicial identificada e obter quatro variantes com uma única alteração de política em cada uma, para atribuir os efeitos observados à mudança correspondente.

**Why this priority**: sem origem comum e isolamento, os resultados podem decorrer de alterações acumuladas.

**Independent Test**: conferir a origem e a diferença de política de cada variante em relação a B, independentemente do relatório de efeitos.

**Acceptance Scenarios**:

1. **Given** B no commit identificado, **When** uma variante for preparada, **Then** sua origem registrada será esse mesmo commit, sem políticas de outras variantes ou alterações locais adicionais.
2. **Given** MC-01 preparada, **When** MC-02 for preparada, **Then** MC-02 manterá Auditoria → exportar de B e retirará somente a incompatibilidade Consulta + Auditoria.
3. **Given** as quatro variantes, **When** as diferenças em relação a B forem revisadas, **Then** haverá uma única alteração de política por variante conforme a tabela de mudanças, com identificação verificável de cada versão executável.
4. **Given** preparação ou verificação concluída, **When** B for conferida, **Then** código, catálogo, expectativas e controles da versão inicial continuarão disponíveis sem alteração e sem efeitos residuais das variantes.

### User Story 2 - Conferir todos os efeitos por decisão e motivo (Priority: P2)

Como pesquisador, quero executar os 12 casos existentes em cada variante e compará-los com a referência candidata 0.2, para conferir mudanças e preservações em todo o catálogo.

**Why this priority**: verificar somente a decisão ou somente os testes selecionados para regressão pode ocultar efeitos indevidos e mudanças de motivo.

**Independent Test**: para uma variante identificada com origem comprovada, produzir 12 registros de comparação, incluindo casos selecionados e excluídos pela política, mesmo antes de conferir as outras variantes.

**Acceptance Scenarios**:

1. **Given** MC-01 isolada, **When** T01–T12 forem executados, **Then** cada par observado será comparado com a referência; T04 terá expectativa `negar/sem_permissao` e T12 `negar/conflito`.
2. **Given** MC-02 isolada, **When** os 12 casos forem executados, **Then** T06 terá expectativa `permitir/permissao_direta`, T07 `permitir/permissao_herdada`, T12 `permitir/permissao_direta` e T11 `negar/estado`.
3. **Given** MC-03 isolada, **When** os 12 casos forem executados, **Then** T02 e T05 terão expectativa `negar/sem_permissao`; T12 também será executado, com expectativa `negar/conflito`, embora excluído da seleção candidata dessa mudança.
4. **Given** MC-04 isolada, **When** T07 for conferido, **Then** a expectativa será `negar/sem_permissao`, distinguindo-a de `negar/conflito` em B; T12 terá expectativa `permitir/permissao_direta`, em lugar de `negar/conflito` em B.
5. **Given** as quatro verificações, **When** o relatório for consolidado, **Then** cada um dos 48 pares distintos terá comparação ou falha/lacuna explicitamente registrada; somente 48 comparações executadas e conformes permitirão declarar conformidade integral das variantes.

### User Story 3 - Investigar divergências e distinguir aprovações (Priority: P3)

Como pesquisador ou revisor, quero analisar divergências pelas regras e distinguir conformidade executável de revisão científica, para evitar tratar o código como fonte exclusiva das expectativas.

**Why this priority**: concordância com a implementação não valida cientificamente a referência; discordância não autoriza mudar suas respostas silenciosamente.

**Independent Test**: revisar um registro de divergência ou um relatório de conformidade quanto à rastreabilidade, investigação e estado separado da revisão científica. Exemplos documentais não serão classificados como execuções reais.

**Acceptance Scenarios**:

1. **Given** decisão igual e motivo diferente do esperado, **When** a comparação for registrada, **Then** o caso será divergente, conservando os dois pares sem substituir a expectativa pelo observado.
2. **Given** divergência, **When** a causa for investigada, **Then** a análise confrontará RFs, precedência, herança, origem da variante, entrada e referência 0.2, registrando evidências e causa ou hipótese; não presumirá que a implementação está correta.
3. **Given** suspeita de erro na referência, **When** o relatório for concluído, **Then** a suspeita permanecerá pendente de revisão humana, preservando a versão 0.2 e as observações originais; esta Spec não autoriza corrigir expectativas ou conjuntos.
4. **Given** 48 pares conformes em execução futura, **When** o resultado for comunicado, **Then** será declarado como conformidade executável com a referência candidata 0.2, sem aprovação científica atribuída ao orientador ou liberação de piloto/coleta.

### Edge Cases

- Commit B indisponível, origem diferente ou alteração adicional de política: registrar impedimento de procedência e não qualificar a variante como independente.
- Versão inicial divergente de seus 12 resultados ou controles: investigar antes de usar a execução como comparação válida; não corrigir regras ou expectativas automaticamente.
- Mudança somente de motivo, como T07/MC-04: comparar o par completo; decisão igual não significa preservação.
- Maior precedência mantém a saída, como T12/MC-01 e T11/MC-02: registrar preservação sem concluir que a alteração não existe.
- Caso excluído da seleção candidata, como T12/MC-03: executar mesmo assim, porque esta conferência cobre todo o catálogo.
- Caso não executado, erro, saída fora do contrato, duplicata ou ID desconhecido: registrar ocorrência e lacuna; não contar como comparação conforme nem completar observado com valor esperado.
- Repetição após investigação: conservar tentativa e diagnóstico anteriores, distinguindo a nova execução sem sobrescrever evidências.
- Divergência entre requisitos, matriz documental e JSON: registrar fontes e conflito antes de depender da expectativa controversa; não escolher silenciosamente uma fonte ou editar o gabarito.

## Requirements *(mandatory)*

### Functional Requirements

IDs FR são locais desta Spec; RF-01–RF-04 continuam identificando as regras da bancada.

- **FR-001 — origem identificada**: cada mudança DEVE partir de B, no commit completo do cabeçalho. A execução futura DEVE registrar esse commit e identificação verificável de cada variante executada, relacionando origem, diferença de política e resultados. Alterações posteriores no repositório não redefinem B automaticamente.
- **FR-002 — alteração única**: cada variante DEVE aplicar somente a remoção de sua linha na tabela abaixo em relação a B, sem acumular remoções de outras mudanças. Efeitos propagados pelas dependências são consequências da alteração única, não mudanças adicionais de política.
- **FR-003 — preservação da versão inicial**: preparação e execução DEVEM preservar código, entradas T01–T12, saídas esperadas, controles auxiliares e referência de B, sem mutação residual. A conferência futura DEVE comprovar os 12 pares de B e seus controles existentes antes de qualificar comparações das variantes, conservando evidências anteriores e novas separadamente.
- **FR-004 — referência identificada**: as expectativas DEVEM ser as da candidata 0.2 no commit B, rastreáveis a requisitos e catálogo. A execução DEVE identificar a versão usada e conferir sua integridade; o esperado não pode ser gerado a partir do observado. As 48 expectativas e os conjuntos de RFs/testes existentes NÃO DEVEM ser alterados por este incremento sem revisão e autorização separadas.
- **FR-005 — execução completa**: cada variante DEVE executar T01–T12 com as mesmas entradas de B, totalizando 48 pares. Os conjuntos candidatos de regressão de 2/4/8/5 testes NÃO DEVEM reduzir essa execução nem ser modificados. Controles de B não recebem novos IDs experimentais; não se exige preservar nas variantes uma saída de controle que dependa justamente da política retirada.
- **FR-006 — comparação integral**: cada execução DEVE comparar conjuntamente `decisao` e `motivo` com a expectativa da variante. A saída mantém exatamente esses campos e o vocabulário do contrato. Alteração de qualquer valor ou saída fora do contrato DEVE ser distinguida de conformidade; verificar apenas permitir/negar é insuficiente.
- **FR-007 — registro por par**: cada par mudança/teste DEVE registrar ID da mudança, ID do teste, entrada, commit B, identificação da variante executada, referência usada, decisão/motivo esperados, decisão/motivo observados quando disponíveis, estado da execução/comparação, evidência de execução e divergência. Em erro ou ausência de execução, o observado DEVE ficar ausente e a causa explícita. O consolidado DEVE informar executados/previstos, conformes, divergentes, erros e não executados, sem contar duplicatas como pares adicionais ou ausência como conformidade.
- **FR-008 — investigação fundamentada**: cada divergência DEVE conservar esperado/observado originais e análise pelos RFs e sua precedência, conferindo origem/isolamento, entradas e referência. O registro DEVE distinguir causa identificada de hipótese ou causa ainda não determinada, com evidências e resolução ou pendência. Nenhuma divergência pode ser eliminada apenas ajustando o gabarito ao código. Suspeita de erro na referência exige revisão humana em registro próprio com responsável, data e decisão antes de qualquer alteração autorizada.
- **FR-009 — efeitos e preservações**: o relatório DEVE distinguir diferença esperada em relação a B, diferença observada em relação a B e concordância entre esperado e observado na variante. Mudança de comportamento inclui mudança somente de motivo; preservação mantém o par completo. Relevância para seleção continua definida pela política existente, independentemente de mudança da saída final.
- **FR-010 — conclusão e aprovação**: o relatório DEVE distinguir especificado, implementado, executado e conforme, sem marcar descrição como execução. Conformidade integral exige 48/48 pares conformes, B preservada e nenhuma divergência funcional sem resolução. Um relatório com divergências é evidência para investigação, não atestado de conformidade integral. Mesmo conformidade integral NÃO DEVE ser apresentada como aprovação científica do orientador ou liberação de piloto/coleta.

### Mudanças e regras de origem

| ID nesta Spec | ID da referência 0.2 | Única alteração em relação a B | Regras preservadas e efeitos a conferir |
|---|---|---|---|
| MC-01 | MC-01 | Retirar Auditoria → exportar de RF-02 | Consulta → visualizar, herança e incompatibilidade permanecem; conflito ainda pode impedir exportar |
| MC-02 | MC-02 | Retirar incompatibilidade Consulta + Auditoria de RF-04 | Estado, concessões e herança permanecem; acesso pode ser liberado por origem direta ou herdada |
| MC-03 | MC-03 | Retirar Consulta → visualizar de RF-02 | Supervisão ainda inclui Consulta efetivo, mas perde visualizar herdado; incompatibilidade por papéis permanece |
| MC-04 | MC-04-v2 | Retirar Supervisão → Consulta de RF-03 | Concessões de Consulta/Auditoria permanecem; Consulta atribuído continua sujeito a conflito, mas deixa de surgir por Supervisão |

MC-04 é o nome curto de MC-04-v2, sem renomear o JSON ou reintroduzir a antiga proposta de alteração de contas em revisão. RF-01 e a precedência estado → conflito → decisão por permissão permanecem em todas as variantes. Sem bloqueios, direta precede herdada; ausência de concessão resulta em `negar/sem_permissao`.

### Fontes de aceitação e rastreabilidade

Usar os artefatos existentes no commit B, sem reescrever expectativas:

- [Requisitos RF-01–RF-04](../../documentacao/requisitos.md): fundamento das regras, precedência e motivos.
- [Catálogo T01–T12](../../documentacao/qualidade-e-testes.md): entradas e saídas da versão inicial.
- [Referência candidata 0.2](../../documentacao/referencia-candidata-proxima-etapa.md) e [material 02](../../materiais/02_REQUISITOS_TESTES_E_REFERENCIA.md): justificativas e matriz completa de 48 pares.
- [JSON candidato 0.2](../../materiais/modelos/referencia_candidata_NAO_ENVIAR_AO_LLM.json): catálogo de 12 casos e 12 expectativas em `expected` por mudança; status `CANDIDATO_NAO_REVISADO`, revisor/data nulos. Artefato de referência, não fonte exclusiva da verdade.
- [Definições comuns](../../materiais/07_DEFINICOES_COMUNS.md): impacto funcional por dependência, relevância incluindo preservação e seleção estrutural pela versão inicial, sem alteração neste incremento.
- [Evidências T12](../../documentacao/evidencias-t12.md): teste isolado e 18 métodos integrados aprovados anteriormente; não demonstram execução de variantes.

São 12 expectativas de B + 48 de variantes = 60 expectativas. Não são 60 novas observações: nesta etapa nenhuma execução foi realizada. Os exemplos das histórias reproduzem a referência, sem aprová-la ou substituir a matriz completa.

### Key Entities

- **Versão inicial B**: política, código, catálogo, controles e referência identificados por commit e preservados como origem comum.
- **Mudança / variante**: ID, origem B, alteração única, identificação verificável da versão executada e diferenças de política.
- **Caso de teste**: ID T01–T12, estado, papéis atribuídos e operação, com entradas preservadas.
- **Expectativa candidata**: par decisão/motivo de B ou de variante, versão e fundamento nos requisitos.
- **Registro de verificação**: associação mudança/teste/execução, esperado, observado ou erro, comparação, evidência e procedência.
- **Divergência e revisão**: diferença, análise, causa/hipótese, responsável e resolução ou pendência; revisão científica separada de conformidade executável.

## Success Criteria *(mandatory)*

### Measurable Outcomes

Metas futuras, não resultados desta especificação:

- **SC-001**: 4/4 variantes têm o mesmo commit B como origem comprovada, uma única alteração de política e nenhuma acumulação (FR-001/FR-002).
- **SC-002**: B permanece intacta; seus 12/12 casos e controles existentes têm conferência registrada, sem substituir evidências históricas ou expectativas (FR-003/FR-004).
- **SC-003**: o pesquisador dispõe de registros de 48/48 pares distintos; para declarar conformidade integral, os 48 foram executados e coincidem por decisão/motivo com a referência 0.2, sem erros, ignorados ou lacunas (FR-005–FR-007/FR-010).
- **SC-004**: 100% dos pares têm procedência, referência, entrada e estado explícitos; caso não executado tem ausência/causa visíveis e impede declarar verificação completa (FR-007).
- **SC-005**: 100% das divergências conservam esperado/observado e análise rastreável às regras, com causa ou pendência explicitada; nenhuma expectativa ou conjunto é ajustado automaticamente. Se não houver divergências, registrar zero ocorrências, sem inventar investigação (FR-004/FR-008).
- **SC-006**: o relatório permite distinguir mudança de motivo em T07/MC-04, expectativa de liberação em T12/MC-04 e preservações; execução inclui testes excluídos da seleção, sem modificar conjuntos (FR-005/FR-006/FR-009).
- **SC-007**: o fechamento distingue conformidade executável e aprovação científica, mantém revisões pendentes e não inicia nem declara liberados piloto, coleta ou LLM experimental (FR-010).

## Assumptions

- **Autorização desta etapa**: pesquisador, pedido explícito nesta conversa em 19/10/2026, somente Spec e checklist. Sem plano, tarefas, código, implementação de variantes, teste de aplicação, piloto ou LLM experimental. Supera orientações anteriores de não abrir Spec somente nesse alcance. Autorização/estado desta entrega ficam nestes dois artefatos; registros centrais permanecem intactos por restrição de escopo do usuário.
- **Fluxo**: [skill local speckit-specify](../../.agents/skills/speckit-specify/SKILL.md), template local e numeração sequencial; próxima pasta disponível 003. A existência da Spec não declara capacidade implementada.
- **Fonte inicial**: B inclui T12 adotado em D-15 e execução anterior em D-16. Engenharia não presume revisão científica; menções a T12 como proposta nas Specs anteriores são históricas.
- **Dependências para execução futura**: disponibilidade do commit B e sua referência 0.2, autorização própria de implementação/verificação e comprovação de origem. Pendências científicas não impedem especificar a engenharia; não são resolvidas por esta Spec nem liberam experimento.
- **Domínio**: três estados válidos, subconjuntos dos três papéis, visualizar/exportar, um nível de herança e a incompatibilidade existente. Entradas malformadas e ampliação do catálogo ficam fora do escopo.
- **Limites futuros**: preparar/conferir quatro variantes e registrar evidências locais. Não desenvolver coletor/avaliador experimental, alterar notas/prompts, gerar novos testes experimentais, ampliar fatores ou criar framework geral. Representação das variantes e formato de registros pertencem ao planejamento posterior.
- **Contextos**: esta Spec contém expectativas e exemplos resolvidos; não integra pacote permitido ao LLM avaliado. Isolamento experimental exige evidência própria em etapa futura.

### Revisões científicas e institucionais pendentes

Conforme [decisões](../../documentacao/decisoes.md) e [pendências](../../BLOQUEIOS.md):

- **P-01**: confirmar cientificamente critério funcional de impacto e detalhes do desenho, incluindo retirada de herança como quarta mudança. A especificação técnica atende ao pesquisador sem atribuir aprovação científica ao orientador.
- **P-02**: revisão humana da referência 0.2, política conservadora incluindo preservação, notas, prompts e métricas; revisor/data a combinar. Conformidade com 48 expectativas não conclui essa revisão.
- **P-03**: condições, piloto, repetições, análise e congelamento continuam pendentes nos alcances registrados.
- **P-04**: T12 já adotado e verificado em B; não há nova decisão de adoção a solicitar. Expectativas nas quatro mudanças continuam candidatas, integradas à revisão P-02.
- Adoção formal da constituição pendente; modelo/API, orçamento, coleta, avaliação e isolamento continuam futuros. Documentação pronta ou conformidade executável não libera piloto/coleta.
