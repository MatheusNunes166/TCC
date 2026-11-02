# Modelo de dados proposto — Spec 004

> Contrato vigente — 01/11/2026 (D-29): o modelo recebe somente texto preparado, sem ferramentas, repositório, código, comandos, gabarito, resultados de variantes ou histórico. Exigências de identidade/ACL do Windows de T014/T015 substituídas, sem execução ou aprovação retroativa. Permanecem validação de arquivos/caminhos, autorização de conteúdo, integridade, equivalência de condições e avaliação separada. Notas representam conhecimento de analista de testes; texto definitivo e revisão profissional pendentes. Não se avaliam juniores, novos testes ou defeitos reais. Sem modelo escolhido, envio, chamadas externas ou piloto; revisão científica pendente. Histórico preservado em evidencias/spec004/revisao-textual-2026-11-01/originais.

> Convenções vigentes — 27/10/2026, D-26/D-27: o pesquisador adotou PONT-01/PONT-02 como convenções técnicas candidatas, ainda sujeitas à revisão científica. Política `ids-proposta-004-v2`: célula base por configuração/mudança/condição; versões de política ou referência distintas impedem resultado combinado, com diagnóstico e grupos separados por versão. Identidade lógica única por configuração/mudança/condição/repetição; duplicidades bloqueiam o resumo afetado sem escolha automática. Tentativas técnicas vinculadas não são repetições. Jaccard somente entre repetições distintas elegíveis, com número de observações/pares; menos de duas: **não calculável**. I1 corrigido: rejeitar links simbólicos internos/externos, junctions e todos os reparse points. Implementação e controles independentes autorizados, sem LLM/piloto. Registro de 27/10: isolamento por SO não demonstrado; exigência substituída por D-29, sem aprovação retroativa. Textos datados de somente planejamento/sem tarefas abaixo são históricos; originais preservados em evidências.

27/10/2026. Desenho futuro, sem arquivos de dados gerados ou capacidade implementada. [Contrato](contracts/preparacao-avaliacao.md) define CLI, regras e esperados; [research](research.md) fundamenta escolhas técnicas locais.

## 1. Manifesto permitido e documento

`manifesto.json`, UTF-8, enumera um pacote para **uma mudança e uma condição**, com:

| Campo | Conteúdo/regra |
|---|---|
| `versao_contrato`, `pacote_id`, `versao_pacote` | Identidade estável e versão explícita, nunca inferidas de diretório ou HEAD móvel. |
| `mudanca`, `condicao` | Mudança canônica MC-01/MC-02/MC-03/MC-04-v2 e D0/D1/E0/E1; alias documental MC-04 registrado externamente quando usado. |
| `status`, `liberado_para_pesquisa` | `RASCUNHO_PREPARACAO` e sempre `false` neste incremento. |
| `documentos` | Lista fechada e ordenada de objetos `papel`, `arquivo`, `versao`, `sha256`, `tamanho_bytes`, `revisao_conteudo`. |
| `revisao_conteudo` por documento | Estado (`pendente`, `conferido_tecnicamente`, `reprovado`), responsável/data/alcance quando existentes; rascunho e revisão científica separados. Nenhuma revisão fictícia é atribuída a pessoa real. |
| `status_notas`, `origem_notas` | `RASCUNHO_NAO_REVISADO`/pesquisador, ou `ausentes` em D0/E0. Mesmo conteúdo de notas em D1/E1. |

Os oito nomes lógicos permitidos são os da Spec, com `notas.md` somente nos pacotes D1/E1. Schema, manifesto e contrato não recebem conjuntos de resposta. Metadados de revisão, classificação da mudança, caminhos das fontes mistas e vínculos privados não entram no conteúdo preparado ao LLM. Proveniência editorial completa é registro externo, fora do alcance do montador; o manifesto permitido contém apenas identidade dos documentos finais.

