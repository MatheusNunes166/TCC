# Implementation Plan: Autorização direta com bloqueio por estado

> Atualização vigente — 16/10/2026: RF-01/RF-02 implementados e verificados com Python 3.13.3 + unittest, sem terceiros. Sete casos de aceitação conformes, três concessões próprias, 32 combinações de estado e controle Auditoria/visualizar; 10 métodos, zero falhas/erros/ignorados. Evidências em `specs/001-autorizacao-direta/evidencias.md` (caminho desde a raiz). D-09/D-10 registram recorte aceito e autorização. Domínio ativo parcial somente Consulta ou Auditoria isoladamente; RF-03/RF-04 permanecem futuros. Afirmações de ausência de autorização/implementação nos registros de 14/10 abaixo são históricas, superadas somente nesse alcance. Constituição não formalmente adotada; referência, notas, prompts, métricas e piloto pendentes. Nenhum piloto ou LLM experimental executado.


**Branch**: Git atual `main`; o setup retornou identificador de feature `001-autorizacao-direta`, sem criar branch.
**Date**: 2026-10-14 | **Spec**: [spec.md](spec.md)
**Input**: `specs/001-autorizacao-direta/spec.md` e solicitação atual de planejamento.
**Status**: Python + unittest e organização mínima confirmados pelo usuário em 14/10/2026 (D-07); desenho detalhado para execução futura. Tarefas documentadas, sem implementação ou testes executados.

## Summary

Planejar RF-01/RF-02 como função local pura em Python e testes com `unittest`, sem dependências externas. Python + unittest e os dois arquivos mínimos foram confirmados explicitamente pelo usuário; os demais detalhes são desenho técnico, sem alegar aprovações adicionais. A base funcional foi fornecida pelo usuário ao solicitar a Spec; aprovações científicas e revisão da referência permanecem pendentes.

Artefatos produzidos pelo fluxo: este plano, [research.md](research.md), [data-model.md](data-model.md), [contracts/autorizacao.md](contracts/autorizacao.md) e [quickstart.md](quickstart.md). O fluxo de planejamento terminou no desenho; [tasks.md](tasks.md) foi gerado posteriormente por solicitação do usuário.

## Technical Context

**Language/Version**: Python confirmado; compatibilidade proposta 3.11 ou superior, usando apenas recursos disponíveis em 3.11; versão exata do interpretador a registrar na futura preparação do ambiente.
**Primary Dependencies**: biblioteca padrão; nenhuma dependência de terceiros proposta.
**Storage**: nenhuma persistência; solicitações e resultados somente em memória.
**Testing**: `unittest` confirmado, com IDs T existentes nos nomes dos testes; comparações de decisão e motivo.
**Target Platform**: execução local, inicialmente Windows/PowerShell; sem requisito de serviço ou implantação.
**Project Type**: módulo importável por testes, sem interface de usuário, CLI da aplicação ou API de rede.
**Performance Goals**: sem meta temporal ou de carga na Spec; não criar benchmark neste incremento.
**Constraints**: RF-01/RF-02 somente; entradas válidas do vocabulário fechado; sem I/O, autenticação real, banco, herança ou conflito.
**Scale/Scope**: um módulo de produção, um arquivo de testes e sete cenários de aceitação, além de verificações das concessões e da precedência. Não afirmar cobertura total de RBAC.

## Constitution Check

Gates conferidos antes da pesquisa e novamente após o desenho, por revisão documental, sem execução da aplicação.

| Princípio | Antes da pesquisa | Após desenho |
|---|---|---|
| Escopo controlado | RF-01/RF-02 delimitados pela Spec. | Um módulo e testes; capacidades futuras fora do domínio parcial. |
| Decisões explícitas | Contrato fornecido; tecnologia ainda pendente. | Confirmação de Python/unittest/layout em D-07; demais detalhes e alternativas em research. |
| Rastreabilidade | IDs RF/T/SC preservados. | Matriz abaixo e contrato remetem à Spec e baseline completa. |
| Verificação por evidências | Testes somente planejados. | Guia define execução futura e evidências; nenhum resultado declarado. |
| Incrementos pequenos | Uma capacidade. | Uma lista de tarefas pendentes gerada posteriormente, sem implementação ou pesquisa. |
| Separação de contextos | Nenhum pacote experimental montado. | Nenhum acesso a modelo, coleta, avaliação ou gabarito promovido a validado. |

Resultado: nenhuma violação de desenho identificada. A adoção formal da constituição continua pendente; isso não é aprovação do orientador.

## Project Structure

### Documentation (this feature)

