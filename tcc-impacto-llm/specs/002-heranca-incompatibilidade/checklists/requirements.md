> Complemento vigente — 19/10/2026, D-15/D-16: T12 adotado pelo pesquisador e acrescentado à suíte da versão inicial; teste isolado OK e 18 métodos integrados OK. Catálogo atual T01–T12, 48 pares e 60 expectativas com a versão inicial, referência ainda candidata. Evidências em `documentacao/evidencias-t12.md` desde a raiz. O conteúdo datado abaixo preserva o escopo e as evidências originais da Spec 002 (T01–T11); menções a T12 como proposta ou fora da aceitação descrevem aquele incremento, superadas por D-15 apenas nesse alcance. Sem variantes, piloto ou LLM experimental; sem aprovação científica atribuída ao orientador.

# Specification Quality Checklist: Herança de um nível e incompatibilidade efetiva

**Purpose**: conferir qualidade e completude da especificação; checklist originalmente revisada antes do planejamento.
**Created**: 2026-10-16
**Feature**: [spec.md](../spec.md)
**Review Ownership**: assistente, revisão documental solicitada pelo usuário.
**Marker Semantics**: `[x]` indica qualidade de requisitos revisada e satisfeita; não implementação, execução de testes ou aprovação científica.

## Content Quality

- [x] Sem prescrever linguagem, framework, estrutura de código ou novas interfaces; ambiente anterior somente como evidência histórica.
- [x] Valor para o pesquisador explícito nas três histórias.
- [x] Termos do domínio definidos e redação compreensível para revisão.
- [x] Seções obrigatórias do template preenchidas e sem placeholders.

## Requirement Completeness

- [x] Nenhum esclarecimento funcional bloqueante pendente.
- [x] RF-03/RF-04 verificáveis: um nível, Supervisão inclui Consulta e conflito entre Consulta/Auditoria efetivos.
- [x] SC-001–SC-006 mensuráveis e separados dos resultados anteriores.
- [x] Critérios independentes de tecnologia; decisão e motivo verificados juntos.
- [x] T05–T08 preservam IDs, entradas e expectativas originais.
- [x] Bordas incluem vazio, coexistência direta/herdada e precedência.
- [x] Escopo exclui implementação, variantes, piloto, LLM e framework geral.
- [x] Dependências, fontes e pendências científicas identificadas em Assumptions.

## Feature Readiness

- [x] Todas as regras funcionais têm aceitação observável; prioridade entre origens preserva contrato existente.
- [x] Histórias cobrem herança, conflito direto/herdado e preservação do primeiro incremento.
- [x] Onze casos rastreados: sete regressões e quatro ainda não implementados.
- [x] Controles anteriores preservados: três concessões próprias, 32 combinações de estado e Auditoria/visualizar.
- [x] Ampliação futura do domínio explícita; resultado incidental fora do recorte anterior não é contrato de regressão.
- [x] T12 separado da aceitação; revisão nas quatro mudanças e recálculos condicionados à adoção.
- [x] Nenhuma solução técnica prescrita ou capacidade declarada pronta pela existência da Spec.

## Notes

Histórico da revisão inicial: checklist concluída em uma passagem, sem contradição funcional bloqueante. Naquele momento, a Spec estava pronta para planejamento, sem plano ou tarefas criados.

Estado reconciliado — 16/10/2026: especificação, planejamento e [tasks.md](../tasks.md) preparados; análise de consistência Spec/plano/tarefas realizada, com cobertura dos oito itens funcionais e seis critérios de sucesso. Nenhuma contradição funcional identificada; a observação sobre trechos temporais desatualizados é tratada nesta reconciliação. As 22 tarefas de implementação estão pendentes e nenhum teste da Spec 002 foi executado. T12 continua fora da aceitação e as revisões científicas permanecem pendentes. As marcações desta checklist continuam atestando somente qualidade de requisitos.

Fechamento do incremento 1 conferido: [17 tarefas](../../001-autorizacao-direta/tasks.md), [evidências reais](../../001-autorizacao-direta/evidencias.md), código/testes e documentação coerentes quando trechos anteriores são lidos como históricos. SC-001–SC-004 anteriores atendidos no registro. Nenhum teste repetido nesta etapa. Saída inicial truncada continua declarada como resumo; relatórios posteriores comprovam conformidade. Nenhuma lacuna funcional identificada que justifique repetição.

Fluxo aplicado: `.agents/skills/speckit-specify/SKILL.md`; numeração sequencial em `.specify/init-options.json`, próxima pasta `002-heranca-incompatibilidade`. Pilha local de templates conferida: sem overrides ou presets, utilizado `.specify/templates/spec-template.md`; checklist segue ciclo de qualidade de specify. `.specify/extensions.yml` ausente antes e após a escrita, sem hooks ou criação automática de branch.

Histórico da etapa de especificação: por instrução do usuário (somente Spec e checklist), `.specify/feature.json` não foi alterado naquele momento, ficando a seleção para o planejamento. Posteriormente, a Spec 002 foi selecionada e o destino conferido pelos scripts locais antes de gerar planejamento e tarefas. Isso não equivale a execução de implementação.

P-01 parcialmente atendida quanto ao recorte; P-02/P-03/P-04 e adoção constitucional permanecem pendentes. Nenhum catálogo/gabarito/material original, código ou teste alterado. Nenhuma variante, piloto ou chamada ao LLM executada.
