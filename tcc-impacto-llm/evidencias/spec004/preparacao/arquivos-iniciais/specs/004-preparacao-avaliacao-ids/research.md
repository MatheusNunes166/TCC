# Pesquisa e decisões técnicas locais — Spec 004

27/10/2026. Pesquisa exclusivamente documental/local; sem navegação, chamadas externas, implementação ou controles executados. Autorização D-24 e registro técnico D-25 em [decisões](../../documentacao/decisoes.md). Revisão auxiliar somente de leitura prevista na skill `speckit-plan`, sem arquivos alterados pelo revisor.

## R-01 — Python e biblioteca padrão

**Decisão técnica proposta:** manter Python 3.11+ (3.13.3 disponível nesta sessão) e biblioteca padrão: argparse, pathlib, json, hashlib, datetime, uuid, fractions, itertools, unittest, tempfile e unittest.mock nos controles. Dois módulos pequenos e dois arquivos de testes, sem instalação.

**Justificativa:** conjunto fechado de oito documentos lógicos, quatro condições e dois universos de IDs dispensa framework, banco e cliente de provedor. Comparações são operações de conjuntos. Frações permitem expectativas exatas independentes de arredondamento.

**Alternativas consideradas:** jsonschema/pytest/pandas, serviço HTTP, motor genérico de schemas ou de experimentos. Não necessários; o validador aplicará somente o contrato específico do schema já existente. Não alegar implementação de JSON Schema completo.

## R-02 — Lista fechada e exportação editorial anterior à montagem

**Decisão:** pacote de entrada preparado fora do montador, reaproveitando apenas os recortes enumerados na Spec. O montador recebe manifesto e arquivos finais, não caminhos das fontes mistas. Proveniência completa e revisão permanecem em registro editorial externo; nenhuma rotina extrai automaticamente documentos do repositório.

**Justificativa:** requisitos e catálogo contêm avisos históricos e exemplos resolvidos fora das tabelas permitidas. Ler os documentos integrais em tempo de montagem viola a separação. Hash prova identidade com uma versão, não ausência semântica de gabarito; inspeção humana do conteúdo é indispensável.

**Alternativas:** glob de Markdown, busca recursiva, importar o projeto ou extrair contexto por agente de IDE. Rejeitadas. Não incluir gabarito, `expected`, `changed`, `preserved`, evidências, diffs, código ou histórico no pacote. A descrição de uma única mudança é texto permitido, não seu resultado resolvido.

## R-03 — Separação de processos e limite de acesso

**Decisão:** `montagem_entradas.py` não importa o avaliador nem aceita argumento de referência. `avaliacao_ids.py` recebe somente registro de entrada, resposta local/estado técnico e referência separada; não remonta entradas nem escreve no pacote. Comunicação exclusivamente por arquivos copiados em um sentido: montagem → avaliação.

Para verificação real de isolamento no Windows, preparar futuramente execução sob identidade local restrita, cuja leitura alcance somente cópia identificada do montador, pacote permitido e sua saída. Repositório de desenvolvimento, referência, evidências e diretórios da avaliação ficam sem permissão para essa identidade. A conta de avaliação tem leitura da referência e escrita apenas em resultados novos. O assistente de desenvolvimento continua fora desse contexto.

**Limite:** nenhum usuário/ACL/ambiente foi criado agora. Rodar os dois comandos sob a mesma conta ampla demonstra separação lógica, não ausência de acesso ao gabarito. Antes de alegar isolamento, exigir prova de leitura negada de arquivos sentinela fictícios nas zonas proibidas e inspeção dos arquivos efetivamente preparados, sem copiar dados privados para o controle. Se a identidade restrita não puder ser preparada, registrar gate pendente; não trocar silenciosamente por mera separação de pastas. Não adicionar contêiner/orquestrador/SDK de sandbox nesta capacidade.

## R-04 — Condições e notas em rascunho

**Decisão:** para a mesma mudança, conteúdo comum byte a byte idêntico em D0/D1/E0/E1; pedido direto igual em D0/D1; estruturado igual em E0/E1; notas idênticas em D1/E1 e entre mudanças. D0/E0 omitem integralmente o bloco de notas, inclusive delimitadores, sem texto compensatório e sem abrir `notas.md`, alinhando a ausência prevista na Spec.

Separar metadado `status_notas=RASCUNHO_NAO_REVISADO` do texto da nota. Não acrescentar esse rótulo somente ao conteúdo de D1/E1, o que mudaria o texto candidato. Todas as montagens desta capacidade são `PREPARADO_LOCAL_NAO_ENVIADO`, sem origem experimental, e nenhum rascunho recebe liberação de piloto. Preservar conteúdo atual e origem do pesquisador; nenhuma revisão profissional presumida.

**Alternativas:** notas diferentes por condição, texto com gabarito, introduzir exemplos resolvidos ou “compensar” ausência com instruções extras. Rejeitadas por confundir os fatores. Envelope vazio de notas foi descartado no detalhamento para manter ausência integral em D0/E0; esta composição fica explicitamente versionada.

## R-05 — Originais e versões

**Decisão:** entrada preparada é artefato UTF-8 determinístico com delimitadores fixos; preservar bytes e hash do manifesto, de cada documento e da composição final, versão do montador e contrato. Guardar cópias dos documentos efetivamente usados. Alterar delimitador/ordem gera versão nova.

Resposta fornecida ao avaliador é copiada em bytes antes de interpretar, mesmo quando malformada. O avaliador registra hash/versão de si, política e referência e grava resultado em diretório novo. Resposta ausente não produz arquivo artificial. Reavaliação cria avaliação nova ligada ao mesmo original; retentativa técnica liga tentativas da mesma observação.

