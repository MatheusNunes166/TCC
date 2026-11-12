# Bloco de notas MC-04-v2 — descrição com conformidade pendente

11/11/2026, D-50. **Não houve alteração observável na seleção de IDs diante da nota incorreta N02**, nas quatro combinações de modelo e estrutura. As 16 respostas coincidiram com a referência candidata 0.3 em requisitos e testes. Esse empate, incluindo o resultado desfavorável à hipótese de mudança da seleção, foi preservado integralmente.

## Desenho executado e fontes

MC-04-v2 × GPT-6 Sol/Astra `medium` × direta D1/estruturada E1 × N01/N02 × duas repetições = **16 observações em oito células N=2**. N01 é a nota coerente; N02 contém uma afirmação deliberadamente incorreta. O par difere somente nessa afirmação; rótulos e mapa privado não foram enviados ao modelo. A saída solicitada contém exclusivamente listas de requisitos e testes, sem explicação sobre a nota.

[Plano integrado 002](../../captura/notas-mc04-0.3-002/plano.json), SHA-256 `c8363eb2daaac2b1d1d1538470458356a29504cfc378d17cb35c2188d43dc1bd`; [capturas originais](../../captura/notas-mc04-real-001/). Referência candidata **0.3**, catálogo T01–T15, SHA-256 `94b6315b935d9817dd833567a0b107a90e88d9be850e93c747e03337450eebc9`. Política `ids-proposta-004-v2`, SHA-256 `232145fb21526825157a1093adcd02386419da65f7169ebc4d442b2cbc35214c`, sem alteração. O adaptador `notas_exploratorias.py avaliar` reutilizou o avaliador existente, e `coletor_api.py revisao-modelo` gerou a ficha pendente.

Este bloco não incorpora o piloto, controles artificiais ou as 64 observações anteriores. Nenhum material, resposta, configuração ou regra foi ajustado pelos resultados. A autorização de uso do par/plano e das chamadas foi registrada em D-48/D-49; não equivale a revisão de conformidade das capturas.

## Denominadores e comparação

No bloco: **N=16 planejadas, A=16 tentativas, C=16 concluídas, V=16 válidas**; respostas inválidas **I/C=0/16**, falhas técnicas **T/N=0/16**, ausentes **0/16**. Em cada célula: N=A=C=V=2, I=0, T=0 e K=2 com somente IDs conhecidos. Não há duplicatas ou IDs desconhecidos. Validade usa C, métricas e correspondência exata usam V; inválidas e falhas não foram imputadas como seleções vazias ou escores zero.

| Modelo/medium | Estrutura | Nota | V/C | RF exatas/V | RF acertos/omissões/excedentes | Testes exatos/V | Testes acertos/omissões/excedentes |
|---|---|---|---|---|---|---|---|
| Sol | Direta D1 | N01 | 2/2 | 2/2 | 4/0/0 | 2/2 | 16/0/0 |
| Sol | Direta D1 | N02 | 2/2 | 2/2 | 4/0/0 | 2/2 | 16/0/0 |
| Sol | Estruturada E1 | N01 | 2/2 | 2/2 | 4/0/0 | 2/2 | 16/0/0 |
| Sol | Estruturada E1 | N02 | 2/2 | 2/2 | 4/0/0 | 2/2 | 16/0/0 |
| Astra | Direta D1 | N01 | 2/2 | 2/2 | 4/0/0 | 2/2 | 16/0/0 |
| Astra | Direta D1 | N02 | 2/2 | 2/2 | 4/0/0 | 2/2 | 16/0/0 |
| Astra | Estruturada E1 | N01 | 2/2 | 2/2 | 4/0/0 | 2/2 | 16/0/0 |
| Astra | Estruturada E1 | N02 | 2/2 | 2/2 | 4/0/0 | 2/2 | 16/0/0 |

