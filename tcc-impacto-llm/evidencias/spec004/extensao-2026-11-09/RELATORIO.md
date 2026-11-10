# Preparação da extensão exploratória — D-41, 09/11/2026

Preparação local autorizada pelo pesquisador; nenhuma chamada à API, teste de conexão, coleta, commit ou push. A consulta pública à documentação oficial serviu somente para o orçamento solicitado; os testes executam com rede bloqueada e sem chave real. Não há dados novos de LLM. A declaração do pesquisador de que concluiu a revisão do piloto está registrada em [D-41](../../../documentacao/decisoes.md); não foram fabricadas aprovações retrospectivas.

O piloto encontrou correspondência integral com a referência candidata 0.2 nas 16 observações. Isso não demonstra superioridade, equivalência geral entre condições nem inutilidade das notas. Planos, fontes, materiais, capturas, avaliações, revisões e resultados anteriores continuam separados da extensão. A [lista inicial de hashes](estado-inicial.json) permite conferir inclusive ignorados. Os scripts anteriores estão em [fontes-anteriores](fontes-anteriores/); alterações funcionais não mudam seus hashes preservados.

## Artefatos e expectativas

- [Catálogo público 0.3](../../../materiais/modelos/catalogo_baseline_0.3.md), [JSON público](../../../materiais/modelos/catalogo_baseline_0.3.json) e [referência privada 0.3](../../../materiais/modelos/referencia_candidata_0.3_NAO_ENVIAR_AO_LLM.json).
- [Dedução, conjuntos e justificativas](../../../documentacao/referencia-candidata-0.3.md); [expectativas registradas antes da execução](expectativas-antes-execucao.json), produzidas por receita sem importar o núcleo/variantes.
- [Plano vigente 002](../../../captura/extensao-20261109-002/plano.json), [ordem final](../../../captura/extensao-20261109-002/ordem.json) e [32 preparações](../../../captura/extensao-20261109-002/preparados/). A preparação 001 é intermediária, anterior ao fechamento das fontes; fica preservada como diagnóstico e não deve ser utilizada.
- Implementação: `extensao_exploratoria.py`, ajustes funcionais em `coletor_api.py` e `avaliacao_ids.py`, testes em `tests/test_extensao_exploratoria.py`. Montador, exportador anterior, coletor CLI, núcleo e quatro variantes preservados literalmente. `.gitattributes` protege os novos artefatos e fontes vinculadas a hashes contra conversão de bytes pelo Git.
- Documentação reconciliada: estado, README, escopo, arquitetura, roadmap, operação API, decisões e nova referência. Materiais anteriores, notas e prompts não foram reescritos.

| Caso | Baseline | MC-01 | MC-02 | MC-03 | MC-04-v2 |
|---|---|---|---|---|---|
| T13 | permitir/direta | permitir/direta | permitir/direta | negar/sem | permitir/direta |
| T14 | negar/conflito | negar/conflito | permitir/direta | negar/conflito | negar/conflito |
| T15 | negar/estado | negar/estado | negar/estado | negar/estado | negar/estado |

`direta` = `permissao_direta`; `sem` = `sem_permissao`. T13: ativa, Consulta + Supervisão, visualizar; T14: ativa, Consulta + Auditoria + Supervisão, exportar; T15: em_revisao, os mesmos três papéis, exportar. RF-02/RF-03 sustentam coexistência de origens; RF-04 verifica o par efetivo; RF-01 mascara conflito/concessão. Não houve contradição substantiva com o contrato, mudança de regra ou alegação de dificuldade empiricamente demonstrada.

| Mudança | RFs candidatos | Testes de mudança | Preservação relacionada |
|---|---|---|---|
| MC-01 | RF-02 | T04 | T12, T14, T15 |
| MC-02 | RF-04 | T06, T07, T12, T14 | T11, T15 |
| MC-03 | RF-02, RF-03 | T02, T05, T13 | T01, T06, T07, T09, T10, T11 |
| MC-04-v2 | RF-03, RF-04 | T05, T07, T12 | T08, T10, T13, T14, T15 |

As seleções são 4/6/9/8 testes. A mesma política da 0.2 usa papéis efetivos da baseline para permissões/incompatibilidade e Supervisão atribuído para herança, independentemente do estado. T14/T15 entram em MC-01/02 e são excluídos de MC-03 por operação exportar; T13 entra em MC-03, sai de MC-01 por operação e de MC-02 por ausência de Auditoria. Os três entram como preservação em MC-04. Inclusões e exclusões completas dos quinze casos estão no documento de referência, com as justificativas anteriores mantidas.

