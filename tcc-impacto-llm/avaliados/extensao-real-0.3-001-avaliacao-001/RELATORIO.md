# Extensão 0.3 — resultados descritivos com conformidade pendente

09/11/2026, D-43. **64 respostas reais avaliadas offline**, 32 por modelo, usando o plano 003 e a referência candidata 0.3 de 15 testes, hash `94b6315b935d9817dd833567a0b107a90e88d9be850e93c747e03337450eebc9`. Nenhuma chamada nova à API, teste de conexão, commit ou push. Piloto anterior e controles sintéticos não integram estes resultados. Notas, prompts, critérios, referência, coletor e planos utilizados ficaram intactos.

## Resultado e denominadores

[Tabelas por modelo × mudança × condição](TABELAS.md), [CSV](tabelas-descritivas.csv), [JSON descritivo](descritivo-pendente.json) e [64 avaliações individuais](lista.json). Há 32 células, com **N=2 planejadas, C=2 concluídas e V=2 válidas por célula**; zero respostas inválidas ou falhas técnicas. Todos os IDs são conhecidos, sem duplicatas. Precisão/revocação/F1 usam a média por resposta válida (macro), preservando a política existente; exatas usam V como denominador. Acertos/omissões/excedentes abaixo somam as ocorrências nas respostas, sem tomar essa soma como denominador da média macro.

| Modelo | Formato V/C | Requisitos: acertos/omissões/excedentes | Requisitos P/R/F1 macro (V=32) | Requisitos exatos | Testes: acertos/omissões/excedentes | Testes P/R/F1 macro (V=32) | Testes exatos |
|---|---|---|---|---|---|---|---|
| GPT-6 Sol/medium | 32/32 | 48/0/8 | 11/12 ; 1 ; 15/16 | 28/32 | 216/0/0 | 1 ; 1 ; 1 | 32/32 |
| GPT-6 Astra/medium | 32/32 | 48/0/0 | 1 ; 1 ; 1 | 32/32 | 216/0/0 | 1 ; 1 ; 1 | 32/32 |

As diferenças ficaram restritas aos **requisitos de MC-02 no Sol**. Nesse recorte, D1 teve duas respostas exatas; D0/E1 tiveram uma cada, e E0 nenhuma. O Astra teve duas respostas exatas nas quatro condições. Em requisitos, os modelos/condições empataram em MC-01, MC-03 e MC-04-v2; em testes, houve empate integral nas quatro mudanças e condições. Esses resultados não demonstram superioridade geral do modelo ou benefício causal das notas/estrutura: são duas repetições por célula, contra uma referência local ainda candidata.

| MC-02 — Sol | Requisitos P/R/F1 macro (V=2) | Exatas/V | Consistência: Jaccard (1 par) |
|---|---|---|---|
| D0 | 2/3 ; 1 ; 3/4 | 1/2 | 1/3 |
| D1 | 1 ; 1 ; 1 | 2/2 | 1 |
| E0 | 1/3 ; 1 ; 1/2 | 0/2 | 1 |
| E1 | 2/3 ; 1 ; 3/4 | 1/2 | 1/3 |

Nas outras células, precisão/revocação/F1 e Jaccard são 1 em requisitos e testes. As seleções de requisitos foram iguais entre repetições em 14/16 pares de células do Sol e 16/16 do Astra; em testes, 16/16 de cada modelo. E0/MC-02/Sol foi **consistente na seleção excedente**, demonstrando por que consistência não significa acerto. Jaccard foi calculado somente dentro da mesma célula, nunca entre mudanças/condições diferentes.

## Seleções divergentes e IDs

São quatro respostas, todas de Sol/MC-02. Em cada uma: referência de requisitos **{RF-04}**, seleção **{RF-02, RF-03, RF-04}**, acerto RF-04, excedentes **RF-02 e RF-03**, nenhuma omissão. São IDs existentes selecionados em excesso, não IDs inexistentes. Os testes dessas mesmas respostas coincidiram integralmente com {T06, T07, T11, T12, T14, T15}.

- `EXT03-MC-02-D0-SOL-R02`;
- `EXT03-MC-02-E0-SOL-R01`;
- `EXT03-MC-02-E0-SOL-R02`;
- `EXT03-MC-02-E1-SOL-R01`.

[IDs, conjuntos completos e caminhos das avaliações divergentes](divergencias-ids.json). A referência, notas e critérios não foram alterados em resposta a essas seleções.

## Consumo reportado

| Modelo (32 respostas) | Entrada | Saída incluindo raciocínio | Raciocínio, já dentro da saída | Total entrada + saída |
|---|---:|---:|---:|---:|
| GPT-6 Sol | 56.384 | 5.878 | 4.439 | 62.262 |
| GPT-6 Astra | 56.384 | 3.373 | 1.693 | 59.757 |
| Total | 112.768 | 9.251 | 6.132 | 122.019 |

Não se somam novamente os 6.132 tokens de raciocínio ao total. Cada modelo reportou também 28.144 tokens de entrada em cache e 28.144 de escrita de cache; são detalhes reportados da entrada, não novos tokens a adicionar ao total. Os números foram somados dos `usage` preservados e confrontados com os envelopes HTTP, sem nova consulta de saldo/faturamento ou estimativa monetária. [Detalhes por modelo](tokens-por-modelo.json).

