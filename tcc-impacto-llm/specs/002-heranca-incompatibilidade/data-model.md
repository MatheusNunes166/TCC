# Modelo de dados planejado — Spec 002

Desenho para futura implementação; nada persistido. [Contrato](contracts/autorizacao.md).

| Conceito | Representação | Regra |
|---|---|---|
| Estado | str | ativa, suspensa, em_revisao. |
| Papéis atribuídos | frozenset[str] | Qualquer subconjunto de Consulta/Auditoria/Supervisão, inclusive vazio. |
| Operação | str | visualizar ou exportar. |
| Papéis efetivos | frozenset[str] derivado | Atribuídos unidos a Consulta se Supervisão presente; sem recursão. |
| Permissões diretas dos atribuídos | frozenset[str] derivado | Consulta: visualizar; Auditoria: exportar; Supervisão: vazio. |
| Permissões disponíveis pelos efetivos | frozenset[str] derivado | União das concessões próprias dos efetivos; não substitui a origem direta. |
| Incompatibilidade | bool derivado | Consulta e Auditoria presentes nos efetivos, independentemente da operação. |
| Resultado | dict[str, str] | Exatamente decisao e motivo; ambos strings. |

Motivos: estado, conflito, sem_permissao, permissao_direta, permissao_herdada; decisões permitir/negar. Sem campos novos.

Todos os conjuntos retornados são imutáveis. Não há alteração dos atribuídos, estado global mutável, entidade de usuário, armazenamento ou transição de conta. Estado é entrada de cada avaliação.

Entradas válidas são precondições: não há normalização, tratamento de grafias desconhecidas, regra para dados malformados ou novo erro de domínio. O domínio integrado futuro compreende 48 entradas válidas possíveis; o código existente continua com domínio parcial até implementação/verificação. Isso não muda o catálogo nem incorpora T12.
