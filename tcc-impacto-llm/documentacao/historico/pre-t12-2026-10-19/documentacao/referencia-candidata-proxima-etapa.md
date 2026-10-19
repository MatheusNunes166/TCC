# Referência candidata para revisão da próxima etapa científica

Data: 19/10/2026. Versão documental: candidata 0.1. Preparação: assistente, por solicitação do pesquisador nesta conversa. Revisor humano e data de revisão: pendentes. **Não é gabarito aprovado nem autorização para implementar variantes ou executar piloto. Não fornecer este documento ao LLM avaliado.**

## Escopo, governança e fontes

Esta entrega reúne em um único documento as expectativas das quatro mudanças e a análise condicional de T12. Catálogo T01–T11, materiais, referência JSON e código permanecem preservados. Não foram implementadas variantes, executados testes ou iniciadas chamadas ao LLM experimental nesta preparação.

A leitura de [AGENTS.md](../AGENTS.md), da [constituição](../.specify/memory/constitution.md), do [estado](../ESTADO_ATUAL.md), dos [bloqueios](../BLOQUEIOS.md) e do [handoff](../HANDOFF.md) estabelece a distinção entre autorização de engenharia e aprovação científica. D-13/D-14 em [decisões](decisoes.md) registram a implementação da baseline completa em 18/10; avisos anteriores de implementação parcial são históricos. A aba da Spec 001 não redefine a Spec ativa 002. A constituição continua sem adoção formal registrada.

As expectativas abaixo são deduzidas de [requisitos](requisitos.md), do [protocolo, §§1.2 e 1.4](../materiais/01_PROTOCOLO.md) e do [material de referência, §§2.1–2.5](../materiais/02_REQUISITOS_TESTES_E_REFERENCIA.md). O catálogo vem de [qualidade e testes](qualidade-e-testes.md). Os conjuntos foram confrontados documentalmente com a [referência JSON existente](../materiais/modelos/referencia_candidata_NAO_ENVIAR_AO_LLM.json), sem modificá-la. Código e execução futura servem à conferência adicional: eventual divergência deverá ser resolvida pelas regras e pela revisão humana, sem tomar a implementação como única fonte do gabarito.

P-01/P-02/P-03/P-04 continuam pendentes no alcance registrado em decisões. O recorte aceito em D-09 não valida estas expectativas. Esta preparação cobre a parte documental da etapa 3 do [roadmap](roadmap.md), sem concluir seus critérios de passagem. Para manter a entrega em um único documento, o estado desta preparação e a próxima ação estão registrados aqui; os demais documentos não foram atualizados.

## Versão inicial comum e quatro mudanças independentes

A versão inicial B tem as seguintes regras:

- RF-01: somente conta ativa prossegue; suspensa e em revisão retornam `negar/estado`.
- RF-02: Consulta concede visualizar; Auditoria concede exportar; Supervisão não concede permissão própria. Permissões diretas são obtidas dos papéis atribuídos.
- RF-03: Supervisão inclui Consulta como papel efetivo e herda visualizar, em um nível; não herda exportar.
- RF-04: Consulta + Auditoria efetivos são incompatíveis, inclusive quando Consulta vem da herança.

A ordem contratual é estado → conflito → decisão pela permissão; ausência resulta em `negar/sem_permissao`. Se houver concessão direta e herdada da mesma operação, prevalece o motivo `permissao_direta`. Uma concessão não supera estado ou conflito.

| Mudança | Derivação independente | Única alteração | Classificação candidata |
|---|---|---|---|
| MC-01 | B → B com MC-01 | Retirar Auditoria → exportar de RF-02 | Direta |
| MC-02 | B → B com MC-02 | Retirar a incompatibilidade Consulta + Auditoria de RF-04 | Direta |
| MC-03 | B → B com MC-03 | Retirar Consulta → visualizar de RF-02 | Propagada |
| MC-04-v2 | B → B com MC-04-v2 | Retirar Supervisão → Consulta de RF-03 | Propagada |

Nenhuma linha parte da variante anterior. Em MC-04-v2, Auditoria ainda concede exportar e Consulta ainda concede visualizar; em MC-03, a relação de herança e a incompatibilidade permanecem. MC-04-v2 é a alternativa candidata usada nesta análise; a antiga proposta de liberar contas em revisão não é uma quinta mudança nem é combinada com ela. Sua escolha científica ainda precisa ser registrada.

## Critério de impacto e critério de seleção

