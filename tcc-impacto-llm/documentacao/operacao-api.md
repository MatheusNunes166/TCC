# Operação da rota API — integração offline D-39

Situação e pendências vigentes: [estado atual](../ESTADO_ATUAL.md). Este é o procedimento do adaptador integrado em D-39; exemplos com caminhos NOVO/NOVA não autorizam envio. A integração foi offline; evidências de base, patch e 52 testes estão em [D-39](decisoes.md) e [verificação](../captura/integracao-api-2026-11-07/verificacao.json). Os registros reais posteriores são localizados pelo estado central.

## Envio da extensão 0.3 — D-42

Integração solicitada pelo pesquisador, validada sem chamadas reais. O novo comando `iniciar` exige `--enviar-real`, `--limite` inteiro entre 1 e 64 e um plano D-42. `--continuar` retoma o mesmo lote/plano sem reenviar conclusões; falha, estado remoto desconhecido ou desvio bloqueiam reenvio automático. A chave é lida de `OPENAI_API_KEY`, sem persistir seu valor. O orçamento de planejamento **USD 2 refere-se à rodada inteira**; o mesmo valor nas duas configurações é metadado compartilhado, sem somar dois orçamentos, contador automático ou garantia de teto. O pesquisador declarou aceitar esse risco.

Plano vigente 003, gerado pelo preparador com `--origem` 002, preserva as 64 observações, ordem literal e payloads. Modelo/configuração são selecionados em cada linha; ambos usam medium e 4096. Capturas reais têm `origem=real`, `fase=exploratoria`, etapa da extensão, configuração e hashes. Não reutilizar lote do piloto ou de controle. A fonte e a trava do coletor Codex CLI permanecem intactas.

Primeira observação somente — `EXT03-MC-04-v2-E1-SOL-R01`:

```powershell
python -B "D:\TCC-Projeto\TCC\tcc-impacto-llm\extensao_exploratoria.py" iniciar --plano "D:\TCC-Projeto\TCC\tcc-impacto-llm\captura\extensao-20261109-003\plano.json" --lote "D:\TCC-Projeto\TCC\tcc-impacto-llm\captura\extensao-real-0.3-001" --limite 1 --enviar-real
```

Continuação para somente **uma próxima observação pendente**, caso a anterior esteja concluída sem desvio:

```powershell
python -B "D:\TCC-Projeto\TCC\tcc-impacto-llm\extensao_exploratoria.py" iniciar --plano "D:\TCC-Projeto\TCC\tcc-impacto-llm\captura\extensao-20261109-003\plano.json" --lote "D:\TCC-Projeto\TCC\tcc-impacto-llm\captura\extensao-real-0.3-001" --limite 1 --continuar --enviar-real
```

`--limite` é a quantidade máxima **nova por invocação**, não a posição final da ordem nem um limite em dólares. Nenhum desses comandos foi executado nesta implementação. A avaliação permanece separada, após haver capturas, com saída nova por avaliação:

```powershell
python -B "D:\TCC-Projeto\TCC\tcc-impacto-llm\coletor_api.py" avaliar --lote "D:\TCC-Projeto\TCC\tcc-impacto-llm\captura\extensao-real-0.3-001" --referencia "D:\TCC-Projeto\TCC\tcc-impacto-llm\materiais\modelos\referencia_candidata_0.3_NAO_ENVIAR_AO_LLM.json" --saida "D:\TCC-Projeto\TCC\tcc-impacto-llm\avaliados\extensao-real-0.3-001-avaliacao-001"
```

O resumo controlado continua bloqueado enquanto houver revisão de conformidade pendente; a revisão separada existente passa a aceitar a fase exploratória identificada. [D-42, resultados e preservação](../evidencias/spec004/integracao-envio-extensao-2026-11-09-D42/RELATORIO.md). Os comandos e a trava D-41 abaixo são históricos, anteriores a essa integração; não editar os planos antigos para fazê-los passar pelo conferidor novo.

## Extensão 0.3 — preparação D-41

`extensao_exploratoria.py` reutiliza o motor API para a nova configuração de 64 posições, em ordem intercalada entre os modelos. `gpt-6-sol`/medium e `gpt-6-astra`/medium têm IDs próprios; limite comum 4096, sem fallback e sem orçamento declarado automaticamente. As capturas de controle sempre têm origem sintética, modelo efetivamente reportado nulo e envelopes explicitamente artificiais. A extensão não oferece comando de envio real; o motor também bloqueia essa opção antes de acessar credencial. Referência privada é aberta somente na avaliação separada.

Na raiz do projeto, simulação somente de leitura:

```powershell
python -B extensao_exploratoria.py simular --plano captura/extensao-20261109-002/plano.json
```

Controle ARTIFICIAL e retomada em diretório novo (não são observações da pesquisa):

```powershell
python -B extensao_exploratoria.py controle --plano captura/extensao-20261109-002/plano.json --lote captura/CONTROLE-ARTIFICIAL-ext03-NOVO --limite 17
python -B extensao_exploratoria.py controle --plano captura/extensao-20261109-002/plano.json --lote captura/CONTROLE-ARTIFICIAL-ext03-NOVO --limite 47 --continuar
python -B coletor_api.py avaliar --lote captura/CONTROLE-ARTIFICIAL-ext03-NOVO --referencia materiais/modelos/referencia_candidata_0.3_NAO_ENVIAR_AO_LLM.json --saida avaliados/CONTROLE-ARTIFICIAL-ext03-NOVO
```

Preparações e avaliações nunca sobrescrevem diretórios existentes. O plano preserva 64 linhas planejadas; controles não o promovem a executado. Para preparar outra identidade após mudança de fontes, usar `python -B extensao_exploratoria.py preparar --saida captura/extensao-NOVA`. Não editar hashes de planos existentes. Reprodução do coletor anterior: fontes literais em `evidencias/spec004/extensao-2026-11-09/fontes-anteriores/`, com hashes do inventário inicial; as recusas por hash do script atual são deliberadas.

[Referência candidata, conjuntos e justificativas](referencia-candidata-0.3.md); [verificações, preços e pendências](../evidencias/spec004/extensao-2026-11-09/RELATORIO.md). O restante deste documento conserva o procedimento da versão anterior.

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

## Operações reais — autorização própria

Após autorização **distinta** para uma chamada paga e chave configurada localmente, o comando seria:

```text
python -B coletor_api.py conexao --saida captura/conexao-api-NOVA --limite-saida <TOKENS_CONEXAO_ESCOLHIDOS> --enviar-real
```

Envia somente `Responda apenas OK.` com LF final, fora de qualquer observação. Sua fase é `verificacao_conexao`, explicitamente excluída de piloto/coleta principal. Não demonstra preço, saldo, referência validada ou adequação do limite do piloto. A evidência da conexão já realizada está no [estado atual](../ESTADO_ATUAL.md); nenhuma lista de `/v1/models` foi consultada na integração D-39.

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

Para avaliar capturas e preparar uma revisão, usar caminhos novos. O lote real existente já foi avaliado; localizar seus arquivos no [estado atual](../ESTADO_ATUAL.md) antes de executar qualquer comando:

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

Pendências atuais e próximos passos: [estado atual](../ESTADO_ATUAL.md#próximas-tarefas-e-limites). Exemplos operacionais não autorizam chamadas pagas nem coleta principal. Não repetir comandos sobre caminhos existentes ou editar registros para ultrapassar bloqueios.
