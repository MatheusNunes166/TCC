# Pacote para revisão profissional — Spec 004

Versão 1.0 • 01/11/2026 • **PREPARADO PARA REVISÃO; parecer ainda não recebido**.

Destinatário pretendido: profissional com experiência pertinente em testes de software, a identificar. Organização deste pacote: assistente de IA, por solicitação do pesquisador. Nenhuma autoria profissional, concordância ou aprovação é presumida.

## Ordem sugerida

1. Ler [Parte 1 — Contexto e notas](01-contexto-e-notas.md) e preencher a seção A da [ficha](03-ficha-de-revisao.md), **antes de abrir a Parte 2 ou os links para conjuntos candidatos**. Registrar data/hora e comentários iniciais. Se já conhece a referência, declarar essa exposição.
2. Somente depois consultar [Parte 2 — Referência candidata](02-referencia-candidata.md), completar a seção B e registrar se essa consulta alterou o comentário inicial, preservando as duas versões.
3. Devolver a ficha e eventuais sugestões identificadas por item. O pesquisador preencherá posteriormente a resolução; propostas não atualizam automaticamente as fontes.

Se possível, o pesquisador fornece primeiro somente Parte 1 e ficha, e disponibiliza a Parte 2 depois. Essa ordem reduz a influência dos conjuntos de respostas sobre a revisão das notas; não garante revisão cega, pois o contexto já permite deduções. Nenhum envio ao profissional foi realizado por este assistente.

## O que está sendo revisado

A utilidade/neutralidade das notas e a coerência da referência candidata de seleção de requisitos impactados e testes existentes de uma bancada fictícia. As partes contêm o necessário para opinar sem executar código ou navegar pelo repositório; links são aprofundamento opcional. Não há logs extensos.

Este **pacote humano contém respostas candidatas e justificativas**. Não é pacote para o LLM e não integra a lista de arquivos autorizados de `fontes_autorizadas.py`. O modelo experimental receberá apenas texto autorizado, sem ferramentas/acesso ao repositório. Nenhum piloto ou chamada ao LLM foi executado para preparar esta revisão.

## Versões e estado

| Item | Versão/estado examinado nesta compilação |
|---|---|
| Este pacote | 1.0, 01/11/2026; compilação documental nova, não parecer |
| Referência de seleção | Candidata 0.2, `CANDIDATO_NAO_REVISADO`; revisor/data nulos |
| Notas | Bloco único de materiais/04 §4.2, rascunho; conteúdo reproduzido sem alteração |
| Baseline B | `aec474bcb54d6dae2afceff8e5b9226991386490`; T01–T12 |
| Mudanças | MC-01, MC-02, MC-03 e MC-04-v2; independentes sobre B |
| Preparação Spec 004 | Contrato `spec004-v3`, D-29/D-30; engenharia offline verificada |
| Política do avaliador | `ids-proposta-004-v2`, convenções técnicas candidatas; revisão científica pendente |

[Versões e SHA-256 das fontes](versoes.json) fixam os bytes consultados, inclusive a nota literal. HEAD de contexto na preparação: `c94fc54add907ba6aaa50d483d63fed40c6a3dd5`; havia alterações locais da Spec 004. HEAD não identifica sozinho esses arquivos nem substitui seus hashes.

## Detalhes opcionais e limites

[Fechamento técnico Spec 004](../../evidencias/spec004/revisao-textual-2026-11-01/relatorio.md), [evidências Spec 003](../../specs/003-mudancas-controladas/evidencias.md) e [decisões](../decisoes.md). Na cópia avulsa/ZIP, esses links externos ao pacote podem depender do repositório; a leitura das partes e da ficha é autossuficiente.

A bancada foi conferida contra a candidata; isso não aprova cientificamente a referência. Revisão profissional, conteúdo definitivo das notas, fundamentação das métricas, desenho final do piloto e entrega real ao modelo continuam pendentes. Precisão, revocação, F1 e consistência permanecem propostas; este pacote não pede aprovação automática dessas medidas nem fecha a pesquisa.
