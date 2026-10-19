> Estado vigente — 18/10/2026 (D-13/D-14): Spec 002 implementada com Python 3.13.3 + unittest. RF-01–RF-04 integrados; 17 métodos aprovados, T01–T11 11/11 em decisão/motivo e 55 subtestes auxiliares conformes, zero falhas/erros/ignorados. Três estados, oito subconjuntos e duas operações no domínio válido; verificação dirigida, sem matriz que inclua T12. Evidências em `specs/002-heranca-incompatibilidade/quickstart.md` (caminho desde a raiz). T12 somente proposta; catálogo 11/44 e gabarito preservados. Sem variantes, piloto ou LLM experimental. Adoção constitucional e pendências científicas permanecem abertas. Trechos datados anteriores abaixo são históricos e não descrevem a capacidade atual.

﻿# Requisitos e contrato candidato

> Atualização vigente — 16/10/2026: RF-01/RF-02 implementados e verificados com Python 3.13.3 + unittest, sem terceiros. Sete casos de aceitação conformes, três concessões próprias, 32 combinações de estado e controle Auditoria/visualizar; 10 métodos, zero falhas/erros/ignorados. Evidências em `specs/001-autorizacao-direta/evidencias.md` (caminho desde a raiz). D-09/D-10 registram recorte aceito e autorização. Domínio ativo parcial somente Consulta ou Auditoria isoladamente; RF-03/RF-04 permanecem futuros. Afirmações de ausência de autorização/implementação nos registros de 14/10 abaixo são históricas, superadas somente nesse alcance. Constituição não formalmente adotada; referência, notas, prompts, métricas e piloto pendentes. Nenhum piloto ou LLM experimental executado.


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

## Situação da baseline completa e do incremento 1

Para engenharia do incremento 1, o usuário forneceu o contrato RF-01/RF-02, decisão/motivo e precedência do estado na solicitação da Spec (D-06). O recorte e os cenários estão na [Spec 001](../specs/001-autorizacao-direta/spec.md). A baseline completa, a prioridade entre origem direta/herdada e a definição científica de impacto funcional permanecem sujeitas à revisão; essa delimitação não altera RF-03/RF-04 nem aprova o experimento. Os onze resultados esperados são expectativas, não evidências: [qualidade-e-testes.md](qualidade-e-testes.md). Política experimental e conjuntos candidatos permanecem no material de referência, sem duplicação integral aqui.
