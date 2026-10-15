# Feature Specification: Autorização direta com bloqueio por estado

**Feature Branch**: não criada; nenhum hook de branch configurado.

**Feature Directory**: `specs/001-autorizacao-direta`

**Created**: 2026-10-14

**Status**: Draft — especificação documental revisada; capacidade não implementada.

**Input**: Solicitação do usuário nesta conversa: primeira Spec abrangendo RF-01/RF-02, com estado, papéis e operação como entradas e decisão/motivo como saída. Autorização limitada à especificação, sem planejamento técnico ou implementação.

## Objetivo e limites do incremento

Permitir ao pesquisador verificar o bloqueio de contas não ativas e as concessões diretas da política fictícia, construindo a primeira capacidade da bancada de autorização. O contrato fornecido pelo usuário é a base deste incremento de engenharia; isso não registra aprovação do orientador, validação do gabarito ou do protocolo experimental.

Inclui RF-01, RF-02 e a saída observável decisão/motivo. RF-03 (herança) e RF-04 (incompatibilidade) pertencem ao próximo incremento. O contrato completo de [requisitos](../../documentacao/requisitos.md) permanece preservado: Supervisão herdará visualizar de Consulta; Consulta e Auditoria serão incompatíveis, inclusive por herança. A precedência global continua estado → conflito → ausência de permissão.

Permissões diretas serão verificadas com contas ativas e cenários sem dependência de herança ou incompatibilidade. Cenários ativos cuja decisão exija RF-03/RF-04 não recebem resultado provisório nesta Spec, nem critério de negação por ausência temporária dessas capacidades. Em particular, não se define que Supervisão nunca pode visualizar.

Fora do incremento: herança, incompatibilidade, mudanças experimentais, coleta/avaliação, interface, cadastro, autenticação real, banco, implantação e entradas malformadas. Nenhuma tecnologia é selecionada aqui.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Bloquear conta não ativa (Priority: P1)

Como pesquisador, quero que a conta suspensa ou em revisão seja negada por estado, para verificar que permissões não contornam esse bloqueio.

**Why this priority**: RF-01 é a condição de entrada de toda autorização.

**Independent Test**: Informar contas não ativas e verificar decisão e motivo, sem precisar implementar herança ou incompatibilidade.

**Acceptance Scenarios**:

1. **Given** conta suspensa com Consulta, **When** solicita visualizar, **Then** retorna `negar/estado` (T01), apesar da concessão direta.
2. **Given** conta em revisão com Consulta, **When** solicita visualizar, **Then** retorna `negar/estado` (T09).
3. **Given** conta em revisão com Supervisão, **When** solicita visualizar, **Then** retorna `negar/estado` (T10), sem depender de expansão de herança.
4. **Given** conta em revisão com Consulta + Auditoria, **When** solicita visualizar, **Then** retorna `negar/estado` (T11), sem depender da avaliação de incompatibilidade.

### User Story 2 - Consultar permissões diretas (Priority: P2)

Como pesquisador, quero conferir concessões e ausências de permissão direta em contas ativas, para verificar RF-02 isoladamente das capacidades futuras.

**Why this priority**: Estabelece o comportamento de permissão após o bloqueio por estado.

**Independent Test**: Usar Consulta ou Auditoria isoladamente, com conta ativa; não requer RF-03/RF-04.

**Acceptance Scenarios**:

1. **Given** conta ativa com Consulta, **When** solicita visualizar, **Then** retorna `permitir/permissao_direta` (T02).
2. **Given** conta ativa com Consulta, **When** solicita exportar, **Then** retorna `negar/sem_permissao` (T03).
3. **Given** conta ativa com Auditoria, **When** solicita exportar, **Then** retorna `permitir/permissao_direta` (T04).

### Edge Cases

- O bloqueio por estado vale para qualquer conjunto válido de papéis e ambas as operações, independentemente de concessão direta ou capacidade futura.
- Conta ativa não implica permissão: T03 exige negativa por ausência de concessão.
- Supervisão tem conjunto de permissões próprias vazio. Isso é propriedade das concessões diretas, não negativa definitiva de acesso; não usar T05 como teste de negação neste incremento.
- Entradas fora do vocabulário, dados malformados e política de erro para esses casos estão fora do recorte.
- Cenários ativos com dependência de herança/conflito ficam fora da aceitação parcial; não se define resposta alternativa, exceção ou novo motivo para eles nesta etapa.

## Requirements *(mandatory)*

### Functional Requirements

Os IDs RF existentes são preservados; os itens abaixo detalham sua aceitação sem criar novos RFs.

