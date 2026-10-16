# Feature Specification: Herança de um nível e incompatibilidade efetiva

**Feature Branch**: não criada; nenhum hook de branch configurado.

**Feature Directory**: `specs/002-heranca-incompatibilidade`

**Created**: 2026-10-16

**Status**: especificação, planejamento e tarefas preparados; análise de consistência realizada. As 22 tarefas T001–T022 estão pendentes; nenhum teste da Spec 002 executado e RF-03/RF-04 não implementados. T12 fora da aceitação; revisões científicas pendentes.

**Input histórico da especificação**: pedido explícito do usuário nesta conversa: conferir o fechamento do incremento 1 e especificar RF-03/RF-04, preservando RF-01/RF-02. Naquela etapa, produzir somente Spec e checklist, sem plano, tarefas, código, variantes, piloto ou chamadas ao LLM experimental.

**Atualização documental — 16/10/2026**: solicitações posteriores autorizaram o [planejamento](plan.md), a geração de [22 tarefas](tasks.md) e a análise de consistência. A análise identificou cobertura dos oito itens funcionais e seis critérios de sucesso, sem contradição funcional ou tarefa sem vínculo; os trechos temporais desatualizados são reconciliados nesta atualização. Nenhuma tarefa executada; requisitos, critérios de aceitação e gabarito preservados.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Reconhecer acesso herdado (Priority: P1)

Como pesquisador, quero distinguir permissões próprias de herdadas para verificar que Supervisão inclui Consulta e herda somente visualizar.

**Why this priority**: RF-03 completa as concessões da baseline e estabelece os papéis efetivos usados por RF-04.

**Independent Test**: avaliar Supervisão isoladamente nas duas operações, sem conflito, conferindo decisão e motivo.

**Acceptance Scenarios**:

1. **Given** conta ativa com Supervisão, **When** solicita visualizar, **Then** retorna `permitir/permissao_herdada` (T05).
2. **Given** conta ativa com Supervisão, **When** solicita exportar, **Then** retorna `negar/sem_permissao` depois de considerar a herança (T08).
3. **Given** conta em revisão com Supervisão, **When** solicita visualizar, **Then** mantém `negar/estado` (T10), sem permitir que a herança contorne o bloqueio.

### User Story 2 - Bloquear incompatibilidade efetiva (Priority: P1)

Como pesquisador, quero bloquear Consulta + Auditoria efetivos, inclusive quando Consulta vier da herança, para que permissões não contornem conflito.

**Why this priority**: verificar apenas papéis atribuídos deixaria de reconhecer o conflito herdado em T07.

**Independent Test**: T06 verifica conflito direto sem depender da herança; T07 integra RF-03/RF-04; T11 preserva a precedência do estado.

**Acceptance Scenarios**:

1. **Given** conta ativa com Consulta + Auditoria, **When** solicita visualizar, **Then** retorna `negar/conflito`, apesar da concessão direta (T06).
2. **Given** conta ativa com Supervisão + Auditoria, **When** solicita visualizar, **Then** inclui Consulta nos papéis efetivos e retorna `negar/conflito`, apesar da concessão herdada (T07).
3. **Given** conta em revisão com Consulta + Auditoria, **When** solicita visualizar, **Then** mantém `negar/estado`, e não `conflito` (T11).

### User Story 3 - Preservar o primeiro incremento (Priority: P1)

Como pesquisador, quero integrar as novas regras preservando decisões, motivos e concessões próprias já verificados, para completar a baseline com regressão observável.

**Why this priority**: RF-03/RF-04 ampliam o domínio garantido sem redefinir RF-01/RF-02.

**Independent Test**: na futura implementação integrada, conferir os sete casos anteriores e seus controles com as expectativas originais.

**Acceptance Scenarios**:

1. **Given** entradas T01/T02/T03/T04/T09/T10/T11, **When** avaliadas com as novas regras, **Then** os sete pares decisão/motivo permanecem os da tabela abaixo.
2. **Given** Consulta, Auditoria e Supervisão isoladamente, **When** consultadas suas concessões próprias, **Then** permanecem respectivamente somente visualizar, somente exportar e nenhuma; herança não passa a ser concessão própria.
3. **Given** qualquer subconjunto dos três papéis e qualquer das duas operações, **When** a conta está suspensa ou em revisão, **Then** mantém `negar/estado` nas 32 combinações auxiliares anteriores.

### Edge Cases

