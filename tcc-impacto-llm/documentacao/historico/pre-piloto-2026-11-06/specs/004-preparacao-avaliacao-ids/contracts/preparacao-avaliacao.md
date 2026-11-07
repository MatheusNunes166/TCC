# Contrato local proposto — montagem e avaliação de IDs

> Contrato vigente — 01/11/2026 (D-29): o modelo recebe somente texto preparado, sem ferramentas, repositório, código, comandos, gabarito, resultados de variantes ou histórico. Exigências de identidade/ACL do Windows de T014/T015 substituídas, sem execução ou aprovação retroativa. Permanecem validação de arquivos/caminhos, autorização de conteúdo, integridade, equivalência de condições e avaliação separada. Notas representam conhecimento de analista de testes; texto definitivo e revisão profissional pendentes. Não se avaliam juniores, novos testes ou defeitos reais. Sem modelo escolhido, envio, chamadas externas ou piloto; revisão científica pendente. Histórico preservado em evidencias/spec004/revisao-textual-2026-11-01/originais.

> Convenções vigentes — 27/10/2026, D-26/D-27: o pesquisador adotou PONT-01/PONT-02 como convenções técnicas candidatas, ainda sujeitas à revisão científica. Política `ids-proposta-004-v2`: célula base por configuração/mudança/condição; versões de política ou referência distintas impedem resultado combinado, com diagnóstico e grupos separados por versão. Identidade lógica única por configuração/mudança/condição/repetição; duplicidades bloqueiam o resumo afetado sem escolha automática. Tentativas técnicas vinculadas não são repetições. Jaccard somente entre repetições distintas elegíveis, com número de observações/pares; menos de duas: **não calculável**. I1 corrigido: rejeitar links simbólicos internos/externos, junctions e todos os reparse points. Implementação e controles independentes autorizados, sem LLM/piloto. Registro de 27/10: isolamento por SO não demonstrado; exigência substituída por D-29, sem aprovação retroativa. Textos datados de somente planejamento/sem tarefas abaixo são históricos; originais preservados em evidências.

Contrato de arquivos/CLI implementado e verificado offline em D-29/D-30, sem API de rede. A declaração de não implementação de 27/10 permanece no original arquivado; não descreve a capacidade atual. [Spec](../spec.md), [research](../research.md) e [modelo](../data-model.md) compõem o contrato. Regras científicas continuam candidatas.

## 1. Fronteiras

| Processo | Leituras permitidas | Escritas | Exclusões |
|---|---|---|---|
| Edição local | Seis fontes fixas, com seletores de seções/campos enumerados | Recortes, manifestos e autorizações técnicas novos | Referência candidata, descoberta de arquivos e envio integral das fontes mistas |
| Montagem | Pacote e autorização externa explícita | Preparação/texto exato novos | Referência, recuperação de fontes adicionais e rede |
| Avaliação | Preparação copiada, registro de tentativa e resposta local, referência explícita | Diretório novo na zona de avaliação | Montar/enviar pedidos, alterar originais/pacote/referência, buscar arquivos automaticamente, rede |

Preparação, montagem e avaliação têm responsabilidades separadas; somente o avaliador lê a referência. O modelo recebe só o texto preparado, sem ferramentas de leitura do ambiente. Identidade restrita/sentinelas de leitura negada foram substituídas por D-29, sem execução ou aprovação retroativa.

## 2. CLI local vigente

```text
python -B fontes_autorizadas.py --raiz <repositorio-local> --saida <editorial-nova>
python -B montagem_entradas.py --pacote <raiz-permitida> --manifesto <manifesto.json> --autorizacao <catalogo-externo.json> --saida <pasta-nova>
python -B avaliacao_ids.py avaliar --preparacao <preparacao.json> --tentativa <tentativa.json> --referencia <referencia.json> --saida <pasta-nova> [--avaliacao-anterior <avaliacao.json>]
python -B avaliacao_ids.py resumir --avaliacoes <lista-explicita.json> --observacoes <lista-planejada.json> --saida <pasta-nova> [--imputar-invalidas]
```

