# Roadmap incremental

Situação operacional e próximas tarefas: [estado atual](../ESTADO_ATUAL.md). Este documento descreve critérios de passagem; não duplica o andamento nem autoriza execuções.

D-41 (09/11/2026) acrescenta uma extensão exploratória após o piloto encerrado pelo pesquisador: quinze casos e 75 comparações locais; 64 observações novas com dois modelos nomeados, dois blocos de 32 e ordem própria. [Referência candidata 0.3](referencia-candidata-0.3.md) e [preparação/verificação](../evidencias/spec004/extensao-2026-11-09/RELATORIO.md). Isso não congela a coleta principal nem modifica os critérios históricos da versão 0.2 abaixo.

## Ciclo de trabalho

Seguir a [metodologia](../materiais/03_DESENVOLVIMENTO_SPEC_KIT.md): delimitar capacidade → esclarecer contratos → especificar, planejar e decompor tarefas quando autorizado → analisar coerência → implementar quando autorizado → verificar → reconciliar evidências e decisões. Spec Kit é apoio de desenvolvimento, não condição experimental nem validação científica.

## Capacidades e critérios de passagem

| Etapa | Entrega | Evidência necessária |
|---|---|---|
| 0 — Baseline documental | Escopo, contratos e pendências explícitas. | Coerência documental; decisões essenciais registradas. |
| 1 — Autorização direta e estado | RF-01/RF-02, decisão/motivo. | Contrato e implementação da [Spec 001](../specs/001-autorizacao-direta/). |
| 2 — Herança e incompatibilidade | RF-03/RF-04, baseline completa. | Doze casos após adoção de T12, precedência e motivo conferidos; [Spec 002](../specs/002-heranca-incompatibilidade/), [T12](evidencias-t12.md). |
| 3 — Mudanças e referência | Quatro variantes independentes e referência rastreável. | 48 pares teste × mudança, 60 expectativas com baseline; revisão e resolução de divergências; [Spec 003](../specs/003-mudancas-controladas/). |
| 4 — Preparação e avaliação | Payload permitido, registro original, avaliador separado. | Versões, integridade, fronteira textual, controles sintéticos e notas revisadas; [Spec 004](../specs/004-preparacao-avaliacao-ids/). |
| 5 — Piloto e congelamento | MC-01/MC-03 × quatro condições × duas repetições. | Critérios do [material 05](../materiais/05_PILOTO_E_COLETA.md), revisão do piloto, ajustes e congelamento registrados. Execução e avaliação individual não encerram esses critérios automaticamente. |
| 6 — Coleta principal e análise | Repetições principais autorizadas e análise descritiva. | Integridade, desvios, omissões, excedentes, validade e consistência por mudança/condição, com conclusões limitadas ao recorte. |

As etapas 5 e 6 são pesquisa, sem exigir novas funcionalidades quando a bancada atende ao procedimento. Para r repetições principais, planejar r blocos de quatro mudanças × quatro condições, em ordem aleatorizada registrada: 16r chamadas. r = 5/80 chamadas permanece cenário candidato, não escolha produzida pela organização. Fixar r antes da coleta, sem ajuste por vantagem observada de uma condição.

Evidências e autorizações: [decisões](decisoes.md). Planejamentos antigos e limites temporais permanecem nos próprios documentos e no [histórico](historico/).
