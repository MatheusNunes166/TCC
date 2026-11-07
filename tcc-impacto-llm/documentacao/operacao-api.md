# Operação da rota API — integração offline D-39

Autorização vigente: integrar o patch anexado e verificar offline. **Não autoriza gasto, consulta autenticada, conexão real ou piloto.** Nenhum comando de envio foi executado nesta integração. O adaptador mantém comandos futuros sob `--enviar-real`; a presença deles não constitui autorização de uso. [Estado central](../ESTADO_ATUAL.md), [D-39](decisoes.md).

Base conferida antes da integração: branch `main`, commit `873f0a7285c4610335eda5c3a3d88ca2e13cdc8f`, árvore limpa. `git apply --check --verbose` aceitou o patch na raiz Git. Os três arquivos novos do diff não existiam. Código/testes novos foram extraídos e reconciliados; os textos históricos não foram aplicados automaticamente. O relato do patch sobre consulta de modelos, outra conversa ou outro Word não é evidência local e não gerou pendência nova. O desenho preservado é MC-01/MC-03 × D0/D1/E0/E1 × duas repetições, na ordem já registrada.

## Arquivos e fronteiras

- [coletor_api.py](../coletor_api.py): Responses API por biblioteca padrão; preparação, simulação, controle sintético, conexão neutra e coleta futura; avaliação importada somente no comando separado.
- [revisao_conformidade.py](../revisao_conformidade.py): decisões humanas separadas, hashes, exclusões e resumo revisado usando o avaliador existente.
- [testes originais do patch](../tests/test_coletor_api.py), [transporte](../tests/test_transporte_api.py), [revisão](../tests/test_revisao_conformidade.py).

O coletor Codex, sua trava e os planos D-38 permanecem literalmente preservados. A rota API possui versão, configuração e ID próprios, não continua lotes Codex nem transforma controle sintético em lote real. Requer Python/biblioteca padrão, sem SDK ou infraestrutura adicional. Os dados ficam em `captura/` e `avaliados/`, já protegidos por `-text -filter -ident`; não houve normalização dos originais ou mudança dessas regras.

O corpo da requisição tem exatamente `model`, `input`, `reasoning.effort`, `max_output_tokens`, `tools=[]`, `tool_choice=none`, `store=false`, `stream=false`. `input` contém todos os bytes textuais do payload UTF-8 v2-LF após decodificação/reconstrução conferida, inclusive o bloco de sistema original, mantendo a modalidade entre condições. Não acrescenta instructions, histórico, arquivos, código, gabarito ou instrução de reparo. Não força schema pela API além do schema textual existente. GPT-6 Sol (`gpt-6-sol`) e esforço `medium` são solicitados e registrados; modelo reportado permanece separado/desconhecido quando ausente. A garantia é sobre o cliente, sem promessa sobre mecanismos internos do provedor.

## Configuração e orçamento

Preparar plano e consultar ajuda/simulação não lê chave nem abre rede. `OPENAI_API_KEY` só é acessada na função de envio explícito, depois da autorização futura do pesquisador. Não se usam credenciais do Codex; nunca informar chave no chat, argv ou arquivo de evidência. Os testes de envio usam **chave fictícia e HTTP substituído em memória**.

`--orcamento-usd` registra uma declaração positiva: **não é teto monetário garantido**, não consulta saldo/preço e não implementa contador de gasto. `--limite` limita quantas observações a invocação tentará, não dólares. `timeout` controla espera, não garante que a geração remota parou. Os controles de faturamento disponíveis na conta precisam ser conferidos pelo pesquisador antes de autorizar uso real.

