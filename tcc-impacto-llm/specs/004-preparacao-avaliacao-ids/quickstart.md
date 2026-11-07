> Operação vigente: [complemento D-35 do contrato](contracts/preparacao-avaliacao.md#complemento-vigente-d-35--importação-real-e-preparação-06112026) e [estado central](../../ESTADO_ATUAL.md). As restrições históricas a importação somente sintética/revisão externa são superadas nesse alcance; planejamento original abaixo preservado.

# Guia de consulta e validação local — Spec 004

> Contrato vigente — 01/11/2026 (D-29): o modelo recebe somente texto preparado, sem ferramentas, repositório, código, comandos, gabarito, resultados de variantes ou histórico. Exigências de identidade/ACL do Windows de T014/T015 substituídas, sem execução ou aprovação retroativa. Permanecem validação de arquivos/caminhos, autorização de conteúdo, integridade, equivalência de condições e avaliação separada. Notas representam conhecimento de analista de testes; texto definitivo e revisão profissional pendentes. Não se avaliam juniores, novos testes ou defeitos reais. Sem modelo escolhido, envio, chamadas externas ou piloto; revisão científica pendente. Histórico preservado em evidencias/spec004/revisao-textual-2026-11-01/originais.

> Convenções vigentes — 27/10/2026, D-26/D-27: o pesquisador adotou PONT-01/PONT-02 como convenções técnicas candidatas, ainda sujeitas à revisão científica. Política `ids-proposta-004-v2`: célula base por configuração/mudança/condição; versões de política ou referência distintas impedem resultado combinado, com diagnóstico e grupos separados por versão. Identidade lógica única por configuração/mudança/condição/repetição; duplicidades bloqueiam o resumo afetado sem escolha automática. Tentativas técnicas vinculadas não são repetições. Jaccard somente entre repetições distintas elegíveis, com número de observações/pares; menos de duas: **não calculável**. I1 corrigido: rejeitar links simbólicos internos/externos, junctions e todos os reparse points. Implementação e controles independentes autorizados, sem LLM/piloto. Registro de 27/10: isolamento por SO não demonstrado; exigência substituída por D-29, sem aprovação retroativa. Textos datados de somente planejamento/sem tarefas abaixo são históricos; originais preservados em evidências.

27/10/2026. **Somente planejamento.** Montador, avaliador, testes e fixtures aqui citados não existem. Nenhum comando de aplicação abaixo foi executado. Não há pacote permitido exportado, resposta de LLM ou piloto.

## Histórico de planejamento e comandos v2 — 27/10/2026

Os comandos desta seção pertencem ao contrato antigo. Não os reutilizar para montagem v3: a autorização externa agora é obrigatória. Comandos vigentes e evidências D-30 estão ao final.

## Pré-condições

Revisar [plan](plan.md), [research](research.md), [modelo](data-model.md) e [contrato](contracts/preparacao-avaliacao.md). Implementação/testes dependem de pedido posterior; este fluxo não gera tarefas nem as executa. Python 3.13.3 está disponível; desenho compatível com 3.11+, sem instalação.

Antes de usar dados de pesquisa, atender revisão profissional/científica da referência/política, notas definitivas, revisão de métricas e desenho final do piloto. Para controles locais, usar apenas documentos/respostas fictícios rotulados, notas em rascunho e referência sintética fixa. O diretório de trabalho do desenvolvimento não é ambiente isolado de envio.

## Seleção e setup realizados nesta fase documental

Na raiz `D:\TCC-Projeto\TCC\tcc-impacto-llm`, após atualizar `.specify/feature.json` para `specs/004-preparacao-avaliacao-ids`, foram executados sequencialmente:

```powershell
& 'C:/Program Files/Git/bin/bash.exe' .specify/scripts/bash/check-prerequisites.sh --json --paths-only
& 'C:/Program Files/Git/bin/bash.exe' .specify/scripts/bash/setup-plan.sh --json
```

Primeiro retorno confirmou FEATURE_SPEC/IMPL_PLAN em 004 antes do setup; segundo confirmou o mesmo destino e a cópia do template. BRANCH=`004-preparacao-avaliacao-ids` é contexto do resolvedor, sem branch Git criada/trocada. Seletor/setup/contracts exigiram repetição autorizada após bloqueios de escrita do sandbox; não foram falhas de teste nem de LLM. Repetir setup não é necessário para consultar o planejamento pronto.

## 1. Preparar controles e esperados — futuro

Após autorização de implementação, fixar fixtures por S-xx/subcaso em `tests/fixtures/spec004/`, com bytes exatos e expectativas **literais** conferidas previamente pelo contrato. A referência sintética G_RF={RF-02}, G_T={T04,T12} é fixa; não chamar a implementação para produzi-la. Identificar autor/revisão técnica sem presumir aprovação científica.

Preparar quatro pacotes fictícios da mesma mudança: sete documentos em D0/E0, oito em D1/E1, além de manifesto de cada um. Só documentos enumerados; as notas têm mesmo conteúdo em D1/E1 e status `RASCUNHO_NAO_REVISADO`. Não copiar evidências ou referência para a raiz permitida. Metadados não entram no payload.

## 2. Validar composição e acesso — futuro

Os comandos seguintes são **propostos e ainda não implementados**. Paths representam fixtures futuras; cada saída precisa ser nova. Nunca usar pastas da Spec 003 como saída.

```powershell
python -B montagem_entradas.py --pacote tests/fixtures/spec004/pacotes/D0 --manifesto tests/fixtures/spec004/pacotes/D0/manifesto.json --saida evidencias/spec004/controle-D0-001
python -B montagem_entradas.py --pacote tests/fixtures/spec004/pacotes/D1 --manifesto tests/fixtures/spec004/pacotes/D1/manifesto.json --saida evidencias/spec004/controle-D1-001
python -B montagem_entradas.py --pacote tests/fixtures/spec004/pacotes/E0 --manifesto tests/fixtures/spec004/pacotes/E0/manifesto.json --saida evidencias/spec004/controle-E0-001
python -B montagem_entradas.py --pacote tests/fixtures/spec004/pacotes/E1 --manifesto tests/fixtures/spec004/pacotes/E1/manifesto.json --saida evidencias/spec004/controle-E1-001
```

Esses paths no repositório servem a testes locais de composição e não comprovam isolamento. Conferir payload integral/delimitadores, cópias originais e hashes comuns, igualdade de notas D1/E1 e diferença apenas de pedido/notas conforme condição. Esperar retorno 0 e `PREPARADO_LOCAL_NAO_ENVIADO`, sem liberação de pesquisa.

> **Exigência histórica substituída por D-29, não executada/aprovada:** Separadamente, S-14 de fronteira de acesso exige runner/pacote em zona restrita sob identidade sem leitura das zonas de desenvolvimento/avaliação. Demonstrar leitura permitida dos documentos e negada das sentinelas fictícias nas zonas proibidas, mantendo provas. Sem essa preparação/permissão e inspeção humana, registrar “isolamento não demonstrado”; não marcar S-14 integralmente conforme só pelos testes de paths/mocks. Nenhuma identidade/ACL é criada neste planejamento.

## 3. Importar originais e conferir avaliação — futuro

Fornecer resposta local ou ausência/fragmento pelo registro de tentativa. Avaliador não chama serviço nem solicita resposta nova. Exemplo de invocação futura para S-01, com referência sintética e pasta nova:

```powershell
python -B avaliacao_ids.py avaliar --preparacao evidencias/spec004/controle-D0-001/preparacao.json --tentativa tests/fixtures/spec004/S-01/tentativa.json --referencia tests/fixtures/spec004/referencia-sintetica.json --saida evidencias/spec004/avaliacao-S01-001
```

Esperado: resposta/entrada/registro íntegros copiados antes da interpretação; RF TP/FP/FN=1/0/0, testes=2/0/0, P/R/F propostas iguais a 1; origem sintética/modelo nulo; retorno 0. Em S-02, retorno também 0 com omissão e R/F menores em testes: resposta incorreta não é falha do avaliador. Em formato inválido, retorno 1 com originais preservados e métricas observadas nulas. Em falha técnica importada, retorno 1 e estado técnico distinto. Em referência/integridade inválida, retorno 2, sem pontuar resposta.

Não usar a candidata para produzir o esperado sintético. Conferência futura do adaptador da candidata verifica leitura de `rfs`/`tests`, status e hashes exclusivamente no avaliador, sem exportar essa referência para os pacotes ou regravar seus campos históricos.

## 4. Verificar as 16 famílias — futuro

```powershell
python -B -m unittest discover -s tests -p test_montagem_entradas.py -v
python -B -m unittest discover -s tests -p test_avaliacao_ids.py -v
```

Contagens de métodos unittest não substituem cobertura de 16 famílias e todos os subcasos do contrato:

- S-01–S-04: exata/parcial/todos/vazias, com contagens e frações literais.
- S-05–S-08: duplicatas/ordem, desconhecidos, sem normalização e IDs trocados de dimensão.
- S-09/S-10: formato estrito (incluindo BOM/UTF-8/chaves repetidas/constantes/recusa) e independência das dimensões.
- S-11/S-12: falhas técnicas sem resposta/com fragmento, referência incompleta ou defeituosa sem escores.
- S-13/S-14: integridade no fechamento, diretórios novos, composição negativa/positiva e prova de acesso restrito.
- S-15/S-16: todos os pares de Jaccard, insuficiência de pares, resumos/denominadores, imputação opcional e tentativas vinculadas.

Preservar comando, cwd, Python, retorno, stdout/stderr, versões/hashes, esperado/observado e cobertura por subcaso. Não contar esses controles como respostas LLM, repetições do piloto ou pares de 003. Falha inicial e execução corrigida ficam em pastas diferentes; não ajustar esperado ao observado.

## 5. Resumos candidatos — futuro

```powershell
python -B avaliacao_ids.py resumir --avaliacoes tests/fixtures/spec004/S-16/avaliacoes-lista.json --observacoes tests/fixtures/spec004/S-16/observacoes-planejadas.json --saida evidencias/spec004/resumo-S16-001
python -B avaliacao_ids.py resumir --avaliacoes tests/fixtures/spec004/S-16/avaliacoes-lista.json --observacoes tests/fixtures/spec004/S-16/observacoes-planejadas.json --saida evidencias/spec004/resumo-S16-imputado-001 --imputar-invalidas
```

Cenário A de S-16: três observações, uma exata, uma inválida e uma técnica. Esperado N=3,A=3,C=2,V=1,I=1,T=1; validade=1/2, completude=2/3. Resumo válido P/R/F=1 em ambas; opção imputada acrescenta operacional P/R/F=1/2 em ambas, sem converter a falha técnica em seleção vazia. Jaccard não calculável. Retorno 1 informa diagnósticos/incompletude técnica; listas/denominadores devem permanecer explícitos.

Cenário B: uma observação e duas tentativas técnicas vinculadas, segunda exata; N=1,A=2,C=V=1,T=0. Não contar como duas repetições ou criar par Jaccard. Conflito de duas respostas concluídas para o mesmo ID bloqueia resumo até decisão explícita; não escolher a melhor.

## Fechamento e pendências

Futuro fechamento técnico exige cobertura/esperados e prova de acesso real, preservação/rechecagem de integridade e estado coerente. Roteiro pronto e controles conformes não aprovam cientificamente referência ou métricas. Revisão profissional, notas definitivas, fundamentação/revisão de medidas e desenho final do piloto continuam pendentes. Nenhuma dessas execuções foi feita nesta fase; próxima ação autorizável é revisar planejamento e solicitar tarefas.

## Histórico técnico parcial — 27/10/2026 (substituído no alcance de D-29)

Implementados `montagem_entradas.py` e `avaliacao_ids.py`, sem rede/provedor. Convenções D-26 candidatas, política ids-proposta-004-v2; 39 tarefas independentes concluídas. T014/T015 e T042–T048 pendentes: runner isolado não provisionado e criação de symlink real negada com WinError1314. Não há fechamento integral. [Evidências e limites](../../evidencias/spec004/revisao-parcial/relatorio.md). As descrições anteriores datadas de planejamento/comandos futuros são históricas; comandos locais agora existentes só preparam/avaliam arquivos sintéticos, sem envio ou piloto. Métricas, notas definitivas, referência e desenho científico continuam sujeitos à revisão. Checklist de qualidade preservada, sem remarcação.

Consulta das evidências existentes na raiz do projeto, sem reexecução:

```powershell
Get-Content -Encoding utf8 evidencias/spec004/revisao-parcial/relatorio.md
Get-Content -Encoding utf8 evidencias/spec004/revisao-parcial/matriz.json
Get-Content -Encoding utf8 evidencias/spec004/isolamento/ambiente.json
Get-Content -Encoding utf8 evidencias/spec004/montagem-final/comando.json
Get-Content -Encoding utf8 evidencias/spec004/avaliacao-confirmacao/comando.json
Get-Content -Encoding utf8 evidencias/spec004/demonstracao-001/resumos/A/resumo.json
```

Preparações originais em demonstracao-001/preparacoes; respostas e registros originais em entradas-avaliacao e nas saídas de avaliacoes. A demonstração identifica os hashes da versão executada; checkpoints finais incluem endurecimento posterior de lstat sem seguir links. Para reavaliar, usar pasta nova e --avaliacao-anterior quando aplicável, preservando a avaliação anterior. Não reexecutar scripts de preparação sobre diretórios existentes.

## Contrato textual verificável — D-29

Preparação editorial local em `fontes_autorizadas.py`, com seis caminhos fixos e recortes enumerados: instrução/notas/pedidos de materiais/04; definições integrais de materiais/07; contrato inicial de documentacao/requisitos; seis primeiras colunas da tabela T01–T12 de documentacao/qualidade-e-testes (sem coluna de destaques de RF); somente descrição de uma remoção na tabela da Spec 003; schema existente. Documentos mistos são lidos nessa edição local para selecionar os trechos, nunca enviados inteiros. A referência candidata não é lida nessa etapa.

`montagem_entradas.py`, contrato `spec004-v3`, lê pacote plano e `--autorizacao` externa explícita, fixando hashes de manifesto/documentos. Atualizar apenas seu próprio manifesto não autoriza texto alterado. A autorização é registro técnico controlado, não assinatura de autoridade ou detector semântico de qualquer gabarito: confrontar fontes, recortes, conteúdo e bytes. Mudança de fonte/recorte requer nova conferência; revisão profissional continua pendente. Fixtures v2 e comandos anteriores são históricos, preservados e não reexecutados como prova do contrato atual.

Somente `payload.txt` se destina ao modelo. Manifesto, autorização, cópias de documentos, fontes/hashes e `entrega-textual.json` são registros locais; não anexar diretório, código, fontes mistas ou referência. O recibo fixa texto/hash, `ferramentas=[]`, `anexos_ambiente=[]`, sem histórico e `envio_realizado=false`. Entrega real e ausência de ferramentas na plataforma serão conferidas antes do piloto; não foram exercitadas aqui, pois não há chamadas externas. Não se alega isolamento por SO.

Caminhos suportados: CLI com caminho local absoluto com drive ou relativo ao cwd; documentos do pacote filhos diretos com nomes enumerados; avaliador admite subdiretórios relativos declarados com separadores `/` ou `\`, confinados à raiz. Recusar drive relativo, raiz sem drive no Windows, UNC/dispositivos, streams `arquivo:fluxo`, dispositivos reservados, ponto/espaço final, componentes declarados vazios/`.`/`..` e links/junctions/reparse points. São controles de inclusão indevida, sem contas/permissões ou alegação de isolamento.

S-14 vigente verifica recortes/fontes, autorização independente, conteúdo proibido fictício em negativos, 16 combinações (quatro mudanças × quatro condições), texto exato e notas iguais D1/E1/ausentes D0/E0. Criação de symlink e negação de leitura por identidade são exigências antigas substituídas: não foram aprovadas. Esses objetos não pertencem às entradas suportadas; permanecem controles de recusa, sem exigir criação privilegiada para aceitar o contrato textual. PONT-01/PONT-02 e fórmulas candidatas não mudaram.

CLI vigente (usar diretórios novos, não os exemplos antigos v2):

```powershell
python -B fontes_autorizadas.py --raiz . --saida <editorial-nova>
python -B montagem_entradas.py --pacote <editorial-nova>/pacotes/MC-01-D0 --manifesto <editorial-nova>/pacotes/MC-01-D0/manifesto.json --autorizacao <editorial-nova>/autorizacoes/MC-01-D0.json --saida <preparacao-nova>
```

Avaliação continua na CLI separada com --referencia. Sem parâmetros de modelo/provedor, envio ou chamada externa.



## Verificação vigente — 01/11/2026 (D-30)

Engenharia offline do contrato D-29 concluída no alcance verificado: 49 tarefas vigentes atendidas; T014/T015 substituídas, não executadas/aprovadas. Recortes das seis fontes, autorização externa e montagem v3 produziram 16 pacotes; bytes, conteúdo, documentos comuns, notas D1/E1 e ausência de notas D0/E0 confrontados. Referência somente no avaliador separado; resposta de demonstração explicitamente sintética. As 16 famílias estão consolidadas com evidências anteriores preservadas e verificações necessárias das alterações; não se reexecutou pontuação inalterada nem se contou sintéticos como LLM.

[Relatório e limitações](../../evidencias/spec004/revisao-textual-2026-11-01/relatorio.md) inclui comandos, esperado/observado, hashes, matriz, caminhos suportados, limitação da criação de symlink e provas de SO substituídas. As seções de 27/10 são históricas; os gates atuais são D-29 e esta verificação, sem aprovação retroativa. Checklist é qualidade documental, preservada sem remarcação. Sem prova de entrega real ao modelo, modelo escolhido, chamada externa ou piloto. Revisão profissional/científica, notas definitivas, fundamentação das métricas, desenho final/congelamento do piloto e adoção constitucional permanecem pendentes.
