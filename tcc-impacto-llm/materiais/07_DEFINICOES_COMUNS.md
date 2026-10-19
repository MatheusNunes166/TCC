# Definições comuns de impacto e relevância

Este bloco deve constar integralmente e com o mesmo texto no pacote comum às quatro condições. Sua presença independe das notas. A política é conservadora e específica desta bancada; não procura um subconjunto mínimo nem garante detecção de todos os defeitos.

**Requisito impactado:** regra diretamente alterada ou regra dependente cujo valor funcional produzido se altera em pelo menos um cenário válido da suíte. O texto da regra dependente pode permanecer igual. Consideram-se permissões diretas, permissões herdadas, papéis efetivos e predicado de incompatibilidade, além da saída final. Uma mera pré-condição ou um teste compartilhado não basta para incluir outro requisito.

**Teste relevante:** caso existente cuja entrada se enquadra no item de política alterado, direta ou indiretamente, mesmo se uma restrição de precedência maior mantiver o resultado. Pode verificar mudança de comportamento ou preservação de comportamento relacionado. A aplicabilidade é estrutural, com os papéis efetivos da versão inicial; não exige que a execução alcance a regra.

**Mudança de comportamento:** alteração de decisão ou motivo, pois ambos compõem a saída observável. **Preservação relacionada:** decisão e motivo permanecem iguais em um caso que satisfaz a política de seleção, inclusive quando estado ou conflito prevalecem sobre a regra alterada. Manter a saída, isoladamente, não torna qualquer teste relevante.

Selecionar todos os casos existentes que satisfaçam a regra aplicável:

1. **Permissão:** a operação do teste é a alterada e seu conjunto de papéis efetivos da versão inicial contém o papel cuja concessão mudou.
2. **Incompatibilidade:** os papéis efetivos da versão inicial contêm o par cuja restrição mudou, independentemente do estado da conta.
3. **Herança:** os papéis atribuídos do teste contêm o papel filho da relação alterada, independentemente da operação ou estado.

Aplicar a mesma política a todas as mudanças. Cada mudança parte, isoladamente, da mesma versão inicial. Não recalcular aplicabilidade com os papéis da variante. Requisitos impactados e testes relevantes são conjuntos distintos, obtidos por critérios distintos.
