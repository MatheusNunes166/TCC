# Recebimento e avaliação pendente — ensaio exploratório MC-04

Registro documental: 05/11/2026. **AGUARDANDO ORIGINAIS — nenhuma resposta avaliada.** Esta data identifica o registro local; não é data atribuída às execuções do modelo.

## Configuração declarada pelo pesquisador

| Item | Confirmação recebida |
|---|---|
| Interface | Codex |
| Modelo reportado | GPT-6 Astra |
| Raciocínio | Médio |
| Contextos | Quatro conversas novas e independentes, conforme declaração do pesquisador |
| Ordem declarada | D0 → D1 → E0 → E1 |
| Repetições | Uma execução por condição; quatro execuções declaradas |
| Fase | Exploratória, excluída do piloto e da coleta principal |

Detalhes em [configuracao-confirmada.json](configuracao-confirmada.json). A configuração declarada não comprova versão/build do modelo, data de cada execução, correspondência dos bytes enviados, ausência de ferramentas/anexos ou configurações não informadas. Esses dados permanecem nulos/desconhecidos. Confirmar a configuração não é concluir a revisão dos textos ou a revisão profissional/científica.

## Situação das respostas e comparação

A busca no diretório do ensaio encontrou somente as quatro fichas planejadas, sem arquivos originais de respostas. Foram criados registros de recebimento com a configuração declarada e estado `AGUARDANDO_ORIGINAL`, preservando as fichas planejadas e os pacotes anteriores. Nenhum arquivo de resposta foi criado a partir da referência.

| Condição | Ordem declarada | Original recebido | Validade | Requisitos: acertos/omissões/excedentes | Testes: acertos/omissões/excedentes |
|---|---|---|---|---|---|
| D0 | 1 | Não | Não examinada | Não avaliados | Não avaliados |
| D1 | 2 | Não | Não examinada | Não avaliados | Não avaliados |
| E0 | 3 | Não | Não examinada | Não avaliados | Não avaliados |
| E1 | 4 | Não | Não examinada | Não avaliados | Não avaliados |

Não há comparação de desempenho possível neste recebimento. Arquivo não localizado não significa resposta vazia, formato inválido ou falha técnica da execução. Não há contagens zero de TP/FP/FN nem escores imputados; há dados ausentes. Não se calcula consistência entre repetições: existe somente uma execução declarada por condição.

## Arquivos solicitados e continuação

Solicitados os caminhos dos quatro arquivos originais D0/D1/E0/E1. Se ainda não estiverem no workspace, o pesquisador deverá fornecê-los, com identificação inequívoca da condição e sem remover cercas, explicações, recusas ou outros trechos. Exportações que incluam o contexto devem ser preservadas; eventual extração da mensagem do modelo será uma cópia derivada identificada, nunca substituição do original.

Se disponíveis, fornecer também o conteúdo efetivamente enviado e seus registros/exportações. Caso não haja cópia, registrar essa limitação e eventual confirmação do pesquisador, sem apresentar o payload preparado como captura original da transmissão. Datas/horários, tokens, duração, custo e recursos efetivos só serão preenchidos quando houver informação; se desconhecidos, permanecerão assim.

Após o recebimento, avaliar requisitos e testes separadamente com a função existente `avaliacao_ids.avaliar_resposta`, conforme [AVALIAR.md](../AVALIAR.md), mantendo origem `llm_exploratoria`. Não utilizar ou contornar a CLI restrita a sintéticos. O comando documentado também exige datas/cópia do enviado; dados desconhecidos não serão fabricados para satisfazer suas asserções. Qualquer adequação documental necessária para registrar metadados ausentes será explicitada, sem mudar parser, política ou pontuação.

Registros locais por condição: [D0](../registros/D0/registro.json), [D1](../registros/D1/registro.json), [E0](../registros/E0/registro.json), [E1](../registros/E1/registro.json). A configuração tem identificador local próprio, sem fingir versão de provedor. Os arquivos `ensaio.json`, `registro-planejado.json` e os recibos de preparação continuam históricos da etapa anterior; seus estados de não envio não são um novo relato sobre as execuções agora declaradas.

## Preservação e limites

[preservacao.json](preservacao.json) registra os hashes dos 67 arquivos anteriores do ensaio e das fontes protegidas, sem divergências. Notas/prompts e referência candidata 0.2 continuam intactos; política `ids-proposta-004-v2` permanece candidata à revisão científica. Nenhum módulo ou contrato da CLI foi alterado, e o avaliador não foi executado sem originais.

Não houve chamada nova pelo assistente. O relato de quatro execuções é do pesquisador e ainda aguarda os artefatos correspondentes. O ensaio não integra automaticamente piloto/coleta principal, e este relatório de recebimento não é fechamento da avaliação nem revisão científica.