Para controles, documentos fictícios conferidos tecnicamente permitem preparar entrada **sintética local**, mesmo com notas marcadas rascunho; isso não autoriza uso experimental. Documento pendente ou reprovado impede montagem utilizável. A aceitação técnica de um rascunho não deve ser rotulada como aprovação de conteúdo científico.

## 2. Entrada preparada

Diretório exclusivo por `preparacao_id`, com:

- `payload.txt`: bytes UTF-8 exatos preparados, com delimitadores fixos e ordem do contrato; não representa envio ocorrido.
- `manifesto-original.json`: cópia exata do manifesto recebido.
- `documentos/`: cópias byte a byte somente dos documentos efetivamente usados.
- `preparacao.json`: ID, instante UTC, versão/hash do montador e do contrato, manifesto/hash, condição/mudança, lista ordenada de hashes/versões, estado das notas, hash/tamanho do payload, revisão técnica e `status=PREPARADO_LOCAL_NAO_ENVIADO`.

Em falha, `status=BLOQUEADO`, causa e artefatos disponíveis identificados, sem `payload_pronto=true`. Nunca transformar composição parcial em payload utilizável. Saída fica fora da raiz de entrada. O diretório existente não pode ser reutilizado; integridade é conferida na escrita e ao consolidar. Não criar manifesto de congelamento científico.

## 3. Observação e tentativas locais

Reaproveitar conceitos de `materiais/modelos/registro_execucao.json`, preservando esse modelo sem edições; contrato de 004 é versão derivada explícita.

| Campo | Regra |
|---|---|
| `observacao_id`, `tentativa_id`, `tentativa_anterior` | Uma unidade lógica e suas tentativas técnicas; retentativa não é nova repetição. |
| `origem` | `sintetica` nos controles deste incremento; experimental é valor reservado para etapa futura autorizada, não usado agora. |
| `mudanca`, `condicao`, `repeticao_sintetica` | Identidade da célula de controle; não presumir piloto/bloco/repetição experimental. |
| `preparacao_id`, `preparacao_sha256`, `payload_sha256` | Vínculo à entrada exata; erro de vínculo bloqueia avaliação. |
| `estado_tecnico` | `concluida` ou `falha_tecnica`; causa obrigatória na falha. |
| `resposta_arquivo`, `resposta_sha256`, `resposta_tamanho` | Original disponibilizado ao avaliador; nulos quando ausente. Arquivo vazio recebido é resposta de tamanho zero, distinta de ausência. |
| `fragmento` | Indica conteúdo parcial em falha técnica, sem promovê-lo a resposta concluída. |
| `modelo_reportado` | Nulo nos controles; sem inventar configuração/provedor. |

Importação no avaliador copia o registro de tentativa e original em bytes antes de interpretação, sempre que disponíveis. Caminhos vêm explicitamente do registro/argumentos e são confinados à raiz de importação. Registro inválido, vínculo quebrado ou múltiplas respostas concluídas para a mesma observação impedem avaliação/resumo utilizável, com erro próprio.

## 4. Referência — exclusiva do avaliador

Candidata existente: `materiais/modelos/referencia_candidata_NAO_ENVIAR_AO_LLM.json`, versão 0.2, status `CANDIDATO_NAO_REVISADO`, revisor/data nulos. Não modificar. A avaliação registra cópia/hash/versão/status em sua zona privada. Campo de observação histórico é preservado literalmente.

Adaptador extrai somente `mudancas[id].rfs` e `mudancas[id].tests` como G. Universos: RF-01–RF-04 e T01–T12. Não usar `changed`, `preserved`, `expected`, saídas da bancada ou correspondência textual para derivar G. Verificar mudança única, IDs conhecidos, listas não vazias e sem repetição, versão/status presentes. Mapear somente alias documental exato MC-04 → MC-04-v2; persistir ambas as identidades. Divergência de G bloqueia por erro de referência.

Referência sintética de controle tem identidade própria, versão/hash e os mesmos dois campos de seleção, fixados manualmente. Não consultar a candidata para gerar expectativas dos testes. JSON com `expected` ausente no controle não é defeito: o avaliador de IDs não depende dessas saídas funcionais.

