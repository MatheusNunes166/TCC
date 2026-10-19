# 4. Notas do analista e solicitações ao LLM

## 4.1 O que as notas representam

São observações redigidas pelo pesquisador no papel de analista de testes, com base nas regras e nos contratos revisados. Seu propósito experimental é verificar se tornar certas informações mais salientes altera a seleção. Não afirmar que são conhecimento tácito de especialistas reais, experiência profissional coletada ou evidência de participação humana.

Nesta proposta, informações indispensáveis já aparecem na documentação comum. Assim, “com notas” mede o efeito desse contexto complementar/reiterado, inclusive sua extensão, não o acesso exclusivo a uma regra secreta. Não se pode atribuir eventual ganho à autoridade de um especialista. A condição com notas necessariamente tem mais texto; registrar tokens quando disponíveis e discutir essa diferença.

## 4.2 Nota candidata única, comum a todas as mudanças

> Observações do analista de testes: esta bancada usa uma política fictícia e fechada; práticas habituais de outros sistemas de autorização não substituem as regras documentadas. O motivo da decisão faz parte do resultado observável, inclusive quando a operação continua negada. Os casos de preservação previstos na política de seleção têm relevância mesmo sem alteração do resultado esperado.

Texto proposto, ainda sujeito à revisão de neutralidade. Não acrescentar nomes dos papéis, pares de dependência particulares, IDs de requisitos/testes ou exemplos resolvidos que revelem a seleção da mudança. Não usar as notas para inserir um passo a passo exclusivo de E1: a diferença de estrutura já é o outro fator.

## 4.3 Como preparar e revisar as notas

1. Escrever antes de consultar respostas experimentais; registrar autor, data e origem de cada observação.
2. Conferir que todo conteúdo factual consta do contrato/política comum. Se faltar uma regra essencial, corrigir a documentação de todas as condições, não apenas as notas.
3. Pedir ao revisor combinado que procure respostas implícitas, pistas de IDs, repetições de pares corretos e instruções procedimentais que confundam os fatores.
4. Aprovar ou reformular com justificativa registrada; guardar a versão.
5. Usar exatamente o mesmo bloco em D1 e E1, para todas as mudanças. D0/E0 recebem uma seção vazia de notas, sem afirmações compensatórias.
6. Depois do congelamento, não melhorar notas ao observar erros do modelo. Registrar a limitação para a discussão ou para uma nova rodada separada.

Checklist: [ ] não contém gabarito; [ ] não resolve uma mudança; [ ] não cria regra exclusiva; [ ] não traz instruções de etapas; [ ] tem origem registrada; [ ] revisão humana registrada; [ ] mesmo texto em D1/E1.

## 4.4 Pacote comum — montagem futura

Ordem fixa:
1. Mensagem de sistema: responder à tarefa usando apenas o material fornecido, sem ferramentas externas, no esquema exigido.
2. Definição de requisito impactado e política de seleção (documentos 1.2 e 2.3, sem gabaritos).
3. RFs e política inicial, incluindo precedência e contrato dos motivos.
4. Catálogo T01–T11 com entradas e saídas da baseline.
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