Arquivos de lista enumeram caminhos/IDs/hashes exatos, sem glob ou busca recursiva. O manifesto determina mudança/condição; não permitir argumento que as substitua silenciosamente. `tentativa.json` aponta original/fragmento e origem sintética ou falha sem resposta. Não há `--modelo`, `--provedor`, credenciais ou comando de envio/retentativa automática.

Retornos propostos:

| Código | Montagem | Avaliar/resumir |
|---|---|---|
| 0 | Entrada local completa, sem envio e sem liberação científica | Registro completo de resposta de formato válido/resumo completo. Pontuação baixa ou desconhecidos podem retornar 0: não são falha de execução. |
| 1 | Não utilizado | Registro completo de formato inválido ou falha técnica importada; causa distinta no registro. Não significa defeito do avaliador. |
| 2 | Pacote/caminho/revisão/integridade/escrita inválidos; montagem bloqueada | Infraestrutura, referência, contrato de importação, conflito de observações ou persistência impedem avaliação utilizável. Prioritário sobre 1. |

Resumo com falhas técnicas/invalidade registradas pode existir, mas retorna 1 e informa incompletude/diagnósticos; 2 prevalece se há erro do mecanismo. Não interpretar código como escore nem falha técnica como resposta incorreta. Preservar stdout/stderr, retorno e versões na verificação futura.

## 3. Manifesto, composição e preservação

Um pacote por mudança/condição. Nomes permitidos exatos: `sistema.txt`, `definicoes-comuns.md`, `requisitos-baseline.md`, `catalogo-baseline.md`, `mudanca.md`, `pedido.txt`, `schema_saida.json`; acrescentar `notas.md` só em D1/E1. `manifesto.json` é metadado e não será enviado. A lista e recortes têm origem na tabela da Spec, não nos diretórios completos de materiais.

Conferir nomes exatos, unicidade dos papéis/paths, ordem, versões, hashes e tamanho. Somente filhos diretos da raiz; rejeitar absoluto, `..`, subdiretórios, links simbólicos/junctions/reparse points e destino real externo. Conferência direta dos nomes presentes na **raiz permitida** pode rejeitar extras; não é busca recursiva ou varredura do repositório. Pacote D0/E0 contém só sete documentos e manifesto; `notas.md` extra nesse pacote é erro, não arquivo a ignorar. Saída deve ser nova e fora da raiz de entrada; rejeitar caminho que sobreponha fontes, referência ou saída anterior.

Os documentos devem estar conferidos tecnicamente para preparação local, com status de rascunho preservado e `liberado_para_pesquisa=false`. Revisão pendente/reprovada ou contaminação conhecida bloqueia. Não prometer detecção semântica automática de gabarito: seu impedimento depende da preparação editorial/revisão, identidade dos bytes aprovados e fronteira de acesso. Em S-14, a contaminação artificial é rejeitada por revisão reprovada ou por hash diferente do conteúdo conferido.

Conteúdo de cada documento UTF-8 válido é preservado, sem trim ou alteração de quebras de linha. A composição utiliza, nesta versão, cabeçalho fixo `<<<inicio:<papel>>>` seguido de LF, bytes do documento, LF e `<<<fim:<papel>>>` seguido de LF. Delimitadores exatos e LF pertencem à versão do contrato. Não intercalar versões/hashes, paths, status de revisão ou IDs de seleção no payload.

Ordem e equivalências:

| Bloco | D0 | D1 | E0 | E1 |
|---|---|---|---|---|
| Sistema/definições/requisitos/catálogo/mudança/schema | Mesmo conteúdo para a mesma mudança nas quatro condições | Igual D0 | Igual D0 | Igual D0 |
| Notas | Bloco ausente | Texto N em rascunho | Bloco ausente | Mesmo texto N |
| Pedido | Direto P_D | Mesmo P_D | Estruturado P_E | Mesmo P_E |

