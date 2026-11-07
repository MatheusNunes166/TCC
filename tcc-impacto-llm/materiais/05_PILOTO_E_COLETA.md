# 5. Do piloto à coleta principal

## 5.1 Antes do piloto

Atualização de catálogo (D-15): 12 testes, 48 pares teste × mudança, 60 expectativas incluindo a versão inicial. Baseline T01–T12 e quatro variantes já implementadas/verificadas em D-20/D-21 (12/12 e 48/48 pares por decisão/motivo). Não repetir toda a bancada sem alteração que o justifique. Referência 0.2 candidata, sem revisão científica concluída.

O piloto só começa quando a baseline existe, a referência está revisada, os prompts/notas estão versionados e a coleta registra payload e resposta originais. A versão inicial e as variantes já foram verificadas; a revisão própria declarada em D-35 deve ter seu alcance documentado sem preencher aprovações individuais. Os demais critérios e a conferência do novo texto permanecem necessários. Documentação preparada não prova implementação da coleta nem libera piloto.

Checklist de entrada:
- [ ] Definições de impacto e seleção aprovadas; MC-04-v2 aceita ou referência reescrita.
- [ ] Baseline e quatro variantes conferidas contra expectativas humanas.
- [ ] Alcance da revisão própria do pesquisador, versão, data e divergências registrados; sem revisor externo nesta etapa. A declaração geral de D-35 não aprova automaticamente cada expectativa.
- [ ] Conferência do novo texto 0.2-local e dos payloads pelo pesquisador; autoria e apoio de IA registrados. A reformulação posterior ao exploratório conhecido é uma limitação explícita.
- [ ] Mesmo modelo, configuração, pacote e modalidade por condição.
- [ ] Ambiente avaliado sem acesso ao gabarito, histórico, indexação ou ferramentas extras.
- [ ] Parser e pontuação conferidos com exemplos sintéticos conhecidos, incluindo vazio e todos os testes.
- [ ] Orçamento e registros de falha definidos.

## 5.2 Ensaio proposto: 16 chamadas

Usar MC-01 (direta) e MC-03 (propagada), quatro condições e duas repetições: **2 × 4 × 2 = 16**. Essas mudanças representam tamanhos de seleção distintos e permitem exercitar notas, omissões e preservação. Cada chamada começa em contexto independente.

Em cada repetição, embaralhar a ordem das oito combinações de mudança/condição e guardar a ordem e a semente usada. Não reutilizar a resposta anterior como contexto. Semente da ordem não implica controle da aleatoriedade do provedor.

Objetivo: verificar formato, registros, isolamento, orçamento, clareza operacional e cálculo. Não escolher a melhor condição nem provar efeito com dezesseis respostas. Como dois casos reaparecem na coleta principal, o piloto não é um conjunto de teste independente: declarar essa reutilização e evitar ajustar prompts para ensinar os IDs que o modelo errou.

## 5.3 Critérios para prosseguir

| Verificação | Evidência exigida | Se falhar |
|---|---|---|
| Rastreabilidade | 16 tentativas planejadas com IDs, payloads, respostas/erros e hashes | Corrigir registro e repetir o ensaio afetado |
| Isolamento | Inspeção dos payloads: nenhum gabarito/histórico; notas só onde previsto | Invalidar o ensaio contaminado e corrigir montagem |
| Referência | Nenhuma divergência substantiva pendente entre regra, expectativa e revisão | Rever antes de pontuar a coleta principal |
| Avaliador | Exemplos conhecidos produzem os números esperados | Corrigir o cálculo e reavaliar registros preservados |
| Formato | Taxa de validade medida e causas conhecidas | Falha de integração deve ser corrigida; falha do modelo pode permanecer como resultado |
| Viabilidade | Tempo, consumo disponível e custo do ensaio registrados | Ajustar plano uniformemente, antes da coleta |

Não exigir F1 mínimo para liberar a coleta. Uma condição errar pode ser justamente o fenômeno a observar. Aprovação do piloto significa procedimento utilizável, não IA bem-sucedida.

## 5.4 Relatório do piloto — preencher após executar

Data e responsável; versões; condições executadas; válidas/total; falhas técnicas; exemplos de problemas de coleta; ambiguidades encontradas; tempo/custo observado; alterações propostas; justificativa de cada alteração; quem revisou; decisão de prosseguir.