## 5. Avaliação derivada por dimensão

`avaliacao.json` conserva `avaliacao_id`, `avaliacao_anterior` quando houver, tentativa/observação, hashes dos originais e da referência, versão/hash do avaliador/contrato, política `ids-proposta-004-v2`, instante UTC e:

- `integridade`: estado e causas independentes.
- `estado_tecnico`: espelho da tentativa, não derivado da correção do conteúdo.
- `json_sintatico`: válido/inválido/não analisado; `formato_contrato`: válido/inválido/não analisado, com causa. Chave repetida é inválida para o parser estrito.
- `somente_ids_conhecidos`: indicador global e por dimensão, sem confundi-lo com sintaxe/estrutura.
- `requisitos` e `testes`: lista original extraída em ordem, duplicatas com posições (índice a partir de zero), desconhecidos únicos, S/G ordenados apenas para apresentação, listas de acertos/excedentes/omissões e TP/FP/FN.
- `metricas_propostas`: P/R/F por dimensão em frações numerador/denominador e decimal derivado; seleção completa e correspondência exata também identificadas como propostas. Nunca escore único RF+testes.
- `status_avaliacao`: `avaliada`, `resposta_formato_invalido`, `falha_tecnica`, `erro_referencia` ou `erro_integridade`, com causas disponíveis mesmo quando mais de um diagnóstico existe.

Resposta concluída de formato válido, mesmo com desconhecidos ou vazia, pode ser `avaliada`. Isso significa operação do avaliador concluída, não resposta correta. Acerto exato depende de S=G. Formato inválido deixa extração/conjuntos/contagens/escores **observados** nulos nas duas dimensões. Erro técnico/integridade/referência também não recebe escores. Campos de diagnóstico podem coexistir, sem preencher seleção por suposição.

Diretório novo de avaliação guarda original da tentativa, resposta/fragmento se existente, entrada importada identificada, referência na zona privada, avaliação e log. Arquivos parciais ou hashes divergentes impedem `completo=true`; conferir novamente ao fechar. Retentativa/reavaliação nunca sobrescreve registro anterior.

## 6. Resumo derivado opcional

Identidade própria, hash/versão de política e lista exata de avaliações incluídas/excluídas com causas. Por mudança/condição/origem:

- Planejadas N (lista explícita de observações), tentativas A, concluídas C, falhas técnicas finais T, formato válido V, inválido I, somente IDs conhecidos K; erros de referência/integridade/missing separados. Não supor C+T=N se há ausências/erros.
- Taxa de formato válido V/C, IDs conhecidos K/V, completude C/N; denominador zero dá indisponível. Publicar contagens junto, não só taxas.
- Resumo de seleção usa V respostas concluídas com integridade/referência válidas; desconhecidos são FP. Média por dimensão de P/R/F calculada sobre observações elegíveis, sem misturar células.
- Visão operacional, apenas se explicitamente pedida: V+I observações concluídas elegíveis tecnicamente; imputação de P/R/F zero só às I, identificada por observação; sem inventar S/G/TP/FP/FN observados. Falha técnica não entra nesse denominador.
- Jaccard: todos os pares de observações elegíveis de repetições distintas na mesma célula/dimensão, com IDs dos pares, numerador/denominador, contagem elegível/usada e média candidata. Invalidade/tentativa não cria par; menos de duas elegíveis informa estado nao_calculavel, motivo “não calculável”, valor nulo e número de observações/pares.

Sem resumo geral entre mudanças neste incremento. Nenhuma agregação oculta exclui “resposta ruim”. `origem=sintetica` acompanha cada linha e permanece explícita no resumo.

## 7. Controle sintético e estados

