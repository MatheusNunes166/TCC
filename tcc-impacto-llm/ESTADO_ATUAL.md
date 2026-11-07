# Estado atual — 07/11/2026

## Integração API offline — D-39

Patch integrado à base `main`/`873f0a7285c4610335eda5c3a3d88ca2e13cdc8f`, inicialmente limpa e compatível com o diff. [Operação API](documentacao/operacao-api.md), [comandos/testes/hashes](captura/integracao-api-2026-11-07/verificacao.json). **Somente integração e verificações offline; nenhuma chamada real, consulta autenticada, conexão paga ou piloto.** Os relatos históricos do patch sobre disponibilidade da conta, outra conversa ou outro Word não foram adotados como evidência ou pendência nova.

- `coletor_api.py` usa configuração/ID próprios e preserva GPT-6 Sol/medium, os oito payloads v2-LF e as 16 posições da ordem D-38. Captura/avaliação seguem separadas; o código Codex e sua trava, montador, avaliador e referência permanecem inalterados.
- Transporte trata IncompleteRead/HTTPException, falhas de I/O e interrupções; preserva fragmentos, tipo e estado remoto desconhecido, sem gravar segredo ou reenviar automaticamente. TLS verificado, redirects recusados e sem proxies/retries herdados. Limite de saída deve ser escolhido para raciocínio+final; 512 dos testes não é escolha do piloto. Orçamento é declaração sem teto automático.
- `revisao_conformidade.py` registra responsável/data/justificativa/inclusão-exclusão com hashes. Avaliação pendente é descritiva; resumo controlado só após revisão explícita, preservando exclusões/dados/N planejado. Desvio registrado não é convertido em conforme por edição de captura.
- **52 testes offline aprovados**, incluindo os 13 originais e as regressões citadas no patch (12 coletor, 4 controles CLI, 7 avaliação real), mais 9 de transporte e 7 de revisão. Lote sintético de 16 capturado/continuado/avaliado; não são resultados de LLM.

Antes de qualquer chamada paga: obter autorização operacional distinta, escolher limite/configuração e orçamento/preço aceitáveis, conferir acesso real GPT-6 Sol/medium e as revisões de materiais/referência/política/medidas já pendentes. Não se executaram os comandos futuros de conexão ou envio. A autorização de integração não autoriza gasto. O estado D-38 abaixo continua descrevendo a rota Codex.

## Rota Codex — D-38 preservada
Comece aqui. Decisões e alcance: [D-38, D-37, D-36 e D-35](documentacao/decisoes.md). Coletor implementado e verificado offline; **envio real bloqueado**, nenhum piloto/chamada ao LLM/coleta principal ou congelamento realizado.