Alterações admissíveis: corrigir truncamento, contrato ambíguo, parser, log ou erro comprovado da referência. Não adicionar pistas específicas para elevar o desempenho de uma condição. Aplicar correções comuns de modo igual; alterações de prompts/notas/referência pedem novo ensaio das combinações afetadas e identificação da nova versão. Dados exploratórios nunca migram para a planilha principal.

## 5.5 Congelamento antes da coleta principal

Preencher `modelos/manifesto_congelamento.json` com valores reais; campos nulos indicam pendência. Congelar: baseline, quatro mudanças escolhidas, suíte, política de seleção, referência, notas, prompts, mensagem de sistema, esquema, código do avaliador, modelo/configuração, ordem planejada, tratamento de falhas e quantidade de repetições.

Proposta inicial: cinco repetições por mudança/condição, total de 80 chamadas principais. Confirmar após o piloto por viabilidade e objetivo descritivo. Cinco não é cálculo de poder estatístico nem garantia de generalização. Registrar eventual mudança de quantidade antes de olhar resultados principais.

## 5.6 Executar em lotes e monitorar

Planejar cinco blocos de dezesseis chamadas: cada bloco contém as quatro mudanças nas quatro condições, em ordem aleatorizada e registrada. Uma sessão por chamada. Os blocos organizam o acompanhamento; não são dezesseis passos de uma conversa.

Ao fechar cada bloco, verificar integridade, contagem, payloads, modelo informado, truncamentos e arquivos faltantes. Não editar prompts/notas com base no placar parcial. Guardar custo/latência como dados operacionais opcionais, sem atribuir-lhes papel de desfecho principal.

Interromper o protocolo se houver vazamento, mudança de versão do modelo identificada ou referência incorreta. Registrar desvio e definir nova versão/coorte; não misturar silenciosamente execuções incompatíveis. Uma troca necessária não pode ser escondida como simples repetição.

## 5.7 Dados de cada execução

Usar `modelos/registro_execucao.json` como estrutura, sem confundir campos nulos com resultados. Registrar: ID, fase, bloco, ordem, mudança, condição, repetição, instante, configuração real, versões/hashes, payload e resposta originais, status técnico, validade, listas extraídas, duplicatas/IDs desconhecidos, TP/FP/FN e escores separados. Se custo/tokens não estiverem disponíveis, usar nulo, não zero.

Dados sintéticos usados para verificar o avaliador devem ter fase `verificacao_sintetica`, nunca `principal`. Respostas reais usam origem `real`, fase `exploratoria`, `piloto` ou `principal` e repetição própria; não converter exploratório em piloto. A CLI aceita os dois tipos explicitamente, em listas e diretórios separados. Não há respostas do piloto preenchidas neste pacote.

## 5.8 Entregas finais esperadas

Uma tabela por mudança/condição com qualidade e variabilidade; uma tabela de omissões/excedentes; comparações planejadas de estrutura e notas; registro de falhas; discussão das limitações. Relatar também ausência de diferença ou resultados desfavoráveis. Entregar o protocolo e os artefatos versionados para permitir repetição no mesmo recorte, sem alegar desempenho geral de LLMs.

## 5.9 Tabela proposta e configuração — D-35, 06/11/2026
São **16 chamadas propostas**, distintas dos **16 pacotes** preparados para todas as quatro mudanças. Aqui são oito pacotes únicos (MC-01/MC-03 × quatro condições), cada um usado em duas conversas independentes. A lista abaixo é um inventário, **não a ordem de execução**; nenhuma tentativa aconteceu.

