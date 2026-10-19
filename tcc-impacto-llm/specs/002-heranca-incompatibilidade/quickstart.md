> Complemento vigente — 19/10/2026, D-15/D-16: T12 adotado pelo pesquisador e acrescentado à suíte da versão inicial; teste isolado OK e 18 métodos integrados OK. Catálogo atual T01–T12, 48 pares e 60 expectativas com a versão inicial, referência ainda candidata. Evidências em `documentacao/evidencias-t12.md` desde a raiz. O conteúdo datado abaixo preserva o escopo e as evidências originais da Spec 002 (T01–T11); menções a T12 como proposta ou fora da aceitação descrevem aquele incremento, superadas por D-15 apenas nesse alcance. Sem variantes, piloto ou LLM experimental; sem aprovação científica atribuída ao orientador.

# Evidências reais — 18/10/2026

Autorização D-13; Python 3.13.3, sem terceiros. Revisão inicial: 7fe549157c71f60347484b4815c7f42869e37016; árvore inicialmente limpa. Alterações desta execução não commitadas.

## T001–T002: preparação

Comandos reais: Get-Content -Encoding UTF8 .specify/feature.json; python --version; git status --short; git rev-parse HEAD. Spec ativa confirmada: specs/002-heranca-incompatibilidade, independentemente da aba do IDE. Governança, materiais pertinentes, Spec/plano/research/modelo/contrato/tasks confrontados com código.

Inventário: dez métodos preservados literalmente: TestEstado.test_T01/test_T09/test_T10/test_T11/test_estados_32_combinacoes; TestDiretas.test_T02/test_T03/test_T04/test_auditoria_visualizar/test_concessoes_proprias. Sete IDs anteriores, 32 combinações não ativas, três concessões próprias e Auditoria/visualizar. Evidência 001 permanece histórica.

Assinaturas preservadas: autorizar(str, frozenset[str], str) -> dict[str, str]; obter_permissoes_diretas(frozenset[str]) -> frozenset[str]. Precondições: ativa/suspensa/em_revisao, subconjuntos de Consulta/Auditoria/Supervisão inclusive vazio, visualizar/exportar; saída exatamente decisao/motivo strings; sem novas guardas de malformados. Domínio inicial ativo parcial, ampliado somente na integração verificada.

Primeira escrita via Python negada por PermissionError; permissão técnica solicitada e concedida. Edições por apply_patch; arquivo temporário de verificação removido. Não foi falha de teste.

## T003–T008: US1

T003/T004: T05/T08 e oito efetivos com expectativas explícitas, tipo frozenset, repetição e entradas intactas.
T005, comando seletivo: python -m unittest discover -s tests -p 'test_*.py' -k TestHeranca -v. Três métodos descobertos: T05 falhou (negar/sem_permissao em vez de permitir/permissao_herdada); T08 passou incidentalmente; oito erros de subteste AttributeError por obter_papeis_efetivos ausente. Sem erro de ambiente/importação. Este é resumo fiel da execução inicial, não transcrição bruta.
T006/T007: união imutável de atribuídos com Consulta por Supervisão, sem recursão; consulta direta intacta; estado primeiro, direta antes de herdada. RF-04 ainda pendente nessa etapa.
T008: python -m unittest discover -s tests -p 'test_*.py' -v: 13 métodos OK; oito efetivos, T05/T08/T10 e dez métodos anteriores conformes. Não demonstrava RF-04.

## T009–T014: US2

T009/T010: T06/T07 e oito expectativas booleanas explícitas de incompatibilidade, sem expansão no predicado, entradas intactas e repetição.
T011: python -m unittest discover -s tests -p 'test_*.py' -k TestConflito -v. Três métodos: duas falhas (T06 permitir/direta; T07 permitir/herdada) e oito AttributeError pela ausência de ha_incompatibilidade. Descoberta não vazia, sem erro de ambiente/importação.
T012/T013: predicado puro Consulta+Auditoria nos efetivos, integrado antes da decisão por permissão.
T014: comando completo de descoberta: 16 métodos OK; oito predicados, T06/T07/T11, US1 e regressão anterior conformes.

## T015–T018: US3

