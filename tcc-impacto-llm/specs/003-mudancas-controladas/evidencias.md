# Evidências de engenharia — Spec 003

21/10/2026. Autorização do pesquisador D-20; execução/revisão pelo assistente, D-21. Conformidade executável com **referência candidata 0.2**; sem aprovação científica, piloto, coleta ou chamada ao LLM. Revisão profissional, possíveis novos modelos e métricas aguardam transcrição e decisão explícita.

## Fontes, preservação e versões

Spec ativa `003-mudancas-controladas`, confirmada por `.specify/scripts/bash/check-prerequisites.sh --json --require-tasks --include-tasks`; checklist de qualidade 23/23 satisfeita. Constituição 1.0.0 ainda sem ratificação. B fixo `aec474bcb54d6dae2afceff8e5b9226991386490`; HEAD inicial/do executor `8041b0b1deca09f13c8b95069699616c7a1a7a60`. Implementação local identificada por estado Git, SHA-256 e snapshots, sem criação de commit/branch. Python **3.13.3**, executável `C:\Program Files\Python313\python.exe`, Windows/PowerShell, biblioteca padrão e Git local, sem instalação.

Sete alterações documentais locais existentes preservadas em [inventário](../../evidencias/spec003/preparacao/inventario.json) e `../../evidencias/spec003/preparacao/alteracoes-locais-iniciais/`. O status do inventário também inclui os primeiros arquivos novos desta implementação, já criados no instante da captura. Revisões anteriores e evidências T12 não foram apagadas. Arquivos de código/testes/referência de B permanecem sem diff. Materiais são conferidos por hashes antes/depois; textos da candidata em B continuam datados do momento da preparação, com observações posteriores somente nestes relatórios.

| Fonte de B | Blob Git |
|---|---|
| autorizacao.py | c219b9ab1f2ed75a92664c79009a1a417e75ef11 |
| tests/test_autorizacao.py | e2d9c09a43268abc96a5b7e93095f22e023266f4 |
| JSON candidato 0.2 | 9533e7dfa053af0f73449de8a42747e81949c53d |

## Alteração única e procedência

Quatro leituras independentes de B, registradas pela operação [preparar.py](../../evidencias/spec003/desenvolvimento/preparar.py). O executor somente lê fontes já preparadas; não gera variantes ou esperados. Diffs textuais lidos pelo assistente e aprovados para engenharia em 21/10/2026, com conferência AST fora/dentro da expressão permitida, assinatura e demais nós preservados. Docstrings de B são mantidas para atender à restrição de edição mínima.

| Variante | Única alteração | SHA-256 executado | Diff final |
|---|---|---|---|
| MC-01 | Retirar Auditoria → exportar de RF-02 | a4cb55e710cda2ddf29b46128f2494d1100e16dbbd3590b99f753f58f5609895 | [MC-01.diff](../../evidencias/spec003/rodada-final/diffs/MC-01.diff) |
| MC-02 | Retorno de ha_incompatibilidade = False (RF-04) | c267731ef32d2024e7b420f23ede111c2eedb0304e2bb8e22fbdd932f7fe2baf | [MC-02.diff](../../evidencias/spec003/rodada-final/diffs/MC-02.diff) |
| MC-03 | Retirar Consulta → visualizar de RF-02 | b82c2013267ef826a5a403753b49a9cea20b5e1b8f3dcbe4eb6b251868eb411c | [MC-03.diff](../../evidencias/spec003/rodada-final/diffs/MC-03.diff) |
| MC-04-v2 | RF-03 retorna somente papéis atribuídos, sem expansão | bf98ddb5dd67c2c189c810e51fc592d8ff4cb8c62d04c75edecf00b574c1a1e4 | [MC-04-v2.diff](../../evidencias/spec003/rodada-final/diffs/MC-04-v2.diff) |

