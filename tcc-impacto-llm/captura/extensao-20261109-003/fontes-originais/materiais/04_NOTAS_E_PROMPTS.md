# 4. Notas do analista e solicitações ao LLM

## 4.1 O que as notas representam

São notas simuladas pelo pesquisador, Matheus Henrique Braun Nunes, com apoio de IA, inspiradas em observações e heurísticas de um analista de testes experiente. Podem salientar riscos e interações não escritos literalmente em um requisito, desde que compatíveis com as regras documentadas. Não são conhecimento tácito coletado de especialistas reais, depoimentos ou evidência de participação de profissionais.

Versão vigente: **notas 0.2-local, 06/11/2026**; prompts **0.2-local**. Responsabilidade autoral: pesquisador; apoio de redação e conferência técnica: assistente de IA. D-35 registra revisão própria declarada pelo pesquisador, sem revisor externo nesta etapa e sem aprovação atribuída ao orientador. A declaração não aprova retrospectivamente cada expectativa nem o novo texto gerado nesta etapa: este permanece para conferência do pesquisador.

A busca local por nome e conteúdo não localizou uma reformulação anterior identificada como v0.2; a referência candidata 0.2 é outro artefato. Esta é uma nova consolidação local, posterior ao exploratório já conhecido (D-34), e não uma versão presumidamente integrada. Não houve ajuste iterativo por erros/acertos ou por vantagem de condição. Essa exposição prévia deve constar como limitação. [Versão anterior integral](../documentacao/historico/pre-piloto-2026-11-06/materiais/04_NOTAS_E_PROMPTS.md).

Nesta proposta, informações indispensáveis já aparecem na documentação comum. Assim, “com notas” mede o efeito desse contexto complementar/reiterado, inclusive sua extensão, não o acesso exclusivo a uma regra secreta. Não se pode atribuir eventual ganho à autoridade de um especialista. A condição com notas necessariamente tem mais texto; registrar tokens quando disponíveis e discutir essa diferença.

## 4.2 Nota candidata única, comum a todas as mudanças

> Observações simuladas de análise de testes: hábitos de outros sistemas de autorização podem induzir suposições incompatíveis com uma política fechada. Uma dependência pode mudar o valor produzido por uma regra cujo texto permanece intacto; compartilhar um cenário, por si só, não demonstra esse impacto. Restrições de maior precedência podem ocultar uma alteração na saída final, sem retirar a relevância de um caso abrangido pela política de seleção. Uma decisão igual pode esconder mudança de motivo; conservar ambos também pode ser relevante, quando a entrada está abrangida pela política. Confundir papéis atribuídos com efetivos, ou usar a variante para decidir a aplicabilidade, pode omitir interações previstas na versão inicial.

Texto proposto, ainda sujeito à revisão de neutralidade. Não acrescentar nomes dos papéis, pares de dependência particulares, IDs de requisitos/testes ou exemplos resolvidos que revelem a seleção da mudança. Não usar as notas para inserir um passo a passo exclusivo de E1: a diferença de estrutura já é o outro fator.

## 4.3 Como preparar e revisar as notas

1. Registrar autor, apoio de IA, versão, data e exposição prévia ao exploratório. Nesta reformulação, não alegar escrita anterior às respostas conhecidas.
2. Conferir que todo conteúdo factual consta do contrato/política comum. Se faltar uma regra essencial, corrigir a documentação de todas as condições, não apenas as notas.
3. O próprio pesquisador confere respostas implícitas, pistas de IDs, pares corretos e instruções procedimentais que confundam os fatores; não haverá revisor externo nesta etapa. Registrar somente o alcance efetivamente examinado.
4. Aprovar ou reformular com justificativa registrada; guardar a versão.
5. Usar exatamente o mesmo bloco em D1 e E1, para todas as mudanças. D0/E0 não recebem arquivo nem bloco de notas, sem afirmações compensatórias.
6. Depois do congelamento, não melhorar notas ao observar erros do modelo. Registrar a limitação para a discussão ou para uma nova rodada separada.

Conferência editorial do assistente: sem IDs, solução específica, regras exclusivas ou sequência de etapas; origem registrada. Conferência final do novo texto pelo pesquisador: pendente. Equivalência de bytes: ver relatório da preparação ligado no estado atual. Nada disso aprova individualmente as expectativas candidatas.

Comparação: o texto anterior ressaltava política fechada, motivo e preservação. O novo conserva esses cuidados e acrescenta riscos de confundir impacto funcional com texto alterado/teste compartilhado, de mascaramento por precedência e de confusão entre papéis atribuídos/efetivos e versões. Cada observação deriva das definições comuns e do contrato dos requisitos; não altera a política nem acrescenta informação factual exclusiva. A extensão maior é parte da intervenção e deve ser relatada.

## 4.4 Pacote comum — montagem futura

Ordem fixa:
1. Mensagem de sistema: responder à tarefa usando apenas o material fornecido, sem ferramentas ou acesso a arquivos do projeto, no esquema exigido. Selecionar requisitos impactados e testes existentes relevantes, incluindo mudança e preservação de comportamento relacionado. Não propor novos testes, código ou descoberta de defeitos reais; não expor raciocínio interno.
2. Bloco integral de `07_DEFINICOES_COMUNS.md`: definição de impacto e relevância incluindo preservação, com a mesma política de seleção em D0/D1/E0/E1; fora das notas, sem gabaritos ou exemplos resolvidos.
3. RFs e política inicial, incluindo precedência e contrato dos motivos.
4. Catálogo T01–T12 com entradas e saídas da baseline.
5. Uma descrição de mudança, isolada, sem rótulo “direta/propagada” nem conjuntos corretos.
6. Notas: bloco candidato apenas em D1/E1.
7. Pedido direto ou estruturado.
8. Mesmo contrato de saída em todas as condições.

**Não enviar estes guias inteiros:** contêm respostas e comparações! Exportar apenas os blocos permitidos, revisar o texto montado e registrar seu hash. O ID de mudança no log pode ser mantido fora do texto enviado; isso reduz pistas desnecessárias.

## 4.5 Pedido direto — D0 e D1

> Identifique os requisitos impactados pela mudança e selecione os testes existentes relevantes conforme as definições e a política de seleção fornecidas. Retorne somente os dois conjuntos de identificadores no JSON exigido.

## 4.6 Pedido estruturado — E0 e E1

> Organize a análise em etapas: examine a regra alterada; verifique as dependências funcionais; determine os requisitos impactados; aplique a política de seleção aos casos existentes; confira as duas listas. Retorne somente os dois conjuntos de identificadores no JSON exigido.

Uma chamada e uma resposta em todas as condições. Não solicitar exposição de raciocínio interno, diálogos adicionais ou ferramentas somente nas condições estruturadas. A alteração experimental é o texto de organização em etapas; o conteúdo factual e o formato final permanecem comuns.

## 4.7 Contrato de saída

Objeto JSON com exatamente as chaves `requisitos` e `testes`, ambas listas de strings com os IDs fornecidos. Sem explicação fora do JSON; ordem não importa; não criar IDs. Listas vazias são permitidas pelo formato e avaliadas conforme o protocolo. O arquivo `modelos/schema_saida.json` formaliza a estrutura, sem conter o gabarito.

Se a API oferecer saída estruturada forçada, escolher antes do piloto se ela será usada em todas as condições. Não mudar a modalidade entre condições e não alegar que JSON válido significa seleção correta.
