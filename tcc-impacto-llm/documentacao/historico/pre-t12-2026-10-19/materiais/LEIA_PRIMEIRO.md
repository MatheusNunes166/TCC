# Experimento do TCC — revisão após o feedback
**Matheus Henrique Braun Nunes | 29/09/2026 | versão candidata 0.1**

Este pacote transforma o feedback em um desenho executável. Não contém aplicativo implementado, resultados de LLM, piloto realizado ou aprovação do orientador. Os documentos anteriores foram preservados. As tabelas de referência são hipóteses justificadas para revisão humana.

## Comece por aqui
1. Envie somente `Desenho_Experimental_Para_Orientador.docx` ao orientador. Ele resume objeto, comparação, referência, medidas e três decisões.
2. Leia `01_PROTOCOLO.md`: explica o que a pesquisa mede e o que pode concluir.
3. Revise `02_REQUISITOS_TESTES_E_REFERENCIA.md` com ele: concretiza os quatro requisitos, onze testes, quatro mudanças e o gabarito candidato.
4. Com essas decisões registradas, use `03_DESENVOLVIMENTO_SPEC_KIT.md` para começar pela documentação e avançar por pequenos incrementos.
5. Prepare as notas e os pedidos ao modelo com `04_NOTAS_E_PROMPTS.md`.
6. Execute o ensaio descrito em `05_PILOTO_E_COLETA.md`, congele o protocolo e só então faça a coleta principal.
7. Consulte `06_FONTES_E_DECISOES.md` para ver o que foi aproveitado, corrigido ou deixado para validação.

## O que muda em relação à pauta anterior
- O foco passa a ser a **avaliação da seleção de IDs**, com referência e denominadores explícitos. O sistema é uma bancada pequena para viabilizar essa avaliação.
- Propõe-se substituir MC-04 por retirada da relação de herança. A antiga mudança sobre contas em revisão fica no histórico, sem entrar junto na coleta.
- A relevância dos testes recebe uma política única de seleção, incluindo preservação de comportamentos. Não se considera que apenas resultados alterados sejam relevantes.
- Precisão, revocação, F1 e consistência já ficam propostos. O piloto verifica a operação e pode exigir ajustes documentados antes do congelamento.
- Spec Kit organiza o desenvolvimento; as quatro condições experimentais continuam sendo D0, D1, E0 e E1. Não são quatro ferramentas.
- Notas são artefatos preparados pelo pesquisador no papel de analista de testes. Não representam depoimentos de especialistas nem conhecimento tácito coletado.

## Vocabulário em linguagem simples
- **RF:** requisito funcional, uma regra do sistema. RF-03 trata da herança.
- **T:** caso de teste já existente na bancada. T05 verifica acesso herdado.
- **MC:** mudança controlada, aplicada sozinha sobre a mesma versão inicial.
- **Gabarito:** conjuntos esperados e suas justificativas, revisados antes da coleta.
- **Spec:** descrição de um incremento, com critérios, plano e tarefas.
- **Incremental:** construir uma capacidade pequena, verificar e registrar antes da próxima.
- **Piloto:** ensaio do procedimento; seus resultados não entram na comparação principal.
- **Congelamento:** registrar as versões e parar de alterar regras, notas e pedidos durante a coleta.

As figuras são elaboração própria com apoio de IA. Descrevem o protocolo candidato, não uma arquitetura já implementada. As referências externas fundamentam conceitos e ferramentas; não certificam este experimento.
