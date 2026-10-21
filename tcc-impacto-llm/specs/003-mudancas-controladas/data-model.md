> Estado vigente — 21/10/2026 (D-20/D-21): Spec 003 implementada e verificada; 35/35 tarefas concluídas com evidências. Quatro variantes independentes de B `aec474bcb54d6dae2afceff8e5b9226991386490`, uma edição por fonte, diffs/AST e revisão registrados. Python 3.13.3: suíte original 18 métodos OK, baseline 12/12 pares e variantes 48/48 conformes por decisão/motivo, zero divergências/erros/lacunas; 17 métodos sintéticos separados da bancada. Baseline, testes, materiais, referência candidata 0.2 e seleções 2/4/8/5 preservados. Evidências e diagnóstico do mecanismo: `specs/003-mudancas-controladas/evidencias.md` (desde a raiz). P-01/P-02/P-03, revisão das expectativas T12 e adoção constitucional pendentes; T12 já adotado/verificado em B. Revisão profissional, possíveis novos modelos e métricas aguardam transcrição da orientação e decisão explícita. Sem piloto, coleta ou LLM. Próxima ação: revisão humana das evidências e da referência candidata, seguida de detalhamento da orientação; nenhuma etapa experimental liberada. Registros anteriores abaixo são históricos.

# Modelo de dados — verificação local

Data: 19/10/2026. Desenho futuro; sem registros preenchidos de execução. JSON e biblioteca padrão, sem banco ou schemas externos. Regras e referência candidata de B continuam sendo fundamentos, não este modelo.

## ReferenciaInicial

`baseline_commit` = `aec474bcb54d6dae2afceff8e5b9226991386490`; raiz/prefixo Git; caminhos/objeto Git/SHA-256 de módulo, testes, requisitos, catálogo e JSON. Referência `versao = 0.2`, `status = CANDIDATO_NAO_REVISADO`, revisor/data nulos enquanto pendentes. `catalogo` e `mudancas[].expected` são extraídos de B, imutáveis.

## Caso

ID T01–T12 único; estado ativa/suspensa/em_revisao; papéis com nomes canônicos Consulta/Auditoria/Supervisão sem duplicação; operação visualizar/exportar; esperado inicial (`decisao`, `motivo`). Conservar valores/ordem do catálogo; apenas converter papéis para frozenset ao chamar. Não calcular esperado com o módulo.

## Variante

ID canônico MC-01/MC-02/MC-03/MC-04-v2, rótulo MC-04 opcional; B; caminho versionado/snapshot absoluto; SHA-256 antes/depois; identidade do módulo/loader; descrição de alteração; diff (caminho/hash); auditoria AST; revisão técnica com responsável/data/resultado/observação. Exatamente quatro variantes com 12 expectativas cada. Auditoria inválida ou pendente bloqueia sua execução.

## Tentativa — manifesto.json

- `schema_version = 1`: formato local de evidência, independente da referência 0.2.
- ID da tentativa, início/fim UTC, comando/argumentos, diretório, plataforma e Python (caminho/versão).
- Commit do executor, estado Git relevante, SHA-256 e snapshot do executor/testes novos. HEAD sem hashes não descreve alterações locais; informá-las antes de usá-las.
- ReferenciaInicial e quatro Variantes; arquivos fonte/logs/diffs, hashes iniciais/finais e revisão científica separada, ainda pendente.
- Suíte original: comando, retorno, stdout/stderr, descoberta e resumo. Evidência histórica não conta como execução nesta tentativa.
- Integridade de origem/política única/fontes/registros; estado preparando/em_execucao/concluida/invalida/interrompida.

## Comparacao — resultados.json

Duas listas: `baseline` (12 pares iniciais) e `variantes` (48 pares previstos). Chave única `(id_execucao, mudanca, teste)`; para inicial usar `mudanca = BASELINE`.

| Campo | Conteúdo |
|---|---|
| id_execucao, mudanca, teste | IDs; MC-04-v2 canônico |
| entrada | Estado, papéis, operação do catálogo |
| versao_executada | B, ID/BASELINE, caminho absoluto carregado, SHA-256, chave do manifesto |
| referencia | 0.2, caminho/hash extraído e chave catalogo[id].esperado ou mudancas[id].expected[teste] |
| esperado | Objeto completo decisao/motivo, copiado do esperado específico |
| observado | Resultado válido completo; null se indisponível ou malformado |
| observado_bruto | Retorno malformado preservado com tipo/representação; null sem retorno |
| estado | conforme/divergente/erro/nao_executado |
| comparacao | igual/diferente/nao_comparavel e diferenças por campo |
| efeito_esperado | mudou/preservou contra esperado inicial |
| efeito_observado | mudou/preservou/indisponivel contra observado inicial da mesma rodada |
| erro | Tipo/mensagem/traceback ou causa da não execução; null nos demais |
| evidencia | Log e subteste identificados |
| diagnostico | Causa/hipótese/pendência, RFs, evidências, responsável/data e resolução |

Retorno inválido não serializável: guardar repr e tipo no bruto, identificado como representação, sem converter em resultado válido. Exceção não produz observado inventado. Um caso só é conforme com contrato de saída e ambos os valores iguais.

## Resumo e invariantes

Previstos = 48; contagens disjuntas `conformes + divergentes + erros + nao_executados = 48`; tentados = conformes + divergentes + erros; comparados = conformes + divergentes. Exigir exatamente os 48 IDs esperados, sem duplicatas; ID inválido/duplicata é falha de integridade, não caso extra.

Verificação completa exige 48 tentados e integridade válida. Conformidade integral exige 48 conformes, zero erros/divergências/lacunas, B e controles conformes, auditorias válidas e fontes preservadas. Nenhum desses estados aprova cientificamente a candidata. Erro global de referência que impeça obter esperado produz manifesto inválido/diagnóstico, sem fabricar registros conformes.

## Transições

1. Preparar: extrair B, validar JSON/IDs/chaves/vocabulário, snapshot e fontes, hashes/diff/AST/revisão.
2. Inicializar registros conhecidos como não executados, observado null e causa ainda_nao_executado. Isso não é evidência de chamada realizada.
3. Conferir B/controles. Falha mantém variantes não executadas por pré-condição; não qualificar conformidade.
4. Fonte inválida mantém seus 12 pares não executados; executar outras válidas. Registrar resultado antes da asserção; erro individual não interrompe demais casos.
5. Persistir resultados/logs em encerramento protegido, também em falha. Interrupção marca remanescentes e tentativa interrompida. Falha de escrita invalida conclusão.
6. Retentativa tem novo ID/pasta e vínculo retentativa_de, sem sobrescrever anterior. Revisão de referência exige decisão humana/versionamento fora desta autorização.
