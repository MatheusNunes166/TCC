# Implementation Plan: Preparação de entradas e avaliação separada de IDs

**Feature**: `004-preparacao-avaliacao-ids` | **Date**: 2026-10-27 | **Spec**: [spec.md](spec.md)

**Branch (contexto do resolvedor)**: `004-preparacao-avaliacao-ids`; nenhuma branch Git criada ou trocada.

**Input**: Spec/checklist 004, governança e encaminhamentos da orientação; autorização documental D-24 e decisões técnicas D-25 em [decisões](../../documentacao/decisoes.md). Esta entrega contém cinco artefatos de planejamento, sem tarefas ou implementação.

## Summary

Projetar dois comandos locais em Python: montagem de conteúdo por manifesto fechado de documentos permitidos e avaliação de respostas originais já salvas, com referência candidata acessível somente ao avaliador. Sem cliente LLM ou integração de provedores. Preservar bytes, versões, hashes e registros anteriores; comparar conjuntos de IDs de requisitos e testes independentemente. Verificação futura cobre as 16 famílias sintéticas da Spec com esperados prévios independentes.

O plano não exporta agora pacote de entrada nem transforma notas em texto definitivo. Precisão, revocação, F1 e consistência têm fórmulas/convenções propostas, sem aprovação científica. [Pesquisa local](research.md), [modelo de dados](data-model.md), [contrato](contracts/preparacao-avaliacao.md) e [guia de validação futura](quickstart.md) detalham o desenho.

## Technical Context

**Language/Version**: Python 3.11+; Python 3.13.3 confirmado localmente. Registrar versão efetiva em futuras execuções.

**Primary Dependencies**: somente biblioteca padrão: argparse, pathlib, json, hashlib, datetime, uuid, fractions, itertools, unittest, tempfile e mocks somente nos controles. Sem instalação, SDK, JSON Schema genérico ou dependência de rede.

**Storage**: arquivos locais UTF-8/JSON; originais copiados em bytes; SHA-256, versões e diretórios exclusivos. Sem banco. Manifesto identifica todos os arquivos de entrada; saídas de avaliação ficam em zona separada.

**Testing**: unittest em dois arquivos novos futuros; fixtures sintéticas explícitas com esperados literais e racionais. Nenhum teste executado agora. Suite original, variantes e verificador 003 permanecem intocados.

**Target Platform**: Windows/PowerShell; pathlib para caminhos e sys.executable no futuro. Bash do Git somente no fluxo local do Spec Kit. Isolamento real exige execução restrita por permissões, além da lista permitida; não está demonstrado nesta entrega.

**Project Type**: dois utilitários locais de preparação/avaliação, sem serviço, API, interface gráfica, framework ou automação de coleta.

**Performance Goals**: rastreabilidade integral e recusa determinística de entradas inválidas; sem meta de latência/tokens, ganho de tempo ou benchmark.

**Constraints**: sem tarefas, implementação, chamadas externas, modelos escolhidos, piloto/coleta, geração de código ou semelhança textual. Referência 0.2 e histórico preservados; notas atuais `RASCUNHO_NAO_REVISADO`.

**Scale/Scope**: oito documentos lógicos, quatro mudanças isoladas, quatro condições candidatas, universos de quatro RFs/doze testes e 16 famílias de controles com subcasos. Não fixa repetições experimentais.

### Seleção e procedência desta fase

HEAD inicial `da82bd6a0bccf517205ee06f9fbd546ca39f4c2d`. Árvore já tinha alterações documentais locais da etapa anterior e arquivos não rastreados, inclusive transcrição, encaminhamentos, roteiro e Spec 004; nenhum deles foi descartado. B da bancada continua `aec474bcb54d6dae2afceff8e5b9226991386490`, sem redefinição por HEAD.

Sequência realizada antes de redigir o plano: ler governança/Spec/checklist/encaminhamentos → persistir `specs/004-preparacao-avaliacao-ids` em `.specify/feature.json` → executar `check-prerequisites.sh --json --paths-only` → conferir FEATURE_SPEC/IMPL_PLAN em 004 → executar `setup-plan.sh --json`. O setup copiou o template correto e retornou o mesmo diretório. Escritas inicialmente negadas pelo sandbox no seletor/setup/contracts foram repetidas com aprovação técnica; não representam autorização experimental. Bash usado: `C:/Program Files/Git/bin/bash.exe`, pois bash não estava no PATH. Não houve criação de branch/commit.

## Constitution Check

Revisão anterior à fase 0 e posterior ao desenho. Constituição 1.0.0 ainda sem ratificação; conformidade documental não a adota.

| Princípio/gate | Antes | Depois do desenho | Evidência do alcance documental |
|---|---|---|---|
| Escopo controlado | Conforme | Conforme | Dois utilitários locais; cinco documentos; sem cliente, tarefas ou pesquisa executada |
| Decisões explícitas | Conforme | Conforme | D-24/D-25; research R-06 destaca efeitos de convenções na pontuação |
| Rastreabilidade | Conforme | Conforme | Manifesto, conteúdo integral, referência/hash, versão das regras e originais separados |
| Verificação por evidências | Conforme | Conforme | Esperados sintéticos prévios, observado futuro; metas não apresentadas como resultados |
| Incrementos pequenos | Conforme | Conforme | Apenas preparação/avaliação offline; sem infraestrutura genérica |
| Separação de contextos | Conforme no desenho | Conforme no desenho | Montador sem referência; avaliação separada; acesso real ainda exige prova antes do uso |
| Fechamento | Conforme | Conforme | Estado/handoff/pendências atualizados, histórico preservado; revisão científica pendente |

