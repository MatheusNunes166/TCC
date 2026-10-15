# Arquitetura mínima proposta

Estado: desenho documental; componentes e tecnologias não implementados. Limites em [contexto-e-escopo.md](contexto-e-escopo.md), contrato em [requisitos.md](requisitos.md).

## Componentes e responsabilidades

| Componente futuro | Responsabilidade |
|---|---|
| Política e núcleo de autorização local | Representar a baseline e produzir decisão/motivo para uma entrada, sem serviços externos. |
| Testes da bancada | Conferir os onze casos, precedência e variantes isoladas contra expectativas humanas revisadas. |
| Preparação de variantes | Aplicar uma mudança por vez à mesma baseline, preservando a versão inicial. |
| Montador de payload | Exportar somente blocos permitidos: definições, regras, catálogo da baseline, uma mudança, pedido e notas quando previstas. |
| Cliente e registrador da coleta | Fazer chamadas independentes e preservar payload, resposta/erro, configuração, versões e ordem. |
| Avaliador local | Ler registros e referência separada; validar formato, extrair conjuntos e calcular métricas de RF e testes separadamente. |

Fluxo proposto: política → núcleo → testes; pacote permitido → montador → cliente LLM → registros; registros + referência separada → avaliador → tabelas.

## Separação da coleta e avaliação

O processo que consulta o modelo deve ter acesso somente ao pacote permitido, sem gabarito, histórico, indexação do repositório ou ferramentas extras. O avaliador acessa a referência separadamente e não a devolve ao contexto experimental. A interface entre coleta e avaliação são arquivos, sem conversa compartilhada.

Uma pasta chamada privada ou um `.gitignore` não impõe isolamento. A separação física/de acesso e a inspeção do payload precisam de evidência antes do piloto. Esta pasta documental contém expectativas e não constitui pacote experimental permitido.

## Escolhas técnicas e pendências

- Confirmados pelo usuário para o incremento 1: Python + unittest e organização mínima em `autorizacao.py` e `tests/test_autorizacao.py`, sem dependências externas (D-07 em [decisoes.md](decisoes.md)). pytest permanece alternativa histórica não adotada.
- O [plano 001](../specs/001-autorizacao-direta/plan.md) detalha o desenho local parcial. Representação de variantes e formatos dos futuros registros experimentais continuam pendentes; JSON é proposta para esses registros, não requisito de persistência do núcleo.
- Provedor, modelo/versão, modalidade de API, parâmetros suportados, limite de saída e orçamento.
- Uso uniforme de saída estruturada forçada, tratamento operacional de acesso e mecanismo de isolamento.
- Ferramentas e versões de desenvolvimento, inclusive Spec Kit, a confirmar antes de uso; sua utilização não escolhe o modelo avaliado.

As decisões devem ser registradas em [decisoes.md](decisoes.md) antes do incremento correspondente. Detalhes experimentais e falhas: [protocolo](../materiais/01_PROTOCOLO.md), [prompts](../materiais/04_NOTAS_E_PROMPTS.md) e [piloto/coleta](../materiais/05_PILOTO_E_COLETA.md).

