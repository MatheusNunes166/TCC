# Tasks: Autorização direta com bloqueio por estado

**Input**: [Spec](spec.md), [plano](plan.md), [research](research.md), [modelo de dados](data-model.md), [contrato](contracts/autorizacao.md) e [guia de verificação](quickstart.md).
**Prerequisites**: D-06/D-07/D-08 em [decisoes.md](../../documentacao/decisoes.md); implementação ainda não autorizada nesta entrega.
**Tests**: exigidos pela Spec. Todas as tarefas abaixo estão inicialmente pendentes, inclusive preparação, execução e documentação. Gerar esta lista não executa nenhuma tarefa nem fecha incremento.
**Organization**: US1 = bloqueio por estado (P1); US2 = permissões diretas (P2).

## Format: `[ID] [P?] [Story] Description`

IDs T001–T017 identificam tarefas; T01–T11 continuam sendo IDs dos casos de teste da bancada. Não os confundir. `[P]` só seria usado em tarefas sem dependência e em arquivos distintos; nenhuma foi marcada nesta organização mínima.

## Path Conventions

Caminhos relativos à raiz com `documentacao/`, `materiais/` e `.specify/`. Únicos arquivos Python futuros: `autorizacao.py` e `tests/test_autorizacao.py`. Não criar outra raiz de projeto, dependências externas, empacotamento, interface ou banco.

## Phase 1: Setup (Shared Infrastructure)

**Propósito**: verificar ambiente e preparar evidência, somente quando autorizado implementar.

- [ ] T001 Conferir Python compatível com a proposta 3.11+ e registrar versão real, comando e data em `specs/001-autorizacao-direta/quickstart.md`; não instalar pytest ou declarar ambiente pronto sem conferência.

## Phase 2: Foundational (Blocking Prerequisites)

**Propósito**: fixar o domínio de uso antes das duas histórias, sem implementar capacidades futuras.

- [ ] T002 Criar `autorizacao.py` inicialmente apenas com documentação do domínio parcial e criar a pasta `tests/` para `tests/test_autorizacao.py`; documentar entradas válidas (`ativa`, `suspensa`, `em_revisao`; papéis Consulta/Auditoria/Supervisão como `frozenset[str]`; visualizar/exportar), saída com exatamente `decisao` e `motivo` strings, contas não ativas com qualquer subconjunto e contas ativas somente com Consulta ou Auditoria isoladamente. Não definir retorno, exceção, guarda ou novo motivo para ativos fora do recorte; preservar vocabulário e precedência completos.

**Checkpoint**: estrutura mínima e domínio documentados; nenhuma funcionalidade presumida.

## Phase 3: User Story 1 — Bloquear conta não ativa (Priority: P1)

**Goal**: RF-01 nega por estado antes das demais decisões.
**Independent Test**: T01/T09/T10/T11 e verificação auxiliar não ativa, sem depender de concessões, herança ou conflito.

### Tests for User Story 1

- [ ] T003 [US1] Escrever em `tests/test_autorizacao.py` testes unittest identificados T01 (suspensa, Consulta, visualizar), T09 (em_revisao, Consulta, visualizar), T10 (em_revisao, Supervisão, visualizar) e T11 (em_revisao, Consulta+Auditoria, visualizar); comparar dicionários completos com `decisao=negar` e `motivo=estado`, sem campos extras. Cobrir SC-001 (parte), SC-002 e SC-004 (parte), sem testar RF-03/RF-04.
- [ ] T004 [US1] Acrescentar em `tests/test_autorizacao.py` verificação auxiliar tabelada dos dois estados bloqueados × oito subconjuntos dos três papéis × duas operações (32 entradas), esperando sempre `negar/estado` e argumentos preservados; manter esses exemplos separados dos IDs T do catálogo experimental. Cobrir universalidade RF-01 e precedência.
- [ ] T005 [US1] Executar os testes US1 antes da implementação conforme `specs/001-autorizacao-direta/quickstart.md` e registrar resultado real nesse arquivo; confirmar que identificam ausência da capacidade, distinguindo ausência de `autorizar` de erro de ambiente/sintaxe. Não relatar erro de preparação ou zero testes como falha funcional demonstrada nem como sucesso.

### Implementation for User Story 1

