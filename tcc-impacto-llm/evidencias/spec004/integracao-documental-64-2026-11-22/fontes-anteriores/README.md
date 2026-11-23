# Impacto de mudanças com LLM

Pesquisa sobre seleção de requisitos impactados e testes de regressão existentes em um módulo fictício de autorização. Compara pedidos diretos e estruturados, com e sem notas simuladas de análise, usando uma referência local. [Estado atual e pendências](ESTADO_ATUAL.md).

## Abrir o painel

Na pasta `tcc-impacto-llm`, execute:

```text
python apresentar.py
```

O painel abre em **http://127.0.0.1:8765**, com duas telas: **Executar** e **Resultados**. Mantenha o terminal aberto; Ctrl+C encerra o servidor. Abrir a página, consultar resultados ou visualizar o payload não envia chamadas. Não exige pacotes externos.

Em **Executar**, escolha modelo, mudança, condição e nota aplicável. **Ver material enviado** apresenta o payload exato. **Executar chamada real** inicia uma única chamada paga, sem repetição automática. O painel preserva a captura antes de usar o avaliador existente. A chave `OPENAI_API_KEY` fica somente no ambiente do servidor; sem chave, os resultados continuam acessíveis e o envio fica desabilitado. Não há exigência de orçamento positivo nem teto monetário automático, conforme D-49.

Em **Resultados**, escolha demonstrações novas, comparação de **64 observações** ou bloco de **16 notas**. Filtre por modelo, mudança e condição; em **Mais filtros**, use nota, resultado, requisito ou teste. IDs relacionados incluem esperados e selecionados, conservando omissões e excedentes. Abra uma linha para comparar requisitos/testes, mudança/preservação e métricas, consultar resposta original, payload, notas e metadados ou abrir as pastas. Informações extensas começam recolhidas.

Novas chamadas são demonstrações `DEMO-...`, armazenadas em `captura/demonstracoes-painel/` e `avaliados/demonstracoes-painel/`. Não entram automaticamente nas coortes científicas; conformidade permanece pendente. Somente o payload preservado é enviado: sem referência, resultados anteriores, arquivos do projeto ou histórico da conversa. A referência é privada do avaliador.

Para iniciar sem abrir o navegador: `python apresentar.py --sem-abrir`. Se a porta estiver ocupada: `python apresentar.py --porta 8766`.

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
