# Parte 1 — Contexto e notas

Pacote 1.0 • 01/11/2026 • **Rascunho para revisão profissional**.

Examinar e comentar as notas nesta parte antes de consultar a Parte 2 ou conjuntos de respostas. Usar a seção A da ficha. Não há respostas selecionadas por mudança nesta parte; catálogo da baseline e descrições de mudança são contexto necessário e podem permitir deduções.

## Objetivo e limites da pesquisa

Comparar como a organização da solicitação e a presença de notas que representam conhecimento de analista de testes afetam os IDs de requisitos impactados e testes existentes relevantes selecionados por um único LLM, a definir. Observar acertos, omissões, seleções excedentes e consistência, sem medir participantes juniores, geração de testes novos/código, descoberta de defeitos reais, cobertura ou economia de tempo.

A bancada fictícia recebe estado de conta, papéis e operação e devolve decisão com motivo. Domínio fechado: estados `ativa`, `suspensa`, `em_revisao`; papéis Consulta, Auditoria, Supervisão; operações visualizar/exportar. Herança de um nível, sem ciclos, usuários reais, banco ou interface.

| Condição candidata | Pedido | Notas |
|---|---|---|
| D0 | Direto | Ausentes |
| D1 | Direto | Mesmo bloco rascunho N |
| E0 | Organizado em etapas | Ausentes |
| E1 | Organizado em etapas | Mesmo bloco rascunho N |

As quatro condições recebem as mesmas definições, regras, catálogo inicial, descrição da mudança e schema; o pedido é igual em D0/D1 e em E0/E1. O bloco N é o mesmo para todas as mudanças em D1/E1; D0/E0 não têm bloco/delimitador de notas. O material histórico menciona seção vazia; o contrato vigente D-29 exige ausência integral. O LLM só recebe texto preparado, sem ferramentas, código, comandos, gabarito, variantes ou histórico. Revisão científica e desenho final do piloto pendentes; nenhuma chamada/modelo novo ou piloto nesta preparação.

## Quatro requisitos e dependências da baseline B

| ID | Regra da bancada |
|---|---|
| RF-01 | Somente conta ativa prossegue. Suspensa/em revisão retornam `negar/estado`, mesmo havendo permissão ou conflito. |
| RF-02 | Obter permissões diretas dos papéis atribuídos: Consulta concede visualizar; Auditoria concede exportar; Supervisão não tem concessão própria. |
| RF-03 | Supervisão inclui Consulta como papel efetivo e herda sua permissão de visualizar; não herda exportar. Um nível de herança. |
| RF-04 | Consulta + Auditoria efetivos são incompatíveis; retornar `negar/conflito`, inclusive quando Consulta vier da herança. |

Ordem: verificar estado → obter permissões diretas e expandir herança → verificar conflito sobre papéis efetivos → decidir pela permissão. Sem concessão: `negar/sem_permissao`; com concessão: `permitir/permissao_direta` ou `permitir/permissao_herdada`. Se direta e herdada coexistirem, usar motivo direto. Concessões nunca superam estado ou conflito.

RF-03 usa as concessões de RF-02 para produzir permissões herdadas e fornece papéis efetivos à verificação de RF-04. RF-04 depende dos papéis efetivos, não da existência de uma concessão. RF-01 tem precedência sobre todas as demais. Participar de uma mesma execução ou ser pré-condição não significa automaticamente ser requisito impactado.

## Quatro mudanças independentes

| Mudança | Única alteração sobre B |
|---|---|
| MC-01 | Retirar Auditoria → exportar de RF-02. |
| MC-02 | Retirar a incompatibilidade Consulta + Auditoria de RF-04. |
| MC-03 | Retirar Consulta → visualizar de RF-02. |
| MC-04-v2 | Retirar Supervisão → Consulta da herança de RF-03. |

Nenhuma mudança acumula a anterior. MC-04 é rótulo curto para MC-04-v2; a antiga proposta sobre conta em revisão não participa deste pacote. As descrições acima não informam os conjuntos candidatos de requisitos/testes impactados.

## Catálogo T01–T12 e expectativas da baseline

Papéis abaixo são os atribuídos; a expansão de herança é feita pelas regras. A saída inclui **decisão e motivo**. Resultados esperados da baseline fazem parte do contexto comum das condições; não são seleções de respostas por mudança.

| Teste | Estado | Papéis atribuídos | Operação | Expectativa em B |
|---|---|---|---|---|
| T01 | suspensa | Consulta | visualizar | negar/estado |
| T02 | ativa | Consulta | visualizar | permitir/permissao_direta |
| T03 | ativa | Consulta | exportar | negar/sem_permissao |
| T04 | ativa | Auditoria | exportar | permitir/permissao_direta |
| T05 | ativa | Supervisão | visualizar | permitir/permissao_herdada |
| T06 | ativa | Consulta + Auditoria | visualizar | negar/conflito |
| T07 | ativa | Supervisão + Auditoria | visualizar | negar/conflito |
| T08 | ativa | Supervisão | exportar | negar/sem_permissao |
| T09 | em_revisao | Consulta | visualizar | negar/estado |
| T10 | em_revisao | Supervisão | visualizar | negar/estado |
| T11 | em_revisao | Consulta + Auditoria | visualizar | negar/estado |
| T12 | ativa | Supervisão + Auditoria | exportar | negar/conflito |