T015: quatro bordas explícitas, ativa sem papéis e Supervisão+Consulta nas duas operações, entradas intactas e repetição; dez métodos anteriores inalterados.
T016: python -m unittest discover -s tests -p 'test_*.py' -k TestBordas -v: um método, quatro subtestes OK; sem correção funcional adicional necessária.
T017: módulo e contrato atualizados para três estados, oito subconjuntos e duas operações, funções puras e cinco motivos.
T018: python -m unittest discover -s tests -p 'test_*.py' -v, após atualização do código. 17 métodos, zero falhas/erros/ignorados. T01–T11 11/11 conforme dicionários completos; sete originais 7/7.
Contagem: dez métodos anteriores + quatro IDs + três auxiliares. 55 subtestes: 32 estado, três concessões, oito efetivos, oito predicados e quatro bordas. Isso não amplia o catálogo experimental.

### Relatório bruto final

```text
test_vazio_e_prioridade_direta (test_autorizacao.TestBordas.test_vazio_e_prioridade_direta) ... ok
test_T06 (test_autorizacao.TestConflito.test_T06) ... ok
test_T07 (test_autorizacao.TestConflito.test_T07) ... ok
test_incompatibilidade_oito_subconjuntos (test_autorizacao.TestConflito.test_incompatibilidade_oito_subconjuntos) ... ok
test_T02 (test_autorizacao.TestDiretas.test_T02) ... ok
test_T03 (test_autorizacao.TestDiretas.test_T03) ... ok
test_T04 (test_autorizacao.TestDiretas.test_T04) ... ok
test_auditoria_visualizar (test_autorizacao.TestDiretas.test_auditoria_visualizar) ... ok
test_concessoes_proprias (test_autorizacao.TestDiretas.test_concessoes_proprias) ... ok
test_T01 (test_autorizacao.TestEstado.test_T01) ... ok
test_T09 (test_autorizacao.TestEstado.test_T09) ... ok
test_T10 (test_autorizacao.TestEstado.test_T10) ... ok
test_T11 (test_autorizacao.TestEstado.test_T11) ... ok
test_estados_32_combinacoes (test_autorizacao.TestEstado.test_estados_32_combinacoes) ... ok
test_T05 (test_autorizacao.TestHeranca.test_T05) ... ok
test_T08 (test_autorizacao.TestHeranca.test_T08) ... ok
test_efetivos_oito_subconjuntos (test_autorizacao.TestHeranca.test_efetivos_oito_subconjuntos) ... ok

----------------------------------------------------------------------
Ran 17 tests in 0.004s

OK
```

## T019–T020: revisão e critérios

git diff -- autorizacao.py tests/test_autorizacao.py e git diff --check executados; exit 0, somente avisos LF/CRLF. Revisão contra Spec/plano/contrato confirmou: atribuídos preservados, única herança de um nível, sem Auditoria herdada; conflito efetivo antes de decidir permissões; estado encerra antes das consultas; direta antes de herdada; ausência por último. Saída exata, consultas imutáveis, funções sem I/O/mutação/política global mutável. Expectativas anteriores preservadas literalmente no diff. Sem T12, variantes ou chamadas externas. Nenhuma lacuna funcional no recorte; não se afirma cobertura exaustiva do domínio.

Patch documental parcialmente aplicado retornou erro de contexto já alterado; releitura confirmou módulo correto e contrato foi concluído separadamente antes de T018. Sem mudança funcional posterior.

| Critério | Evidência |
|---|---|
| SC-001 | T05/T08 2/2 e oito efetivos |
| SC-002 | T06/T07 2/2 e oito predicados |
| SC-003 | Sete anteriores preservados; 11/11 integrados |
| SC-004 | 32 estados, três concessões, Auditoria/visualizar |
| SC-005 | Onze dicionários completos |
| SC-006 | Quatro bordas com repetição e entradas intactas |

## T021–T022: fechamento

Conferência final adicional: comparação AST dos métodos originais contra HEAD confirmou os dez métodos e auxiliar intactos; onze IDs T01–T11 presentes sem T12; git diff --name-only confirmou materiais/gabarito sem alterações. A primeira leitura AST encontrou BOM U+FEFF no arquivo histórico; repetida com utf-8-sig passou. Foi ajuste de leitura da ferramenta de revisão, sem alteração do código. git diff --check final também passou.