| Observação | Mudança | Condição | Repetição/bloco | Ordem | Estado |
|---|---|---|---:|---|---|
| PIL-MC-01-D0-R01 | MC-01 | D0 | 1 | a definir | planejada |
| PIL-MC-01-D1-R01 | MC-01 | D1 | 1 | a definir | planejada |
| PIL-MC-01-E0-R01 | MC-01 | E0 | 1 | a definir | planejada |
| PIL-MC-01-E1-R01 | MC-01 | E1 | 1 | a definir | planejada |
| PIL-MC-03-D0-R01 | MC-03 | D0 | 1 | a definir | planejada |
| PIL-MC-03-D1-R01 | MC-03 | D1 | 1 | a definir | planejada |
| PIL-MC-03-E0-R01 | MC-03 | E0 | 1 | a definir | planejada |
| PIL-MC-03-E1-R01 | MC-03 | E1 | 1 | a definir | planejada |
| PIL-MC-01-D0-R02 | MC-01 | D0 | 2 | a definir | planejada |
| PIL-MC-01-D1-R02 | MC-01 | D1 | 2 | a definir | planejada |
| PIL-MC-01-E0-R02 | MC-01 | E0 | 2 | a definir | planejada |
| PIL-MC-01-E1-R02 | MC-01 | E1 | 2 | a definir | planejada |
| PIL-MC-03-D0-R02 | MC-03 | D0 | 2 | a definir | planejada |
| PIL-MC-03-D1-R02 | MC-03 | D1 | 2 | a definir | planejada |
| PIL-MC-03-E0-R02 | MC-03 | E0 | 2 | a definir | planejada |
| PIL-MC-03-E1-R02 | MC-03 | E1 | 2 | a definir | planejada |

O [plano preenchível](modelos/plano_piloto.json) contém os mesmos 16 IDs, configuração e ordem nulas. Preencher antes de enviar: provedor/interface/modalidade, modelo e versão efetivamente reportada, parâmetros expostos e não expostos, limite de saída quando controlável, modalidade JSON comum, orçamento, configuração das ferramentas/acesso/histórico, captura e responsável/data da conferência. Parâmetro indisponível é registrado como não exposto ou não suportado, com justificativa, nunca como valor escolhido. Não copiar automaticamente gpt-6-astra/medium ou a ordem do exploratório.

### Ordenação repetível, ainda não aprovada para o piloto
O pesquisador define uma semente de **ordenação local**, antes de qualquer chamada; ela não controla o LLM. O utilitário lê a lista canônica do plano, usa um único gerador `random.Random(semente)` e embaralha as oito combinações de cada bloco na ordem dos blocos 1 e 2. Salva semente, versão do Python, algoritmo e as 16 posições, sem sobrescrever saída. Executar da raiz, substituindo SEMENTE pelo inteiro escolhido:

```powershell
python -B materiais/modelos/ordenar_piloto.py --semente SEMENTE --saida saidas-locais/ordem-piloto-proposta.json
```

Conferir exatamente uma ocorrência de cada combinação por bloco e cada posição global de 1 a 16. Guardar a ordem escolhida fora de saídas regeneráveis ao usá-la como evidência; vincular os hashes dos oito payloads e o identificador de configuração real às observações. O identificador de configuração editorial D35 não é configuração aprovada do modelo: antes do piloto, exportar para pasta nova com `python -B fontes_autorizadas.py --raiz . --saida saidas-locais/pacotes-configurados --configuracao-id ID_ESCOLHIDO`, usando o ID da configuração decidida, e montar os oito pacotes do piloto pelo comando do contrato. Isso cria manifestos/autorizações novos, preservando os pacotes de preparação e o texto aprovado. Somente então salvar a lista de `observacoes` para o resumo da CLI.

## 5.10 Procedimento de cada chamada futura
1. Conferir os critérios de entrada e a autorização específica para iniciar. Abrir conversa nova, sem mensagens anteriores, memórias/recuperação de arquivos, ferramentas ou acesso ao projeto. Registrar instruções adicionais conhecidas da plataforma. Não usar a conversa de desenvolvimento como sessão experimental.
2. Colar o **conteúdo completo de payload.txt na primeira mensagem**, com todos os blocos; não fornecer somente caminho, anexo referenciado ou pedido para ler arquivo. Registrar modo real de entrega e papéis da mensagem. Se houver papel de sistema separado, definir a mesma modalidade para todas as condições antes do piloto.
3. Preservar bytes do payload preparado e do texto efetivamente enviado, captura/exportação de origem, sessão/turno, instante e configuração real. Conferir diferenças inclusive CRLF/LF, prefixos automáticos e truncamentos; registrar desvios, sem reescrever o original para fazê-lo coincidir.
4. Preservar a resposta original completa ou o erro/fragmento de transporte, com origem e hash. Preencher [registro_execucao.json](modelos/registro_execucao.json); não colocar métricas manualmente no registro bruto. Manter original mesmo quando inválido, recusa ou seleção vazia. Não pedir explicação, reparo ou resposta melhor.
5. Se houver falha técnica, no máximo uma nova tentativa vinculada, com o mesmo payload e configuração; não é nova repetição. Falha de formato permanece inválida. Registrar ferramentas, histórico ou mensagem extra como desvio; não selecionar silenciosamente o melhor retorno.
6. Avaliar offline pela CLI e arquivar saídas separadas por origem/fase, conforme [contrato](../specs/004-preparacao-avaliacao-ids/contracts/preparacao-avaliacao.md). Conferir validade e denominadores, mantendo requisitos e testes separados. Avaliação descritiva de desvio não certifica elegibilidade para resumo controlado.

