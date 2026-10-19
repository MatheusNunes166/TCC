> Complemento vigente — 19/10/2026, D-15/D-16: T12 adotado pelo pesquisador e acrescentado à suíte da versão inicial; teste isolado OK e 18 métodos integrados OK. Catálogo atual T01–T12, 48 pares e 60 expectativas com a versão inicial, referência ainda candidata. Evidências em `documentacao/evidencias-t12.md` desde a raiz. O conteúdo datado abaixo preserva o escopo e as evidências originais da Spec 002 (T01–T11); menções a T12 como proposta ou fora da aceitação descrevem aquele incremento, superadas por D-15 apenas nesse alcance. Sem variantes, piloto ou LLM experimental; sem aprovação científica atribuída ao orientador.

> Estado vigente — 18/10/2026 (D-13/D-14): Spec 002 implementada com Python 3.13.3 + unittest. RF-01–RF-04 integrados; 17 métodos aprovados, T01–T11 11/11 em decisão/motivo e 55 subtestes auxiliares conformes, zero falhas/erros/ignorados. Três estados, oito subconjuntos e duas operações no domínio válido; verificação dirigida, sem matriz que inclua T12. Evidências em `specs/002-heranca-incompatibilidade/quickstart.md` (caminho desde a raiz). T12 somente proposta; catálogo 11/44 e gabarito preservados. Sem variantes, piloto ou LLM experimental. Adoção constitucional e pendências científicas permanecem abertas. Trechos datados anteriores abaixo são históricos e não descrevem a capacidade atual.

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
