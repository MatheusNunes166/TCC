# 1. O que será avaliado

**Pergunta operacional:** neste módulo e nestas quatro mudanças, como a organização da solicitação e a presença de notas do analista alteram os acertos, as omissões, as seleções excedentes e a consistência dos IDs de requisitos e testes indicados por um único LLM?

**Entrega acadêmica:** protocolo documentado, referência rastreável, registros reproduzíveis e comparação descritiva das quatro condições. O módulo, a documentação e uma rotina simples de coleta/avaliação são instrumentos. Não se propõe desenvolver um framework genérico nem um benchmark de vários sistemas. O feedback sobre framework é tratado como sugestão, não como autorização para mudar o objetivo da proposta.

## 1.1 Escopo e unidade de análise

Um módulo fictício de autorização; quatro RFs; três papéis; duas operações; herança de um nível; uma incompatibilidade; onze casos existentes; quatro mudanças independentes; um LLM. Não há cadastro, interface, autenticação real, banco, implantação, vários modelos ou geração de novos testes pelo LLM avaliado.

Cada observação é uma resposta de **mudança × condição × repetição**. Cada mudança começa na mesma baseline, nunca no resultado da anterior. Cinco repetições por combinação são uma proposta inicial, derivada das avaliações: 4 × 4 × 5 = 80 chamadas principais, mais 16 de piloto. Confirmar viabilidade após o ensaio e fixar a quantidade antes da coleta; não parar quando uma condição parecer melhor.

## 1.2 O significado dos resultados

- **Requisito impactado:** regra diretamente alterada ou regra dependente cujo valor funcional produzido se altera em pelo menos um cenário válido da suíte. O texto da regra dependente pode permanecer igual. Uma mera pré-condição ou um teste compartilhado não basta para incluir outro RF.
- **Teste relevante:** caso incluído pela política de seleção da seção 2.3. Pode ter resultado alterado ou verificar a preservação de um comportamento relacionado.
- **Melhora:** maior completude da seleção e menos indicações excedentes em relação à referência, com estabilidade entre repetições. Resultados podem mostrar empate ou compensações; não é obrigatório declarar um vencedor único.

O estudo mede concordância com uma referência local revisada. Não mede compreensão interna do modelo, segurança de produção, cobertura de código, detecção de defeitos ou redução real do tempo de regressão. Uma alteração correta de resultado esperado não é, por si, um defeito. Para medir detecção de falhas seria necessário outro desenho com defeitos e oráculos, fora deste recorte.

## 1.3 Quatro condições e controles

| Condição | Solicitação | Notas |
|---|---|---|
| D0 | Pedido direto | Não |
| D1 | Mesmo pedido direto | Sim |
| E0 | Pedido com etapas explícitas, em uma chamada | Não |
| E1 | Mesmo pedido estruturado | Sim |

Todas recebem os mesmos requisitos, política inicial, dependências, catálogo de testes com resultados da baseline, definição de impacto, política de seleção e uma mudança. Não recebem os resultados esperados após a mudança, conjuntos corretos, este guia completo, histórico de desenvolvimento ou exemplos resolvidos do caso. Notas idênticas nas condições D1 e E1 e iguais entre mudanças nesta versão.

Fixar: provedor, ID e versão disponível do modelo, modalidade de API, parâmetros realmente suportados, limite de saída, mensagem de sistema, textos integrais, ordem e versão dos documentos, esquema JSON, ferramentas desativadas e regras de falha. Registrar parâmetros indisponíveis como “não suportado”, sem simular controle. Temperatura baixa ou zero não garante determinismo.

**Recomendação de ambiente:** chamadas isoladas por API, sem histórico ou recuperação automática de arquivos. A IDE usada para construir o módulo pode ler o projeto; o modelo avaliado recebe apenas um pacote por lista permitida. Uma pasta chamada “privado” e um .gitignore não impedem que um agente leia o gabarito. Separar fisicamente o ambiente de execução e verificar o payload final. Não indexar gabarito, notas ausentes ou histórico no ambiente experimental.

## 1.4 Como construir e revisar o gabarito

1. Fechar a redação da baseline e o contrato `decisão + motivo`.
2. Aplicar, em papel, cada mudança isoladamente; obter saídas esperadas dos onze casos.
3. Identificar a regra alterada e os valores dependentes que mudam. Justificar cada RF incluído e cada exclusão contestável.
4. Aplicar a mesma política de seleção aos onze casos; marcar por que cada teste entra ou fica fora.
5. Implementar e executar futuramente os testes da baseline e das variantes como verificação adicional. A implementação não é a única fonte de verdade: confrontá-la com regras e expectativas revisadas.
6. Solicitar revisão humana do gabarito e das notas. Proposta: pesquisador prepara e orientador revisa; combinar isso explicitamente. Registrar divergências, resolução, revisor e data.
7. Gerar versão e hash dos artefatos; guardar a referência fora do contexto do LLM avaliado.

A checklist comprova que essa preparação foi feita. Ela **não** é uma nota de qualidade das respostas. As respostas recebem os números abaixo.

## 1.5 Medidas propostas, calculadas separadamente para RFs e testes

