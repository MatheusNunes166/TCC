# Fechamento analítico da extensão 0.3

11/11/2026, D-44. Análise offline das 64 observações já executadas; conformidade humana ainda pendente. Este complemento concentra a análise solicitada e a síntese para o TCC. O [relatório descritivo D-43](../avaliados/extensao-real-0.3-001-avaliacao-001/RELATORIO.md), suas tabelas e seu manifesto permanecem literais, inclusive os hashes. Não foram criadas novas avaliações ou outra ficha de revisão.

## Conferência das quatro divergências

As respostas abaixo foram lidas em `captura/extensao-real-0.3-001/<ID>/T01/resposta.bin`, confrontadas com o texto extraído do respectivo `resposta-http.bin`, com `resposta-original.bin` da avaliação e com os [conjuntos avaliados](../avaliados/extensao-real-0.3-001-avaliacao-001/divergencias-ids.json). Os quatro originais contêm somente as listas JSON; não fornecem justificativas para a seleção.

| Observação | Requisitos no original | Testes no original |
|---|---|---|
| [EXT03-MC-02-D0-SOL-R02](../captura/extensao-real-0.3-001/EXT03-MC-02-D0-SOL-R02/T01/resposta.bin) | RF-02, RF-03, RF-04 | T06, T07, T11, T12, T14, T15 |
| [EXT03-MC-02-E0-SOL-R01](../captura/extensao-real-0.3-001/EXT03-MC-02-E0-SOL-R01/T01/resposta.bin) | RF-02, RF-03, RF-04 | T06, T07, T11, T12, T14, T15 |
| [EXT03-MC-02-E0-SOL-R02](../captura/extensao-real-0.3-001/EXT03-MC-02-E0-SOL-R02/T01/resposta.bin) | RF-02, RF-03, RF-04 | T06, T07, T11, T12, T14, T15 |
| [EXT03-MC-02-E1-SOL-R01](../captura/extensao-real-0.3-001/EXT03-MC-02-E1-SOL-R01/T01/resposta.bin) | RF-02, RF-03, RF-04 | T06, T07, T11, T12, T14, T15 |

A mudança enviada foi “Retirar incompatibilidade Consulta + Auditoria de RF-04”. A [definição comum](../materiais/07_DEFINICOES_COMUNS.md), conferida também nos pacotes efetivamente enviados, inclui a regra diretamente alterada ou a dependente cujo **próprio valor funcional produzido** muda em algum cenário válido. Considera permissões diretas, permissões herdadas, papéis efetivos e predicado de incompatibilidade, além da saída final. Compartilhar um teste ou funcionar como pré-condição é insuficiente.

| Regra | Comparação baseline → MC-02 | Consequência pelo critério utilizado |
|---|---|---|
| RF-04 | A restrição Consulta + Auditoria é retirada; o predicado deixa de bloquear o par efetivo. | Diretamente impactado: integra G = {RF-04}. |
| RF-02 | Consulta continua concedendo visualizar; Auditoria continua concedendo exportar; Supervisão continua sem concessão direta própria. | Nenhuma permissão direta produzida muda: RF-02 é excedente. |
| RF-03 | Supervisão continua incluindo Consulta como papel efetivo e herdando visualizar; não passa a herdar exportar. | Expansão, papéis efetivos e permissões herdadas permanecem iguais: RF-03 é excedente. |

Por exemplo, T06 passa de `negar/conflito` a `permitir/permissao_direta`, e T07 a `permitir/permissao_herdada`; T12 e T14 passam a `permitir/permissao_direta`. Isso libera concessões que já existiam, sem alterar o que RF-02 ou RF-03 produz. A dependência relevante vai das permissões/expansão para a decisão final e o conflito; remover o bloqueio não propaga uma alteração de volta às concessões ou à herança. RF-01 mantém o filtro de estado.

A [referência candidata 0.3](referencia-candidata-0.3.md) aplica exatamente essa distinção: requisitos {RF-04}; testes {T06, T07, T11, T12, T14, T15}. T11/T15 preservam `negar/estado`, mas continuam relevantes porque seus papéis efetivos da baseline contêm o par alterado. A aplicabilidade estrutural dos testes tem critério distinto do impacto dos RFs.

