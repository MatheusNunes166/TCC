# Specification Quality Checklist: Quatro mudanças controladas e verificação de efeitos

**Purpose**: validar completude e qualidade da especificação antes de planejamento posterior.

**Created**: 2026-10-19

**Feature**: [spec.md](../spec.md)

**Review Ownership**: assistente, revisão documental solicitada pelo pesquisador.

**Marker Semantics**: `[x]` significa qualidade dos requisitos revisada e satisfeita; não implementação, execução de testes, conformidade de variantes ou aprovação científica.

## Content Quality

- [x] Sem prescrever linguagem, framework, estrutura de código, estratégia de isolamento ou formato de registros; commit e IDs são requisitos de procedência solicitados.
- [x] Valor para o pesquisador explícito: atribuir efeitos à alteração isolada, conferir resultados e investigar divergências.
- [x] Termos de domínio, decisão/motivo, variante, referência e resultado definidos para revisão.
- [x] Seções obrigatórias preenchidas na ordem do template: cenários, requisitos, critérios de sucesso e premissas.

## Requirement Completeness

- [x] Nenhum esclarecimento funcional bloqueante ou placeholder aberto; pendências científicas têm alcance explícito.
- [x] FR-001–FR-010 são verificáveis e separados dos IDs RF-01–RF-04 da bancada.
- [x] SC-001–SC-007 têm contagens ou condições observáveis e vínculos aos requisitos.
- [x] Critérios de sucesso independem da tecnologia de implementação das variantes/registros.
- [x] US1–US3 têm prioridade, teste independente e cenários Dado/Quando/Então para os fluxos principais.
- [x] Bordas cobrem motivo divergente, preservação por precedência, caso excluído, origem inválida, erro/ausência, duplicata e conflito documental.
- [x] Escopo atual limitado a Spec/checklist; implementação, execução e pesquisa ficam explicitamente futuras.
- [x] Dependências/premissas identificam commit B, referência 0.2, T12, autorização futura e revisões pendentes.

## Feature Readiness

- [x] FR-001/FR-002 e US1 exigem quatro mudanças independentes sobre `aec474bcb54d6dae2afceff8e5b9226991386490`, sem acumulação e com identificação da versão executada.
- [x] Tabela contém exatamente as quatro remoções solicitadas; MC-04 corresponde a MC-04-v2 sem renomear JSON ou reintroduzir a mudança histórica de estado.
- [x] FR-003 exige preservar B e conferir seus casos/controles, distinguindo preservação de B de saídas que mudam nas variantes.
- [x] FR-004/FR-005 identificam matriz 0.2 e exigem 12 casos por variante, 48 pares e 60 expectativas incluindo B; distinguem seleção 2/4/8/5 de execução integral.
- [x] FR-006/FR-009 exigem decisão e motivo, inclusive T07/MC-04 e T12; cenários reproduzem expectativas existentes.
- [x] FR-007 exige esperado, observado, procedência e divergência por par, sem inventar observação em erro/ausência ou contar duplicatas.
- [x] FR-008 exige investigação pelas regras e revisão humana separada de suspeita de erro na referência, sem ajuste automático ao código.
- [x] FR-010/SC-003 distinguem investigação de conformidade integral; lacunas ou divergências pendentes não permitem declarar 48/48 conforme.
- [x] Todos os FRs têm aceitação nas histórias, bordas ou SCs, sem depender de desenho de implementação.
- [x] FR-010/SC-007 distinguem conformidade executável, autorização do pesquisador e aprovação científica; T12 continua adotado e gabarito candidato.
- [x] Nenhum detalhe de implementação ou resultado futuro é apresentado como trabalho realizado; não foram gerados plano/tarefas ou executados testes da bancada.

## Notes

Revisão documental em 19/10/2026, uma passagem, sem contradição funcional bloqueante. “48/48 conforme” é meta futura. Marcações atestam qualidade da Spec; revisão científica continua pendente.

Fluxo: [skill local speckit-specify](../../../.agents/skills/speckit-specify/SKILL.md). Configuração `feature_numbering: sequential`, diretórios existentes 001/002, próximo 003. Pilha local conferida, sem presets/overrides; usado `.specify/templates/spec-template.md` e ciclo de checklist de qualidade de specify. `.specify/extensions.yml` ausente antes da escrita e novamente no fechamento; sem hooks a despachar. Nenhuma branch ou commit criado.

Por instrução de produzir somente Spec/checklist, `.specify/feature.json` continua na Spec 002. A persistência de seleção prevista pela skill fica para planejamento autorizado: adaptação de escopo ao pedido do usuário, sem necessidade de confirmação. A próxima etapa deverá selecionar explicitamente `specs/003-mudancas-controladas` e confirmar o destino antes de gerar artefatos.

Repositório inicialmente limpo; HEAD identificado no cabeçalho da Spec. Leitura do JSON confirmou versão 0.2, status `CANDIDATO_NAO_REVISADO`, 12 casos e 12 expectativas por mudança, conjuntos de 2/4/8/5 testes. Fontes, expectativas e conjuntos permanecem intactos. Evidências T12 anteriores lidas, sem repetição de testes de aplicação nesta etapa documental.

Pronta documentalmente para planejamento quando solicitado. Permanecem P-01/P-02/P-03, revisão científica das expectativas T12 em P-02, adoção formal da constituição e pendências de coleta/isolamento. Especificar retirada de herança não registra aprovação científica dessa escolha. Sem implementação de variantes, piloto ou LLM experimental.
