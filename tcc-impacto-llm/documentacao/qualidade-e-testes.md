# Qualidade e testes planejados

Estado: onze casos planejados, não implementados nem executados nesta entrega. Os resultados abaixo são expectativas candidatas da baseline, derivadas de [requisitos.md](requisitos.md) e do [material de referência](../materiais/02_REQUISITOS_TESTES_E_REFERENCIA.md); não constituem gabarito validado.

## Estratégia de verificação

Revisar primeiro regras, precedência, entradas e expectativas com o revisor a combinar. Futuramente, verificar cada capacidade pequena, registrar evidências reais e reconciliar resultados com o contrato antes de avançar. Divergência entre implementação e expectativa exige análise das regras; nenhuma das duas deve ser promovida automaticamente a verdade.

Verificar decisão e motivo. A suíte completa só é exigida após herança e incompatibilidade; o primeiro incremento verifica o subconjunto compatível com sua capacidade. A suíte é pequena e não promete cobertura total de RBAC. Os vínculos abaixo indicam comportamentos exercitados, sem substituir a política de impacto experimental.

## Onze casos da baseline

| ID | Estado | Papéis | Operação | Decisão esperada | Motivo esperado | RFs exercitados em destaque |
|---|---|---|---|---|---|---|
| T01 | suspensa | Consulta | visualizar | negar | estado | RF-01 |
| T02 | ativa | Consulta | visualizar | permitir | permissao_direta | RF-02 |
| T03 | ativa | Consulta | exportar | negar | sem_permissao | RF-02 |
| T04 | ativa | Auditoria | exportar | permitir | permissao_direta | RF-02 |
| T05 | ativa | Supervisão | visualizar | permitir | permissao_herdada | RF-03 |
| T06 | ativa | Consulta + Auditoria | visualizar | negar | conflito | RF-04 |
| T07 | ativa | Supervisão + Auditoria | visualizar | negar | conflito | RF-03, RF-04 |
| T08 | ativa | Supervisão | exportar | negar | sem_permissao | RF-02, RF-03 |
| T09 | em_revisao | Consulta | visualizar | negar | estado | RF-01 |
| T10 | em_revisao | Supervisão | visualizar | negar | estado | RF-01 |
| T11 | em_revisao | Consulta + Auditoria | visualizar | negar | estado | RF-01; preservação da precedência sobre conflito |

## Variantes e avaliação futura

As quatro mudanças e as 44 expectativas teste × mudança permanecem no material de referência. Conferir todas antes do piloto, mantendo alterações independentes. Em MC-04-v2, T07 continua negado, mas o motivo candidato muda para `sem_permissao`; conferir somente a decisão seria insuficiente.

Antes da coleta, verificar parser e pontuação com exemplos sintéticos de seleção vazia, todos, exata, parcial, formato inválido, duplicatas e IDs inexistentes. Esses exemplos não são resultados da pesquisa. O protocolo define fórmulas e tratamento de falhas, sem necessidade de reproduzi-los integralmente aqui.

**Redução nominal só pode ser interpretada favoravelmente em resposta válida, com seleção completa dos testes relevantes (revocação de testes = 1) e sem IDs inexistentes.** Não implica economia real de tempo ou detecção de defeitos. Omissões e revocação têm prioridade de apresentação.

Documentação preparada não libera o piloto: ainda são necessárias baseline/variantes verificadas, referência e notas revisadas, coleta rastreável, isolamento demonstrado e avaliador conferido. Critérios completos em [piloto/coleta](../materiais/05_PILOTO_E_COLETA.md); sequência em [roadmap.md](roadmap.md).
