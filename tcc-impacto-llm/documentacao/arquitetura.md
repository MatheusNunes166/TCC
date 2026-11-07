# Arquitetura mínima proposta

Situação operacional: [estado atual](../ESTADO_ATUAL.md). Integração API D-39 e análise CLI D-38: [decisões](decisoes.md), com evidências e limites datados. [Operação API](operacao-api.md).

## Componentes e responsabilidades

| Componente | Responsabilidade |
|---|---|
| Política e núcleo de autorização local | Representar a baseline e produzir decisão/motivo para uma entrada, sem serviços externos. |
| Testes da bancada | Conferir os doze casos, precedência e variantes isoladas contra expectativas humanas revisadas. |
| Preparação de variantes | Aplicar uma mudança por vez à mesma baseline, preservando a versão inicial. |
| Montador de payload | Exportar somente blocos permitidos: definições, regras, catálogo da baseline, uma mudança, pedido e notas quando previstas. |
| Coletor `coletor_piloto.py` (D-37) | Adaptar `codex exec`, registrar ordem, preservar entrada/eventos/texto/erro e recuperar estado. Motor verificado com substituto local; envio real bloqueado pelos controles D-29 e de retentativa pendentes. |
| Coletor API e revisão de conformidade | `coletor_api.py` usa HTTPS direto, sem agente e com identidade própria; `revisao_conformidade.py` registra decisões separadas ligadas a hashes, sem editar capturas. |
| Avaliador local | Ler registros e referência separada; validar formato, extrair conjuntos e calcular métricas de RF e testes separadamente. |

Fluxo proposto: política → núcleo → testes; pacote permitido → montador → cliente LLM → registros; registros + referência separada → avaliador → tabelas.

## Separação da coleta e avaliação

O modelo recebe somente o texto do pacote permitido, sem gabarito, histórico, indexação do repositório ou ferramentas extras. Preparar conteúdo e avaliar são etapas separadas; somente o avaliador lê a referência e não a devolve ao contexto experimental. A interface entre coleta e avaliação são arquivos, sem conversa compartilhada. D-29 não exige uma identidade restrita para o processo local de preparação.

Uma pasta privada ou .gitignore não define o contexto do modelo. Pelo contrato D-29, o contexto experimental é somente o payload textual, sem ferramentas/anexos de ambiente; o avaliador lê a referência separadamente. A prova exigida é proveniência, inspeção e bytes preparados, e posteriormente correspondência na entrega real. Não se exige nem se alega isolamento por sistema operacional.

## Escolhas técnicas e pendências

- Confirmados pelo usuário para o incremento 1: Python + unittest e organização mínima em `autorizacao.py` e `tests/test_autorizacao.py`, sem dependências externas (D-07 em [decisoes.md](decisoes.md)). pytest permanece alternativa histórica não adotada.
- O [plano 001](../specs/001-autorizacao-direta/plan.md) detalha o desenho local parcial. Variantes estão implementadas; o contrato da Spec 004 define registros JSON para preparação e avaliação offline, sem alterar a persistência do núcleo.
- Configuração efetivamente utilizada: plano copiado no lote, localizado no [estado atual](../ESTADO_ATUAL.md). Não confundir controles sintéticos com escolhas de pesquisa.
- Uso uniforme de saída estruturada forçada e verificação futura da entrega textual sem ferramentas/anexos; identidade de SO deixou de ser exigida em D-29.
- A rota Codex histórica conserva sua trava: seus controles não demonstraram a fronteira D-29 nem controle das retentativas internas; [evidências D-38](../captura/analise-bloqueios-cli-2026-11-07-D38/RELATORIO.md). Não transferir esses limites automaticamente para outro cliente nem misturar lotes.
- Ferramentas e versões de desenvolvimento, inclusive Spec Kit, a confirmar antes de uso; sua utilização não escolhe o modelo avaliado.

As decisões devem ser registradas em [decisoes.md](decisoes.md) antes do incremento correspondente. Detalhes experimentais e falhas: [protocolo](../materiais/01_PROTOCOLO.md), [prompts](../materiais/04_NOTAS_E_PROMPTS.md) e [piloto/coleta](../materiais/05_PILOTO_E_COLETA.md).
