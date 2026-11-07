# D-38 — análise delimitada da CLI, 07/11/2026

**Os dois bloqueios permanecem pendentes.** Foram demonstrados controles parciais de configuração e uma incompatibilidade concreta da rota embutida de retentativas. Nenhum `codex exec`, criação de thread/turno de modelo, chamada ao LLM, piloto, instalação, migração de provedor, stage, commit ou push. O coletor conserva sua trava incondicional de envio.

## Escopo e compatibilidade das fontes

Autorização: pedido do pesquisador nesta conversa, análise de ferramentas/contexto e retries, com ajustes locais comprovados e verificações offline. Responsável: Matheus Henrique Braun Nunes; execução técnica pelo assistente. [D-38](../../documentacao/decisoes.md) registra alcance e limites.

A documentação oficial consultada é corrente, **não uma documentação congelada da versão alpha**. A compatibilidade foi conferida pontualmente no binário instalado: ajuda, pacote, schema de protocolo gerado por ele, parser estrito e consultas locais por IPC. Nenhuma afirmação de efeito em transporte foi deduzida somente da documentação ou de parsing bem-sucedido. A skill OpenAI Docs orientou esse confronto.

Fontes oficiais: [configuração](https://learn.chatgpt.com/docs/config-file/config-reference) para skills/memórias e definições por provedor; [configuração avançada](https://learn.chatgpt.com/docs/config-file/config-advanced#azure-provider-and-per-provider-tuning) para tuning de HTTP/stream e reserva do provedor `openai`; [precedência](https://learn.chatgpt.com/docs/config-file/config-basic) para configuração em camadas. A documentação descreve defaults HTTP=4 e streaming=5 para os campos de provedor; **esses números não foram medidos na rota ChatGPT desta instalação**.

## Instalação, autenticação e subprocesso

[inspecao.json](inspecao.json) identifica executável, SHA-256, versão e comandos: **codex-cli 0.162.0-alpha.17.2**, extensão VS Code `26.1007.21434`, Windows x86_64. `login status`, recebendo o **mesmo ambiente filtrado do coletor**, informou **Logged in using ChatGPT** em [autenticacao-stderr.bin](autenticacao-stderr.bin). Nenhum token ou auth.json foi lido/exportado pelos scripts. A consulta fora do sandbox foi autorizada porque dentro dele a CLI não encontra o diretório do usuário.

[subprocesso-solicitado.json](subprocesso-solicitado.json) registra o argv/env/configuração na fronteira do coletor. O ramo real **não foi iniciado**; portanto não existe configuração runtime de uma execução real a certificar. Os controles são:

| Origem | Solicitado pelo coletor D-38 | Evidência/limite |
|---|---|---|
| Modelo/provedor/auth | gpt-6-sol, medium, `model_provider="openai"`, `forced_login_method="chatgpt"` | Modelo/esforço/provedor/auth explícitos aceitos em config/read; não prova acesso remoto |
| Configuração herdada | `--ignore-user-config`, `--ignore-rules`, `--strict-config`, nenhum profile | Ajuda do **exec**; ignore-rules trata execpolicy, não todas as configurações ou instruções |
| Instruções de projeto | `project_doc_max_bytes=0` | Sentinela de AGENTS ausente no render local; não desativa por si `.codex/config.toml` ou requisitos gerenciados |
| Skills/memórias | `skills.include_instructions=false`; `memories.use_memories=false`; `memories.generate_memories=false` | Parser nativo aceita; instruções automáticas de skills ausentes no render. Não elimina automaticamente ferramentas de todos os tipos |
| Plugins/apps/hooks e ferramentas | Lista existente `--disable` preservada, web_search disabled | Recursos configurados false no config/read, sem inventário de tools do request |
| Histórico/ambiente | Novo exec, sem resume/fork/daemon, efêmero, stdin integral; allowlist de variáveis | Testes no coletor; CODEX_THREAD_ID, instruções via ambiente e chaves de API não são herdados |
| Pasta/sandbox | Pasta nova, sandbox read-only | Medidas de ambiente; **não demonstram ausência de ferramentas** |

O allowlist do filho contém apenas variáveis de sistema/caminho/perfil/temporários/idioma. Não se alterou HOME/CODEX_HOME. O argv não inclui anexos, schema forçado adicional ou instruções de reparo. Os novos campos ficaram congelados em configuração/ID D-38, sem substituir GPT-6 Sol por GPT-6.1 Sol.

### Camadas realmente observadas e diferença entre interfaces

[config-base.json](config-base.json) é uma consulta do **app-server**, não do exec. Ela reporta camadas sessionFlags, user e system. A camada user fornece gpt-6.1-sol/high nesse diagnóstico sem overrides de modelo; **não é o modelo escolhido pelo coletor**. [config-ajustes-aplicados.json](config-ajustes-aplicados.json), com os overrides explícitos, retorna gpt-6-sol/medium/openai/chatgpt, read-only e controles false.

Essa API não oferece a flag `exec --ignore-user-config`; logo não se apresentam suas camadas como equivalentes às da futura coleta. [fontes-configuracao-metadados.json](fontes-configuracao-metadados.json) registra existência, hash e nomes de chaves sem conteúdo sensível: o arquivo de usuário existe e contém model/effort/projects/windows; os caminhos de sistema testados não existem. Uma origem system enumerada pelo config/read **não prova arquivo de sistema presente ou conteúdo gerenciado ativo**. Não se editou qualquer configuração do usuário/sistema.

Não foi encontrado MCP configurado nesse config/read (`mcp={}`), nem plugin configurado na sua visão. Isso é ausência de entradas nessa consulta, **não indisponibilidade global de MCP/plugins**. Desativar um MCP conhecido requer `mcp_servers.<id>.enabled=false`; um mapa vazio não foi usado como suposta limpeza de herança. Configurações do projeto confiável, requisitos administrados e fontes de ferramentas do cliente continuam exigindo inspeção na rota efetiva. Não existe na ajuda consultada um comando que certifique todo esse conjunto como indisponível.

### O que o render offline demonstrou

`debug prompt-input` apenas renderizou uma sentinela artificial local, sem execução de modelo. [contexto-ajustes-aplicados.json](contexto-ajustes-aplicados.json) e seu stdout original mostram:

- A sentinela `D38_SENTINELA_PAYLOAD_ARTIFICIAL` aparece; a sentinela colocada em AGENTS.md não aparece com o limite zero.
- `<skills_instructions>` não aparece após o controle explícito.
- Permanecem **três mensagens developer, quatro partes de instrução**, e uma mensagem user de `<environment_context>` além da mensagem user da sentinela. São instruções de permissões/modo/coordenação e descrição do ambiente; não se atribui sua origem a um arquivo particular sem evidência.
- O JSON é uma lista de itens de input. **Não contém o envelope completo `instructions`/`tools` de uma requisição ao provedor.** O catálogo embutido D-37 também contém base_instructions e capacidades de agente. O render não é prova de que esse catálogo inteiro vira contexto ou de que qualquer tool específica foi efetivamente oferecida.

O debug não possui as flags exclusivas de exec `--ignore-user-config`/`--ignore-rules`; o render é uma evidência local limitada, não o request experimental. Ainda assim, demonstra que a configuração parcial não produz por si um input exclusivamente igual ao payload. `model_instructions_file` é documentado como substituição de instruções base; **não foi aplicado arquivo vazio** como se isso retirasse mensagens developer, environment, MCP e ferramentas. Essa remoção integral não foi demonstrada.

### Distinções exigidas

| Estado | O que se pode afirmar |
|---|---|
| Configurado como desativado | Valores false aceitos e retornados pelo parser/config manager; web disabled, leitura de AGENTS limitada, skills e memórias desligadas por chaves específicas |
| Comprovadamente indisponível | Não há prova global de ferramentas indisponíveis ao modelo. No controle local, a sentinela AGENTS e certas variáveis/instruções não entram nos artefatos inspecionados; a garantia fica restrita a esse teste |
| Disponível, mas não utilizado | Um recurso habilitado em features/defaults ou anunciado no catálogo não certifica disponibilidade efetiva. Não houve sessão LLM; portanto não se produziu observação experimental dessa categoria. Zero invocações nunca é usado como prova de indisponibilidade |

**Situação ferramentas/contexto: pendente.** D-29 exige payload textual sem ferramentas/contexto adicional; o coletor ainda não dispõe de prova da fronteira na rota exec. O diagnóstico não autoriza relaxar D-29 nem chamar uma execução com contexto adicional de conforme.

## Retentativas de transporte

### Valores aceitos, efeito documentado e aplicabilidade

[config-custom-zero.json](config-custom-zero.json) preserva ambos os campos com **0** na definição de um provedor personalizado de controle, não selecionado. [config-custom-one.json](config-custom-one.json) confirma **1**. Negativos são recusados com `expected u64` nos dois campos; texto `"zero"` também é rejeitado. São valores **aceitos pelo parser**, sem demonstração de número de requisições executadas.

`request_max_retries` é documentado como orçamento de retry HTTP; `stream_max_retries`, de recuperação de interrupção do stream. A documentação consultada não especifica de forma suficiente a semântica operacional de zero nesta versão alpha. Não se fez inferência de “zero desliga” a partir de unsigned/aceitação. Não foi realizado teste HTTP nem SSE com provedor real ou substituto nesta entrega.

A limitação concreta da autenticação atual está em [config-builtin-zero.json](config-builtin-zero.json): o binário rejeita `model_providers.openai` com **reserved built-in provider IDs / Built-in providers cannot be overridden**. A documentação avançada confirma essa reserva. Logo, os campos da definição personalizada **não podem ser aplicados desse modo ao provedor embutido escolhido com login ChatGPT**. Alterar somente openai_base_url não demonstra alteração do orçamento de retries. Criar/selectar `openai-custom` mudaria a rota/provedor e sua autenticação; não foi feito automaticamente.

`--disable unbounded_connection_retries` continua aplicado e o config manager retorna false. Isso só demonstra que o recurso denominado “unbounded” está false; **não estabelece zero retries, zero reconexões ou zero novas requisições**. Os valores efetivos request_max_retries/stream_max_retries da rota embutida permanecem **desconhecidos**, não zeros inventados.

As primeiras tentativas de usar `features list --strict-config` foram rejeitadas porque essa versão não suporta strict-config nesse subcomando, antes de validar chaves. Os arquivos são preservados como verificações inconclusivas, não como rejeição de zero. A validação subsequente foi feita pelo app-server com parser estrito. O controle de chave deliberadamente inexistente foi recusado, confirmando o funcionamento desse parser. `--strict-config` existe na ajuda do exec e foi acrescentado ao coletor.

### Transporte, geração, turno e observação

Uma observação continua sendo a célula/ID planejado; T01 e T02 são tentativas do coletor vinculadas, não repetições independentes. Um turno pode envolver mais de uma requisição/conexão interna. Uma reconexão pode recuperar o mesmo stream ou levar o cliente a reenviar algo; sem identificadores/recibos observáveis não se afirma que foi a mesma geração nem uma geração nova. Texto de reconnect ou evento genérico error não fornece contagem confiável de POSTs/gerações.

Foi corrigido um caso local: **error seguido de mensagem final e turn.completed no mesmo turno** conserva estado concluída e a resposta literal, registra desvio e bloqueia continuação para conferência. Antes, qualquer error fazia a captura parecer falha técnica, arriscando outra geração em T02 apesar de um final íntegro. Os registros agora distinguem erros de cliente e turnos iniciados observados; `retentativas_transporte_observadas=null` conserva a falta de evidência. Não se conta um reconnect como nova observação. Eventos terminais conflitantes também geram desvio.

A retentativa técnica do protocolo permanece no coletor, no máximo uma, após falha técnica e continuação explícita; respostas inválidas/concluídas não são repetidas. **Situação retentativas da CLI: pendente** para a rota atual. Nenhuma garantia se estende a mecanismos internos não expostos do provedor, mesmo se controles do cliente forem demonstrados no futuro.

## Ajustes, testes e preservação

Alterações limitadas a `coletor_piloto.py`, `tests/test_controles_cli.py`, um teste novo em `tests/test_coletor_piloto.py` e documentação afetada. Sem mudança no avaliador, protocolo de pontuação, payloads, referência, notas ou resultados. [validacao-offline.json](validacao-offline.json) e os logs registram **16 testes aprovados**: quatro de controles CLI e doze do coletor; zero falhas/erros/ignorados. Os subprocessos dos testes são exclusivamente substitutos Python locais. A simulação retorna 0 e `iniciar --enviar-real` retorna 2 sem criar lote real. Um teste esvazia a lista de bloqueios e confirma que a trava incondicional continua levantando erro.

O coletor anterior está preservado literalmente em [coletor-antes-D38.py](coletor-antes-D38.py); planos/capturas/avaliações D-37 não foram regravados. [Novo plano D-38](../planejamento-piloto-2026-11-07-D38/plano.json) reutiliza **a ordem já registrada** e mantém os oito hashes de payload anteriores, agora com ID/configuração/hash de produtor novos. O plano D-37 deixa de passar no coletor atualizado por diferença de configuração/código; isso é bloqueio de integridade deliberado, não razão para editar evidência antiga. Fontes testadas D-38 ficam em `fontes-D38/`.

## Verificações futuras, não executadas

Offline, ainda seria possível instrumentar o cliente contra um endpoint substituto **exclusivamente local**, sem credenciais ou LLM, para capturar envelope instructions/tools e provocar HTTP 503/SSE truncado. Isso demonstraria comportamento somente daquela rota/configuração; um custom provider local não prova o transporte do provedor embutido ChatGPT. Não se criou esse transporte/infraestrutura nem se extrapolaram resultados de parser para ele.

Uma verificação futura **com chamada real**, se especificamente autorizada e após resolver as incompatibilidades, precisaria capturar de forma segura o envelope efetivamente entregue e seus recibos/configuração na rota de produção: modelo reportado, tools realmente oferecidas (inclusive diferidas/Code Mode), messages/instructions adicionais, identificadores de request/turno/resposta e eventos de transporte. Teria de confirmar que novas observações não recebem histórico/material externo. A resposta do modelo dizendo “não tenho ferramentas” ou simplesmente não chamar tools não seria prova. Provocar falhas reais para medir retries também não está autorizado e não controlaria mecanismos privados do servidor.

## Menor alternativa viável, apenas proposta

Se a rota CLI instalada continuar incompatível com D-29, a menor alternativa técnica é um **adaptador HTTP direto à Responses API**, usando biblioteca padrão, sem agente, plugins, MCP ou serviço persistente. Enviaria somente o payload como entrada textual, sem conversa anterior, tools fornecidas vazias e sem instruções adicionais do cliente; resposta não streaming simplificaria a captura. O cliente não teria loop automático de retries: o único retry técnico continuaria no coletor, com falhas ambíguas preservadas/bloqueadas. Isso delimitaria a garantia ao cliente; não removeria políticas internas do provedor.

Impactos: autenticação própria de API/conta habilitada, sem reutilização ou exportação automática dos tokens do login ChatGPT; orçamento e possíveis cobranças por uso/créditos da API precisam ser conferidos, sem presumir cobertura pelo login da CLI ([autenticação e início](https://developers.openai.com/api/docs/quickstart), [preços](https://developers.openai.com/api/docs/pricing)). GPT-6 Sol/medium permanece solicitado, sujeito ao acesso real dessa conta. O desenho conservaria payloads, ordem, 16 observações e avaliador, mas exigiria registrar nova modalidade/configuração, autenticação, limites/orçamento e provas de entrega/retry, além da autorização de início; não misturar silenciosamente coortes CLI/API. [Geração textual pela API](https://developers.openai.com/api/docs/guides/text).

**A alternativa não foi implementada, contratada ou executada.** Manter a CLI sem prova implicaria alterar D-29 para permitir explicitamente contexto/ferramentas de agente, uma decisão científica nova, não um simples ajuste local.

| Bloqueio | Causa | Configuração aplicada | Evidência | Situação |
|---|---|---|---|---|
| Ferramentas/contexto | Render ainda contém mensagens adicionais; falta envelope/inventário real de tools na rota exec | Skills/memórias false, provedor/auth explícitos, strict-config; controles anteriores preservados | config-ajustes-aplicados + contexto-ajustes-aplicados + testes | **Pendente** |
| Retentativas internas | Provedor embutido openai é reservado; zero apenas aceito no parser de custom provider, sem semântica de transporte demonstrada | Unbounded=false preservado; não aplicados overrides inválidos; final após error não gera retry automático | config-builtin-zero + custom-zero/one/negativos + testes | **Pendente** |
