# Referência candidata 0.3 — extensão exploratória D-41

09/11/2026. Para revisão do pesquisador; revisor e data de revisão permanecem nulos. Não enviar este documento ao modelo. A [referência 0.2](referencia-candidata-proxima-etapa.md), seus materiais e os dados do piloto permanecem nos caminhos originais. A ampliação foi autorizada pelo pesquisador no pedido de D-41; não há aprovação atribuída ao orientador ou a revisor externo.

As [75 expectativas JSON](../materiais/modelos/referencia_candidata_0.3_NAO_ENVIAR_AO_LLM.json) foram escritas pela [receita documental](../evidencias/spec004/extensao-2026-11-09/preparar_referencia.py), que não importa o núcleo, variantes ou avaliador. O [registro anterior à execução](../evidencias/spec004/extensao-2026-11-09/expectativas-antes-execucao.json) fixa seu hash. As 60 expectativas anteriores são conservadas. O [catálogo público 0.3](../materiais/modelos/catalogo_baseline_0.3.md) contém somente entradas e resultados da baseline; as expectativas das variantes permanecem privadas.

Os quatro RFs, três papéis, duas operações e herança de um nível são os mesmos. O [contrato](requisitos.md#ordem-global) determina estado → conflito → permissão e dá prioridade à origem direta quando direta e herdada coexistem. As quatro variantes são independentes, cada qual derivada da mesma baseline. Não foi encontrada contradição substantiva entre os três novos casos e o contrato. Nenhuma regra ou variante foi adaptada para satisfazer o gabarito.

| Caso | Entrada | Baseline | MC-01 | MC-02 | MC-03 | MC-04-v2 |
|---|---|---|---|---|---|---|
| T13 | ativa; Consulta + Supervisão; visualizar | permitir/direta | permitir/direta | permitir/direta | negar/sem | permitir/direta |
| T14 | ativa; Consulta + Auditoria + Supervisão; exportar | negar/conflito | negar/conflito | permitir/direta | negar/conflito | negar/conflito |
| T15 | em_revisao; Consulta + Auditoria + Supervisão; exportar | negar/estado | negar/estado | negar/estado | negar/estado | negar/estado |

`direta` designa `permissao_direta`; `sem` designa `sem_permissao`.

T13 exercita coexistência das duas origens: em MC-03, retirar Consulta/visualizar remove ambas; em MC-04, retirar a herança conserva Consulta diretamente atribuído. T14 diferencia conflito com Consulta direto de conflito dependente exclusivamente da herança, como T12: em MC-04 só o segundo desaparece. Em MC-02, retirar a incompatibilidade libera exportar diretamente por Auditoria. T15 exercita o mascaramento de conflito e concessão pelo estado, inclusive após as quatro mudanças. Isso amplia a cobertura de interações; dificuldade empírica não foi estabelecida.

A política conservadora e a definição de impacto funcional são as mesmas da [0.2](referencia-candidata-proxima-etapa.md#critério-de-impacto-e-critério-de-seleção). A aplicabilidade usa os papéis efetivos da baseline: permissão exige a operação alterada e o papel concedente; incompatibilidade exige o par efetivo; herança exige Supervisão atribuído, qualquer que seja operação ou estado. Mudança é qualquer diferença de decisão **ou motivo**; preservação relacionada conserva ambos em teste selecionado.

| Mudança | RFs candidatos | Testes de mudança | Testes de preservação relacionada | Total |
|---|---|---|---|---|
| MC-01 | RF-02 | T04 | T12, T14, T15 | 4 |
| MC-02 | RF-04 | T06, T07, T12, T14 | T11, T15 | 6 |
| MC-03 | RF-02, RF-03 | T02, T05, T13 | T01, T06, T07, T09, T10, T11 | 9 |
| MC-04-v2 | RF-03, RF-04 | T05, T07, T12 | T08, T10, T13, T14, T15 | 8 |

Os conjuntos de RFs não mudaram: MC-01 edita somente a concessão direta de Auditoria; MC-02 edita o predicado de conflito sem alterar a expansão; MC-03 altera a concessão de Consulta e sua permissão herdada; MC-04 altera a expansão de Supervisão e o conflito que dependia dela. RF-01 conserva o filtro de estado em todas; mera participação em teste não implica impacto.

| Mudança | Inclusão/exclusão dos novos casos | Exclusões completas pela política |
|---|---|---|
| MC-01 | T14/T15 preservam conflito/estado diante da perda de exportar; T13 excluído por visualizar | T01, T02, T03, T05, T06, T07, T08, T09, T10, T11, T13: visualizar ou ausência de Auditoria efetivo |
| MC-02 | T14 muda após retirada do conflito; T15 preserva estado; T13 não tem Auditoria | T01, T02, T03, T04, T05, T08, T09, T10, T13: falta o par Consulta + Auditoria efetivo |
| MC-03 | T13 muda ao perder visualizar direto e herdado; T14/T15 excluídos por exportar | T03, T04, T08, T12, T14, T15: operação exportar |
| MC-04-v2 | T13/T14/T15 têm Supervisão e preservam, respectivamente, concessão direta, conflito direto e estado | T01, T02, T03, T04, T06, T09, T11: Supervisão não atribuído |

As justificativas anteriores para T01–T12 continuam na referência 0.2; as adicionais estão também no JSON 0.3, por mudança/teste. Todo teste selecionado pertence a exatamente uma partição. Excluído significa não enquadrado nesta política, sem alegação de irrelevância universal. As reduções nominais candidatas com denominador 15 são 73,33%, 60%, 40% e 46,67%; são propriedades dos conjuntos, sem resultado empírico novo.

O avaliador escolhe o universo de testes pela versão: 0.2 mantém T01–T12; 0.3 reconhece T01–T15. A referência 0.3 exige preparação identificada com versão e hash correspondentes; preparações antigas não podem ser reinterpretadas silenciosamente. Mantêm-se as métricas e o formato `requisitos`/`testes`, sem mudar a política de pontuação.

Verificações executadas e limitações constam do [relatório D-41](../evidencias/spec004/extensao-2026-11-09/RELATORIO.md). A concordância local com as 75 expectativas é verificação de engenharia; a referência permanece candidata para revisão do pesquisador.