**Alteração textual** identifica o RF cuja regra é editada. **Impacto funcional por dependência** identifica outro RF cujo valor funcional produzido muda em pelo menos um cenário válido da suíte, mesmo com texto preservado. Consideram-se valores de permissões diretas, permissões herdadas, papéis efetivos e predicado de incompatibilidade, além da saída final. Compartilhar um teste ou servir de pré-condição não basta para declarar impacto.

Exemplos: em MC-03, muda a concessão de RF-02 e, por dependência, a permissão herdada produzida por RF-03 em T05. Em MC-04-v2, muda a expansão de RF-03 e o predicado de RF-04 em T07 passa de verdadeiro a falso. Em MC-02, T07 usa herança, mas a expansão permanece idêntica: isso não inclui RF-03 no impacto.

**Mudança de comportamento de teste** significa alteração de decisão ou motivo. **Preservação relacionada** significa resultado completo idêntico em um teste incluído pela política, inclusive se estado ou conflito impedirem alcançar a permissão modificada. Teste não selecionado também pode manter a saída, mas não integra a categoria de preservação selecionada.

A política conservadora de seleção é a mesma nas quatro mudanças, aplicada estruturalmente com os papéis efetivos de B:

1. Permissão: incluir se a operação é a alterada e os papéis efetivos de B contêm o papel cuja concessão mudou.
2. Incompatibilidade: incluir se os papéis efetivos de B contêm o par alterado, qualquer que seja o estado.
3. Herança: incluir se os papéis atribuídos contêm o filho Supervisão da relação alterada, qualquer que seja a operação ou o estado.

Por isso RF-01 não é impactado, mas testes bloqueados por estado podem ser relevantes. Não recalcular a aplicabilidade usando a variante: isso excluiria justamente dependências removidas. Os conjuntos não pretendem ser mínimos nem garantir detecção de todos os defeitos; exclusão significa somente não enquadramento nesta política.

## Catálogo preservado e expectativas da versão inicial

Nas tabelas, `P` = `permitir`, `N` = `negar`, `direta` = `permissao_direta`, `herdada` = `permissao_herdada`, `sem` = `sem_permissao`. Cada célula sempre apresenta decisão/motivo.

| Teste | Estado | Papéis atribuídos | Operação | B | Fundamentação |
|---|---|---|---|---|---|
| T01 | suspensa | Consulta | visualizar | N/estado | RF-01 precede a concessão de RF-02 |
| T02 | ativa | Consulta | visualizar | P/direta | RF-02 concede; não há conflito |
| T03 | ativa | Consulta | exportar | N/sem | RF-02 não concede exportar a Consulta |
| T04 | ativa | Auditoria | exportar | P/direta | RF-02 concede; não há conflito |
| T05 | ativa | Supervisão | visualizar | P/herdada | RF-03 inclui Consulta e herda sua concessão |
| T06 | ativa | Consulta + Auditoria | visualizar | N/conflito | RF-04 supera a concessão direta |
| T07 | ativa | Supervisão + Auditoria | visualizar | N/conflito | RF-03 inclui Consulta; RF-04 supera a concessão herdada |
| T08 | ativa | Supervisão | exportar | N/sem | RF-02/RF-03 não concedem exportar a Supervisão |
| T09 | em_revisao | Consulta | visualizar | N/estado | RF-01 precede a concessão direta |
| T10 | em_revisao | Supervisão | visualizar | N/estado | RF-01 precede a concessão herdada |
| T11 | em_revisao | Consulta + Auditoria | visualizar | N/estado | RF-01 precede inclusive RF-04 |

## MC-01 — retirar Auditoria → exportar

Impacto candidato: **{RF-02}**. A regra editada deixa de produzir exportar como permissão direta de Auditoria (testemunho T04). RF-03 não herda Auditoria e sua expansão/permissão permanece; RF-04 mantém o mesmo par e o mesmo predicado; RF-01 mantém o filtro de estado. Esses três RFs ficam excluídos do conjunto de impacto.

