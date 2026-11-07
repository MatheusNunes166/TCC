# Coletor do piloto — entrega offline D-37, 07/11/2026

**Implementação e controles offline concluídos; envio real bloqueado. Nenhuma chamada ao LLM ou execução do piloto. Sem instalação, contratação de API, stage, commit ou push.** Responsável pela autorização: Matheus Henrique Braun Nunes; execução técnica pelo assistente, conforme [D-37](../../documentacao/decisoes.md). As capturas deste relatório são **artificiais**, sem resultados de pesquisa.

## Arquivos entregues

| Grupo | Arquivos |
|---|---|
| Implementação | [coletor_piloto.py](../../coletor_piloto.py): consultas locais, preparação, simulação, adaptador Codex bloqueado, motor sequencial, continuação/recuperação e avaliação separada |
| Ajuste do avaliador | [avaliacao_ids.py](../../avaliacao_ids.py): aceita modelo efetivo nulo explícito com causa; não altera pontuação, referência ou conjuntos |
| Controles novos | [test_coletor_piloto.py](../../tests/test_coletor_piloto.py), [substituto_coletor.py](../../tests/substituto_coletor.py); caso adicional em [test_avaliacao_real.py](../../tests/test_avaliacao_real.py) |
| Operação e contrato | [material 05, §5.11](../../materiais/05_PILOTO_E_COLETA.md#511-coletor-offline-d-37-07112026), [contrato Spec 004](../../specs/004-preparacao-avaliacao-ids/contracts/preparacao-avaliacao.md) |
| Governança/continuidade | [AGENTS](../../AGENTS.md), [ESTADO_ATUAL](../../ESTADO_ATUAL.md), [BLOQUEIOS](../../BLOQUEIOS.md), [HANDOFF](../../HANDOFF.md), [decisões](../../documentacao/decisoes.md), [arquitetura](../../documentacao/arquitetura.md), [qualidade](../../documentacao/qualidade-e-testes.md), [roadmap](../../documentacao/roadmap.md) |
| Artefatos novos preservados | `captura/conferencia-codex-2026-11-07/`, `captura/planejamento-piloto-2026-11-07/`, esta pasta de controles, `captura/controles-cli-2026-11-07/` e `avaliados/controles-cli-2026-11-07/` |

Os links deste relatório partem de `captura/controles-coletor-2026-11-07/`. As fontes originais, os 16 pacotes D-36, os exploratórios, a referência candidata, notas/prompts e históricos existentes não foram regravados. Os snapshots `fontes/` desta pasta são cópias literais dos produtores/testes usados, sem envio ao modelo.

## Instalação efetivamente consultada

[ambiente.json](../conferencia-codex-2026-11-07/ambiente.json) registra comandos/retornos; arquivos irmãos preservam stdout/stderr. Executável fornecido pela extensão VS Code `openai.chatgpt-26.1007.21434-win32-x64`, **codex-cli 0.162.0-alpha.17.2**. Todos os cinco comandos registrados retornaram 0: `--version`, `--help`, `exec --help`, `login status`, `debug models --bundled`. A primeira consulta dentro do sandbox não encontrou home; as consultas foram repetidas fora dele mediante permissão. Não se modificaram variáveis HOME/CODEX_HOME, configurações do usuário ou arquivos de autenticação.

`login status` informou autenticação via ChatGPT; nenhum token foi lido/exportado pelo coletor. Catálogo consultado com **`--bundled`**, sem atualização remota. O resumo [catalogo-embutido-stdout.txt](../conferencia-codex-2026-11-07/catalogo-embutido-stdout.txt) identifica exatamente `gpt-6-sol`, default e suporte a `medium`, `shell_type=unified_exec`, `apply_patch_tool_type=freeform`, `tool_mode=code_mode_only`, ferramentas experimentais `send_user_message_async`/`clock` e instruções base presentes (hash preservado). Isso demonstra capacidades embutidas, não acesso remoto ou modelo efetivamente usado.

[features-list.txt](../conferencia-codex-2026-11-07/features-list.txt) registra a consulta local adicional: shell, imagens, apps, plugins, navegador, computer use, multiagente, hooks e retentativas ilimitadas são recursos reconhecidos. A ajuda suporta `--disable`; o argv solicitado desativa os recursos enumerados na configuração, sem inventar `--tools=[]`. A lista efetiva enviada à plataforma não foi obtida. Desativar shell sozinho deixaria outras fontes de ferramentas possíveis.

Documentação oficial consultada para distinguir a interface dos controles efetivos: [exec não interativo](https://learn.chatgpt.com/docs/non-interactive-mode) documenta JSONL, eventos e retomada; [referência de configuração](https://learn.chatgpt.com/docs/config-file/config-reference) distingue shell, leitura de AGENTS e retentativas de requisição/stream. O suporte local de flags foi conferido pela ajuda, e nomes de recursos por `features list`; não se presume que toda chave publicada esteja implementada nesta versão. [Modelo GPT-6 Sol](https://developers.openai.com/api/docs/models/gpt-6-sol) foi consultado preservando o alvo solicitado. A skill OpenAI Docs orientou essa conferência, sem escolher outro modelo nem autorizar chamadas.

## Plano e payloads

[plano.json](../planejamento-piloto-2026-11-07/plano.json) foi preparado pelo comando `preparar`. Pesquisa de arquivos fora de `saidas-locais/` não encontrou ordem do piloto anterior; o plano canônico tinha ordem nula. Reutilizado o ordenador existente, semente **20261106**, gerador `random.Random`, shuffle de oito combinações em cada bloco (1 e 2), Python **3.13.3** completo registrado. Essa semente controla somente a ordem. `ordem_aprovada=false` preserva ausência de aprovação operacional/científica.

As 16 posições são MC-01/MC-03 × D0/D1/E0/E1 × duas repetições. Remontados oito pacotes a partir exclusivamente dos documentos exportados v2-LF, com ID solicitado `piloto-codex-gpt-6-sol-medium-D37`, pelo montador existente e novas autorizações vinculadas aos novos manifestos. Comparação explícita com cada payload v2-LF confirma **mesmos hashes/bytes**, sem alteração dos originais. Repetições compartilham os mesmos bytes e configuração. Os outros oito pacotes D-36 não foram incluídos no piloto.

`simular` não usa subprocesso LLM; verifica identidades, hashes/tamanhos, vínculos, nomes/caminhos sem links, composição e condições. Mostra argv de sessões novas com payload inteiro por stdin, gpt-6-sol/medium, efêmera/sem daemon, configuração do usuário/regras ignoradas e desativações solicitadas. Não força schema fora do payload. O controle de ambiente do filho remove variáveis de contexto do desenvolvimento e chaves de API. Não se alega isolamento por SO nem que essas medidas retirem instruções base/gerenciadas da plataforma.

## Verificações executadas

[testes.json](testes.json) conserva comandos, retornos, Python e hashes de fontes; logs `test_*-stdout.bin`/`test_*-stderr.bin` preservam bytes das saídas. [verificar_offline.py](verificar_offline.py) é o produtor, com criação exclusiva: para repetir, copiar o produtor para nova pasta sob `captura/`, sem sobrescrever esta execução.

| Grupo | Descobertos | Resultado |
|---|---:|---|
| Coletor | 11 | 11 aprovados |
| Avaliador sintético e importação real artificial | 22 | 22 aprovados |
| Montagem | 8 | 7 aprovados, 1 ignorado |
| Exportador | 5 | 5 aprovados |
| Total | **46** | **45 aprovados, 1 ignorado; zero falhas/erros** |

O teste de symlink real foi ignorado por **WinError 1314**, falta de privilégio do Windows; não se declara esse controle demonstrado. O controle de junction real passou. Não foram repetidas baseline/variantes, pois não sofreram mudanças. Não se fez novo teste de transporte Git ou commit temporário nesta entrega.

[operacao.json](operacao.json) registra sete verificações pela CLI real do coletor, produzidas por [conferir_operacao.py](conferir_operacao.py): ajuda 0; simulação 0; iniciar sem flag 2; iniciar com flag 2; controle local parcial 0; continuação local 0; avaliação sintética 0. Não foi criado lote real. Todos os processos filhos dessa captura são o substituto Python fixo, sem biblioteca de rede, chamadas ao Codex ou consulta do gabarito.

Controles demonstrados:

- 16 capturas **sintéticas**, cada uma com sessão local distinta, oito entradas únicas repetidas literalmente. Pausa após três tentativas e continuação das outras 13 sem reenvio das três concluídas. Eco do stdin igual ao payload preparado.
- Resposta com CRLF/espaços preservada literalmente; resposta inválida com cercas e resposta de zero bytes permanecem concluídas e não são reenviadas. Eventos brutos e todas as mensagens ficam preservados; final é extraído do último `item.completed/agent_message.text`, com UTF-8 e sem trim/correção/reescrita do JSON da resposta.
- Falha técnica com stderr/retorno 7; falha antes de iniciar o filho; continuação técnica única T02 vinculada a T01, mesmo payload/configuração, sem T03. A falha para o lote, permitindo corrigir indisponibilidade antes da continuação explícita.
- Interrupção conserva bytes parciais e tentativas concluídas anteriores. Estado de envio ambíguo não é reenviado automaticamente. Recuperação após salvar tentativa e antes de fechar inventário acontece sem enviar. Lock protege contra duas instâncias concorrentes.
- Ferramenta, turnos adicionais, modelo divergente, sessão compartilhada e eventos inesperados têm detecção no motor; testes dirigidos cobrem ferramenta/turnos/modelo. Desvio é preservado e bloqueia continuação automática. Não se infere conformidade de ausência de eventos de ferramentas ou de pontuação.
- Adulteração de captura, identidade, ordem, configuração/modelo, hash e traversal bloqueiam o fluxo. Plano, código e adaptador são congelados por hash; capturas fechadas são revalidadas antes da continuação/importação.
- Avaliação é etapa posterior sobre arquivos e referência explícita. Importação real artificial confere modelo desconhecido nulo com causa, preservando esse estado; nenhum valor solicitado vira modelo reportado. Inválidas têm seleções/medidas nulas. Todos os artefatos do smoke têm origem sintética/fase de verificação; o resumo não é resultado do piloto.

As tabelas JSON geradas pelo avaliador estão em [resumo/resumo.json](../../avaliados/controles-cli-2026-11-07/resumo/resumo.json); cada resposta/entrada original e avaliação fica na célula correspondente. A referência aparece somente na zona de avaliação. Ferramentas de envio não recebem resultados dessa etapa.

`git check-attr text filter ident` confirmou os três atributos **unset** em caminhos representativos de plano, captura e avaliação, cobertos pelas regras D-36 existentes. Não houve edição de `.gitattributes`, normalização de originais ou sobrescrita de evidências. `git diff --check` foi executado na revisão; avisos sobre conversão futura de código-fonte LF/CRLF não foram tratados como alteração de capturas.

## Pendências concretas e limite da entrega

1. **Fronteira D-29:** ausência de ferramentas e de contexto adicional ainda não demonstrada. Instruções base de agente existem no catálogo; não foi encontrado na ajuda um controle único que comprove sua remoção e inventário vazio. Novas verificações podem esclarecer capacidades, mas não se afirma impossibilidade definitiva da CLI nem conformidade já obtida. Não se executou `codex exec` para descobrir isso com uma chamada real.
2. **Retentativas internas:** recursos da CLI e documentação indicam reconexões/retentativas próprias. Limitar T01/T02 no coletor não limita sozinho requisições internas; falta demonstrar controle suportado nesta versão. Nenhuma chave de retry não verificada foi inventada no argv.
3. **Acesso/configuração remotos:** gpt-6-sol/medium comprovado somente no catálogo embutido. Modelo efetivamente reportado, limites, custo/orçamento e parâmetros não expostos continuam desconhecidos. O ramo real não foi exercitado; sua interoperabilidade de eventos precisa de validação futura autorizada.
4. **Revisão e autorização do início:** continuam as pendências científicas/operacionais do estado central, incluindo revisão dos materiais/referência/política/medidas e da ordem. Nenhuma aprovação atribuída ao orientador. O gate real exige novo incremento com evidências, sem opção para ignorá-lo.
5. **Interrupção ambígua:** o coletor não promete exatamente uma execução remota sem recibo/idempotência da plataforma. Quando não sabe se houve conclusão, preserva e bloqueia reenvio; não classifica silenciosamente como erro de transporte.

A configuração e a ordem estão prontas para conferência offline. O protocolo, payloads, conjuntos 2/4/8/5 e avaliação científica não foram ajustados a resultados. Exploratório MC-04 permanece separado; **não existe piloto real executado nesta entrega**.
