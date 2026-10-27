# Guia de validação futura — Spec 004

> Convenções vigentes — 27/10/2026, D-26/D-27: o pesquisador adotou PONT-01/PONT-02 como convenções técnicas candidatas, ainda sujeitas à revisão científica. Política `ids-proposta-004-v2`: célula base por configuração/mudança/condição; versões de política ou referência distintas impedem resultado combinado, com diagnóstico e grupos separados por versão. Identidade lógica única por configuração/mudança/condição/repetição; duplicidades bloqueiam o resumo afetado sem escolha automática. Tentativas técnicas vinculadas não são repetições. Jaccard somente entre repetições distintas elegíveis, com número de observações/pares; menos de duas: **não calculável**. I1 corrigido: rejeitar links simbólicos internos/externos, junctions e todos os reparse points. Implementação e controles independentes autorizados, sem LLM/piloto. Isolamento real não demonstrado; T014/T015 e dependentes permanecem pendentes. Textos datados de somente planejamento/sem tarefas abaixo são históricos; originais preservados em evidências.

27/10/2026. **Somente planejamento.** Montador, avaliador, testes e fixtures aqui citados não existem. Nenhum comando de aplicação abaixo foi executado. Não há pacote permitido exportado, resposta de LLM ou piloto.

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

Separadamente, S-14 de fronteira de acesso exige runner/pacote em zona restrita sob identidade sem leitura das zonas de desenvolvimento/avaliação. Demonstrar leitura permitida dos documentos e negada das sentinelas fictícias nas zonas proibidas, mantendo provas. Sem essa preparação/permissão e inspeção humana, registrar “isolamento não demonstrado”; não marcar S-14 integralmente conforme só pelos testes de paths/mocks. Nenhuma identidade/ACL é criada neste planejamento.

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

## Estado técnico parcial — 27/10/2026

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

