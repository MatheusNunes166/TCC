# Modelo de dados proposto — incremento 001

Somente desenho, sem código ou persistência. Vocabulário de origem em [requisitos](../../documentacao/requisitos.md); uso parcial em [contrato](contracts/autorizacao.md).

| Conceito | Representação proposta | Regras |
|---|---|---|
| Estado | string | `ativa`, `suspensa`, `em_revisao`; recebido por solicitação. |
| Papéis atribuídos | `frozenset[str]` | Subconjunto de `Consulta`, `Auditoria`, `Supervisão`; sem duplicatas ou ordem significativa. |
| Operação | string | `visualizar` ou `exportar`. |
| Concessões próprias | Relação local papel → conjunto de operações | Consulta → visualizar; Auditoria → exportar; Supervisão → vazio. Não representa papéis efetivos ou herança. |
| Resultado | `dict[str, str]` com exatamente `decisao` e `motivo` | Uma decisão e um motivo estável, sem mutação da entrada. |

Resultado no domínio parcial: `negar/estado`, `permitir/permissao_direta` ou `negar/sem_permissao`. O vocabulário global inclui ainda `conflito` e `permissao_herdada`, sem produzi-los ou removê-los do contrato nesta entrega.

Não há entidade de usuário, credenciais, conta persistida ou alteração de estado. O estado é um dado de entrada; não existem transições ou operações de cadastro/suspensão implementadas neste incremento.

As entradas são precondições válidas. Validação de strings desconhecidas, normalização de maiúsculas, tratamento de dados malformados e resposta para cenários ativos dependentes das capacidades futuras não são acrescentados. O domínio parcial é descrito no contrato e não reduz o domínio final do sistema.
