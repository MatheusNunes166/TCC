# 2. Baseline e referência candidata

**Situação:** proposta para revisão; não é gabarito aprovado. Expectativas derivadas dos requisitos. A versão inicial T01–T12 foi conferida em execução local; as 48 expectativas das variantes não foram executadas. Isso não valida cientificamente a referência. Atualização 0.2 autorizada pelo pesquisador em D-15, em 19/10/2026; histórico 0.1 preservado em `../documentacao/historico/pre-t12-2026-10-19/`.

## 2.1 Contrato da bancada

Entrada: estado da conta (`ativa`, `suspensa`, `em_revisao`), conjunto de papéis e operação (`visualizar`, `exportar`). Dados fictícios e pertencentes ao vocabulário fechado. Não estudar entradas malformadas nesta coleta.

Saída observável: decisão `permitir`/`negar` e motivo estável: `estado`, `conflito`, `sem_permissao`, `permissao_direta` ou `permissao_herdada`. Se a mesma permissão vier de ambas as origens, registrar `permissao_direta`. Negações obedecem à precedência estado → conflito → ausência de permissão. Esses motivos detalham o contrato previsto na pauta; confirmar a redação na revisão.

| ID | Regra candidata | Critério de aceitação |
|---|---|---|
| RF-01 | Somente conta ativa prossegue. | Suspensa e em revisão negadas por estado, antes das demais regras. |
| RF-02 | Obter permissões diretas dos papéis atribuídos. | Consulta permite visualizar; Auditoria permite exportar; Supervisão não tem permissão própria. |
| RF-03 | Expandir papéis e permissões por uma relação de herança, com um nível. | Supervisão inclui Consulta como papel efetivo e pode herdar visualizar. |
| RF-04 | Verificar incompatibilidade entre papéis efetivos. | Consulta + Auditoria nega por conflito, inclusive quando Consulta é herdado. |

Depois de RF-01, obter permissões diretas e expandir herança; verificar conflito; somente então decidir pela presença da permissão. Não negar em RF-02 antes de consultar RF-03. Não há hierarquia de vários níveis, ciclos ou conflitos adicionais.

## 2.2 Doze testes existentes quando começar a comparação

P = permitir; N = negar. Os nomes curtos de motivo abaixo correspondem ao contrato acima.

| Teste | Estado | Papéis | Operação | Baseline |
|---|---|---|---|---|
| T01 | Suspensa | Consulta | visualizar | N/estado |
| T02 | Ativa | Consulta | visualizar | P/direta |
| T03 | Ativa | Consulta | exportar | N/sem permissão |
| T04 | Ativa | Auditoria | exportar | P/direta |
| T05 | Ativa | Supervisão | visualizar | P/herdada |
| T06 | Ativa | Consulta + Auditoria | visualizar | N/conflito |
| T07 | Ativa | Supervisão + Auditoria | visualizar | N/conflito |
| T08 | Ativa | Supervisão | exportar | N/sem permissão |
| T09 | Em revisão | Consulta | visualizar | N/estado |
| T10 | Em revisão | Supervisão | visualizar | N/estado |
| T11 | Em revisão | Consulta + Auditoria | visualizar | N/estado |
| T12 | Ativa | Supervisão + Auditoria | exportar | N/conflito |

## 2.3 Política de seleção — a mesma para todas as condições

Selecionar **todos os casos existentes cuja entrada se enquadre no item de política alterado**, direta ou indiretamente, mesmo se uma restrição de precedência maior mantiver o resultado. A aplicabilidade é estrutural, usando os papéis efetivos da baseline; não exige que a execução alcance a regra. Não procurar um subconjunto mínimo.

A regra é operacionalizada por tipo de alteração:

1. **Permissão:** a operação do teste é a alterada e seu conjunto de papéis efetivos da baseline contém o papel cuja concessão mudou.
2. **Incompatibilidade:** os papéis efetivos da baseline contêm o par cuja restrição mudou, independentemente do estado da conta.
3. **Herança:** o teste contém o papel filho da relação alterada, independentemente da operação ou estado.

Esta política e essas três regras entram no contexto de TODAS as condições, sem exemplos resolvidos e sem IDs corretos. O gabarito apenas aplica a política. Assim, o modelo conhece o critério de relevância, mas precisa identificar os casos e os impactos.

A política é conservadora e específica da bancada. Ela incorpora testes de preservação sem escolher controles arbitrários depois de observar respostas. Não é uma seleção mínima, uma garantia de detectar todos os defeitos ou uma definição universal de regressão. Antes do piloto, verificar se o orientador considera esse alvo compatível com o objetivo do TCC.

## 2.4 Mudanças independentes e conjuntos candidatos

**Revisão proposta:** MC-04-v2 substitui a antiga liberação de contas em revisão. Agora muda a relação de herança, permitindo observar sua consequência na incompatibilidade. Manter ambas na coleta ampliaria o escopo; escolher uma antes do piloto. Aqui, todas as tabelas usam exclusivamente MC-04-v2.

| Mudança | Alteração única | Tipo | RFs candidatos | Testes pela política |
|---|---|---|---|---|
| MC-01 | Retirar Auditoria → exportar. | Direto | RF-02 | T04, T12 |
| MC-02 | Retirar a incompatibilidade Consulta + Auditoria. | Direto | RF-04 | T06, T07, T11, T12 |
| MC-03 | Retirar Consulta → visualizar. | Propagado | RF-02, RF-03 | T01, T02, T05, T06, T07, T09, T10, T11 |
| MC-04-v2 | Retirar Supervisão → Consulta da herança. | Propagado | RF-03, RF-04 | T05, T07, T08, T10, T12 |

### Por que esses requisitos entram

