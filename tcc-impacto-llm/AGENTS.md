# Orientações para agentes

Atualização D-39: integração do patch API e testes offline autorizados nesta conversa. Ler [operação API](documentacao/operacao-api.md). Essa autorização não permite chamada real, consulta autenticada, conexão paga, piloto, commit ou push. A rota API tem identidade própria; o coletor Codex e sua trava permanecem preservados. Não importar como fatos relatos históricos do patch sobre consulta/modelos, outro Word ou testes ainda não reproduzidos. A conformidade depende de decisão externa vinculada a hashes, sem editar brutos; orçamento é declaração, não teto monetário. D-38 abaixo permanece vigente para a rota Codex.

## Ordem de leitura

1. Este arquivo e [.specify/memory/constitution.md](.specify/memory/constitution.md).
2. [ESTADO_ATUAL.md](ESTADO_ATUAL.md), [BLOQUEIOS.md](BLOQUEIOS.md), [HANDOFF.md](HANDOFF.md).
3. Em `documentacao/`: [contexto-e-escopo.md](documentacao/contexto-e-escopo.md), [decisoes.md](documentacao/decisoes.md), [requisitos.md](documentacao/requisitos.md), [arquitetura.md](documentacao/arquitetura.md), [qualidade-e-testes.md](documentacao/qualidade-e-testes.md), [roadmap.md](documentacao/roadmap.md).
4. [materiais/LEIA_PRIMEIRO.md](materiais/LEIA_PRIMEIRO.md) e fontes pertinentes indicadas nele.

## Fontes e decisões

Preserve materiais. A documentação sintetiza a baseline; os materiais sustentam sua origem. Siga instruções atuais do usuário no escopo autorizado. Diante de divergência, registre fontes, impacto e proposta de resolução em `documentacao/decisoes.md`; não escolha silenciosamente uma versão nem promova histórico a regra vigente. Solicite decisão apenas quando a divergência impedir o trabalho corrente e continue tarefas independentes.

Considere confirmada somente decisão com responsável, data e evidência registrados. Autorização de engenharia não equivale à aprovação científica do orientador. Propostas e expectativas permanecem candidatas até revisão registrada.

## Trabalho e fechamento

Desenvolva uma capacidade por vez, conforme roadmap e constituição. Antes de fechar incrementos, revise alterações e confronte critérios com evidências reais, registrando lacunas. Não declare testes executados, capacidades prontas ou pesquisa concluída sem evidência. Atualize documentação afetada, estado, bloqueios e handoff. Centralize decisões em `documentacao/decisoes.md` e use referências.

## Desenvolvimento e experimento

O contexto do assistente de desenvolvimento não é o pacote do LLM avaliado. Não envie estes arquivos ou materiais inteiros ao experimento: contêm expectativas e referência candidata. Siga a separação de coleta/avaliação de `documentacao/arquitetura.md`. Documentação pronta não libera piloto.


Escopo vigente: análise delimitada/ajustes offline D-38 e coletor D-37 em decisões; D-36/D-35 mantidas para preservação e conteúdo experimental. Estado central em ESTADO_ATUAL.md. Histórico literal anterior em documentacao/historico/pre-piloto-2026-11-06/AGENTS.md. Sem chamadas ao LLM, piloto, coleta principal ou stage/commit/push no projeto. Ambos os bloqueios permanecem: inventário/contexto D-29 não demonstrados e provedor embutido openai reservado para overrides de retries. Configurado false não é comprovadamente indisponível; read-only/pasta vazia/ausência de invocações não provam isso. Não remover a trava por booleano nem migrar automaticamente para API/outro provedor. Commit local da D-36 foi permitido exclusivamente no repositório temporário de transporte, não necessário nesta etapa. Não há revisor externo; não inferir aprovação individual de expectativas.