Nenhuma violação documental identificada. Gates de isolamento implementado, referência/notas revisadas e métricas fundamentadas continuam não atendidos para pesquisa; não declarar liberação de piloto.

## Project Structure

### Documentation (this feature)

```text
specs/004-preparacao-avaliacao-ids/
├── spec.md
├── checklists/requirements.md
├── plan.md
├── research.md
├── data-model.md
├── contracts/preparacao-avaliacao.md
└── quickstart.md
```

Cinco artefatos de planejamento. `tasks.md` não será criado nesta fase. Complementos datados em Spec/checklist reconciliam o novo alcance e preservam o texto anterior.

### Source Code (repository root) — desenho futuro, arquivos não criados

```text
montagem_entradas.py              # somente manifesto/pacote permitido → entrada preservada
avaliacao_ids.py                  # registro/resposta local + referência → avaliação derivada
tests/test_montagem_entradas.py   # controles de composição, isolamento e preservação
tests/test_avaliacao_ids.py       # formato, conjuntos, métricas e resumos sintéticos
tests/fixtures/spec004/           # bytes e esperados literais revisados, nunca pacote LLM
```

**Structure Decision**: dois módulos independentes, sem importação do avaliador pelo montador, sem importação do núcleo/variantes/verificador 003. Evitar pacote genérico, plug-ins ou abstração de provedor. Fixtures não são artefatos experimentais.

Zonas de execução futuras: pacote permitido/runner/saída da montagem sob identidade restrita, sem acesso ao repositório; zona de avaliação recebe cópias de entrada/resposta e referência privada; resultados ficam somente na avaliação. Os caminhos concretos serão fornecidos explicitamente, sem busca recursiva e sem criar outro repositório. Detalhes de arquivos e CLI no contrato. Nenhuma dessas zonas foi criada agora.

### Fluxo projetado

1. Preparação editorial fora do montador: produzir apenas recortes da lista da Spec e registrar proveniência/revisão externamente; notas permanecem rascunho. Para controles locais, usar documentos fictícios rotulados.
2. Montador confere manifesto, paths reais/links, hashes, tipos e condições; abre apenas itens aplicáveis; monta conteúdo determinístico e guarda originais/manifesto/payload exato. Sem argumento de referência, rede ou histórico.
3. Avaliador importa arquivo de resposta ou falha técnica, preserva bytes antes de interpretar e valida integridade da entrada. Referência é lida somente aqui, de caminho explícito.
4. Parser estrito valida JSON completo/contrato; extrai conjuntos únicos sem normalização; usa `rfs`/`tests` como G. Registra IDs conhecidos, duplicatas, acertos, omissões e excedentes por dimensão.
5. Avaliação nova conserva versões/hashes, estados e cálculos candidatos; resumo opcional distingue observações de tentativas e inválidas imputadas. Nenhuma etapa envia mensagens ou chama LLM.

### Pontuação: atenção antes de adotar convenções

Pesquisa R-06 identifica os pontos que mudam resultados: (a) G_T é `tests`, não `changed`; (b) inválida não vira seleção vazia observada, zero só em visão operacional explicitamente solicitada; (c) desconhecido é FP único, não descartado; (d) BOM/UTF-8 inválido e constantes/chaves repetidas são inválidos pela proposta estrita explicitada; (e) tentativas não ampliam denominadores de observações; mais de uma resposta concluída para a mesma observação bloqueia resumo até adjudicação explícita. O contrato reúne fórmulas, denominadores e convenções de vazios. Nenhuma ambiguidade é resolvida pela observação mais favorável. São regras técnicas candidatas, sujeitas à revisão científica antes de experimento.

### Cobertura do desenho

| Requisitos | Artefatos e verificação futura |
|---|---|
| FR-001–FR-003 | Manifesto/CLI montagem, fronteira de acesso e S-14 |
| FR-004–FR-006 | Payload/registro de tentativa, integridade e S-11/S-13/S-16 |
| FR-007–FR-009 | Parser específico, adaptador da referência e S-01–S-10/S-12 |
| FR-010 | Política de métricas versionada, resumos e S-15/S-16 |
| FR-011 | Matriz explícita S-01–S-16, fixtures futuras independentes |
| FR-012 | Escopo desta entrega, sem tarefas/código/chamadas |

## Complexity Tracking

Sem exceção constitucional a justificar. O controle de acesso é gate obrigatório de uso, não motivo para criar infraestrutura genérica. Sem novo serviço ou biblioteca externa.

## Fechamento desta fase

Planejamento documental encerrado na fase 1 do fluxo local; somente este plano, research, data-model, contrato e quickstart produzidos. Nenhum esperado sintético executado; pacote permitido não exportado; notas/referência não revisadas cientificamente. Próxima ação: revisar planejamento e eventuais convenções e solicitar tarefas quando desejado. P-01/P-02/P-03 e adoção constitucional permanecem abertas; calendário da apresentação e compartilhamento do repositório seguem com o pesquisador.

Conferência documental final: resolvedor retornou 004 e research/data-model/contracts/quickstart disponíveis; 115 links locais válidos nos 12 documentos conferidos; nenhum placeholder técnico ou espaço final; `git diff --check` sem erros. Hash/tamanho de 191 arquivos protegidos mantidos. Sem tasks.md, módulos ou testes novos. `.specify/extensions.yml` ausente antes/depois, sem hooks. Essas verificações não executam a aplicação nem demonstram isolamento. Revisão auxiliar somente de leitura conferiu pontuação/estados/16 famílias; ajuste documental omite integralmente bloco de notas em D0/E0, conforme a Spec.