**Alternativas:** armazenar só IDs extraídos, reserializar JSON como “original” ou sobrescrever saída de avaliação. Rejeitadas por perda de evidência.

## R-06 — Atenção: escolhas que afetam pontuação

As distinções abaixo foram destacadas antes de completar o plano. São convenções candidatas explícitas para verificação técnica, não aprovação científica. A Spec já estabelece os itens A–F; não se solicita nova adoção deles. Divergência futura exige decisão/versionamento, sem alterar originais.

| Ponto | Fonte e interpretação a preservar | Tratamento no desenho |
|---|---|---|
| A — inválida versus vazia | Protocolo §1.6 fala em vazios/zeros operacionais; Spec exige extração observada ausente e admite imputação separada. | Formato inválido: listas/conjuntos/métricas observados nulos. Visão operacional opcional, explicitamente pedida, pode imputar zeros com identificação. Falha técnica fica sem escore em ambas. |
| B — G de testes | A candidata contém `tests`, `changed`, `preserved` e `expected`. Eles têm papéis distintos. | G_RF=`rfs`, G_T=`tests`. Nunca usar somente `changed` ou inferir G das saídas `expected`. Relevantes incluem preservação. |
| C — desconhecido/duplicata | Spec determina FP para strings desconhecidas e conjunto único. | Não descartar desconhecidos nem normalizar IDs. Duplicata exata conta uma vez. Uma resposta com desconhecido mantém formato válido e indicador de IDs conhecidos negativo. |
| D — sem avaliação parcial | Contrato exige ambas as listas. | Uma lista com tipo inválido invalida formato do objeto inteiro; a outra não é pontuada isoladamente. Lista vazia válida não invalida o objeto. |
| E — vazios e consistência | Convenções da Spec para G não vazio, dois S vazios e pares insuficientes. | P/R/F zero para S vazio; Jaccard de dois vazios 1 com omissões expostas; menos de duas respostas elegíveis: indisponível. G vazio bloqueia, sem nova convenção automática. |
| F — tentativas e denominadores | Retentativa técnica não é repetição experimental. | Contar uma observação por identidade; conservar tentativas vinculadas. Usar única resposta concluída da observação; múltiplas concluídas sem adjudicação bloqueiam resumo, sem escolher a melhor. |
| G — detalhes de codificação/JSON | `json.loads` sozinho aceita chaves repetidas e constantes especiais. Schema estrutural não resolve esses casos. | Proposta técnica explícita: decodificação UTF-8 estrita, sem remoção de BOM; BOM/codificação inválida classificadas como formato inválido após preservar bytes. Rejeitar NaN/Infinity, chave repetida e texto residual. Registrar estes subcasos em S-09. Isso afeta taxa de validade e continua sujeito à revisão. |

**Mecanismo planejado:** `json.loads` com `object_pairs_hook` que detecta repetição e `parse_constant` que rejeita constantes não JSON; conferência de exatamente duas chaves, listas e strings. Espaços exteriores permitidos; sem cercas ou texto adicional. Separar sintaxe, estrutura, IDs conhecidos e estados técnicos no resultado; `json_valido` do modelo histórico isoladamente não basta.

**Mapeamento de referência:** alias documental exato MC-04 → MC-04-v2, já previsto; persistir valor pedido e canônico. Não aplicar aliases a IDs das respostas. JSON candidato permanece `CANDIDATO_NAO_REVISADO` com revisor/data nulos. A observação histórica de variantes não executadas é preservada e contextualizada pelo fechamento posterior da Spec 003, não regravada.

## R-07 — Cálculos sem interpretação científica antecipada

**Decisão proposta:** TP/FP/FN e listas separados para RF/testes. P/R/F e Jaccard em política candidata versionada `ids-proposta-004-v1`; frações exatas no registro, representação decimal apenas derivada. Contrato define denominadores, elegibilidade e escore indisponível. Sem nota conjunta, ranking de modelos, semelhança textual ou alegação de economia de regressão.

Resumo válido por mudança/condição, sem combinar mudanças neste incremento. Considerar todos os pares elegíveis, n(n−1)/2; pares não são novas observações independentes. Comparações científicas/agregação geral e fundamentos bibliográficos permanecem fora da entrega técnica, a revisar em P-02/P-03.

**Alternativas:** usar somente IDs conhecidos para melhorar precisão, transformar falha técnica em omissão do LLM ou escolher só pares favoráveis. Rejeitadas.

## R-08 — Esperados independentes e cobertura

**Decisão:** tabelas de controles revisadas manualmente antes da implementação, com entradas/bytes e esperados literais em fixtures futuras. Testes não chamam função de produção para gerar o próprio gabarito. S-01–S-16 expandidos no [contrato](contracts/preparacao-avaliacao.md), sem criar novas famílias, sem executar agora.

Referência sintética G_RF={RF-02}, G_T={T04,T12}; não derivá-la automaticamente da candidata, apesar da coincidência de IDs. Preservar histórico de falhas e novas tentativas em pastas próprias. Os controles de 004 não integram T01–T12, os 48 pares de 003 ou resultados de LLM.

## Fontes e conclusão da pesquisa local

Lidos: governança/constituição, Spec/checklist, encaminhamentos da orientação, arquitetura, materiais 01/04/07, schema, modelo de registro e estrutura da candidata 0.2. Não foi feita pesquisa bibliográfica ou consulta externa. Não há dependência técnica que exija biblioteca adicional. Questões científicas e prova de isolamento permanecem gates de uso futuro, não esclarecimentos técnicos resolvidos por esta pesquisa. Sem tarefas, código, pacote exportado, respostas experimentais ou chamadas.