Documentação de arquitetura, qualidade, decisões, roadmap, estado, handoff, bloqueios e tarefas reconciliada; status operacional atualizado. Sem contrato/expectativa/gabarito redefinido. T001–T022 têm evidências nas seções acima e nos arquivos alterados.

T12 permanece proposta P-04, não adotada nem executada. Catálogo 11/44 e materiais/gabarito preservados. Sem variantes, piloto, coleta ou LLM experimental. Pendentes: adoção formal da constituição; demais detalhes P-01; revisão humana P-02; condições/repetições/congelamento P-03; decisão P-04; modelo/API/orçamento/isolamento. Engenharia não valida referência científica.

---

O guia abaixo é planejamento histórico de 16/10, superado pelos resultados acima.

# Guia futuro de verificação — Spec 002 (histórico)

Planejamento, não relatório de execução. RF-03/RF-04 ainda não implementados; nenhum teste executado nesta etapa. Não confundir os dez métodos existentes aprovados no incremento 1 com a integração futura.

## Preparação após autorização

Confirmar Python 3.11+ (3.13.3 usado no incremento 1), implementar segundo tarefas futuras e manter organização existente. Sem dependências a instalar. A partir da raiz tcc-impacto-llm, comandos futuros:

```powershell
python --version
python -m unittest discover -s tests -p 'test_*.py' -v
```

Não executar agora. Os arquivos atuais não contêm T05–T08; a suíte antiga sozinha não demonstra conformidade da Spec 002.

## Verificações exigidas

- Integrar T05/T06/T07/T08 aos sete IDs anteriores, comparar os onze dicionários inteiros da [Spec](spec.md); sem mudanças de expectativa ou casos ignorados.
- Conservar 32 subtestes de estado, três concessões próprias com retornos imutáveis/entradas preservadas/repetição e controle Auditoria/visualizar.
- Conferir ativa sem papéis e Supervisão + Consulta nas duas operações: quatro controles auxiliares; mesma resposta em chamadas repetidas e nenhuma mutação.
- Conferir efetivos nos oito subconjuntos com expectativas explícitas e independentes: vazio→vazio; Consulta→Consulta; Auditoria→Auditoria; Supervisão→Supervisão+Consulta; Consulta+Auditoria→mesmo; Consulta+Supervisão→mesmo; Auditoria+Supervisão→três; três→três.
- Conferir predicado de incompatibilidade nos oito subconjuntos já efetivos: verdadeiro somente nos que contêm Consulta e Auditoria. Entrada do auxiliar não é solicitação de autorização e não executa T12.
- Revisar que estado encerra antes de consultas, conflito antes de permissão, direta antes de herdada e ausência somente após considerar herança.

Manter dez métodos existentes e acrescentar quatro para T05–T08; antes dos controles novos, 14 métodos. Registrar contagem final real, separando métodos, cenários e subtestes. Aceitação não depende de uma contagem inventada de métodos.

## Evidências futuras

Registrar versão, data, comandos, revisão/diff, relatório bruto, contagens por categoria e falhas/resolução. Exigir onze IDs descobertos, 11/11 conformes e nenhum erro/falha/ignorado. Atualizar tarefas somente com evidências reais e revisar contrato/documentação antes de fechar.

O teste antes da implementação deve identificar capacidades ausentes ou divergência real, distinguindo erro de ambiente/importação e descoberta vazia. Os testes da integração devem ser executados após implementação; evidência do incremento 1 comprova somente o estado anterior.

## Limites

Não executar matriz completa de autorizar que inclua T12, nem criar seu teste de aceitação. T12 continua proposto fora da suíte; domínio futuro o abrange semanticamente, mas não há adoção do cenário. Nenhuma variante, piloto ou LLM experimental. Catálogo 11/44 e referência original preservados; resultados de engenharia não validam gabarito.

## Registro operacional desta etapa

Spec ativa selecionada em .specify/feature.json. Resolvido antes de gerar: `check-prerequisites.sh --json --paths-only` retornou FEATURE_SPEC e IMPL_PLAN na Spec 002. `setup-plan.sh --json` copiou template no mesmo destino; primeira tentativa negada pelo sandbox, repetição autorizada bem-sucedida. Criação da pasta contracts também exigiu permissão técnica. Nenhum bloqueio funcional identificado ou teste de aplicação executado.