| Teste | Esperado após MC-01 | Seleção e justificativa |
|---|---|---|
| T01 | N/estado | Excluir: operação visualizar; RF-01 mantém bloqueio |
| T02 | P/direta | Excluir: visualizar de Consulta continua concedido |
| T03 | N/sem | Excluir: exportar, mas sem Auditoria efetivo; Consulta continua sem concessão |
| T04 | N/sem | Incluir — mudança: Auditoria perde a única concessão de exportar |
| T05 | P/herdada | Excluir: visualizar herdado de Consulta não muda |
| T06 | N/conflito | Excluir: visualizar; RF-04 mantém conflito |
| T07 | N/conflito | Excluir: visualizar; herança e conflito permanecem |
| T08 | N/sem | Excluir: exportar, mas sem Auditoria efetivo; Supervisão já não o herdava |
| T09 | N/estado | Excluir: visualizar; estado continua prevalecendo |
| T10 | N/estado | Excluir: visualizar; estado continua prevalecendo |
| T11 | N/estado | Excluir: visualizar; estado continua prevalecendo sobre conflito |

Regressão candidata: **{T04}**; mudança: **{T04}**; preservação relacionada selecionada: **∅**. O catálogo atual não tem outro caso que combine exportar com Auditoria efetivo. Não se acrescentam controles arbitrários para preencher essa lacuna.

## MC-02 — retirar incompatibilidade Consulta + Auditoria

Impacto candidato: **{RF-04}**. A regra editada deixa de detectar conflito em T06/T07. RF-03 continua produzindo Consulta efetivo e visualizar herdado; seu uso por T07 não é alteração de seu comportamento. RF-02 preserva as concessões e RF-01 preserva o filtro; ambos ficam excluídos, assim como RF-03.

| Teste | Esperado após MC-02 | Seleção e justificativa |
|---|---|---|
| T01 | N/estado | Excluir: não contém o par efetivo; RF-01 bloqueia |
| T02 | P/direta | Excluir: só Consulta; concessão direta intacta |
| T03 | N/sem | Excluir: só Consulta; exportar continua ausente |
| T04 | P/direta | Excluir: só Auditoria; concessão direta intacta |
| T05 | P/herdada | Excluir: Supervisão inclui Consulta, mas falta Auditoria; herança intacta |
| T06 | P/direta | Incluir — mudança: retirado o conflito, RF-02 permite visualizar de Consulta |
| T07 | P/herdada | Incluir — mudança: retirado o conflito, RF-03 permite visualizar herdado de Consulta |
| T08 | N/sem | Excluir: falta Auditoria efetivo; exportar continua ausente |
| T09 | N/estado | Excluir: não contém o par; RF-01 bloqueia |
| T10 | N/estado | Excluir: não contém Auditoria efetivo; RF-01 bloqueia |
| T11 | N/estado | Incluir — preservação: contém o par, mas RF-01 continua bloqueando antes do conflito removido |

Regressão candidata: **{T06, T07, T11}**; mudança: **{T06, T07}**; preservação relacionada: **{T11}**. A operação não restringe seleção por incompatibilidade; a exclusão dos demais decorre da ausência do par efetivo, não do estado.

## MC-03 — retirar Consulta → visualizar

Impacto candidato: **{RF-02, RF-03}**. Texto editado: RF-02, cuja concessão direta desaparece (T02). Dependência afetada: RF-03 continua incluindo Consulta, mas não produz mais visualizar herdado (T05). RF-04 fica excluído: incompatibilidade depende de papéis, não das permissões que eles concedem; o predicado continua verdadeiro em T06/T07. RF-01 também fica excluído, pois seu filtro não muda.

| Teste | Esperado após MC-03 | Seleção e justificativa |
|---|---|---|
| T01 | N/estado | Incluir — preservação: visualizar com Consulta efetivo, mas RF-01 bloqueia conta suspensa |
| T02 | N/sem | Incluir — mudança: RF-02 retira visualizar; não há outra concessão |
| T03 | N/sem | Excluir: operação exportar; já não concedida a Consulta |
| T04 | P/direta | Excluir: exportar e ausência de Consulta efetivo; Auditoria mantém concessão |
| T05 | N/sem | Incluir — mudança: RF-03 mantém o papel Consulta, mas perde visualizar herdado |
| T06 | N/conflito | Incluir — preservação: visualizar com Consulta efetivo; RF-04 ainda bloqueia antes da ausência de permissão |
| T07 | N/conflito | Incluir — preservação: Consulta continua efetivo por RF-03; RF-04 ainda bloqueia |
| T08 | N/sem | Excluir: operação exportar; Supervisão continua sem concessão |
| T09 | N/estado | Incluir — preservação: visualizar com Consulta efetivo; RF-01 bloqueia em revisão |
| T10 | N/estado | Incluir — preservação: visualizar com Consulta efetivo herdado; RF-01 bloqueia |
| T11 | N/estado | Incluir — preservação: visualizar com Consulta efetivo; RF-01 continua anterior a conflito e permissão |

