# Feature Specification: Preparação de entradas e avaliação separada de IDs

> Convenções vigentes — 27/10/2026, D-26/D-27: o pesquisador adotou PONT-01/PONT-02 como convenções técnicas candidatas, ainda sujeitas à revisão científica. Política `ids-proposta-004-v2`: célula base por configuração/mudança/condição; versões de política ou referência distintas impedem resultado combinado, com diagnóstico e grupos separados por versão. Identidade lógica única por configuração/mudança/condição/repetição; duplicidades bloqueiam o resumo afetado sem escolha automática. Tentativas técnicas vinculadas não são repetições. Jaccard somente entre repetições distintas elegíveis, com número de observações/pares; menos de duas: **não calculável**. I1 corrigido: rejeitar links simbólicos internos/externos, junctions e todos os reparse points. Implementação e controles independentes autorizados, sem LLM/piloto. Isolamento real não demonstrado; T014/T015 e dependentes permanecem pendentes. Textos datados de somente planejamento/sem tarefas abaixo são históricos; originais preservados em evidências.

> Complemento de planejamento — 27/10/2026 (D-24/D-25): planejamento autorizado em pedido posterior, sem tarefas ou implementação. Spec 004 selecionada e confirmada antes do setup. [Plano](plan.md), [pesquisa local](research.md), [modelo](data-model.md), [contrato](contracts/preparacao-avaliacao.md) e [guia futuro](quickstart.md) preparados. FR-012, SC-007 e premissas de somente Spec/checklist/seletor 003 abaixo registram o alcance histórico da entrega inicial; o pedido atual os supera somente quanto aos artefatos de planejamento/seleção. Requisitos funcionais, controles, referência e pendências científicas preservados. Nenhum controle, envio, coleta ou piloto executado.

**Feature Directory**: `specs/004-preparacao-avaliacao-ids` (sem criação de branch)

**Created**: 2026-10-27

**Status**: Rascunho revisado documentalmente; somente especificação, sem implementação ou execução.

**Input**: Pedido do pesquisador: registrar a orientação de 21/10, demonstrar a Spec 003 com artefatos existentes e preparar somente Spec 004/checklist para montagem por lista permitida, preservação de entrada/resposta e avaliação de IDs de requisitos e testes com controles sintéticos identificados. D-22/D-23 em [decisões](../../documentacao/decisoes.md).

## User Scenarios & Testing *(mandatory)*

### User Story 1 — Conferir exatamente o que poderá ser enviado (Priority: P1)

Como pesquisador, quero montar uma entrada apenas com documentos explicitamente permitidos, identificando conteúdo e origem, para impedir acesso ao gabarito e ao contexto de desenvolvimento.

**Why this priority**: uma resposta que recebe a referência compromete a avaliação.

**Independent Test**: futuramente, montar entrada local com documentos permitidos e conferir recusa de uma origem não permitida, sem rede ou cliente LLM.

**Acceptance Scenarios**:

1. **Dado** um manifesto revisado, **quando** se montar a entrada de uma mudança/condição, **então** todos os trechos pertencem à lista permitida, com ordem e conteúdo integral verificáveis, sem resultados após a mudança ou conjuntos esperados.
2. **Dado** caminho externo, documento ausente, hash divergente ou conteúdo contaminado, **quando** se solicitar montagem, **então** ela é bloqueada com causa registrada, sem buscar substitutos ou produzir entrada parcial utilizável.
3. **Dadas** D0/D1/E0/E1 candidatas para a mesma mudança, **quando** se confrontarem as entradas, **então** o bloco comum é idêntico, notas só aparecem em D1/E1 com mesmo conteúdo e pedido só varia pela estrutura da condição. Não há histórico de conversa ou recuperação automática.

### User Story 2 — Preservar entrada e resposta originais (Priority: P1)

Como pesquisador, quero ligar a entrada integral a uma resposta original ou falha identificada, permitindo auditoria sem reconstrução por resumos.

**Why this priority**: a interpretação de uma resposta não pode apagar o que foi recebido.

**Independent Test**: futuramente, registrar entrada e importar resposta sintética local, conferindo recuperação integral e integridade antes/depois da avaliação.

**Acceptance Scenarios**:

