# Estado atual — 09/11/2026

Fonte única da situação operacional; navegação no [README](README.md), decisões e autorizações em [decisoes.md](documentacao/decisoes.md). Registros datados descrevem seus incrementos, sem substituir este estado.

## Extensão 0.3 capturada e avaliada offline — D-43

O pesquisador informou a conclusão da captura em `captura/extensao-real-0.3-001`, pelo plano 003. A conferência offline confirmou **64 resultados reais concluídos**, 32 Sol/medium e 32 Astra/medium, limite comum 4096, duas repetições por combinação, ordem/identidades e 1.312 vínculos de fechamento conformes. Referência candidata 0.3 confirmada pelo hash `94b6315b935d9817dd833567a0b107a90e88d9be850e93c747e03337450eebc9`. Coletor, planos, dados, notas, prompts e referência foram preservados; nenhuma chamada nova à API foi feita nesta avaliação.

Saída nova: [relatório descritivo](avaliados/extensao-real-0.3-001-avaliacao-001/RELATORIO.md), [tabelas por modelo/mudança/condição](avaliados/extensao-real-0.3-001-avaliacao-001/TABELAS.md), [64 avaliações](avaliados/extensao-real-0.3-001-avaliacao-001/lista.json). Formato válido 64/64; testes exatos 64/64. Requisitos exatos: Sol 28/32 e Astra 32/32. Quatro seleções de Sol/MC-02 excederam a referência com RF-02 e RF-03, sem omissões; nas demais mudanças e nos testes houve empate integral. Resultados locais descritivos, sem superioridade geral ou inferência estatística forte a partir de duas repetições.

**Conformidade: 64 pendentes, zero aprovadas.** [Modelo separado com hashes e decisões pendentes](avaliados/extensao-real-0.3-001-avaliacao-001/revisao-conformidade-pendente.json); responsável/data não preenchidos. O resumo controlado continua bloqueado, sem alterar conformidades para produzir a descrição. [Conferência de integridade](evidencias/spec004/avaliacao-extensao-0.3-D43/integridade.json) e [6.442 arquivos anteriores preservados](evidencias/spec004/avaliacao-extensao-0.3-D43/preservacao.json), sem pendência técnica detectada. Piloto e controles não entram nos denominadores.

Tokens reportados: Sol 56.384 entrada + 5.878 saída = 62.262; Astra 56.384 + 3.373 = 59.757. Raciocínio (4.439/1.693) já incluído na saída, sem somá-lo novamente. [Detalhes](avaliados/extensao-real-0.3-001-avaliacao-001/tokens-por-modelo.json). A captura ocorreu em 09/11/2026, 23:01:24–23:17:57, UTC−03:00, conforme registros originais.

## Histórico da integração de envio — D-42

O pesquisador autorizou a integração mínima do envio e declarou **USD 2 de orçamento de planejamento, sem controle automático ou garantia de teto**, aceitando esse risco. Implementado `extensao_exploratoria.py iniciar`, com `--enviar-real`, `--limite` obrigatório e `--continuar`; a coleta reutiliza o motor API e seleciona a configuração de cada observação. Registros reais usam fase `exploratoria` e identidade da extensão. A rota Codex CLI permanece intacta e bloqueada.

Plano vigente: [extensão 003](captura/extensao-20261109-003/plano.json), gerado pelo preparador a partir do 002, com os mesmos **64 itens, ordem literal e hashes de payload**, referência 0.3, Sol/medium e Astra/medium, limite comum 4096. Há novas identidades e hashes funcionais; planos anteriores preservados. **Nenhuma observação real foi executada nesta implementação**; todas permanecem planejadas. `envio_autorizado=true` identifica a habilitação técnica do novo plano; cada envio exige também a flag explícita.

[D-42](documentacao/decisoes.md), [relatório e comandos absolutos](evidencias/spec004/integracao-envio-extensao-2026-11-09-D42/RELATORIO.md), [verificação offline](evidencias/spec004/integracao-envio-extensao-2026-11-09-D42/verificacao-001/resultado.json). Captura, avaliação e revisão de conformidade permanecem separadas; USD 2 não é teto garantido. Nenhuma conexão, coleta, commit ou push foi feita nesta entrega.

Verificação D-42: **52 testes aprovados**, zero falhas/erros/ignorados, com rede bloqueada e HTTP/chave fictícios nos controles. 64 envios simulados com ambos os modelos, captura/retomada sem reenvio, avaliação separada e conformidade pendente; 8.543 arquivos anteriores conferidos sem divergências. Os 64 itens, ordem literal, payloads e referência foram preservados entre 002/003.

## Histórico da preparação offline — D-41

Autorizada somente preparação e verificação offline: catálogo **0.3, T01–T15**, referência candidata **0.3**, quatro mudanças × D0/D1/E0/E1 × GPT-6 Sol/medium e GPT-6 Astra/medium × duas repetições = **64 observações novas**, em dois blocos de 32. Nenhuma dessas observações foi executada. Limite proposto comum: **4096 tokens**, incluindo raciocínio e resposta final. Notas 0.2-local, pedidos e demais textos experimentais preservados; 16 textos de payload, idênticos entre os modelos, em 32 preparações com identidades próprias.