Não preencher conformidade como `conforme` apenas porque a resposta acertou. Conferir contexto/entrega/configuração, independentemente do escore. Entrega na plataforma e ausência efetiva de ferramentas ainda precisam ser verificadas; os testes offline não demonstram isso. Nenhum resultado anterior será incorporado ao piloto, e o manifesto principal continua não congelado.

## 5.11 Coletor offline D-37 — 07/11/2026

D-39: há agora uma [rota API independente preparada offline](../documentacao/operacao-api.md), com transporte corrigido e revisão externa de conformidade. Ela conserva os oito payloads/ordem, sem alterar o coletor Codex ou a trava descritos abaixo. A integração não autoriza chamada paga, conexão ou piloto. Os comandos próprios de simulação/conexão futura/revisão estão naquele ponto de operação, sem copiar parâmetros artificiais para a pesquisa.

Atualização operacional D-38: [análise dos bloqueios](../captura/analise-bloqueios-cli-2026-11-07-D38/RELATORIO.md). O coletor v1.1 usa nova configuração/plano D-38, preservando integralmente D-37, ordem e payloads. Os comandos abaixo apontam agora para D-38; o plano antigo é recusado pelo código novo por diferença de hash/configuração. Não editar os registros antigos para contornar essa conferência.

Implementação: [coletor_piloto.py](../coletor_piloto.py), Python 3.13.3/biblioteca padrão. A integração solicitada é `codex exec`, **GPT-6 Sol (`gpt-6-sol`) / medium**, sem troca automática de modelo. A CLI instalada `0.162.0-alpha.17.2` reconhece sessão efêmera, entrada por stdin, seleção de modelo/esforço e eventos JSONL; login ChatGPT ativo e medium presente no catálogo embutido. Isso não prova acesso remoto nem conformidade D-29. [Consultas locais](../captura/conferencia-codex-2026-11-07/ambiente.json), [testes e limites](../captura/controles-coletor-2026-11-07/RELATORIO.md).

**O envio real permanece bloqueado inclusive com `--enviar-real`.** Não foi demonstrado contexto exclusivamente textual/inventário vazio de ferramentas. Há instruções de agente embutidas; desativar recursos individuais, ignorar configuração do usuário, usar pasta vazia e sandbox read-only não prova essa fronteira. Retentativas internas da CLI também não estão controladas experimentalmente. A implementação não oferece opção para ignorar esses bloqueios. A autorização desta etapa termina nos trabalhos offline.

### Conferir ambiente e plano

Da pasta `tcc-impacto-llm`, usar diretórios novos a cada conferência/preparação:

```powershell
python -B coletor_piloto.py --help
python -B coletor_piloto.py ambiente --saida captura/conferencia-codex-nova
```

`ambiente` consulta somente versão, ajuda, `exec --help`, `login status` e catálogo **embutido** (`debug models --bundled`), sem atualização remota ou prompts. Não abre `auth.json`/tokens/configuração para exportá-los. Salva retornos, saídas e erros; o catálogo é reduzido às capacidades do modelo solicitado e presença/hash das instruções base. No sandbox desta entrega o Codex não encontrou o diretório de usuário; as consultas foram repetidas fora dele com permissão, mantendo o mesmo ambiente do usuário. Não alterar `HOME`/`CODEX_HOME` nem instalar outra ferramenta para contornar isso.

O [plano D-38](../captura/planejamento-piloto-2026-11-07-D38/plano.json) copia a ordem já registrada em D-37, com semente original **20261106**, algoritmo e versão do Python preservados; não há novo sorteio. São 16 posições e oito payloads distintos em duas repetições; não é dado de execução. Para apenas conferir esse plano:

```powershell
python -B coletor_piloto.py simular --plano captura/planejamento-piloto-2026-11-07-D38/plano.json
```