## Integridade e revisão pendente

A [conferência técnica](../../evidencias/spec004/avaliacao-extensao-0.3-D43/integridade.json) confirmou 64 identidades, request IDs e response IDs únicos; duas repetições por combinação, 1.312 vínculos de fechamentos e a ordem real compatível com o plano. Conferiu requisição/payload/configuração, preparações copiadas, extração literal, modelo reportado, uso de tokens e ausência de retries. HTTP 200 em todas, sem desvios registrados/detectados nos envelopes. Período observado: **09/11/2026, 23:01:24 a 23:17:57, UTC−03:00**, conforme timestamps originais. [6.442 arquivos anteriores preservados](../../evidencias/spec004/avaliacao-extensao-0.3-D43/preservacao.json), inclusive dados do piloto e avaliações anteriores.

**Conformidade: 64 pendentes, zero aprovadas.** O [resumo controlado existente](resumo/resumo.json) continua bloqueado; seu manifesto registra retorno 2. As tabelas deste relatório são descrições das respostas disponíveis e não um resumo elegível após revisão humana. HTTP, inexistência de desvio detectado ou resposta correta não aprovam conformidade.

O mecanismo separado produziu o [modelo de revisão com hashes das 64 observações](revisao-conformidade-pendente.json). Responsável/data permanecem nulos; todas as decisões continuam `pendente`, sem justificativa preenchida em nome do pesquisador. Para sua revisão:

1. Confrontar os hashes/artefatos de cada observação com o material autorizado: plano 003, configuração do modelo, medium/4096, notas somente em D1/E1 e igualdade dos textos correspondentes entre modelos.
2. Conferir a independência das solicitações e a fronteira textual sem ferramentas/histórico, usando `entrada.bin`, `requisicao.json`, `resposta-http.bin` e os metadados vinculados. A conferência automática subsidia sua decisão, não a substitui.
3. Registrar inclusão/exclusão/pendência e justificativa por observação, responsável e data com fuso no arquivo separado, conservando originais e N=64. Avaliar conformidade independentemente de acerto; as quatro seleções excedentes não constituem automaticamente desvio de protocolo nem motivo de exclusão.

Não há pendência técnica de integridade detectada; a revisão humana de conformidade permanece aberta, assim como a condição candidata da referência. Nenhuma aprovação externa foi atribuída.

[Conferência final das médias, contagens, consistência, preservação e bytes Git](../../evidencias/spec004/avaliacao-extensao-0.3-D43/conferencia-final.json) confronta as tabelas com as avaliações por observação, sem alterar seus registros. Os arquivos descritivos têm um [manifesto próprio de hashes](manifesto-descritivo.json), separado dos manifestos originais do avaliador.

## Comandos efetivamente executados

Na raiz `D:\TCC-Projeto\TCC\tcc-impacto-llm`:

```powershell
python -B evidencias/spec004/avaliacao-extensao-0.3-D43/conferir_relatar.py conferir
python -B "D:\TCC-Projeto\TCC\tcc-impacto-llm\coletor_api.py" avaliar --lote "D:\TCC-Projeto\TCC\tcc-impacto-llm\captura\extensao-real-0.3-001" --referencia "D:\TCC-Projeto\TCC\tcc-impacto-llm\materiais\modelos\referencia_candidata_0.3_NAO_ENVIAR_AO_LLM.json" --saida "D:\TCC-Projeto\TCC\tcc-impacto-llm\avaliados\extensao-real-0.3-001-avaliacao-001"
python -B "D:\TCC-Projeto\TCC\tcc-impacto-llm\coletor_api.py" revisao-modelo --lote "D:\TCC-Projeto\TCC\tcc-impacto-llm\captura\extensao-real-0.3-001" --avaliacoes "D:\TCC-Projeto\TCC\tcc-impacto-llm\avaliados\extensao-real-0.3-001-avaliacao-001\lista.json" --observacoes "D:\TCC-Projeto\TCC\tcc-impacto-llm\avaliados\extensao-real-0.3-001-avaliacao-001\observacoes.json" --saida "D:\TCC-Projeto\TCC\tcc-impacto-llm\avaliados\extensao-real-0.3-001-avaliacao-001\revisao-conformidade-pendente.json"
python -B evidencias/spec004/avaliacao-extensao-0.3-D43/conferir_relatar.py relatar
```

As saídas existem e foram criadas sem sobrescrever anteriores; os comandos de criação não devem ser repetidos sobre os mesmos destinos. [Registro das execuções e retornos](../../evidencias/spec004/avaliacao-extensao-0.3-D43/comandos-executados.json). O shell retornou não zero para a avaliação, como esperado pelo bloqueio de conformidade; as 64 avaliações individuais estão completas. Uma primeira tentativa de relato foi recusada pelo controle de repetições duplicadas ao agregar células diferentes; o relato foi corrigido para manter Jaccard somente dentro de cada célula e médias por modelo ponderadas por V, sem mudar avaliador, critérios ou dados.