Notas ausentes não produzem bloco nem delimitadores em D0/E0; nenhum arquivo de notas é aberto. N é o mesmo entre mudanças. Metadados registram `RASCUNHO_NAO_REVISADO` sem acrescentar rótulo ao texto candidato. Conferir hashes dos blocos comuns e igualdade byte a byte entre condições; o payload inteiro difere legitimamente por notas/pedido. A ordem coloca schema por último, como na Spec.

Armazenar payload exato, cópias dos documentos/manifesto e preparação com versões/hashes. Uma composição local não é mensagem enviada; só futura etapa autorizada poderá demonstrar correspondência ao conteúdo efetivamente enviado.

Na versão de montagem `spec004-v3`, `--autorizacao` é obrigatório. JSON externo `autorizacao-textual-v1`, `status=CONFERIDO_TECNICAMENTE_RASCUNHO`, `manifesto_sha256` e lista ordenada `documentos` (`arquivo`/`sha256`) devem corresponder exatamente ao pacote. Exportação conserva também fonte/hash/tamanho e receita `recortes-D29-v1`; copiar autorização em `autorizacao-original.json`. Não é assinatura nem detector semântico. `entrega-textual.json` é metadado local: payload/sha256, `ferramentas=[]`, `anexos_ambiente=[]`, `historico_conversa=false`, `envio_realizado=false`, `isolamento_por_SO_alegado=false`. Nenhum desses metadados entra no payload. Política de pontuação continua `ids-proposta-004-v2`, com versionamento independente do montador.

## 4. Importação e JSON estrito

Preservar resposta original em bytes antes de interpretar e vincular à preparação/tentativa. Resposta ausente é nula; arquivo recebido de zero bytes é presente e inválido. Fragmento de transporte nunca vira resposta concluída. Falha de copiar/ler íntegro é erro técnico do mecanismo, não erro de conteúdo.

Proposta explícita da política `ids-proposta-004-v2`: UTF-8 estrito sem remover BOM; BOM/codificação inválida classificadas como formato inválido, com bytes guardados. Parser rejeita chaves repetidas, NaN/Infinity e texto residual. Espaços JSON externos são aceitos. Usar hooks específicos da biblioteca padrão e validação manual do contrato existente; não implementar JSON Schema genérico.

Objeto final tem exatamente `requisitos` e `testes`, listas cujos itens são strings. Null, número, bool, objeto, campo extra/faltante, explicação/cercas externas ou truncamento invalidam **as duas dimensões**. Não normalizar IDs, reparar JSON, aproveitar parcialmente ou solicitar resposta melhor. Escapes JSON legítimos são decodificados segundo JSON: por exemplo `RF-\u0030\u0032` corresponde à mesma string `RF-02`; isso é interpretação sintática, não correção aproximada. Duplicatas são detectadas após essa decodificação; não aplicar normalização Unicode adicional.

Formato válido e IDs conhecidos são indicadores independentes. Recusa textual recebida é formato inválido. Registrar estados de sintaxe/estrutura/IDs/integridade/transporte separadamente; o antigo campo `json_valido` não substitui esse diagnóstico.

## 5. Referência e comparação

Somente o avaliador lê referência, em caminho explícito. Candidata atual versão 0.2; G_RF=`mudancas[id].rfs`, G_T=`mudancas[id].tests`. `changed`/`preserved`/`expected` não definem G. Exemplo de rastreabilidade documental: T12 está em G_T de MC-01 embora sua saída funcional seja preservada; não excluí-lo. Não executar variantes para descobrir G.

Validar versão/status, mudança única, universos e conjuntos não vazios/sem duplicata. Universos fechados: RF-01–RF-04, T01–T12. Alias exato de mudança MC-04 → MC-04-v2 já documentado; sem outros aliases, especialmente para respostas. Erro de referência impede escores; não editar fonte nem preencher lacunas pelo observado. Copiar referência apenas para zona privada de avaliação com hash/status de revisão, nunca para montagem.

