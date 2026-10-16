# Pendências por etapa — 14/10/2026

## Situação vigente — 16/10/2026

Primeiro incremento sem bloqueio: implementação autorizada por D-10 e concluída; Python 3.13.3 conferido, 10 métodos passaram. [Evidências](specs/001-autorizacao-direta/evidencias.md). As duas pendências de implementação/ambiente de 14/10 abaixo estão resolvidas.

P-01 parcialmente atendida quanto ao recorte aceito pelo orientador (relato do usuário, D-09); não presume aprovação integral do desenho. Permanecem revisão do gabarito, notas, prompts, métricas e piloto, demais alinhamentos P-01/P-02/P-03, modelo/API/orçamento/isolamento e adoção formal da constituição. P-04/T12: proposta não executada; revisar relevância nas quatro mudanças e atualizar suíte/cálculos se adotada. RF-03/RF-04 e variantes futuros, piloto/coleta sem liberação. Registros de 14/10 abaixo são históricos.

Não há bloqueio para concluir a governança documental. Este quadro delimita efeitos; o registro central permanece em [decisoes.md](documentacao/decisoes.md).

## Primeiro incremento

Contrato base fornecido pelo usuário (D-06); especificação e planejamento realizados. Python + unittest e organização mínima confirmados (D-07); geração de tarefas autorizada (D-08). Essas escolhas não são mais bloqueios.

| Pendência | O que impede | Quem decide ou verifica |
|---|---|---|
| Solicitação de implementação futura. | Executar tasks agora; o pedido atual termina em tarefas e análise. | Usuário/responsável do projeto. |
| Conferir interpretador e versão compatível com a proposta 3.11+. | Executar verificações automatizadas sem ambiente disponível; disponibilidade ainda não conferida. Não bloqueia a lista de tarefas. | Responsável técnico durante preparação autorizada. |

A adoção formal da constituição segue pendente de registro pelo responsável; não equivale à aprovação científica nem é declarada resolvida pela confirmação técnica. Não há contradição funcional bloqueante identificada na conferência prévia Spec/plano.

## Somente experimento futuro

| Pendência | O que impede | Quem decide |
|---|---|---|
| P-01: objeto, impacto funcional e escolha de MC-04. | Fechar desenho e referência das mudanças; não impede especificar RF-01/RF-02 no recorte atual. | Orientador em alinhamento com pesquisador. |
| P-02: política, medidas, revisor e revisão da referência/notas. | Declarar referência validada e liberar piloto. | Orientador alinha política/medidas e revisor; revisor combinado realiza revisão e pesquisador registra. |
| P-03: condições, piloto, análise e repetições. | Congelar protocolo e executar pesquisa principal. | Orientador e pesquisador; quantidade final fixada após viabilidade do piloto. |
| Modelo/API, parâmetros suportados, orçamento, modalidade de saída e isolamento demonstrado. | Preparar coleta utilizável e liberar piloto; não impede núcleo de permissões. | Pesquisador/responsável técnico, com alinhamento científico se alterar o desenho. |

Condições de entrada do piloto permanecem em [qualidade-e-testes.md](documentacao/qualidade-e-testes.md) e no material de piloto/coleta. Documentação pronta não as satisfaz por si só.
