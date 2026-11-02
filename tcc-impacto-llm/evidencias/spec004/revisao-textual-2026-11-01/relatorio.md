# Verificação local do contrato textual — Spec 004

01/11/2026, assistente sob autorização do pesquisador D-29; registro técnico D-30 em [decisões](../../../documentacao/decisoes.md). Datas UTC nos registros de execução podem ser 02/11, correspondendo à noite de 01/11 em America/Sao_Paulo. Spec ativa `004-preparacao-avaliacao-ids`, confirmada pelo fluxo local antes das alterações. Python 3.13.3, biblioteca padrão; sem provedor, modelo escolhido, rede, LLM ou piloto.

## Resultado e alcance

Concluídas as 49 tarefas vigentes de engenharia offline. T014/T015 permanecem desmarcadas, **substituídas por D-29 e não executadas/aprovadas**. O contrato antigo exigia runner com identidade Windows separada; o contrato vigente exige texto autorizado verificável e entrega futura ao modelo sem ferramentas/acesso adicional. Não se alega isolamento por sistema operacional. Relatórios de 27/10 e suas limitações permanecem inalterados; não se convertem provas ausentes em resultados positivos.

Somente `payload.txt` se destina ao LLM. Manifesto, autorização, diretórios, proveniência, código e evidências são registros locais. `entrega-textual.json` registra hash/arquivo, ferramentas e anexos vazios, ausência de histórico e `envio_realizado=false`. Isso é uma declaração verificável da preparação local, **não prova de envio ou configuração de uma plataforma externa**. A entrega real deve preservar os bytes e demonstrar ausência de ferramentas/anexos de ambiente antes do piloto, sob autorização própria.

## Conteúdo autorizado inspecionado

[fontes_autorizadas.py](../../../fontes_autorizadas.py) lê seis caminhos fixos, sem descoberta de dependências, histórico ou referência de seleção. As leituras reais estão em [leituras-editoriais.json](demonstracao-textual-001/leituras-editoriais.json). A edição local pode ler essas fontes mistas para extrair somente os recortes; elas não são enviadas inteiras nem abertas pelo montador.

| Fonte local | Conteúdo exportado e limite de inclusão |
|---|---|
| materiais/04_NOTAS_E_PROMPTS.md | Uma instrução de sistema em §4.4; pedidos literais §4.5/§4.6; única nota literal §4.2 somente D1/E1. Excluídos texto editorial, exemplos, histórico e outros blocos. |
| materiais/07_DEFINICOES_COMUNS.md | Definições integrais de impacto/relevância; regras comuns, sem seleções resolvidas por mudança. |
| documentacao/requisitos.md | Contrato inicial: entradas/saídas, quatro RFs e ordem global; termina antes do histórico de implementação. |
| documentacao/qualidade-e-testes.md | Seis primeiras colunas T01–T12: entradas e decisão/motivo da baseline. Excluída a coluna de destaques de RF e todas as seções de variantes/evidências. |
| specs/003-mudancas-controladas/spec.md | Somente célula de descrição da mudança selecionada; excluídas outras colunas, aceitação, fonte e histórico. |
| materiais/modelos/schema_saida.json | Schema existente integral, sem consulta à URL declarativa `$schema`. Sem IDs selecionados ou referência de avaliação. |

Inspeção técnica dos oito documentos possíveis: regras/precedência da baseline, catálogo de testes existentes, definições comuns, uma remoção, instrução, pedido, schema e nota rascunho. Não há código, diffs, resultados após mudança, conjuntos G_RF/G_T, seleções resolvidas, transcrição/governança ou histórico. Resultados **esperados da baseline** são material autorizado do catálogo; resultados das variantes e referência de seleção continuam proibidos. As quatro descrições são isoladas sobre a mesma baseline. A nota permanece literalmente a original, inclusive prefixo Markdown e final de linha; texto definitivo e revisão profissional continuam pendentes.

