# Orientações para agentes

> Atualização vigente — 16/10/2026: RF-01/RF-02 implementados e verificados com Python 3.13.3 + unittest, sem terceiros. Sete casos de aceitação conformes, três concessões próprias, 32 combinações de estado e controle Auditoria/visualizar; 10 métodos, zero falhas/erros/ignorados. Evidências em `specs/001-autorizacao-direta/evidencias.md` (caminho desde a raiz). D-09/D-10 registram recorte aceito e autorização. Domínio ativo parcial somente Consulta ou Auditoria isoladamente; RF-03/RF-04 permanecem futuros. Afirmações de ausência de autorização/implementação nos registros de 14/10 abaixo são históricas, superadas somente nesse alcance. Constituição não formalmente adotada; referência, notas, prompts, métricas e piloto pendentes. Nenhum piloto ou LLM experimental executado.


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

A etapa atual é documental: sem código ou nova Spec. Uma instrução futura pode autorizar outra etapa; a restrição atual não é veto permanente.