**Requisitos:** precisão=1, revocação=1 e F1=1 em cada resposta e em cada célula; Jaccard entre R01/R02=1, um par por célula. **Testes:** precisão=1, revocação=1 e F1=1 em cada resposta e em cada célula; Jaccard entre R01/R02=1, um par por célula. As médias são macro por resposta válida dentro de cada célula, pelas funções existentes. As contagens de acertos acima somam ocorrências, sem usá-las como denominador das médias. Consistência é separada de acerto, embora ambos coincidam neste lote.

| Comparação dentro do mesmo modelo/estrutura | RF exatas N01 → N02 | Testes exatos N01 → N02 | Diferença nos conjuntos N01/N02, por repetição |
|---|---|---|---|
| Sol/D1 | 2/2 → 2/2 | 2/2 → 2/2 | Nenhuma em R01 ou R02 |
| Sol/E1 | 2/2 → 2/2 | 2/2 → 2/2 | Nenhuma em R01 ou R02 |
| Astra/D1 | 2/2 → 2/2 | 2/2 → 2/2 | Nenhuma em R01 ou R02 |
| Astra/E1 | 2/2 → 2/2 | 2/2 → 2/2 | Nenhuma em R01 ou R02 |

Cada lado da comparação mantém seu V=2. A correspondência pelo índice R01/R02 é descritiva nos blocos de execução; não é teste estatístico pareado. [CSV completo das oito células](tabelas-descritivas.csv) e [JSON com avaliações, conjuntos, métricas e diferenças individuais](descritivo-pendente.json).

## IDs selecionados e divergências

Em **todas as 16 observações**, os conjuntos selecionados e esperados foram:

- Requisitos: **{RF-03, RF-04}**. Acertos: ambos; omissões: nenhuma; excedentes: nenhum.
- Testes: **{T05, T07, T08, T10, T12, T13, T14, T15}**. Acertos: os oito; omissões: nenhuma; excedentes: nenhum.

**Nenhum ID diferiu da referência ou entre as duas execuções da mesma célula.** Nenhum ID foi acrescentado/retirado de N01 para N02 em R01 ou R02, em qualquer modelo/estrutura. No JSON, `divergencias_referencia` é vazio; os 16 registros de comparação entre repetições (oito células × duas dimensões) e os 16 registros N01/N02 (quatro combinações × duas repetições × duas dimensões) conservam diferenças vazias, sem suprimir empates. Os 16 IDs de observação e suas listas originais estão em `observacoes` e na ficha com hashes. Igualdade dos conjuntos não implica igualdade de espaços/quebras de linha; os bytes das respostas foram preservados.

## Conferência técnica e consumo

A [conferência de integridade](../../evidencias/spec004/avaliacao-notas-0.3-D50/integridade.json) confirmou 16 identidades, oito células, um T01 por observação, **336 vínculos de fechamento**, preparações/payloads/requisições literais, `nota_id` em todos os registros, modelo reportado igual ao solicitado, `medium` e limite 4096 também reportados nos envelopes, HTTP 200 e `completed` em todas. A extração textual e os tokens foram confrontados com os envelopes originais. Há 16 request IDs e 16 response IDs únicos; a ordem temporal é compatível com a ordem do plano. Período registrado: **11/11/2026, 20:51:41 a 20:59:35, America/Sao_Paulo**.

Não foram detectados desvios nos registros/envelopes. Retentativas registradas do cliente: **0**; falhas de transporte/fragmentos: **0**. Requisições independentes contêm somente o payload previsto, sem ferramentas, gabarito, instruções adicionais ou vínculo por `previous_response_id`; `store=false` e `stream=false`. A conferência descreve as evidências locais e o que a API reportou, sem alegar acesso aos mecanismos internos do provedor.

| Modelo — oito observações | Entrada | Saída | Raciocínio incluído na saída | Total entrada + saída |
|---|---:|---:|---:|---:|
| Sol | 14.868 | 1.464 | 1.010 | 16.332 |
| Astra | 14.868 | 866 | 386 | 15.734 |

Os tokens de raciocínio já integram a saída; não são somados novamente. `usage` por observação está na evidência de integridade e os totais no JSON descritivo. Não houve consulta de saldo/faturamento nem estimativa de custo. O orçamento novo permanece nulo conforme a autorização D-49 arquivada; USD 2 nas configurações é metadado histórico.

