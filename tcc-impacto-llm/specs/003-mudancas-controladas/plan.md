# Implementation Plan: Quatro mudanças controladas e verificação de efeitos

**Feature**: `003-mudancas-controladas` | **Date**: 2026-10-19 | **Spec**: [spec.md](spec.md)

**Input**: Spec/checklist 003 e referência candidata 0.2. Autorização do pesquisador para planejamento, seleção ativa e reconciliação documental, registrada em D-17 de [decisões](../../documentacao/decisoes.md). Sem tarefas, variantes ou testes novos implementados.

## Summary

Preparar futuramente quatro módulos autônomos, cada um extraído diretamente do mesmo blob de B e com uma edição mínima. Preservar módulo e suíte iniciais. Conferir origem/diff antes de executar. Python + unittest percorre o catálogo completo de 12 casos em cada variante, usando seu `expected` da referência 0.2 e comparando decisão/motivo: 48 pares. B e seus controles são conferidos separadamente. Evidências por tentativa conservam fontes, esperado, observado, identidade executada e divergências.

Quatro cópias pequenas, sem worktrees, branches adicionais, motor de políticas, flags na baseline ou geração dinâmica de variantes. Decisões em [research.md](research.md), modelo em [data-model.md](data-model.md), interface em [contracts/verificacao.md](contracts/verificacao.md) e validação futura em [quickstart.md](quickstart.md).

## Technical Context

**Language/Version**: Python 3.13.3 disponível; compatibilidade mínima existente 3.11+. Registrar versão real da execução futura.

**Primary Dependencies**: somente biblioteca padrão (unittest, json, pathlib, hashlib, subprocess, importlib.util, ast, difflib, datetime, sys, uuid) e Git local para leitura de objetos. Nenhuma instalação.

**Storage**: módulos versionados; arquivos JSON e logs/diffs em diretório exclusivo por tentativa. Referência extraída de B, nunca regravada pelo verificador.

**Testing**: unittest; preservar literalmente os 18 métodos da suíte inicial, T01–T12 e controles. Nova matriz usa subtestes por par e contagem explícita dos 48 IDs, não “Ran N tests”. Testes de infraestrutura com dados sintéticos são separados do catálogo experimental.

**Target Platform**: Windows/PowerShell local; pathlib e subprocessos com lista de argumentos e sys.executable, sem shell para executar a bancada. Bash somente para scripts locais do Spec Kit.

**Project Type**: bancada e interface local de verificação; sem serviço ou integração com LLM.

**Performance Goals**: completude e rastreabilidade das 48 comparações, sem meta de latência ou alegação de economia real.

**Constraints**: B imutável; preservar testes/expectativas/conjuntos; seleção 2/4/8/5 não filtra execução. Sem infraestrutura, dependências, tarefas ou implementação nesta etapa.

**Scale/Scope**: quatro mudanças × 12 casos = 48 pares de variantes; mais 12 expectativas iniciais = 60. Controles não ampliam o catálogo.

### Origem comum confirmada

B: **`aec474bcb54d6dae2afceff8e5b9226991386490`**, como na Spec. HEAD da sessão: `3cdff8ec1c82b4919bce3761364364754863ca81`, que acrescenta a Spec 003. `git status --short` inicial vazio: nenhuma alteração relevante não commitada antes de fixar B.

| Artefato relativo ao projeto | Objeto blob Git em B | Conferência por leitura |
|---|---|---|
| autorizacao.py | c219b9ab1f2ed75a92664c79009a1a417e75ef11 | RF-01–RF-04, quatro funções e assinatura existente |
| tests/test_autorizacao.py | e2d9c09a43268abc96a5b7e93095f22e023266f4 | AST: 18 métodos test_*, IDs T01–T12, T12/exportar/negar-conflito e controles |
| JSON de referência | 9533e7dfa053af0f73449de8a42747e81949c53d | 0.2, CANDIDATO_NAO_REVISADO, 12 casos, 12 expected por mudança, conjuntos 2/4/8/5 |

`git diff B HEAD --` desses três arquivos, requisitos, catálogo e evidências T12 estava vazio. Isso confirma disponibilidade e identidade, não execução nesta sessão. Evidência histórica em [evidencias-t12.md](../../documentacao/evidencias-t12.md).

