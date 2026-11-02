# Specification Quality Checklist: Preparação de entradas e avaliação separada de IDs

> Complemento — 27/10/2026, D-24/D-25: cinco artefatos de planejamento preparados após novo pedido, com seleção 004 confirmada. [Plano](../plan.md) e [contrato](../contracts/preparacao-avaliacao.md) detalham o desenho. Marcações abaixo continuam sendo revisão da qualidade da especificação original; referências à ausência de plano e à seleção 003 são históricas. Nenhuma marcação representa execução das 16 famílias, isolamento demonstrado ou revisão científica; não há tarefas/implementação.

**Purpose**: revisar completude e qualidade da especificação antes de eventual planejamento.

**Created**: 2026-10-27

**Feature**: [spec.md](../spec.md)

**Review Ownership**: assistente, revisão documental solicitada pelo pesquisador (D-22/D-23).

**Marker Semantics**: `[x]` significa requisito documental conferido. Não significa implementação, controle executado, isolamento demonstrado, métricas aprovadas ou pesquisa liberada.

## Content Quality

- [x] Valor explícito: entrada permitida auditável, preservação de originais e comparação separada de seleções.
- [x] Sem prescrever linguagem, bibliotecas, serviços, cliente/API ou estrutura de implementação; nomes/campos expressam contrato de dados.
- [x] Entrada, resposta original, referência, sintético, formato válido e IDs conhecidos têm significados distintos.
- [x] Seções do template preenchidas: histórias/testes, requisitos/entidades, critérios observáveis e premissas.

## Requirement Completeness

- [x] FR-001–FR-012 verificáveis; revisões científicas não são apresentadas como resolvidas.
- [x] SC-001–SC-007 definem condições/contagens observáveis sem depender de tecnologia.
- [x] US1–US4 têm prioridades, verificação independente e aceitação sem LLM real.
- [x] Lista permitida enumera documentos/conteúdo, fontes reaproveitadas, ordem, hashes, versões e condições; pacote ainda não exportado/revisado.
- [x] Montador não consulta fontes mistas, gabarito/histórico/resultados/avaliador; inspeção de conteúdo e fronteira efetiva são exigidas futuramente.
- [x] Entrada integral, resposta bruta, erros, identificação, integridade e vínculos preservados; avaliação/retentativa não sobrescrevem originais.
- [x] Universos RF-01–RF-04/T01–T12 e referência por mudança explícitos; listas não são inferidas entre dimensões.
- [x] Formato válido, IDs desconhecidos, seleção vazia e falha técnica são estados distintos; esquema não significa acerto.
- [x] Duplicatas/ordem, string vazia, IDs trocados/aproximados, chaves repetidas e tipos/campos inválidos têm regras explícitas.
- [x] Desconhecidos contam como FP único sem descarte; duplicatas brutas não inflam contagens.
- [x] Formato inválido não produz extração observada ou avaliação parcial; zero operacional é imputação separada com denominador.
- [x] Transporte/fragmentos, integridade e referência defeituosa/vazia têm tratamento próprio, sem fabricar resposta/ajustar gabarito.
- [x] TP/FP/FN auditáveis; precisão/revocação/F1/Jaccard têm fórmulas/convenções candidatas, incluindo vazias e pares insuficientes.
- [x] Fundamentação/revisão das medidas pendentes; sem nota combinada, semelhança textual ou geração de código.

## Feature Readiness

- [x] FR-001–FR-003 vinculados a US1/SC-001/S-14; FR-004–FR-006 a US2/SC-002/SC-004/S-11/S-13/S-16.
- [x] FR-007–FR-009 vinculados a US3/SC-003/S-01–S-10/S-12; FR-010 a SC-004/SC-005/S-15/S-16.
- [x] FR-011 vinculado a US4/SC-006, S-01–S-16 com expectativas prévias e origem sintética obrigatória.
- [x] Controles abrangem exata, parcial, todos, vazias, duplicadas, desconhecidos, formato inválido, falha técnica e integridade; nenhum executado/apresentado como resultado LLM.
- [x] FR-012/SC-007 limitam 004 a Spec/checklist; sem plano, tarefas, implementação, interface/API/repositório, modelos ou chamadas.
- [x] Baseline, candidata 0.2, seleções 2/4/8/5, T12 adotado, variantes e evidências preservados.
- [x] Revisão profissional, notas definitivas, fundamentação de medidas, piloto final e adoção constitucional pendentes e rastreáveis.
- [x] Histórico/evidências de engenharia não viram aprovação científica ou autorização de piloto/coleta.

## Notes

Revisão documental em 27/10/2026: 26/26 itens satisfeitos após conferência com orientação/governança/fechamento 003 e materiais candidatos. Marcações atestam qualidade da especificação, não cumprimento futuro dos SCs. S-01–S-16 são planejados; não existe novo montador/avaliador e nenhum teste da aplicação foi executado nesta etapa.

Conferência final: 94 links locais válidos nos nove documentos novos/atualizados, sem placeholders ou espaços finais; 12 FRs/7 SCs/16 famílias S-xx. Consultas de leitura do roteiro recuperaram os quatro registros iniciais e cinco de variantes que sustentam suas tabelas. Histórico preservado; código, materiais e evidências existentes sem alterações. São verificações documentais, sem execução dos controles desta Spec.

Fluxo: [skill local speckit-specify](../../../.agents/skills/speckit-specify/SKILL.md), numeração sequencial 004, template core `.specify/templates/spec-template.md` (sem overrides/presets/extensões presentes). `.specify/extensions.yml` ausente nas conferências anterior/final, sem hooks. Sem branch/commit criado. Pelo limite de somente Spec/checklist para 004, a persistência do seletor prevista pela skill fica para planejamento autorizado; `.specify/feature.json` continua em 003.

Pronta documentalmente para revisão e eventual planejamento solicitado. Não congela política científica, exporta pacote ou demonstra isolamento. Revisão profissional, notas definitivas e desenho final do piloto continuam abertos em [decisões](../../../documentacao/decisoes.md) e [bloqueios](../../../BLOQUEIOS.md).
