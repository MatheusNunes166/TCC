> Estado vigente — 19/10/2026 (D-15/D-16): T12 adotado pelo pesquisador e verificado na versão inicial como negar/conflito. Python 3.13.3: teste isolado OK; suíte integrada com 18 métodos OK, T01–T12 12/12 e controles anteriores preservados. Catálogo: 12 testes; referência candidata: 48 pares teste × mudança, 60 expectativas incluindo a versão inicial; seleções 2/4/8/5. Variantes não implementadas nem executadas; sem piloto ou LLM experimental. A adoção é autorização do pesquisador, sem aprovação científica atribuída ao orientador. Revisão científica e adoção formal da constituição continuam pendentes. Evidências: `documentacao/evidencias-t12.md` (caminho desde a raiz).

## Estado anterior preservado — 18/10/2026

> Estado histórico — 18/10/2026 (D-13/D-14): Spec 002 implementada com Python 3.13.3 + unittest. RF-01–RF-04 integrados; 17 métodos aprovados, T01–T11 11/11 em decisão/motivo e 55 subtestes auxiliares conformes, zero falhas/erros/ignorados. Três estados, oito subconjuntos e duas operações no domínio válido; verificação dirigida, sem matriz que inclua T12. Evidências em `specs/002-heranca-incompatibilidade/quickstart.md` (caminho desde a raiz). T12 somente proposta; catálogo 11/44 e gabarito preservados. Sem variantes, piloto ou LLM experimental. Adoção constitucional e pendências científicas permanecem abertas. Trechos datados anteriores abaixo são históricos e não descrevem a capacidade atual.

﻿# Contexto e escopo

> Atualização vigente — 16/10/2026: RF-01/RF-02 implementados e verificados com Python 3.13.3 + unittest, sem terceiros. Sete casos de aceitação conformes, três concessões próprias, 32 combinações de estado e controle Auditoria/visualizar; 10 métodos, zero falhas/erros/ignorados. Evidências em `specs/001-autorizacao-direta/evidencias.md` (caminho desde a raiz). D-09/D-10 registram recorte aceito e autorização. Domínio ativo parcial somente Consulta ou Auditoria isoladamente; RF-03/RF-04 permanecem futuros. Afirmações de ausência de autorização/implementação nos registros de 14/10 abaixo são históricas, superadas somente nesse alcance. Constituição não formalmente adotada; referência, notas, prompts, métricas e piloto pendentes. Nenhum piloto ou LLM experimental executado.


Baseline documental preparada em 14/10/2026. O desenho de pesquisa e os contratos permanecem candidatos à revisão; não há implementação, testes executados ou gabarito validado nesta entrega. Situações e responsáveis estão em [decisoes.md](decisoes.md).

## Objetivo da pesquisa

Comparar como a organização da solicitação e a presença de notas do analista afetam os conjuntos de IDs de requisitos impactados e testes relevantes selecionados por um único LLM. Observar acertos, omissões, excedentes e consistência em quatro mudanças independentes do mesmo módulo.

A entrega proposta é um protocolo documentado, referência rastreável revisada por humanos, registros reproduzíveis e análise descritiva. As condições candidatas são D0 (direta sem notas), D1 (direta com notas), E0 (etapas sem notas) e E1 (etapas com notas), sempre com uma chamada independente. As notas são preparadas pelo pesquisador, sem representar depoimentos de especialistas.

## Finalidade do sistema

O sistema de permissões é uma bancada local fictícia para tornar regras, dependências e mudanças verificáveis. Recebe estado da conta, papéis e operação e retorna decisão e motivo. Seu contrato está em [requisitos.md](requisitos.md); estrutura proposta em [arquitetura.md](arquitetura.md).

## Limites

- Quatro RFs, três papéis, duas operações, herança de um nível e uma incompatibilidade.
- Doze casos no catálogo, descritos em [qualidade-e-testes.md](qualidade-e-testes.md).
- Quatro mudanças isoladas, cada uma sobre a mesma baseline; um LLM e comparação dentro de cada mudança.
- Impacto candidato inclui alteração funcional de uma dependência, mesmo sem alteração textual do requisito.
- Resultados medem concordância com a referência local; não demonstram compreensão interna, detecção de defeitos, cobertura de código ou economia real de regressão.

## Fora do escopo

Cadastro, interface, autenticação real, banco, implantação, dados reais, entradas malformadas, hierarquia multinível, ciclos, conflitos adicionais, vários modelos, novos testes gerados pelo LLM avaliado, framework geral e benchmark de vários sistemas.

Na preparação inicial foram autorizados apenas os seis documentos desta baseline. Posteriormente foram autorizados Spec, planejamento, tarefas e análise, registrados em [decisoes.md](decisoes.md) (D-06–D-08). Implementação e pesquisa ainda não executadas nem autorizadas nesta entrega. A preparação documental não libera o piloto. Próximas capacidades e critérios de passagem estão em [roadmap.md](roadmap.md).

Fontes: [guia de leitura](../materiais/LEIA_PRIMEIRO.md), [protocolo](../materiais/01_PROTOCOLO.md) e [fontes e decisões](../materiais/06_FONTES_E_DECISOES.md). Os materiais permanecem preservados como fontes; estes documentos não devem ser enviados integralmente ao modelo avaliado.
