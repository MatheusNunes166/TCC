> Estado vigente — 21/10/2026 (D-20/D-21): Spec 003 implementada e verificada; 35/35 tarefas concluídas com evidências. Quatro variantes independentes de B `aec474bcb54d6dae2afceff8e5b9226991386490`, uma edição por fonte, diffs/AST e revisão registrados. Python 3.13.3: suíte original 18 métodos OK, baseline 12/12 pares e variantes 48/48 conformes por decisão/motivo, zero divergências/erros/lacunas; 17 métodos sintéticos separados da bancada. Baseline, testes, materiais, referência candidata 0.2 e seleções 2/4/8/5 preservados. Evidências e diagnóstico do mecanismo: `specs/003-mudancas-controladas/evidencias.md` (desde a raiz). P-01/P-02/P-03, revisão das expectativas T12 e adoção constitucional pendentes; T12 já adotado/verificado em B. Revisão profissional, possíveis novos modelos e métricas aguardam transcrição da orientação e decisão explícita. Sem piloto, coleta ou LLM. Próxima ação: revisão humana das evidências e da referência candidata, seguida de detalhamento da orientação; nenhuma etapa experimental liberada. Registros anteriores abaixo são históricos.

> Revisão vigente — 21/10/2026 (D-19): Spec 003 confirmada pelo resolvedor local; tasks.md existente revisado, 35 tarefas pendentes. T024 separa controles sintéticos da matriz real e da CLI futura. B aec474bcb54d6dae2afceff8e5b9226991386490 disponível; fontes iniciais e referência 0.2 preservadas. Somente inspeção Git/JSON/documental e script de pré-requisitos; nenhuma variante implementada, teste ou chamada ao LLM executados. Revisão profissional, possíveis novos modelos e alterações nas métricas aguardam transcrição da orientação e decisão explícita. P-01/P-02/P-03 e adoção constitucional pendentes. Próxima ação: considerar o relatório de consistência desta revisão; implementação depende de pedido próprio. Registros datados abaixo são históricos.

# Pendências vigentes — 20/10/2026

Atualização D-18: tarefas da Spec 003 geradas, 35 pendentes; fluxo setup-tasks confirmou a seleção ativa. Spec/plano/contrato/referência lidos, análise de consistência posterior somente documental e apresentada na resposta. Geração não executa tarefas ou testes. Próxima ação de engenharia: revisar lista/achados e autorizar implementação quando desejado, sem dispensar revisões científicas da tabela. Nenhuma variante, teste, piloto ou chamada experimental nesta etapa; expectativas/conjuntos intactos. Atualizações de 19/10 abaixo preservam o histórico do planejamento e não mantêm pendência de gerar tarefas.

Atualização D-17: Spec 003 ativa, cinco artefatos de planejamento preparados em `specs/003-mudancas-controladas/`. B aec474bcb54d6dae2afceff8e5b9226991386490 confirmado por leitura, código/testes/referência necessários presentes e nenhuma alteração relevante não commitada inicialmente. Sem dúvida técnica bloqueante para este planejamento. Próxima ação de engenharia: revisar desenho e solicitar tarefas; não existem tarefas/variantes implementadas nem nova execução de testes. A solicitação atual supera a próxima ação antiga abaixo somente no alcance documental de planejamento. Pendências científicas da tabela continuam abertas, sem nova adoção de T12 a solicitar.

Decisões centrais: D-15/D-16 em [decisões](documentacao/decisoes.md). T12 adotado pelo pesquisador e executado na versão inicial; teste isolado e suíte integrada (18 métodos) aprovados. Sem divergência ou bloqueio funcional de engenharia; evidências em [evidencias-t12.md](documentacao/evidencias-t12.md). Catálogo e referência candidata harmonizados: 12 testes, 48 pares, 60 expectativas incluindo a versão inicial; seleções 2/4/8/5.

| Pendência atual | Situação e responsável |
|---|---|
| P-04/T12 — adoção e implementação do teste inicial | Concluídas por autorização do pesquisador D-15; evidências D-16. Não pedir novamente decisão de adoção. |
| P-04/T12 — revisão científica das expectativas das mudanças | Candidatas em referência 0.2; integrar à revisão P-02 com revisor/data a combinar. Nenhuma variante executada. |
| P-01 — critério funcional e desenho das mudanças | Alinhamento científico restante com orientador/pesquisador; MC-04 designa a retirada de herança MC-04-v2 nesta referência. |
| P-02 — gabarito, notas, prompts, política e métricas | Revisão humana ainda pendente; adoção de T12 pelo pesquisador não registra aprovação do orientador. |
| P-03 — condições, piloto, repetições e congelamento | Propostas pendentes; piloto não iniciado nem liberado. |
| Modelo/API, orçamento, coleta, avaliador e isolamento | Implementação/configuração/verificação futuras, sob autorização própria; bloco comum documental não prova isolamento de payload. |
| Adoção formal da constituição | Continua pendente do responsável. |

Próxima ação: revisão humana da referência candidata 0.2. Proibidas nesta etapa implementação de variantes, piloto e chamadas ao LLM experimental. Registros abaixo descrevem a situação anterior e são preservados como histórico, inclusive a antiga pendência de adoção de T12.

## Histórico — 18/10/2026

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