Por dimensão, extrair lista em ordem e registrar repetições/posições. S é conjunto de strings distintas, **inclusive desconhecidas**. G é conjunto esperado. Calcular acertos=S∩G, excedentes=S−G e omissões=G−S. TP/FP/FN são suas cardinalidades. Exibir desconhecidos separadamente como subconjunto dos FP; excedentes podem conter IDs conhecidos que não são esperados. Não somar desconhecidos outra vez ao FP.

IDs com espaços/caixa diferente, vazio, alias ou da outra dimensão são strings desconhecidas e FP únicos. Item não string é erro de formato. Ordenação lexicográfica é só apresentação; não altera listas originais ou correspondência. Posições de duplicata começam em zero.

## 6. Fórmulas e convenções propostas

Estas escolhas permanecem sujeitas à fundamentação/revisão científica. Não avaliam texto/código ou compreensão interna do modelo.

| Medida por dimensão | Fórmula/convenção candidata |
|---|---|
| Precisão P | TP/(TP+FP); se S vazio e G não vazio, 0. |
| Revocação R | TP/(TP+FN); G não vazio é pré-condição. |
| F1 | 2TP/(2TP+FP+FN); S vazio/G não vazio dá 0. |
| Seleção completa | 1 se FN=0, senão 0; extra/desconhecido não apaga omissão nem equivale a exatidão. |
| Correspondência exata | 1 se S=G, senão 0. |
| Consistência Jaccard | Interseção/união de S de duas observações elegíveis da mesma mudança/condição, por dimensão. Dois S vazios: 1 com omissões/revocação expostas; menos de duas observações elegíveis: não calculável. |

Conservar frações exatas, inclusive médias, e decimal derivado sem arredondamento intermediário; proposta de exibição com seis casas, nunca usada para decidir conformidade. G vazio bloqueia, sem aplicar fórmula alternativa. Desconhecidos permanecem em S também no Jaccard.

### Resumos e ausências — distinção que afeta escores

O material histórico §1.6 propõe vazios/zero no resumo operacional. A Spec 004 determina que isso não é extração observada: resposta inválida mantém extração/TP/FP/FN/métricas **nulos**. Por padrão, só resumo de respostas de formato válido; opção explícita `--imputar-invalidas` acrescenta visão operacional separada de P/R/F com zeros identificados por observação. Não inferir seleção completa/exatidão/Jaccard a partir desses zeros e não inventar listas observadas vazias. Falhas técnicas não recebem escore, mesmo nessa visão.

Por célula: lista planejada contém N observações únicas; A tentativas; C observações tecnicamente concluídas com integridade/referência válidas; V de formato válido; I de formato inválido; T falhas técnicas finais. V+I=C; ausências/erros adicionais são relatados, sem forçar C+T=N. Taxas V/C, K/V (IDs conhecidos) e C/N usam contagens explícitas; denominador zero dá indisponível. P/R/F no resumo válido usam V; operacional usa V+I, não A ou N. Não produzir resumo geral entre mudanças.

Retentativa de transporte: somente uma candidata, mesmo payload/observação e vínculo à anterior. Não implementar transporte agora. Um registro concluído após falha é a resposta daquela observação; tentativa anterior permanece no log. Duas concluídas para a mesma observação causam conflito e bloqueiam resumo até adjudicação explícita, sem selecionar melhor escore. Jaccard usa todos os pares elegíveis de repetições distintas, n(n−1)/2; informar pares/IDs e exclusões; pares não são observações independentes.

## 7. Controles sintéticos e esperados independentes

Todos com origem `sintetica`, sem modelo, sem piloto. Fixar manualmente G_RF={RF-02}, G_T={T04,T12} e referências/bytes/esperados antes de implementar. Em tabelas abaixo, triplas significam TP/FP/FN; nada foi executado. O teste não pode chamar avaliador/parser de produção para gerar seu esperado. Expandir subcasos como fixtures separadas, sem criar novas famílias.