[Metadados/revisão](../../variantes/procedencia.json), [auditoria inicial](../../evidencias/spec003/procedencia/manifesto.json), [revisão posterior aos diffs](../../evidencias/spec003/procedencia/revisao.json). MC-04 é rótulo curto; JSON permanece MC-04-v2. Não há alterações acumuladas nem importação entre variantes. Baseline executada em subprocesso isolado; matriz carrega caminhos absolutos e nomes exclusivos, sem alterar sys.modules['autorizacao'] ou sys.path. Fontes executadas têm snapshot e hashes antes/depois/no fechamento, com -B e sem cache.

## Resultados reais da bancada

| Rodada | Finalidade | Suíte B | Pares B | Pares variantes | Divergências/erros/ausentes |
|---|---|---|---|---|---|
| integracao-us2 | T024, antes da CLI/diagnóstico finais | 18 métodos OK | 12/12 | 48/48 conformes | 0/0/0 |
| rodada-final | T032, integração final de CLI, diagnóstico e integridade | 18 métodos OK | 12/12 | 48/48 conformes | 0/0/0 |

São **48 pares distintos por rodada**, não 96 cenários distintos nem controles sintéticos. As duas tentativas permanecem separadas, e a final não apaga a primeira. Testes selecionados 2/4/8/5 não filtram execução. T07/MC-04-v2 observou negar/sem_permissao, mudança somente de motivo. T12 observou negar/conflito em MC-01/MC-03 e permitir/permissao_direta em MC-02/MC-04-v2. T12/MC-03 foi executado mesmo excluído da seleção.

Comando final, cwd `D:\TCC-Projeto\TCC\tcc-impacto-llm`:

```powershell
python -B verificacao_variantes.py --saida evidencias/spec003/rodada-final
```

Código **0**. Snapshot de B: `python -B -m unittest discover -s tests -p test_autorizacao.py -v`, 18 métodos, zero falhas/erros/ignorados; doze observados iniciais adicionais registrados separadamente. Matriz unittest contém um método com 48 subtestes; contagem dos pares vem das 48 chaves mudança/teste, não de “Ran 1 test”.

- [Comando final, retorno e stdout/stderr originais](../../evidencias/spec003/rodada-final-comando/comando.json), em arquivos irmãos `stdout.txt`/`stderr.txt`.
- [Manifesto final](../../evidencias/spec003/rodada-final/manifesto.json): comando/cwd/Python, HEAD/estado, objetos/hashes, fontes, auditorias, resumo e conclusão restrita.
- [Resultados por par](../../evidencias/spec003/rodada-final/resultados.json) e [originais anteriores ao diagnóstico](../../evidencias/spec003/rodada-final/resultados-originais.json): entrada, fonte/versão efetivamente executada, referência/chave, esperado, observado, conformidade, efeitos e evidência.
- [Tabela dos 48 pares](../../evidencias/spec003/rodada-final/relatorio.md), [suíte B original](../../evidencias/spec003/rodada-final/baseline-unittest.txt), [log matriz](../../evidencias/spec003/rodada-final/variantes-unittest.txt) e `baseline-pares.jsonl`.
- [Primeira integração](../../evidencias/spec003/integracao-us2/manifesto.json), [resultados](../../evidencias/spec003/integracao-us2/resultados.json) e [comando de integração dos componentes](../../evidencias/spec003/integracao-us2-comando/comando.json).

## Controles sintéticos e desvio corrigido

Executados em processo separado: `python -B -m unittest discover -s tests -p test_variantes.py -v`. **17 métodos finais OK**, além de subcasos de falha; nenhum entra nos 48 pares reais. Respostas controladas/mocks aparecem somente nesses testes, identificados como sintéticos, usando diretórios temporários. A matriz real chama as quatro funções reais sem mocks.

Registros por fase, com comando/retorno, stdout/stderr originais e snapshot do código/teste no checkpoint:

