# Consolidação offline para o piloto — 06/11/2026

Responsabilidade das decisões: pesquisador, D-35. Execução técnica: assistente de IA. Git inicialmente limpo, branch main, HEAD `310c9f28f4267bc6e052f6b93910400cd0e31bc2`. Estado e navegação central: [ESTADO_ATUAL](../../../ESTADO_ATUAL.md). Nenhuma chamada externa, piloto, coleta principal ou commit/push nesta etapa.

## Entrega e decisões
Notas/prompts **0.2-local**, autoria do pesquisador com apoio de IA, inspiradas em heurísticas de analista experiente; sem coleta de conhecimento tácito real. Revisão própria declarada, sem revisor externo nesta etapa, sem aprovação atribuída a orientador/profissional ou inferida para todas as expectativas. Novo texto para conferência do pesquisador. [D-35](../../../documentacao/decisoes.md) e [notas integrais/comparação](../../../materiais/04_NOTAS_E_PROMPTS.md).

A busca por nomes e conteúdo no workspace não localizou uma reformulação anterior das notas v0.2. A candidata 0.2 encontrada é a referência. Esta consolidação local é posterior ao exploratório conhecido D-34; não houve nova chamada, iteração por pontuação ou busca de vantagem. A exposição anterior e a maior extensão das notas são limitações metodológicas registradas.

O estudo avalia seleção de requisitos impactados e testes existentes pelo LLM. Apoio a juniores é motivação, sem participantes juniores ou medida de melhora deles. Inválidas conservam medidas observadas nulas; vazias válidas e falhas técnicas continuam distintas. Imputação opcional permanece separada, identificada e sem substituir observações.

## Pacotes e condições
Gerados **16 pacotes**: quatro mudanças × D0/D1/E0/E1. Índice de recortes: [indice.json](artefatos/recortes/indice.json). Payloads completos abaixo; todos preparados localmente, não enviados.

| Mudança | D0: direto | D1: direto + notas | E0: etapas | E1: etapas + notas |
|---|---|---|---|---|
| MC-01 | [D0](artefatos/preparados/MC-01-D0/payload.txt) | [D1](artefatos/preparados/MC-01-D1/payload.txt) | [E0](artefatos/preparados/MC-01-E0/payload.txt) | [E1](artefatos/preparados/MC-01-E1/payload.txt) |
| MC-02 | [D0](artefatos/preparados/MC-02-D0/payload.txt) | [D1](artefatos/preparados/MC-02-D1/payload.txt) | [E0](artefatos/preparados/MC-02-E0/payload.txt) | [E1](artefatos/preparados/MC-02-E1/payload.txt) |
| MC-03 | [D0](artefatos/preparados/MC-03-D0/payload.txt) | [D1](artefatos/preparados/MC-03-D1/payload.txt) | [E0](artefatos/preparados/MC-03-E0/payload.txt) | [E1](artefatos/preparados/MC-03-E1/payload.txt) |
| MC-04-v2 | [D0](artefatos/preparados/MC-04-v2-D0/payload.txt) | [D1](artefatos/preparados/MC-04-v2-D1/payload.txt) | [E0](artefatos/preparados/MC-04-v2-E0/payload.txt) | [E1](artefatos/preparados/MC-04-v2-E1/payload.txt) |

D0/D1 conservam o mesmo pedido direto; E0/E1, o mesmo pedido estruturado. As oito ocorrências de notas são idênticas; D0/E0 não contêm bloco/arquivo de notas. Sistema, definições, requisitos, catálogo e schema são iguais nas 16 preparações; a mudança é igual nas quatro condições do respectivo caso. Requisitos/definições/schema e entradas/saídas do catálogo mantêm o conteúdo factual anterior. A mensagem comum de sistema explicita os limites da tarefa. O formato final continua objeto JSON com listas `requisitos` e `testes`.

Os recortes incluem apenas os sete documentos permitidos, mais notas quando cabíveis. Catálogo exporta seis colunas da baseline, sem vínculos de RF como pistas; mudança exporta só a descrição; notas/pedidos são blocos literais. Conferência de recortes/bytes e controles de exclusão não encontraram gabarito, código, resultados de variantes ou histórico no payload. Não se alega detector semântico universal de vazamento.

## Referência preservada
Conferência documental das 12 entradas/saídas de baseline e 48 expectativas, comparando catálogo, material 02, justificativas detalhadas e JSON candidato. Sem divergência substantiva encontrada; nenhuma expectativa, conjunto candidato ou aprovação do JSON foi alterada. A observação histórica dentro do JSON sobre variantes não executadas foi preservada literalmente e contextualizada no documento de referência: execução técnica posterior está em D-20/D-21.