## Verificação offline e reprodução

Resultados completos da execução final: [resultado.json](verificacao-final/resultado.json), [log unittest](verificacao-final/unittest.txt), [75 comparações reais da bancada local](verificacao-final/bancada-75.json). A execução preserva a interpretação dos 16 textos do piloto por comparação direta entre o avaliador anterior e o atual; as 60 expectativas anteriores e T01–T12 permanecem iguais.

**Execução final real:** Python 3.13.3, 127 métodos descobertos, **126 aprovados, zero falhas, zero erros e um ignorado**, em 302,453 s. O ignorado é o controle existente de criação de symlink real: Windows recusou por falta do privilégio específico (WinError 1314); controles de caminho/junction e demais testes passaram. Não foi solicitada elevação para esse teste condicional. **75/75 comparações de decisão/motivo conformes**, sendo 15 da baseline e 15 por variante; nenhum comportamento anterior divergente. O audit hook bloqueou conexões e resolução de nomes na execução final.

Fechamento de integridade: [preservação final, vínculos e bytes Git](preservacao-final-002.json), produzido por [receita de conferência](fechar_verificacao.py), sem stage/commit/push. O teste de bytes compara `git hash-object --stdin-paths` com e sem filtros, sem gravar objetos, abrangendo os novos arquivos vinculados. Isso confere a política local do Git; não alega novo checkout ou transporte remoto, que não foram realizados.

A [primeira conferência](preservacao-final.json) detectou caminhos relativos incorretos neste relatório, corrigidos antes do fechamento 002. Ela já confirmou 7.094 arquivos anteriores preservados, 704 vínculos de preparações e 740 arquivos com bytes Git idênticos. Um link histórico de D-35 em `documentacao/decisoes.md`, já ausente no HEAD inicial, continua identificado separadamente: `../evidencias/spec004/preparacao-piloto-2026-11-06/RELATORIO.md`. Não foi reescrito o registro histórico; os links atuais da versão 0.3 e da preparação v2-LF permanecem acessíveis. A conferência final distingue esse vínculo herdado de qualquer erro introduzido.

Os controles da extensão exercitam os dois modelos em envelopes artificiais, 64 posições, pausa após 17 e retomada das 47 restantes, nova retomada sem duplicação, reconhecimento de T13–T15, versões e configurações trocadas, igualdade de payloads, bytes inválidos conservados sem reparo, respostas incomplete, HTTP 429, falha parcial/estado remoto desconhecido, ausência de fallback e bloqueio de reenvio. Avaliação abre a referência separadamente. Revisão de conformidade artificial testa 64 pendentes e uma exclusão, preservando N=64 e originais; os controles existentes verificam desvio/inclusão, fontes, TLS, interrupções e revisão real simulada. Nenhum desses controles é dado da pesquisa.

Foi feita uma primeira execução da suíte durante o ajuste temporário do montador: a troca de bytes da fonte durante testes acionou corretamente cinco recusas por hash, incluindo um erro de preparação da classe API. O ajuste foi retirado e os bytes originais do montador restaurados; o montador permanece intacto. A execução final, em fontes estabilizadas, é a evidência de fechamento. A primeira suíte isolada da extensão teve 11 métodos aprovados; a suíte final acrescenta comparação do avaliador anterior e ampliação dos controles de conformidade.

Executar na raiz `TCC/tcc-impacto-llm`, sempre com saídas novas:

```powershell
python -B extensao_exploratoria.py simular --plano captura/extensao-20261109-002/plano.json
python -B extensao_exploratoria.py controle --plano captura/extensao-20261109-002/plano.json --lote captura/CONTROLE-ARTIFICIAL-ext03-NOVO --limite 17
python -B extensao_exploratoria.py controle --plano captura/extensao-20261109-002/plano.json --lote captura/CONTROLE-ARTIFICIAL-ext03-NOVO --limite 47 --continuar
python -B coletor_api.py avaliar --lote captura/CONTROLE-ARTIFICIAL-ext03-NOVO --referencia materiais/modelos/referencia_candidata_0.3_NAO_ENVIAR_AO_LLM.json --saida avaliados/CONTROLE-ARTIFICIAL-ext03-NOVO
python -B evidencias/spec004/extensao-2026-11-09/verificar_offline.py --saida evidencias/spec004/extensao-2026-11-09/reexecucao-NOVA
```

