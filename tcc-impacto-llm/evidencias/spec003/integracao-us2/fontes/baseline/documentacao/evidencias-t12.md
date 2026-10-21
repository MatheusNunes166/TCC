# Evidências da adoção de T12 — 19/10/2026

Autorização: D-15 em [decisões](decisoes.md), pesquisador, pedido explícito nesta conversa. Execução técnica: assistente. Python 3.13.3 + unittest, sem terceiros. Somente a versão inicial foi executada; variantes, piloto e LLM experimental não foram iniciados. Adoção pelo pesquisador não equivale a aprovação científica do orientador.

## Expectativa e rastreabilidade

Entrada: `ativa`, `frozenset({'Supervisão', 'Auditoria'})`, `exportar`. Esperado: `{'decisao': 'negar', 'motivo': 'conflito'}`.

RF-01 permite prosseguir. RF-02 concede exportar diretamente por Auditoria. RF-03 inclui Consulta efetivo por Supervisão. RF-04 bloqueia Consulta + Auditoria efetivos antes de decidir pela concessão. A expectativa foi estabelecida pelos requisitos e confirmada pela execução, sem alterar `autorizacao.py`.

Foi acrescentado somente `TestConflito.test_T12` à suíte anterior, com comparação do dicionário completo. T01–T11 e os seis métodos auxiliares anteriores permanecem iguais. Permanecem os 55 subtestes de controle (32 estados, três concessões próprias, oito conjuntos efetivos, oito predicados de incompatibilidade e quatro bordas), além do controle Auditoria/visualizar. O catálogo contém 12 casos, enquanto a suíte integrada contém 18 métodos.

## Comandos e saída real

Diretório: raiz de `tcc-impacto-llm`. Comandos executados sequencialmente; ambos os testes terminaram em OK:

```text
python --version
Python 3.13.3

python -m unittest discover -s tests -p test_autorizacao.py -k test_T12 -v
test_T12 (test_autorizacao.TestConflito.test_T12) ... ok

----------------------------------------------------------------------
Ran 1 test in 0.001s

OK

python -m unittest discover -s tests -v
test_vazio_e_prioridade_direta (test_autorizacao.TestBordas.test_vazio_e_prioridade_direta) ... ok
test_T06 (test_autorizacao.TestConflito.test_T06) ... ok
test_T07 (test_autorizacao.TestConflito.test_T07) ... ok
test_T12 (test_autorizacao.TestConflito.test_T12) ... ok
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
Ran 18 tests in 0.005s

OK
```

Resultado: T12 isolado aprovado; suíte integrada aprovada, sem falhas, erros ou ignorados. Nenhuma divergência em relação a negar/conflito; nenhuma regra ou expectativa anterior precisou mudar.

## Conferência documental e limites

Referência 0.2 continua `CANDIDATO_NAO_REVISADO`, com revisor/data nulos. O JSON passa a registrar as 12 entradas/saídas da versão inicial e as 48 expectativas das mudanças, além dos conjuntos. Foram conferidos catálogo, partições de mudança/preservação, seleção estrutural e correspondência entre tabelas e JSON: 2/4/8/5 testes relevantes, 48 pares e 60 expectativas no total. Isso não é execução de variantes nem validação científica.

Conferência executada por script transitório local (`python conferir_t12.py`, removido após uso), sem executar variantes. Comparou tabelas/JSON, conjuntos pela política estrutural, 44 células anteriores, partições, hashes históricos e notas. Comparou a árvore sintática dos métodos anteriores com `git show HEAD:./tests/test_autorizacao.py`, e o núcleo com a versão Git: nenhum método anterior ou regra alterado. Saída real:

```text
OK: 12 casos; 48 pares; 60 expectativas; selecoes 2/4/8/5; tabelas/JSON/politica consistentes.
OK: 15 copias historicas e hashes; 44 expectativas anteriores, RFs, metodos e controles preservados.
OK: notas intactas; bloco comum sem IDs/gabarito; regras e schema inalterados; manifesto nao congelado.
```

`git diff --check` concluído sem erros de whitespace; somente avisos de normalização LF/CRLF do Git no Windows. Essas verificações são de integridade documental e preservação, não revisão científica das expectativas.

O schema de saída contém listas de strings, sem enumeração ou restrição que exclua T12; permanece igual para que IDs inexistentes continuem pontuáveis como excedentes. Não há coletor, parser ou avaliador implementado a alterar. O manifesto continua `NAO_CONGELADO`; a adoção do catálogo não preenche aprovação científica nem versões futuras.

O bloco comum de [impacto e relevância](../materiais/07_DEFINICOES_COMUNS.md) é obrigatório e igual para D0/D1/E0/E1. Não contém conjuntos esperados ou exemplos resolvidos; as notas foram preservadas literalmente. A inspeção documental não demonstra isolamento de payloads futuros, que permanece pendente.

Histórico: [cópias pré-T12](historico/pre-t12-2026-10-19/LEIA_PRIMEIRO.md) de 15 artefatos, incluindo o JSON 0.1, preservadas literalmente com manifesto SHA-256. Evidências anteriores das Specs continuam datadas e não foram reescritas. A execução documental encontrou bloqueio de escrita no sandbox; criação de histórico e atualização local foram repetidas com autorização técnica. Duas verificações do script de atualização exigiram correção (trecho já atualizado e cabeçalho interpretado como linha de catálogo); não foram falhas da bancada e não alteraram expectativas. O script transitório foi removido após a conferência.
