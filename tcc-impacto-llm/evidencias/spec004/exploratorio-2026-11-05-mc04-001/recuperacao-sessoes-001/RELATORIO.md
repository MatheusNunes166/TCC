# Recuperação literal e avaliação descritiva — MC-04

Registro: 06/11/2026. **Quatro entradas textuais completas e seus finais recuperados; histórico preliminar adicional de D0 também preservado.** Nenhuma nova chamada ou mensagem foi enviada às conversas experimentais. Fase exploratória, excluída do piloto e da coleta principal.

## Escopo e identificação

Foi consultado o índice local `state_5.sqlite` com `mode=ro` e `query_only=ON`, apenas para metadados de localização. O cwd aparece como `\\?\D:\Tcc-ensaio`; removido esse prefixo de representação do Windows, corresponde à pasta informada. O filtro encontrou exatamente quatro sessões `gpt-6-astra` / `medium`. Somente os quatro históricos correspondentes foram abertos; não foram consultados corpos de outras conversas. [Índice filtrado](indice-sessoes-filtrado.json).

Cada condição foi identificada pelo bloco de texto efetivamente presente na mensagem, comparado unicamente aos quatro payloads preparados, **antes de ler a referência de avaliação**. Ordem/título não definiram a condição. Para essa identificação foram consideradas equivalentes apenas CRLF/LF e quebras LF terminais; as cópias reais não foram normalizadas. Todos os blocos documentais correspondem à condição indicada; não foi necessário reconstruir qualquer resposta.

| Condição | ID da sessão | Linhas da mensagem / final no JSONL | Data/hora da mensagem, UTC−03 | Cópias literais |
|---|---|---|---|---|
| D0 | `01a1aeb3-83c5-7f20-b121-c20efd4d2a6e` | 38 / 42 | 2026-11-05T23:37:51.727000-03:00 | [entrada](D0/mensagem-enviada.txt) · [final](D0/resposta-final.txt) |
| D1 | `01a1aeba-14c8-7121-903e-99a6d6a054ae` | 12 / 15 | 2026-11-05T23:39:56.199000-03:00 | [entrada](D1/mensagem-enviada.txt) · [final](D1/resposta-final.txt) |
| E0 | `01a1aebb-667a-7623-b559-1fdaa6091f35` | 12 / 16 | 2026-11-05T23:41:21.224000-03:00 | [entrada](E0/mensagem-enviada.txt) · [final](E0/resposta-final.txt) |
| E1 | `01a1aebc-26c9-7702-9200-143d39f2c127` | 12 / 16 | 2026-11-05T23:42:10.752000-03:00 | [entrada](E1/mensagem-enviada.txt) · [final](E1/resposta-final.txt) |

A ordem temporal dos **envios textuais completos** confirma D0 → D1 → E0 → E1. As datas originais em UTC são 06/11/2026, entre 02:37 e 02:42; em America/Sao_Paulo (UTC−03), correspondem à noite de **05/11/2026**. Não se usou o nome do arquivo ou a data desta recuperação como data das execuções. IDs de turno, timestamps UTC e hashes estão em [identificacao.json](identificacao.json) e nos registros por condição.

## O que foi preservado

- `origens/<sessao-id>.jsonl`: cópia byte a byte de cada histórico, com hash igual ao arquivo de origem antes/depois da leitura.
- `<condicao>/mensagem-enviada.txt`: campo textual integral da mensagem do usuário, incluindo o prefixo da IDE.
- `<condicao>/payload-enviado.txt`: trecho literal a partir do primeiro delimitador do sistema até o fim da mensagem; sem remover quebras ou acrescentar caracteres.
- `<condicao>/resposta-final.txt`: texto final literal, em UTF-8, sem reserializar JSON, remover cercas ou acrescentar newline. D0/D1 mantêm a forma compacta; E0/E1 mantêm a indentação recebida.
- Linhas JSONL originais das mensagens/finais, metadados e eventos por condição; todos os cinco finais também em `todos-os-finais/`.
- `D0/preliminar/`: mensagem por referência a anexo, primeiro retorno, anexo original e proveniência, além da avaliação separada desse retorno.