Regressão candidata: **{T01, T02, T05, T06, T07, T09, T10, T11}**; mudança: **{T02, T05}**; preservação relacionada: **{T01, T06, T07, T09, T10, T11}**. Os seis casos preservados entram estruturalmente, mesmo sem alcançar a concessão removida na execução.

## MC-04-v2 — retirar Supervisão → Consulta

Impacto candidato: **{RF-03, RF-04}**. Texto editado: RF-03; Supervisão deixa de produzir Consulta efetivo e visualizar herdado (T05/T07). Dependência afetada: o predicado de RF-04 para Supervisão + Auditoria muda de verdadeiro para falso (T07), embora o texto da incompatibilidade continue igual. RF-02 fica excluído: suas concessões próprias continuam iguais; perder uma concessão herdada não modifica a consulta direta dos atribuídos. RF-01 permanece intacto.

| Teste | Esperado após MC-04-v2 | Seleção e justificativa |
|---|---|---|
| T01 | N/estado | Excluir: sem Supervisão; RF-01 bloqueia |
| T02 | P/direta | Excluir: sem Supervisão; Consulta mantém visualizar direto |
| T03 | N/sem | Excluir: sem Supervisão; Consulta continua sem exportar |
| T04 | P/direta | Excluir: sem Supervisão; Auditoria mantém exportar direto |
| T05 | N/sem | Incluir — mudança: Supervisão perde Consulta efetivo e visualizar herdado |
| T06 | N/conflito | Excluir: sem Supervisão; Consulta atribuído ainda conflita com Auditoria |
| T07 | N/sem | Incluir — mudança de motivo: sem Consulta efetivo desaparece o conflito; Auditoria não concede visualizar e Supervisão perdeu a herança |
| T08 | N/sem | Incluir — preservação: tem Supervisão; nem a versão inicial nem a variante concedem exportar a esse papel isolado |
| T09 | N/estado | Excluir: sem Supervisão; RF-01 bloqueia |
| T10 | N/estado | Incluir — preservação: tem Supervisão, mas RF-01 mantém o bloqueio anterior à herança removida |
| T11 | N/estado | Excluir: sem Supervisão; estado continua anterior ao conflito entre papéis atribuídos |

Regressão candidata: **{T05, T07, T08, T10}**; mudança: **{T05, T07}**; preservação relacionada: **{T08, T10}**. T07 é mudança observável mesmo mantendo `negar`: seu motivo passa de `conflito` a `sem_permissao`. Exigir mudança de decisão para incluir RF-04 ou T07 contrariaria o contrato decisão + motivo.

## Proposta T12 — análise separada, sem adoção

Entrada proposta: **conta ativa, Supervisão + Auditoria, operação exportar**. Em B, RF-03 inclui Consulta efetivo; RF-04 nega por conflito, apesar da concessão direta de Auditoria. Resultado candidato de B: **negar/conflito**.

| Mudança independente | Resultado esperado de T12 | Seleção condicional | Dedução pelos requisitos |
|---|---|---|---|
| MC-01 | N/conflito | Incluir — preservação | Exportar com Auditoria efetivo enquadra a permissão alterada. RF-02 perde a concessão, mas RF-03 mantém Consulta efetivo e RF-04 mantém o conflito, que prevalece |
| MC-02 | P/direta | Incluir — mudança | O par efetivo enquadra a incompatibilidade retirada. Sem conflito, RF-02 concede exportar por Auditoria atribuído; RF-03 não concede exportar |
| MC-03 | N/conflito | Excluir | A operação é exportar, não visualizar. RF-03 mantém Consulta efetivo, RF-04 mantém conflito e a concessão de exportar de Auditoria não muda |
| MC-04-v2 | P/direta | Incluir — mudança | Tem Supervisão. RF-03 deixa de incluir Consulta; RF-04 deixa de detectar conflito. RF-02 conserva exportar direto de Auditoria, agora liberado |

T12 contribuiria com um caso de preservação sob conflito em MC-01, hoje sem preservação selecionada, e com uma liberação direta após retirar o conflito em MC-02. Em MC-04-v2, tornaria visível na decisão final a consequência da dependência RF-03 → RF-04: `negar/conflito` → `permitir/permissao_direta`. Complementa T07, que observa essa dependência pela mudança de motivo, e T05, que observa a perda de acesso herdado. Não cria um RF impactado novo nem substitui esses casos. Sua exclusão em MC-03 preserva a aplicação uniforme da política por operação.