- Conta ativa sem papéis: `negar/sem_permissao` nas duas operações.
- Supervisão + Consulta não cria conflito: visualizar retorna `permitir/permissao_direta`, pois Consulta foi atribuído; exportar retorna `negar/sem_permissao`. Quando origens direta e herdada coexistem para a operação, prevalece a direta.
- Auditoria isolada não herda visualizar: preservar o controle `negar/sem_permissao`.
- Incompatibilidade depende dos papéis efetivos, independentemente da operação: concessão não libera conflito e ausência de permissão não o encobre. Estado não ativo sempre prevalece.
- Avaliar não altera entradas nem política; repetir solicitações mantém resultados. Controles auxiliares não acrescentam IDs ao catálogo experimental.
- Entradas malformadas, outros papéis/conflitos, herança multinível e ciclos estão fora do recorte.

## Requirements *(mandatory)*

### Functional Requirements

Os IDs RF existentes são preservados, sem criar novos requisitos funcionais.

- **RF-03 — papéis efetivos**: incluir todos os papéis atribuídos e incluir Consulta sempre que Supervisão estiver presente, pela única relação de herança de um nível. Não herdar Auditoria nem remover papéis atribuídos.
- **RF-03 — concessão herdada**: Supervisão herda visualizar de Consulta, sem herdar exportar. A decisão por ausência de permissão deve considerar concessões diretas e herdadas.
- **RF-04 — incompatibilidade**: Consulta e Auditoria simultâneos nos papéis efetivos produzem `negar/conflito` em conta ativa, inclusive se Consulta vier da herança e mesmo com permissão para a operação. Nenhuma outra combinação é incompatível na baseline.
- **RF-01/RF-04 — precedência**: estado não ativo produz `negar/estado` antes das demais decisões. Em conta ativa, conflito prevalece sobre concessão e ausência de permissão. Precedência das negações: estado → conflito → ausência de permissão.
- **RF-02/RF-03 — origem**: sem bloqueios, concessão direta produz `permitir/permissao_direta`; somente herdada produz `permitir/permissao_herdada`; ausência de ambas produz `negar/sem_permissao`. Se ambas concedem a operação, prevalece `permissao_direta`, conforme o contrato completo existente.
- **RF-01–RF-04 — saída**: preservar exatamente os campos `decisao` e `motivo`, com valores do vocabulário existente e sem campos adicionais. Verificar os dois valores em conjunto; apenas permitir/negar é insuficiente.
- **RF-01/RF-02 — regressão**: preservar as concessões próprias, os resultados garantidos e os controles do primeiro incremento, sem efeitos externos ou alteração das entradas. A consulta de concessões próprias permanece imutável e distinta da herança.
- **RF-01–RF-04 — domínio integrado**: abranger os três estados válidos, qualquer subconjunto dos três papéis, inclusive vazio, e as duas operações. Esta é uma ampliação futura da garantia parcial da Spec 001; resultados incidentais fora do domínio anterior não são comportamento a preservar.

### Casos existentes e integração

Expectativas de engenharia de [requisitos.md](../../documentacao/requisitos.md) e do [catálogo](../../documentacao/qualidade-e-testes.md). Sua inclusão nesta Spec não valida o gabarito científico. Nenhum teste novo foi executado nesta etapa.

| ID | Estado | Papéis atribuídos | Operação | Decisão | Motivo | Papel na integração |
|---|---|---|---|---|---|---|
| T01 | suspensa | Consulta | visualizar | negar | estado | Regressão RF-01 |
| T02 | ativa | Consulta | visualizar | permitir | permissao_direta | Regressão RF-02 |
| T03 | ativa | Consulta | exportar | negar | sem_permissao | Regressão RF-02 |
| T04 | ativa | Auditoria | exportar | permitir | permissao_direta | Regressão RF-02 |
| T05 | ativa | Supervisão | visualizar | permitir | permissao_herdada | RF-03, ainda não implementado |
| T06 | ativa | Consulta + Auditoria | visualizar | negar | conflito | RF-04, ainda não implementado |
| T07 | ativa | Supervisão + Auditoria | visualizar | negar | conflito | RF-03/RF-04, ainda não implementado |
| T08 | ativa | Supervisão | exportar | negar | sem_permissao | Ausência após herança, ainda não implementado |
| T09 | em_revisao | Consulta | visualizar | negar | estado | Regressão RF-01 |
| T10 | em_revisao | Supervisão | visualizar | negar | estado | Estado sobre herança |
| T11 | em_revisao | Consulta + Auditoria | visualizar | negar | estado | Estado sobre conflito |

T05–T08 são casos existentes, não novos IDs: falta torná-los executáveis na implementação futura. Integrar os onze casos sem alterar as expectativas dos sete anteriores e conservar os controles auxiliares. T10/T11 no incremento 1 provaram bloqueio por estado, sem demonstrar RF-03/RF-04 implementados.

### Key Entities

- **Solicitação**: estado da conta, papéis atribuídos e operação, no vocabulário válido existente.
- **Papéis efetivos**: atribuídos acrescidos de Consulta quando houver Supervisão; determinam incompatibilidade.
- **Concessões por origem**: próprias dos papéis atribuídos ou obtidas pela herança; origem necessária para distinguir motivos.
- **Resultado observável**: par decisão/motivo usado como unidade de verificação.