[Referência e justificativas 0.3](documentacao/referencia-candidata-0.3.md), [plano vigente](captura/extensao-20261109-002/plano.json), [ordem completa](captura/extensao-20261109-002/ordem.json), [relatório, custo e verificações](evidencias/spec004/extensao-2026-11-09/RELATORIO.md). A preparação `extensao-20261109-001` foi intermediária, anterior ao fechamento das fontes; seus hashes não autorizam execução. O coletor API foi reutilizado; a extensão possui trava de envio real no código. Os controles artificiais são identificados como sintéticos, separados da pesquisa.

Verificação final: **75/75 comparações conformes**; 127 métodos descobertos, 126 aprovados, zero falhas/erros e um ignorado condicional por privilégio Windows de symlink. [Evidência](evidencias/spec004/extensao-2026-11-09/verificacao-final/resultado.json), com conexões/DNS bloqueados. Estimativa informativa dos 64 envios: USD 2,73 no cenário de 1024 tokens de saída e USD 8,63–10,81 usando o limite 4096, conforme hipóteses de entrada; orçamento novo ainda não declarado e saldo não presumido.

## Piloto real encerrado pelo pesquisador e preservado

O pesquisador declarou concluída sua revisão do piloto de 16 observações no pedido de D-41. As **16 capturas reais e 16 avaliações individuais** continuam intactas, concluídas/avaliadas e com formato válido. Houve correspondência integral com a referência candidata 0.2, sem conclusão de superioridade, equivalência geral entre condições ou inutilidade das notas. D-39 registra a integração offline anterior. Nenhum registro antigo substitui observação da extensão, cujo catálogo foi ampliado.

| Artefato utilizado | Fonte preservada |
|---|---|
| Plano, ordem e configuração efetivos | [Plano API 002](captura/plano-api-piloto-002/plano.json), idêntico ao [plano copiado no lote](captura/piloto-api-001/plano-original.json) |
| Brutos, requisições, metadados e fechamentos | [captura/piloto-api-001](captura/piloto-api-001/) |
| Avaliações individuais e lista de hashes | [avaliados/piloto-api-001/lista.json](avaliados/piloto-api-001/lista.json) |
| Resumo já produzido | [resumo.json](avaliados/piloto-api-001/resumo/resumo.json): incompleto, com diagnósticos de conformidade pendente |
| Oito payloads únicos usados duas vezes | [Preparações do plano 002](captura/plano-api-piloto-002/preparados/); origem [v2-LF](evidencias/spec004/preparacao-piloto-2026-11-06-v2-lf/RELATORIO.md) |

Configuração registrada: **GPT-6 Sol (`gpt-6-sol`), esforço `medium`**, `piloto-api-74180c81329ee360`, Responses API, limite de saída 4096, timeout 120 s, orçamento declarado USD 1,00 (não é teto imposto pelo coletor). MC-01/MC-03 × D0/D1/E0/E1 × duas repetições, na ordem do plano, sem novo sorteio. O plano original ainda diz `PLANEJADA_NAO_EXECUTADA`: retrata a preparação; tentativas/fechamentos documentam a execução. Não corrigir esse original.

Os registros originais continuam com `conformidade_protocolo=pendente`, e o resumo existente conserva seu bloqueio histórico. A declaração atual de revisão concluída foi registrada em D-41, sem editar esses registros, fabricar decisões individuais ligadas a hashes ou completar aprovações retrospectivas. Os exemplos da integração são sintéticos. HTTP 200, formato válido e acertos não aprovam conformidade por si.

A [conexão neutra](captura/conexao-api-20261107-001/resultado.json) está concluída e reporta `gpt-6-sol`, na fase `verificacao_conexao`, excluída do piloto e da coleta principal. O [exploratório MC-04](evidencias/spec004/exploratorio-2026-11-05-mc04-001/) e controles sintéticos permanecem separados dos dados reais.

## Próximas tarefas e limites

1. Pesquisador revisar explicitamente a conformidade das 64 observações no mecanismo separado, com responsável, data, decisão e justificativa por observação ligadas aos hashes. O relatório lista o que conferir; HTTP 200, ausência de desvio detectado ou resposta correta não aprovam conformidade. Não excluir seleções incorretas apenas pelo escore.
2. Após revisão registrada, usar o resumo revisado existente para as observações elegíveis, conservando N=64, capturas, avaliações originais e exclusões. Até lá, usar somente as tabelas identificadas como descritivas com conformidade pendente.
3. Manter notas, prompts, referência candidata e critérios utilizados; não ajustá-los em função dos quatro excedentes. Nenhuma chamada nova, mudança de desenho, commit ou push está autorizada nesta avaliação. Notas incorretas continuam fora desta etapa e o piloto permanece separado.

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
