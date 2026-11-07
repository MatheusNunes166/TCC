# Estado atual — 06/11/2026
Comece aqui. Decisões e alcance: [D-36 e D-35](documentacao/decisoes.md). A correção D-36 trata somente da preservação dos arquivos; não iniciou piloto, chamadas externas ou coleta principal e não congelou a coleta.

- Notas **0.2-local** simuladas pelo pesquisador com apoio de IA, posteriores ao exploratório conhecido; [texto integral e comparação](materiais/04_NOTAS_E_PROMPTS.md). Revisão própria declarada, sem revisor externo. Novo texto para conferência; nenhuma aprovação individual de todas as expectativas foi inferida.
- Referência **0.2 candidata**, quatro RFs, T01–T12, mudanças independentes e conjuntos 2/4/8/5 preservados. Baseline e variantes já implementadas/verificadas em D-20/D-21; [evidências 003](specs/003-mudancas-controladas/evidencias.md). Não reexecutadas nesta consolidação.
- Montagem offline vigente: **v2-LF, 16 pacotes** = quatro mudanças × D0/D1/E0/E1. UTF-8 sem BOM/LF antes dos hashes, fontes originais preservadas e regras Git específicas. [Relatório, pacotes e prova após quatro checkouts limpos](evidencias/spec004/preparacao-piloto-2026-11-06-v2-lf/RELATORIO.md). Conteúdo experimental D-35 preservado; a versão anterior é histórica por divergência de bytes após conversão CRLF/LF.
- Proposta do piloto: **16 chamadas** = MC-01/MC-03 × quatro condições × duas repetições. [Plano, tabela e configuração pendente](materiais/05_PILOTO_E_COLETA.md). São oito payloads únicos repetidos duas vezes; os outros oito pacotes não pertencem a esse piloto.
- Avaliação real offline preparada na CLI existente; originais, origem, fase, configuração e versões preservados. Inválidas têm medidas observadas nulas; vazias válidas e falhas técnicas continuam distintas. [Contrato e comandos](specs/004-preparacao-avaliacao-ids/contracts/preparacao-avaliacao.md).
- O estudo mede seleção de requisitos e testes existentes pelo LLM. Apoio a juniores é motivação, sem participantes juniores nem comprovação de melhoria de desempenho deles.

## Antes de qualquer chamada do piloto
O pesquisador ainda precisa conferir o novo texto e os payloads, registrar o alcance da revisão da referência/política/medidas e resolver divergências; definir modelo/modalidade/configuração suportada/orçamento e ordem; demonstrar conversa nova com mensagem completa, ferramentas desativadas e sem acesso ao projeto; preparar captura dos originais e dos desvios. Aprovação operacional de início não foi registrada. Adoção constitucional continua pendente, sem confundir essa pendência com revisão científica.

## Navegação
| Conteúdo | Local vigente |
|---|---|
| Regras de trabalho | [AGENTS](AGENTS.md), [constituição](.specify/memory/constitution.md) |
| Protocolo, condições e medidas | [material 01](materiais/01_PROTOCOLO.md) |
| Notas e prompts | [material 04](materiais/04_NOTAS_E_PROMPTS.md) |
| Referência privada e justificativas | [material 02](materiais/02_REQUISITOS_TESTES_E_REFERENCIA.md), [revisão detalhada](documentacao/referencia-candidata-proxima-etapa.md), [JSON candidato](materiais/modelos/referencia_candidata_NAO_ENVIAR_AO_LLM.json) |
| Plano do piloto e operação | [material 05](materiais/05_PILOTO_E_COLETA.md) |
| Núcleo, montagem e avaliação | [autorizacao.py](autorizacao.py), [fontes_autorizadas.py](fontes_autorizadas.py), [montagem_entradas.py](montagem_entradas.py), [avaliacao_ids.py](avaliacao_ids.py) |
| Testes, variantes e verificador | [tests](tests/), [variantes](variantes/), [verificacao_variantes.py](verificacao_variantes.py) |
| Desenvolvimento e evidências | [specs](specs/), [evidencias](evidencias/); Spec 004 ativa |
| Índice dos materiais | [LEIA_PRIMEIRO](materiais/LEIA_PRIMEIRO.md) |

## Histórico e saídas locais
[Preparação D-35 anterior](evidencias/spec004/preparacao-piloto-2026-11-06/RELATORIO.md), manifestos/hashes e evidências permanecem integrais. Seus 16 payloads locais misturavam LF/CRLF; `core.autocrlf=true` converteu CRLF em LF nos blobs do commit `8920756d9a82daa244add102c299ed53f0655ad8`, invalidando os hashes publicados. O texto continuou equivalente. Não corrigir retrospectivamente esses registros nem usar seus hashes como prova de integridade da versão vigente. [Diagnóstico por payload](evidencias/spec004/preparacao-piloto-2026-11-06-v2-lf/diagnostico-anterior.json).

[Exploratório MC-04](evidencias/spec004/exploratorio-2026-11-05-mc04-001/recuperacao-sessoes-001/RELATORIO.md) permanece exploratório, com desvios de contexto/ferramentas e bloqueio do resumo controlado D0; não entra no piloto/principal. Resultados conhecidos não orientaram ajustes por pontuação.

[Históricos documentais](documentacao/historico/) e [originais desta consolidação](documentacao/historico/pre-piloto-2026-11-06/LEIA_PRIMEIRO.md) preservam versões anteriores. O [pacote profissional 1.0](documentacao/revisao-profissional-spec004-v1/LEIA-PRIMEIRO.md) é histórico da proposta de revisão externa, sem parecer recebido; não é o próximo passo vigente. DOCX/figuras anteriores em materiais também são históricos. Diretórios de temporários dentro de evidências são registros preservados, não lixo a excluir. Apenas futuras saídas em `saidas-locais/` são regeneráveis e ignoradas pelo Git.
