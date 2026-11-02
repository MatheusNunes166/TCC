# Parte 2 — Referência candidata

Pacote 1.0 • 01/11/2026 • **Consultar após registrar os comentários iniciais sobre as notas.**

Referência candidata 0.2: `CANDIDATO_NAO_REVISADO`; revisor e data nulos. A seguir estão expectativas e seleções para revisão, não respostas aprovadas por profissional/orientador. Não fornecer esta parte ao LLM avaliado.

## Como interpretar

As entradas T01–T12, requisitos e dependências estão na Parte 1. Cada variante parte da mesma baseline B. Impacto funcional pode ocorrer em requisito dependente sem edição textual; teste relevante pode preservar sua saída. Exclusão significa não enquadramento na política local, não inutilidade geral do teste ou garantia de ausência de defeito.

Esta parte consolida a candidata existente, sem recalcular conjuntos a partir do código. As justificativas abaixo são transcritas do documento de revisão de 19/10. As afirmações históricas desse documento/JSON sobre variantes ainda não executadas foram superadas pelo fechamento técnico da Spec 003; os originais não foram regravados. A rodada final existente contém 12 expectativas da baseline e 48 das variantes, todas coincidentes com os respectivos observados. Nesta preparação apenas se conferiram esses registros existentes; **não se executou novamente a bancada e isso não aprova a referência cientificamente**.

## Conjuntos candidatos e partições de testes

“Alteração” significa diferença de decisão **ou motivo**. “Preservação relacionada” mantém ambos em teste incluído estruturalmente pela política. Todo selecionado pertence a uma dessas duas categorias, que não se sobrepõem; demais T01–T12 ficam excluídos com justificativas abaixo.

| Mudança | Requisitos impactados | Testes selecionados | Alteração | Preservação relacionada |
|---|---|---|---|---|
| MC-01 | RF-02 | T04, T12 | T04 | T12 |
| MC-02 | RF-04 | T06, T07, T11, T12 | T06, T07, T12 | T11 |
| MC-03 | RF-02, RF-03 | T01, T02, T05, T06, T07, T09, T10, T11 | T02, T05 | T01, T06, T07, T09, T10, T11 |
| MC-04-v2 | RF-03, RF-04 | T05, T07, T08, T10, T12 | T05, T07, T12 | T08, T10 |

As quantidades de selecionados são 2/4/8/5. Não determinam por si dificuldade, economia ou qualidade do modelo. Conjuntos de requisitos e de testes são avaliados separadamente; um não compensa erros no outro.

## Expectativas de decisão/motivo — baseline e variantes

Legenda sem perda do motivo: **P**=`permitir`; **N**=`negar`; **direta**=`permissao_direta`; **herdada**=`permissao_herdada`; **sem**=`sem_permissao`; `estado` e `conflito` mantêm os nomes. Assim, N/sem representa exatamente `negar/sem_permissao`.

| Teste | Baseline B | MC-01 | MC-02 | MC-03 | MC-04-v2 |
|---|---|---|---|---|---|
| T01 | N/estado | N/estado | N/estado | N/estado | N/estado |
| T02 | P/direta | P/direta | P/direta | N/sem | P/direta |
| T03 | N/sem | N/sem | N/sem | N/sem | N/sem |
| T04 | P/direta | N/sem | P/direta | P/direta | P/direta |
| T05 | P/herdada | P/herdada | P/herdada | N/sem | N/sem |
| T06 | N/conflito | N/conflito | P/direta | N/conflito | N/conflito |
| T07 | N/conflito | N/conflito | P/herdada | N/conflito | N/sem |
| T08 | N/sem | N/sem | N/sem | N/sem | N/sem |
| T09 | N/estado | N/estado | N/estado | N/estado | N/estado |
| T10 | N/estado | N/estado | N/estado | N/estado | N/estado |
| T11 | N/estado | N/estado | N/estado | N/estado | N/estado |
| T12 | N/conflito | N/conflito | P/direta | N/conflito | P/direta |

São 60 expectativas candidatas, não 60 resultados de LLM. Observar somente a decisão perderia, por exemplo, a alteração do motivo de T07 em MC-04-v2.

## Justificativas de requisitos, inclusões e exclusões

As quatro explicações de impacto distinguem a regra editada da dependência afetada e justificam também os RFs excluídos. As tabelas cobrem todos os testes, inclusive os não selecionados, sob a mesma política da Parte 1.

