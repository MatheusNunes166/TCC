> Estado vigente — 18/10/2026 (D-13/D-14): Spec 002 implementada com Python 3.13.3 + unittest. RF-01–RF-04 integrados; 17 métodos aprovados, T01–T11 11/11 em decisão/motivo e 55 subtestes auxiliares conformes, zero falhas/erros/ignorados. Três estados, oito subconjuntos e duas operações no domínio válido; verificação dirigida, sem matriz que inclua T12. Evidências em `specs/002-heranca-incompatibilidade/quickstart.md` (caminho desde a raiz). T12 somente proposta; catálogo 11/44 e gabarito preservados. Sem variantes, piloto ou LLM experimental. Adoção constitucional e pendências científicas permanecem abertas. Trechos datados anteriores abaixo são históricos e não descrevem a capacidade atual.

# Implementation Plan: Herança e incompatibilidade efetiva

**Branch**: nenhuma criada | **Date**: 2026-10-16 | **Spec**: [spec.md](spec.md)

**Input**: `specs/002-heranca-incompatibilidade/spec.md`. Histórico: planejamento autorizado pelo usuário em 16/10/2026, com código, tarefas e pesquisa experimental fora daquela etapa.

**Estado reconciliado — 16/10/2026**: especificação, planejamento e [tasks.md](tasks.md) preparados; análise de consistência realizada, sem contradição funcional ou requisito sem tarefa. As 22 tarefas de implementação T001–T022 estão pendentes; nenhum teste da Spec 002 executado. T12 fora da aceitação, revisões científicas pendentes. Esta atualização altera somente o estado documental, preservando o desenho e os critérios.

## Summary

Completar futuramente RF-03/RF-04 sobre o núcleo RF-01/RF-02 existente, sem mudar concessões próprias, interface ou expectativas T01–T11. Expansão explícita de um nível e incompatibilidade por papéis efetivos, com estado antes de conflito e decisão por permissão. Conservar origem direta/herdada para o motivo. Desenho local, sem dependências externas ou infraestrutura de variantes.

## Technical Context

**Language/Version**: Python 3.11+; Python 3.13.3 foi usado no incremento 1, conforme suas [evidências](../001-autorizacao-direta/evidencias.md). Ambiente não revalidado nesta etapa.
**Primary Dependencies**: biblioteca padrão, sem terceiros.
**Storage**: nenhum; entradas e resultados em memória.
**Testing**: unittest; preservar arquivo, classes e dez métodos atuais, acrescentar quatro métodos T05–T08 e controles auxiliares.
**Target Platform**: local Windows/PowerShell; sem implantação.
**Project Type**: módulo importável, sem CLI de aplicação, HTTP ou UI.
**Performance Goals**: nenhuma meta de carga/tempo; sem benchmark.
**Constraints**: entradas válidas, três papéis, duas operações, um nível, uma incompatibilidade; sem ciclos, validação de dados malformados, configuração geral ou chamadas externas.
**Scale/Scope**: onze casos existentes integrados; T12 proposto, não adotado nem executado. Controles não ampliam o catálogo experimental.

## Constitution Check

Registro histórico da revisão documental antes da pesquisa técnica e após o desenho; não prova implementação. A geração posterior de tarefas e sua análise não executam o trabalho descrito abaixo.

| Princípio | Antes da pesquisa | Após desenho |
|---|---|---|
| Escopo controlado | Spec 002 e checklist lidas; somente RF-03/RF-04. | Um módulo e arquivo de testes existentes, sem variantes. |
| Decisões explícitas | Python/unittest solicitados; contrato completo disponível. | Escolhas e alternativas em research; autorização D-12 no registro central. |
| Rastreabilidade | RF/T/SC preservados. | Matriz de verificação abaixo liga SC-001–SC-006 a comportamentos observáveis. |
| Verificação por evidências | Incremento 1 possui evidências reais. | Guia futuro separa metas de execução; nenhum teste executado agora. |
| Incrementos pequenos | Planejamento autorizado, tarefas/código excluídos. | Cinco artefatos de planejamento; próxima etapa depende de solicitação. |
| Separação de contextos | Sem pacote experimental preparado. | Sem LLM, piloto, coleta ou promoção do gabarito a validado. |

Nenhuma violação identificada. A constituição 1.0.0 continua sem adoção formal; revisão de engenharia não a ratifica.

## Project Structure

### Documentation (this feature)

```text
specs/002-heranca-incompatibilidade/
├── spec.md
├── checklists/requirements.md
├── plan.md
├── research.md
├── data-model.md
├── contracts/autorizacao.md
├── quickstart.md
└── tasks.md
```

Histórico: `tasks.md` não foi produzido pela etapa de planejamento; foi gerado posteriormente pelo fluxo de tarefas, com 22 itens ainda pendentes.

### Source Code (repository root)

```text
autorizacao.py
tests/test_autorizacao.py
```

**Structure Decision**: reutilizar organização existente; sem novos módulos, fixtures JSON, classes de política, empacotamento ou serviços.

## Desenho e ordem de decisão

Preservar `obter_permissoes_diretas(papeis)` com a semântica atual e retorno imutável. Acrescentar futuramente `obter_papeis_efetivos(papeis)` e `ha_incompatibilidade(papeis_efetivos)`, no mesmo módulo. Assinaturas e exemplos no [contrato](contracts/autorizacao.md).

