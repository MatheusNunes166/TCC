# Impacto de mudanças com LLM

Pesquisa sobre seleção de IDs de requisitos impactados e testes relevantes em uma bancada de permissões. Compara D0/D1/E0/E1, com e sem notas simuladas de analista, em mudanças independentes. Captura e avaliação são separadas; referência e justificativas são exclusivas do avaliador.

**Comece pelo [estado atual e próximas tarefas](ESTADO_ATUAL.md).** Ele centraliza a situação do piloto e as pendências. A integração D-42 disponibiliza envio explícito da extensão; nenhuma chamada foi realizada na implementação.

D-43: a captura real da extensão terminou e foi avaliada offline. [Relatório descritivo e comandos](avaliados/extensao-real-0.3-001-avaliacao-001/RELATORIO.md), [tabelas por modelo/mudança/condição](avaliados/extensao-real-0.3-001-avaliacao-001/TABELAS.md) e [revisão de conformidade pendente](avaliados/extensao-real-0.3-001-avaliacao-001/revisao-conformidade-pendente.json). São 64 respostas válidas; testes exatos 64/64; requisitos Sol 28/32 e Astra 32/32, com quatro excedentes em Sol/MC-02. Nenhuma conformidade foi aprovada automaticamente; o resumo controlado permanece bloqueado.

Preparação offline D-41: [catálogo e referência candidata 0.3](documentacao/referencia-candidata-0.3.md), [plano de 64 observações](captura/extensao-20261109-002/plano.json) e [verificação offline, comandos e custo](evidencias/spec004/extensao-2026-11-09/RELATORIO.md). O catálogo 0.2 e os dados do piloto abaixo são preservados como versão anterior; a revisão do piloto foi declarada concluída pelo pesquisador. Essa entrega antecede a captura real descrita em D-43.

D-42 integra o envio real mediante flag explícita, sem executar chamadas nesta implementação. Plano operacional vigente: [extensão 003](captura/extensao-20261109-003/plano.json), com mesmos textos e ordem do 002 e orçamento de planejamento USD 2, sem garantia de teto. [Relatório e comandos absolutos](evidencias/spec004/integracao-envio-extensao-2026-11-09-D42/RELATORIO.md).

| Procurar | Caminho |
|---|---|
| Objetivo, escopo e desenho | [Contexto](documentacao/contexto-e-escopo.md), [protocolo](materiais/01_PROTOCOLO.md), [piloto/coleta](materiais/05_PILOTO_E_COLETA.md) |
| Requisitos, arquitetura, mudanças e testes | [Requisitos](documentacao/requisitos.md), [arquitetura](documentacao/arquitetura.md), [catálogo T01–T12](documentacao/qualidade-e-testes.md), [Specs](specs/), [variantes](variantes/) |
| Notas e prompts utilizados | [Notas 0.2-local e prompts](materiais/04_NOTAS_E_PROMPTS.md), [definições comuns](materiais/07_DEFINICOES_COMUNS.md) |
| Payloads e ordem utilizados no piloto | [Plano API 002](captura/plano-api-piloto-002/plano.json), [oito preparações](captura/plano-api-piloto-002/preparados/), [origem v2-LF e prova de bytes](evidencias/spec004/preparacao-piloto-2026-11-06-v2-lf/RELATORIO.md) |
| Referência e justificativas — **não enviar ao LLM** | [Material privado](materiais/02_REQUISITOS_TESTES_E_REFERENCIA.md), [referência JSON](materiais/modelos/referencia_candidata_NAO_ENVIAR_AO_LLM.json), [rastreabilidade](documentacao/referencia-candidata-proxima-etapa.md) |
| Código e testes offline | Módulos Python na raiz; [testes e fixtures](tests/); [verificação de variantes](verificacao_variantes.py) |
| Operação do coletor e avaliador | [Rota API, transporte e revisão de conformidade](documentacao/operacao-api.md), [contrato de preparação/avaliação](specs/004-preparacao-avaliacao-ids/contracts/preparacao-avaliacao.md) |
| Dados e resultados do piloto | [Capturas originais](captura/piloto-api-001/), [avaliações individuais](avaliados/piloto-api-001/lista.json), [resumo existente e seus diagnósticos](avaliados/piloto-api-001/resumo/resumo.json) |
| Conexão neutra e exploratório — separados do piloto | [Conexão API](captura/conexao-api-20261107-001/), [exploratório MC-04](evidencias/spec004/exploratorio-2026-11-05-mc04-001/) |
| Decisões, governança e histórico | [Decisões datadas](documentacao/decisoes.md), [AGENTS](AGENTS.md), [constituição](.specify/memory/constitution.md), [histórico documental](documentacao/historico/), [roadmap](documentacao/roadmap.md) |

`captura/` conserva também planos anteriores, a rota Codex bloqueada e controles técnicos. `avaliados/` distingue os controles sintéticos do piloto real. `evidencias/` conserva versões, ferramentas, falhas e provas de reprodução; as cópias com caminhos/hashes próprios não são duplicatas descartáveis. [Classificação e critérios de conservação](ESTADO_ATUAL.md#conservação-do-repositório).
