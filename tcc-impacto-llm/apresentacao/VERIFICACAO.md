# Verificação do painel atual — 13/11/2026, D-52

Abrir: `python apresentar.py`. Somente servidor: `python apresentar.py --sem-abrir`. Porta alternativa: `python apresentar.py --porta 8766`. Verificar offline: `python apresentar.py verificar`. Tarefa padrão do workspace abre o painel; a segunda tarefa verifica a bancada. Ctrl+C encerra sem reenviar chamadas.

Versão anterior detectada; patch de atualização conferido por `git apply --check`, com conflitos em três registros locais. Integração manual das fontes necessárias, sem reset/aplicação forçada, sem aplicar o completo ou substituir revisões.

Controles executados no Windows/PowerShell com Python 3.13.3, chave removida e rede externa bloqueada. Somente HTTP da fixture em `127.0.0.1` permitido:

- **41 descobertos: 12 do painel, 11 da apresentação e 18 da aplicação; 40 aprovados, um ignorado, zero falhas/erros.** Symlink ignorado por `WinError 1314`. Reprodução: `python -B -m unittest discover -s tests -p test_painel_llm.py -v`, repetido para `test_apresentacao.py` e `test_autorizacao.py`. HTTP/chave/respostas artificiais em temporários. Controles preservam formato inválido, fragmentos, falhas e originais antes da avaliação, sem retry.
- `python -B apresentar.py verificar`: retorno 0, 18 testes originais aprovados, **75/75 comparações conformes**, **64 + 16 originais** e **324 hashes consumidos** conferidos. Não gera arquivos ou HTML, confirmado por teste.
- `node tests/test_interface_painel.cjs`: aprovado. DOM mínimo artificial com 80 registros e 20 perfis. Filtros por coorte/modelo/mudança/condição/nota/resultado/requisito/teste; excedentes, mudança/preservação, notas N02, detalhes recolhidos, preview sem envio, clique duplicado, falha de POST e ausência de chave. Zero chamadas reais ou gravações científicas.
- JavaScript, JSON/tarefas do workspace, referências operacionais e `git diff --check` conferidos. Inicialização sem envio; controles desabilitados até carregar opções. Repetição/retomada não reenviam.

Removidos template/gerador estáticos, opções exclusivas e duas pastas de cinco saídas descartáveis, conferidas quanto a identidade, rastreamento, links/junctions e dependências científicas. Regra de ignore exclusiva retirada; nenhum cache científico ou histórico descartado. Nenhum ZIP/patch de integração dentro da entrega fora das áreas históricas; pacote original fora do repositório.

Preservação: inventário anterior de **17.380 arquivos locais**, inclusive ignorados; os **13.064 nas áreas científicas mantêm os hashes**. Núcleo, transporte, avaliador, notas, prompts, planos, referência e decisões humanas preservados. Somente fontes/documentação da apresentação atualizadas. Inventário e controles temporários ficam no temporário do sistema, fora do repositório.

**Limitações:** a conexão de automação do Chrome iniciou, mas os comandos de inspeção não responderam. Nenhuma captura renderizada foi validada; DOM artificial não comprova contraste, espaçamento ou legibilidade em 1366×768/na tela da banca. Conferir manualmente Executar, Resultados, filtros/detalhes antes da apresentação. Ctrl+Shift+B, abertura nativa por `os.startfile`, Git Bash e symlink com privilégio também não foram validados. Zero chamadas reais, testes de conexão externa, commit, push ou conformidades preenchidas.

Os registros abaixo são históricos; seus comandos/artefatos estáticos foram substituídos pelo fluxo acima.

# Verificação da organização e demonstração

## Integração local no Windows — 13/11/2026 (D-51)

Raiz Git `D:\TCC-Projeto\TCC`, inicialmente limpa, no commit-base `97af9f093018973e423117ac9e19ab4e4e5074a2`. SHA-256 do patch igual ao de `VALIDACAO.json`: `e14eddc8bd76c7c4abe5c6d6b1c6ec8b0f2936e2bd4f0444c7304ad30ba10b06`. `git apply --check` e `git apply` concluídos sem conflitos, sem reset ou sobrescrita forçada. A configuração `safe.directory` foi passada somente aos comandos/processos do sandbox; nenhuma configuração Git global foi alterada.

- PowerShell, Python 3.13.3: `python -B -m unittest discover -s tests -p test_apresentacao.py -v`, retorno 0; **10 descobertos, 9 aprovados, 1 ignorado, zero falhas/erros**. O teste `test_link_de_cache_nao_e_seguido` foi ignorado por `WinError 1314`, sem privilégio de criação de symlink. Os controles de limpeza usam somente fixtures temporárias; nenhum cache do projeto foi removido.
- `python apresentar.py --sem-abrir`, retorno 0: **18 métodos da autorização aprovados**, **75/75 comparações conformes**, **64 + 16 respostas originais** somente lidas. Processos da bancada com rede bloqueada e chave removida do ambiente.
- Painel gerado (`saidas/20261113-193130-72da02/relatorio.html`, removido em D-52), manifesto local (`saidas/20261113-193130-72da02/execucao-local.json`, removido em D-52), matriz (`saidas/20261113-193130-72da02/matriz-bancada.json`, removido em D-52), log da autorização (`saidas/20261113-193130-72da02/testes-autorizacao.txt`, removido em D-52) e `matriz-stderr.txt` vazio. Os cinco arquivos ficam em área ignorada pelo Git e não constituem nova coleta.
- JSON incorporado no HTML igual ao manifesto, quatro seções presentes (`bancada`, `llm`, `resultados`, `arquivos`), nenhum recurso externo de renderização, sintaxe JavaScript aprovada por `node --check`, 11 destinos locais existentes e 334 hashes de fontes consumidas reconferidos. T12/MC-04 muda de negar/conflito para permitir/permissao_direta; T14 conserva negar/conflito. Blocos separados em 32 e oito células, com 64 e 16 observações.
- JSON do [workspace](../Apresentacao-TCC.code-workspace), pasta resolvida, script da tarefa de tipo `process` e seleção da tarefa padrão de build conferidos estaticamente. O atalho não foi acionado.