### MC-01 — Retirar Auditoria → exportar.

Impacto candidato: **{RF-02}**. A regra editada deixa de produzir exportar como permissão direta de Auditoria (testemunho T04). RF-03 não herda Auditoria e sua expansão/permissão permanece; RF-04 mantém o mesmo par e o mesmo predicado; RF-01 mantém o filtro de estado. Esses três RFs ficam excluídos do conjunto de impacto.

| Teste | Inclusão ou exclusão e justificativa candidata |
|---|---|
| T01 | Excluir: operação visualizar; RF-01 mantém bloqueio |
| T02 | Excluir: visualizar de Consulta continua concedido |
| T03 | Excluir: exportar, mas sem Auditoria efetivo; Consulta continua sem concessão |
| T04 | Incluir — mudança: Auditoria perde a única concessão de exportar |
| T05 | Excluir: visualizar herdado de Consulta não muda |
| T06 | Excluir: visualizar; RF-04 mantém conflito |
| T07 | Excluir: visualizar; herança e conflito permanecem |
| T08 | Excluir: exportar, mas sem Auditoria efetivo; Supervisão já não o herdava |
| T09 | Excluir: visualizar; estado continua prevalecendo |
| T10 | Excluir: visualizar; estado continua prevalecendo |
| T11 | Excluir: visualizar; estado continua prevalecendo sobre conflito |
| T12 | Incluir — preservação: exportar com Auditoria efetivo; RF-04 continua bloqueando apesar da concessão removida em RF-02 |

### MC-02 — Retirar a incompatibilidade Consulta + Auditoria.

Impacto candidato: **{RF-04}**. A regra editada deixa de detectar conflito em T06/T07. RF-03 continua produzindo Consulta efetivo e visualizar herdado; seu uso por T07 não é alteração de seu comportamento. RF-02 preserva as concessões e RF-01 preserva o filtro; ambos ficam excluídos, assim como RF-03.

| Teste | Inclusão ou exclusão e justificativa candidata |
|---|---|
| T01 | Excluir: não contém o par efetivo; RF-01 bloqueia |
| T02 | Excluir: só Consulta; concessão direta intacta |
| T03 | Excluir: só Consulta; exportar continua ausente |
| T04 | Excluir: só Auditoria; concessão direta intacta |
| T05 | Excluir: Supervisão inclui Consulta, mas falta Auditoria; herança intacta |
| T06 | Incluir — mudança: retirado o conflito, RF-02 permite visualizar de Consulta |
| T07 | Incluir — mudança: retirado o conflito, RF-03 permite visualizar herdado de Consulta |
| T08 | Excluir: falta Auditoria efetivo; exportar continua ausente |
| T09 | Excluir: não contém o par; RF-01 bloqueia |
| T10 | Excluir: não contém Auditoria efetivo; RF-01 bloqueia |
| T11 | Incluir — preservação: contém o par, mas RF-01 continua bloqueando antes do conflito removido |
| T12 | Incluir — mudança: contém o par efetivo; sem conflito, RF-02 permite exportar diretamente por Auditoria |

### MC-03 — Retirar Consulta → visualizar.

Impacto candidato: **{RF-02, RF-03}**. Texto editado: RF-02, cuja concessão direta desaparece (T02). Dependência afetada: RF-03 continua incluindo Consulta, mas não produz mais visualizar herdado (T05). RF-04 fica excluído: incompatibilidade depende de papéis, não das permissões que eles concedem; o predicado continua verdadeiro em T06/T07. RF-01 também fica excluído, pois seu filtro não muda.

| Teste | Inclusão ou exclusão e justificativa candidata |
|---|---|
| T01 | Incluir — preservação: visualizar com Consulta efetivo, mas RF-01 bloqueia conta suspensa |
| T02 | Incluir — mudança: RF-02 retira visualizar; não há outra concessão |
| T03 | Excluir: operação exportar; já não concedida a Consulta |
| T04 | Excluir: exportar e ausência de Consulta efetivo; Auditoria mantém concessão |
| T05 | Incluir — mudança: RF-03 mantém o papel Consulta, mas perde visualizar herdado |
| T06 | Incluir — preservação: visualizar com Consulta efetivo; RF-04 ainda bloqueia antes da ausência de permissão |
| T07 | Incluir — preservação: Consulta continua efetivo por RF-03; RF-04 ainda bloqueia |
| T08 | Excluir: operação exportar; Supervisão continua sem concessão |
| T09 | Incluir — preservação: visualizar com Consulta efetivo; RF-01 bloqueia em revisão |
| T10 | Incluir — preservação: visualizar com Consulta efetivo herdado; RF-01 bloqueia |
| T11 | Incluir — preservação: visualizar com Consulta efetivo; RF-01 continua anterior a conflito e permissão |
| T12 | Excluir: operação exportar, não visualizar; RF-03 mantém Consulta efetivo e RF-04 mantém conflito |