1. **Dada** resposta sintética identificada, **quando** registrada e avaliada, **então** entrada/resposta integrais permanecem inalteradas; extração, diagnóstico e cálculos ficam em registros derivados vinculados.
2. **Dada** falha técnica sem resposta, **quando** registrada, **então** a resposta fica ausente com causa, sem fabricar JSON vazio ou valores observados.
3. **Dada** tentativa existente, **quando** houver correção do avaliador ou nova tentativa, **então** novo registro referencia o anterior sem sobrescrever arquivos/resultados. Falha de escrita/integridade impede declarar registro completo.

### User Story 3 — Avaliar duas listas sem confundir dimensões (Priority: P2)

Como pesquisador, quero comparar separadamente IDs de requisitos e testes com referência identificada, explicitando acertos, excedentes e omissões.

**Why this priority**: uma dimensão não compensa a outra; formato válido não comprova seleção correta.

**Independent Test**: futuramente, aplicar referência sintética fixa a respostas exata, parcial e vazia, conferindo TP/FP/FN independentemente, sem bancada ou LLM.

**Acceptance Scenarios**:

1. **Dadas** listas dentro do contrato, **quando** avaliadas, **então** ordem não altera resultado, duplicatas são relatadas e contadas uma vez, e RFs/testes têm conjuntos e contagens independentes.
2. **Dado** ID desconhecido, **quando** avaliado, **então** ele permanece explícito como FP único nessa dimensão, sem correção, descarte ou transferência entre listas.
3. **Dadas** listas vazias válidas e referência não vazia, **quando** comparadas, **então** expectativas são omissões; seleção vazia, formato inválido e falha técnica têm estados distintos.
4. **Dada** referência incompleta, vazia ou sem versão, **quando** avaliada, **então** avaliação é bloqueada por erro da referência, sem ajustá-la à resposta.

### User Story 4 — Conferir o avaliador com controles identificados (Priority: P2)

Como pesquisador, quero verificar regras com respostas sintéticas e expectativas declaradas previamente, sem apresentá-las como respostas de modelo.

**Why this priority**: controles verificam engenharia do avaliador, não efeitos experimentais.

**Independent Test**: futuramente, executar S-01–S-16 abaixo, com origem sintética e evidências próprias, sem configurar cliente/provedor/modelo.

**Acceptance Scenarios**:

1. **Dada** a matriz, **quando** executada, **então** cada controle conserva entrada, expectativa independente, observado e conformidade/erro; nenhum entra em contagens de LLM ou nos 48 pares da Spec 003.
2. **Dada** divergência, **quando** investigada, **então** originais são preservados e eventual correção conferida em nova tentativa, sem trocar expectativa pelo observado.

### Edge Cases

- Lista ausente, nulo, número, campo extra, chave JSON repetida, texto/cercas exteriores ou truncamento: formato inválido, sem reparo ou avaliação parcial.
- IDs com caixa/espaços diferentes, aliases, strings vazias ou dimensão errada: desconhecidos; itens não string violam formato; nunca corrigir por aproximação.
- Documento substituído após revisão, caminho/link resolvido fora da raiz ou notas na condição errada: bloquear montagem; nome de pasta não comprova isolamento.
- Resposta inexistente, fragmento técnico, recusa textual ou falha de persistência: preservar o disponível e distinguir causas, sem repetir para melhorar conteúdo.
- Referência com ID desconhecido/duplicado, mudança ausente ou conjunto vazio: erro de referência, sem escores até revisão explícita e versionada.

## Requirements *(mandatory)*

### Functional Requirements

FRs são locais da Spec 004; RF-01–RF-04 continuam sendo regras do sistema de autorização.

