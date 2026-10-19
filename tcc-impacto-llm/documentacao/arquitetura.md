> Estado vigente — 18/10/2026 (D-13/D-14): Spec 002 implementada com Python 3.13.3 + unittest. RF-01–RF-04 integrados; 17 métodos aprovados, T01–T11 11/11 em decisão/motivo e 55 subtestes auxiliares conformes, zero falhas/erros/ignorados. Três estados, oito subconjuntos e duas operações no domínio válido; verificação dirigida, sem matriz que inclua T12. Evidências em `specs/002-heranca-incompatibilidade/quickstart.md` (caminho desde a raiz). T12 somente proposta; catálogo 11/44 e gabarito preservados. Sem variantes, piloto ou LLM experimental. Adoção constitucional e pendências científicas permanecem abertas. Trechos datados anteriores abaixo são históricos e não descrevem a capacidade atual.

﻿# Arquitetura mínima proposta

> Atualização vigente — 16/10/2026: RF-01/RF-02 implementados e verificados com Python 3.13.3 + unittest, sem terceiros. Sete casos de aceitação conformes, três concessões próprias, 32 combinações de estado e controle Auditoria/visualizar; 10 métodos, zero falhas/erros/ignorados. Evidências em `specs/001-autorizacao-direta/evidencias.md` (caminho desde a raiz). D-09/D-10 registram recorte aceito e autorização. Domínio ativo parcial somente Consulta ou Auditoria isoladamente; RF-03/RF-04 permanecem futuros. Afirmações de ausência de autorização/implementação nos registros de 14/10 abaixo são históricas, superadas somente nesse alcance. Constituição não formalmente adotada; referência, notas, prompts, métricas e piloto pendentes. Nenhum piloto ou LLM experimental executado.


Estado: desenho documental; componentes e tecnologias não implementados. Limites em [contexto-e-escopo.md](contexto-e-escopo.md), contrato em [requisitos.md](requisitos.md).

Implementado: núcleo local em autorizacao.py e suíte em tests/test_autorizacao.py, sem terceiros. obter_papeis_efetivos expande Supervisão→Consulta; ha_incompatibilidade verifica Consulta+Auditoria efetivos. Consulta direta preservada. Demais componentes experimentais abaixo permanecem propostos.

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
