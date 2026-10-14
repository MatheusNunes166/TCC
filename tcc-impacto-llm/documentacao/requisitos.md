# Requisitos e contrato candidato

Estado: definições derivadas do [material de referência](../materiais/02_REQUISITOS_TESTES_E_REFERENCIA.md), ainda sujeitas à revisão humana. A criação desta baseline não registra aprovação do orientador. Ver [decisoes.md](decisoes.md).

## Entradas e saídas

Entrada: estado (`ativa`, `suspensa`, `em_revisao`), conjunto de papéis (`Consulta`, `Auditoria`, `Supervisão`) e operação (`visualizar`, `exportar`). Vocabulário fechado, dados fictícios e entradas válidas; validação de entradas malformadas está fora do recorte.

Saída: decisão `permitir` ou `negar`, acompanhada de um motivo estável: `estado`, `conflito`, `sem_permissao`, `permissao_direta` ou `permissao_herdada`. Decisão e motivo compõem o resultado observável.

## Regras e aceitação planejada

| ID | Regra candidata | Critérios de aceitação |
|---|---|---|
| RF-01 | Somente conta ativa prossegue. | Suspensa e em revisão retornam `negar/estado`, mesmo com permissão ou conflito. Conta ativa segue para as demais regras. |
| RF-02 | Obter permissões diretas dos papéis atribuídos. | Consulta concede visualizar; Auditoria concede exportar; Supervisão não concede permissão própria. Sem bloqueios, concessão direta retorna `permitir/permissao_direta`. Não negar antes de avaliar a herança. |
| RF-03 | Expandir papéis e permissões por uma relação de herança de um nível. | Supervisão inclui Consulta como papel efetivo e herda visualizar; sem bloqueios, retorna `permitir/permissao_herdada`. Não herda exportar. Sem expansão multinível ou ciclos. |
| RF-04 | Verificar incompatibilidade entre papéis efetivos. | Consulta + Auditoria retorna `negar/conflito`, inclusive se Consulta vier da herança; estado mantém precedência. |

## Ordem global

1. Verificar estado; se não ativo, negar por `estado`.
2. Obter permissões diretas e expandir papéis/permissões herdados.
3. Verificar incompatibilidade sobre os papéis efetivos; negar por `conflito` se presente.
4. Decidir pela permissão da operação. Sem concessão, negar por `sem_permissao`. Com concessão, permitir pela origem; se direta e herdada coexistirem, usar `permissao_direta`.

A precedência das negações é estado → conflito → ausência de permissão. Um incremento parcial de RF-01/RF-02 não pode redefinir o contrato global ou alegar suporte a RF-03/RF-04.

## Definições ainda candidatas

Permanecem para confirmação: redação dos quatro RFs, contrato `decisão + motivo`, precedência, prioridade da origem direta e definição de impacto funcional em dependências. Os onze resultados esperados são expectativas, não evidências: [qualidade-e-testes.md](qualidade-e-testes.md). Política experimental e conjuntos candidatos permanecem no material de referência, sem duplicação integral aqui.