Evidências locais adicionais em `D:\TCC-Projeto\integracao-apresentacao-20261113`: `inventario-antes.json`, cópias literais dos quatro documentos anteriores, `testes-apresentacao.txt`, `demonstracao.txt`, `arquivos-gerados.json` e `preservacao-final.json`. O inventário inicial cobre **16.363 arquivos locais, 60.736.208 bytes**, inclusive ignorados e excluindo metadados `.git`. A comparação final confirmou **16.359 arquivos idênticos, quatro alterações intencionais e nenhum ausente**; somente `.gitignore`, `README.md`, `ESTADO_ATUAL.md` e `documentacao/decisoes.md` mudaram entre os arquivos anteriores. O histórico de decisões e a seção científica do estado foram conferidos literalmente, incluindo os finais de linha originais. Código da bancada, variantes, capturas, avaliações, notas, prompts, referência e pontuação mantêm os hashes anteriores. Esses números diferem do inventário apenas versionado da preparação abaixo.

**Pendências no Windows:** inspeção visual renderizada das quatro seções e seletores, Ctrl+Shift+B no VS Code, abertura de pastas por `os.startfile` e execução no Git Bash. O comando solicitado usou `--sem-abrir`; nenhum navegador ou Explorer foi aberto nesta integração. A validação estrutural/sintática não equivale a inspeção visual. O controle real de symlink também permanece condicionado ao privilégio do ambiente. Sem chamadas à API, limpeza do projeto, commit, push ou alteração de conformidade.

## Registro de origem do pacote — preparação em Linux

O registro de 12/11 a seguir descreve as verificações informadas pelo pacote; os resultados locais efetivamente executados estão acima.

12/11/2026. Implementação preparada em cópia do repositório no commit `97af9f093018973e423117ac9e19ab4e4e5074a2`, sem commit/push. Esta entrega não muda a pesquisa nem declara conformidades aprovadas.

## Execução conferida

- `python -B -m unittest discover -s tests -p test_apresentacao.py -v`: **10 métodos aprovados**, zero falhas/erros/ignorados neste ambiente Linux. Fixtures artificiais em diretórios temporários; nenhum acesso à API.
- `python -B apresentar.py --sem-abrir`: **18 métodos da autorização aprovados**, **75/75 comparações conformes** pela função de matriz já existente, leitura das **64 + 16 respostas originais**. Nenhuma chamada nova ao LLM.
- O comando também foi executado a partir de outra pasta usando o caminho absoluto do script, sem depender da pasta corrente.
- `python -B apresentar.py limpar`: prévia concluída; nenhum candidato de cache nesta cópia, nenhum arquivo removido.
- Lógica JavaScript exercitada em DOM mínimo artificial: T12/MC-04 libera exportar; T14 preserva conflito; divergência MC-02/Sol exibe RF-02/RF-03; N02 conserva a afirmação incorreta; duas tabelas de 32 e oito células separadas; 11 links locais existentes.
- JSON do workspace válido e `git diff --check` sem erros.

Os controles novos conferem recusa de referência/resposta/nota trocadas, bloqueio de rede e remoção da chave do ambiente dos testes; limpeza em prévia/aplicação sem tocar em capturas; recusa de cache rastreado e link de cache. A função não importa o coletor para enviar dados nem duplica a pontuação.

## Preservação e limpeza

Inventário inicial de **13.227 arquivos versionados**, 49.686.121 bytes, com hashes calculados antes da edição. Desses, **13.223 permaneceram idênticos**. Os quatro alterados intencionalmente são `.gitignore`, `README.md`, `ESTADO_ATUAL.md` e `documentacao/decisoes.md`; os originais continuam no commit de origem. Nenhum arquivo anterior ausente. Núcleo, variantes, testes anteriores, notas, prompts, referências, capturas, avaliações e evidências mantêm seus bytes.

Não se comprovou descarte seguro das cópias históricas ou dos controles. Eles não foram removidos. O ganho de organização vem de um README curto, um comando e uma janela de apresentação com exclusões visuais; os arquivos permanecem acessíveis pelos links e pela abertura normal da pasta.

## Limites que precisam de conferência local

A abertura de navegador/arquivo local foi bloqueada pelo ambiente de preparação; **não houve inspeção visual renderizada do painel**. A verificação de lógica em DOM artificial não substitui essa inspeção. Antes da apresentação, abrir o HTML no Windows e conferir as quatro seções, seleção de casos e observações, tabelas e legibilidade.

O Windows, o Git Bash, a tecla Ctrl+Shift+B e a abertura nativa de pastas por `os.startfile` não foram executados aqui. O comando usa Python/biblioteca padrão, caminhos pela localização do script e uma tarefa VS Code de tipo process, sem comandos específicos de PowerShell/Bash. A conferência final deve acontecer na máquina da apresentação.

Não se altera a conformidade de nenhuma execução científica. A visualização identifica o estado no registro original e remete às decisões separadas; relatórios descritivos não são promoção automática a resultado revisado. Uma demonstração de chamada nova à API não está incluída neste comando offline.
