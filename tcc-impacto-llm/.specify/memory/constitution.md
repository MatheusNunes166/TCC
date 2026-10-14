<!-- Sync Impact Report
Version change: template sem versão → 1.0.0 (constituição inicial preparada).
Modified principles: placeholders → Escopo controlado; Decisões explícitas;
Rastreabilidade; Verificação por evidências; Incrementos pequenos.
Added sections: Separação de contextos; Fluxo e fechamento; Governance preenchida.
Removed sections: nenhuma; exemplos substituídos.
Follow-up TODO: RATIFICATION_DATE — registrar adoção pelo responsável do projeto.
Templates e comandos dependentes não alterados; leem a constituição em execução.
Comentário temporário para revisão, a remover antes de commit após acompanhamento.
-->
# TCC Impacto LLM Constitution

## Core Principles

### I. Escopo controlado

Toda capacidade deve ter objetivo, limites e critérios observáveis antes da implementação.
Ampliações exigem decisão explícita e atualização do escopo. Conveniência técnica não autoriza
transformar a bancada em produto ou framework geral.

### II. Decisões explícitas

Decisões confirmadas devem registrar responsável, data, justificativa e evidência em
`documentacao/decisoes.md`. Propostas, hipóteses e aprovações têm estados distintos.
Não inferir aprovação do orientador a partir de documentação ou autorização de engenharia.

### III. Rastreabilidade

Requisitos, critérios, testes e mudanças devem manter IDs e vínculos verificáveis com as fontes.
Preservar materiais originais e registrar divergências e resolução antes de depender delas.
Alterações de contrato exigem revisão dos artefatos afetados.

### IV. Verificação por evidências

Testes devem confrontar entradas e saídas observáveis com expectativas identificadas e revisáveis.
Planejado, implementado e executado são estados distintos. Fechamento exige evidências reais dos
critérios aplicáveis; documentação ou código presente não prova correção nem valida a referência.

### V. Incrementos pequenos

Trabalhar uma capacidade delimitada por vez. Revisar alterações e lacunas antes de concluir,
reconciliar realizado e planejado e atualizar documentação, estado, bloqueios e handoff.
Não avançar silenciosamente da preparação para implementação ou pesquisa.

## Separação de contextos

Desenvolvimento e experimento devem ter contextos separados. A coleta deve usar pacote permitido
verificável, sem referência privada ou histórico de desenvolvimento; a avaliação acessa a referência
separadamente. Escolhas científicas pendentes permanecem em `documentacao/decisoes.md`, sem se
converterem em princípios constitucionais. Documentação pronta não libera piloto ou coleta.

## Fluxo e fechamento

Seguir o ciclo incremental de `documentacao/roadmap.md`. Resolver antes da implementação decisões
que afetem a capacidade corrente; pendências futuras não bloqueiam atividades independentes.
Toda revisão de fechamento deve conferir escopo, rastreabilidade, evidências e atualização do estado.
Instruções operacionais e ordem de leitura ficam em `AGENTS.md`.

## Governance

Versão preparada por solicitação do usuário; não registra aprovação científica do desenho.
TODO(RATIFICATION_DATE): registrar data de adoção explícita pelo responsável do projeto.
Alterações devem registrar responsável, justificativa, impacto e aprovação em
`documentacao/decisoes.md`, atualizar esta versão e revisar coerência dos documentos dependentes.
Usar SemVer: MAJOR para remoção/redefinição incompatível, MINOR para novo princípio ou expansão
material e PATCH para esclarecimento sem mudança de regra. Revisões de incremento devem verificar
conformidade; divergências exigem resolução explícita, sem exceções silenciosas.

**Version**: 1.0.0 | **Ratified**: pendente de adoção registrada | **Last Amended**: 2026-10-14