O texto recuperado é a sequência de caracteres dos campos dos registros locais, com sua serialização original preservada no JSONL. Não é uma captura de bytes HTTP nem prova de todo contexto interno do provedor. A existência atual do anexo não prova que seu conteúdo tenha sido fornecido ao modelo no primeiro turno.

## Desvios observados — não declarar conformidade integral

1. **Todos os envios incluem prefixo da IDE**, de 94 bytes, mencionando a aba `config.toml`, além dos blocos preparados. Os registros também contêm mensagens de ambiente e instruções da plataforma. O conteúdo dessas mensagens permanece no snapshot, sem ser confundido com o payload autorizado. Não foi lido o arquivo de configuração externo para completar fatos ausentes.
2. **Não há igualdade byte a byte entre payload preparado e trecho enviado.** O texto passou de CRLF a LF e recebeu um LF terminal adicional. Os preparados têm 26 CRLF em D0/E0 e 27 em D1/E1; os trechos enviados têm zero CRLF. Os blocos têm o mesmo conteúdo textual, mas isso não apaga a diferença dos originais. [Confronto](confronto-entradas-reais.json).
3. **D0 tem dois turnos concluídos.** Primeiro houve referência a `Pasted text.txt`; o modelo respondeu que não recebeu o conteúdo e pediu que fosse colado. O envio textual completo veio depois, na mesma sessão, portanto já tinha histórico. Ambos os retornos foram preservados. Não é uma execução única em contexto vazio nem uma retentativa técnica com conteúdo idêntico.
4. **Houve ferramentas em D0 antes do envio completo:** três chamadas de `functions.exec`, para descobrir ferramentas e consultar recursos/templates MCP. Os eventos estão em `D0/eventos-ferramentas.json`; não são chamadas realizadas por esta recuperação. Não há chamadas de ferramentas registradas no turno do payload completo de D0 nem nas outras três sessões; isso **não comprova indisponibilidade de ferramentas** ou impossibilidade de acesso ao ambiente. Não há evidência de consulta ao gabarito, o que também não equivale a garantia de impedimento de acesso.

Nos trechos efetivamente enviados, os documentos comuns são iguais entre condições; notas só em D1/E1, com mesmo texto; pedidos iguais em D0/D1 e E0/E1, conforme os prompts. Essas igualdades não demonstram controle de todo o contexto da interface.

## Avaliação descritiva das respostas reais

Foi reutilizada `avaliacao_ids.avaliar_resposta`, com origem `llm_exploratoria`. A CLI sintética não foi utilizada ou modificada. Referência candidata 0.2, `CANDIDATO_NAO_REVISADO`; política `ids-proposta-004-v2`, ainda candidata à revisão científica. Referência e fonte do avaliador foram copiadas para a pasta local de avaliação, com hashes conferidos. Não retornaram ao modelo.

**Adequação explícita do procedimento:** o comando integral de AVALIAR.md exige igualdade de hashes do preparado/enviado e presume um registro concluído por observação; os históricos recuperados não satisfazem essas premissas. Não se forçaram hashes ou estados para passar nas asserções. A pontuação abaixo examina somente os bytes dos finais recuperados com o comparador existente, como descrição de conteúdo, **sem promover esses registros a observações conformes para um resumo controlado**.

O vínculo com o final de cada envio textual foi determinado pelo turno do payload, antes de consultar o gabarito. Não é escolha pela melhor resposta. Para D0, o primeiro retorno permanece separado e o resumo de uma única observação da célula está **bloqueado**, conforme a convenção candidata de não selecionar silenciosamente entre retornos duplicados.

| Final examinado | Formato | RFs: acertos / omissões / excedentes | Testes: acertos / omissões / excedentes | Evidência |
|---|---|---|---|---|
| D0 (turno do texto integral) | valido | 2 / 0 / 0 | 5 / 0 / 0 | [avaliação](D0/avaliacao-descritiva-001.json) |
| D1 | valido | 2 / 0 / 0 | 5 / 0 / 0 | [avaliação](D1/avaliacao-descritiva-001.json) |
| E0 | valido | 2 / 0 / 0 | 5 / 0 / 0 | [avaliação](E0/avaliacao-descritiva-001.json) |
| E1 | valido | 2 / 0 / 0 | 5 / 0 / 0 | [avaliação](E1/avaliacao-descritiva-001.json) |

