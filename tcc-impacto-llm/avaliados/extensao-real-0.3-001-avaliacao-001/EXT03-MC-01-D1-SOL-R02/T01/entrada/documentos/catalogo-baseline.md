| ID | Estado | Papéis | Operação | Decisão esperada | Motivo esperado |
| --- | --- | --- | --- | --- | --- |
| T01 | suspensa | Consulta | visualizar | negar | estado |
| T02 | ativa | Consulta | visualizar | permitir | permissao_direta |
| T03 | ativa | Consulta | exportar | negar | sem_permissao |
| T04 | ativa | Auditoria | exportar | permitir | permissao_direta |
| T05 | ativa | Supervisão | visualizar | permitir | permissao_herdada |
| T06 | ativa | Consulta + Auditoria | visualizar | negar | conflito |
| T07 | ativa | Supervisão + Auditoria | visualizar | negar | conflito |
| T08 | ativa | Supervisão | exportar | negar | sem_permissao |
| T09 | em_revisao | Consulta | visualizar | negar | estado |
| T10 | em_revisao | Supervisão | visualizar | negar | estado |
| T11 | em_revisao | Consulta + Auditoria | visualizar | negar | estado |
| T12 | ativa | Supervisão + Auditoria | exportar | negar | conflito |
| T13 | ativa | Consulta + Supervisão | visualizar | permitir | permissao_direta |
| T14 | ativa | Consulta + Auditoria + Supervisão | exportar | negar | conflito |
| T15 | em_revisao | Consulta + Auditoria + Supervisão | exportar | negar | estado |