Expansão: os efetivos são os atribuídos mais Consulta se Supervisão estiver presente. Não há recursão, travessia de grafo ou herança de Auditoria. Conflito: efetivos contêm simultaneamente Consulta e Auditoria, independentemente da operação.

Sequência futura de `autorizar`:

1. Retornar `negar/estado` imediatamente para suspensa/em_revisao, antes de consultar permissões ou expandir papéis.
2. Consultar permissões diretas dos **atribuídos**; calcular efetivos e permissões disponíveis consultando a relação direta sobre os efetivos.
3. Verificar incompatibilidade dos efetivos; retornar `negar/conflito` antes de decidir acesso.
4. Se a operação pertence às diretas dos atribuídos, retornar `permitir/permissao_direta`.
5. Se pertence às disponíveis pelos efetivos, retornar `permitir/permissao_herdada`.
6. Caso contrário, retornar `negar/sem_permissao`.

Consultar a relação direta com efetivos serve ao cálculo interno de disponibilidade; não redefine concessões próprias dos atribuídos. Não subtrair atribuídos dos efetivos para determinar origem: Supervisão + Consulta pode ter ambas as origens, e direta deve prevalecer.

## Evolução do domínio

Hoje, ativas são garantidas apenas para Consulta ou Auditoria isoladamente; não ativas já cobrem qualquer subconjunto. Após implementação e verificação futuras, `autorizar` garantirá os três estados × oito subconjuntos × duas operações (48 entradas válidas possíveis). Isso descreve domínio, não obrigação de executar matriz completa nem ampliação do catálogo de onze casos. A matriz completa incluiria T12; não a propor como execução nesta etapa.

Preservar resultados garantidos da Spec 001; resultados incidentais atuais para ativas vazias, Supervisão ou múltiplos papéis não são contrato de regressão. Atualizar futuramente docstrings para explicitar a ampliação somente quando implementada. Sem novas guardas, exceções ou motivos para entradas malformadas.

## Verificação planejada e rastreabilidade

| Critério | Verificação futura | Evidência exigida |
|---|---|---|
| SC-001 | T05 permitir/herdada; T08 negar/sem_permissao. | Dois dicionários completos conformes. |
| SC-002 | T06 conflito direto; T07 conflito herdado. | Dois dicionários negar/conflito. |
| SC-003 | Integrar T05–T08 aos sete anteriores. | Onze IDs presentes, 11/11, nenhum ignorado. |
| SC-004 | Manter 32 subtestes de estado, três concessões e Auditoria/visualizar. | Mesmos esperados explícitos, imutabilidade e repetição. |
| SC-005 | Comparar dicionários completos nos onze casos. | Exatamente decisao/motivo e vocabulário da Spec. |
| SC-006 | Ativa sem papéis e Supervisão + Consulta, duas operações. | Quatro combinações auxiliares, entradas preservadas e resultados repetidos. |
| RF-03/RF-04 | Verificar auxiliares com expectativas explícitas. | Efetivos nos oito subconjuntos; predicado de incompatibilidade nos oito subconjuntos, sem autorizar/exportar para T12. |

Manter os dez métodos existentes; acrescentar quatro métodos com IDs e controles auxiliares. Antes de controles novos, a base seria 14 métodos; contagem final será registrada na execução, distinguindo métodos, cenários e subtestes. Não derivar esperados da mesma tabela usada em produção.

T10/T11 devem permanecer negar/estado; isso demonstra precedência na integração, sem avaliar regras posteriores quando o estado bloqueia. A inspeção da ordem no código complementará os testes.

## Preparação e revisão desta etapa

Selecionado o apontador local `.specify/feature.json` para a Spec 002 e confirmado por `check-prerequisites.sh --json --paths-only` antes da geração. `setup-plan.sh --json` copiou o template para este destino, após permissão técnica por acesso negado no sandbox. O identificador BRANCH retornado é contexto, não branch Git criada. Template local sem overrides/presets; hooks ausentes em `.specify/extensions.yml` antes/depois.

Pesquisa de desenho baseada no contrato e código locais, com revisão auxiliar somente leitura conforme a skill speckit-plan. Sem nova consulta externa, dependência ou alteração tecnológica. Revisão documental dos cinco artefatos: domínio, precedência, origem, rastreabilidade e links; resultados não são testes de aplicação.

## Pendências e próxima etapa

Nenhuma dúvida funcional bloqueante encontrada. Direta prevalece sobre herdada conforme contrato já documentado; não é nova política. Adoção formal da constituição e P-01/P-02/P-03/P-04 permanecem no [registro central](../../documentacao/decisoes.md). T12 fora da aceitação: eventual adoção exige revisar relevância nas quatro mudanças e cálculos/tamanho. Sem gabarito validado.

Histórico: ao concluir este desenho, a próxima ação era solicitar geração de tarefas; naquela etapa não havia tarefa, código, variante ou piloto produzido. Posteriormente, foram preparadas 22 tarefas e realizada a análise de consistência; somente a reconciliação temporal ficou apontada como ajuste documental, tratado aqui.

Próxima ação atual: solicitar implementação quando desejado e executar a sequência de tasks.md com evidências reais. Nenhuma tarefa concluída, nenhum teste da Spec 002 executado e nenhum código, variante ou piloto produzido nesta etapa documental.

## Complexity Tracking

Sem exceção constitucional ou complexidade adicional necessária.