Assim, em **cada** divergência: requisitos TP=1, FN=0, FP=2, revocação=1, precisão=1/3, F1=1/2, seleção completa=1 e correspondência exata=0; testes TP=6, FN=0, FP=0 e correspondência exata=1. Ao todo são quatro respostas com oito ocorrências excedentes, sempre dos mesmos dois IDs existentes. RF-02 e RF-03 participam desses cenários, mas suas permissões e papéis efetivos permanecem inalterados; por isso são seleções excedentes conforme o critério fornecido. **Confundir participação com impacto é uma hipótese interpretativa**, não evidência do raciocínio interno do modelo. As listas não permitem afirmar por que os IDs foram selecionados. Esta interpretação, explicitada em D-46, não altera referência, pontuação ou respostas.

## Subsídios à ficha existente de conformidade

A [ficha existente das 64 observações](../avaliados/extensao-real-0.3-001-avaliacao-001/revisao-conformidade-pendente.json) foi reutilizada como vínculo de revisão e conferida contra `revisao_conformidade.contexto`: fontes, IDs e as cinco assinaturas por observação (avaliação, tentativa, fechamento, payload e resposta). Permanece **sem preenchimento humano**: `responsavel=null`, `data=null`, 64 decisões `pendente` e 64 justificativas nulas. Seus bytes e hash não foram alterados.

| Verificação comprovada offline | Alcance da evidência |
|---|---|
| Plano 003 e cópia no lote idênticos; 64 identidades e duas repetições em cada uma das 32 combinações. | Quatro mudanças × quatro condições × dois modelos × duas repetições; 32 observações por modelo, sem misturar piloto ou controles. |
| Fechamentos e fontes da ficha íntegros; 1.312 vínculos de fechamento conferidos. | Payloads, preparações, requisições, respostas, metadados e avaliações vinculados por hash. |
| Modelo solicitado e reportado coincidentes; esforço solicitado medium, limite 4096. | Requisições reconstruídas literalmente a partir do payload/configuração; não demonstra implementação interna do esforço pelo provedor. |
| Dezesseis payloads únicos, iguais entre modelos e repetições correspondentes; definições comuns idênticas em todos. | Notas presentes somente em D1/E1, com um único hash de texto; documentos autorizados validados pelo conferidor do plano. |
| Requisições com apenas os oito campos previstos, `input` igual ao payload, `tools=[]`, `tool_choice=none`, `store=false`, `stream=false`. | Sem campo adicional de instrução, histórico, referência privada ou anexo no corpo enviado pelo cliente. |
| Envelopes sem instruções adicionais, `previous_response_id` nulo, ferramentas vazias e saída somente dos tipos mensagem/raciocínio. | Nenhuma chamada de ferramenta ou encadeamento reportados. Não comprova mecanismos privados do provedor nem isolamento por sistema operacional. |
| 64 HTTP 200 concluídos, sem falha, retry ou desvio detectado; IDs remotos únicos e ordem temporal compatível com o plano. | Uma tentativa T01 por observação; texto final extraído literalmente do envelope; tokens coincidem com os registros. |
| 64 respostas válidas, sem IDs desconhecidos, duplicatas ou omissões em RFs/testes. | Verificação de formato e desempenho separada de conformidade; quatro seleções excedentes de RFs são resultados preservados. |

Base histórica: [integridade D-43](../evidencias/spec004/avaliacao-extensao-0.3-D43/integridade.json). Na reconferência de D-44, executada com conexões/DNS bloqueados por audit hook e Python `-B`, também foram comparados os **6.442 hashes originais** do inventário D-43 e os **1.325 vínculos** do manifesto descritivo, sem divergências. Foram utilizados os validadores existentes `extensao_exploratoria.conferir`, `revisao_conformidade.contexto` e `coletor_api.interpretar`, somente para leitura; não foram repetidos os comandos de criação de D-43.

**Problemas e limites encontrados:** nenhum erro técnico de integridade ou desvio de protocolo foi detectado nos artefatos examinados. As quatro divergências são de seleção em relação à referência, não fundamento automático para exclusão. A ausência de desvio detectado não aprova conformidade. A referência continua `CANDIDATO_NAO_REVISADO`, com revisor/data nulos; a documentação das notas 0.2-local também conserva a conferência final do pesquisador como pendente. Não há aprovação externa ou parecer do orientador registrado para esses itens.

**Decisões a registrar pelo pesquisador:**

