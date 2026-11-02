# Modelo de dados proposto — Spec 004

> Convenções vigentes — 27/10/2026, D-26/D-27: o pesquisador adotou PONT-01/PONT-02 como convenções técnicas candidatas, ainda sujeitas à revisão científica. Política `ids-proposta-004-v2`: célula base por configuração/mudança/condição; versões de política ou referência distintas impedem resultado combinado, com diagnóstico e grupos separados por versão. Identidade lógica única por configuração/mudança/condição/repetição; duplicidades bloqueiam o resumo afetado sem escolha automática. Tentativas técnicas vinculadas não são repetições. Jaccard somente entre repetições distintas elegíveis, com número de observações/pares; menos de duas: **não calculável**. I1 corrigido: rejeitar links simbólicos internos/externos, junctions e todos os reparse points. Implementação e controles independentes autorizados, sem LLM/piloto. Isolamento real não demonstrado; T014/T015 e dependentes permanecem pendentes. Textos datados de somente planejamento/sem tarefas abaixo são históricos; originais preservados em evidências.

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

## Estado técnico parcial — 27/10/2026

Implementados `montagem_entradas.py` e `avaliacao_ids.py`, sem rede/provedor. Convenções D-26 candidatas, política ids-proposta-004-v2; 39 tarefas independentes concluídas. T014/T015 e T042–T048 pendentes: runner isolado não provisionado e criação de symlink real negada com WinError1314. Não há fechamento integral. [Evidências e limites](../../evidencias/spec004/revisao-parcial/relatorio.md). As descrições anteriores datadas de planejamento/comandos futuros são históricas; comandos locais agora existentes só preparam/avaliam arquivos sintéticos, sem envio ou piloto. Métricas, notas definitivas, referência e desenho científico continuam sujeitos à revisão. Checklist de qualidade preservada, sem remarcação.