Considere G = IDs esperados e S = IDs indicados. Após retirar duplicatas, TP = |S ∩ G|; FP = |S − G|; FN = |G − S|.

| Medida | Cálculo | O que responde |
|---|---|---|
| Revocação/completude | TP / (TP + FN) | Quantos itens esperados foram lembrados? |
| Precisão | TP / (TP + FP) | Quantos itens indicados pertencem à referência? |
| F1 | 2TP / (2TP + FP + FN) | Resumo do equilíbrio entre as duas medidas |
| Seleção completa | 1 se FN = 0, senão 0 | A resposta incluiu todo o conjunto esperado? |
| Correspondência exata | 1 se S = G, senão 0 | A resposta coincidiu integralmente com a referência? |
| Consistência de Jaccard | tamanho(Sᵢ ∩ Sⱼ) / tamanho(Sᵢ ∪ Sⱼ) | Quanto duas repetições da mesma condição se parecem? |
| Fração de testes selecionados | IDs válidos de testes selecionados / 11 | Quanto da suíte foi indicado? |
| Redução nominal | 1 − fração selecionada | Quanto ficou de fora, sem inferir economia real? |

G é não vazio em todos os casos candidatos. Se S for vazio, definir precisão, revocação e F1 como zero. Jaccard entre duas seleções vazias é 1 por convenção, mas isso não indica qualidade; mostrar a revocação zero junto. G vazio em uma futura revisão exige nova convenção antes da coleta.

**Prioridade de interpretação:** apresentar omissões e revocação primeiro; depois precisão, F1 e consistência. Examinar redução apenas entre respostas válidas com revocação de testes igual a 1 e sem IDs inexistentes. Não converter tudo em uma nota ponderada arbitrária. F1 alto não apaga uma omissão. FP é excedente perante esta política, não prova que um teste seja inútil em qualquer estratégia de regressão.

### Exemplo calculado, não resultado de experimento

Para MC-02, a referência candidata tem T06, T07 e T11, em uma suíte de onze testes.

| Seleção hipotética | Precisão | Revocação | F1 | Redução nominal | Interpretação |
|---|---:|---:|---:|---:|---|
| Nenhum | 0% | 0% | 0% | 100% | Omite tudo; não é melhora |
| Todos os onze | 27,3% | 100% | 42,9% | 0% | Completa, com oito excedentes |
| T06, T07, T11 | 100% | 100% | 100% | 72,7% | Coincide com a referência |
| T06, T07 | 100% | 66,7% | 80% | 81,8% | Omite a preservação da regra de estado |

Precisão usa como denominador o que o modelo selecionou; revocação, o que deveria selecionar; redução, os onze testes disponíveis. Esse é o balanceamento solicitado pelo professor. A fundamentação de precisão/recall/F1 consta em [F3]; a política concreta e a prioridade de interpretação são decisões deste estudo, não prescrições dessa fonte.

## 1.6 Saídas inválidas e falhas

Exigir JSON com exatamente duas listas de strings, `requisitos` e `testes`. Guardar a resposta original sempre. Não corrigir manualmente IDs aproximados ou texto livre. Duplicatas são removidas para calcular conjuntos e registradas como ocorrência. IDs inexistentes contam como FP; reportar sua quantidade separadamente.

JSON inválido, truncado ou fora do esquema conta como falha de formato, sem nova tentativa de “melhorar a resposta”. Para o resumo operacional, essa execução recebe conjuntos vazios e escores zero; informar a taxa de validade e apresentar também o resumo das respostas válidas, com os denominadores. Não interpretar esses zeros como seleções vazias deliberadas.

Erro de transporte pode ter no máximo uma nova tentativa com o mesmo payload, registrada. Se falhar novamente, marcar falha técnica, sem inventar resposta. Mostrar executadas/planejadas e não declarar uma coleta completa com células faltantes. Corrigir indisponibilidade antes de retomar o lote; nunca repetir apenas respostas ruins.

## 1.7 Análise e limites

Montar uma linha por execução e dois blocos de métricas, RF e testes. Para cada mudança e condição, mostrar TP/FP/FN, média, mediana e amplitude dos escores, taxa de seleção completa, correspondência exata e validade. Com cinco repetições há dez pares para Jaccard em cada célula; esses dez pares não são dez observações independentes. Informar quantos pares válidos foram usados.

Comparações planejadas dentro da mesma mudança: E0−D0 e E1−D1 para organização; D1−D0 e E1−E0 para notas. Se os efeitos diferirem, descrever a interação, sem atribuir causalidade além dos fatores controlados. Um resumo geral dá peso igual a cada mudança e sempre vem acompanhado das quatro linhas individuais.

A análise inicial é descritiva, sem teste de significância ou promessa de generalização. Oitenta chamadas não representam oitenta sistemas independentes. Diretas e propagadas têm tamanhos de referência diferentes: comparar condições dentro de cada mudança; não concluir que “propagação é mais difícil” somente pela diferença entre os grupos. O piloto pode revelar efeito de teto (todas acertam) ou piso; isso é achado, não motivo para dificultar regras até surgir a vantagem desejada.