| Mudança | RFs candidatos | Testes de mudança | Testes de preservação |
|---|---|---|---|
| MC-01 | RF-02 | T04 | T12 |
| MC-02 | RF-04 | T06, T07, T12 | T11 |
| MC-03 | RF-02, RF-03 | T02, T05 | T01, T06, T07, T09, T10, T11 |
| MC-04-v2 | RF-03, RF-04 | T05, T07, T12 | T08, T10 |

T07 em MC-04-v2 muda o motivo, mantendo a decisão; portanto é mudança observável. A conferência técnica não aprova cientificamente cada expectativa. Baseline, variantes, testes da bancada, referência JSON, manifesto principal, pacote profissional e evidências anteriores permanecem sem diff. Nenhuma nova rodada da bancada 003 foi necessária.

## Avaliação real e piloto proposto
A CLI existente reutiliza o comparador e aceita explicitamente `--origem real --fase exploratoria|piloto|principal`. Preserva resposta original, entrada efetiva, origem/sessão/turno, identidade, repetição, configuração, versões e hashes. Requisitos e testes separados. Modo sintético permanece separado; mistura de origem/fase/versões, duplicidades e desvios impedem resumo controlado. Fórmulas, parser e comparador foram conferidos por AST contra HEAD: inalterados. [Contrato/comandos](../../../specs/004-preparacao-avaliacao-ids/contracts/preparacao-avaliacao.md).

Caminhos de CLI com componente pai legítimo eram recusados pelo teste de nomes terminados em ponto; passam a ser resolvidos e verificados. Caminhos declarados nos JSONs continuam sem traversal e sem links/reparse. O teste do fluxo real chama a CLI por caminho absoluto a partir de outro diretório Windows, cobrindo a falha de contexto de importação encontrada no procedimento exploratório anterior, sem migrar a plataforma.

O [plano do piloto](../../../materiais/05_PILOTO_E_COLETA.md) mantém **MC-01/MC-03 × quatro condições × duas repetições = 16 chamadas propostas**, oito payloads únicos. [Tabela/configuração](../../../materiais/modelos/plano_piloto.json) permanece não executada, com ordem e campos indisponíveis nulos. Ordenador local exige semente explícita; sementes 17/18 foram apenas controles artificiais, sem escolher a do piloto. A opção `--configuracao-id` permite gerar nova preparação após a decisão real, sem copiar automaticamente configuração exploratória. Coleta principal não congelada.

## Verificações e resultados
Ambiente efetivo: Windows/PowerShell, Python 3.13.3, biblioteca padrão, sem rede.

| Verificação | Resultado | Registro |
|---|---|---|
| Avaliador existente e importação real simulada | 21 métodos aprovados | [log](avaliacao-stderr.txt) |
| Recortes/fontes | 4 aprovados; repetidos somente após acrescentar configuração explícita | [final](fontes-configuracao-stderr.txt), [anterior](fontes-stderr.txt) |
| Montagem/caminhos | 7 aprovados, 1 ignorado por WinError1314 ao criar symlink real | [log](montagem-stderr.txt) |
| Montagem e conferência documental | 16 pacotes, 12 baseline, 48 expectativas; zero divergências | [resultado](artefatos/verificacao.json), [script repetível](verificar_preparacao.py) |
| Preservação, versões/fontes finais e comparador | hashes dos 20 originais históricos e fontes atuais conferidos; AST preservada | [fechamento](fechamento.json) |
| Ordem proposta | 16 posições únicas; blocos completos; repetibilidade com mesma semente | controles no script documental; plano original continua sem ordem |
| Diff | `git diff --check` sem erros | retorno em fechamento.json |

**32 métodos únicos aprovados e 1 ignorado**; a repetição dos quatro métodos de fontes não aumenta a contagem. Os controles de importação usam metadados artificiais para exercitar o ramo real em diretórios temporários; não são respostas de LLM e não entram no piloto. Nenhuma resposta real foi reimportada ou reavaliada nesta etapa. [Comandos e retornos](verificacoes-testes.json).

Não houve tentativa de elevar privilégios para criar symlinks. O teste ignorado não é aprovado. Testes offline não comprovam entrega real do payload nem indisponibilidade de ferramentas na plataforma. Desvios do exploratório anterior continuam registrados e seus dados separados. A CLI resume médias, contagens e Jaccard por célula; mediana/amplitude e análise interpretativa posterior previstas no protocolo não são automatizadas por esta alteração.