1. Para cada uma das 64 observações, decidir `incluir`, `excluir` ou `pendente`, com justificativa de procedimento ligada aos hashes existentes. Uma decisão de exclusão precisa identificar o desvio/evidência; pontuação baixa, inclusive nas quatro divergências, não é motivo de exclusão. Nenhuma observação foi excluída nesta análise.
2. Informar o responsável real e a data efetiva da revisão, em ISO 8601 com fuso, sem retroagir a data da captura. O registro de pendência também exige justificativa; enquanto existir alguma decisão pendente, o resumo continuará bloqueado.
3. Registrar em [decisões](decisoes.md) o alcance efetivo da revisão científica da referência 0.3, da definição de impacto/política e da neutralidade das notas utilizadas: versão/hash, itens examinados, divergências e resolução. Não alterar os originais ou declarar aprovação retrospectiva. Essa revisão científica é distinta da decisão de conformidade por observação.

## Síntese curta para o TCC

**Pergunta investigada.** Neste módulo fictício de autorização e em quatro mudanças independentes, como a organização do pedido e a presença de notas simuladas do analista se relacionam com acertos, omissões, excedentes e consistência na seleção de requisitos impactados e testes existentes, usando GPT-6 Sol e GPT-6 Astra?

**Desenho executado.** A extensão exploratória 0.3 reuniu 64 respostas: quatro mudanças × quatro condições (D0: direta sem notas; D1: direta com notas; E0: etapas sem notas; E1: etapas com notas) × dois modelos/medium × duas repetições. O plano 003 organizou dois blocos de 32, com ordem aleatorizada registrada; cada chamada recebeu um pacote independente, com catálogo de quinze testes e limite comum de 4096 tokens. As listas foram avaliadas offline contra a mesma referência candidata 0.3, mantendo o piloto e os controles fora dos denominadores.

**Resultados.** As 64 respostas tiveram formato válido, sem omissões de requisitos ou testes. Houve empate integral na seleção de testes: 64/64 correspondências exatas. Em requisitos, Sol apresentou 28/32 respostas exatas e Astra 32/32. As quatro divergências ficaram em MC-02/Sol: RF-02 e RF-03 foram selecionados além de RF-04. Nesse recorte, D0/D1/E0/E1 tiveram, respectivamente, 1/2, 2/2, 0/2 e 1/2 respostas exatas; nas demais mudanças houve empate. E0/MC-02/Sol repetiu a seleção excedente, mostrando que consistência não equivale a acerto.

**Interpretação.** Os resultados registram concordância elevada com a referência local, efeito de teto nos testes e divergências localizadas na delimitação do impacto dos requisitos. A distribuição observada não sustenta superioridade geral de modelo ou benefício causal das notas/estrutura, nem revela o processo interno que levou às seleções.

**Limitações.** São somente duas repetições por combinação, produzindo um único par de Jaccard por célula; não permitem caracterizar bem a variabilidade ou efeitos estáveis. O recorte usa um único módulo fictício pequeno, quatro mudanças e referência ainda candidata. As notas são simuladas com apoio de IA, acrescentam texto e foram reformuladas após exposição ao exploratório anterior, limitação preservada no histórico. Não se medem desempenho de analistas juniores, compreensão interna, cobertura de código, detecção de defeitos ou economia real de regressão. A conformidade das 64 observações continua pendente; esta síntese é descritiva e não substitui o resumo controlado após revisão humana.

## O que falta para gerar o resumo revisado

O [mecanismo existente](../revisao_conformidade.py) já atende ao lote exploratório. Faltam **o preenchimento humano e o registro validado das decisões**, seguidos da execução offline do resumo. Não faltam capturas, avaliações ou uma nova implementação. O bloqueio atual não exige novas chamadas à API.

1. Quando efetivamente fizer a revisão, o pesquisador deve usar a ficha existente como modelo e conservar seus campos de fontes/IDs/hashes. Como a ficha pendente também integra o manifesto descritivo preservado, salvar o preenchimento em **um único arquivo novo**, `avaliados/extensao-real-0.3-001-avaliacao-001/revisao-conformidade-preenchida-001.json`. Não criar outra ficha pendente. Preencher `responsavel`, `data` e as 64 decisões/justificativas. Para desbloquear, nenhuma decisão pode permanecer `pendente`.
2. Registrar esse arquivo por `revisar`; o comando valida novamente as fontes e grava um registro separado e uma cópia literal das decisões com hash. Ele não transforma avaliações/capturas originais em conformes. Um desvio já registrado não pode ser incluído como conforme por esse mecanismo.
3. Executar `resumir-revisado` sobre o registro validado, em destino novo. O mecanismo revalida os hashes e usa as métricas existentes somente nas respostas incluídas e válidas. Conserva `N_planejado_original=64`, exclusões justificadas, ausências e contagens operacionais originais.

