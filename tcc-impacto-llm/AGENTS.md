> Estado vigente — 19/10/2026 (D-15/D-16): T12 adotado pelo pesquisador e verificado na versão inicial como negar/conflito. Python 3.13.3: teste isolado OK; suíte integrada com 18 métodos OK, T01–T12 12/12 e controles anteriores preservados. Catálogo: 12 testes; referência candidata: 48 pares teste × mudança, 60 expectativas incluindo a versão inicial; seleções 2/4/8/5. Variantes não implementadas nem executadas; sem piloto ou LLM experimental. A adoção é autorização do pesquisador, sem aprovação científica atribuída ao orientador. Revisão científica e adoção formal da constituição continuam pendentes. Evidências: `documentacao/evidencias-t12.md` (caminho desde a raiz).

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

Etapa autorizada em D-15: adoção e teste de T12 na versão inicial, harmonização documental e preservação do histórico. Fechamento em D-16. Não implementar variantes, iniciar piloto ou chamadas ao LLM experimental sem nova autorização e cumprimento dos critérios aplicáveis.
