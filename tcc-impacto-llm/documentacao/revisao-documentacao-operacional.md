# Revisão privada — documentação consolidada e operacional

22/11/2026. **NÃO ENVIAR ESTE GUIA, O PLANO OU O MANIFESTO AO MODELO.** O pesquisador adotou o desenho nesta conversa: “perfeito é isso ai mesmo que eu quero vamos fazer”. Isso autoriza preparar o recorte descrito; não registra aprovação científica externa ou revisão já feita dos novos textos. **Nenhuma chamada executada.**

## O que foi preparado

Comparar uma documentação consolidada, com critérios e explicações das consequências, com uma documentação operacional que distribui os fatos entre cinco documentos. O modelo recebe todos esses documentos como blocos de um único payload textual; não navega em pastas ou usa ferramentas.

O controle **CONSOLIDADA** é literalmente o payload preservado da extensão 0.3. Em **OPERACIONAL**, somente o bloco `requisitos-baseline` é substituído. Permanecem literais: sistema, política comum de impacto/relevância, catálogo **com as seis colunas e os 15 testes**, mudança, notas quando previstas, pedido e schema. Portanto, a proposta anterior de retirar duas colunas **não será executada neste bloco**. Se ela tiver sido integrada localmente, conservá-la como proposta anterior, sem misturar seu plano a este.

Textos operacionais completos para leitura:

1. [Especificação funcional](../captura/documentacao-operacional-0.3-001/documentos-operacionais/01-especificacao-funcional.md): entradas/saídas e os quatro IDs de requisitos com suas regras.
2. [Cadastro de papéis](../captura/documentacao-operacional-0.3-001/documentos-operacionais/02-cadastro-de-papeis.md): concessões próprias, papéis atribuídos e conjunto efetivo.
3. [Configuração de herança](../captura/documentacao-operacional-0.3-001/documentos-operacionais/03-configuracao-de-heranca.md): relação configurada, um nível e origem das permissões herdadas.
4. [Configuração de incompatibilidades](../captura/documentacao-operacional-0.3-001/documentos-operacionais/04-configuracao-de-incompatibilidades.md): par configurado e domínio de aplicação do predicado.
5. [Contrato de execução](../captura/documentacao-operacional-0.3-001/documentos-operacionais/05-contrato-de-execucao.md): sequência, prioridades e motivos dos retornos.

Não há explicação particular de que uma retirada de herança muda um conflito. A versão operacional conserva os fatos necessários para relacionar as regras. As notas originais continuam apontando riscos gerais em D1, sem trazer IDs corretos ou regra factual exclusiva. A política comum permanece integral, inclusive os critérios estruturais de seleção.

## Rastreabilidade factual

Origem: bloco de requisitos de SHA-256 `0d1e465d42d36b241933e688965b5dc562711e7670198b7869b4b06bef5ae4cb`, obtido das requisições preservadas, não do gabarito privado. Fonte fora dessa versão é recusada pelo preparador.

| Fato a preservar | Origem consolidada | Destino operacional |
|---|---|---|
| Domínio de estados, papéis e operações; dados válidos | Entradas e saídas | Documento 01, texto literal |
| Decisão e motivo são observáveis; cinco motivos | Entradas e saídas | Documento 01, texto literal |
| Vocabulário fechado, sem validação de malformados | Entradas e saídas | Documento 01, texto literal |
| IDs e regra principal de RF-01–RF-04 | Colunas ID e regra | Documento 01, cópia literal dessas colunas |
| Só conta ativa prossegue | RF-01 e ordem global | Documento 01 e prioridade 1 do documento 05 |
| Consulta concede visualizar | RF-02 | Cadastro do documento 02 |
| Auditoria concede exportar | RF-02 | Cadastro do documento 02 |
| Supervisão sem concessão própria | RF-02 | Cadastro do documento 02 |
| Concessão direta vem dos papéis atribuídos | RF-02 | Documento 02 |
| Efetivos preservam atribuídos e incluem herança | RF-03 e ordem global | Documento 02 |
| Supervisão inclui Consulta | RF-03 | Relação do documento 03 |
| Herança de um nível, sem ciclos/multinível | RF-03 | Documento 01 e documento 03 |
| Concessão herdada vem do papel incluído | RF-03 | Documento 03 |
| Par incompatível Consulta + Auditoria | RF-04 | Configuração do documento 04 |
| Incompatibilidade considera efetivos | RF-04 | Documento 01 e documento 04 |
| Estado precede conflito, que precede concessão | Ordem global | Prioridades 1–4 do documento 05 |
| Direta prevalece quando também há herdada | Ordem global | Prioridades 3 e 4 do documento 05 |
| Ausência de concessão nega por sem_permissao | Ordem global | Prioridade 5 do documento 05 |
| Expandir antes de verificar conflito/decidir concessão | Ordem global e RF-02 | Primeiro parágrafo do documento 05 |
| Incremento parcial não redefine o contrato global | Última frase | Último parágrafo do documento 05 |

As frases explicativas “herda visualizar”, “não herda exportar” e “inclusive se Consulta vier da herança” não foram copiadas. Seus fundamentos continuam nos cadastros, relação, definição de efetivos e prioridades. Essa é uma conferência técnica de fatos e consequências modeladas; não certifica equivalência de toda interpretação humana ou de um LLM. Conferência textual do pesquisador continua necessária.

## Desenho adotado para preparação: 32 posições