Comandos preparados para uso **após o preenchimento humano**, a partir de `D:\TCC-Projeto\TCC\tcc-impacto-llm`; não executados em D-44:

```powershell
python -B coletor_api.py revisar --decisoes avaliados/extensao-real-0.3-001-avaliacao-001/revisao-conformidade-preenchida-001.json --saida avaliados/extensao-real-0.3-001-avaliacao-001/revisao-conformidade-001.json
python -B coletor_api.py resumir-revisado --revisao avaliados/extensao-real-0.3-001-avaliacao-001/revisao-conformidade-001.json --saida avaliados/extensao-real-0.3-001-avaliacao-001/resumo-revisado-001
```

Os destinos novos ainda não existem. O resumo revisado preservará o [resumo bloqueado original](../avaliados/extensao-real-0.3-001-avaliacao-001/resumo/resumo.json). Retornos previstos pelo mecanismo: **2** se houver pendência; **1** com cobertura incompleta por exclusões/ausências; **0** se o resumo elegível estiver completo. Retorno 0 não constitui validação científica da referência: o código exige decisões de conformidade, não preenche revisão de gabarito, notas ou aprovação do orientador.

## Alterações e pendências deste fechamento

Somente este complemento, [ESTADO_ATUAL.md](../ESTADO_ATUAL.md) e o registro D-44 em [decisoes.md](decisoes.md) foram acrescentados/atualizados. Dados, hashes, notas, prompts, referência, regras de pontuação, ficha pendente e relatórios anteriores foram preservados. Não houve chamadas externas, commit ou push. Permanecem pendentes as decisões humanas descritas acima e, depois delas, os dois comandos offline; não se declara a pesquisa encerrada ou a conformidade aprovada.

## Revisão assistida de conformidade — D-45, aguardando decisão humana

11/11/2026. O pesquisador solicitou realizar sua revisão das 64 observações, com apresentação de evidências, agrupamento das verificações comuns e decisões individuais ligadas aos hashes. **A solicitação de revisão não contém ainda decisão de incluir/excluir observações.** A ficha original permanece pendente; não foram executados `revisar` ou `resumir-revisado`. Nenhum acerto, erro ou escore foi usado para formar os grupos ou avaliar conformidade.

### Fontes vinculadas e resultado da reconferência

Ficha reutilizada: [revisao-conformidade-pendente.json](../avaliados/extensao-real-0.3-001-avaliacao-001/revisao-conformidade-pendente.json), SHA-256 **`10bc74969683b1f3622d67e8efec47da838f9071ed561d6c83f210ed5bbe9307`**. Cada um dos 64 registros conserva seus hashes completos de avaliação, tentativa, fechamento, payload e resposta. A comparação com `revisao_conformidade.contexto` confirmou todas as fontes e assinaturas; responsável/data e justificativas continuam nulos, decisões `pendente`.

Plano: [extensao-20261109-003/plano.json](../captura/extensao-20261109-003/plano.json), SHA-256 `e00fd77c23e3b018cb3781e5ebee9b0d1b765e36e7c53fdf9eba8588e45c2e3e`, idêntico à cópia do lote. Referência identificada pelo hash `94b6315b935d9817dd833567a0b107a90e88d9be850e93c747e03337450eebc9`, preservada e aberta apenas na avaliação separada. Preservação reconferida em D-45: **6.442 hashes originais, 1.325 vínculos do manifesto descritivo e 1.312 vínculos de fechamento**, sem divergências. Conferência local com rede/DNS bloqueados e Python `-B`.