- **FR-001 — lista permitida fechada**: montagem futura DEVE ler somente documentos enumerados no manifesto permitido, conforme tabela abaixo, com versão/hash, ordem e condição. Não varrer/indexar o repositório, resolver dependências automaticamente ou incluir arquivos adicionais.
- **FR-002 — separação de acesso**: montador e eventual processo de envio NÃO DEVEM acessar gabarito, histórico de desenvolvimento, contexto do assistente, resultados resolvidos ou ambiente do avaliador. A comprovação futura exige fronteira de acesso efetiva e inspeção integral da entrada; `.gitignore`, nome de pasta ou instrução textual não bastam. O avaliador lê referência separada sem devolvê-la à montagem/envio.
- **FR-003 — bloqueio e revisão**: arquivos ausentes, alterados, externos, não permitidos ou contaminados DEVEM impedir montagem utilizável, com causa registrada. A inspeção abrange conteúdo, não somente nomes/hashes. Lista, recortes e neutralidade precisam de revisão com responsável/data antes de uso experimental.
- **FR-004 — reprodução da entrada**: cada montagem DEVE conservar conteúdo integral ordenado que seria enviado, incluindo instruções, pedido, schema e notas presentes/ausentes, com hash, manifesto, IDs de montagem/mudança/condição e origem dos blocos. Envio futuro deve vincular o conteúdo efetivamente enviado, sem reconstruí-lo de resumos. Nesta etapa não há envio real.
- **FR-005 — resposta bruta e estados**: cada registro DEVE preservar resposta original integral quando disponível, vinculada à entrada e identificada por origem (`sintetica` ou, só em etapa futura, experimental), tentativa, instante e integridade. Transporte, resposta recebida, validade de formato, IDs conhecidos e integridade são estados separados; ausência de resposta não vira JSON vazio.
- **FR-006 — registros derivados**: extração/avaliação DEVEM ser registros derivados com versão de regras e referência/hash. Não modificar entrada, resposta, candidata 0.2, baseline, variantes, testes ou evidências anteriores. Reavaliação/retentativa tem ID novo e vínculo ao anterior; falha de persistência impede atestar completude.
- **FR-007 — formato**: reutilizar [schema_saida.json](../../materiais/modelos/schema_saida.json): objeto JSON com exatamente `requisitos` e `testes`, listas de strings. Sem campos extras, chaves repetidas ou texto exterior. Listas vazias são permitidas. Não consertar texto, cercas, tipos ou IDs. Formato válido não implica pertinência ou acerto.
- **FR-008 — dimensões independentes**: avaliar requisitos e testes em blocos distintos, pelos universos RF-01–RF-04 e T01–T12 e pela mudança exata da referência. Aplicar regras de duplicatas/desconhecidos abaixo. Não inferir uma lista da outra; sem nota combinada ou semelhança textual.
- **FR-009 — comparação auditável**: por dimensão de resposta de formato válido, registrar lista original, conjunto único S, esperado G, acertos S∩G, excedentes S−G, omissões G−S e TP/FP/FN. Ordem não altera resultado. Referência é exclusiva do avaliador, com status científico visível, nunca gerada a partir do observado.
- **FR-010 — regras propostas versionadas**: usar para conferência técnica futura a política e fórmulas candidatas abaixo, identificadas como provisórias. Fundamentação/revisão de precisão, revocação, F1 e consistência permanecem pendentes; aritmética sintética não aprova escolhas científicas.
- **FR-011 — controles separados**: verificar futuramente S-01–S-16 com respostas locais rotuladas, referências sintéticas prévias e registros esperado/observado. Sem LLM, modelo simulado como escolhido, novos testes experimentais T13+ ou soma dos controles à bancada/pesquisa.
- **FR-012 — limites**: entrega atual contém somente Spec/checklist no diretório 004, além de orientação/roteiro/reconciliação documental solicitados. Sem plano, tarefas, montador/avaliador implementado, cliente, chamadas, escolha de modelos, interface/API/repositório novo, semelhança textual ou geração de código como objeto de avaliação. Não libera piloto/coleta.

### Documentos permitidos — proposta de contrato de entrada

Documentos abaixo serão preparados/revisados futuramente: **não foram exportados e não formam pacote aprovado**. Caminhos são relativos à futura raiz de entrada isolada, não ao repositório. Preparação editorial dos recortes ocorre fora do montador; ele recebe somente documentos finais enumerados e manifesto, sem abrir fontes mistas para extrair trechos em tempo de montagem.