Cada fixture S-xx/subcaso tem bytes/registro de entrada, referência sintética fixa, expectativa literal de status/listas/TP/FP/FN/frações/denominadores, fundamento na regra e revisão técnica registrada antes da implementação. Resultado futuro inclui observado e conformidade/erro. Expectativa nunca é obtida pela função em teste.

Transições projetadas: pacote pendente → conferido tecnicamente ou reprovado; montagem → preparado local ou bloqueado; tentativa → concluída ou falha técnica; importação → avaliação ou erro/inválida; consolidação → completa só com integridade revalidada. Reavaliação gera nova identidade, sem transição destrutiva do original. Nenhum estado desta modelagem foi executado nesta fase documental.

## Convenção de identidade e grupos — D-26

`configuracao_id` é string não vazia nos manifestos/preparações/tentativas/avaliações; nos controles vale `controle-local-v1`, sem escolher modelo. `repeticao_sintetica` é inteiro positivo (bool excluído), conforme contrato técnico de importação dos controles. A identidade lógica é `(configuracao_id, mudanca canônica, condicao, repeticao_sintetica)`; `observacao_id` deve corresponder univocamente a ela. `tentativa_id` é único e `tentativa_anterior` vincula no máximo uma retentativa com o mesmo payload. Reavaliações têm IDs próprios; duplicar avaliações não cria observações extras.

O resumo mantém célula base configuração/mudança/condição e subgrupos explícitos por versão/hash da política e versão/hash da referência. Mistura de versões recebe diagnóstico/retorno 2 e nenhum resultado combinado; inventários de grupos homogêneos são apresentados separadamente, sem pontuação no resumo misto. Novo resumo com lista homogênea explícita pode calcular o grupo, sem presumir distribuição de N entre versões. Duplicidade de observação/repetição bloqueia métricas da célula afetada, preserva entradas e diagnósticos e não escolhe a melhor resposta. Outras células independentes podem ter resultados.

## Histórico técnico parcial — 27/10/2026 (substituído no alcance de D-29)

Implementados `montagem_entradas.py` e `avaliacao_ids.py`, sem rede/provedor. Convenções D-26 candidatas, política ids-proposta-004-v2; 39 tarefas independentes concluídas. T014/T015 e T042–T048 pendentes: runner isolado não provisionado e criação de symlink real negada com WinError1314. Não há fechamento integral. [Evidências e limites](../../evidencias/spec004/revisao-parcial/relatorio.md). As descrições anteriores datadas de planejamento/comandos futuros são históricas; comandos locais agora existentes só preparam/avaliam arquivos sintéticos, sem envio ou piloto. Métricas, notas definitivas, referência e desenho científico continuam sujeitos à revisão. Checklist de qualidade preservada, sem remarcação.

## Contrato textual verificável — D-29

Preparação editorial local em `fontes_autorizadas.py`, com seis caminhos fixos e recortes enumerados: instrução/notas/pedidos de materiais/04; definições integrais de materiais/07; contrato inicial de documentacao/requisitos; seis primeiras colunas da tabela T01–T12 de documentacao/qualidade-e-testes (sem coluna de destaques de RF); somente descrição de uma remoção na tabela da Spec 003; schema existente. Documentos mistos são lidos nessa edição local para selecionar os trechos, nunca enviados inteiros. A referência candidata não é lida nessa etapa.

`montagem_entradas.py`, contrato `spec004-v3`, lê pacote plano e `--autorizacao` externa explícita, fixando hashes de manifesto/documentos. Atualizar apenas seu próprio manifesto não autoriza texto alterado. A autorização é registro técnico controlado, não assinatura de autoridade ou detector semântico de qualquer gabarito: confrontar fontes, recortes, conteúdo e bytes. Mudança de fonte/recorte requer nova conferência; revisão profissional continua pendente. Fixtures v2 e comandos anteriores são históricos, preservados e não reexecutados como prova do contrato atual.