- [ ] T006 [US1] Implementar em `autorizacao.py` o bloqueio de `autorizar(estado, papeis, operacao)` para `suspensa` e `em_revisao`, retornando exatamente `{'decisao': 'negar', 'motivo': 'estado'}` antes de consultar permissões. Manter entradas intactas e documentar que a parte ativa ainda depende de US2; não criar resultado de negócio provisório para cenários ativos futuros.
- [ ] T007 [US1] Executar novamente apenas a verificação US1 e registrar comandos, IDs, contagens reais e resultados em `specs/001-autorizacao-direta/quickstart.md`; investigar falhas antes de avançar e verificar por revisão de `autorizacao.py` que o bloqueio precede consulta de permissões. Não declarar o incremento completo com US2 ausente.

**Checkpoint**: US1 pode ser demonstrada isoladamente com contas não ativas. Isso não prova permissões diretas, herança ou incompatibilidade.

## Phase 4: User Story 2 — Consultar permissões diretas (Priority: P2)

**Goal**: RF-02 observa concessões próprias e decide no domínio ativo direto, preservando RF-01.
**Independent Test**: T02/T03/T04 e as três relações de concessões, sem cenários dependentes de RF-03/RF-04. A sequência usa US1 para preservar o bloqueio na mesma função.

### Tests for User Story 2

- [ ] T008 [US2] Escrever em `tests/test_autorizacao.py` os testes T02 (ativa, Consulta, visualizar → permitir/permissao_direta), T03 (ativa, Consulta, exportar → negar/sem_permissao) e T04 (ativa, Auditoria, exportar → permitir/permissao_direta), comparando o dicionário inteiro; acrescentar como controle auxiliar Auditoria isolada solicitando visualizar → negar/sem_permissao, sem inventar novo ID T. Cobrir RF-02, SC-001 e SC-004 restantes e ambas as operações do domínio direto.
- [ ] T009 [US2] Escrever em `tests/test_autorizacao.py` verificações de `obter_permissoes_diretas(papeis)` para Consulta → `frozenset({'visualizar'})`, Auditoria → `frozenset({'exportar'})` e Supervisão → `frozenset()`; esperados explícitos e independentes da política interna. Conferir retorno imutável, ausência de mutação das entradas e consistência em chamadas repetidas. Cobrir SC-003; não interpretar Supervisão sem concessão própria como negativa final de visualizar.
- [ ] T010 [US2] Executar os testes US2 antes da implementação correspondente e registrar resultados reais em `specs/001-autorizacao-direta/quickstart.md`; identificar capacidade ausente, separando falhas funcionais de importação/preparação, sem registrar expectativas como execução bem-sucedida.

### Implementation for User Story 2

- [ ] T011 [US2] Implementar em `autorizacao.py` a relação de concessões próprias e `obter_permissoes_diretas(papeis)`, retornando união imutável das operações diretas sem expor política mutável: Consulta somente visualizar, Auditoria somente exportar, Supervisão vazio. Não expandir herança ou verificar conflito.
- [ ] T012 [US2] Completar `autorizar` em `autorizacao.py` para contas ativas do domínio direto: usar concessões próprias e retornar exatamente `permitir/permissao_direta` ou `negar/sem_permissao` nas chaves `decisao`/`motivo`; manter RF-01 primeiro, função pura e vocabulário estável. Documentar a precondição parcial; não adicionar respostas, exceções, stubs de herança/conflito ou critérios de aceitação para ativos com Supervisão/combinações dependentes de RF-03/RF-04.
- [ ] T013 [US2] Executar a suíte integrada conforme `specs/001-autorizacao-direta/quickstart.md`, registrando resultados reais dos sete casos T01/T02/T03/T04/T09/T10/T11, três concessões, 32 combinações de estado e controles auxiliares; exigir descoberta não vazia, ausência de falhas e nenhum caso de aceitação ignorado. Conferir regressão US1 e SC-001–SC-004; não executar T05–T08 como se implementados ou iniciar piloto.

**Checkpoint**: sete cenários de aceitação e controles conformes, somente se evidências reais o demonstrarem. RF-03/RF-04 continuam fora da entrega.

## Phase 5: Polish & Cross-Cutting Concerns