Nos quatro finais ligados aos envios textuais completos: requisitos selecionados `RF-03, RF-04`; testes `T05, T07, T08, T10, T12`. Coincidem com a candidata: omissões, excedentes, desconhecidos e duplicatas vazios nas duas dimensões. As medidas P/R/F1 propostas resultam em 1 nesses finais, sem aprovação científica atribuída à aritmética.

O **retorno preliminar adicional de D0** é texto fora do JSON: `resposta_formato_invalido`, com requisitos/testes e escores observados nulos, sem imputação ou substituição pelo retorno posterior. [Avaliação preliminar](D0/preliminar/avaliacao-descritiva-001.json). Não se calcula uma taxa global de validade misturando os cinco retornos como se fossem quatro execuções independentes.

A tabela permite descrever os finais, mas não demonstrar benefício de notas ou estrutura. Não há resumo agregado, teste estatístico, estimativa de efeito ou cálculo de consistência/Jaccard. O turno extra de D0 não é uma repetição independente. [Resumo de conteúdo e limites](avaliacao/resumo-descritivo.json).

## Metadados realmente disponíveis

| Condição | Timestamp do final, UTC−03 | Duração da tarefa reportada (ms) | Tokens input/output do turno reportados |
|---|---|---|---|
| D0 | 2026-11-05T23:37:55.131000-03:00 | 3524 | 15270 / 66 |
| D1 | 2026-11-05T23:39:59.094000-03:00 | 4565 | 13877 / 36 |
| E0 | 2026-11-05T23:41:25.701000-03:00 | 5132 | 13805 / 75 |
| E1 | 2026-11-05T23:42:14.051000-03:00 | 4049 | 13892 / 83 |

Valores copiados de `task_complete` e `token_usage_record`, identificados por turno; não são durações estimadas, custo, tempo isolado de inferência ou contagem do texto do payload. Tokens podem incluir instruções, contexto e tokens de raciocínio; campos de cache/raciocínio e IDs de resposta permanecem nos eventos, sem somar contadores acumulados. D0 usa aqui somente o turno do texto completo; os quatro eventos de uso e a duração da etapa preliminar continuam preservados separadamente.

Modelo e esforço constam dos `turn_context`: `gpt-6-astra`, `medium`; versão de build do modelo, temperatura, top_p, seed e custo não estão estabelecidos e permanecem desconhecidos. IDs de sessão/turno, cwd, versão CLI disponível no índice, permissões declaradas, timestamps e eventos de ferramentas estão preservados; permissões declaradas não demonstram isolamento por SO ou ausência de capacidade de acesso.

## Preservação, falhas locais e pendências

[preservacao.json](preservacao.json) confere as origens, o anexo, todos os arquivos anteriores do ensaio e as fontes protegidas, sem divergências. Fichas `AGUARDANDO_ORIGINAL` e o relatório de recebimento anterior são históricos, não foram sobrescritos; esta recuperação resolve a falta dos arquivos, mas não corrige retrospectivamente seus desvios. Notas/prompts/gabarito e módulos não foram alterados; revisão profissional/científica e notas definitivas continuam pendentes.

A primeira execução de `recuperar.py` preservou entradas/saídas e parou antes de avaliar por um caminho de importação Python. A continuação identificada em `avaliar-recuperados.py` corrigiu apenas a localização do módulo existente e concluiu a comparação. [Diagnóstico preservado](falha-primeira-avaliacao.txt). Esse erro local não foi atribuído ao modelo, convertido em seleção vazia ou pontuado como zero.

Não falta nenhuma das quatro entradas textuais ou respostas finais. Permanecem limites de evidência sobre o contexto completo, disponibilidade de ferramentas, recepção efetiva do anexo inicial e parâmetros/custo não reportados. Para tratar D0 como uma observação única de experimento controlado, seria necessária resolução explícita do pesquisador sobre os dois turnos e a elegibilidade, sem escolher automaticamente um retorno. **Nenhuma nova execução foi proposta ou feita para substituir esses dados.** Resultados mantidos exclusivamente como exploratórios, sem incorporação automática ao piloto/coleta principal.