### MC-04-v2 — Retirar Supervisão → Consulta da herança.

Impacto candidato: **{RF-03, RF-04}**. Texto editado: RF-03; Supervisão deixa de produzir Consulta efetivo e visualizar herdado (T05/T07). Dependência afetada: o predicado de RF-04 para Supervisão + Auditoria muda de verdadeiro para falso (T07), embora o texto da incompatibilidade continue igual. RF-02 fica excluído: suas concessões próprias continuam iguais; perder uma concessão herdada não modifica a consulta direta dos atribuídos. RF-01 permanece intacto.

| Teste | Inclusão ou exclusão e justificativa candidata |
|---|---|
| T01 | Excluir: sem Supervisão; RF-01 bloqueia |
| T02 | Excluir: sem Supervisão; Consulta mantém visualizar direto |
| T03 | Excluir: sem Supervisão; Consulta continua sem exportar |
| T04 | Excluir: sem Supervisão; Auditoria mantém exportar direto |
| T05 | Incluir — mudança: Supervisão perde Consulta efetivo e visualizar herdado |
| T06 | Excluir: sem Supervisão; Consulta atribuído ainda conflita com Auditoria |
| T07 | Incluir — mudança de motivo: sem Consulta efetivo desaparece o conflito; Auditoria não concede visualizar e Supervisão perdeu a herança |
| T08 | Incluir — preservação: tem Supervisão; nem a versão inicial nem a variante concedem exportar a esse papel isolado |
| T09 | Excluir: sem Supervisão; RF-01 bloqueia |
| T10 | Incluir — preservação: tem Supervisão, mas RF-01 mantém o bloqueio anterior à herança removida |
| T11 | Excluir: sem Supervisão; estado continua anterior ao conflito entre papéis atribuídos |
| T12 | Incluir — mudança: sem Consulta efetivo desaparece o conflito e RF-02 mantém exportar direto de Auditoria |


## Questões para a segunda etapa da revisão

- Os conjuntos de requisitos respeitam a diferença entre editar texto, alterar funcionalmente uma dependência e somente participar da execução? Há RF incluído/excluído sem fundamento?
- As 60 expectativas respeitam estado, conflito, permissão, origem direta/herdada e cada remoção isolada? Justificar divergências por regra e teste, sem assumir que a implementação é a autoridade final.
- Inclusões/exclusões aplicam uniformemente a política estrutural da baseline, inclusive quando estado ou conflito preserva a saída? Essa política é defensável para o objetivo do estudo?
- T12 está corretamente incluído como preservação em MC-01, como alteração em MC-02/MC-04-v2 e excluído em MC-03? A revisão é das expectativas; a adoção de T12 no catálogo já ocorreu.
- Após ver os conjuntos, mudou sua opinião sobre pistas nas notas? Registrar o comentário posterior separado do parecer inicial, citando trecho e resposta que poderia antecipar.

Usar a seção B da [ficha](03-ficha-de-revisao.md). Se discordar, informar expectativa/conjunto proposto e fundamento; não corrigir silenciosamente a fonte. O pesquisador registrará resolução posterior, inclusive divergência mantida ou decisão pendente.

## Fontes e detalhes opcionais

[Referência documental e justificativas integrais](../referencia-candidata-proxima-etapa.md), [JSON candidato 0.2](../../materiais/modelos/referencia_candidata_NAO_ENVIAR_AO_LLM.json), [material 02](../../materiais/02_REQUISITOS_TESTES_E_REFERENCIA.md), [evidências técnicas Spec 003](../../specs/003-mudancas-controladas/evidencias.md), [fechamento offline Spec 004](../../evidencias/spec004/revisao-textual-2026-11-01/relatorio.md). Versões/hashes em [versoes.json](versoes.json). Esses documentos podem conter contexto de desenvolvimento; não integram o pacote destinado ao modelo.
