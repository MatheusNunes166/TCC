# Pendências

D-39/API: integração e testes offline concluídos, sem autorização de gasto/conexão/piloto. Pendente autorização específica, acesso real GPT-6 Sol/medium, configuração/limite que comporte raciocínio+final, preço/orçamento e revisões de materiais já registradas. Conformidade real começa pendente e tem [procedimento separado de revisão](documentacao/operacao-api.md#avaliação-descritiva-e-revisão-explícita-de-conformidade). Nenhuma lista autenticada de modelos foi consultada nesta integração. Os bloqueios D-38 abaixo continuam próprios da rota Codex, cuja trava não foi alterada.

D-38: **ambos continuam pendentes**, agora delimitados: contexto adicional no render/inventário tools não demonstrado; provedor embutido openai rejeita redefinição de retries. Chaves de skills/memórias/provedor/auth e strict-config aceitas foram aplicadas, sem retirar a trava. [Tabela e evidências](captura/analise-bloqueios-cli-2026-11-07-D38/RELATORIO.md). O registro D-37 abaixo permanece como estado anterior.

D-37: envio por `codex exec` bloqueado em código. Faltam demonstração de `tools=[]`/contexto textual D-29 e controle das retentativas internas da CLI; autenticação e catálogo local não comprovam acesso remoto ao modelo. [Evidências e limites](captura/controles-coletor-2026-11-07/RELATORIO.md). Não há bloqueio para simulação, controles locais ou avaliação offline.
O estado e as pendências vigentes estão centralizados em [ESTADO_ATUAL.md — Antes de qualquer chamada](ESTADO_ATUAL.md#antes-de-qualquer-chamada-do-piloto). D-35 retira a revisão externa do procedimento desta etapa, sem presumir aprovação das expectativas. Não há bloqueio para a preparação offline autorizada.

Registros anteriores preservados em [histórico](documentacao/historico/pre-piloto-2026-11-06/BLOQUEIOS.md).