Somente `payload.txt` se destina ao modelo. Manifesto, autorização, cópias de documentos, fontes/hashes e `entrega-textual.json` são registros locais; não anexar diretório, código, fontes mistas ou referência. O recibo fixa texto/hash, `ferramentas=[]`, `anexos_ambiente=[]`, sem histórico e `envio_realizado=false`. Entrega real e ausência de ferramentas na plataforma serão conferidas antes do piloto; não foram exercitadas aqui, pois não há chamadas externas. Não se alega isolamento por SO.

Caminhos suportados: CLI com caminho local absoluto com drive ou relativo ao cwd; documentos do pacote filhos diretos com nomes enumerados; avaliador admite subdiretórios relativos declarados com separadores `/` ou `\`, confinados à raiz. Recusar drive relativo, raiz sem drive no Windows, UNC/dispositivos, streams `arquivo:fluxo`, dispositivos reservados, ponto/espaço final, componentes declarados vazios/`.`/`..` e links/junctions/reparse points. São controles de inclusão indevida, sem contas/permissões ou alegação de isolamento.

S-14 vigente verifica recortes/fontes, autorização independente, conteúdo proibido fictício em negativos, 16 combinações (quatro mudanças × quatro condições), texto exato e notas iguais D1/E1/ausentes D0/E0. Criação de symlink e negação de leitura por identidade são exigências antigas substituídas: não foram aprovadas. Esses objetos não pertencem às entradas suportadas; permanecem controles de recusa, sem exigir criação privilegiada para aceitar o contrato textual. PONT-01/PONT-02 e fórmulas candidatas não mudaram.



## Verificação vigente — 01/11/2026 (D-30)

Entidades locais acrescentadas em D-29 (fora do texto destinado ao modelo):

| Entidade | Campos e invariantes vigentes |
|---|---|
| Proveniência editorial | Seis fontes fixas, `arquivo`/`sha256`/`tamanho_bytes`; receita `recortes-D29-v1`. Seletores únicos de seção/campo, com recusa de ambiguidade; fontes mistas não enviadas inteiras. |
| Autorização externa | Versão `autorizacao-textual-v1`, status técnico de rascunho, hash exato do manifesto e lista ordenada de documentos/hashes. Fora do pacote/saída; original copiado para preparação. Registro técnico controlado, sem aprovação científica ou assinatura. |
| Preparação v3 | Contrato `spec004-v3`, hash da autorização, `fronteira=conteudo_textual_sem_ferramentas`, `isolamento_por_SO_alegado=false`; conserva todos os bytes e estado de preparado não enviado. Versão independente da política de pontuação v2. |
| Envelope local de entrega | `entrega-textual.json` fixa arquivo/hash do payload, ferramentas/anexos vazios, sem histórico, sem envio e sem alegação de SO. Somente payload é destinado ao modelo; entrega externa permanece não exercitada. |

Engenharia offline do contrato D-29 concluída no alcance verificado: 49 tarefas vigentes atendidas; T014/T015 substituídas, não executadas/aprovadas. Recortes das seis fontes, autorização externa e montagem v3 produziram 16 pacotes; bytes, conteúdo, documentos comuns, notas D1/E1 e ausência de notas D0/E0 confrontados. Referência somente no avaliador separado; resposta de demonstração explicitamente sintética. As 16 famílias estão consolidadas com evidências anteriores preservadas e verificações necessárias das alterações; não se reexecutou pontuação inalterada nem se contou sintéticos como LLM.

[Relatório e limitações](../../evidencias/spec004/revisao-textual-2026-11-01/relatorio.md) inclui comandos, esperado/observado, hashes, matriz, caminhos suportados, limitação da criação de symlink e provas de SO substituídas. As seções de 27/10 são históricas; os gates atuais são D-29 e esta verificação, sem aprovação retroativa. Checklist é qualidade documental, preservada sem remarcação. Sem prova de entrega real ao modelo, modelo escolhido, chamada externa ou piloto. Revisão profissional/científica, notas definitivas, fundamentação das métricas, desenho final/congelamento do piloto e adoção constitucional permanecem pendentes.