| Documento enumerado | Conteúdo permitido e fonte existente a reaproveitar | Condição |
|---|---|---|
| `sistema.txt` | Instrução de usar somente o material recebido, sem ferramentas, retornando o contrato; diretriz de `materiais/04_NOTAS_E_PROMPTS.md`, §4.4. | Todas |
| `definicoes-comuns.md` | Conteúdo integral de `materiais/07_DEFINICOES_COMUNS.md`, após revisão; sem comentários novos ou exemplos resolvidos. | Todas, idêntico |
| `requisitos-baseline.md` | Só RF-01–RF-04, entradas/saídas, política inicial e precedência de `documentacao/requisitos.md`; excluir avisos históricos, status e seção resolvida T12. | Todas, idêntico |
| `catalogo-baseline.md` | Só tabela T01–T12 com entradas/saídas da baseline de `documentacao/qualidade-e-testes.md`; excluir resultados de variantes, seleções e histórico. | Todas, idêntico |
| `mudanca.md` | Uma descrição de remoção da tabela de `specs/003-mudancas-controladas/spec.md`, somente a célula “Única alteração em relação a B”; excluir efeitos, classificação direta/propagada, conjuntos e exemplos. ID no registro externo. | Uma mudança por montagem |
| `notas.md` | Só bloco candidato §4.2 de `materiais/04_NOTAS_E_PROMPTS.md`, após revisão de origem/neutralidade e decisão sobre texto definitivo. | D1/E1, mesmo conteúdo em todas as mudanças; ausente em D0/E0 |
| `pedido.txt` | Só pedido §4.5 ou §4.6 de `materiais/04_NOTAS_E_PROMPTS.md`. | Direto D0/D1; estruturado E0/E1 |
| `schema_saida.json` | Contrato de `materiais/modelos/schema_saida.json`, sem conjuntos esperados. | Todas, idêntico |

Ordem: sistema → definições → requisitos → catálogo → mudança → notas quando previstas → pedido → schema. Manifesto enumera arquivo exato, raiz, hash, versão, ordem e condição; sem curingas, busca recursiva ou links para fora da raiz. Cada montagem usa só documentos aplicáveis; versões alternativas de mudança/pedido são preparadas explicitamente, sem descoberta automática. Schema contém tipos/campos, não referência de seleção.

**Excluídos da montagem/envio:** AGENTS, constituição, estado/decisões/handoff, transcrição/encaminhamentos/roteiro, Specs/planos/tarefas/checklists, `.git`, histórico, scripts/testes/código de desenvolvimento, fontes mistas integrais `materiais/01`–`06`, `referencia-candidata-proxima-etapa.md`, `referencia_candidata_NAO_ENVIAR_AO_LLM.json`, evidências Spec 003, diffs, saídas após mudança, conjuntos esperados e exemplos sintéticos resolvidos. Proveniência citada nesta Spec não autoriza acesso pelo montador. Lista/recortes revisados e isolamento demonstrado são critérios futuros.

### Política candidata de validade, duplicatas e falhas

Reaproveita `materiais/01_PROTOCOLO.md`, §§1.5–1.7, e `materiais/04_NOTAS_E_PROMPTS.md`, §4.7, explicitando distinções sem alterar materiais ou congelar protocolo. **“Formato válido”** e **“somente IDs conhecidos”** são indicadores separados; nunca relatar “válido” sem qualificação.

| Situação | Tratamento proposto | Efeito na avaliação |
|---|---|---|
| Objeto correto com duas listas de strings | Formato válido; avaliar ambas separadamente. | TP/FP/FN por dimensão. |
| Duplicata exata | Preservar lista bruta, registrar ID/posições/repetições; conjunto único. | Não multiplicar TP/FP; ordem indiferente. |
| String desconhecida, inclusive `rf-02`, ` RF-02`, `T4`, vazia ou da outra dimensão | Formato válido; indicador de IDs conhecidos negativo nessa dimensão. Sem trim, caixa, aliases ou transferência. | Cada desconhecido distinto conta uma vez como FP, com lista/quantidade próprias; não removê-lo do denominador. |
| Lista(s) vazia(s) | Seleção vazia deliberada, formato válido. | TP=0, FP=0, FN=\|G\| na dimensão vazia; P/R/F propostos zero com G não vazio. |
| JSON inválido/truncado, campo ausente/extra, tipo errado, chave repetida, explicação/cercas externas | Formato inválido com causa/original preservados; sem reparo ou avaliação parcial. Espaços JSON exteriores permitidos. | Extração e métricas observadas ausentes. Só em resumo operacional separado admite-se zero convencional identificado como imputação, nunca seleção vazia observada. |
| Recusa textual recebida | Preservar resposta fora do formato exigido. | Formato inválido; sem repetir para melhorar conteúdo. |
| Falha de transporte, sem resposta | Falha técnica, erro e ausência explícitos. | Sem seleção/escores observados; fora do resumo válido; informar falhas/planejadas. |
| Falha de transporte com fragmento | Preservar fragmento e estado incompleto; diagnóstico de formato separado. | Não avaliar como resposta concluída, mesmo se fragmento incidentalmente parseável. |
| Retentativa de transporte | Proposta histórica: no máximo uma, só em transporte, conteúdo idêntico, tentativas vinculadas. | Apenas documentada; sem transporte agora; não repetir conteúdo ruim nem escolher melhor resposta. |
| Falha de escrita/hash, referência incompleta/inconsistente ou G vazio | Bloquear por infraestrutura/referência com diagnóstico. | Sem escores; não punir resposta por defeito do avaliador nem completar esperado pelo observado. G vazio exige nova convenção revisada. |

