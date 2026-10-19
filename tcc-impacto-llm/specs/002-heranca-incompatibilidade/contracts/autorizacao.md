# Contrato local planejado — baseline integrada

Status: implementado em 18/10/2026; evidências em [quickstart](../quickstart.md). Evolui o [contrato parcial](../../001-autorizacao-direta/contracts/autorizacao.md); assinaturas existentes preservadas. Sem HTTP, CLI ou persistência.

## Funções

| Função | Entrada | Saída/semântica |
|---|---|---|
| autorizar(estado, papeis, operacao) | str, frozenset[str], str | dict[str, str] com exatamente decisao e motivo. |
| obter_permissoes_diretas(papeis) | frozenset[str] | frozenset[str] das concessões próprias dos papéis recebidos; sem herança ou conflito. Semântica existente preservada. |
| obter_papeis_efetivos(papeis) | frozenset[str] atribuídos | frozenset[str] com atribuídos e Consulta se houver Supervisão; implementada. |
| ha_incompatibilidade(papeis_efetivos) | frozenset[str] já efetivos | bool, verdadeiro se contém Consulta e Auditoria; não expande herança; implementada. |

Funções puras, sem I/O, mutação de argumentos ou exposição de política mutável. Vocabulário: estados ativa/suspensa/em_revisao; papéis Consulta/Auditoria/Supervisão; operações visualizar/exportar.

## Domínio e evolução

Atual: três estados válidos, oito subconjuntos dos papéis, duas operações. Garantia parcial ampliada pela integração. Verificação dirigida, sem executar toda a matriz de autorização: T12 permanece excluído.

A consulta de concessões próprias já aceita todos os conjuntos válidos. Retorno para Supervisão continua vazio; isso não implica negação final de visualizar após RF-03.

## Ordem e resultados

| Condição | Decisão | Motivo |
|---|---|---|
| suspensa/em_revisao | negar | estado |
| ativa, Consulta + Auditoria efetivos | negar | conflito |
| ativa, sem conflito, operação concedida diretamente nos atribuídos | permitir | permissao_direta |
| ativa, sem conflito, sem concessão direta, operação disponível pelos efetivos | permitir | permissao_herdada |
| ativa, sem conflito, sem concessão | negar | sem_permissao |

Estado encerra antes de consultas; conflito precede a decisão por permissão; direta precede herdada quando coexistem. Os efetivos preservam atribuídos e incluem Consulta por Supervisão, nunca Auditoria por herança.

Exemplos: Supervisão/visualizar → permitir/permissao_herdada; Supervisão/exportar → negar/sem_permissao; Supervisão+Auditoria/visualizar → negar/conflito; Supervisão+Consulta/visualizar → permitir/permissao_direta; ativa sem papéis → negar/sem_permissao.

Onze casos e expectativas na [Spec](../spec.md). Verificar dicionários inteiros e retornos imutáveis das consultas. T12 é proposta separada, não critério desta interface. Nenhuma guarda, exceção ou motivo novo para entradas inválidas; elas permanecem fora do domínio.
