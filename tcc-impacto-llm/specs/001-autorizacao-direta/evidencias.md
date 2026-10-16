# Evidências da Spec 001 — 16/10/2026

Ambiente: Windows/PowerShell, `python --version` → Python 3.13.3; `py --list` → Python 3.13 64-bit. Sem instalações. Comandos na raiz tcc-impacto-llm.

1. `python -m unittest discover -s tests -p 'test_*.py' -k TestEstado -v` antes: 5 métodos, 36 erros AttributeError por ausência de autorizar (4 casos + 32 subtestes). Interface ausente, sem comparação funcional; não erro de ambiente/sintaxe. Saída inicial truncada na ferramenta; este resumo não é relatório bruto integral.
2. Mesmo comando após RF-01: 5 métodos, OK.
3. `python -m unittest discover -s tests -p 'test_*.py' -k TestDiretas -v` antes de RF-02: 5 métodos, quatro falhas (None em vez de dicionário), três erros em subtestes por ausência de obter_permissoes_diretas.
4. `python -m unittest discover -s tests -p 'test_*.py' -v` integrada: 10 métodos, OK, zero falhas/erros/ignorados.

Contagens: sete casos T01/T02/T03/T04/T09/T10/T11; SC-001 5/5, SC-002 2/2, SC-004 7/7. Um controle Auditoria/visualizar. Um método com três subtestes de concessões (SC-003 3/3, imutabilidade, entradas preservadas, repetição). Um método com 32 subtestes de estado (2 × 8 × 2). Subtestes não são métodos adicionais ou novos IDs experimentais.

Revisão T014/T015: arquivos locais autorizacao.py e tests/test_autorizacao.py, sem commit criado; leitura integral confrontada com Spec/plano/contrato. Chaves/motivos exatos, estado antes de consultar permissões, funções sem I/O/mutação, concessões imutáveis, domínio parcial explícito. Nenhuma contradição funcional, alteração de contrato ou RF-03/RF-04 implementado. T05–T08/T12 não executados. Usados Get-Content, git diff --check, git status --short e git diff --stat; nova revisão documental ao fechamento.

Preparação: primeira tentativa de registrar decisão/redirecionar saída por PowerShell recebeu acesso negado; teste redirecionado não iniciou. Escritas posteriores por apply_patch, testes sem redirecionamento. Não contabilizado como falha funcional. Acentos nas saídas refletem o terminal. Nenhum piloto ou chamada LLM experimental.

## US1 após RF-01

```text
test_T01 (test_autorizacao.TestEstado.test_T01) ... ok
test_T09 (test_autorizacao.TestEstado.test_T09) ... ok
test_T10 (test_autorizacao.TestEstado.test_T10) ... ok
test_T11 (test_autorizacao.TestEstado.test_T11) ... ok
test_estados_32_combinacoes (test_autorizacao.TestEstado.test_estados_32_combinacoes) ... ok

----------------------------------------------------------------------
Ran 5 tests in 0.002s

OK
```

## US2 antes de RF-02

```text
test_T02 (test_autorizacao.TestDiretas.test_T02) ... FAIL
test_T03 (test_autorizacao.TestDiretas.test_T03) ... FAIL
test_T04 (test_autorizacao.TestDiretas.test_T04) ... FAIL
test_auditoria_visualizar (test_autorizacao.TestDiretas.test_auditoria_visualizar) ... FAIL
test_concessoes_proprias (test_autorizacao.TestDiretas.test_concessoes_proprias) ...
  test_concessoes_proprias (test_autorizacao.TestDiretas.test_concessoes_proprias) (papel='Consulta') ... ERROR
  test_concessoes_proprias (test_autorizacao.TestDiretas.test_concessoes_proprias) (papel='Auditoria') ... ERROR
  test_concessoes_proprias (test_autorizacao.TestDiretas.test_concessoes_proprias) (papel='Supervis�o') ... ERROR

======================================================================
ERROR: test_concessoes_proprias (test_autorizacao.TestDiretas.test_concessoes_proprias) (papel='Consulta')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\TCC-Projeto\TCC\tcc-impacto-llm\tests\test_autorizacao.py", line 61, in test_concessoes_proprias
    resultado = autorizacao.obter_permissoes_diretas(papeis)
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AttributeError: module 'autorizacao' has no attribute 'obter_permissoes_diretas'

======================================================================
ERROR: test_concessoes_proprias (test_autorizacao.TestDiretas.test_concessoes_proprias) (papel='Auditoria')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\TCC-Projeto\TCC\tcc-impacto-llm\tests\test_autorizacao.py", line 61, in test_concessoes_proprias
    resultado = autorizacao.obter_permissoes_diretas(papeis)
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AttributeError: module 'autorizacao' has no attribute 'obter_permissoes_diretas'

======================================================================
ERROR: test_concessoes_proprias (test_autorizacao.TestDiretas.test_concessoes_proprias) (papel='Supervis�o')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\TCC-Projeto\TCC\tcc-impacto-llm\tests\test_autorizacao.py", line 61, in test_concessoes_proprias
    resultado = autorizacao.obter_permissoes_diretas(papeis)
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AttributeError: module 'autorizacao' has no attribute 'obter_permissoes_diretas'

======================================================================
FAIL: test_T02 (test_autorizacao.TestDiretas.test_T02)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\TCC-Projeto\TCC\tcc-impacto-llm\tests\test_autorizacao.py", line 39, in test_T02
    self.assertEqual(autorizacao.autorizar('ativa', frozenset({'Consulta'}), 'visualizar'),
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                     {'decisao': 'permitir', 'motivo': 'permissao_direta'})
                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: None != {'decisao': 'permitir', 'motivo': 'permissao_direta'}

======================================================================
FAIL: test_T03 (test_autorizacao.TestDiretas.test_T03)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\TCC-Projeto\TCC\tcc-impacto-llm\tests\test_autorizacao.py", line 43, in test_T03
    self.assertEqual(autorizacao.autorizar('ativa', frozenset({'Consulta'}), 'exportar'),
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                     {'decisao': 'negar', 'motivo': 'sem_permissao'})
                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: None != {'decisao': 'negar', 'motivo': 'sem_permissao'}

======================================================================
FAIL: test_T04 (test_autorizacao.TestDiretas.test_T04)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\TCC-Projeto\TCC\tcc-impacto-llm\tests\test_autorizacao.py", line 47, in test_T04
    self.assertEqual(autorizacao.autorizar('ativa', frozenset({'Auditoria'}), 'exportar'),
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                     {'decisao': 'permitir', 'motivo': 'permissao_direta'})
                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: None != {'decisao': 'permitir', 'motivo': 'permissao_direta'}

======================================================================
FAIL: test_auditoria_visualizar (test_autorizacao.TestDiretas.test_auditoria_visualizar)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\TCC-Projeto\TCC\tcc-impacto-llm\tests\test_autorizacao.py", line 51, in test_auditoria_visualizar
    self.assertEqual(autorizacao.autorizar('ativa', frozenset({'Auditoria'}), 'visualizar'),
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                     {'decisao': 'negar', 'motivo': 'sem_permissao'})
                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: None != {'decisao': 'negar', 'motivo': 'sem_permissao'}

----------------------------------------------------------------------
Ran 5 tests in 0.006s

FAILED (failures=4, errors=3)
```

## Integrada

```text
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

----------------------------------------------------------------------
Ran 10 tests in 0.004s

OK
```
