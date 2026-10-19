> Estado vigente — 18/10/2026 (D-13/D-14): Spec 002 implementada com Python 3.13.3 + unittest. RF-01–RF-04 integrados; 17 métodos aprovados, T01–T11 11/11 em decisão/motivo e 55 subtestes auxiliares conformes, zero falhas/erros/ignorados. Três estados, oito subconjuntos e duas operações no domínio válido; verificação dirigida, sem matriz que inclua T12. Evidências em `specs/002-heranca-incompatibilidade/quickstart.md` (caminho desde a raiz). T12 somente proposta; catálogo 11/44 e gabarito preservados. Sem variantes, piloto ou LLM experimental. Adoção constitucional e pendências científicas permanecem abertas. Trechos datados anteriores abaixo são históricos e não descrevem a capacidade atual.

Próxima ação: revisão humana dos resultados e das pendências científicas registradas em documentacao/decisoes.md. Nenhuma nova etapa iniciada automaticamente. Spec ativa permanece 002 em .specify/feature.json; aba da Spec 001 não define seleção.

## Registro histórico anterior

# Handoff — 16/10/2026

Ler [AGENTS](AGENTS.md), constituição, estado, bloqueios e decisões; depois [Spec 002](specs/002-heranca-incompatibilidade/spec.md), checklist, os cinco artefatos de [planejamento](specs/002-heranca-incompatibilidade/plan.md) e [tasks.md](specs/002-heranca-incompatibilidade/tasks.md).

Spec ativa: `specs/002-heranca-incompatibilidade` em .specify/feature.json. Resolvedor confirmou FEATURE_SPEC/IMPL_PLAN antes de setup-plan; nenhum branch criado. Não voltar à Spec 001 por suposição ou gerar nova Spec.

Incremento 1 fechado para engenharia; [evidências](specs/001-autorizacao-direta/evidencias.md) preservadas. O código atual continua RF-01/RF-02 parcial. Spec 002: especificação, planejamento e tarefas preparados; análise de consistência realizada, sem contradição funcional ou requisito sem tarefa. As 22 tarefas T001–T022 permanecem pendentes. Nenhum teste da Spec 002 executado e nenhuma implementação concluída.

Histórico: o planejamento anterior (D-12) terminou sem tarefas; a solicitação posterior autorizou somente sua geração e análise. Esta reconciliação corrige o estado temporal dos documentos, sem executar tarefas ou modificar requisitos, código e gabarito.

Desenho futuro mantém autorizacao.py e tests/test_autorizacao.py, Python + unittest. Preserva consulta direta dos atribuídos; funções puras de papéis efetivos e incompatibilidade; estado primeiro, conflito antes da decisão por permissão, direta antes de herdada e ausência por último. Ampliação do domínio só vale após implementar/verificar. Integrar T05–T08 aos sete casos, preservar controles e acrescentar bordas da Spec. Guia registra execução futura; não confundir com resultados.

Próxima ação: solicitar implementação quando desejado; então seguir T001–T022 (preparação → herança → conflito → regressão/integração → revisão/documentação), registrando evidências antes de marcar conclusão. Não implementar automaticamente. Nenhuma dúvida funcional bloqueante identificada.

D-12 registra autorização de planejamento e alcance; D-09/P-04 preservam limites científicos. T12 permanece proposto fora da aceitação/execução planejada. Sua eventual adoção exige revisão nas quatro mudanças e recálculos. Sem gabarito alterado ou validado, sem variantes/piloto/LLM experimental. Adoção formal da constituição e revisão científica continuam pendentes em [BLOQUEIOS](BLOQUEIOS.md).