**Denominadores propostos:** mostrar planejadas, concluídas, falhas técnicas, formato válido/inválido e somente IDs conhecidos, com numeradores/denominadores explícitos. Resumo de seleção usa respostas concluídas de formato válido, inclusive desconhecidos penalizados como FP. Eventual resumo operacional com zeros para formato inválido é visão derivada separada, como proposto no material histórico; não substitui resumo válido nem imputa falhas técnicas como seleções vazias. Candidata pode apoiar conferência técnica futura com status explícito, sem presumir revisão científica.

### Medidas candidatas a fundamentar e revisar

Por dimensão: G é o conjunto esperado; S contém strings distintas indicadas, inclusive desconhecidas. TP=\|S∩G\|, FP=\|S−G\|, FN=\|G−S\|. Listas/contagens permitem auditoria independentemente da escolha posterior de métricas.

Propostas existentes: precisão = TP/(TP+FP), revocação = TP/(TP+FN), F1 = 2TP/(2TP+FP+FN). Para S vazio/G não vazio, convenção proposta zero nas três. Não arredondar antes das contagens/cálculos; identificar regra de apresentação. Não pontuar texto explicativo, código, diffs ou semelhança textual; não combinar RFs/testes em escore único.

Consistência de Jaccard = \|Sᵢ∩Sⱼ\|/\|Sᵢ∪Sⱼ\| continua proposta: pares de respostas concluídas de formato válido da mesma mudança/condição, repetições distintas, por dimensão, informando pares elegíveis/usados. Dois conjuntos vazios dão 1 pela convenção candidata, sem significar qualidade: mostrar revocação zero perante G não vazio. Menos de duas respostas elegíveis informa “não calculável”, com valor nulo e observações/pares explícitos. Desconhecidos permanecem no conjunto e são expostos. Não se criam repetições experimentais agora.

São hipóteses operacionais para conferir controles, não fundamentação bibliográfica nova, aprovação do orientador ou protocolo definitivo. Revisão pode exigir nova versão antes de piloto; o avaliador deverá identificar qual versão calculou. Redução de testes/economia de tempo não são critérios de sucesso desta Spec.

### Matriz de controles sintéticos — especificada, não executada

Referência de controle prévia: G_RF={`RF-02`}, G_T={`T04`,`T12`}. Usa IDs existentes para exercitar contrato; não é novo gabarito aprovado nem resposta LLM. Origem obrigatória `sintetica`, IDs S-xx, sem modelo reportado, fase piloto ou contagem experimental. Exemplos pertencem só à avaliação, nunca ao pacote permitido. P/R/F são precisão/revocação/F1 **propostas**.