- **RF-01 — entradas e estado**: Receber estado (`ativa`, `suspensa`, `em_revisao`), conjunto de papéis atribuídos e operação (`visualizar`, `exportar`). Somente `ativa` prossegue para consulta de permissões.
- **RF-01 — precedência**: `suspensa` e `em_revisao` devem produzir `negar/estado` antes de qualquer decisão de permissão, para qualquer entrada válida. T01/T09 demonstram o bloqueio apesar de permissão direta; T10/T11 preservam o estado sobre capacidades futuras.
- **RF-02 — concessões próprias**: Consulta possui diretamente apenas visualizar; Auditoria, apenas exportar; Supervisão não possui permissão própria. Verificar essa relação sem confundir permissão própria com acesso herdado futuro.
- **RF-02 — decisão no recorte**: Em conta ativa sem dependência de RF-03/RF-04, operação concedida diretamente deve produzir `permitir/permissao_direta`; ausência de concessão deve produzir `negar/sem_permissao`.
- **RF-01/RF-02 — saída**: Cada avaliação abrangida retorna decisão e motivo. O vocabulário completo permanece `permitir`/`negar` e `estado`, `conflito`, `sem_permissao`, `permissao_direta`, `permissao_herdada`. Neste recorte, os motivos observáveis são `estado`, `sem_permissao` e `permissao_direta`; os demais ficam reservados às capacidades futuras.

### Casos de teste correspondentes

Todos os casos são planejados, não implementados ou executados. IDs e expectativas são reaproveitados de [qualidade-e-testes.md](../../documentacao/qualidade-e-testes.md).

| ID | Estado | Papéis | Operação | Decisão esperada | Motivo esperado | Papel na aceitação |
|---|---|---|---|---|---|---|
| T01 | suspensa | Consulta | visualizar | negar | estado | Núcleo RF-01 |
| T02 | ativa | Consulta | visualizar | permitir | permissao_direta | Núcleo RF-02 |
| T03 | ativa | Consulta | exportar | negar | sem_permissao | Núcleo RF-02 |
| T04 | ativa | Auditoria | exportar | permitir | permissao_direta | Núcleo RF-02 |
| T09 | em_revisao | Consulta | visualizar | negar | estado | Núcleo RF-01 |
| T10 | em_revisao | Supervisão | visualizar | negar | estado | Complemento de precedência RF-01 |
| T11 | em_revisao | Consulta + Auditoria | visualizar | negar | estado | Complemento de precedência RF-01 |

T05–T08 permanecem planejados para a baseline completa do próximo incremento; suas entradas e saídas originais não são alteradas. T10/T11 aqui não demonstram herança ou incompatibilidade implementadas. O catálogo existente não esgota todas as combinações do contrato nem prova cobertura total.

### Key Entities *(include if feature involves data)*

- **Solicitação de autorização**: estado da conta, conjunto de papéis atribuídos e operação solicitada; dados fictícios do vocabulário fechado.
- **Política de permissões diretas**: relação entre papéis e operações concedidas, distinta das relações futuras de herança/incompatibilidade.
- **Resultado observável**: par decisão e motivo; ambos necessários para avaliar a conformidade.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Os cinco casos centrais T01–T04 e T09 devem coincidir integralmente com os pares decisão/motivo esperados (5/5).
- **SC-002**: Os dois casos complementares de bloqueio T10/T11 devem coincidir com `negar/estado` (2/2), sem exigir RF-03/RF-04.
- **SC-003**: As três concessões próprias descritas em RF-02 devem ser verificáveis sem ambiguidade: Consulta = visualizar; Auditoria = exportar; Supervisão = nenhuma permissão própria (3/3 relações).
- **SC-004**: O pesquisador deve conseguir distinguir, em todos os sete casos de aceitação, bloqueio por estado, ausência de permissão ou concessão direta por meio do motivo, sem interpretação de texto livre.

Esses critérios são metas de verificação futura, não resultados alcançados. Nenhuma taxa experimental ou meta de desempenho temporal é introduzida.

## Assumptions

- A solicitação atual autoriza especificar usando o contrato apresentado; não autoriza planejar tecnicamente, implementar, executar testes ou iniciar pesquisa.
- Usar `em_revisao` como identificação do estado descrito em linguagem natural como “em revisão”, conforme o vocabulário existente. Papéis são conjuntos e entradas são válidas.
- Não se exige interface humana: o pesquisador é o usuário da bancada, sem definição do mecanismo de interação nesta etapa.
- Dependências documentais: [governança](../../AGENTS.md), [constituição](../../.specify/memory/constitution.md), [escopo](../../documentacao/contexto-e-escopo.md), [decisões](../../documentacao/decisoes.md), [arquitetura proposta](../../documentacao/arquitetura.md) e [roadmap](../../documentacao/roadmap.md). Origem das expectativas: [referência candidata](../../materiais/02_REQUISITOS_TESTES_E_REFERENCIA.md).
- Não há dependência de modelo/API, escolha de MC-04, métricas ou número de repetições para especificar esta capacidade.

### Dúvidas e pendências remanescentes

Não há dúvida funcional bloqueante para esta Spec com o contrato fornecido. Linguagem, ferramenta de testes e modo de interação ficam para o planejamento técnico, sem escolha antecipada. O comportamento de cenários ativos dependentes de RF-03/RF-04 deve ser tratado ao especificar a próxima capacidade, preservando o contrato completo; esta Spec não promete suporte a eles.

Adoção formal da constituição, alinhamentos P-01/P-02/P-03 e revisão humana da referência continuam pendentes nos registros existentes. Esta especificação não resolve essas pendências nem libera piloto/coleta.