Se T12 for adotado após revisão, os conjuntos ficariam:

| Mudança | Regressão condicional | Mudança de comportamento | Preservação relacionada |
|---|---|---|---|
| MC-01 | T04, T12 | T04 | T12 |
| MC-02 | T06, T07, T11, T12 | T06, T07, T12 | T11 |
| MC-03 | T01, T02, T05, T06, T07, T09, T10, T11 | T02, T05 | T01, T06, T07, T09, T10, T11 |
| MC-04-v2 | T05, T07, T08, T10, T12 | T05, T07, T12 | T08, T10 |

Os conjuntos de RFs permaneceriam {RF-02}, {RF-04}, {RF-02, RF-03} e {RF-03, RF-04}. As quantidades de testes relevantes passariam de 1/3/8/4 para 2/4/8/5. Isso altera a composição e comparabilidade das mudanças; não permite concluir que uma classe de mudança é intrinsecamente mais difícil.

A eventual adoção exigiria, em etapa própria:

1. Registrar decisão P-04 com responsável, data, justificativa, revisão humana e alcance em decisões; registrar também a escolha de MC-04-v2 e o critério funcional de impacto.
2. Versionar o catálogo de 11 para 12 testes e a matriz de 44 para 48 pares teste × mudança, incluindo B e as quatro expectativas de T12. Atualizar a referência JSON, conjuntos e justificativas somente após aprovação; preservar a versão anterior.
3. Harmonizar requisitos/testes documentados, materiais, pacote comum T01–T12, prompts, schemas ou validadores que restrinjam IDs, exemplos e avaliador. Revisar as notas quanto a consistência e ausência de pistas; T12 e suas respostas não devem ser introduzidos nas notas. Manter o mesmo catálogo em todas as condições.
4. Recalcular TP/FP/FN e medidas para os conjuntos novos quando houver dados. Precisão e revocação continuam usando seus denominadores próprios; a fração selecionada e a redução nominal passam a usar 12. Para seleção exata, as reduções seriam 83,33%, 66,67%, 33,33% e 58,33%, respectivamente, em vez de 90,91%, 72,73%, 27,27% e 63,64%. São cálculos da referência, não resultados experimentais; sua interpretação favorável continua condicionada à validade, completude e ausência de IDs inexistentes.
5. Conferir futuramente baseline e variantes contra expectativas humanas, incluindo T12, mediante autorização de implementação/verificação. Não confundir evidências atuais de T01–T11 com execução de T12.
6. Atualizar versões/hashes, manifesto e critérios de revisão antes do congelamento. T12 não muda por si o número de chamadas: permanecem quatro mudanças × quatro condições × r repetições, isto é, 16r, com r ainda a definir; o piloto de 16 chamadas continua apenas proposto. Reavaliar extensão do pacote e viabilidade antes de executar.

Nenhum desses ajustes foi aplicado nesta entrega. T12 permanece proposta fora do catálogo e do gabarito existentes.

## Conferência documental, pendências e próxima ação

As quatro tabelas cobrem 11 testes cada (44 expectativas) e coincidem com a matriz candidata do material 02. Os conjuntos e suas partições de mudança/preservação coincidem com o JSON existente: 1, 3, 8 e 4 casos selecionados. Cada teste selecionado pertence a exatamente uma dessas duas categorias; cada exclusão foi justificada pela mesma política. T12 foi analisado apenas de modo condicional nas quatro mudanças. Esta é uma conferência documental, sem execução de software ou validação científica concluída.

Para a revisão humana, registrar neste documento ou no registro central, quando autorizado: revisor, data, versão examinada, concordâncias, divergências, fundamento nos RFs e resolução. Permanecem por confirmar o critério funcional em vez de apenas textual, a seleção conservadora com preservação, a escolha de MC-04-v2, as 44 expectativas e a adoção ou rejeição de T12. Até lá, todas são referências candidatas.

A próxima ação é a revisão humana deste documento. Implementação das variantes e conferência executável constituem trabalho posterior; piloto e coleta continuam dependentes dos critérios de [piloto/coleta](../materiais/05_PILOTO_E_COLETA.md), da separação de contextos de [arquitetura](arquitetura.md) e da revisão de [notas/prompts](../materiais/04_NOTAS_E_PROMPTS.md). Nenhuma dessas etapas está liberada por esta preparação.
