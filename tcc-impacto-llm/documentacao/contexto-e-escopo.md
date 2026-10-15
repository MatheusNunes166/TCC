# Contexto e escopo

Baseline documental preparada em 14/10/2026. O desenho de pesquisa e os contratos permanecem candidatos à revisão; não há implementação, testes executados ou gabarito validado nesta entrega. Situações e responsáveis estão em [decisoes.md](decisoes.md).

## Objetivo da pesquisa

Comparar como a organização da solicitação e a presença de notas do analista afetam os conjuntos de IDs de requisitos impactados e testes relevantes selecionados por um único LLM. Observar acertos, omissões, excedentes e consistência em quatro mudanças independentes do mesmo módulo.

A entrega proposta é um protocolo documentado, referência rastreável revisada por humanos, registros reproduzíveis e análise descritiva. As condições candidatas são D0 (direta sem notas), D1 (direta com notas), E0 (etapas sem notas) e E1 (etapas com notas), sempre com uma chamada independente. As notas são preparadas pelo pesquisador, sem representar depoimentos de especialistas.

## Finalidade do sistema

O sistema de permissões é uma bancada local fictícia para tornar regras, dependências e mudanças verificáveis. Recebe estado da conta, papéis e operação e retorna decisão e motivo. Seu contrato está em [requisitos.md](requisitos.md); estrutura proposta em [arquitetura.md](arquitetura.md).

## Limites

- Quatro RFs, três papéis, duas operações, herança de um nível e uma incompatibilidade.
- Onze casos planejados, descritos em [qualidade-e-testes.md](qualidade-e-testes.md).
- Quatro mudanças isoladas, cada uma sobre a mesma baseline; um LLM e comparação dentro de cada mudança.
- Impacto candidato inclui alteração funcional de uma dependência, mesmo sem alteração textual do requisito.
- Resultados medem concordância com a referência local; não demonstram compreensão interna, detecção de defeitos, cobertura de código ou economia real de regressão.

## Fora do escopo

Cadastro, interface, autenticação real, banco, implantação, dados reais, entradas malformadas, hierarquia multinível, ciclos, conflitos adicionais, vários modelos, novos testes gerados pelo LLM avaliado, framework geral e benchmark de vários sistemas.

Na preparação inicial foram autorizados apenas os seis documentos desta baseline. Posteriormente foram autorizados Spec, planejamento, tarefas e análise, registrados em [decisoes.md](decisoes.md) (D-06–D-08). Implementação e pesquisa ainda não executadas nem autorizadas nesta entrega. A preparação documental não libera o piloto. Próximas capacidades e critérios de passagem estão em [roadmap.md](roadmap.md).

Fontes: [guia de leitura](../materiais/LEIA_PRIMEIRO.md), [protocolo](../materiais/01_PROTOCOLO.md) e [fontes e decisões](../materiais/06_FONTES_E_DECISOES.md). Os materiais permanecem preservados como fontes; estes documentos não devem ser enviados integralmente ao modelo avaliado.

