# Especificação funcional

## Entradas e saídas

Entrada: estado (`ativa`, `suspensa`, `em_revisao`), conjunto de papéis (`Consulta`, `Auditoria`, `Supervisão`) e operação (`visualizar`, `exportar`). Vocabulário fechado, dados fictícios e entradas válidas; validação de entradas malformadas está fora do recorte.

Saída: decisão `permitir` ou `negar`, acompanhada de um motivo estável: `estado`, `conflito`, `sem_permissao`, `permissao_direta` ou `permissao_herdada`. Decisão e motivo compõem o resultado observável.

## Requisitos

| ID | Regra |
| --- | --- |
| RF-01 | Somente conta ativa prossegue. |
| RF-02 | Obter permissões diretas dos papéis atribuídos. |
| RF-03 | Expandir papéis e permissões por uma relação de herança de um nível. |
| RF-04 | Verificar incompatibilidade entre papéis efetivos. |