| Controle | Resposta/variação artificial | Expectativa para verificação futura |
|---|---|---|
| S-01 exata | `{"requisitos":["RF-02"],"testes":["T04","T12"]}` | RF TP/FP/FN=1/0/0; testes=2/0/0; P/R/F=1 em ambos. |
| S-02 parcial | RF-02; testes só T04 | RF=1/0/0; testes=1/0/1, P=1, R=1/2, F=2/3. |
| S-03 todos | Quatro RFs e doze testes | RF=1/3/0, P=1/4, R=1, F=2/5; testes=2/10/0, P=1/6, R=1, F=2/7. |
| S-04 vazias | Ambas `[]` | Formato válido; RF=0/0/1; testes=0/0/2; escores propostos zero. |
| S-05 duplicadas/ordem | RF-02 repetido; T12,T04,T04 | Conjuntos/contagens de S-01; duplicatas/posições registradas. |
| S-06 desconhecidos | RF-02,RF-99,RF-99; T04,T12,T99,T99 | RF=1/1/0; testes=2/1/0; um desconhecido único por dimensão, repetições registradas. |
| S-07 sem normalizar | `rf-02`; `T4` | Formato válido, desconhecidos; RF=0/1/1; testes=0/1/2; sem aproximação. |
| S-08 trocadas | Requisitos=[T04]; testes=[RF-02] | RF=0/1/1; testes=0/1/2; sem mover IDs. |
| S-09 formato inválido | Subcasos: chave ausente, extra, lista nula, item numérico, chave repetida, texto/cercas, JSON truncado | Cada subcaso preservado/identificado; formato inválido; nenhuma dimensão pontuada. |
| S-10 independência | Requisitos=[]; testes=[T04,T12] | RF omite tudo, testes exatos; não compensar nem invalidar lista vazia. |
| S-11 falha técnica | Sem resposta; outro subcaso com fragmento incompleto | Erro registrado, sem seleção, métrica ou resposta fabricada. |
| S-12 referência defeituosa | Subcasos: G vazio, mudança ausente, ID esperado duplicado/desconhecido | Bloquear por referência; não alterar candidata original. |
| S-13 integridade | Subcasos: entrada/resposta alterada, escrita incompleta, tentativa repetida | Detectar erro, impedir fechamento completo, preservar originais; nova tentativa tem ID/vínculo próprios. |
| S-14 montagem/isolamento | Subcasos: arquivo extra, caminho externo ou link interno/externo, junction/reparse point, hash diferente, gabarito no conteúdo, notas na condição errada | Bloquear cada caso; montagem íntegra/revisada é controle positivo. Usar arquivos fictícios marcados nos controles negativos, sem dar acesso real à referência. |
| S-15 consistência | S-01 × S-02; S-04 × S-04 de repetições sintéticas distintas; par com inválida; só uma elegível | Jaccard RF=1/testes=1/2 no primeiro; 1/1 no vazio, com omissões expostas; inválida excluída com denominador; uma elegível dá indisponível. |
| S-16 resumo/retentativa | Uma exata, uma inválida, uma falha técnica; simular transporte e uma retentativa vinculada com mesmo payload | Denominadores explícitos; resumo válido só exata; operacional distingue zero imputado e falha sem escore; tentativas não viram repetições adicionais. |

Fechamento futuro exige todos os subcasos, com logs e divergências preservadas. Nenhum controle foi executado ao escrever esta especificação.

### Key Entities

- **Manifesto permitido**: lista fechada, versões/hashes, ordem, condições e revisão, sem gabarito.
- **Entrada integral**: conteúdo que seria/foi enviado, mudança/condição e manifesto.
- **Tentativa/resposta bruta**: identidade/origem, entrada, original ou ausência/fragmento, estados técnicos e integridade.
- **Referência de avaliação**: mudança, G_RF/G_T, universos, versão/hash e revisão, só no avaliador.
- **Avaliação derivada**: versão de regras, validade/diagnóstico, listas/conjuntos, TP/FP/FN e métricas provisórias separadas.
- **Controle sintético**: S-xx, expectativa prévia, observado futuro, conformidade/erro e evidência separada da pesquisa.

## Success Criteria *(mandatory)*

### Measurable Outcomes

Metas futuras, não resultados realizados:

