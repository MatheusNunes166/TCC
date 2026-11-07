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