- **MC-01:** muda o conjunto direto produzido por RF-02 para Auditoria. Nenhum papel herda Auditoria; herança e conflito mantêm seus valores. G_RF = {RF-02}.
- **MC-02:** muda RF-04. A expansão de herança em RF-03 é a mesma antes e depois; T07 usa herança, mas isso não torna RF-03 impactado. G_RF = {RF-04}.
- **MC-03:** RF-02 perde a concessão de Consulta; RF-03 passa a produzir um conjunto de permissões herdadas sem visualizar para Supervisão. A herança ainda existe e o par incompatível continua igual. G_RF = {RF-02, RF-03}.
- **MC-04-v2:** RF-03 deixa de incluir Consulta nos papéis efetivos de Supervisão. Em Supervisão + Auditoria, o predicado de incompatibilidade de RF-04 muda de verdadeiro para falso. A permissão direta de Auditoria não muda. G_RF = {RF-03, RF-04}.

RF-01 não entra nos conjuntos de impacto porque nenhuma mudança altera a regra de estado. Seus testes podem entrar na seleção para verificar preservação. **Requisitos impactados e testes de regressão não são o mesmo conjunto de relações.**

### Por que os testes entram

| Mudança | Resultado/motivo muda | Resultado preservado, mas relevante | Excluídos pela política |
|---|---|---|---|
| MC-01 | T04 | T12 | T01, T02, T03, T05, T06, T07, T08, T09, T10, T11 |
| MC-02 | T06, T07, T12 | T11 | T01, T02, T03, T04, T05, T08, T09, T10 |
| MC-03 | T02, T05 | T01, T06, T07, T09, T10, T11 | T03, T04, T08, T12 |
| MC-04-v2 | T05, T07, T12 | T08, T10 | T01, T02, T03, T04, T06, T09, T11 |

- MC-01: T04 e T12 combinam Auditoria efetivo e exportar. T04 perde a concessão e nega por sem_permissao; T12 mantém negar/conflito pela precedência de RF-04.
- MC-02: T06/T07/T12 verificam a retirada do conflito, T12 liberando exportar direto por Auditoria; T11 verifica que conta em revisão continua bloqueada apesar dessa retirada.
- MC-03: T02/T05 perdem acesso. T01/T09/T10/T11 continuam negados por estado; T06/T07, por conflito. Todos combinam Consulta efetivo e visualizar. T03/T08/T12 usam exportar; T04 não tem Consulta efetivo. T12 mantém negar/conflito e fica excluído pela operação.
- MC-04-v2: T05 perde o acesso herdado; T07 continua negado, agora por ausência de permissão, não por conflito. T08 mantém a ausência de permissão de exportar; T10 continua negado por estado. T12 passa de negar/conflito a permitir/permissao_direta, pois RF-02 mantém exportar de Auditoria e o conflito herdado desaparece. Os cinco têm Supervisão.

### Matriz de resultados esperados das quatro variantes

Cada célula compara a MESMA entrada com uma única mudança aplicada à baseline. O LLM avaliado não recebe esta matriz.

| Teste | Baseline | MC-01 | MC-02 | MC-03 | MC-04-v2 |
|---|---|---|---|---|---|
| T01 | N/estado | N/estado | N/estado | N/estado | N/estado |
| T02 | P/direta | P/direta | P/direta | N/sem permissão | P/direta |
| T03 | N/sem permissão | N/sem permissão | N/sem permissão | N/sem permissão | N/sem permissão |
| T04 | P/direta | N/sem permissão | P/direta | P/direta | P/direta |
| T05 | P/herdada | P/herdada | P/herdada | N/sem permissão | N/sem permissão |
| T06 | N/conflito | N/conflito | P/direta | N/conflito | N/conflito |
| T07 | N/conflito | N/conflito | P/herdada | N/conflito | N/sem permissão |
| T08 | N/sem permissão | N/sem permissão | N/sem permissão | N/sem permissão | N/sem permissão |
| T09 | N/estado | N/estado | N/estado | N/estado | N/estado |
| T10 | N/estado | N/estado | N/estado | N/estado | N/estado |
| T11 | N/estado | N/estado | N/estado | N/estado | N/estado |
| T12 | N/conflito | N/conflito | P/direta | N/conflito | P/direta |

T07 evidencia por que verificar só “permitir/negar” é insuficiente para MC-04-v2: a decisão continua negar, mas o motivo muda. Trata-se de uma expectativa contratual, não de uma falha introduzida.

## 2.5 Revisão e limitações da referência

Revisor e data: **a combinar**. Conferir: precedência; valores intermediários que justificam cada RF; os doze casos nas quatro variantes; inclusões/exclusões pela política; notas sem respostas; ausência de dependência de um resultado do LLM. Registrar cada divergência e resolvê-la antes do piloto.

A suíte pequena não pretende cobrir todo RBAC. O número de testes relevantes difere (2, 4, 8 e 5), e a seleção de MC-03 pode ser mais óbvia ou extensa. Essas diferenças limitam comparações entre tipos de mudança; não invalidam a comparação entre condições aplicada à mesma mudança. Se houver efeito de teto, relatar e discutir com o orientador antes de ampliar a bancada.

Se a definição de impacto exigir modificação textual em vez de alteração funcional, a referência de RF-03/04 precisa ser revista; não alterar o conceito durante a coleta.

Total: 12 testes na versão inicial + 48 pares teste × mudança = 60 expectativas. MC-04 nesta etapa é a retirada de herança identificada como MC-04-v2. O bloco comum exportável de impacto/relevância está em [07_DEFINICOES_COMUNS.md](07_DEFINICOES_COMUNS.md); não exportar este material com o gabarito.