`simular` não inicia processo do modelo, consulta autenticação ou acessa rede. Reconfere identidades, configuração, 16 itens, oito payloads, hashes e tamanhos, autorizações, composição e equivalência das condições. Mostra o argv completo de cada sessão nova, o arquivo que forneceria stdin e controles pendentes, sem credenciais. Não usa `--output-schema`: o schema já integra o payload e nenhuma restrição adicional de saída foi aprovada.

Se houver necessidade de preparar outra versão em pasta nova:

```powershell
python -B coletor_piloto.py preparar --saida captura/planejamento-piloto-novo --ordem-registrada captura/planejamento-piloto-2026-11-07-D38/plano.json
```

`--ordem-registrada` preserva as posições existentes, sem novo embaralhamento. Somente a primeira preparação, sem esse argumento e na ausência de ordem anterior, usa a semente 20261106 pelo ordenador existente. O comando remonta oito pacotes v2-LF com o novo ID de configuração solicitado, preservando os bytes dos payloads, a referência e todos os artefatos anteriores. Registrar novamente um plano não autoriza o piloto. Hashes do coletor/montador mudados exigem nova preparação; não corrigir registros antigos nem presumir continuidade após conversão de bytes do código em checkout.

### Iniciar e continuar futuramente

Comandos disponibilizados para a operação futura, **atualmente retornam 2 antes de iniciar qualquer subprocesso LLM ou criar lote real**:

```powershell
python -B coletor_piloto.py iniciar --plano captura/planejamento-piloto-2026-11-07-D38/plano.json --lote captura/piloto/lote-001 --enviar-real
python -B coletor_piloto.py iniciar --plano captura/planejamento-piloto-2026-11-07-D38/plano.json --lote captura/piloto/lote-001 --enviar-real --continuar
```

O gate exige novo incremento com prova dos controles antes da liberação, além das pendências científicas/operacionais no [estado central](../ESTADO_ATUAL.md). A flag explícita é necessária, mas não basta. Nenhuma chamada ocorre por padrão ou ao consultar ajuda. A CLI conserva instruções de agente adicionais; não se afirma que `--ignore-user-config` as remova. Limite de saída, custo, temperatura, top_p, seed do modelo e modelo efetivamente reportado permanecem nulos quando desconhecidos. Autenticação por conta existente não autoriza contratação de API.

O motor faz uma observação por vez, processo/sessão novos, sem `resume`/`fork`, recebe o payload integral exclusivamente via stdin e filtra variáveis herdadas para não transportar contexto/chaves do desenvolvimento. A pasta de trabalho do filho começa vazia. Essas medidas são solicitadas e testadas no substituto; não comprovam ausência real de ferramentas ou das instruções de plataforma. Modelo/esforço/configuração são fixos; bytes e binários são reconferidos. `--limite N` pausa entre observações após N tentativas, sem mudar a configuração, para posterior `--continuar`.

### Exercitar controles locais

```powershell
python -B -m unittest discover -s tests -p test_coletor_piloto.py -v
python -B coletor_piloto.py controle --plano captura/planejamento-piloto-2026-11-07-D38/plano.json --lote captura/controles-locais/lote-novo --limite 3
python -B coletor_piloto.py controle --plano captura/planejamento-piloto-2026-11-07-D38/plano.json --lote captura/controles-locais/lote-novo --continuar
```

`controle` usa somente [substituto local fixo](../tests/substituto_coletor.py), sem rede/modelo/gabarito. Registra sempre `origem=sintetica`, `fase=verificacao_sintetica`, mesmo usando IDs do plano. Os testes também exercitam resposta inválida/vazia, falha técnica, ferramentas/turnos/modelo divergentes, adulteração, interrupção e recuperação. Nada disso constitui execução do piloto. Os testes do importador real usam metadados artificiais somente em temporários, identificados como controles, e não são importados como dados reais.

Continuar recupera o estado dos arquivos e pula conclusões fechadas, inclusive inválidas ou vazias; não retoma a conversa do modelo. Falha técnica para o lote: depois de corrigir a indisponibilidade, a continuação admite somente T02 vinculada a T01, com mesmo payload/configuração e nova sessão. Depois de T02 falhar, a observação permanece falha técnica final e a continuação segue para a próxima. Não há T03 nem reenvio por pontuação/formato.

Interrupção entre observações preserva as concluídas. Interrupção durante o processo preserva eventos parciais e bloqueia reenvio automático, pois não prova se o modelo concluiu remotamente. Se o processo morrer depois de salvar `tentativa.json` e antes de `fechamento.json`, recuperar apenas os arquivos:

