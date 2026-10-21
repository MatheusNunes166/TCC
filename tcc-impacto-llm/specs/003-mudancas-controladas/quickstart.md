> Estado vigente — 21/10/2026 (D-20/D-21): Spec 003 implementada e verificada; 35/35 tarefas concluídas com evidências. Quatro variantes independentes de B `aec474bcb54d6dae2afceff8e5b9226991386490`, uma edição por fonte, diffs/AST e revisão registrados. Python 3.13.3: suíte original 18 métodos OK, baseline 12/12 pares e variantes 48/48 conformes por decisão/motivo, zero divergências/erros/lacunas; 17 métodos sintéticos separados da bancada. Baseline, testes, materiais, referência candidata 0.2 e seleções 2/4/8/5 preservados. Evidências e diagnóstico do mecanismo: `specs/003-mudancas-controladas/evidencias.md` (desde a raiz). P-01/P-02/P-03, revisão das expectativas T12 e adoção constitucional pendentes; T12 já adotado/verificado em B. Revisão profissional, possíveis novos modelos e métricas aguardam transcrição da orientação e decisão explícita. Sem piloto, coleta ou LLM. Próxima ação: revisão humana das evidências e da referência candidata, seguida de detalhamento da orientação; nenhuma etapa experimental liberada. Registros anteriores abaixo são históricos.

> Revisão vigente — 21/10/2026 (D-19): Spec 003 confirmada pelo resolvedor local; tasks.md existente revisado, 35 tarefas pendentes. T024 separa controles sintéticos da matriz real e da CLI futura. B aec474bcb54d6dae2afceff8e5b9226991386490 disponível; fontes iniciais e referência 0.2 preservadas. Somente inspeção Git/JSON/documental e script de pré-requisitos; nenhuma variante implementada, teste ou chamada ao LLM executados. Revisão profissional, possíveis novos modelos e alterações nas métricas aguardam transcrição da orientação e decisão explícita. P-01/P-02/P-03 e adoção constitucional pendentes. Próxima ação: considerar o relatório de consistência desta revisão; implementação depende de pedido próprio. Registros datados abaixo são históricos.

# Guia de validação — Spec 003

Preparação da implementação autorizada em 21/10/2026: Spec ativa 003, checklist 23/23 satisfeito. B confirmado; HEAD `8041b0b1deca09f13c8b95069699616c7a1a7a60`. Sete alterações documentais locais preservadas em `evidencias/spec003/preparacao/alteracoes-locais-iniciais/`, hashes/comandos/Python em `inventario.json`. Novos caminhos limitados a `variantes/`, verificador, controles e evidências. Blobs iniciais: módulo `c219b9ab1f2ed75a92664c79009a1a417e75ef11`, testes `e2d9c09a43268abc96a5b7e93095f22e023266f4`, referência `9533e7dfa053af0f73449de8a42747e81949c53d`; baseline e candidata 0.2 serão conferidas novamente por hashes antes/depois. T001/T002 realizados sem execução da bancada; demais registros abaixo são históricos até o fechamento da implementação.

Data: 19/10/2026. **Planejado, não executado.** Variantes, verificador e teste novo ainda não existem. Comandos de execução dependem de autorização própria, implementação e revisão; este guia não atesta capacidade pronta.

## Pré-condições

Spec ativa 003 e desenho revisado; Git/Python locais, sem pacotes novos. B = `aec474bcb54d6dae2afceff8e5b9226991386490`, com módulo/testes/requisitos/catálogo/JSON 0.2 disponíveis. Implementar futuramente as quatro fontes com origem B, edição única e diffs/AST revisados conforme [plano](plan.md). Executor versionado/identificado, pasta nova de saída; alterações relevantes não commitadas devem ser informadas antes de incluídas, sem redefinir B.

## Conferência de procedência — comandos de leitura

Na raiz de tcc-impacto-llm:

```powershell
git status --short
git rev-parse HEAD
git rev-parse --show-toplevel
git rev-parse --show-prefix
git cat-file -t aec474bcb54d6dae2afceff8e5b9226991386490
git diff aec474bcb54d6dae2afceff8e5b9226991386490 -- autorizacao.py tests/test_autorizacao.py materiais/modelos/referencia_candidata_NAO_ENVIAR_AO_LLM.json
python --version
```

Esperado: commit disponível, fontes iniciais sem diferenças relevantes, T01–T12 e 0.2 completos. HEAD do executor pode conter implementação posterior e é registrado separadamente. Snapshot por extração binária do Git; evitar redirecionar git show para arquivos pelo PowerShell.

## Rodada integrada futura

```powershell
python -B verificacao_variantes.py --saida evidencias/spec003/rodada-001
```