| Item | Evidência examinada nas 64 observações | Resultado comprovado e limite |
|---|---|---|
| Plano e execução | Plano/cópia, ordem, observações planejadas e `tentativa.json`. | Quatro mudanças × quatro condições × dois modelos × duas repetições, 32 células com duas observações; IDs e ordem coincidentes. Nenhuma posição faltante ou extra. |
| Configurações | Configuração de cada linha, corpo de requisição e envelope recebido. | Sol `ext-api-sol-c876e81f01df3a17` e Astra `ext-api-astra-9d2e238e64485a09`; modelos solicitado/reportado coincidentes, medium solicitado e reportado, limite comum solicitado 4096, timeout configurado 120 s, sem fallback. Não se alega controle de mecanismos internos do provedor. |
| Conteúdo dos payloads | Reconstrução dos dezesseis textos pelas fontes editoriais preservadas do plano, com `fontes_autorizadas.reunir_fontes`, catálogo público 0.3 e política de bytes já utilizada. | Todos os documentos entregues coincidem byte a byte com os recortes esperados; o payload recomposto coincide com `payload.txt`, `entrada.bin` e `input` da requisição. Nenhuma alteração de material para esta conferência. |
| Distribuição das notas/pedidos | Arquivos/ordem do manifesto e bytes dos recortes reconstruídos. | Sete documentos sem notas; oito com notas somente em D1/E1. Pedido direto em D0/D1, estruturado em E0/E1. Textos correspondentes iguais entre modelos e repetições; notas únicas comuns, sem ajustes por resultado. |
| Independência no cliente | Requisição completa, IDs e envelope de cada observação. | Uma entrada textual por requisição, sem campos de conversa/arquivos/anexos; `previous_response_id=null` e `instructions=null` em todos os envelopes; 64 request IDs e 64 response IDs únicos, execução sequencial compatível com a ordem. Nenhuma resposta anterior acrescentada ao `input` reconstruído. Isso comprova a fronteira registrada do cliente, não o funcionamento privado do provedor. |
| Ferramentas | Requisições, envelopes e tipos de saída. | `tools=[]` e `tool_choice=none` em 64/64; sem saída de chamada de ferramenta. Os contadores reportam zero requisições de busca e zero tokens de geração de imagem. `store=false` e `stream=false` no cliente. |
| Ausência de gabarito entregue | Lista fechada, recortes reconstruídos e corpo literal enviado. | Somente sistema, definições comuns, RFs/baseline, catálogo com resultados da baseline, uma mudança, pedido, schema e notas quando previstas. Não foram entregues arquivo da referência privada, matriz das variantes, listas corretas pós-mudança ou guias completos. A presença de resultados da baseline é parte autorizada do catálogo; não é a referência das variantes. A neutralidade substantiva das notas continua tema de revisão humana. |
| Preservação e extração | Fechamentos, manifesto, ficha, envelope HTTP e cópias literais na avaliação. | Hashes coincidentes; texto extraído igual à resposta capturada e à cópia da avaliação, sem correção ou reserialização. Os originais e a ficha permanecem intocados. |
| Tentativas e ocorrências técnicas | Diretórios por observação, tentativa, transporte, envelope e timestamps. | Uma pasta T01 por observação, HTTP 200 concluído, sem falha registrada, sem tentativa anterior e zero retentativas do cliente em todas. Sem desvio técnico detectado. Isso não é aprovação humana automática nem prova de ausência de eventos fora do lote. |

Hash comum das definições efetivamente entregues: `14d60b975109cce15613c66948f235e7572489ba7eb5ed0b4038869e5b43b37e`. Hash das notas efetivamente entregues em D1/E1: `5e209b6e58ba986df05846f6d36c9464fbc3d669f70ab97d8d0014872dc00add`.

### Exceções e pontos que exigem interpretação explícita

- **Nenhuma exceção técnica individual detectada** nas verificações acima: não há observação destacada por hash divergente, ferramenta, histórico encadeado, payload diferente, falha ou retry. Essa constatação não escolhe inclusão/exclusão.
- **Metadados históricos de preparação:** o plano conserva `PREPARADO_NAO_ENVIADO` e linhas `PLANEJADA_NAO_EXECUTADA`; os pacotes conservam `RASCUNHO_PREPARACAO`, `liberado_para_pesquisa=false` e a entrega textual conserva `envio_realizado=false`. São os documentos de preparação preservados. A execução é comprovada por tentativas/transportes/respostas/fechamentos reais posteriores, sob a autorização D-42; não foram corrigidos retroativamente os originais. O pesquisador pode registrar se considera suficiente essa distinção para a conformidade do procedimento.
- **Campo do provedor:** todos os envelopes reportam `reasoning.context=all_turns`, além de `effort=medium`, `mode=standard` e `summary=null`. Registra-se o valor literal; ele não demonstra por si a existência de outros turnos, nem permite garantir a implementação interna do contexto. A independência demonstrada é a das requisições completas sem encadeamento ou conteúdo adicional. Não se exige que o pesquisador ateste o que os registros não permitem observar.
- **Revisão científica separada:** a referência continua candidata, com revisor/data nulos; notas permanecem com conferência final documentada como pendente. O pesquisador deve explicitar se sua decisão agora cobre somente conformidade do lote ao procedimento documentado, sem converter isso em aprovação científica retrospectiva da referência/notas. Se considerar essa lacuna impeditiva de uma observação ou grupo, deve registrar a pendência e sua justificativa.
- **Ocorrências externas:** os registros não permitem descobrir tentativas manuais, intervenção, troca de arquivos ou contexto adicional fora dos artefatos preservados. Cabe ao pesquisador informar ocorrências conhecidas e os IDs afetados; a declaração de que não conhece outras ocorrências é distinta da evidência técnica acima.