```powershell
python -B coletor_piloto.py recuperar --lote captura/controles-locais/lote-novo
```

Um lock existente exige conferir que o processo terminou antes de remover **somente `coletor.lock`**. Não remover diretórios de tentativas. Sem `tentativa.json`, o estado permanece ambíguo e bloqueado; não reclassificar manualmente como falha de transporte nem reenviar automaticamente. Desvios registrados também bloqueiam a continuação, sem selecionar outra resposta.

### Avaliar depois da captura

```powershell
python -B coletor_piloto.py avaliar --lote captura/controles-locais/lote-novo --referencia materiais/modelos/referencia_candidata_NAO_ENVIAR_AO_LLM.json --saida avaliados/controles-locais/avaliacao-nova
```

O mesmo comando serve ao lote real futuro trocando `--lote` e `--saida` pelos diretórios reais. Origem/fase são lidas do cabeçalho do lote, sem opção para promover controle a piloto. O avaliador existente importa cada tentativa, gera lista explícita/observações planejadas e resumo. Nenhum resultado retorna ao modelo. Avaliação real com conformidade pendente/desvio permanece descritiva: seu resumo controlado continua bloqueado conforme contrato. Retorno 1 indica inválidas, falhas ou incompletude registrada; 2 indica erro de integridade/contrato/bloqueio, não pontuação ruim.

### Localização dos arquivos

| Artefato | Caminho dentro do lote/avaliação |
|---|---|
| Plano e configuração fixos | `plano-original.json`, `lote.json` |
| Preparação de cada tentativa | `PIL-.../T01/preparacao/` (ou T02) |
| Entrada fornecida ao subprocesso | `PIL-.../T01/entrada.bin`; no controle, eco `ambiente/stdin-recebido.bin` |
| Fluxo original de eventos e erros | `PIL-.../T01/eventos.jsonl`, `stderr.bin` |
| Texto final extraído sem trim/correção | `PIL-.../T01/resposta.bin`; todas as mensagens em `mensagem-NN.bin` |
| Comando, instantes, retorno, sessão, configuração e desvios | `inicio.json`, `tentativa.json`, `fechamento.json` |
| Avaliação e originais copiados | `avaliados/.../PIL-.../T01/` |
| Lista, planejamento e tabelas por célula | `lista.json`, `observacoes.json`, `resumo/resumo.json` (tabelas JSON) |

Os eventos originais são a evidência primária da CLI; `resposta.bin` é a codificação UTF-8 do campo textual final identificado, sem reserializar o JSON da resposta. Não há garantia de comparação com uma entrada efetiva da plataforma enquanto o envio continuar bloqueado. Capturas/avaliações usam os caminhos já protegidos por `.gitattributes` D-36, sem normalizar originais e sem sobrescrever saídas existentes.

### Controles adicionais D-38 e seus limites

O argv acrescenta `--strict-config`, `model_provider="openai"`, `forced_login_method="chatgpt"`, `skills.include_instructions=false`, `memories.use_memories=false` e `memories.generate_memories=false`, aceitos na inspeção nativa. As desativações anteriores continuam. Configurado false não certifica tool indisponível. No render de sentinela, AGENTS e instruções automáticas de skills ficam ausentes, mas permanecem mensagens developer e environment; debug não fornece o envelope completo tools/instructions nem replica todas as flags do exec.

Zero/um são aceitos em request_max_retries/stream_max_retries de custom provider, mas `model_providers.openai` é recusado por ser reservado. Não há override desses campos aplicado ao coletor com login ChatGPT e não se afirma que unbounded=false elimina retries. Os valores efetivos e sua semântica permanecem desconhecidos. Erro de cliente seguido de final íntegro no mesmo turno conserva a conclusão com desvio; não causa outra geração automática. Contagem de erro/reconexão não vira observação, turno ou geração por inferência. [Evidências e tabela final D-38](../captura/analise-bloqueios-cli-2026-11-07-D38/RELATORIO.md).

Menor alternativa apenas proposta: adaptador HTTP direto sem agente, com autenticação própria de API, orçamento/créditos/custo a conferir e nova configuração/modalidade registrada; mantém payloads/ordem/avaliador. Não foi implementado nem houve migração. Não iniciar qualquer alternativa ou remover a trava com base em declaração ou booleano.
