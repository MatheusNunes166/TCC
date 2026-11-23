# Impacto de mudanças com LLM

Pesquisa sobre seleção de requisitos impactados e testes de regressão existentes em um módulo fictício de autorização. Compara pedidos diretos e estruturados, com e sem notas simuladas de análise, usando uma referência local. [Estado atual e pendências](ESTADO_ATUAL.md).

## Abrir o painel

Na pasta `tcc-impacto-llm`:

```text
python apresentar.py
```

O painel abre em **http://127.0.0.1:8765**, com **Executar** e **Resultados**.
Mantenha o terminal aberto; Ctrl+C encerra o servidor. Abertura, consulta,
prévia e filtros não fazem chamadas. O painel usa somente a biblioteca padrão.

Em **Executar → Modo de execução → Pesquisa documental • 64 observações •
D0/D1/E0/E1**, consulte plano fixo, configurações, próxima posição e progresso.
**Ver payload da próxima posição** apresenta o material exato. Clique em
**Executar próxima observação • 1 chamada paga** para enviar somente a primeira.
Depois de conferir seus registros técnicos, escolha o limite e use **Continuar
lote • N chamadas pagas** para enviar até esse número de pendentes, sequencialmente.
Clique duplicado e execução concorrente são bloqueados; posições já iniciadas,
inclusive falhas ou estado remoto desconhecido, não são reenviadas.

O novo bloco tem **64 posições, 32 células N=2, dois blocos de 32 e 16 payloads**.
D0/E0 sem notas; D1/E1 com a mesma nota original. CONSOLIDADA é literal;
OPERACIONAL substitui somente requisitos pelos cinco documentos do pacote.
Catálogo de quinze casos/seis colunas e política integral permanecem. A preparação
anterior de 32 posições e seu produtor continuam preservados e conferíveis.
[Operação completa, arquivos, avaliação e limites](documentacao/operacao-documentacao.md).

Em **Resultados**, escolha **Pesquisa documental • 64 observações** no filtro
Origem. Use os filtros de documentação/modelo/mudança/condição/nota/repetição/
situação e requisitos/testes relacionados. Cada linha mostra seleção, referência,
métricas, original, payload e metadados; a consistência é calculada por célula,
com denominadores separados. Conformidade permanece pendente de revisão humana.

**Demonstração livre** continua disponível no modo de execução, com controles
próprios de perfil/modelo e identidades `DEMO-...`, fora das coortes de pesquisa.
As 64 observações anteriores e as 16 notas continuam nos filtros originais.
O bloco documental usa `DOCOP64-...`, fase/coorte próprias e pastas
`captura/documentacao-operacional-64-real-001/` e
`avaliados/documentacao-operacional-64-real-001/`.

`OPENAI_API_KEY` fica somente no ambiente do servidor; sem chave, envio é
desabilitado e consulta/prévia continuam disponíveis. Medium/4096 e demais
parâmetros do plano são protegidos. Não há exigência de orçamento positivo ou
garantia de teto monetário. A referência privada nunca entra no input.

Nesta integração: **zero chamadas reais**, nenhum teste de conexão externa,
conformidade preenchida, commit ou push. A ampliação é decisão do pesquisador,
sem atribuição de aprovação científica ao orientador. Tratamento conjunto de
distribuição, redação, explicações e extensão; não garante dificuldade maior.

Sem abrir navegador: `python apresentar.py --sem-abrir`. Porta alternativa:
`python apresentar.py --porta 8766`. [Verificações efetivas](apresentacao/VERIFICACAO.md).

## Verificar offline

```text
python apresentar.py verificar
```

Executa os **18 métodos originais da aplicação**, reutiliza a matriz de **75 comparações** (15 casos × cinco versões) e confere os **64 + 16 originais** sem reavaliar. Os subprocessos ficam sem chave e com rede bloqueada. Não gera HTML, relatórios descartáveis ou novas capturas. Os controles do painel usam transporte e respostas artificiais; comandos e limitações em [verificação](apresentacao/VERIFICACAO.md).

## Abrir pelo VS Code

Abra [Apresentacao-TCC.code-workspace](Apresentacao-TCC.code-workspace) em **Arquivo → Abrir Workspace do Arquivo**. **Ctrl+Shift+B** inicia o painel. A tarefa **TCC: verificar bancada offline** executa o comando de verificação. O Explorer dessa janela oculta pastas volumosas, preservando seus caminhos e conteúdos; abrir a pasta normal mostra o projeto completo.

## Limpeza segura e conservação

`python apresentar.py limpar` apresenta uma prévia somente dos caches `__pycache__`, `.pytest_cache` e `.ruff_cache` **da raiz**. Para removê-los, use `python apresentar.py limpar --aplicar`. A operação recusa diretório rastreado, link/junction ou ausência de comprovação por Git. Não percorre capturas, avaliações ou evidências.

O inventário desta organização encontrou **13.227 arquivos versionados**, aproximadamente **50 MB decimais**. Capturas, avaliações e evidências concentram 13.003 arquivos. Não havia caches versionados identificados para descarte imediato. As cópias históricas e os controles têm vínculos de caminho/hash; não foram tratados como lixo.

| Procurar | Onde está |
|---|---|
| Objetivo e desenho | [Contexto](documentacao/contexto-e-escopo.md), [protocolo](materiais/01_PROTOCOLO.md) e [arquitetura](documentacao/arquitetura.md) |
| Requisitos e expectativas | [Requisitos](documentacao/requisitos.md), [catálogo 0.3](materiais/modelos/catalogo_baseline_0.3.md), [referência candidata 0.3](documentacao/referencia-candidata-0.3.md) |
| Notas e pedidos | [Texto e origem](materiais/04_NOTAS_E_PROMPTS.md), [política comum](materiais/07_DEFINICOES_COMUNS.md) |
| Comparação de 64 respostas | [Relatório](avaliados/extensao-real-0.3-001-avaliacao-001/RELATORIO.md), [análise das divergências](documentacao/analise-extensao-0.3.md) |
| Bloco de 16 respostas de notas | [Relatório e limites](avaliados/notas-mc04-real-001/RELATORIO.md) |
| Operação de pesquisa | [API e revisão](documentacao/operacao-api.md), [notas](documentacao/operacao-notas.md), [estado vigente](ESTADO_ATUAL.md) |
| Desenvolvimento e histórico | [Specs](specs/), [decisões](documentacao/decisoes.md), [histórico](documentacao/historico/) |

O piloto de 16 chamadas permanece separado. Conformidade das execuções e revisão científica da referência/notas são decisões distintas: HTTP 200 ou acerto não aprovam nenhuma delas. A apresentação lê os resultados existentes sem substituir esses registros.

Cronologias e comandos anteriores continuam no estado, nas decisões e nos relatórios originais. O [README anterior](https://github.com/MatheusNunes166/TCC/blob/97af9f093018973e423117ac9e19ab4e4e5074a2/tcc-impacto-llm/README.md) está preservado no Git.