| Fase | Falha inicial preservada | Verificação posterior |
|---|---|---|
| Fundação | sintetico-fundacao-red: módulo inexistente | sintetico-fundacao-green: 4 métodos OK |
| Procedência | sintetico-procedencia-red: auditor/loader inexistentes | sintetico-procedencia-green: 6 métodos OK |
| Matriz | sintetico-matriz-red: comparação/matriz inexistentes | sintetico-matriz-green: 11 métodos OK |
| Interface/diagnóstico | sintetico-interface-red: funções finais inexistentes | sintetico-interface-green: 15 métodos OK |
| Integridade no fechamento | sintetico-integridade-final-red: 2 falhas reproduzidas | [sintetico-final-green](../../evidencias/spec003/sintetico-final-green/comando.json): 17 métodos OK |

Todos os caminhos da tabela estão sob `evidencias/spec003/`, sem sobrescrita. Cobrem commit ausente, IDs inválidos/duplicados, expected incompleto, diretório repetido/perigoso, edição extra/encadeada, assinatura alterada, caminho/hash/cache, mudança apenas de motivo, saída inválida/exceção, fonte inválida sem bloquear as outras, B inválida bloqueando as 48, interrupção e persistência, código 2 prioritário, falha de escrita, tentativa nova vinculada à anterior e campos de diagnóstico.

**M-01 — causa confirmada no mecanismo de fechamento.** Inspeção revelou que arquivos/fontes eram conferidos ao término da execução, mas não novamente ao consolidar. Controles removeram um log e alteraram uma fonte em cópias temporárias: o fechamento retornava 0 indevidamente. Originais em [stderr red](../../evidencias/spec003/sintetico-integridade-final-red/stderr.txt), com os dois `AssertionError: 0 != 2`. Correção em `finalize_attempt`: revalidar hashes/arquivos, registrar falha de integridade e retornar 2. Os dois controles e a suíte completa passaram depois; rodada real final posterior com arquivos íntegros. Nenhum esperado foi ajustado; não foi erro de requisito nem da candidata.

**Bancada real: zero divergências e zero erros**, logo não há investigação de expectativa a inventar, correção funcional nas variantes ou decisão humana bloqueante. Suspeitas futuras devem conservar os originais e seguir RFs/precedência/origem/entrada/referência, com decisão humana separada antes de mudar o gabarito. Uma nova tentativa deve usar pasta/ID novos; não sobrescrever resultado anterior.

## Tarefas e critérios

| Tarefas concluídas | Evidência |
|---|---|
| T001–T002 | Inventário, seleção/checklist, B/blobs e cópias das sete alterações locais |
| T003–T008 | Checkpoints sintéticos fundação, extração/validação/registros e código snapshot |
| T009–T017 | Checkpoints procedência, quatro fontes, diffs/AST/revisão/metadados |
| T018–T025 | Checkpoints matriz, primeira integração real, 60 registros separados e hashes |
| T026–T029 | Interface/diagnóstico/integridade: checkpoints red/green, casos 0/1/2 e preservação |
| T030–T031 | Zero divergências reais, ausência de suspeita de gabarito; M-01 investigado/corrigido com evidências |
| T032–T033 | Rodada final, conferência de logs/snapshots/hashes e dos 48 pares distintos |
| T034–T035 | Estado, Spec/plano/checklist/quickstart, decisões, governança, handoff, bloqueios e documentação reconciliados |

FR-001/FR-002 e SC-001: origem/edição única; FR-003/FR-004 e SC-002: B e referência preservadas; FR-005–FR-007 e SC-003/SC-004: 48 pares completos e procedência; FR-008 e SC-005: investigação preservada, zero divergência real; FR-009 e SC-006: efeitos esperados/observados e motivo T07 distintos; FR-010 e SC-007: aprovação científica separada. **35/35 tarefas concluídas; nenhuma pendência funcional identificada.**

P-01/P-02/P-03, revisão científica das expectativas T12 e adoção constitucional continuam pendentes. Etapa 3 entregue no alcance de engenharia; referência/política/MC-04-v2 não recebem aprovação científica pela concordância com código. T12 já adotado na baseline. Revisão profissional, novos modelos e métricas não viraram decisões aprovadas. Sem coletor/avaliador de LLM, piloto ou liberação experimental.