## Organização e arquivos
Estado central em ESTADO_ATUAL.md; HANDOFF e BLOQUEIOS remetem a ele. Índice de materiais atualizado; arquivos datados antigos foram copiados literalmente para [histórico](../../../documentacao/historico/pre-piloto-2026-11-06/LEIA_PRIMEIRO.md), sem mover evidências/snapshots existentes. Não foi criado outro README duplicando o estado. Código e módulos não foram renomeados. `.gitignore` apenas acrescenta `/saidas-locais/` para futuras saídas regeneráveis; nada versionado foi removido.

Fontes modificadas ou criadas (hashes em fechamento.json), além dos históricos e artefatos desta evidência:

- [.gitignore](../../../.gitignore)
- [AGENTS.md](../../../AGENTS.md)
- [BLOQUEIOS.md](../../../BLOQUEIOS.md)
- [ESTADO_ATUAL.md](../../../ESTADO_ATUAL.md)
- [HANDOFF.md](../../../HANDOFF.md)
- [avaliacao_ids.py](../../../avaliacao_ids.py)
- [documentacao/arquitetura.md](../../../documentacao/arquitetura.md)
- [documentacao/contexto-e-escopo.md](../../../documentacao/contexto-e-escopo.md)
- [documentacao/decisoes.md](../../../documentacao/decisoes.md)
- [documentacao/qualidade-e-testes.md](../../../documentacao/qualidade-e-testes.md)
- [documentacao/referencia-candidata-proxima-etapa.md](../../../documentacao/referencia-candidata-proxima-etapa.md)
- [documentacao/roadmap.md](../../../documentacao/roadmap.md)
- [fontes_autorizadas.py](../../../fontes_autorizadas.py)
- [materiais/01_PROTOCOLO.md](../../../materiais/01_PROTOCOLO.md)
- [materiais/02_REQUISITOS_TESTES_E_REFERENCIA.md](../../../materiais/02_REQUISITOS_TESTES_E_REFERENCIA.md)
- [materiais/04_NOTAS_E_PROMPTS.md](../../../materiais/04_NOTAS_E_PROMPTS.md)
- [materiais/05_PILOTO_E_COLETA.md](../../../materiais/05_PILOTO_E_COLETA.md)
- [materiais/LEIA_PRIMEIRO.md](../../../materiais/LEIA_PRIMEIRO.md)
- [materiais/modelos/registro_execucao.json](../../../materiais/modelos/registro_execucao.json)
- [montagem_entradas.py](../../../montagem_entradas.py)
- [specs/004-preparacao-avaliacao-ids/contracts/preparacao-avaliacao.md](../../../specs/004-preparacao-avaliacao-ids/contracts/preparacao-avaliacao.md)
- [specs/004-preparacao-avaliacao-ids/data-model.md](../../../specs/004-preparacao-avaliacao-ids/data-model.md)
- [specs/004-preparacao-avaliacao-ids/plan.md](../../../specs/004-preparacao-avaliacao-ids/plan.md)
- [specs/004-preparacao-avaliacao-ids/quickstart.md](../../../specs/004-preparacao-avaliacao-ids/quickstart.md)
- [specs/004-preparacao-avaliacao-ids/spec.md](../../../specs/004-preparacao-avaliacao-ids/spec.md)
- [materiais/modelos/ordenar_piloto.py](../../../materiais/modelos/ordenar_piloto.py)
- [materiais/modelos/plano_piloto.json](../../../materiais/modelos/plano_piloto.json)
- [tests/test_avaliacao_real.py](../../../tests/test_avaliacao_real.py)
- [evidencias/spec004/preparacao-piloto-2026-11-06/verificar_preparacao.py](../../../evidencias/spec004/preparacao-piloto-2026-11-06/verificar_preparacao.py)
- [tests/test_fontes_autorizadas.py](../../../tests/test_fontes_autorizadas.py)

## Conferências antes das chamadas
O pesquisador precisa conferir o novo texto/payloads e registrar o alcance da revisão da referência/política/medidas; decidir configuração suportada, modalidade, orçamento e ordem; verificar conversa nova com conteúdo completo na primeira mensagem, sem ferramentas/acesso ao projeto; preparar captura de originais e desvios e autorizar o início do piloto. Não atribuir aprovação externa nem individualizar retroativamente expectativas não examinadas.