Extrair fontes por subprocesso Git em bytes, com argumentos separados. Resolver `--show-toplevel` e `--show-prefix`: o projeto está em `tcc-impacto-llm/` dentro da raiz Git. Usar `git show <B>:<prefixo><arquivo>`, nunca HEAD móvel ou redirecionamento textual do PowerShell. Preservar BOM/quebras de linha. Registrar objeto Git e SHA-256 dos bytes extraídos/carregados; hash de arquivo de trabalho com CRLF pode diferir do blob e não substitui sua identidade.

## Constitution Check

Revisão antes da fase 0 e novamente após o desenho. Constituição 1.0.0 continua sem ratificação formal; engenharia não presume aprovação científica.

| Princípio | Antes | Após desenho | Evidência |
|---|---|---|---|
| Escopo controlado | Conforme | Conforme | Quatro cópias e verificador local; sem piloto/novos fatores |
| Decisões explícitas | Conforme | Conforme | D-17, research e pendências científicas separadas |
| Rastreabilidade | Conforme | Conforme | B/blobs, fonte carregada, referência 0.2 e registro por par |
| Verificação por evidências | Conforme | Conforme | Esperado/observado separados; lacunas explícitas; nada executado agora |
| Incrementos pequenos | Conforme | Conforme | Cinco documentos; sem tasks, variantes ou teste novo |
| Contextos separados | Conforme | Conforme | Spec/referência/logs não integram pacote do LLM avaliado |

Sem violação ou dúvida técnica bloqueante. Revisões científicas pendentes não são convertidas em decisões aprovadas.

## Project Structure

### Documentation (this feature)

```text
specs/003-mudancas-controladas/
├── spec.md
├── checklists/requirements.md
├── plan.md
├── research.md
├── data-model.md
├── contracts/verificacao.md
└── quickstart.md
```

Cinco artefatos de planejamento; tasks.md não é produzido por esta fase.

### Source Code (repository root) — desenho futuro

```text
autorizacao.py                    # existente, preservado
tests/test_autorizacao.py         # existente, preservado
variantes/
├── mc01.py                       # futuro: B + MC-01
├── mc02.py                       # futuro: B + MC-02
├── mc03.py                       # futuro: B + MC-03
└── mc04.py                       # futuro: B + MC-04-v2
verificacao_variantes.py          # futuro: procedência, unittest, evidências
tests/test_variantes.py           # futuro: matriz e controles do registrador
evidencias/spec003/<id_execucao>/  # futuro: diretório novo por tentativa
├── manifesto.json
├── resultados.json
├── baseline-unittest.txt
├── variantes-unittest.txt
├── diffs/
└── fontes/                      # snapshot B, variantes e executor
```

**Structure Decision**: variantes autônomas, sem importar código de B/outra variante, monkeypatch ou parâmetro de política na API inicial. Arquivos futuros não foram criados. Evidências não sobrescrevem materiais/modelos nem logs anteriores.

## Phase 0 — pesquisa técnica

[research.md](research.md) resolve as escolhas por inspeção local, incluindo revisão auxiliar de leitura prevista pela skill; sem consulta externa ou execução da bancada. Nenhuma incerteza técnica pendente.

## Phase 1 — desenho

### Quatro cópias a partir de B

Extrair novamente o mesmo blob de B para cada fonte; jamais copiar MC-02 de MC-01. Uma única diferença executável permitida:

| Fonte | ID canônico | Edição |
|---|---|---|
| variantes/mc01.py | MC-01 | Retirar só ('Auditoria', 'exportar') da sequência de concessões de obter_permissoes_diretas |
| variantes/mc02.py | MC-02 | Trocar só o retorno de ha_incompatibilidade por False |
| variantes/mc03.py | MC-03 | Retirar só ('Consulta', 'visualizar') da sequência de concessões de obter_permissoes_diretas |
| variantes/mc04.py | MC-04-v2 | Trocar só o retorno de obter_papeis_efetivos pelos atribuídos, sem expansão |

Preservar tupla unitária válida nas remoções. Diff textual contra B guardado e revisado com responsável/data. Conferência AST assegura igualdade de assinaturas e de todos os nós fora da expressão autorizada; dentro dela, aceitar apenas a remoção/substituição exata. AST audita a edição: não gera variante ou gabarito. Nenhuma revisão encadeada; quatro diffs contra B. Fonte com alteração extra ou revisão pendente não é executada; seus 12 pares ficam não executados por procedência inválida, sem impedir a conferência de outras variantes válidas.

### Snapshot e carregamento

Nova pasta de tentativa, sem sobrescrita, com fontes extraídas de B (módulo/testes/JSON e fundamentos), variantes e executor. Hashes antes/depois; versão de variante = B + ID + SHA-256 da fonte executada, com caminho e identificação do executor. Não requer quatro commits.

