# Estado atual — 07/11/2026

Fonte única da situação operacional; navegação no [README](README.md), decisões e autorizações em [decisoes.md](documentacao/decisoes.md). Registros datados descrevem seus incrementos, sem substituir este estado.

## Piloto real preservado

O pedido atual informa a execução e avaliação individual do piloto e autoriza somente organização/limpeza. A conferência offline encontrou **16 capturas reais e 16 avaliações individuais**, todas concluídas/avaliadas e com formato válido. Nenhuma nova execução foi realizada nesta organização. D-39 registra a integração offline anterior.

| Artefato utilizado | Fonte preservada |
|---|---|
| Plano, ordem e configuração efetivos | [Plano API 002](captura/plano-api-piloto-002/plano.json), idêntico ao [plano copiado no lote](captura/piloto-api-001/plano-original.json) |
| Brutos, requisições, metadados e fechamentos | [captura/piloto-api-001](captura/piloto-api-001/) |
| Avaliações individuais e lista de hashes | [avaliados/piloto-api-001/lista.json](avaliados/piloto-api-001/lista.json) |
| Resumo já produzido | [resumo.json](avaliados/piloto-api-001/resumo/resumo.json): incompleto, com diagnósticos de conformidade pendente |
| Oito payloads únicos usados duas vezes | [Preparações do plano 002](captura/plano-api-piloto-002/preparados/); origem [v2-LF](evidencias/spec004/preparacao-piloto-2026-11-06-v2-lf/RELATORIO.md) |

Configuração registrada: **GPT-6 Sol (`gpt-6-sol`), esforço `medium`**, `piloto-api-74180c81329ee360`, Responses API, limite de saída 4096, timeout 120 s, orçamento declarado USD 1,00 (não é teto imposto pelo coletor). MC-01/MC-03 × D0/D1/E0/E1 × duas repetições, na ordem do plano, sem novo sorteio. O plano original ainda diz `PLANEJADA_NAO_EXECUTADA`: retrata a preparação; tentativas/fechamentos documentam a execução. Não corrigir esse original.

As 16 avaliações têm `conformidade_protocolo=pendente`. Não foi encontrado registro de revisão separado no lote real; os exemplos de revisão da integração são sintéticos. HTTP 200, formato válido e acertos não aprovam conformidade. O resumo controlado continua bloqueado, sem alterar avaliações ou denominadores.

A [conexão neutra](captura/conexao-api-20261107-001/resultado.json) está concluída e reporta `gpt-6-sol`, na fase `verificacao_conexao`, excluída do piloto e da coleta principal. O [exploratório MC-04](evidencias/spec004/exploratorio-2026-11-05-mc04-001/) e controles sintéticos permanecem separados dos dados reais.

## Próximas tarefas e limites

1. Revisar explicitamente a conformidade das observações reais pelo [procedimento existente](documentacao/operacao-api.md#avaliação-descritiva-e-revisão-explícita-de-conformidade), com responsável, data, justificativas, inclusão/exclusão e hashes. Preservar pendentes, falhas, excluídas e N planejado. A limpeza não executa essa decisão humana.
2. Analisar o piloto e registrar decisões antes de congelar a coleta principal. Referência 0.2/política candidata, origem das notas 0.2-local e limites de interpretação permanecem como registrados nos materiais; esta organização não concede aprovação científica ou revisão externa.
3. Definir e autorizar separadamente qualquer etapa principal, suas versões, repetições, ordem e orçamento. Nenhuma chamada externa, novo piloto, coleta principal, commit ou push está autorizada nesta tarefa.

A rota Codex anterior continua bloqueada por ferramentas/contexto e retentativas internas; [D-38 e evidências](captura/analise-bloqueios-cli-2026-11-07-D38/RELATORIO.md). Seus planos, fontes e controles foram mantidos. A rota API tem identidade própria; não misturar lotes ou interpretar a integração D-39 como liberação de gasto.

## Conservação do repositório

| Classe | Conteúdo e tratamento |
|---|---|
| Essenciais e vigentes | Plano API 002, piloto real, avaliações, payloads v2-LF, notas/prompts, referência privada e justificativas nas versões usadas; código, testes/fixtures, variantes, contratos e governança. Mantidos nos caminhos existentes. |
| Históricos necessários | Plano API 001, planos/rota Codex, conexão neutra, exploratório, controles sintéticos, ferramentas e relatórios de reprodução, Specs e histórico documental. Mantidos: versões e cópias têm vínculos de hash/caminho próprios. |
| Regeneráveis comprovados | Cache Python da raiz; recomposições de `saidas-locais/verificacao-lf-v2-local-001/`; cópia `operacao-api-do-patch.md`. Removidos após comparação: 184 arquivos da recomposição idênticos aos preservados, 16 preparações diferentes apenas em ID/data sem hash referenciado; cópia documental idêntica à seção do patch original preservado. |
| Origem ou utilidade incerta | Não foi comprovada a dispensa dos scripts locais de integração nem do schema completo da CLI: mantidos como produtores/fontes históricos. Repositórios de transporte têm finalidade conhecida e também permanecem: o snapshot Git conserva o commit temporário referido nos registros. Nenhum desses ignorados foi tratado como lixo. |

Não há arquivamento novo. Os repositórios de transporte (~8 MB) são referidos para inspeção, com commit e caminhos nos comandos históricos. Compactá-los exigiria restauração antes dessas inspeções; o ganho não justifica mudar esses acessos. As evidências já guardam relatórios compactos dos checkouts. Os schemas (~4,4 MB) e scripts também permanecem acessíveis. `.gitignore` não autoriza excluir seu conteúdo.

Versões científicas e ferramentas não foram movidas, normalizadas ou regravadas. `.gitattributes` conserva a política de bytes. Histórico de decisões em [decisoes.md](documentacao/decisoes.md), versões documentais em [historico/](documentacao/historico/). O pacote [revisão profissional v1](documentacao/revisao-profissional-spec004-v1/LEIA-PRIMEIRO.md) é histórico; não representa parecer externo obtido.
