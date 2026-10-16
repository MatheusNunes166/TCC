# Pesquisa de desenho — Spec 002

Data: 16/10/2026. Revisão do código, testes, Spec e contrato locais; sem teste de aplicação ou pesquisa experimental. Python + unittest e organização existente solicitados pelo usuário; escolhas abaixo são desenho técnico, não aprovação científica.

## Linguagem e organização

**Decisão**: manter Python 3.11+, unittest e os dois arquivos existentes. Versão 3.13.3 comprovada apenas na execução do incremento 1.
**Justificativa**: capacidade pequena em memória; nenhuma necessidade de terceiros ou reorganização.
**Alternativas**: pytest acrescenta dependência; classes, enum/dataclass e módulos adicionais não resolvem lacuna deste recorte.

## Expansão e conflito

**Decisão**: funções puras `obter_papeis_efetivos` e `ha_incompatibilidade`. União imutável acrescenta Consulta quando houver Supervisão; predicado verifica Consulta e Auditoria nos efetivos.
**Justificativa**: torna valores intermediários observáveis sem framework e separa RF-03 de RF-04.
**Alternativas**: recursão, grafo e política configurável ampliam escopo; tudo dentro de autorizar reduz verificabilidade dos valores intermediários.

## Concessões e origem

**Decisão**: preservar a consulta direta e usá-la separadamente sobre atribuídos e efetivos. Autorizar verifica estado, calcula permissões/efetivos, verifica conflito, decide direta, depois herdada, depois ausência.
**Justificativa**: impede classificar visualizar herdado de Supervisão como direto e preserva a preferência direta em Supervisão + Consulta.
**Alternativas**: auxiliar público específico de permissões herdadas acrescenta interface desnecessária; calcular origem apenas pela diferença efetivos menos atribuídos obscurece coexistência das origens. Política mutável não deve ser exposta.

## Domínio e integração

**Decisão**: ampliar futuramente o domínio ativo para todos os subconjuntos, preservando apenas as garantias anteriores. Mesmas entradas e saída; sem tratamento novo de malformados.
**Justificativa**: resultados incidentais do núcleo parcial não devem impedir RF-03/RF-04.
**Alternativas**: manter restrição parcial após implementar regras deixa a baseline incompleta; inventar exceções/negações para ativos antes da implementação altera contrato.

**Decisão**: integrar T05–T08, conservar os sete casos e controles, acrescentar bordas da Spec e testes de efetivos/conflito. T12 permanece fora da aceitação e da execução planejada.
**Justificativa**: assegura regressão e observabilidade dos motivos sem mudar catálogo experimental. Regras gerais abrangem semanticamente T12, mas isso não equivale a adotar o cenário.
**Alternativas**: executar matriz completa de autorizar incluiria T12 e ultrapassaria sua separação; verificar apenas permitir/negar perde distinção de motivos.

## Conclusão documental

Revisão auxiliar de pesquisa prevista na skill speckit-plan confirmou o desenho mínimo e ausência de dúvida funcional bloqueante. Nenhum código/teste alterado ou executado. Contratos científicos, T12, piloto e adoção constitucional continuam pendentes. Fontes: [Spec](spec.md), [contrato completo](../../documentacao/requisitos.md), [contrato anterior](../001-autorizacao-direta/contracts/autorizacao.md), autorizacao.py e tests/test_autorizacao.py na raiz.