Executar com `-B`, snapshot novo sem __pycache__. Suíte original em subprocesso com cwd no snapshot B e seu autorizacao.py. Para matriz, carregar B e variantes por importlib.util.spec_from_file_location, caminhos absolutos e nomes exclusivos por tentativa/variante; conferir module.__file__, loader e hash. Não alterar sys.path ou sys.modules['autorizacao']; não reutilizar módulos entre tentativas. Falha de hash/procedência invalida qualificação.

### B, matriz e registro

1. Validar JSON de B: versão/status, T01–T12 únicos, quatro IDs e mesmos 12 IDs em cada expected; validar chaves/tipos/vocabulário. Não usar tests/changed/preserved como filtro. Confrontar fundamentos documentais; conflito exige investigação, sem fonte escolhida silenciosamente.
2. Executar suíte original no snapshot B: 18 métodos e controles, descoberta não vazia, logs/retorno. Obter ainda os 12 observados iniciais pelo catálogo e comparar catalogo[].esperado na mesma tentativa. São registros de B, separados dos 48. Falha/divergência de B impede qualificação de variantes; manter os 48 não executados por pré-condição inválida.
3. Para cada variante válida, percorrer os 12 itens de catalogo, converter papéis para frozenset e chamar autorizar. Esperado vem de mudancas[id].expected[teste]. Unittest com subTest(mudanca, teste), registro antes da asserção e persistência protegida mesmo em falha. Um erro de par não impede os demais.
4. Comparar dict completo com duas chaves e strings válidas. Retorno válido diferente = divergente; exceção/saída malformada = erro, preservando bruto e sem inventar observado válido. Registrar efeito esperado contra resultado inicial esperado, e efeito observado contra o observado de B da mesma tentativa. T07/MC-04 muda só motivo; T12/MC-03 é executado apesar da exclusão na seleção.
5. Contar 48 chaves distintas, não métodos/subtestes. Resumo distingue conformes/divergentes/erros/não executados. Conformidade integral exige 48 conformes, B/controles conformes, integridade das fontes e registros. Log ausente por falha de escrita invalida fechamento mesmo com unittest OK.

### Divergência e conclusão

Conservar fontes, esperado, observado e logs. Diagnosticar origem/isolamento, entrada/ID/esperado carregados e integridade de referência; depois RF-01, permissões RF-02, expansão RF-03, conflito RF-04 e precedência. Registrar causa confirmada, hipótese ou pendência com evidência por par. Correção futura de implementação requer nova tentativa, sem sobrescrever resultado. Suspeita de erro no gabarito vai à revisão humana em decisões; verificador nunca escreve na referência.

Conformidade com candidata 0.2 é apenas conferência executável. Permanecem P-01 (impacto/desenho e MC-04-v2), P-02 (gabarito/política/notas/prompts/métricas e expectativas T12), P-03 (piloto/repetições/congelamento) e adoção constitucional. T12 já adotado pelo pesquisador; não pedir nova adoção nem atribuir aprovação ao orientador. Sem piloto ou LLM.

## Rastreabilidade e fechamento

| Spec | Cobertura futura |
|---|---|
| FR-001/FR-002; SC-001 | B, quatro cópias, manifesto/diff/AST |
| FR-003/FR-004; SC-002 | Blobs, suíte intacta, referência de B e hashes antes/depois |
| FR-005/FR-006; SC-003/SC-006 | 12 × 4, decisão/motivo sem filtro de seleção |
| FR-007; SC-004 | Registro por par, 48 chaves e tentativas exclusivas |
| FR-008; SC-005 | Diagnóstico pelas regras, referência imutável |
| FR-009/FR-010; SC-007 | Efeitos contra B e conclusão científica separada |

Seleção real: .specify/feature.json → specs/003-mudancas-controladas. check-prerequisites.sh --json --paths-only confirmou FEATURE_SPEC/IMPL_PLAN/FEATURE_DIR antes de setup-plan.sh --json, que copiou template para 003. BRANCH=003-mudancas-controladas é contexto do resolvedor, não branch criada. Setup bloqueado inicialmente pelo sandbox, repetido com autorização técnica. Nenhum teste da bancada executado, só Git/AST de fontes existentes e revisão documental. Próxima etapa: revisar desenho e solicitar tarefas quando desejado.

## Complexity Tracking

Sem exceção constitucional ou infraestrutura adicional. Quatro cópias são proporcionais ao módulo pequeno; alternativas rejeitadas no research.
