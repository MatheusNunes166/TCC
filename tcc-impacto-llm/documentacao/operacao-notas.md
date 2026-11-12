# Operação do bloco de notas — D-47 a D-50

Integração de MC-04-v2 × Sol/Astra medium × direta/estruturada × N01/N02 × duas repetições. **16 capturas reais concluídas e avaliadas offline em D-50; 16 decisões de conformidade pendentes.** [Relatório, comparação e revisão](../avaliados/notas-mc04-real-001/RELATORIO.md). Estado e autorizações: [ESTADO_ATUAL](../ESTADO_ATUAL.md) e [decisões D-47 a D-50](decisoes.md). O pesquisador aprovou explicitamente o par e o plano integrado em D-48; a [preparação original 001](../captura/notas-mc04-0.3-001/REVISAO-PRIVADA.md) permanece literal.

## Plano e fontes

O [plano integrado 002](../captura/notas-mc04-0.3-002/plano.json) tem identidade funcional nova e vínculo ao hash do 001. Conserva os 16 IDs, ordem literal, notas, payloads, referência 0.3 e configurações. Os snapshots de preparação e os corpos de requisição foram copiados literalmente, pois o motor exige caminhos relativos contidos no diretório do plano. Não se criaram novas expectativas ou outra versão das notas.

[notas_exploratorias.py](../notas_exploratorias.py) coordena o motor de `coletor_api.capturar`, o avaliador e a revisão existentes; não implementa outro transporte ou novas fórmulas. Fontes anteriores de coletor/avaliador/revisão e do teste afetado foram preservadas literalmente em [fontes-anteriores](../evidencias/spec004/integracao-notas-0.3-D47/fontes-anteriores/), com os hashes do inventário inicial. Os produtores e planos antigos continuam históricos: conferidores que exigem os hashes antigos podem recusá-los com as fontes atuais. Reproduzir a versão antiga em ambiente separado usando esses arquivos, sem sobrescrever as fontes atuais. A integração confere a preparação 001 contra seu manifesto/hash original e as fontes atuais ou arquivadas de hash correspondente.

D-49 preserva o plano 002 byte a byte e revisa somente o adaptador para aceitar a decisão explícita de não definir orçamento. O [registro de atualização](../evidencias/spec004/autorizacao-sem-orcamento-notas-D49/atualizacao-fontes.json) liga hash do plano, hash da fonte anterior arquivada e hash da fonte atual; seu próprio hash consta da autorização específica. A compatibilidade é restrita a esse plano e a essa fonte; as demais fontes continuam exigindo os hashes originais. Não há aceitação genérica de fontes alteradas ou substituição dos hashes do plano.

## Identidade e denominadores

`nota_id` e `bloco_exploratorio` são preservados no plano, tentativa, início local, avaliação, ficha e resumo. A entrada da API permanece só o payload; não recebe IDs de nota, rótulos, mapa privado ou esta documentação. `modelo` e estrutura D1/E1 são preservados nos registros e rótulos das células.

O resumo usa **modelo/configuração × estrutura × nota_id**, oito células com N=2, um par de Jaccard por célula se ambas as respostas forem válidas. Validade, requisitos/testes, TP/FN/FP, métricas e consistência seguem as funções existentes; a política de pontuação e o hash de suas regras não foram reformulados. Não agregar N01/N02, planos distintos ou as 64 observações anteriores. Misturas, fatores ausentes, nota trocada ou cadeia inválida são recusados.

O motor conserva requisição, entrada, envelope HTTP, resposta/fragmento, falha, tentativa e fechamento por hash. Continuação pula conclusões íntegras, inclusive respostas de formato inválido; não faz reparo, reenvio ou retry automático. Falha, estado ambíguo, desvio ou identidade divergente bloqueiam a retomada. `--limite` conta tentativas novas da invocação, não dólares.

## Simulação somente de leitura

Comando absoluto, independente da pasta corrente:

```powershell
python -B "D:\TCC-Projeto\TCC\tcc-impacto-llm\notas_exploratorias.py" simular --plano "D:\TCC-Projeto\TCC\tcc-impacto-llm\captura\notas-mc04-0.3-002\plano.json"
```

Não lê chave, não cria lote e não abre rede. A primeira observação da ordem preservada é **NOTA03-MC-04-v2-D1-N02-ASTRA-R01**. O comando não envia essa observação.

## Autorização específica e comando histórico de somente uma observação

O plano integrado mantém literalmente `envio_autorizado=false`; a autorização é externa. O [modelo separado](../captura/notas-mc04-0.3-002/autorizacao-modelo.json) continua original, com campos nulos/flags falsas. Em D-48 o pesquisador aprovou o par/plano e autorizou as chamadas. Em D-49 decidiu prosseguir sem definir orçamento monetário, reconhecendo chamadas pagas e aceitando a ausência de teto automático. O [registro específico](../captura/autorizacao-notas-mc04-001.json) conserva nome, data da aprovação inicial e flags verdadeiras; acrescenta a declaração D-49 com data/fuso e mantém **`orcamento_usd=null`**. A validação offline agora aceita esse registro. A disponibilidade da credencial local não foi reconferida em D-49; a última verificação em D-48 indicava ausência.