### Grupos disponíveis para decisão conjunta

Todos os grupos passaram pelas verificações comuns acima. O agrupamento serve à leitura e à declaração do pesquisador; não cria decisão automática ou unidade nova de pontuação. **Cada grupo contém exatamente os oito IDs** `EXT03-{mudança}-{condição}-{modelo}-R{repetição}`, com mudanças **MC-01, MC-02, MC-03, MC-04-v2** e repetições **01 e 02**. Modelo no ID é `SOL` ou `ASTRA`. Os oito grupos são disjuntos e cobrem as 64 entradas da ficha.

| Grupo | Modelo no ID | Condição | Pedido | Notas | Quantidade | Decisão humana atual |
|---|---|---|---|---|---:|---|
| G01 | SOL | D0 | Direto | Ausentes | 8 | Não declarada |
| G02 | SOL | D1 | Direto | Presentes | 8 | Não declarada |
| G03 | SOL | E0 | Em etapas | Ausentes | 8 | Não declarada |
| G04 | SOL | E1 | Em etapas | Presentes | 8 | Não declarada |
| G05 | ASTRA | D0 | Direto | Ausentes | 8 | Não declarada |
| G06 | ASTRA | D1 | Direto | Presentes | 8 | Não declarada |
| G07 | ASTRA | E0 | Em etapas | Ausentes | 8 | Não declarada |
| G08 | ASTRA | E1 | Em etapas | Presentes | 8 | Não declarada |

Uma declaração explícita pode abranger grupos ou todas as 64 observações, com exceções por ID. Na transcrição futura, a decisão/justificativa será escrita **em cada uma das linhas individuais da ficha copiada**, mantendo os cinco hashes completos e as fontes originais. Não se substituirá essa vinculação por um único registro agregado. Uma exceção individual prevalece sobre a decisão do grupo; qualquer ambiguidade permanece sem decisão até esclarecimento.

### Declaração necessária do pesquisador e próximos passos condicionais

Para registrar a revisão, faltam: identificação/ratificação do responsável; decisões `incluir|excluir|pendente` para os grupos/IDs abrangidos, com justificativa baseada no procedimento; indicação de ocorrências conhecidas fora do lote e exceções; data efetiva com fuso. A data/hora pode ser a do recebimento da declaração explícita (UTC−03:00), se o pesquisador assim autorizar; não a data da captura.

Formato possível, **a preencher ou alterar pelo pesquisador; não representa aprovação já dada**:

```text
Responsável: [nome].
Decisões: [grupos ou IDs e incluir/excluir/pendente].
Justificativa: [verificações aceitas e motivos de eventuais exceções/pendências].
Ocorrências conhecidas fora dos registros: [nenhuma conhecida ou descrição/IDs].
Alcance: [conformidade ao procedimento documentado; indicar se inclui outro alcance].
Data: [ISO 8601 com fuso ou autorizar a data/hora desta declaração].
```

Somente após a declaração explícita será produzido o arquivo preenchido separado a partir desta ficha, sem alterar suas fontes/assinaturas. Serão utilizados `revisar` e `resumir-revisado` com os destinos novos e o contrato descritos acima; N planejado permanecerá 64. Havendo decisões pendentes, o resultado continuará bloqueado, e nenhuma será convertida em inclusão para liberar o resumo. Esta etapa aguarda a declaração humana; não criou ficha duplicada, arquivo de decisões preenchidas ou resumo revisado.
