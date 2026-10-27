# Roteiro de demonstração — Spec 003

Preparado em 27/10/2026. Duração sugerida: 5–7 minutos. Fonte técnica: [fechamento e evidências](../specs/003-mudancas-controladas/evidencias.md). Atende aos [encaminhamentos da orientação](encaminhamentos-orientacao-21-10-2026.md), usando terminal e arquivos do mesmo repositório. Não foi executada nova rodada para preparar este roteiro.

## 1. Contexto e sistema — 1 minuto

“O estudo pretende comparar a seleção de IDs de requisitos impactados e testes relevantes conforme a organização do pedido e a presença de notas. O objeto de estudo é uma bancada fictícia de autorização. Ela recebe estado da conta, papéis e operação e devolve `decisao` e `motivo`. A bancada torna os efeitos das mudanças observáveis; a avaliação futura das respostas do LLM é uma camada separada.”

Abrir [requisitos](requisitos.md) e o snapshot [autorizacao.py](../evidencias/spec003/rodada-final/fontes/baseline/autorizacao.py). Explicar os quatro requisitos:

| ID | Comportamento da base |
|---|---|
| RF-01 | Somente conta ativa prossegue; suspensa/em revisão nega por estado. |
| RF-02 | Consulta concede visualizar, Auditoria concede exportar; Supervisão não tem concessão própria. |
| RF-03 | Supervisão inclui Consulta e herda visualizar, em um nível. |
| RF-04 | Consulta + Auditoria efetivos geram conflito, inclusive por herança. |

Precedência: estado → conflito → decisão pela permissão; concessão direta precede herdada. Mostrar o catálogo T01–T12 em [qualidade e testes](qualidade-e-testes.md). B comum: `aec474bcb54d6dae2afceff8e5b9226991386490`. Cada mudança parte de B, sem acumular alterações.

## 2. MC-01 — 1–2 minutos

“Retiramos somente Auditoria → exportar de RF-02.” Abrir [MC-01.diff](../evidencias/spec003/rodada-final/diffs/MC-01.diff): a tupla `('Auditoria', 'exportar')` foi removida; a concessão de Consulta permanece.

| Caso e entrada preservada | Saída inicial observada | Saída observada em MC-01 | Explicação |
|---|---|---|---|
| T04: ativa, Auditoria, exportar | permitir / permissao_direta | negar / sem_permissao | Retirada da concessão direta. |
| T12: ativa, Supervisão + Auditoria, exportar | negar / conflito | negar / conflito | Herança e conflito continuam; a saída é preservada pela precedência. |

Os conjuntos candidatos de seleção MC-01 incluem T04/T12. Isso ilustra por que relevância não se limita a saídas alteradas; a política de seleção ainda depende de revisão científica.

## 3. MC-04 — 1–2 minutos

“Agora voltamos à mesma B e retiramos somente Supervisão → Consulta de RF-03.” MC-04 é abreviação de **MC-04-v2**; não é a antiga proposta sobre contas em revisão. Abrir [MC-04-v2.diff](../evidencias/spec003/rodada-final/diffs/MC-04-v2.diff): `obter_papeis_efetivos` passa a retornar apenas os papéis atribuídos.

| Caso e entrada preservada | Saída inicial observada | Saída observada em MC-04-v2 | Explicação |
|---|---|---|---|
| T05: ativa, Supervisão, visualizar | permitir / permissao_herdada | negar / sem_permissao | Acesso herdado deixa de existir. |
| T07: ativa, Supervisão + Auditoria, visualizar | negar / conflito | negar / sem_permissao | Decisão igual, motivo diferente; comparar apenas permitir/negar perderia o efeito. |
| T12: ativa, Supervisão + Auditoria, exportar | negar / conflito | permitir / permissao_direta | Consulta deixa de surgir pela herança; desaparece o conflito, preservando exportar de Auditoria. |

## 4. Consultar a evidência — 1 minuto

Todos os comandos abaixo são de leitura, em PowerShell, com diretório de trabalho `D:\TCC-Projeto\TCC\tcc-impacto-llm`. Não exigem instalar nada nem chamar LLM.

```powershell
Get-Content -Encoding utf8 specs/003-mudancas-controladas/evidencias.md
Get-Content -Encoding utf8 evidencias/spec003/rodada-final/diffs/MC-01.diff
Get-Content -Encoding utf8 evidencias/spec003/rodada-final/diffs/MC-04-v2.diff
$rodada = Get-Content -Raw -Encoding utf8 evidencias/spec003/rodada-final/resultados-originais.json | ConvertFrom-Json
$rodada.baseline | Where-Object { $_.teste -in @('T04','T05','T07','T12') } | Select-Object teste,entrada,observado | ConvertTo-Json -Depth 8
$rodada.variantes | Where-Object { ($_.mudanca -eq 'MC-01' -and $_.teste -in @('T04','T12')) -or ($_.mudanca -eq 'MC-04-v2' -and $_.teste -in @('T05','T07','T12')) } | Select-Object mudanca,teste,entrada,esperado,observado,estado,versao_executada | ConvertTo-Json -Depth 8
Get-Content -Encoding utf8 evidencias/spec003/rodada-final/relatorio.md
Get-Content -Encoding utf8 evidencias/spec003/rodada-final-comando/comando.json
Get-Content -Encoding utf8 evidencias/spec003/rodada-final/manifesto.json
```

Os filtros selecionam registros já existentes; não executam o sistema. `resultados-originais.json` conserva os registros anteriores ao diagnóstico; `resultados.json` acrescenta o diagnóstico consolidado. `baseline-pares.jsonl` conserva os doze observados iniciais. Logs: `baseline-unittest.txt`, `variantes-unittest.txt`, e `../rodada-final-comando/stdout.txt`/`stderr.txt`, relativos à pasta da rodada. Fontes executadas e hashes constam no manifesto.

Os comandos de execução já existentes estão no [quickstart](../specs/003-mudancas-controladas/quickstart.md): `python -B verificacao_variantes.py --saida evidencias/spec003/rodada-001` é exemplo de nova tentativa; só usar uma pasta que ainda não exista. O comando histórico final usou `rodada-final`, que deve ser preservada. Para a suíte original, o comando existente é `python -B -m unittest discover -s tests -p test_autorizacao.py -v`, no snapshot da baseline indicado no quickstart; controles do verificador usam `python -B -m unittest discover -s tests -p test_variantes.py -v`, na raiz. Esses comandos são referências para um ensaio futuro autorizado, não instruções para reexecutar ou sobrescrever evidências nesta preparação.

## 5. Limite da demonstração — 30 segundos

“A execução registrada conferiu 18 métodos originais, 12 pares da base e 48 pares de variantes, conformes com uma referência candidata. Os 17 métodos sintéticos do verificador são controles separados. Isso demonstra a operação técnica local; não aprova cientificamente a referência nem mede desempenho de LLM. A próxima especificação prepara entradas permitidas e avaliação separada de listas. Revisão profissional, notas definitivas, fundamentação das medidas e desenho final do piloto continuam pendentes.”
