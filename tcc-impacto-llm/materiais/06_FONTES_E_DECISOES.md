# 6. Fontes, decisões e resposta ao feedback

## 6.1 Base documental consolidada

Foram usados os materiais disponíveis nesta conversa e no workspace. Versões históricas permanecem preservadas; não foram tratadas como decisões simultaneamente vigentes.

| Material | Como foi utilizado |
|---|---|
| Proposta revisada mais recente disponível, final `(3)` | Objetivo comparativo, quatro requisitos/mudanças, um LLM e limites do estudo |
| Pauta de alinhamento em Markdown e versão Word com diagramas | Baseline de três papéis, onze testes e quatro condições; é a base operacional mais recente |
| Visão geral da pesquisa | Separação entre aplicação de apoio e avaliação de respostas |
| Plano de documentação e kit anteriores | Organização de artefatos; regras antigas de vários níveis não foram carregadas para a baseline |
| Documento formal de escopo e pesquisa de delimitação | Histórico do recorte; divergências subordinadas à pauta mais recente, sem apagar fontes |
| Ata da segunda orientação coletiva | Contexto versionado, baseline de engenharia e desenvolvimento por pequenas entregas |
| Metodologia incremental assistida por IA | Ciclo capacidade → Spec → planejamento → implementação → evidência → atualização |
| SKILL.md fornecido (`fechar-spec`) | Disciplina de fechamento; seus responsáveis e particularidades de outro projeto não foram importados |
| Avaliações.xlsx, três linhas de avaliação | Métricas provisórias, saída estruturada, isolamento do ambiente, notas sem respostas e rigor da coleta |
| Quatro imagens do feedback do orientador | Concisão, foco, origem do gabarito, denominadores e equilíbrio entre completude e quantidade |
| Análises e versões anteriores da proposta | Histórico; não substituem as orientações posteriores nem servem como aprovação deste redesenho |

As três avaliações não estão identificadas nominalmente por professor na planilha: todas trazem o mesmo campo de orientador. A linha 1 tem nota 2 em clareza/delimitação e em resultados/validação; as demais dimensões recebem 3. A linha 2 tem 3 em todas. A linha 3 tem 2 em resultados/validação e 3 nas demais. Isso reforça a prioridade dada à definição operacional do resultado, sem atribuir comentários a professores não identificados.

## 6.2 Ajustes rastreáveis

| Pedido/risco | Resposta concreta nesta versão | Situação |
|---|---|---|
| Documento longo e perguntas difusas | Resumo de duas páginas; apenas três decisões agrupadas | Preparado |
| Não fica claro o que é analisado | Seleção de conjuntos RF/testes, comparada por mudança/condição | Proposto |
| De onde vem o gabarito? | Regras, política explícita, tabela de expectativas e revisão humana | Candidato, sem revisão concluída |
| Menos testes não significa melhor | Recall/omissões primeiro; redução condicionada à completude | Proposto |
| IDE pode contaminar contexto | Coleta por payload permitido, sem indexação do repositório | A implementar e verificar |
| Notas podem entregar respostas | Nota comum sem IDs; revisão antes do piloto | Candidata |
| Métricas muito abertas | Fórmulas, convenções e tratamento de falhas antecipados | A congelar após o piloto |
| Muitas combinações ampliam o TCC | Um módulo, quatro mudanças, um LLM e análise descritiva | Mantido |
| MC-04 tinha propagação discutível | Substituição candidata por retirada da herança | Requer alinhamento |
| Cinco repetições sugeridas na avaliação | Proposta inicial de 80 execuções; decisão final registrada após piloto | Não apresentar como imposição aprovada |

Não alterar o título ou a proposta formal nesta etapa. Se o orientador quiser transformar o TCC em construção/validação de um framework geral, isso requer um novo alinhamento de objetivo e escopo; este pacote não faz essa mudança.

## 6.3 Fontes externas consultadas — 29/09/2026