## Success Criteria *(mandatory)*

### Measurable Outcomes

IDs SC locais a esta Spec. São metas futuras, não resultados observados.

- **SC-001**: T05 e T08 coincidem integralmente com seus pares decisão/motivo (2/2), distinguindo herança e ausência de permissão.
- **SC-002**: T06 e T07 coincidem com `negar/conflito` (2/2), demonstrando conflito direto e herdado.
- **SC-003**: sete casos T01/T02/T03/T04/T09/T10/T11 preservados (7/7); conjunto integrado T01–T11 conforme a tabela (11/11), sem casos ignorados.
- **SC-004**: 32 combinações não ativas preservam `negar/estado`; três concessões próprias e controle Auditoria/visualizar mantêm expectativas anteriores. Essas contagens auxiliares não ampliam a suíte experimental.
- **SC-005**: os onze casos retornam os dois campos exatos, distinguindo estado, conflito, ausência, concessão direta e herdada sem interpretar texto livre.
- **SC-006**: controles de conta ativa sem papéis e Supervisão + Consulta, nas duas operações, satisfazem Edge Cases, preservam entradas e resultados repetidos; coexistência direta/herdada conserva `permissao_direta`. Sem novos IDs T.

## Assumptions

- Histórico: o pedido inicial em 16/10/2026 autorizou somente Spec/checklist, sem plano, tarefas, implementação ou pesquisa. Pedidos posteriores autorizaram planejamento, tarefas e análise; a reconciliação atual registra esse avanço documental, sem autorizar ou declarar implementação/testes da Spec 002.
- Governança: [AGENTS](../../AGENTS.md), [constituição](../../.specify/memory/constitution.md), [roadmap](../../documentacao/roadmap.md) e [decisões D-09–D-11/P-04](../../documentacao/decisoes.md). Ordem global e prioridade entre origens preservam o contrato completo; nenhuma nova decisão funcional foi introduzida.
- Fechamento do incremento 1 conferido contra [tasks](../001-autorizacao-direta/tasks.md), [evidências](../001-autorizacao-direta/evidencias.md), [contrato parcial](../001-autorizacao-direta/contracts/autorizacao.md), código e testes existentes: 17 tarefas com evidências correspondentes, sete casos e controles conformes, 10 métodos aprovados no registro com Python 3.13.3. Nenhum teste repetido nesta revisão: sem alteração de código/testes ou dúvida funcional concreta.
- Limitações anteriores registradas: saída inicial de erros truncada e resumida explicitamente; relatórios posteriores preservados. A revisão inicial distinguiu trechos históricos de 14/10 dos registros vigentes de 16/10; estado e handoff foram posteriormente reconciliados com o planejamento e, agora, com tarefas/análise. Não há lacuna funcional bloqueante identificada; não confundir fechamento de engenharia com aprovação científica.
- Código continua parcial até implementação autorizada. A existência desta Spec não amplia sua garantia real.
- Fora do escopo: variantes MC, mudanças de política, coleta/avaliação, piloto, LLM experimental, interface, banco, autenticação real, implantação ou framework geral.

### Proposta adicional separada — T12 (P-04)

T12 não integra a tabela nem os critérios de sucesso: conta ativa, Supervisão + Auditoria, exportar. Expectativa proposta: baseline `negar/conflito`; MC-04 sem herança `permitir/permissao_direta`. Retirar a herança elimina Consulta efetivo e o conflito; a concessão direta de Auditoria pode liberar exportar. T07 permanece correto para visualizar: baseline `negar/conflito`; sem herança, expectativa candidata `negar/sem_permissao`.

T12 não adotado, aprovado cientificamente ou executado. Antes de eventual adoção, revisar relevância e expectativas nas quatro mudanças, justificar inclusões/exclusões e atualizar catálogo, conjuntos de referência, notas/prompts, tamanho da suíte e todos os cálculos/denominadores. Seriam 12 casos e 48 pares teste × mudança em vez de 11/44, sem alterar automaticamente o número de chamadas. Nenhum gabarito, JSON ou catálogo original alterado nesta entrega.

### Decisões ainda pendentes

Adoção formal da constituição; demais pontos de P-01 além do recorte aceito; revisão de gabarito, notas, prompts e métricas (P-02); condições, piloto, repetições e congelamento (P-03); adoção de T12 (P-04); modelo/API, orçamento e isolamento. O aceite do recorte pelo orientador, relatado pelo usuário, não aprova esses detalhes. Planejamento e tarefas já preparados por solicitações posteriores; implementação ainda depende de solicitação, com todas as 22 tarefas pendentes.