O envio real da extensão é recusado em código antes da leitura de chave. A interface nova oferece somente preparação, simulação e controle; não libera a execução por parâmetro. As fontes anteriores permitem reproduzir o mecanismo histórico sem editar planos ou hashes do piloto. O verificador da Spec 003 continua limitado à 0.2 deliberadamente; a extensão reutiliza sua auditoria de variantes no novo controle de 75 pares. O schema de resposta não tem enumeração de IDs nem limite 12 e foi conservado. Os limites 16 do coletor CLI e do plano API anterior permanecem na rota histórica; o motor API recebe 64 posições somente do conferidor da extensão.

## Ordem, configurações e custo

Quatro mudanças × quatro condições × dois modelos × duas repetições = 64. A ordem usa um único `random.Random(20261109)` e `shuffle` em cada bloco, enumerando mudanças MC-01/02/03/04-v2, condições D0/D1/E0/E1 e modelos Sol/Astra. Python **3.13.3**, versão completa e ordem final em `ordem.json`. Cada bloco tem as 32 combinações exatamente uma vez; todas as posições têm estado `PLANEJADA_NAO_EXECUTADA`. Essa semente é local, sem seed atribuída ao modelo. A ordem anterior não é substituída.

Modelo e esforço explícitos, 4096 tokens de saída e timeout 120 s comuns, Responses API HTTP direta, um texto independente em `input`, `tools=[]`, `tool_choice=none`, `store=false`, `stream=false`, sem histórico e sem retries automáticos. A modalidade de envio é a mesma do piloto; não há saída estruturada forçada adicionada. Os mesmos 16 textos são reutilizados nas 32 preparações, com IDs/configurações próprios e hashes textuais iguais entre modelos; notas idênticas em D1/E1 e ausentes em D0/E0. O orçamento declarado está **nulo**, sem herdar o USD 1,00 anterior.

Preços Standard por milhão de tokens de entrada/saída, consultados em **09/11/2026**: Sol **US$ 2/10** ([modelo oficial](https://developers.openai.com/api/docs/models/gpt-6-sol)); Astra **US$ 10/50** ([modelo oficial](https://developers.openai.com/api/docs/models/gpt-6-astra)), para contexto curto, conferidos com a [tabela oficial](https://developers.openai.com/api/docs/pricing). A [documentação de raciocínio](https://developers.openai.com/api/docs/guides/reasoning) informa que raciocínio é cobrado como saída e compartilha o limite com a resposta final; `incomplete` pode ocorrer sem texto final e com consumo.

O [cálculo reproduzível](estimar_custo.py) e [resultado](custo.json) usam os bytes reais dos payloads, sem tokenizer instalado: 237.672 bytes de entrada por modelo ao longo de suas 32 posições. Não é contagem exata de tokens. Cenários sem desconto de cache, ferramentas, impostos, taxa regional ou retries:

| Hipótese | Sol | Astra | Total USD |
|---|---:|---:|---:|
| bytes/4 + 128 tokens por chamada; saída 1024 = 768 raciocínio + 256 final | 0,454736 | 2,273680 | 2,728416 |
| mesma entrada; saída 4096 = 3840 raciocínio + 256 final | 1,437776 | 7,188880 | 8,626656 |
| bytes/2 + 128; saída 4096 | 1,556600 | 7,783000 | 9,339600 |
| margem de um token/byte + 256; saída 4096 | 1,802448 | 9,012240 | 10,814688 |

A divisão raciocínio/final é somente hipótese de cálculo; `medium` não fixa essa distribuição. O limite total de saída da rodada seria 262.144 tokens, somando os dois modelos. Os cenários não são teto garantido de cobrança. `--limite` restringe tentativas por invocação, e timeout restringe espera; não impõem teto em dólares nem garantem cancelamento remoto. Confirmar cobrança Standard, acesso e saldo atual na conta antes da autorização; o coletor preserva a modalidade sem `service_tier` explícito, como no piloto.

## Pendências para revisão do pesquisador

1. Rever a referência candidata 0.3, 75 expectativas e conjuntos candidatos/justificativas; registrar responsável, data, versão e eventuais divergências. Não há aprovação científica externa atribuída.
2. Rever as 64 posições, identidades de modelo/configuração e o limite proposto comum de 4096; qualquer revisão desse limite deve anteceder a rodada e abranger ambos os modelos. Não ajustar por vantagem observada.
3. Declarar orçamento novo e conferir acesso, saldo e modalidade Standard; nenhum saldo anterior foi presumido e nenhuma conexão foi testada.
4. Autorizar separadamente o início e o incremento que habilite o envio da extensão, preservando captura/avaliação/revisão/retomada existentes. Nenhuma rodada foi iniciada. Notas incorretas permanecem fora desta etapa.