| Fator | Níveis |
|---|---|
| Mudança | MC-02 e MC-04-v2 |
| Modelo solicitado | Sol e Astra |
| Condição | D0 e D1, mesmo pedido direto sem/com nota original |
| Documentação | CONSOLIDADA e OPERACIONAL |
| Repetição | R01 e R02 |

**2 × 2 × 2 × 2 × 2 = 32**. Dezesseis células, N=2 por célula; dois blocos balanceados de 16, semente 20261122. Oito payloads únicos; modelo e repetição não mudam o input textual de uma combinação. Condições D0/D1 diferem somente pela nota e sua delimitação. Rótulos de tratamento, ordem e IDs de observação ficam fora do input.

Os controles consolidados serão novos, no mesmo bloco. As 64 respostas anteriores e as 16 de notas ficam separadas, sem reaproveitamento como controle intercambiável. Piloto, demonstrações da interface e proposta de retirada de colunas também não entram. E0/E1 e N01/N02 não integram este bloco; não se poderão estender a eles conclusões específicas desta documentação.

MC-02 e MC-04 foram escolhidas após conhecer os resultados anteriores. Registrar essa seleção pós-exploratória: MC-02 teve excedentes em Sol e MC-04 apresentou empate. Não é amostragem aleatória de tarefas ou sistemas.

## Limites da comparação

O fator é a **versão documental como um conjunto**: distribuição entre blocos, redação, retirada de explicações derivadas e extensão textual podem variar. Não isola o efeito de cada componente. Os rótulos não demonstram que a versão operacional será mais difícil; tabelas operacionais podem até facilitar. A política comum explícita e o tamanho reduzido da bancada continuam limitações.

Nesta preparação, cada payload operacional tem **917 bytes UTF-8 e 888 caracteres a mais** que seu controle, contando os novos títulos e delimitadores. Não é uma redução do volume total. Essa diferença integra a intervenção e deve ser reportada, sem atribuir eventual efeito somente à fragmentação.

Registrar tamanho literal agora e tokens reais quando reportados pela API. Não inventar tokens a partir de caracteres. As notas são simuladas pelo pesquisador com apoio de IA; o bloco não mede desempenho de analistas juniores ou conhecimento tácito de profissionais reais. Os IDs não mostram raciocínio interno nem descoberta de defeitos.

Fixar estes textos e a quantidade antes de chamadas. Relatar melhora, piora ou empate. Não ajustar documentos por desempenho, procurar uma nota vencedora, trocar modelos ou adicionar repetições até obter diferenças. A nova reformulação já é posterior a resultados conhecidos; esse caráter exploratório precisa constar da análise.

## Configuração e avaliação

Proposta técnica preservada: medium, 4096 tokens máximos de saída incluindo raciocínio/resposta, timeout 120 s, HTTP direto à Responses API, tools=[], tool_choice=none, store=false, stream=false e zero retentativas automáticas do cliente. Modelo solicitado/reportado devem ser registrados; desconhecido permanece nulo. Não houve consulta de saldo, preço atual ou acesso autenticado nesta preparação. Não se impõe orçamento positivo ao pesquisador que decidiu em D-49 não defini-lo.

Uma requisição independente por observação. Captura primeiro, referência privada somente na avaliação posterior. Reutilizar avaliador e convenções existentes, com requisitos/testes separados: acertos, omissões, excedentes, precisão, revocação, F1, exatas e Jaccard entre repetições elegíveis. Mostrar falhas, inválidas, elegibilidade e denominadores sem reparo ou imputação silenciosa. Conformidade continua humana e não usa acerto como critério de inclusão.

## Verificação offline e operação

- [Plano](../captura/documentacao-operacional-0.3-001/plano.json), [manifesto](../captura/documentacao-operacional-0.3-001/manifesto.json) e [payloads](../captura/documentacao-operacional-0.3-001/payloads/).
- [Preparador](../preparar_documentacao_operacional.py): somente preparar/conferir, com saída nova e recusa de sobrescrita.
- [Seis controles](../tests/test_documentacao_operacional.py): catálogo/política/notas literais, balanceamento, derivações declarativas, recusa de alteração e fronteira sem chave/referência privada/transporte.

```text
python -B preparar_documentacao_operacional.py conferir --pasta captura/documentacao-operacional-0.3-001
```

Isso **não executa chamadas**. A preparação e a conferência não leem a referência privada ou a chave. O transporte real foi proibido nos controles. Os fatos extraídos dos documentos operacionais foram confrontados com baseline e quatro variantes em 48 entradas válidas por versão: **240 pares de decisão/motivo conformes**. Esse confronto técnico não substitui revisão científica das expectativas ou prova da interpretação do modelo.

[Evidência da execução e preservação](../evidencias/spec004/documentacao-operacional-2026-11-22/verificacao.json). Núcleo, variantes, coletor, avaliador, referências, notas, prompts e coortes anteriores permanecem intactos.

O desenho foi adotado pelo pesquisador; a conferência dos novos textos e a integração de captura continuam pendentes. O painel atual não conhece estes perfis e não foi alterado. Antes de envio futuro, a integração precisa preservar documentacao_id, condição, nota_id, mudança, modelo, repetição, origem, plano e hashes ao longo de captura/avaliação/revisão/resumo, em coorte própria. Não adaptar este plano simplesmente ligando envio_autorizado nem fornecê-lo a uma CLI de outro contrato. As 64 + 16 conformidades anteriores continuam separadas e pendentes nas fontes atuais.