- **SC-001**: 100% dos blocos de cada entrada têm origem permitida/revisada; todos os subcasos não permitidos S-14 são recusados, com evidência de ausência de acesso ao gabarito/histórico (FR-001–FR-003).
- **SC-002**: 100% das entradas/respostas disponíveis são recuperáveis integralmente com integridade/vínculo conferidos; nenhuma tentativa sobrescrita; ausências/fragmentos/erros explícitos (FR-004–FR-006, S-11/S-13).
- **SC-003**: S-01–S-10 produzem estados/contagens previstos, por dimensão, sem correção de IDs ou dupla contagem (FR-007–FR-009).
- **SC-004**: S-11–S-13/S-16 distinguem falha técnica, formato inválido, seleção vazia e referência/integridade defeituosa; sem seleção inventada; resumos expõem denominadores/imputações (FR-005/FR-006/FR-010).
- **SC-005**: cálculos propostos S-01–S-06/S-15 são auditáveis, com convenções/versão provisória; sem escore combinado, semelhança textual ou validação científica atribuída (FR-008–FR-010).
- **SC-006**: 16/16 controles e seus subcasos têm origem sintética, expectativa prévia e evidências próprias no fechamento futuro; zero contabilizados como LLM, piloto ou pares Spec 003 (FR-011).
- **SC-007**: nesta entrega, diretório 004 contém exatamente `spec.md` e `checklists/requirements.md`; nenhuma implementação, chamada ou pesquisa declarada realizada; pendências/limites rastreáveis (FR-012).

## Assumptions

- **Autorização em 27/10/2026:** pedido atual, D-22, somente documentação da orientação, roteiro, Spec/checklist e reconciliação. Sem plano/tarefas/implementação/execução do avaliador. `.specify/feature.json` continua em 003; selecionar 004 cabe ao planejamento autorizado posterior.
- **Reaproveitamento:** [arquitetura](../../documentacao/arquitetura.md), [protocolo](../../materiais/01_PROTOCOLO.md), [prompts/notas](../../materiais/04_NOTAS_E_PROMPTS.md), schema e [modelo de registro](../../materiais/modelos/registro_execucao.json) orientam contratos futuros, sem alterações agora. Persistência e mecanismo de isolamento pertencem ao planejamento posterior.
- **Base preservada:** D-20/D-21, B `aec474bcb54d6dae2afceff8e5b9226991386490`, candidata 0.2 `CANDIDATO_NAO_REVISADO`, 12 testes, 48 expectativas de variantes, seleções 2/4/8/5. MC-04=MC-04-v2. Concordância técnica 48/48 não revisa cientificamente conjuntos/política/notas. JSONs da Spec 003 não são respostas LLM.
- **Regras candidatas:** detalhamento de chaves repetidas, IDs não normalizados e G não vazio explicita a política anterior; não revoga materiais silenciosamente. Revisão de convenção exige decisão/nova versão antes do uso. Zero para inválidas é só imputação no resumo operacional separado, nunca extração observada.
- **Pendências:** P-01/P-02: revisão científica/profissional da referência/política e expectativas T12, conteúdo definitivo/origem/neutralidade das notas/prompts, fundamentação/revisão de precisão/revocação/F1/consistência, com responsáveis/datas a combinar. P-03: desenho final do piloto, condições, repetições, configuração/orçamento e congelamento. Sem modelo escolhido/chamado. Adoção formal da constituição pendente.
- **Demonstração e pesquisa:** MC-01/MC-04 são exemplos do [roteiro](../../documentacao/roteiro-demonstracao-spec003.md), sem decidir piloto. Exportação permitida e isolamento precisam de implementação/verificação/revisão próprias; documentação não libera experimento.

Fonte da orientação e classificação de pedidos/sugestões/decisões abertas: [encaminhamentos](../../documentacao/encaminhamentos-orientacao-21-10-2026.md). Esta Spec contém exemplos resolvidos e é excluída do contexto do LLM avaliado.

## Estado técnico parcial — 27/10/2026

Implementados `montagem_entradas.py` e `avaliacao_ids.py`, sem rede/provedor. Convenções D-26 candidatas, política ids-proposta-004-v2; 39 tarefas independentes concluídas. T014/T015 e T042–T048 pendentes: runner isolado não provisionado e criação de symlink real negada com WinError1314. Não há fechamento integral. [Evidências e limites](../../evidencias/spec004/revisao-parcial/relatorio.md). As descrições anteriores datadas de planejamento/comandos futuros são históricas; comandos locais agora existentes só preparam/avaliam arquivos sintéticos, sem envio ou piloto. Métricas, notas definitivas, referência e desenho científico continuam sujeitos à revisão. Checklist de qualidade preservada, sem remarcação.