- Novo [coletor Python](coletor_piloto.py): conferência local, plano/ordem registrados, simulação, captura sequencial, pausa/continuação, recuperação conservadora e avaliação separada. [Comandos de operação](materiais/05_PILOTO_E_COLETA.md#511-coletor-offline-d-37-07112026).
- Configuração solicitada: **GPT-6 Sol / medium**, sem substituição por GPT-6.1 Sol. CLI `0.162.0-alpha.17.2`, autenticação ChatGPT ativa e medium no catálogo embutido; acesso remoto não testado. [Consultas locais](captura/conferencia-codex-2026-11-07/ambiente.json).
- [Plano offline D-38](captura/planejamento-piloto-2026-11-07-D38/plano.json): mesma ordem D-37 (semente original 20261106), 16 observações/oito payloads v2-LF únicos. Coletor v1.1-D38 acrescenta controles aceitos de skills/memórias/provider/auth e validação estrita; conserva a trava. Dezesseis testes afetados aprovados. [Análise dos dois bloqueios](captura/analise-bloqueios-cli-2026-11-07-D38/RELATORIO.md). O [plano D-37](captura/planejamento-piloto-2026-11-07/plano.json) e suas evidências permanecem preservados; o código novo o recusa por diferença de hash/configuração.

- Notas **0.2-local** simuladas pelo pesquisador com apoio de IA, posteriores ao exploratório conhecido; [texto integral e comparação](materiais/04_NOTAS_E_PROMPTS.md). Revisão própria declarada, sem revisor externo. Novo texto para conferência; nenhuma aprovação individual de todas as expectativas foi inferida.
- Referência **0.2 candidata**, quatro RFs, T01–T12, mudanças independentes e conjuntos 2/4/8/5 preservados. Baseline e variantes já implementadas/verificadas em D-20/D-21; [evidências 003](specs/003-mudancas-controladas/evidencias.md). Não reexecutadas nesta consolidação.
- Montagem offline vigente: **v2-LF, 16 pacotes** = quatro mudanças × D0/D1/E0/E1. UTF-8 sem BOM/LF antes dos hashes, fontes originais preservadas e regras Git específicas. [Relatório, pacotes e prova após quatro checkouts limpos](evidencias/spec004/preparacao-piloto-2026-11-06-v2-lf/RELATORIO.md). Conteúdo experimental D-35 preservado; a versão anterior é histórica por divergência de bytes após conversão CRLF/LF.
- Proposta do piloto: **16 chamadas** = MC-01/MC-03 × quatro condições × duas repetições. [Plano, tabela e configuração pendente](materiais/05_PILOTO_E_COLETA.md). São oito payloads únicos repetidos duas vezes; os outros oito pacotes não pertencem a esse piloto.
- Avaliação real offline preparada na CLI existente; originais, origem, fase, configuração e versões preservados. Inválidas têm medidas observadas nulas; vazias válidas e falhas técnicas continuam distintas. [Contrato e comandos](specs/004-preparacao-avaliacao-ids/contracts/preparacao-avaliacao.md).
- O estudo mede seleção de requisitos e testes existentes pelo LLM. Apoio a juniores é motivação, sem participantes juniores nem comprovação de melhoria de desempenho deles.

## Antes de qualquer chamada do piloto
O pesquisador ainda precisa conferir o novo texto e os payloads, registrar o alcance da revisão da referência/política/medidas e resolver divergências; confirmar disponibilidade remota de GPT-6 Sol/medium, parâmetros/limite e orçamento, e revisar a ordem já preparada. D-38 demonstra controles parciais, mas o render local mantém mensagens adicionais e não fornece inventário real de tools/instructions da rota exec. Na rota ChatGPT, o provedor embutido openai é reservado e rejeita os overrides de request_max_retries/stream_max_retries; aceitar zero em custom provider não prova seu efeito na coleta. Ambos os bloqueios permanecem pendentes. [Causas, evidências e alternativa mínima apenas proposta](captura/analise-bloqueios-cli-2026-11-07-D38/RELATORIO.md). Captura/retomada foram exercitadas somente com substituto artificial; nenhum exec/modelo foi iniciado nos diagnósticos. A trava permanece incondicional, inclusive com opção explícita. Aprovação operacional de início e adoção constitucional continuam pendentes, sem confundir esta última com revisão científica.

## Navegação
| Conteúdo | Local vigente |
|---|---|
| Regras de trabalho | [AGENTS](AGENTS.md), [constituição](.specify/memory/constitution.md) |
| Protocolo, condições e medidas | [material 01](materiais/01_PROTOCOLO.md) |
| Notas e prompts | [material 04](materiais/04_NOTAS_E_PROMPTS.md) |
| Referência privada e justificativas | [material 02](materiais/02_REQUISITOS_TESTES_E_REFERENCIA.md), [revisão detalhada](documentacao/referencia-candidata-proxima-etapa.md), [JSON candidato](materiais/modelos/referencia_candidata_NAO_ENVIAR_AO_LLM.json) |
| Plano do piloto e operação | [material 05](materiais/05_PILOTO_E_COLETA.md) |
| Núcleo, montagem, coleta e avaliação | [autorizacao.py](autorizacao.py), [fontes_autorizadas.py](fontes_autorizadas.py), [montagem_entradas.py](montagem_entradas.py), [coletor_piloto.py](coletor_piloto.py), [avaliacao_ids.py](avaliacao_ids.py) |
| Testes, variantes e verificador | [tests](tests/), [variantes](variantes/), [verificacao_variantes.py](verificacao_variantes.py) |
| Desenvolvimento e evidências | [specs](specs/), [evidencias](evidencias/); Spec 004 ativa |
| Índice dos materiais | [LEIA_PRIMEIRO](materiais/LEIA_PRIMEIRO.md) |

## Histórico e saídas locais
[Preparação D-35 anterior](evidencias/spec004/preparacao-piloto-2026-11-06/RELATORIO.md), manifestos/hashes e evidências permanecem integrais. Seus 16 payloads locais misturavam LF/CRLF; `core.autocrlf=true` converteu CRLF em LF nos blobs do commit `8920756d9a82daa244add102c299ed53f0655ad8`, invalidando os hashes publicados. O texto continuou equivalente. Não corrigir retrospectivamente esses registros nem usar seus hashes como prova de integridade da versão vigente. [Diagnóstico por payload](evidencias/spec004/preparacao-piloto-2026-11-06-v2-lf/diagnostico-anterior.json).

[Exploratório MC-04](evidencias/spec004/exploratorio-2026-11-05-mc04-001/recuperacao-sessoes-001/RELATORIO.md) permanece exploratório, com desvios de contexto/ferramentas e bloqueio do resumo controlado D0; não entra no piloto/principal. Resultados conhecidos não orientaram ajustes por pontuação.

[Históricos documentais](documentacao/historico/) e [originais desta consolidação](documentacao/historico/pre-piloto-2026-11-06/LEIA_PRIMEIRO.md) preservam versões anteriores. O [pacote profissional 1.0](documentacao/revisao-profissional-spec004-v1/LEIA-PRIMEIRO.md) é histórico da proposta de revisão externa, sem parecer recebido; não é o próximo passo vigente. DOCX/figuras anteriores em materiais também são históricos. Diretórios de temporários dentro de evidências são registros preservados, não lixo a excluir. Apenas futuras saídas em `saidas-locais/` são regeneráveis e ignoradas pelo Git.