T12 já foi adotado pelo pesquisador; sua adoção técnica não comprova aprovação científica das expectativas.

## Definições comuns candidatas

Reproduzidas do material 07, igualmente presentes nas quatro condições e fora das notas. A adequação profissional dessa política conservadora também está aberta à revisão.

Este bloco deve constar integralmente e com o mesmo texto no pacote comum às quatro condições. Sua presença independe das notas. A política é conservadora e específica desta bancada; não procura um subconjunto mínimo nem garante detecção de todos os defeitos.

**Requisito impactado:** regra diretamente alterada ou regra dependente cujo valor funcional produzido se altera em pelo menos um cenário válido da suíte. O texto da regra dependente pode permanecer igual. Consideram-se permissões diretas, permissões herdadas, papéis efetivos e predicado de incompatibilidade, além da saída final. Uma mera pré-condição ou um teste compartilhado não basta para incluir outro requisito.

**Teste relevante:** caso existente cuja entrada se enquadra no item de política alterado, direta ou indiretamente, mesmo se uma restrição de precedência maior mantiver o resultado. Pode verificar mudança de comportamento ou preservação de comportamento relacionado. A aplicabilidade é estrutural, com os papéis efetivos da versão inicial; não exige que a execução alcance a regra.

**Mudança de comportamento:** alteração de decisão ou motivo, pois ambos compõem a saída observável. **Preservação relacionada:** decisão e motivo permanecem iguais em um caso que satisfaz a política de seleção, inclusive quando estado ou conflito prevalecem sobre a regra alterada. Manter a saída, isoladamente, não torna qualquer teste relevante.

Selecionar todos os casos existentes que satisfaçam a regra aplicável:

1. **Permissão:** a operação do teste é a alterada e seu conjunto de papéis efetivos da versão inicial contém o papel cuja concessão mudou.
2. **Incompatibilidade:** os papéis efetivos da versão inicial contêm o par cuja restrição mudou, independentemente do estado da conta.
3. **Herança:** os papéis atribuídos do teste contêm o papel filho da relação alterada, independentemente da operação ou estado.

Aplicar a mesma política a todas as mudanças. Cada mudança parte, isoladamente, da mesma versão inicial. Não recalcular aplicabilidade com os papéis da variante. Requisitos impactados e testes relevantes são conjuntos distintos, obtidos por critérios distintos.

## Nota atual — RASCUNHO_NAO_REVISADO

Bloco único, reproduzido literalmente de materiais/04 §4.2, sem acrescentar instruções ou IDs ao texto:

> Observações do analista de testes: esta bancada usa uma política fictícia e fechada; práticas habituais de outros sistemas de autorização não substituem as regras documentadas. O motivo da decisão faz parte do resultado observável, inclusive quando a operação continua negada. Os casos de preservação previstos na política de seleção têm relevância mesmo sem alteração do resultado esperado.

**Origem documentada:** materiais/04 §4.1 atribui a redação ao pesquisador no papel de analista de testes, com base nas regras e contratos revisados. É um artefato de trabalho do projeto; não é depoimento, conhecimento tácito coletado ou texto produzido/revisado por profissional externo. Esta compilação e sua transcrição foram feitas pelo assistente de IA. Os registros consultados não individualizam autor/data de cada observação nem permitem atestar o grau de apoio de IA na redação original; o pesquisador deve confirmar esses dados na ficha. Não atribuir o bloco ao futuro revisor.

A intenção é tornar informações já disponíveis no contexto mais salientes. A presença de mais texto pode influenciar a resposta; eventual diferença não provaria efeito da autoridade de um especialista. Conteúdo definitivo, utilidade profissional e neutralidade ainda não foram aprovados.

## Perguntas antes de consultar os conjuntos candidatos

1. As observações são tecnicamente corretas e úteis a um profissional que seleciona requisitos/testes após uma mudança? Qual experiência concreta sustenta seu parecer? Podem ser apenas repetição das definições comuns?
2. As notas representam conhecimento profissional útil ou apenas lembram particularidades artificiais desta bancada? A denominação “observações do analista de testes” descreve adequadamente sua origem e alcance?
3. Alguma frase antecipa uma resposta específica, aponta implicitamente um requisito/teste ou beneficia uma das mudanças? Citar o trecho e explicar a pista percebida, mesmo sem saber o conjunto candidato.
4. Alguma informação indispensável está disponível apenas na nota? Se sim, indicar o que deveria ser documento comum a todas as condições, sem editar as fontes agora.
5. A ênfase em motivo e preservação é adequada e neutra, ou induz seleção excessiva? A política distingue preservação relacionada de simples ausência de mudança?
6. Há instrução de procedimento exclusiva que confunda o fator “notas” com o fator “organização em etapas”? Há redação ambígua, redundante ou ausente que mereça sugestão identificada?

Registrar concordâncias, divergências, justificativas e sugestões na seção A da [ficha](03-ficha-de-revisao.md), inclusive “sem sugestão” quando cabível. Se complementar ou produzir texto novo, indicar autoria real e separar a proposta do bloco original. Só depois consultar a Parte 2; preservar o parecer inicial.

Detalhes opcionais sem conjuntos selecionados: [regras](../requisitos.md), [definições](../../materiais/07_DEFINICOES_COMUNS.md). Links para materiais completos com respostas ficam na Parte 2.