| Família | Entradas e esperado mínimo literal |
|---|---|
| S-01 exata | RF-02 e T04/T12: RF=1/0/0, T=2/0/0; P/R/F=1, exata/completa=1 nas duas. |
| S-02 parcial | RF-02 e T04: RF=1/0/0; T=1/0/1, P=1, R=1/2, F=2/3; T completa/exata=0. |
| S-03 todos | RFs quatro e testes doze: RF=1/3/0, P=1/4,R=1,F=2/5; T=2/10/0,P=1/6,R=1,F=2/7. Completa=1/exata=0 em ambas. |
| S-04 vazias | Ambas []; RF=0/0/1,T=0/0/2; P/R/F=0, completa/exata=0. Formato válido, zero desconhecidos. |
| S-05 duplicatas/ordem | RF-02 duas vezes, T12/T04/T04: contagens de S-01; repetições em posições 1 e 2 respectivamente, únicas por dimensão. Subcaso com escape JSON equivalente mantém mesmo ID decodificado. |
| S-06 desconhecidos | RF-02/RF-99/RF-99, T04/T12/T99/T99: RF=1/1/0,P=1/2,R=1,F=2/3; T=2/1/0,P=2/3,R=1,F=4/5. Um desconhecido único por dimensão; completa=1/exata=0. |
| S-07 sem correção | `rf-02` e `T4`: RF=0/1/1,T=0/1/2,P/R/F=0. Subcasos independentes com espaço exterior ao ID, vazio e caixa; desconhecidos únicos, sem normalizar. |
| S-08 dimensão trocada | requisitos=[T04],testes=[RF-02]: RF=0/1/1,T=0/1/2; P/R/F=0. Não transferir. |
| S-09 inválidas | Subcasos separados: objeto sem uma chave, chave extra, null/lista errada, item numérico/bool/objeto, chave repetida, texto/cercas, truncamento, recusa, original vazio recebido, BOM, UTF-8 inválido, NaN/Infinity. Todos formato inválido, sem extração/métricas observadas nas duas dimensões; copiar bytes integralmente. Controle positivo: espaços exteriores e escape JSON legítimo válidos. |
| S-10 independência | RF=[],T04/T12: RF=0/0/1,P/R/F=0; T=2/0/0,P/R/F=1; não nota conjunta. |
| S-11 técnicas | (a) nenhuma resposta: falha técnica, original ausente; (b) fragmento, inclusive JSON incidentalmente parseável: bruto preservado, sem seleção/escore. Ambos fora de V/I, retorno 1 se registro completo. |
| S-12 referência | Subcasos: G vazio, mudança ausente/duplicada, versão ausente, ID esperado duplicado/desconhecido, lista com tipo errado. Todos erro de referência, retorno 2, sem escore, fonte intacta. Referência sintética fixa válida é controle positivo. Alias MC-04 é mapeamento de mudança, não ID de resposta. |
| S-13 integridade | Subcasos: payload/original alterado após importação, hash divergente, arquivo removido antes de fechar, escrita parcial, pasta de saída repetida. Detectar, retorno 2, sem fechamento completo; nova avaliação com ID novo preserva a anterior. |
| S-14 vigente | Verificar fontes/recortes enumerados, autorização e negativos de inclusão indevida; 16 pacotes/condições/notas/texto exato. Exigências antigas de identidade/criação privilegiada substituídas por D-29, não aprovadas. |
| S-15 Jaccard | S-01×S-02: RF=1,T=1/2; dois S-04 de repetições distintas: 1/1 com FN=1/2 expostos. Para três seleções T={T04,T12},{T04},{}: 3 pares, valores 1/2,0,0, média 1/6; RF={RF-02},{RF-02},{}: média 1/3. Um válido sozinho: sem par, não calculável; inválida/tentativa excluída com causa. |
| S-16 resumos | Cenário A: N=3,A=3,C=2,V=1,I=1,T=1,K=1,completude=2/3,validade=1/2,conhecidos=1; uma exata, uma inválida e uma falha técnica. P/R/F válido=1, operacional=1/2 por dimensão, técnica sem escore, Jaccard não calculável. Cenário B: N=1,A=2,C=1,V=1,I=0,T=0, primeira tentativa técnica falhou e segunda exata com payload idêntico: taxas=1 e uma única observação. Subcasos: segunda falha (C=0,T=1, taxas de conteúdo indisponíveis), payload diferente na retentativa, duas concluídas para mesmo ID (erro 2), lista planejada com ausente (completude menor, ausência explícita). |

