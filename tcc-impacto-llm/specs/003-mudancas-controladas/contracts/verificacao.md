> Estado vigente — 21/10/2026 (D-20/D-21): Spec 003 implementada e verificada; 35/35 tarefas concluídas com evidências. Quatro variantes independentes de B `aec474bcb54d6dae2afceff8e5b9226991386490`, uma edição por fonte, diffs/AST e revisão registrados. Python 3.13.3: suíte original 18 métodos OK, baseline 12/12 pares e variantes 48/48 conformes por decisão/motivo, zero divergências/erros/lacunas; 17 métodos sintéticos separados da bancada. Baseline, testes, materiais, referência candidata 0.2 e seleções 2/4/8/5 preservados. Evidências e diagnóstico do mecanismo: `specs/003-mudancas-controladas/evidencias.md` (desde a raiz). P-01/P-02/P-03, revisão das expectativas T12 e adoção constitucional pendentes; T12 já adotado/verificado em B. Revisão profissional, possíveis novos modelos e métricas aguardam transcrição da orientação e decisão explícita. Sem piloto, coleta ou LLM. Próxima ação: revisão humana das evidências e da referência candidata, seguida de detalhamento da orientação; nenhuma etapa experimental liberada. Registros anteriores abaixo são históricos.

# Contrato da interface local de verificação

Data: 19/10/2026. Interface planejada, não implementada. Contrato para o pesquisador e arquivos de evidência; não é API de coleta experimental.

## Chamada futura

```powershell
python -B verificacao_variantes.py --saida evidencias/spec003/<id-novo>
```

Partir da raiz do projeto. Saída deve ser pasta nova dentro da área de evidência, sem sobrescrever tentativa ou interceptar código/testes/referência. Sem remoção recursiva, opção de trocar B por HEAD, filtro de testes ou atualização do gabarito. B/mapeamento fixos neste incremento. Fontes das quatro variantes precisam ser implementadas e revisadas em etapa futura.

Git/Python locais; extrair objetos em bytes com raiz/prefixo reais e copiar fontes de execução em snapshot novo. Identificar commit do executor, estado local, versão Python, B, objetos e hashes. Alteração local relevante deve ser informada antes de incluída e não redefine B.

## Interface do núcleo

Preservar assinatura `autorizar(estado: str, papeis: frozenset[str], operacao: str) -> dict[str, str]`. Cada módulo tem as funções/assinaturas de B e apenas sua expressão alterada conforme o plano; não importa outras variantes nem recebe flag de mudança.

Entrada válida do catálogo. Saída: dict com exatamente decisao e motivo, strings do vocabulário existente. Comparar os dois campos; retorno válido diferente → divergente; exceção ou retorno fora do contrato → erro, com bruto preservado. Motivo diferente com decisão igual reprova o par.

## Execução e evidências

1. Conferir B/referência e fonte única por variante: diff revisado com responsável/data e AST fora da expressão permitida idêntica. Invalidade impede executar a fonte, não é relevada por saídas incidentais.
2. Executar suíte original no snapshot B com `sys.executable -B -m unittest discover -s tests -p test_autorizacao.py -v`, cwd no snapshot, guardando descoberta/logs/retorno. Obter ainda os 12 observados iniciais pelo catálogo na mesma tentativa. Não aplicar expectativas de B às variantes.
3. Matriz unittest com subTest por mudança/teste, percorrendo catalogo e expected de cada mudança, sem filtro de seleção. Registrar antes da asserção; falha de par não elimina os demais. Sem mocks nas 48 comparações reais.
4. Persistir manifesto.json, resultados.json, logs e diffs conforme [modelo](../data-model.md). Observado null em ausência/erro, bruto separado se retorno malformado. Contagens de previstos/tentados/comparados/conformes/divergentes/erros/não executados, sem métricas de LLM.
5. Hashes finais e conclusão restrita de engenharia. Escrita incompleta ou falta de evidência não pode retornar sucesso.

| Código de saída | Significado futuro |
|---|---|
| 0 | 48 conformes, B/controles conformes, fontes/procedência/registros íntegros; apenas conformidade com candidata 0.2 |
| 1 | Matriz completa, sem erros/lacunas de execução, com ao menos uma divergência válida em variante |
| 2 | Erro de entrada/procedência/execução/registrador, matriz incompleta ou interrupção conhecida; prioridade sobre 1 |

Se B divergir, variantes ficam não executadas por pré-condição e o código é 2; a divergência inicial permanece registrada como tal. Códigos não substituem contagens nem concedem aprovação científica.

## Diagnóstico e preservação

Conservar esperado/observado/fontes/logs; conferir origem/isolamento/entrada e depois requisitos, dependências e precedência. Uma edição pode causar vários efeitos propagados; não acrescentar edições para suprimir efeitos previstos. Registrar causa confirmada/hipótese/pendência. Suspeita de erro da referência exige revisão humana separada, nunca adaptação automática. Nova tentativa não apaga divergência anterior.

Expectativas/conjuntos permanecem intactos; verificador não os grava. Nenhum comando/scenário foi executado nesta fase. Piloto, LLM, coletor e avaliador científico ficam fora do escopo.