Essa conclusão está delimitada aos bytes/recortes identificados, cuja proveniência e hashes constam nas [autorizações](demonstracao-textual-001/editorial/indice.json). Sentinelas negativas e busca por termos proibidos são controles auxiliares; não constituem detector semântico universal. Alterar fontes/recortes exige nova inspeção e nova autorização. O catálogo externo é uma âncora técnica controlada, não uma assinatura ou barreira contra alguém que possa substituir simultaneamente pacote e autorização.

## Confrontos funcionais executados

| Critério | Evidência e observado |
|---|---|
| FR-001/FR-003, SC-001: inclusão fechada | Quatro testes de recortes, incluindo fontes fictícias com conteúdo proibido fora dos recortes, seletor duplicado e espião das leituras. Montador lê pacote plano/autorização; [leituras reais](demonstracao-textual-001/leituras-montador.json) não incluem referência nem fontes editoriais. Arquivo extra, ausente, hash/revisão indevidos e conteúdo trocado mesmo com manifesto atualizado são recusados. |
| FR-002, SC-001: separação | Preparação das 16 combinações termina antes de invocar CLI de avaliação. Referência candidata somente no argumento do avaliador em [comando separado](demonstracao-textual-001/comandos/avaliacao-separada/comando.json); não aparece no pacote/payload. Nenhum argumento de referência/modelo/provedor no montador. |
| FR-004, SC-002: condições e bytes | [confrontos.json](demonstracao-textual-001/confrontos.json): recomposição independente dos delimitadores e bytes de cada documento igual ao payload; hashes de preparação/recibo iguais; cópias documentais recuperadas. Comuns idênticos nas quatro condições por mudança, pedidos D0/D1 e E0/E1 iguais, única nota idêntica nas oito condições com notas e bloco ausente nas oito sem notas. `nota_literal_preservada=false` em D0/E0 significa nota ausente por desenho, não corrupção. |
| FR-005/FR-006, SC-002/SC-004: originais | Demonstração usa resposta **sintética** literal, origem sintética/modelo nulo. Avaliador preserva bytes completos da resposta e do payload; esperado independente MC-01: RF TP/FP/FN=1/0/0; testes=2/0/0. Candidata continua `CANDIDATO_NAO_REVISADO`. Controles dirigidos mantêm ausência, fragmento, falha técnica, nova avaliação e integridade no fechamento. |
| FR-007–FR-010, SC-003–SC-005: seleção e política | Política `ids-proposta-004-v2` inalterada; comparação de AST de todas as funções fora dos três guardas de caminho/leitura. Esperados e métodos anteriores do avaliador intactos. [Matriz](matriz.json) referencia confrontos anteriores de JSON estrito, duplicatas, desconhecidos, vazios, dimensões, referência inválida, P/R/F, Jaccard e resumos PONT-01/PONT-02. Não se reexecutou a suíte de pontuação inalterada. |
| FR-011, SC-006: controles | 16 famílias consolidadas com identificação de versão/origem; S-13 ampliada por caminhos/importação, S-14 substituída no alcance textual. Sem contabilizar métodos, arquivos ou links como demonstração funcional. Sintéticos não são observações LLM nem pares da bancada 003. |
| FR-012, SC-007: limites e documentação | Spec/plano/pesquisa/modelo/contrato/guia/tarefas/governança reconciliados sob D-29/D-30, com históricos e pendências explícitos. Checklist mantida byte a byte; 26 marcas existentes são revisão documental, não prova de execução. |

Execuções novas com fontes, comandos, retornos, stdout/stderr, esperados/observados e temporários preservados:

- [recortes-primeira](recortes-primeira/comando.json): quatro métodos aprovados.
- [montagem-revisada](montagem-revisada/comando.json): sete métodos aprovados, um ignorado por criação de symlink negada (WinError1314). Junctions reais internas/externas recusadas; teste lógico de bit reparse identificado como lógico.
- [entrada-avaliador](entrada-avaliador/comando.json): sete métodos dirigidos aprovados (`S13`, `S11`, `cli`), sem ampliar teste da pontuação inalterada.
- [prova-comando](prova-comando/comando.json): exportador e montagem pela CLI para as 16 combinações, confrontos reais de arquivos e avaliação separada; retorno zero. [provar.py](provar.py) contém as asserções independentes de bytes e contagens.

[preservacao.json](preservacao.json) confronta 2.128 arquivos protegidos/controles com o inventário original, sem divergências. Inclui gabarito, materiais/notas, bancada 003, código baseline e toda evidência anterior. As funções alteradas do avaliador são exclusivamente `caminho_seguro`, `relativo` e `ler`; as demais e os métodos de teste anteriores têm AST idêntica. O teste editorial inicial antecede as mudanças do avaliador e não o exercita; sua versão não é apresentada como teste do avaliador final. [auditar.py](auditar.py) registra esse confronto, sem executar testes.

## Entradas suportadas e limites

CLI aceita caminhos **locais absolutos com drive ou relativos ao cwd**, sem links em nenhum componente. Pacote: somente filhos diretos com nomes/ordem exatos; autorização fora de pacote/saída; saída nova sem sobreposição. Avaliador: arquivos relativos declarados com `/` ou `\`, subdiretórios confinados à raiz de importação. Casos positivos reais usam caminho relativo de CLI e caminhos absolutos, além de importação de subdiretórios.

Recusados: drive relativo (`C:arquivo`), raiz Windows sem drive, UNC/caminhos de dispositivo, streams NTFS, aliases com ponto/espaço final, dispositivos reservados e componentes declarados vazios/`.`/`..`; links internos/externos, junctions/reparse points, extras, subdiretórios no pacote, entradas divergentes e sobrescrita. Nenhuma conta, permissão, elevação ou restrição foi alterada. Verificação de caminhos/integridade não promete segurança contra mutação hostil concorrente nem isolamento de SO.

O teste real de symlink não executado permanece ignorado. Não é aprovado nem convertido em prova de identidade. Objetos desse tipo são entradas recusadas; o domínio aceito desta entrega é de arquivos regulares. A prova antiga de criação privilegiada/negação por identidade foi substituída por decisão do pesquisador, não satisfeita por simulação. Não há pendência de criar conta/ACL ou contornar esse erro para fechar o contrato offline revisado.

## Consulta e pendências

Da raiz do repositório, consultar as evidências sem reexecutar o experimento:

```powershell
Get-Content -Encoding utf8 evidencias/spec004/revisao-textual-2026-11-01/demonstracao-textual-001/confrontos.json
Get-Content -Encoding utf8 evidencias/spec004/revisao-textual-2026-11-01/demonstracao-textual-001/preparados/MC-01-D0/payload.txt
Get-Content -Encoding utf8 evidencias/spec004/revisao-textual-2026-11-01/demonstracao-textual-001/avaliacao/avaliacao.json
```

Os comandos exatos executados estão nos registros vinculados; cada nova execução exige destino novo. [Quickstart vigente](../../../specs/004-preparacao-avaliacao-ids/quickstart.md) distingue exemplos v2 históricos da CLI v3 com autorização externa obrigatória.

Pendentes: revisão profissional/científica da referência/política/expectativas T12; conteúdo definitivo, origem e neutralidade das notas/prompts; fundamentação/revisão de precisão, revocação, F1 e consistência; desenho final/configuração/orçamento/congelamento do piloto e adoção constitucional. Entrega real sem ferramentas deve ser verificada antes da pesquisa. Notas representam conhecimento de analista de testes; não se avaliam juniores, geração de testes novos, código ou descoberta de defeitos reais. Fechamento somente de engenharia offline no escopo D-29, sem liberação experimental.
