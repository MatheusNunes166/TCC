# Orientações para agentes

O [README](README.md) orienta a navegação; o [estado atual](ESTADO_ATUAL.md) é a fonte da situação operacional. Autorizações e seus limites estão em [decisões](documentacao/decisoes.md). Siga o pedido atual do usuário; organização/limpeza não autoriza chamadas externas, nova coleta, commit ou push.

## Ordem de leitura

1. Este arquivo e [.specify/memory/constitution.md](.specify/memory/constitution.md).
2. [ESTADO_ATUAL.md](ESTADO_ATUAL.md); [BLOQUEIOS.md](BLOQUEIOS.md) e [HANDOFF.md](HANDOFF.md) apenas encaminham à mesma fonte.
3. Em `documentacao/`: [contexto-e-escopo.md](documentacao/contexto-e-escopo.md), [decisoes.md](documentacao/decisoes.md), [requisitos.md](documentacao/requisitos.md), [arquitetura.md](documentacao/arquitetura.md), [qualidade-e-testes.md](documentacao/qualidade-e-testes.md), [roadmap.md](documentacao/roadmap.md).
4. [materiais/LEIA_PRIMEIRO.md](materiais/LEIA_PRIMEIRO.md) e fontes pertinentes indicadas nele.

## Fontes e decisões

Preserve materiais. A documentação sintetiza a baseline; os materiais sustentam sua origem. Siga instruções atuais do usuário no escopo autorizado. Diante de divergência, registre fontes, impacto e proposta de resolução em `documentacao/decisoes.md`; não escolha silenciosamente uma versão nem promova histórico a regra vigente. Solicite decisão apenas quando a divergência impedir o trabalho corrente e continue tarefas independentes.

Considere confirmada somente decisão com responsável, data e evidência registrados. Autorização de engenharia não equivale à aprovação científica do orientador. Propostas e expectativas permanecem candidatas até revisão registrada.

## Trabalho e fechamento

Desenvolva uma capacidade por vez, conforme roadmap e constituição. Antes de fechar incrementos, revise alterações e confronte critérios com evidências reais, registrando lacunas. Não declare testes executados, capacidades prontas ou pesquisa concluída sem evidência. Atualize documentação afetada, estado, bloqueios e handoff. Centralize decisões em `documentacao/decisoes.md` e use referências.

## Desenvolvimento e experimento

O contexto do assistente de desenvolvimento não é o pacote do LLM avaliado. Não envie estes arquivos ou materiais inteiros ao experimento: contêm expectativas e referência candidata. Siga a separação de coleta/avaliação de `documentacao/arquitetura.md`. Documentação pronta não libera piloto.


Preserve bytes, caminhos, versões e hashes dos registros utilizados, inclusive arquivos ignorados que sustentem reprodução. Não editar fontes identificadas pelo hash do coletor do piloto para fins estéticos. A rota API tem identidade própria; Codex e sua trava são históricos preservados. A conformidade exige decisão separada ligada a hashes; HTTP/escore não a aprovam. Orçamento declarado não é teto garantido. Não inferir aprovação científica ou parecer externo. Histórico anterior: [governança pré-piloto](documentacao/historico/pre-piloto-2026-11-06/AGENTS.md).