## Revisão de conformidade preparada

[Ficha existente do mecanismo, com as 16 decisões pendentes](revisao-conformidade-pendente.json). Cada decisão está ligada aos hashes de avaliação, tentativa, fechamento, payload, resposta e plano, além de `nota_id`/bloco. Responsável/data e justificativas permanecem nulos; não houve inclusão, exclusão ou aprovação humana preenchida pelo assistente. As oito linhas da tabela podem orientar uma revisão conjunta por modelo/estrutura/nota; as decisões continuam individuais na ficha.

| Sustentado pelos arquivos | Depende da confirmação do pesquisador |
|---|---|
| Plano, ordem, par de notas, configuração e autorização correspondem aos hashes preparados/aprovados. | Confirmar o alcance da revisão humana e ocorrências conhecidas fora dos registros. |
| Payload entregue coincide com o preparado; requisições sem ferramentas/gabarito/histórico encadeado; modelo e completude reportados coerentes. | Revisar essas evidências e decidir conformidade de cada observação, sem usar acerto como critério. |
| Uma tentativa por observação, sem retry registrado; originais, extrações e fechamentos íntegros. | Confirmar eventuais intervenções ou execuções externas não representadas no lote. |
| Primeira observação e sequência temporal preservadas; nenhum desvio técnico detectado. | Confirmar a conferência humana da primeira observação antes de prosseguir; os arquivos não registram por si essa decisão intermediária. |

O [resumo controlado](resumo/resumo.json) conserva oito células bloqueadas pela revisão pendente, `completo=false`, retorno **2 no manifesto do avaliador**. As tabelas deste relatório são descritivas e não representam uma aprovação desse resumo. Acerto, HTTP 200 ou ausência de desvio detectado não aprovam conformidade. O comando de avaliação não foi repetido para alterar esse estado.

Após decisões explícitas, salvar preenchimento separado conforme o contrato e usar os comandos existentes, sem sobrescrever a ficha pendente:

```powershell
python -B coletor_api.py revisar --decisoes avaliados/notas-mc04-real-001/decisoes-preenchidas.json --saida avaliados/notas-mc04-real-001/revisao-001.json
python -B coletor_api.py resumir-revisado --revisao avaliados/notas-mc04-real-001/revisao-001.json --saida avaliados/notas-mc04-real-001/resumo-revisado-001
```

Esses dois comandos não foram executados. Preservar N=16 original, exclusões justificadas e oito células separadas. A ficha das 64 observações anteriores continua intacta e pendente.

## Interpretação, limitações e preservação

Não se observou efeito da troca N01/N02 sobre os conjuntos selecionados em Sol/D1, Sol/E1, Astra/D1 ou Astra/E1. O desenho não pediu explicação sobre a nota: a seleção de IDs não permite afirmar reconhecimento explícito da contradição, nem atribuir raciocínio interno ao modelo.

O resultado é local: **uma mudança, um par de notas com diferença localizada, dois modelos em medium e somente duas repetições por célula**. Há um único par de consistência por célula; não há base para conclusão geral sobre resistência a notas incorretas, equivalência entre condições ou ausência de efeito em outros contextos. Documentos comuns permanecem disponíveis junto à nota, e o resultado não isola seus mecanismos de influência. A referência/política continuam candidatas e a revisão humana de conformidade está pendente.

Nenhuma chamada externa/API, conexão, commit ou push foi realizada nesta avaliação. [Inventário inicial](../../evidencias/spec004/avaliacao-notas-0.3-D50/estado-inicial.json), [preservação dos 12.685 arquivos anteriores](../../evidencias/spec004/avaliacao-notas-0.3-D50/preservacao.json), [conferência final](../../evidencias/spec004/avaliacao-notas-0.3-D50/conferencia-final.json) e [manifesto dos descritivos](manifesto-descritivo.json) permitem conferir os vínculos. As fontes funcionais, versões, materiais e dados anteriores permaneceram nos mesmos caminhos e bytes.
