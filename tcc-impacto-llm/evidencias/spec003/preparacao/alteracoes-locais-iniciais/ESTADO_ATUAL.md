> Revisão vigente — 21/10/2026 (D-19): Spec 003 confirmada pelo resolvedor local; tasks.md existente revisado, 35 tarefas pendentes. T024 separa controles sintéticos da matriz real e da CLI futura. B aec474bcb54d6dae2afceff8e5b9226991386490 disponível; fontes iniciais e referência 0.2 preservadas. Somente inspeção Git/JSON/documental e script de pré-requisitos; nenhuma variante implementada, teste ou chamada ao LLM executados. Revisão profissional, possíveis novos modelos e alterações nas métricas aguardam transcrição da orientação e decisão explícita. P-01/P-02/P-03 e adoção constitucional pendentes. Próxima ação: considerar o relatório de consistência desta revisão; implementação depende de pedido próprio. Registros datados abaixo são históricos.

> Estado vigente — 20/10/2026 (D-18): Spec 003 ativa, confirmada por setup-tasks; especificação, cinco artefatos de planejamento e `specs/003-mudancas-controladas/tasks.md` preparados. São 35 tarefas, todas pendentes (US1: 9; US2: 8; US3: 6; preparação/fechamento: 12), quatro paralelizáveis em fontes distintas. Baseline B aec474bcb54d6dae2afceff8e5b9226991386490, testes e referência candidata 0.2 intactos; conjuntos 2/4/8/5 e 48 expectativas preservados. Nenhuma variante implementada ou teste executado nesta etapa; sem piloto/LLM experimental. Análise de consistência somente documental, com relatório na resposta da solicitação. Revisões científicas e adoção constitucional continuam pendentes.

Próxima ação vigente: revisar tarefas 003 e os achados da análise, solicitando implementação somente quando desejado. Ler tasks, Spec/plano/contrato e D-18 em decisões. P-01/P-02/P-03 permanecem; P-04 tem T12 adotado e executado na versão inicial, expectativas das variantes ainda candidatas. Resultados de T12 anteriores em `documentacao/evidencias-t12.md`; registros/próximas ações anteriores abaixo são históricos.

## Estado anterior preservado — 18/10/2026

> Estado histórico — 18/10/2026 (D-13/D-14): Spec 002 implementada com Python 3.13.3 + unittest. RF-01–RF-04 integrados; 17 métodos aprovados, T01–T11 11/11 em decisão/motivo e 55 subtestes auxiliares conformes, zero falhas/erros/ignorados. Três estados, oito subconjuntos e duas operações no domínio válido; verificação dirigida, sem matriz que inclua T12. Evidências em `specs/002-heranca-incompatibilidade/quickstart.md` (caminho desde a raiz). T12 somente proposta; catálogo 11/44 e gabarito preservados. Sem variantes, piloto ou LLM experimental. Adoção constitucional e pendências científicas permanecem abertas. Trechos datados anteriores abaixo são históricos e não descrevem a capacidade atual.

Próxima ação: revisão humana dos resultados e das pendências científicas registradas em documentacao/decisoes.md. Nenhuma nova etapa iniciada automaticamente. Spec ativa permanece 002 em .specify/feature.json; aba da Spec 001 não define seleção.

## Registro histórico anterior

# Estado atual — 16/10/2026

- Incremento 1 fechado para engenharia: RF-01/RF-02 implementados; 17 tarefas com evidências; dez métodos aprovados no registro anterior, sete casos e controles conformes. [Evidências preservadas](specs/001-autorizacao-direta/evidencias.md).
- [Spec 002](specs/002-heranca-incompatibilidade/spec.md) e checklist revisadas; Spec ativa selecionada em `.specify/feature.json`, destino confirmado pelo resolvedor antes de gerar o plano.
- Especificação, checklist, planejamento e [tasks.md](specs/002-heranca-incompatibilidade/tasks.md) da Spec 002 preparados. Planejamento: [plan](specs/002-heranca-incompatibilidade/plan.md), research, data-model, contrato e quickstart; Python + unittest e organização existente mantidos. As 22 tarefas de implementação T001–T022 continuam pendentes, inclusive preparação, verificações e fechamento.
- Análise de consistência Spec/plano/tarefas realizada após a geração: oito itens funcionais e seis critérios de sucesso com tarefas relacionadas; nenhuma contradição funcional ou bloqueio identificado. A pendência de reconciliação temporal apontada na análise é tratada nesta atualização, sem alterar requisitos ou aceitação.
- Código permanece parcial: ativas garantidas somente Consulta ou Auditoria isoladamente. RF-03/RF-04 e ampliação para todos os subconjuntos estão planejados, ainda não implementados/verificados.
- Nenhum teste da Spec 002 executado; código não alterado nesta reconciliação. Evidência do incremento 1 permanece histórica e não demonstra implementação de RF-03/RF-04. Sem variantes, piloto, coleta ou LLM experimental.
- Recorte aceito conforme D-09; gabarito, notas, prompts, métricas e piloto ainda serão revisados. T12 proposto e não executado; catálogo 11/44 intacto. Constituição 1.0.0 sem adoção formal.
- Autorização e escolhas desta etapa: D-12 em [decisoes.md](documentacao/decisoes.md). Restrições antigas de somente documentação/sem Spec descrevem etapas anteriores, superadas no alcance dos pedidos registrados.

Histórico: a etapa anterior produziu somente o planejamento (D-12), sem tarefas; a solicitação posterior autorizou a geração das 22 tarefas e a análise de consistência. A reconciliação atual atualiza o registro documental e não executa nem conclui tarefas.

Próxima ação: solicitar implementação quando desejado e seguir a sequência de tasks.md, produzindo evidências reais. Nenhuma decisão funcional bloqueante identificada. T12 segue fora da aceitação; revisões científicas permanecem pendentes. Pendências e alcance em [BLOQUEIOS.md](BLOQUEIOS.md) e [HANDOFF.md](HANDOFF.md).