**F1 — ISTQB, Certified Tester Foundation Level Syllabus v4.0.1.** Seções 1.4.4 (rastreabilidade), 2.2.3 (regressão) e 5.3 (monitoramento). Apoia relacionar requisitos/testes e acompanhar evidências. É um corpo de conhecimentos, não certificação deste trabalho nem fonte dos IDs corretos.
https://istqb.org/wp-content/uploads/2024/11/ISTQB_CTFL_Syllabus_v4.0.1.pdf

**F2 — ISO/IEC/IEEE 29119-3:2021, Test documentation.** Página pública consultada para delimitar o tema de documentação de testes. Não houve acesso ao texto integral da norma; não se afirmam atendimento de cláusulas, checklist normativa completa ou conformidade. A norma não determina os valores do gabarito local.
https://www.iso.org/standard/79429.html

**F3 — Manning, Raghavan e Schütze, Introduction to Information Retrieval, avaliação de conjuntos não ordenados.** Fundamenta precisão, revocação e F1, adaptados aqui a conjuntos de IDs. O tratamento de saída vazia e a prioridade de interpretação são convenções declaradas do protocolo.
https://nlp.stanford.edu/IR-book/html/htmledition/evaluation-of-unranked-retrieval-sets-1.html

**F4 — GitHub Spec Kit, README oficial.** Apoia o uso de especificação, planejamento, tarefas, implementação e convergência. Não é método de validação científica nem gerador autônomo de gabarito correto.
https://github.com/github/spec-kit

**F5 — Spec Kit, referência de integrações.** Informa `--integration` e a forma `$speckit-<etapa>` no Codex; a forma exposta depende da integração instalada.
https://github.github.io/spec-kit/reference/integrations.html

**F6 — Spec Kit, release v1.0.12.** Comando de instalação com tag fixada. Não instalado nem testado nesta entrega.
https://github.com/github/spec-kit/releases/tag/v1.0.12

**F7 — Spec Kit, referência do CLI.** Inicialização, verificação e gestão da ferramenta. Conferir a ajuda da versão fixada antes de executar procedimentos.
https://github.github.io/spec-kit/reference/core.html

**F8 — Rothermel e Harrold (1996), Analyzing Regression Test Selection Techniques.** Registro e resumo no repositório da universidade: fundamentam a necessidade de critérios explícitos para comparar seleção de regressão. Não equiparar as métricas de recuperação de IDs deste TCC a uma prova de seleção segura de testes.
https://digitalcommons.unl.edu/csearticles/13/

**Jaccard:** definição matemática de interseção/união explicitada no protocolo; sugerida na terceira avaliação anexada. Mede repetibilidade dos conjuntos, não acerto. Não atribuir sua fórmula ao Spec Kit ou à ISO.

Em síntese metodológica: boas práticas orientam os artefatos; as regras locais e sua revisão sustentam a referência; métricas de conjuntos quantificam a comparação. Nenhuma fonte externa aprova automaticamente o desenho proposto.

## 6.4 Três decisões a obter do orientador

1. **Objeto e casos:** podemos manter o estudo de seleção de IDs nesse módulo, contando impacto funcional em dependências, e substituir a quarta mudança pela retirada da herança? A entrega será protocolo + avaliação no recorte, sem framework geral.
2. **Referência e medidas:** a política conservadora de testes é adequada? Podemos usar recall/precisão/F1 separados para RF e testes, e consistência, com redução somente quando não houver omissões? O senhor pode revisar a referência/notas, ou indica outro revisor?
3. **Execução:** podemos seguir com quatro condições, uma chamada por execução, piloto de 16 e proposta de 80 chamadas principais, análise descritiva e congelamento após o piloto?

Registro a preencher: data; decisão; ajustes solicitados; responsável; documentos afetados; próxima ação. Resposta parcial não equivale à aprovação dos demais pontos.