O registro específico fica fora do diretório imutável do plano, preservando versão e hash. Continuam obrigatórios `responsavel`, `data` ISO 8601 com fuso, `justificativa`, `revisao_par_pacotes_ordem=true`, `autoriza_envio_real=true` e o campo `orcamento_usd`. Esse campo aceita valor próprio positivo/finito ou **nulo somente com `decisao_sem_orcamento` completa**: `prosseguir_sem_definir_orcamento=true`, `reconhece_chamadas_pagas=true`, `aceita_ausencia_teto_automatico=true`, mesmo responsável da autorização, data com fuso e declaração textual não vazia. Ausência de campo, decisão incompleta, flags falsas ou apenas texto livre não dispensam o orçamento. Valores zero, negativos ou não finitos continuam recusados. A autorização do plano 002 também exige `atualizacao_fontes_sha256` coincidente com o registro D-49.

USD 2 nas configurações continua exclusivamente histórico. Não há teto automático de cobrança. A chave deve estar disponível no ambiente local para uso futuro; a primeira invocação deve usar somente `--limite 1` e aguardar a conferência técnica determinada em D-48. D-49 autoriza apenas o ajuste e verificações offline neste atendimento.

O comando abaixo foi apresentado antes da coleta para enviar somente a primeira observação. **O lote está completo em D-50; não executar novamente para este lote.** O atendimento D-50 fez somente conferência/avaliação offline, sem envio:

```powershell
python -B "D:\TCC-Projeto\TCC\tcc-impacto-llm\notas_exploratorias.py" iniciar --plano "D:\TCC-Projeto\TCC\tcc-impacto-llm\captura\notas-mc04-0.3-002\plano.json" --lote "D:\TCC-Projeto\TCC\tcc-impacto-llm\captura\notas-mc04-real-001" --limite 1 --enviar-real --autorizacao "D:\TCC-Projeto\TCC\tcc-impacto-llm\captura\autorizacao-notas-mc04-001.json"
```

Sem `--enviar-real`, `--limite` válido, autorização, revisão verdadeira, orçamento positivo ou decisão explícita completa para nulo, ou hashes corretos, o envio é recusado antes de acessar a chave/criar lote/abrir transporte. A autorização efetiva foi arquivada literalmente, ligada por hash ao cabeçalho e às tentativas, incluindo a decisão de prosseguir sem orçamento; o cabeçalho conserva o orçamento novo nulo, separado dos metadados históricos. Chave somente no ambiente local `OPENAI_API_KEY`, nunca no chat ou argv. Em lote parcial, `--continuar` exige a mesma autorização vinculada e pula conclusões íntegras; não há continuação pendente neste lote completo.

## Controle artificial e avaliação offline

Os testes executados usam apenas temporários, chave fictícia e HTTP substituído, com conexões/DNS bloqueados. Para um controle manual adicional, usar destinos novos e claramente artificiais; os exemplos abaixo não foram executados sobre dados reais:

```powershell
python -B notas_exploratorias.py controle --plano captura/notas-mc04-0.3-002/plano.json --lote captura/CONTROLE-ARTIFICIAL-notas-NOVO --limite 16
python -B notas_exploratorias.py avaliar --lote captura/CONTROLE-ARTIFICIAL-notas-NOVO --referencia materiais/modelos/referencia_candidata_0.3_NAO_ENVIAR_AO_LLM.json --saida avaliados/CONTROLE-ARTIFICIAL-notas-NOVO
```

`controle` não lê chave nem usa rede; grava `origem=sintetica`, fase de verificação e modelo reportado nulo. Sua resposta substituta padrão é artificial, não resultado de LLM. `avaliar` abre a referência exclusivamente nessa etapa separada e usa o mesmo fluxo para lote artificial ou futuro lote real. Cada avaliação terá `nota_id`, bloco e hash do plano. Ausências e falhas conservam N planejado original; não viram listas vazias observadas ou respostas inventadas. Os IDs não permitem afirmar reconhecimento explícito da contradição.

## Avaliação executada e conformidade separada

D-50 executou `notas_exploratorias.py avaliar --lote captura/notas-mc04-real-001 --referencia materiais/modelos/referencia_candidata_0.3_NAO_ENVIAR_AO_LLM.json --saida avaliados/notas-mc04-real-001` e o comando de modelo abaixo. Os destinos já existem e não devem ser sobrescritos/repetidos. Resultado: oito células N=2, 16 válidas, nenhuma falha/inválida; seleção igual entre N01/N02 e à referência em requisitos/testes. [Tabela e limitações](../avaliados/notas-mc04-real-001/RELATORIO.md). A ficha pendente está pronta para revisão humana; os dois comandos de registro/resumo revisado continuam futuros.

Capturas começam pendentes/desvio, independentemente de HTTP ou escore. A avaliação real individual é produzida com a pendência preservada; o resumo controlado fica bloqueado (retorno 2) até revisão própria. Reutilizar os comandos existentes, após eventual captura/avaliação e em destinos novos:

```powershell
python -B coletor_api.py revisao-modelo --lote captura/notas-mc04-real-001 --avaliacoes avaliados/notas-mc04-real-001/lista.json --observacoes avaliados/notas-mc04-real-001/observacoes.json --saida avaliados/notas-mc04-real-001/revisao-conformidade-pendente.json
python -B coletor_api.py revisar --decisoes avaliados/notas-mc04-real-001/decisoes-preenchidas.json --saida avaliados/notas-mc04-real-001/revisao-001.json
python -B coletor_api.py resumir-revisado --revisao avaliados/notas-mc04-real-001/revisao-001.json --saida avaliados/notas-mc04-real-001/resumo-revisado-001
```

O preenchimento humano é separado da ficha original e conserva decisões individuais ligadas a hashes, `nota_id`, bloco e plano. O resumo revisado também conserva oito células, exclusões por nota, contagens originais e N=16; métricas somente para respostas incluídas e válidas. Nenhuma revisão ou exclusão das 64 observações anteriores decorre desta integração. Seus registros e sua ficha continuam pendentes e intocados.
