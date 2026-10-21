# Verificação local — rodada-final

Origem: `aec474bcb54d6dae2afceff8e5b9226991386490`. Python: `3.13.3 (tags/v3.13.3:6280bb5, Apr  8 2025, 14:47:33) [MSC v.1943 64 bit (AMD64)]`.
Código de saída: 0. Integridade: True.
Referência candidata 0.2; sem aprovação científica ou liberação de piloto.

Baseline: 12/12 pares conformes.
Suíte original: {'comando': ['C:\\Program Files\\Python313\\python.exe', '-B', '-m', 'unittest', 'discover', '-s', 'tests', '-p', 'test_autorizacao.py', '-v'], 'cwd': 'D:\\TCC-Projeto\\TCC\\tcc-impacto-llm\\evidencias\\spec003\\rodada-final\\fontes\\baseline', 'retorno': 0, 'metodos_descobertos': 18, 'metodos_fonte': 18, 'conforme': True, 'stdout': 'baseline-stdout.txt', 'stderr': 'baseline-stderr.txt', 'log': 'baseline-unittest.txt'}.
Variantes: {'conformes': 48, 'divergentes': 0, 'erros': 0, 'nao_executados': 0, 'previstos': 48, 'tentados': 48, 'comparados': 48}.

| Mudança | Teste | Esperado | Observado | Estado |
|---|---|---|---|---|
| MC-01 | T01 | {"decisao": "negar", "motivo": "estado"} | {"decisao": "negar", "motivo": "estado"} | conforme |
| MC-01 | T02 | {"decisao": "permitir", "motivo": "permissao_direta"} | {"decisao": "permitir", "motivo": "permissao_direta"} | conforme |
| MC-01 | T03 | {"decisao": "negar", "motivo": "sem_permissao"} | {"decisao": "negar", "motivo": "sem_permissao"} | conforme |
| MC-01 | T04 | {"decisao": "negar", "motivo": "sem_permissao"} | {"decisao": "negar", "motivo": "sem_permissao"} | conforme |
| MC-01 | T05 | {"decisao": "permitir", "motivo": "permissao_herdada"} | {"decisao": "permitir", "motivo": "permissao_herdada"} | conforme |
| MC-01 | T06 | {"decisao": "negar", "motivo": "conflito"} | {"decisao": "negar", "motivo": "conflito"} | conforme |
| MC-01 | T07 | {"decisao": "negar", "motivo": "conflito"} | {"decisao": "negar", "motivo": "conflito"} | conforme |
| MC-01 | T08 | {"decisao": "negar", "motivo": "sem_permissao"} | {"decisao": "negar", "motivo": "sem_permissao"} | conforme |
| MC-01 | T09 | {"decisao": "negar", "motivo": "estado"} | {"decisao": "negar", "motivo": "estado"} | conforme |
| MC-01 | T10 | {"decisao": "negar", "motivo": "estado"} | {"decisao": "negar", "motivo": "estado"} | conforme |
| MC-01 | T11 | {"decisao": "negar", "motivo": "estado"} | {"decisao": "negar", "motivo": "estado"} | conforme |
| MC-01 | T12 | {"decisao": "negar", "motivo": "conflito"} | {"decisao": "negar", "motivo": "conflito"} | conforme |
| MC-02 | T01 | {"decisao": "negar", "motivo": "estado"} | {"decisao": "negar", "motivo": "estado"} | conforme |
| MC-02 | T02 | {"decisao": "permitir", "motivo": "permissao_direta"} | {"decisao": "permitir", "motivo": "permissao_direta"} | conforme |
| MC-02 | T03 | {"decisao": "negar", "motivo": "sem_permissao"} | {"decisao": "negar", "motivo": "sem_permissao"} | conforme |
| MC-02 | T04 | {"decisao": "permitir", "motivo": "permissao_direta"} | {"decisao": "permitir", "motivo": "permissao_direta"} | conforme |
| MC-02 | T05 | {"decisao": "permitir", "motivo": "permissao_herdada"} | {"decisao": "permitir", "motivo": "permissao_herdada"} | conforme |
| MC-02 | T06 | {"decisao": "permitir", "motivo": "permissao_direta"} | {"decisao": "permitir", "motivo": "permissao_direta"} | conforme |
| MC-02 | T07 | {"decisao": "permitir", "motivo": "permissao_herdada"} | {"decisao": "permitir", "motivo": "permissao_herdada"} | conforme |
| MC-02 | T08 | {"decisao": "negar", "motivo": "sem_permissao"} | {"decisao": "negar", "motivo": "sem_permissao"} | conforme |
| MC-02 | T09 | {"decisao": "negar", "motivo": "estado"} | {"decisao": "negar", "motivo": "estado"} | conforme |
| MC-02 | T10 | {"decisao": "negar", "motivo": "estado"} | {"decisao": "negar", "motivo": "estado"} | conforme |
| MC-02 | T11 | {"decisao": "negar", "motivo": "estado"} | {"decisao": "negar", "motivo": "estado"} | conforme |
| MC-02 | T12 | {"decisao": "permitir", "motivo": "permissao_direta"} | {"decisao": "permitir", "motivo": "permissao_direta"} | conforme |
| MC-03 | T01 | {"decisao": "negar", "motivo": "estado"} | {"decisao": "negar", "motivo": "estado"} | conforme |
| MC-03 | T02 | {"decisao": "negar", "motivo": "sem_permissao"} | {"decisao": "negar", "motivo": "sem_permissao"} | conforme |
| MC-03 | T03 | {"decisao": "negar", "motivo": "sem_permissao"} | {"decisao": "negar", "motivo": "sem_permissao"} | conforme |
| MC-03 | T04 | {"decisao": "permitir", "motivo": "permissao_direta"} | {"decisao": "permitir", "motivo": "permissao_direta"} | conforme |
| MC-03 | T05 | {"decisao": "negar", "motivo": "sem_permissao"} | {"decisao": "negar", "motivo": "sem_permissao"} | conforme |
| MC-03 | T06 | {"decisao": "negar", "motivo": "conflito"} | {"decisao": "negar", "motivo": "conflito"} | conforme |
| MC-03 | T07 | {"decisao": "negar", "motivo": "conflito"} | {"decisao": "negar", "motivo": "conflito"} | conforme |
| MC-03 | T08 | {"decisao": "negar", "motivo": "sem_permissao"} | {"decisao": "negar", "motivo": "sem_permissao"} | conforme |
| MC-03 | T09 | {"decisao": "negar", "motivo": "estado"} | {"decisao": "negar", "motivo": "estado"} | conforme |
| MC-03 | T10 | {"decisao": "negar", "motivo": "estado"} | {"decisao": "negar", "motivo": "estado"} | conforme |
| MC-03 | T11 | {"decisao": "negar", "motivo": "estado"} | {"decisao": "negar", "motivo": "estado"} | conforme |
| MC-03 | T12 | {"decisao": "negar", "motivo": "conflito"} | {"decisao": "negar", "motivo": "conflito"} | conforme |
| MC-04-v2 | T01 | {"decisao": "negar", "motivo": "estado"} | {"decisao": "negar", "motivo": "estado"} | conforme |
| MC-04-v2 | T02 | {"decisao": "permitir", "motivo": "permissao_direta"} | {"decisao": "permitir", "motivo": "permissao_direta"} | conforme |
| MC-04-v2 | T03 | {"decisao": "negar", "motivo": "sem_permissao"} | {"decisao": "negar", "motivo": "sem_permissao"} | conforme |
| MC-04-v2 | T04 | {"decisao": "permitir", "motivo": "permissao_direta"} | {"decisao": "permitir", "motivo": "permissao_direta"} | conforme |
| MC-04-v2 | T05 | {"decisao": "negar", "motivo": "sem_permissao"} | {"decisao": "negar", "motivo": "sem_permissao"} | conforme |
| MC-04-v2 | T06 | {"decisao": "negar", "motivo": "conflito"} | {"decisao": "negar", "motivo": "conflito"} | conforme |
| MC-04-v2 | T07 | {"decisao": "negar", "motivo": "sem_permissao"} | {"decisao": "negar", "motivo": "sem_permissao"} | conforme |
| MC-04-v2 | T08 | {"decisao": "negar", "motivo": "sem_permissao"} | {"decisao": "negar", "motivo": "sem_permissao"} | conforme |
| MC-04-v2 | T09 | {"decisao": "negar", "motivo": "estado"} | {"decisao": "negar", "motivo": "estado"} | conforme |
| MC-04-v2 | T10 | {"decisao": "negar", "motivo": "estado"} | {"decisao": "negar", "motivo": "estado"} | conforme |
| MC-04-v2 | T11 | {"decisao": "negar", "motivo": "estado"} | {"decisao": "negar", "motivo": "estado"} | conforme |
| MC-04-v2 | T12 | {"decisao": "permitir", "motivo": "permissao_direta"} | {"decisao": "permitir", "motivo": "permissao_direta"} | conforme |

Ocorrências para investigar: 0.
Resultados originais preservados; controles sintéticos não integram esta matriz.
