# Experimento do TCC — revisão após o feedback
**Matheus Henrique Braun Nunes | 29/09/2026 | versão candidata 0.1**

Este pacote transforma o feedback em um desenho experimental. Atualização de 19/10/2026: a versão inicial está implementada e verificada, agora com T12 adotado pelo pesquisador (D-15/D-16). Variantes não foram implementadas nem executadas; não há resultados de LLM ou piloto realizado. A adoção não registra aprovação científica do orientador. As tabelas de referência continuam candidatas à revisão humana; versões anteriores estão preservadas.

## Comece por aqui
1. O arquivo `Desenho_Experimental_Para_Orientador.docx` é histórico, anterior à adoção de T12; não é a versão vigente do catálogo. Para revisão atual, use `../documentacao/referencia-candidata-proxima-etapa.md` e os materiais atualizados. Ele não foi regenerado nesta etapa.
2. Leia `01_PROTOCOLO.md`: explica o que a pesquisa mede e o que pode concluir.
3. Revise `02_REQUISITOS_TESTES_E_REFERENCIA.md` com ele: concretiza os quatro requisitos, doze testes, quatro mudanças e o gabarito candidato.
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

## Atualização do catálogo — 19/10/2026

D-15 registra a adoção de T12 pelo pesquisador, sem aprovação científica do orientador. 12 testes, 48 pares e 60 expectativas incluindo a versão inicial; gabarito candidato 0.2. Histórico literal pré-T12 e hashes em `../documentacao/historico/pre-t12-2026-10-19/`. Diagramas e Word anteriores são materiais históricos. O bloco comum de impacto/relevância é `07_DEFINICOES_COMUNS.md`, idêntico para D0/D1/E0/E1; não contém respostas.
