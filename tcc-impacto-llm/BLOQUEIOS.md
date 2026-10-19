# Pendências por etapa — 18/10/2026

Registro central em [decisoes.md](documentacao/decisoes.md). Quadro vigente substitui pendências temporais antigas de solicitação/ambiente do incremento 1.

## Engenharia

Incremento 1 fechado com evidências; Python 3.13.3 usado naquela execução. Não há bloqueio funcional para o planejamento 002 concluído. Spec 002 ativa; desenho em [plan.md](specs/002-heranca-incompatibilidade/plan.md).

Reconciliação: geração das 22 tarefas e análise já registradas em tasks, estado e handoff de 16/10. Implementação e testes locais agora autorizados pelo pedido de 18/10 (D-13); Python 3.13.3 confirmado. Incremento 002 concluído: 22 tarefas com evidências em [quickstart](specs/002-heranca-incompatibilidade/quickstart.md); 17 métodos OK, onze casos e controles conformes. Nenhum bloqueio funcional identificado. Sem dependências externas. Pendências abaixo continuam científicas/de etapas futuras.

Adoção formal da constituição continua pendente do responsável; cumprimento da revisão de engenharia não equivale a ratificação.

## Pesquisa futura

| Pendência | Efeito | Responsável |
|---|---|---|
| P-01, demais detalhes além do recorte aceito (D-09): impacto funcional e desenho das mudanças. | Fechar desenho científico/referência; não bloqueia núcleo delimitado. | Orientador e pesquisador. |
| P-02: revisão de gabarito, notas, prompts, política e métricas; definir revisor/data. | Validar referência e liberar preparação científica do piloto. | Orientador/pesquisador/revisor combinado. |
| P-03: condições, piloto, análise, repetições e congelamento. | Liberar piloto/coleta conforme gates; números permanecem propostas. | Orientador e pesquisador. |
| P-04/T12: decidir adoção e revisar relevância nas quatro mudanças. | Se adotado, atualizar catálogo, conjuntos e cálculos/denominadores (12/48 em vez de 11/44). | Pesquisador com revisão humana/alinhamento científico. |
| Modelo/API, parâmetros, orçamento, saída e isolamento demonstrado. | Preparar coleta utilizável e liberar piloto. | Responsável técnico/pesquisador. |

T12 não adotado nem executado; suíte e referência preservadas. MC-04 sem herança pode liberar exportar em Supervisão+Auditoria eliminando conflito; T07/visualizar permanece correto. Não há variante implementada. [Condições do piloto](documentacao/qualidade-e-testes.md) continuam obrigatórias; plano pronto não libera experimento.