`--limite-saida` é obrigatório, sem valor de pesquisa padrão. O mínimo técnico validado pelo adaptador é 16; ele não define um valor cientificamente adequado. O limite abrange raciocínio e resposta final: um valor pequeno pode terminar como incomplete e consumir tokens sem texto final. Os exemplos **512/1024 do patch não foram adotados para o piloto**. O controle local preservado usa 512/declaração USD 1 apenas para testar arquivos, sem preço, consumo ou adequação científica inferidos. A escolha da pesquisa deverá ser explícita e gerar outro plano/configuração. Referências públicas conferidas com OpenAI Docs: [raciocínio e limite de saída](https://developers.openai.com/api/docs/guides/reasoning), [Responses API](https://developers.openai.com/api/reference/typescript/resources/responses).

## Preparação, simulação e controles sem rede

Da pasta `tcc-impacto-llm`:

```powershell
python -B coletor_api.py --help
python -B coletor_api.py simular --plano captura/integracao-api-2026-11-07/plano-api-controle/plano.json
```

Esse plano é exclusivamente de **controle offline**, com nova identidade API, oito payloads únicos e 16 posições copiadas de D-38. A semente original 20261106 controla somente a ordem; não há novo sorteio nem seed de modelo. As repetições mantêm os mesmos bytes/configuração. Não promover esse plano artificial a pesquisa por troca de nome/pasta.

Para criar um plano de pesquisa em diretório novo, somente depois de escolher e registrar parâmetros, usar o molde abaixo; os marcadores são valores a preencher, não comandos prontos para PowerShell:

```text
python -B coletor_api.py preparar --ordem captura/planejamento-piloto-2026-11-07-D38/plano.json --saida captura/plano-api-piloto-NOVO --limite-saida <TOKENS_PESQUISA_ESCOLHIDOS> --orcamento-usd <DECLARACAO_ESCOLHIDA> --timeout <SEGUNDOS_ESCOLHIDOS>
```

A preparação é offline e remonta autorizações/manifestos novos, sem mudar texto/notas da v2-LF. Mudança de código/configuração exige plano novo, sem editar hashes antigos. Para novo controle artificial e posterior avaliação independente:

```powershell
python -B coletor_api.py controle --plano captura/integracao-api-2026-11-07/plano-api-controle/plano.json --lote captura/controle-api-NOVO --limite 16
python -B coletor_api.py avaliar --lote captura/controle-api-NOVO --referencia materiais/modelos/referencia_candidata_NAO_ENVIAR_AO_LLM.json --saida avaliados/controle-api-NOVO
```

Controles têm `origem=sintetica`, `fase=verificacao_sintetica`, modelo reportado nulo e nunca entram no piloto. Os testes do ramo real usam metadados simulados apenas em temporários, claramente identificados como artificiais. `--continuar` em controle/conclusão íntegra pula observações já fechadas, sem repetir resposta inválida ou pontuação baixa.

## Conexão neutra futura — não executada

Após autorização **distinta** para uma chamada paga e chave configurada localmente, o comando seria:

```text
python -B coletor_api.py conexao --saida captura/conexao-api-NOVA --limite-saida <TOKENS_CONEXAO_ESCOLHIDOS> --enviar-real
```

Envia somente `Responda apenas OK.` com LF final, fora de qualquer observação. Sua fase é `verificacao_conexao`, explicitamente excluída de piloto/coleta principal. Não demonstra preço, saldo, referência validada ou adequação do limite do piloto. A capacidade real de gerar com GPT-6 Sol/medium permanece **não verificada**; nenhuma lista de `/v1/models` foi consultada nesta integração.

O envio futuro do piloto também exige autorização distinta, plano científico conferido e `--enviar-real`; exemplo apenas documental:

```text
python -B coletor_api.py iniciar --plano captura/plano-api-piloto-NOVO/plano.json --lote captura/piloto-api-NOVO --limite 1 --enviar-real
```

Essa operação enviaria a primeira observação real, não seria uma sondagem neutra. `--continuar` só avança após conclusões fechadas sem desvio, nunca retoma conversa ou repete observação concluída. Sem flag, iniciar/conexão recusam antes de consultar chave/rede.

## Transporte e preservação

HTTPS para endpoint fixo, contexto TLS padrão com verificação de certificado e hostname, redirects recusados e proxies herdados desativados. Não há loop de retry nem handler de autenticação que reenvie requests: uma abertura HTTP por tentativa. Isso não promete controle sobre mecanismos privados do provedor.

`IncompleteRead` e outras `http.client.HTTPException`, OSError de transporte e interrupções são tratados explicitamente. Preservam prefixo já lido, `partial` quando disponível, tipo da falha, status/request-id quando conhecidos e estado remoto desconhecido; o texto potencialmente sensível da exceção não é persistido. EOF anterior a Content-Length também é falha. Uma falha durante leitura do corpo de HTTPError recebe o mesmo tratamento. Defeitos de programação como TypeError/ValueError fora da validação do envelope não são ocultados como transporte.

Após falha/interrupção, **não há reenvio automático nem T02**; a continuação fica bloqueada. Isso respeita o máximo de uma retentativa técnica do protocolo, sem exigir que ela seja feita. Interrupção tratável fecha evidências parciais e retorna 130. Morte abrupta pode deixar início sem fechamento; esse estado também é bloqueado, sem presumir que nada foi enviado. Não remover tentativas ou editar registros para continuar. Se houve resposta íntegra com formato inválido/recusa, ela é preservada e avaliada, sem reparo ou nova chamada.

| Artefato | Local por observação `PIL-.../T01/` |
|---|---|
| Entrada e pacote original | `entrada.bin`, `preparacao/` |
| Requisição integral do cliente sem autenticação | `requisicao.json` (corpo), `http-requisicao.json` (método/URL/headers públicos/hash) |
| Resposta/fragmento HTTP original | `resposta-http.bin` ou `resposta-http-parcial.bin` |
| Status, identificador e falha | `transporte.json`, `tentativa.json` |
| Texto final sem trim, remoção de cercas ou reserialização | `resposta.bin` |
| Integridade | `fechamento.json` |

Authorization existe somente em memória. O corpo HTTP recebido é a evidência primária; o texto extraído não substitui esse original. A conexão neutra tem arquivos equivalentes e resultado/fechamento próprios, sem identidade de observação de piloto.

## Avaliação descritiva e revisão explícita de conformidade

O sucesso HTTP ou a resposta correta **não aprova conformidade**. Capturas reais começam pendentes/desvio. O comando avaliar reutiliza o avaliador atual, importa os originais e gera avaliação descritiva mesmo quando o resumo controlado fica bloqueado por revisão pendente (retorno 2 com diagnósticos no resumo). Não devolver resultados ao modelo.

Depois de uma captura real futura, em caminhos novos:

```text
python -B coletor_api.py avaliar --lote captura/piloto-api-NOVO --referencia materiais/modelos/referencia_candidata_NAO_ENVIAR_AO_LLM.json --saida avaliados/api-NOVO
python -B coletor_api.py revisao-modelo --lote captura/piloto-api-NOVO --avaliacoes avaliados/api-NOVO/lista.json --observacoes avaliados/api-NOVO/observacoes.json --saida avaliados/api-NOVO/decisoes-modelo.json
```

`revisao-modelo` apenas prepara decisões pendentes com hashes da avaliação, tentativa, fechamento, payload e resposta, vinculadas às fontes completas. Copiar o modelo para **arquivo novo**, por exemplo `saidas-locais/decisoes-preenchidas.json`. O pesquisador preenche `responsavel`, `data` ISO 8601 com fuso e, para cada observação disponível, `decisao=incluir|excluir|pendente` e justificativa. Conservar os hashes e fontes. A decisão de procedimento deve ser independente de acertos/escore; todas as capturas devem constar, inclusive falhas e exclusões.

```text
python -B coletor_api.py revisar --decisoes saidas-locais/decisoes-preenchidas.json --saida avaliados/api-NOVO/revisao-001.json
python -B coletor_api.py resumir-revisado --revisao avaliados/api-NOVO/revisao-001.json --saida avaliados/api-NOVO/resumo-revisado-001
```

O registro de revisão é separado, de criação exclusiva, com cópia literal da decisão preenchida e seu hash. Fontes/hashes são revalidados no resumo. Não se alteram capturas, tentativas, fechamentos ou avaliações. O avaliador recebe uma visão transitória explicitamente revisada; ela não é persistida como uma avaliação original “conforme”. Um desvio já registrado não pode ser convertido em conforme por essa revisão: excluir do resumo controlado ou discutir uma mudança explícita do protocolo fora desta operação.

Se alguma decisão continuar pendente, o resumo controlado permanece bloqueado (2). Com decisões completas, as métricas são das observações incluídas e válidas, conforme as mesmas fórmulas. `N_planejado_original` conserva todas as 16 posições; cada célula mostra também `contagens_operacionais_originais`, exclusões/justificativas/hashes e ausências reais separadas. Excluir uma captura não reduz silenciosamente N nem apaga dados. Resumo com exclusão/ausência retorna 1, com cobertura incompleta explícita; resumo elegível completo retorna 0. O arquivo `resumo.json` contém as tabelas.

## Verificações desta integração e próximos passos

[Base/diff](../captura/integracao-api-2026-11-07/base-integracao.json), [comandos, logs e hashes](../captura/integracao-api-2026-11-07/verificacao.json). Os 13 métodos originais do patch foram reproduzidos; o total final inclui controles adicionais de transporte e revisão, além das regressões que o patch citava. Nenhum resultado de teste é resposta de LLM. A evidência de HTTP aqui é somente simulada.

Antes de qualquer chamada paga faltam autorização operacional específica, configuração/limite que comporte raciocínio+final, preço/orçamento aceitável e acesso real na conta, conferência dos materiais/referência/política/medidas no alcance já registrado e revisão dos registros para elegibilidade. Não se adicionou pendência baseada em outro Word/conversa. A preparação API não resolve automaticamente esses pontos nem libera o piloto.