Nome de pasta novo por tentativa; rodada-001 é exemplo. O programa deverá conferir fontes e executar suíte original (18 métodos/controles) no snapshot B, obter 12 pares iniciais e executar os 48 pares de variantes. Ver [contrato](contracts/verificacao.md) para códigos/registros. Preservar evidências mesmo com falha; conjuntos 2/4/8/5 não limitam execução.

Para conferir só a suíte inicial no snapshot da tentativa, usar `python -B -m unittest discover -s tests -p test_autorizacao.py -v` com cwd no snapshot B. Isso não substitui as 48 comparações. Não executar testes originais com expectativas iniciais contra uma variante.

## Aceitação futura

| Conferência | Evidência necessária |
|---|---|
| Origem comum | Mesmo B, objetos/hashes, quatro diffs contra B, nenhum módulo derivado de outra variante |
| Alteração única | Diff revisado/AST limitados às expressões previstas, assinaturas e demais funções intactas |
| Preservação de B | Suíte original 18 métodos OK, 12 pares/controles e hashes antes/depois intactos |
| Matriz completa | 48 chaves distintas: T01–T12 em cada mudança, esperado específico e fonte executada |
| Par integral | Decisão e motivo exatos; T07/MC-04 não passa com motivo conflito |
| T12 | Candidata: MC-01 negar/conflito; MC-02 permitir/permissao_direta; MC-03 negar/conflito; MC-04-v2 permitir/permissao_direta |
| Sem filtro | T12/MC-03 executado mesmo excluído da seleção; conjuntos preservados |
| Registros | Esperado/observado/estado, manifesto, logs/diffs e conclusão de engenharia separada de revisão científica |

Validar mecanismo de registro com fixtures sintéticas: decisão igual/motivo diferente, exceção, saída malformada, alteração extra de fonte, referência incompleta, pasta repetida e persistência após falha. São controles de infraestrutura separados, sem IDs experimentais novos e sem alteração de esperado. Nunca misturar esses dados com as 48 comparações reais.

## Em divergência

Conferir fonte/hash/B, entrada/ID/esperado/diff, requisitos/precedência e fundamentos da candidata. Registrar hipótese/causa/evidência/responsável, sem trocar esperado por observado. Suspeita científica vai a revisão humana/versionamento futuro autorizado; manter 0.2 e resultado original. Retentativa em pasta nova, ligada à anterior.

## Realizado nesta etapa

19/10/2026: governança/Spec/checklist/referência/T12 lidos; árvore inicial limpa, B/blobs conferidos por Git/AST sem importar/executar núcleo. Python 3.13.3 disponível. Seleção 003 persistida em .specify/feature.json; check-prerequisites.sh --json --paths-only confirmou FEATURE_SPEC/IMPL_PLAN de 003 antes do setup-plan.sh --json. Setup copiou template após repetição autorizada por bloqueio do sandbox. BRANCH do resolvedor é contexto, sem criação de branch Git. Cinco artefatos de planejamento produzidos; sem tasks, variantes, teste de aplicação, piloto ou LLM experimental.

P-01/P-02/P-03, revisão das expectativas T12 e adoção constitucional continuam pendentes; T12 já adotado em B. Documentos ou conformidade executável futura não liberam pesquisa. Próxima ação: revisão do planejamento e solicitação de tarefas quando desejado.

Conferência documental final realizada: cinco artefatos presentes, links locais válidos, nenhum placeholder técnico pendente ou whitespace indevido; ausência de tasks e de fontes novas de variantes/verificador/teste. Comparação Git contra B confirmou código, testes, materiais, requisitos, catálogo e referência intactos; JSON continua candidato 0.2, 12 casos, 48 expectativas e conjuntos 2/4/8/5. `git diff --check` sem erros. O resolvedor `check-prerequisites.sh --json --require-spec` retornou FEATURE_DIR de 003 e AVAILABLE_DOCS contendo research.md, data-model.md, contracts/ e quickstart.md. Sem hooks de extensão no fechamento. Essas são verificações documentais, não testes de aplicação.


## Execução concluída — 21/10/2026

Comando final: `python -B verificacao_variantes.py --saida evidencias/spec003/rodada-final`, na raiz do projeto, Python 3.13.3. Código 0; baseline 18 métodos/12 pares conformes, variantes 48/48 conformes; zero divergências/erros/lacunas, hashes intactos. Para repetir, usar outro nome de pasta; uma tentativa existente é recusada.

Controles sintéticos: `python -B -m unittest discover -s tests -p test_variantes.py -v`, 17 métodos OK em `evidencias/spec003/sintetico-final-green/`. Não compõem os 48 pares. [Relatório completo](evidencias.md) registra fases, versões, M-01 e resolução, diffs e evidências originais. Sem suspeita de erro de expectativa; revisão científica pendente. Comandos e descrições futuras datadas acima documentam o planejamento anterior.