- [ ] T014 Revisar as alterações em `autorizacao.py` e `tests/test_autorizacao.py` contra `specs/001-autorizacao-direta/spec.md`, `plan.md` e `contracts/autorizacao.md`; conferir chaves/motivos, precedência, ausência de efeitos externos, domínio parcial explícito e preservação de T05–T08. Resolver divergências no contrato/documentação antes de fechar, sem redefinir baseline completa.
- [ ] T015 Consolidar em `specs/001-autorizacao-direta/quickstart.md` evidência real de comandos, versão, data, revisão ou diff utilizado, contagens por categoria, falhas/resoluções e relatório bruto; distinguir cenários, métodos e subtestes. Somente repetir verificações se houver correções ou dúvida material; não inventar relatório, resultado ou cobertura total.
- [ ] T016 Atualizar `documentacao/arquitetura.md`, `documentacao/qualidade-e-testes.md` e `documentacao/decisoes.md` com realizado versus planejado e evidências de T013–T015; manter catálogo original, RF-03/RF-04 futuros e P-01/P-02/P-03 pendentes. Não validar gabarito ou protocolo como consequência de testes de engenharia.
- [ ] T017 Reconciliar `ESTADO_ATUAL.md`, `BLOQUEIOS.md`, `HANDOFF.md`, `documentacao/roadmap.md` e `specs/001-autorizacao-direta/tasks.md` após revisão/evidências: marcar apenas tarefas comprovadas, declarar limitações restantes e próxima capacidade RF-03/RF-04 sem abri-la automaticamente. Não declarar piloto/coleta realizados ou incremento concluído com lacunas.

## Dependencies & Execution Order

### Phase Dependencies

```text
T001 → T002 → T003 → T004 → T005 → T006 → T007
     → T008 → T009 → T010 → T011 → T012 → T013
     → T014 → T015 → T016 → T017
```

A continuação da segunda linha depende de T007. A ordem linear é deliberada: produção e testes compartilham dois arquivos. Setup e fundação precedem ambas as histórias; US1 precede US2 na execução para verificar que a introdução de concessões não altera o estado. US1 não precisa implementar US2 para ser verificada. US2 tem casos próprios, mas a integração preserva US1.

### Within Each User Story

Escrever testes → observar capacidade ausente e corrigir preparação se necessário → implementar → verificar. A ausência da função durante a primeira rodada deve ser registrada como interface ainda ausente; só comparações executadas contra resultado podem comprovar conformidade ou divergência funcional. Não presumir execução nem marcar tarefas no planejamento.

### Parallel Opportunities / Examples by Story

US1: T003/T004 alteram o mesmo arquivo; execução após escrita e implementação após diagnóstico — manter sequencial. US2: T008/T009 compartilham testes e T011/T012 compartilham o módulo — manter sequencial. Não há oportunidade segura de escrita paralela no recorte mínimo; nenhum marcador `[P]` e nenhuma delegação de implementação proposta.

## Implementation Strategy

MVP demonstrável: US1 (bloqueio por estado), explicitamente parcial. O incremento solicitado só se encerra após US2, suíte integrada, revisão e atualização documental. Não implantar ou publicar a bancada. Começar a executar tarefas apenas com nova solicitação de implementação; o pedido que gerou esta lista autoriza documentação e análise, sem código ou execução de testes da aplicação.

## Coverage Summary

| Requisito/critério | Tarefas principais | Casos/verificação |
|---|---|---|
| RF-01 — entradas/estado e precedência | T002–T007, T013–T015 | T01/T09/T10/T11 e 32 combinações auxiliares |
| RF-02 — concessões próprias | T009–T011, T013–T015 | Três papéis, retorno imutável e chamadas repetidas |
| RF-02 — decisão no recorte | T008, T010–T014 | T02/T03/T04 e controle Auditoria/visualizar |
| RF-01/RF-02 — saída | T003, T008, T012–T015 | Dicionários completos, decisão e motivo |
| SC-001 | T003, T008, T013 | T01/T02/T03/T04/T09 (5/5 esperado) |
| SC-002 | T003, T007, T013 | T10/T11 (2/2 esperado) |
| SC-003 | T009, T011, T013 | Três relações de concessão (3/3 esperado) |
| SC-004 | T003, T008, T013–T015 | Sete pares exatos |
| Domínio parcial e governança | T002, T006, T012, T014–T017 | Sem novas respostas RF-03/RF-04; evidências e documentação |

Contagem: 17 tarefas, todas pendentes; US1 = 5, US2 = 6, preparação/fundação = 2, fechamento = 4. Os percentuais e razões acima são metas, não resultados observados.
