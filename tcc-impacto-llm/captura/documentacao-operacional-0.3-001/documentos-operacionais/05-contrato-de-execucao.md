# Contrato de execução

O processamento primeiro verifica o estado. Para a conta que prossegue,
obtém as permissões diretas e realiza a expansão configurada antes de
verificar incompatibilidades e decidir sobre a operação.

Aplicar o primeiro retorno cuja condição seja satisfeita, na prioridade indicada.

| Prioridade | Condição | Decisão | Motivo |
| --- | --- | --- | --- |
| 1 | estado diferente de ativa | negar | estado |
| 2 | existe incompatibilidade no conjunto efetivo | negar | conflito |
| 3 | operação possui concessão direta | permitir | permissao_direta |
| 4 | operação possui concessão herdada | permitir | permissao_herdada |
| 5 | nenhuma condição anterior satisfeita | negar | sem_permissao |

Um incremento parcial de RF-01/RF-02 não pode redefinir o contrato global
ou alegar suporte a RF-03/RF-04.