O detalhamento de S-16 adiciona diagnóstico de contrato/identidade; não executa retentativa real. Esperados de contagens, estados ausentes/imputados e frações devem ser conferidos independentemente por leitura das fórmulas, sem usar saídas do código futuro como gabarito.

## 8. Gates e limites

Saída íntegra/conforme de controle demonstra comportamento técnico local. Não aprova referência, notas, políticas ou medidas. Antes de pesquisa: revisão profissional/científica registrada, notas definitivas, fundamentação/revisão das convenções, fronteira de acesso demonstrada e desenho final do piloto/configuração/orçamento/congelamento próprios. T12 já adotado em B; sem novo pedido de adoção. Sem modelos, rede, coleta, interface/API ou código nesta entrega.

## 9. Convenções candidatas adotadas — D-26

PONT-01/PONT-02 e I1 conforme complemento vigente. `configuracao_id` não vazio e `repeticao_sintetica` inteiro positivo identificam controles locais, sem configuração de provedor. Listas explícitas de importação/resumo usam itens `arquivo`/`sha256`; a lista planejada identifica observação, configuração, mudança, condição, repetição e payload hash. Tentativas técnicas têm no máximo dois IDs encadeados, mesmo payload e uma única resposta concluída. Observações duplicadas, IDs em células diferentes ou reavaliações sem seleção explícita bloqueiam a célula afetada; não deduplicar por pontuação.

Não combinar hashes/versões distintos de política/referência. Resultado contém diagnóstico de mistura e inventários de grupos homogêneos separados, sem média combinada. A tentativa mista não pontua esses grupos; novo resumo requer lista homogênea explícita para não presumir denominadores planejados. Jaccard registra observações elegíveis e pares utilizados por dimensão; menos de duas resulta `estado=nao_calculavel`, `motivo=não calculável`, valor nulo e zero pares. Os subcasos de S-16 cobrem versões misturadas, duplicidade de repetição/observação e tentativas vinculadas; S-14 cobre também links internos, junctions e todos os reparse points. Essas regras são convenções técnicas do pesquisador sujeitas à revisão científica.

## Histórico técnico parcial — 27/10/2026 (substituído no alcance de D-29)

Implementados `montagem_entradas.py` e `avaliacao_ids.py`, sem rede/provedor. Convenções D-26 candidatas, política ids-proposta-004-v2; 39 tarefas independentes concluídas. T014/T015 e T042–T048 pendentes: runner isolado não provisionado e criação de symlink real negada com WinError1314. Não há fechamento integral. [Evidências e limites](../../../evidencias/spec004/revisao-parcial/relatorio.md). As descrições anteriores datadas de planejamento/comandos futuros são históricas; comandos locais agora existentes só preparam/avaliam arquivos sintéticos, sem envio ou piloto. Métricas, notas definitivas, referência e desenho científico continuam sujeitos à revisão. Checklist de qualidade preservada, sem remarcação.

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

[Relatório e limitações](../../../evidencias/spec004/revisao-textual-2026-11-01/relatorio.md) inclui comandos, esperado/observado, hashes, matriz, caminhos suportados, limitação da criação de symlink e provas de SO substituídas. As seções de 27/10 são históricas; os gates atuais são D-29 e esta verificação, sem aprovação retroativa. Checklist é qualidade documental, preservada sem remarcação. Sem prova de entrega real ao modelo, modelo escolhido, chamada externa ou piloto. Revisão profissional/científica, notas definitivas, fundamentação das métricas, desenho final/congelamento do piloto e adoção constitucional permanecem pendentes.
