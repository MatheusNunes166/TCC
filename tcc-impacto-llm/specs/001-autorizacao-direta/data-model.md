# Modelo de dados proposto — incremento 001

> Atualização vigente — 16/10/2026: RF-01/RF-02 implementados e verificados com Python 3.13.3 + unittest, sem terceiros. Sete casos de aceitação conformes, três concessões próprias, 32 combinações de estado e controle Auditoria/visualizar; 10 métodos, zero falhas/erros/ignorados. Evidências em `specs/001-autorizacao-direta/evidencias.md` (caminho desde a raiz). D-09/D-10 registram recorte aceito e autorização. Domínio ativo parcial somente Consulta ou Auditoria isoladamente; RF-03/RF-04 permanecem futuros. Afirmações de ausência de autorização/implementação nos registros de 14/10 abaixo são históricas, superadas somente nesse alcance. Constituição não formalmente adotada; referência, notas, prompts, métricas e piloto pendentes. Nenhum piloto ou LLM experimental executado.


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
