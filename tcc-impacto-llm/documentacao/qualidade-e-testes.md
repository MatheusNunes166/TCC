# Qualidade e testes da bancada

> Estado vigente — 19/10/2026 (D-15/D-16): T12 adotado pelo pesquisador e verificado na versão inicial como negar/conflito. Python 3.13.3: teste isolado OK; suíte integrada com 18 métodos OK, T01–T12 12/12 e controles anteriores preservados. Catálogo: 12 testes; referência candidata: 48 pares teste × mudança, 60 expectativas incluindo a versão inicial; seleções 2/4/8/5. Variantes não implementadas nem executadas; sem piloto ou LLM experimental. A adoção é autorização do pesquisador, sem aprovação científica atribuída ao orientador. Revisão científica e adoção formal da constituição continuam pendentes. Evidências: `documentacao/evidencias-t12.md` (caminho desde a raiz).

## Estratégia de verificação

Revisar primeiro regras, precedência, entradas e expectativas com o revisor a combinar. Futuramente, verificar cada capacidade pequena, registrar evidências reais e reconciliar resultados com o contrato antes de avançar. Divergência entre implementação e expectativa exige análise das regras; nenhuma das duas deve ser promovida automaticamente a verdade.

Verificar decisão e motivo. A suíte completa só é exigida após herança e incompatibilidade; o primeiro incremento verifica o subconjunto compatível com sua capacidade. A suíte é pequena e não promete cobertura total de RBAC. Os vínculos abaixo indicam comportamentos exercitados, sem substituir a política de impacto experimental.

## Doze casos da baseline

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
| T12 | ativa | Supervisão + Auditoria | exportar | negar | conflito | RF-01 prossegue; RF-03 inclui Consulta; RF-04 supera exportar direto de RF-02 |

## Variantes e avaliação futura

As quatro mudanças e as 48 expectativas teste × mudança permanecem no material de referência. Conferir todas antes do piloto, mantendo alterações independentes. Em MC-04-v2, T07 continua negado, mas o motivo candidato muda para `sem_permissao`; conferir somente a decisão seria insuficiente.

Antes da coleta, verificar parser e pontuação com exemplos sintéticos de seleção vazia, todos, exata, parcial, formato inválido, duplicatas e IDs inexistentes. Esses exemplos não são resultados da pesquisa. O protocolo define fórmulas e tratamento de falhas, sem necessidade de reproduzi-los integralmente aqui.

**Redução nominal só pode ser interpretada favoravelmente em resposta válida, com seleção completa dos testes relevantes (revocação de testes = 1) e sem IDs inexistentes.** Não implica economia real de tempo ou detecção de defeitos. Omissões e revocação têm prioridade de apresentação.

Documentação preparada não libera o piloto: ainda são necessárias baseline/variantes verificadas, referência e notas revisadas, coleta rastreável, isolamento demonstrado e avaliador conferido. Critérios completos em [piloto/coleta](../materiais/05_PILOTO_E_COLETA.md); sequência em [roadmap.md](roadmap.md).


## Adoção de T12 — P-04/D-15

T12 foi adotado pelo pesquisador em 19/10/2026 e executado na versão inicial, com decisão e motivo conformes. A suíte integrada mantém os onze casos anteriores e todos os controles; 18 métodos OK. Evidências em [evidencias-t12.md](evidencias-t12.md). Adoção e execução local não validam cientificamente o gabarito.

Expectativas candidatas: MC-01 negar/conflito, preservação selecionada; MC-02 permitir/permissao_direta, mudança selecionada; MC-03 negar/conflito, excluído por operação; MC-04-v2 permitir/permissao_direta, mudança selecionada. MC-04 nesta etapa designa MC-04-v2 (retirada de herança), preservando o ID do JSON.

São 12 testes, 48 pares teste × mudança e 60 expectativas incluindo a versão inicial; seleções 2/4/8/5. Conjuntos, justificativas e matriz em [referência candidata](referencia-candidata-proxima-etapa.md) e [material 02](../materiais/02_REQUISITOS_TESTES_E_REFERENCIA.md). Versão anterior preservada em [histórico pré-T12](historico/pre-t12-2026-10-19/LEIA_PRIMEIRO.md). Variantes não implementadas nem executadas.
