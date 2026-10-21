> Estado vigente — 21/10/2026 (D-20/D-21): Spec 003 implementada e verificada; 35/35 tarefas concluídas com evidências. Quatro variantes independentes de B `aec474bcb54d6dae2afceff8e5b9226991386490`, uma edição por fonte, diffs/AST e revisão registrados. Python 3.13.3: suíte original 18 métodos OK, baseline 12/12 pares e variantes 48/48 conformes por decisão/motivo, zero divergências/erros/lacunas; 17 métodos sintéticos separados da bancada. Baseline, testes, materiais, referência candidata 0.2 e seleções 2/4/8/5 preservados. Evidências e diagnóstico do mecanismo: `specs/003-mudancas-controladas/evidencias.md` (desde a raiz). P-01/P-02/P-03, revisão das expectativas T12 e adoção constitucional pendentes; T12 já adotado/verificado em B. Revisão profissional, possíveis novos modelos e métricas aguardam transcrição da orientação e decisão explícita. Sem piloto, coleta ou LLM. Próxima ação: revisão humana das evidências e da referência candidata, seguida de detalhamento da orientação; nenhuma etapa experimental liberada. Registros anteriores abaixo são históricos.

> Revisão vigente — 21/10/2026 (D-19): Spec 003 confirmada pelo resolvedor local; tasks.md existente revisado, 35 tarefas pendentes. T024 separa controles sintéticos da matriz real e da CLI futura. B aec474bcb54d6dae2afceff8e5b9226991386490 disponível; fontes iniciais e referência 0.2 preservadas. Somente inspeção Git/JSON/documental e script de pré-requisitos; nenhuma variante implementada, teste ou chamada ao LLM executados. Revisão profissional, possíveis novos modelos e alterações nas métricas aguardam transcrição da orientação e decisão explícita. P-01/P-02/P-03 e adoção constitucional pendentes. Próxima ação: considerar o relatório de consistência desta revisão; implementação depende de pedido próprio. Registros datados abaixo são históricos.

> Estado vigente — 20/10/2026 (D-18): Spec 003 ativa, confirmada por setup-tasks; especificação/planejamento/tarefas preparados. tasks.md contém 35 tarefas, todas pendentes; análise de consistência somente documental na resposta da solicitação. B = aec474bcb54d6dae2afceff8e5b9226991386490; baseline/testes/T12/referência candidata 0.2 e seleções 2/4/8/5 preservados. Nenhuma variante implementada ou teste executado agora; sem piloto/LLM experimental. Revisões científicas e adoção constitucional pendentes. Próxima ação: revisão de tarefas/achados e pedido próprio de implementação.

## Estado anterior preservado — 18/10/2026

> Estado histórico — 18/10/2026 (D-13/D-14): Spec 002 implementada com Python 3.13.3 + unittest. RF-01–RF-04 integrados; 17 métodos aprovados, T01–T11 11/11 em decisão/motivo e 55 subtestes auxiliares conformes, zero falhas/erros/ignorados. Três estados, oito subconjuntos e duas operações no domínio válido; verificação dirigida, sem matriz que inclua T12. Evidências em `specs/002-heranca-incompatibilidade/quickstart.md` (caminho desde a raiz). T12 somente proposta; catálogo 11/44 e gabarito preservados. Sem variantes, piloto ou LLM experimental. Adoção constitucional e pendências científicas permanecem abertas. Trechos datados anteriores abaixo são históricos e não descrevem a capacidade atual.

﻿# Orientações para agentes

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

Etapa autorizada em D-18: gerar tarefas 003 e analisar consistência documental. Planejamento anterior D-17 e adoção/verificação T12 em D-15/D-16 preservados como histórico. Não implementar variantes, executar testes, iniciar piloto ou chamadas ao LLM experimental sem autorização no respectivo escopo.
