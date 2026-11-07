# 5. Do piloto à coleta principal

## 5.1 Antes do piloto

Atualização de catálogo (D-15): 12 testes, 48 pares teste × mudança, 60 expectativas incluindo a versão inicial. T12 foi executado apenas na versão inicial; as quatro variantes continuam sem implementação ou execução. Referência 0.2 candidata, sem revisão científica concluída.

O piloto só começa quando a baseline existe, a referência está revisada, os prompts/notas estão versionados e a coleta registra payload e resposta originais. A versão inicial existe e foi verificada com T12; referência, notas e demais condições científicas/operacionais continuam pendentes. Documentação preparada não prova implementação da coleta nem libera piloto.

Checklist de entrada:
- [ ] Definições de impacto e seleção aprovadas; MC-04-v2 aceita ou referência reescrita.
- [ ] Baseline e quatro variantes conferidas contra expectativas humanas.
- [ ] Revisor, data e divergências do gabarito registrados.
- [ ] Notas revisadas quanto a vazamento e origem.
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

Dados sintéticos usados para verificar o avaliador devem ter fase `verificacao_sintetica`, nunca `principal`. Não há resultados preenchidos neste pacote.

## 5.8 Entregas finais esperadas

Uma tabela por mudança/condição com qualidade e variabilidade; uma tabela de omissões/excedentes; comparações planejadas de estrutura e notas; registro de falhas; discussão das limitações. Relatar também ausência de diferença ou resultados desfavoráveis. Entregar o protocolo e os artefatos versionados para permitir repetição no mesmo recorte, sem alegar desempenho geral de LLMs.
