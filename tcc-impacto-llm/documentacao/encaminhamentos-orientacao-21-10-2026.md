# Encaminhamentos da orientação de 21/10/2026

Registro documental: 27/10/2026, assistente, por solicitação do pesquisador (D-22/D-23 em [decisões](decisoes.md)). Fonte: [transcrição original](21-10-2026.txt), reunião entre Matheus Henrique Braun Nunes e Prof. Me. Muriel Mazzetto, duração 19min41s. A transcrição é automática, com identidades inferidas por contexto e passagens incertas; nomes técnicos e formulações duvidosas exigem conferência na gravação. O original foi preservado.

As classificações abaixo são uma leitura documental das falas, não uma ata aprovada pelo orientador. Datas de execução e autorizações posteriores não são retroativamente atribuídas à reunião.

## Pedidos explícitos

| Trecho da reunião | Encaminhamento | Atendimento ou próximo passo |
|---|---|---|
| 00:00:02–00:00:14 | Levar dúvidas, compartilhar a tela e o repositório com o orientador. | Preparar a navegação no repositório; compartilhamento efetivo ainda a confirmar pelo pesquisador. Nenhum envio realizado nesta etapa. |
| 00:02:31–00:04:31 | Pesquisar como avaliar as respostas e a adequação de precisão/revocação/F1 ao objeto avaliado. A fala distingue comparação textual de seleção de classes/IDs. | Fundamentação e revisão pendentes; Spec 004 delimita listas de IDs. A possibilidade condicionada de usar métricas de classificação não constitui aprovação das métricas deste estudo. |
| 00:04:55–00:06:27; 00:17:00–00:17:43 | Apresentar o desenvolvido, contextualizar o ciclo de software com IA e situar o estudo na seleção de requisitos/testes. Preparar algo rodável para simular a apresentação. | [Roteiro curto](roteiro-demonstracao-spec003.md) com a bancada existente. A primeira semana de novembro e o horizonte de duas semanas são metas de preparação mencionadas, não agendamento confirmado de banca. |
| 00:08:21–00:09:05; 00:18:05–00:18:36 | Explicitar o que foi entregue, o que permanece pendente e possíveis continuações no TCC2. | Separar entrega de engenharia, preparação da avaliação e pesquisa ainda não realizada. |
| 00:10:29–00:10:38 | Organizar a transcrição em tópicos. | Este registro, mantendo referência temporal e incertezas do original. |
| 00:11:34–00:12:35; 00:13:16–00:13:32; 00:14:02–00:16:14 | Descrever o objeto de estudo, fazê-lo rodar com exemplos e mostrar a base, a alteração e o efeito funcional, distinguindo sistema e método de avaliação. | Roteiro com quatro RFs, entrada, saída inicial, diff e saída após mudança, usando MC-01 e MC-04. O pedido não exige criar uma nova aplicação. |
| 00:19:06–00:19:16 | Abrir o repositório e mostrar a demonstração. | Navegação e comandos de consulta no roteiro; não se infere dispensa definitiva de artigo ou de outras exigências institucionais. |

## Sugestões e possibilidades

| Trecho | Sugestão | Situação |
|---|---|---|
| 00:03:19–00:04:00 | Investigar avaliação semântica no caso de respostas textuais. | Possibilidade vinculada ao objeto avaliado; semelhança textual fica fora da Spec 004 por determinação atual do pesquisador. |
| 00:04:48–00:04:54; 00:06:27–00:08:21 | Explorar mais de um modelo/ferramenta ou configurações de custo distinto. | Nenhuma seleção, instalação ou comparação autorizada agora. Nomes transcritos como “Cloud Code”, “anti-gravity”, “ARGO 4”, “Sol” e “Luna” não são identificações técnicas confirmadas. Não se validaram ofertas, créditos ou disponibilidade. |
| 00:05:18–00:05:31; 00:07:18–00:07:27 | Usar slides breves e diagramas de apoio. | Opcionais; materiais existentes podem apoiar, respeitando sua data e caráter candidato. |
| 00:09:11–00:10:07 | Buscar profissionais externos para revisar documentos, gabarito e notas, reduzindo a dependência da visão do autor. | Recomendação forte, ainda sem pessoa, data, parecer ou revisão realizada. Não transformar as notas do pesquisador em depoimentos de especialistas. |
| 00:12:12–00:13:16 | Demonstrar por tela, backend, API ou requisições; a fala em 00:12:52 explicita que interface não é necessária. | Alternativas ilustrativas. O pedido atual mantém terminal/arquivos e o mesmo repositório; não criar interface/API. “GIFs” é passagem incerta, possivelmente relacionada aos diffs; conferir áudio antes de citar literalmente. |
| 00:07:07–00:07:18; 00:17:43–00:18:05 | Verificar viabilidade de uma execução na apresentação, preferencialmente dois exemplos distintos. | Roteiro usa MC-01 e MC-04 com evidências já registradas. Não equivale a executar LLM ao vivo nem fixa casos do piloto. |
| 00:16:19–00:16:53 | Ampliar no TCC2 para outro sistema, possivelmente com tela. | Possível continuidade, sem decisão de trocar objeto ou criar outro repositório. |

## Decisões ainda abertas

- **Revisão profissional e científica (P-01/P-02):** combinar revisor, escopo, data, divergências e resolução para referência 0.2, política de impacto/relevância e expectativas, inclusive T12 nas mudanças. T12 já foi adotado e verificado em B; não precisa de nova adoção.
- **Notas e prompts (P-02):** conteúdo definitivo, origem, neutralidade e revisão. A nota atual é candidata, redigida pelo pesquisador; nenhuma participação externa pode ser presumida.
- **Medidas (P-02):** precisão, revocação, F1 e consistência continuam propostas a fundamentar e revisar, incluindo convenções de validade e falhas. Seleção de IDs e comparação textual são objetos distintos; este incremento trata apenas do primeiro.
- **Piloto (P-03):** desenho final, mudanças, condições, repetições, ordem, orçamento, configuração e critérios de entrada/saída/congelamento. MC-01/MC-04 na demonstração não substituem a proposta histórica MC-01/MC-03 para piloto. Os números históricos de chamadas continuam propostas.
- **Modelos e ferramentas:** avaliar sugestões somente em decisão futura; nenhum modelo novo escolhido. O uso do assistente no desenvolvimento não identifica o LLM experimental.
- **Apresentação:** confirmar calendário, duração, compartilhamento do repositório e execução ao vivo. Adoção formal da constituição continua pendente.

## Relação com o fechamento técnico posterior

Na reunião, o orientando descreve a Spec 003 como próxima etapa (00:11:24–00:11:34). O [fechamento de engenharia](../specs/003-mudancas-controladas/evidencias.md), também datado de 21/10, registra posteriormente quatro variantes, 12 pares iniciais e 48 pares de variantes conformes com a candidata 0.2, além de controles sintéticos separados. A reunião não revisou nem aprovou cientificamente esses resultados posteriores. Os 48 pares são verificações locais de decisão/motivo, não respostas de LLM nem resultados do experimento acadêmico.

O pedido atual autoriza registrar estes encaminhamentos, preparar o roteiro e somente Spec 004/checklist. Não autoriza implementação, novos modelos, chamadas ao LLM, piloto ou coleta. Próximos trabalhos técnicos e científicos permanecem distintos.