```text
specs/001-autorizacao-direta/
├── spec.md
├── checklists/requirements.md
├── plan.md
├── research.md
├── data-model.md
├── contracts/autorizacao.md
└── quickstart.md
```

### Source Code (repository root)

Estrutura mínima confirmada, ainda não implementada:

```text
autorizacao.py              # concessões próprias e função parcial de autorização
tests/
└── test_autorizacao.py      # aceitação RF-01/RF-02 e verificações auxiliares
```

**Structure Decision**: um módulo na raiz evita empacotamento e configuração de importação desnecessários para esta bancada. Não criar camadas de serviço, modelos separados, fixtures JSON, configuração de dependências ou pastas de pesquisa agora. O domínio e a interface estão nos artefatos de desenho; arquivos de produção e testes só surgirão na implementação autorizada.

## Contrato e sequência proposta

Interface local proposta: `autorizar(estado, papeis, operacao)` retorna dicionário com exatamente `decisao` e `motivo`, ambos strings. Propor também `obter_permissoes_diretas(papeis)` para observar concessões próprias sem confundi-las com acesso final. Tipos, domínio de uso e exemplos estão no [contrato](contracts/autorizacao.md).

RF-01 encerra contas suspensas/em revisão com `negar/estado`. Para contas ativas no recorte direto, consultar somente concessões próprias, permitindo com `permissao_direta` ou negando com `sem_permissao`. Nenhum passo de herança ou conflito será implementado, nem stub que alegue resolvê-los.

O uso de `autorizar` em conta ativa fica restrito, neste incremento, aos papéis isolados Consulta ou Auditoria. Isso é precondição temporária de uso/aceitação, não nova política de negócio. Não definir resultado, exceção ou motivo para cenários ativos fora desse recorte; não instalar um mecanismo de rejeição para eles sem revisão da Spec. A documentação e os testes deixarão explícita essa limitação da bancada.

## Verificação planejada e rastreabilidade

| Critério da Spec | Verificação futura | Evidência esperada |
|---|---|---|
| SC-001 / RF-01/RF-02 | Testes identificados T01, T02, T03, T04 e T09; comparar dicionários completos. | Cinco pares decisão/motivo conformes, com IDs no relatório. |
| SC-002 / RF-01 | T10 e T11, contas em revisão, sem consultar capacidades futuras. | Dois resultados `negar/estado`; sem alegar herança/conflito testados. |
| SC-003 / RF-02 | Conferir `obter_permissoes_diretas` para cada papel isolado contra expectativas explícitas independentes da implementação. | Consulta = visualizar; Auditoria = exportar; Supervisão = conjunto vazio. |
| SC-004 / saída | Todos os sete casos com chaves e valores exatos, sem texto livre. | Motivos distinguíveis e decisão coerente em cada caso. |
| Universalidade RF-01 | Verificação auxiliar tabelada dos dois estados bloqueados × oito subconjuntos dos três papéis × duas operações. | Todas as 32 entradas retornam `negar/estado`; entradas não são alteradas. |

Os 32 exemplos auxiliares verificam o contrato de estado sem acrescentar IDs T à suíte experimental ou declarar ampliação de seu catálogo. Para SC-003, os testes não devem derivar os esperados da mesma tabela usada pela implementação. A consulta às concessões não deve permitir que o chamador modifique a política.

T05–T08 permanecem integralmente no catálogo original e fora desta aceitação; não criar testes ignorados que sugiram sua implementação nem substituir seus resultados esperados. RF-03 acrescentará herança antes da decisão por ausência de permissão; RF-04 acrescentará conflito antes da decisão por concessão. O contrato completo permanece estado → conflito → ausência de permissão.

## Revisão e situação após geração de tarefas

A conferência prévia confirmou os sete casos, três concessões próprias, decisão/motivo e domínio parcial, sem contradição funcional com a baseline completa. D-07 em [decisoes.md](../../documentacao/decisoes.md) registra a escolha técnica confirmada; [tasks.md](tasks.md) organiza trabalho futuro. Ambiente e versão exata serão conferidos na execução autorizada, sem instalação ou validação de compatibilidade realizadas agora.

Estado, handoff e bloqueios foram reconciliados para refletir Spec/plano/tarefas existentes. Restrições de etapas anteriores são históricas; o pedido atual autoriza somente registro de escolhas, tarefas e análise. P-01/P-02/P-03, adoção da constituição e revisão do gabarito/notas continuam pendentes. Nenhuma dessas pendências é resolvida pela confirmação técnica; piloto permanece sem liberação.

## Complexity Tracking

Nenhuma exceção constitucional ou complexidade adicional requerida. Sem infraestrutura, dependências externas ou abstrações de extensão antecipadas.
