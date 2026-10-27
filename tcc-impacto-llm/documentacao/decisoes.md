# Decisões, propostas e pendências

## Revisão parcial de engenharia da Spec 004 — 27/10/2026

**D-28 — Registro técnico pelo assistente sob D-26/D-27.** Implementados montador por lista fechada e avaliador local de IDs com Python/biblioteca padrão. Convenções candidatas do pesquisador e I1 refletidos em Spec/plano/research/modelo/contrato/tarefas; política ids-proposta-004-v2, sem aprovação científica presumida. Checklist de qualidade preservada sem remarcação. [Relatório parcial](../evidencias/spec004/revisao-parcial/relatorio.md), [confrontos por família](../evidencias/spec004/revisao-parcial/matriz.json) e [tarefas](../specs/004-preparacao-avaliacao-ids/tasks.md).

PONT-01: mistura de versões gera diagnóstico/retorno 2, inventários separados por versão e nenhum combinado. Para calcular um grupo, fornecer nova lista homogênea explícita, sem presumir distribuição de N entre versões. PONT-02: configuração/mudança/condição/repetição identifica observação; duplicidade bloqueia célula afetada, sem melhor resposta automática; tentativas técnicas vinculadas não ampliam N. Jaccard usa somente elegíveis de repetições distintas, expõe observações/pares e retorna não calculável/valor nulo com menos de duas.

Evidências: montagem-final — seis métodos, cinco aprovados, um ignorado por WinError1314 ao criar symlink real. Junctions reais internas/externas verificadas; bit reparse também tem controle lógico, sem apresentá-lo como isolamento. avaliacao-confirmacao — 14 métodos aprovados, sem falhas/erros/ignorados; valores e estados de 15 famílias conformes no escopo offline, S-14 parcial. Demonstração persistente com quatro pacotes fictícios, conteúdo exato e respostas originais, cenários A/B da CLI em evidencias/spec004/demonstracao-001. São controles sintéticos, não resultados de LLM ou pares da bancada 003; contagens não substituem confrontos funcionais. Falhas iniciais e fontes/versões executadas preservadas; restrição excessiva de saída e construção de fixture com vínculo indevido corrigidas, sem alterar escores esperados/gabarito.

**Impedimentos:** não há runner provisionado sob identidade separada cuja leitura de desenvolvimento/referência/avaliação seja negada. Token atual lê a candidata; não cumpre contrato de isolamento. Provas em [preparação do ambiente](../evidencias/spec004/isolamento/preparacao.md). Nenhuma conta/ACL/credencial/elevação usada para contornar essa restrição; aprovação técnica anterior permitiu somente escrita documental. T014/T015 e T042–T048 permanecem pendentes; 39 tarefas independentes concluídas. Diagnóstico e documentação parciais não concluem tarefas de fechamento dependentes.

Código/testes/materiais/notas/gabarito/evidências anteriores preservados por conferência do inventário; originais documentais anteriores às mudanças arquivados em preparacao/arquivos-iniciais. Sem LLM/piloto, sem modelo escolhido. Revisão profissional da referência/política/expectativas T12, notas definitivas, fundamentação/revisão de precisão/revocação/F1/consistência, piloto final e adoção constitucional continuam pendentes. Não há fechamento integral da Spec 004. Próxima ação operacional depende do runner real restrito; nenhuma simulação satisfaz esse gate.

## Convenções candidatas e implementação parcial autorizada — 27/10/2026

**D-26 — Pesquisador, pedido explícito nesta conversa, 27/10/2026.** Adotar PONT-01: rejeitar agregação de versões distintas de política/referência na mesma célula, preservando registros e separando grupos por versão, sem combinado silencioso. PONT-02: observação única por configuração/mudança/condição/repetição, duplicidades diagnosticadas bloqueiam resumo afetado, sem escolha de resposta; tentativas técnicas distintas de repetições. Jaccard apenas de repetições elegíveis distintas, número de observações/pares e “não calculável” com menos de duas. Corrigir I1 para links internos/externos, junctions/reparse points. São convenções técnicas candidatas do pesquisador, não aprovação científica. Política versionada ids-proposta-004-v2; versão anterior preservada nos originais documentais.

**D-27 — Autorização e execução técnica pelo assistente sob o pedido atual.** Implementar somente tarefas com dependências resolvidas, com controles sintéticos e evidências reais; verificar isolamento primeiro, sem contorno/simulação; se indisponível, registrar capacidade ausente e prosseguir no independente. Sem alterar candidata/notas, chamar LLM ou iniciar piloto. Inventário/originais em evidencias/spec004/preparacao/; ambiente em evidencias/spec004/isolamento/ambiente.json. Token atual não elevado pode ler a referência. Não foi disponibilizado runner sob identidade separada com negação de acesso às zonas proibidas; nenhuma conta/ACL alterada ou credencial/elevação usada para contornar. T014/T015 e fechamento integral permanecem pendentes.

Contrato de importação para controles explicita configuracao_id string não vazia e repeticao_sintetica inteiro positivo, modelo nulo/origem sintética; não seleciona modelo experimental. Checklist de qualidade 26/26 conferida sem alteração de marcas; ciência e isolamento efetivo continuam gates separados. Pendências P-01/P-02/P-03 e adoção constitucional preservadas.

## Planejamento técnico da Spec 004 — 27/10/2026

**D-24 — Autorização do pesquisador.** Responsável: usuário/pesquisador, 27/10/2026; evidência: pedido explícito nesta conversa para planejar 004 pelo fluxo local do Spec Kit, selecionar/confirmar feature antes dos artefatos, manter Python/biblioteca padrão, separar montagem/avaliação, preservar originais, detalhar condições, validação/pontuação e 16 famílias sintéticas. Autoriza os cinco documentos de planejamento e reconciliação, sem tarefas, implementação, escolha de modelo, chamadas externas, piloto ou coleta. Notas continuam rascunho; métricas e convenções científicas continuam propostas. Não ratifica constituição ou aprova cientificamente referência/resultados técnicos.

**D-25 — Desenho técnico e fechamento documental pelo assistente.** Responsável pelo registro: assistente, 27/10/2026. Fluxo da skill local `speckit-plan`; governança, Spec/checklist, encaminhamentos e fontes locais lidos. `.specify/feature.json` seleciona `specs/004-preparacao-avaliacao-ids`; `check-prerequisites.sh --json --paths-only` confirmou FEATURE_SPEC/IMPL_PLAN em 004 antes de `setup-plan.sh --json`, que copiou o template correto e confirmou o mesmo destino. Bash explícito do Git, fora do PATH. Escritas do seletor/setup/contracts inicialmente negadas pelo sandbox e repetidas com aprovação técnica. Campo BRANCH do resolvedor é contexto; nenhuma branch/commit criada ou trocada. HEAD inicial `da82bd6a0bccf517205ee06f9fbd546ca39f4c2d`; alterações locais anteriores preservadas.

Artefatos: [plan](../specs/004-preparacao-avaliacao-ids/plan.md), [research](../specs/004-preparacao-avaliacao-ids/research.md), [data-model](../specs/004-preparacao-avaliacao-ids/data-model.md), [contrato local](../specs/004-preparacao-avaliacao-ids/contracts/preparacao-avaliacao.md), [quickstart futuro](../specs/004-preparacao-avaliacao-ids/quickstart.md). Dois utilitários locais futuros, Python 3.11+ (3.13.3 disponível) e biblioteca padrão, sem serviço/SDK/rede. Montador só lê manifesto/documentos finais permitidos; só avaliador lê candidata. Separação de processos e identidade restrita/permissões projetadas; nenhuma ACL/conta/pacote foi criada e isolamento ainda não foi demonstrado. Notas marcadas `RASCUNHO_NAO_REVISADO` em metadados, texto idêntico D1/E1; nenhuma aprovação profissional atribuída.

**Pontos que afetam pontuação, destacados antes de completar o plano:** G_RF vem de `rfs`, G_T de `tests`, nunca de `changed`/`expected`; preservar testes relevantes de manutenção. Formato inválido deixa extração/escores observados ausentes, reconciliando a Spec com os zeros do resumo operacional proposto no material histórico: imputação somente em visão separada e explicitamente pedida; falha técnica não vira seleção vazia. IDs desconhecidos são FP únicos e duplicatas não multiplicam contagem, sem normalização. Mapeamento documental MC-04→MC-04-v2 não autoriza aliases nas respostas. Tentativas técnicas não são repetições; múltiplas concluídas sem adjudicação bloqueiam resumo. Detalhe adicional proposto explicitamente em research R-06: UTF-8 estrito sem remover BOM, rejeição de chaves repetidas/NaN/Infinity/texto residual; subcasos previstos em S-09. Essa escolha afeta validade e continua candidata à revisão, sem aprovação científica presumida.

Contrato registra fórmulas, frações/denominadores e convenções para vazios/pares insuficientes. S-01–S-16 têm esperados independentes descritos, sem fixture executável ou execução gerada. Revisão auxiliar somente de leitura prevista na skill, restrita a arquivos locais, sem chamada externa. Gates constitucionais conferidos antes/depois do desenho; ciência e isolamento efetivo continuam gates futuros. Nenhum teste de aplicação/controle foi executado; somente conferências documentais e scripts de seleção/setup.

Conferência final documental: resolvedor `check-prerequisites.sh --json --require-spec` confirmou 004 e AVAILABLE_DOCS com research/data-model/contracts/quickstart. Nos 12 documentos conferidos, 115 links locais válidos, sem placeholders técnicos ou espaços finais; `git diff --check` sem erros. SHA-256/tamanho de 191 arquivos protegidos coincidem antes/depois, incluindo código, testes, materiais, variantes, evidências, Specs anteriores, constituição, transcrição, encaminhamentos e roteiro. Diretório 004 contém Spec/checklist e exatamente cinco documentos de planejamento; tasks.md, módulos e testes novos ausentes. `.specify/extensions.yml` ausente antes/depois, sem hooks a executar. São verificações documentais, não execução dos controles. Revisão auxiliar não identificou contradição de pontuação restante; ausência integral do bloco de notas D0/E0 foi alinhada à Spec no desenho.

P-01/P-02/P-03, revisão profissional/científica, notas definitivas, fundamentação/revisão de precisão/revocação/F1/consistência e desenho final do piloto permanecem pendentes. T12 já adotado/verificado em B; referência candidata 0.2, seleções 2/4/8/5, código e evidências preservados. Próxima ação: revisar planejamento/convenções e solicitar tarefas quando desejado; nenhuma implementação ou pesquisa liberada. Restrições de somente Spec/checklist em D-22/D-23 descrevem a entrega anterior, superadas apenas no alcance documental de D-24.

## Orientação registrada e especificação da próxima capacidade — 27/10/2026

**D-22 — Autorização documental do pesquisador.** Responsável: usuário/pesquisador, 27/10/2026; evidência: pedido explícito nesta conversa para ler transcrição de 21/10, governança e fechamento 003; distinguir pedidos explícitos, sugestões e decisões abertas; preparar roteiro MC-01/MC-04 com artefatos existentes e somente Spec 004/checklist para montagem permitida, registros originais e avaliação separada de IDs. Autoriza reconciliação documental, sem implementação, plano/tarefas, escolha de modelos, chamadas ao LLM, interface/API/repositório novo ou piloto/coleta. Sem avaliação de semelhança textual ou geração de código. Não aprova cientificamente resultados técnicos nem ratifica a constituição.

**D-23 — Registro e revisão documental pelo assistente.** Responsável pelo registro: assistente, 27/10/2026. Evidências: [encaminhamentos com tempos/classificações](encaminhamentos-orientacao-21-10-2026.md), [roteiro](roteiro-demonstracao-spec003.md), [Spec 004](../specs/004-preparacao-avaliacao-ids/spec.md) e [checklist de qualidade](../specs/004-preparacao-avaliacao-ids/checklists/requirements.md). Atribuições de falas seguem transcrição automática sujeita a confirmação; síntese não é ata aprovada. Reunião descreve 003 ainda futura; fechamento D-21 posterior na mesma data não recebe aprovação científica retroativa. Original, materiais e evidências preservados.

Pedido de descrever sistema/funcionalidades e mostrar base/alteração/efeito é atendido documentalmente pelo roteiro. API/tela/backend são alternativas ilustrativas; interface é explicitamente dispensável na fala. Comparar ferramentas/modelos, revisão por profissionais externos, métricas semânticas para texto e ampliação no TCC2 são sugestões, sem escolhas aprovadas. A meta de algo rodável no início de novembro não é agendamento confirmado. Compartilhamento efetivo do repositório pelo pesquisador permanece a confirmar; nenhum envio realizado pelo assistente.

Política candidata 004 reaproveita materiais 01/04 e schema/modelo de registro, detalhando documentos enumerados, fronteira de acesso, preservação, formato, duplicatas, desconhecidos como FP e listas vazias/falhas. Distingue ausência de extração observada em formato inválido do zero imputado em eventual resumo operacional separado proposto anteriormente. Falhas técnicas não viram seleção vazia. Detalhamentos/convenções são propostas versionadas, sem congelamento científico ou alteração dos materiais. As 16 famílias de controles sintéticos foram somente especificadas, sem execução ou contagem como LLM.

**Pendências mantidas:** P-01/P-02 — revisão científica/profissional da referência 0.2, política e expectativas T12, revisor/data a combinar; conteúdo definitivo, origem e neutralidade das notas/prompts; fundamentação/revisão de precisão, revocação, F1 e consistência. P-03 — desenho final do piloto, condições, mudanças, repetições, configuração, orçamento, ordem e congelamento. Demonstração MC-01/MC-04 não altera proposta histórica de casos do piloto. Nenhum modelo novo escolhido. Adoção constitucional pendente. T12 já adotado/verificado em B, sem nova adoção a solicitar.

Conferência de fechamento documental: 94 links locais válidos nos nove documentos novos/atualizados; 12 FRs, 7 SCs, 16 famílias sintéticas planejadas e checklist 26/26. Consultas do roteiro recuperaram quatro registros iniciais e cinco registros de variantes correspondentes às tabelas. `git diff --check` sem erros; comparação de leitura confirmou histórico anterior integralmente preservado nos cinco arquivos rastreados alterados e ausência de diff em código/testes/variantes/materiais/evidências/Spec 003/constituição. A transcrição já estava não rastreada no início e não foi editada. Nenhum teste de aplicação executado.

Próxima ação: revisar encaminhamentos/roteiro e Spec 004/checklist; eventual planejamento exige solicitação própria, seleção explícita de 004 e confirmação do destino. `.specify/feature.json` permanece em 003 pelo limite documental. Baseline, candidata/conjuntos e fechamento 003 preservados; nenhuma nova execução da bancada, coleta ou LLM. Registros anteriores abaixo são históricos nos alcances superados por D-22/D-23.

## Implementação e verificação da Spec 003 — 21/10/2026

**D-20 — Autorização do pesquisador.** Responsável: usuário/pesquisador; evidência: pedido explícito nesta conversa para implementar as 35 tarefas, preservar alterações locais/B/T01–T12, executar baseline e 48 comparações por decisão/motivo, investigar divergências sem ajustar automaticamente expectativas e reconciliar documentação. Não autoriza piloto, LLM, novos modelos ou alterações nas métricas; não aprova cientificamente a referência nem ratifica a constituição.

**D-21 — Fechamento de engenharia pelo assistente.** Spec 003 confirmada pelo resolvedor; checklist 23/23 satisfeita. HEAD inicial `8041b0b1deca09f13c8b95069699616c7a1a7a60`; sete alterações documentais locais preservadas e arquivadas com hashes em `evidencias/spec003/preparacao/`. B confirmado, sem redefinição por HEAD. Quatro extrações independentes do mesmo blob; cada fonte possui só a edição do plano, diff/AST/revisão e hashes. Manifestos identificam HEAD, estado local e snapshots dos arquivos novos executados, sem pressupor commit da implementação.

Execução Python 3.13.3: primeira integração US2 e rodada final em pastas distintas; cada uma com 18 métodos originais OK, 12/12 pares B e 48/48 pares reais de variantes conformes. Zero divergências/erros/lacunas na bancada. T07/MC-04 muda apenas motivo; T12/MC-03 executado sem filtro. Controles sintéticos separados, 17 métodos finais OK, sem compor os 48 pares. Originais, comandos/retornos/stdout/stderr, fontes, hashes e diffs preservados. [Relatório e rastreabilidade](../specs/003-mudancas-controladas/evidencias.md).

Desvio de engenharia M-01 encontrado em controles adicionais: o fechamento não revalidava fonte/log entre execução e consolidação. Dois testes sintéticos reproduziram código 0 indevido. Correção: revalidar hashes/arquivos no fechamento e retornar 2 com integridade inválida. Falhas originais e versão corrigida arquivadas em `sintetico-integridade-final-red/` e `sintetico-final-green/`; rodada final posterior integral conforme. Não houve alteração no gabarito, na política ou nas variantes para acomodar resultados. Nenhuma suspeita de erro na referência foi identificada; T031 concluída pela conferência de ausência de ocorrência, sem inventar revisão/resolução.

35 tarefas concluídas com vínculos a evidências; baseline/testes/materiais/referência 0.2 e conjuntos 2/4/8/5 preservados. P-01/P-02/P-03, expectativas T12 e adoção constitucional continuam pendentes. T12 já adotado em B; não pedir nova adoção. Revisão profissional, possíveis novos modelos e mudanças nas métricas aguardam transcrição da orientação e decisão explícita. Textos datados da referência de B são preservados como fonte histórica; observações novas ficam nas evidências externas à referência. Próxima ação: revisão humana, sem liberar etapas experimentais.


## Revisão das tarefas da Spec 003 — 21/10/2026

**D-19 — Autorização do pesquisador.** Responsável: usuário/pesquisador; evidência: pedido explícito nesta conversa para revisar tasks existente, completar apenas o necessário, analisar consistência e reconciliar estado. Somente documentação; sem variantes, testes ou chamadas ao LLM. Revisão profissional, possíveis novos modelos e mudanças nas métricas aguardam transcrição da orientação e decisão explícita.

Conferência pelo assistente: árvore inicialmente limpa; HEAD `8041b0b1deca09f13c8b95069699616c7a1a7a60`; Spec 003 em `.specify/feature.json`, confirmada por `check-prerequisites.sh --json --require-spec --require-tasks --include-tasks`. B disponível; blobs de código/testes/JSON coincidem com o plano. Diff contra B vazio para código, testes, JSON, requisitos, catálogo e evidências T12. Referência 0.2 candidata sem revisor/data; 12 casos, 48 expectativas e seleções 2/4/8/5 preservados.

35 tarefas mantidas pendentes; T024 esclarece controles sintéticos no teste novo e matriz real no verificador, sem depender da CLI futura T027. Nenhuma tarefa concluída por inspeção. Notas vigentes preservam os registros históricos. Análise posterior somente de leitura pela skill local speckit-analyze, com relatório na resposta; sem implementação ou execução da bancada. Pendências científicas e adoção constitucional preservadas.


## Tarefas e análise documental da Spec 003 — 20/10/2026

**D-18 — Autorização do pesquisador.** Responsável: usuário/pesquisador; evidência: pedido explícito nesta conversa para gerar tarefas da Spec 003 pelo fluxo local e analisar a consistência Spec/plano/tarefas, preservando expectativas, conjuntos e pendências científicas. Autoriza somente trabalho documental e reconciliação de contexto; não autoriza implementar variantes, executar testes, iniciar piloto ou chamadas ao LLM experimental. Não representa aprovação científica do orientador ou ratificação constitucional.

Execução documental pelo assistente em 20/10/2026: Spec ativa 003 em `.specify/feature.json`, confirmada por `setup-tasks.sh --json`; template local e research/data-model/contracts/quickstart disponíveis. Árvore inicialmente limpa, HEAD `53bbac223e17dd15516a6d0172275ed995b7dd46`. Leitura dos blobs de B `aec474bcb54d6dae2afceff8e5b9226991386490` confirmou 18 métodos/T12 e referência candidata 0.2 com 12 casos/48 expectativas/conjuntos 2/4/8/5; nenhum módulo da bancada importado ou teste executado.

Gerado [tasks.md](../specs/003-mudancas-controladas/tasks.md): **35 tarefas, todas pendentes**; Setup 2, Fundação 6, US1 9, US2 8, US3 6, Fechamento 4. Quatro tarefas paralelizáveis, somente fontes distintas das variantes após pré-condições. Formato/IDs/caminhos/links conferidos documentalmente; baseline, testes, materiais e referência intactos. Geração pela [skill tasks](../.agents/skills/speckit-tasks/SKILL.md); análise posterior pela [skill analyze](../.agents/skills/speckit-analyze/SKILL.md) em modo somente leitura, com relatório na resposta desta solicitação e sem corrigir silenciosamente achados. Sem arquivo de implementação criado.

Estado de engenharia: especificação, planejamento e tarefas documentados, ainda sem variantes ou teste novo executável. A análise não é teste da aplicação, validação científica ou autorização de implementação. P-01/P-02/P-03 e adoção constitucional continuam pendentes; T12 já adotado em B, expectativas das mudanças ainda candidatas sob P-02. Próxima ação: revisar tarefas e eventuais achados da análise; implementação exige pedido próprio. Registros anteriores mantêm o histórico das etapas, superados apenas no alcance autorizado por D-18.

## Planejamento da Spec 003 — 19/10/2026

**D-17 — Autorização do pesquisador e fechamento documental.** Responsável pela autorização: usuário/pesquisador; evidência: pedido explícito nesta conversa para planejar a Spec 003 pelo fluxo local, selecionar/confirmar a feature ativa, manter Python + unittest e preservar expectativas/conjuntos. Autoriza cinco artefatos de planejamento e reconciliação documental; não autoriza tarefas, variantes implementadas, teste de aplicação, piloto ou LLM experimental. Execução técnica documental: assistente, 19/10/2026. Não representa aprovação científica do orientador ou ratificação constitucional.

Árvore inicialmente limpa; HEAD `3cdff8ec1c82b4919bce3761364364754863ca81`. B permanece `aec474bcb54d6dae2afceff8e5b9226991386490`, já fixado na Spec. Leitura Git/AST confirmou RF-01–RF-04, 18 métodos/T01–T12, controles e JSON 0.2 com 48 expectativas e seleções 2/4/8/5. Código, testes, referência, requisitos, catálogo e evidências T12 sem diferença entre B e HEAD; nenhuma alteração relevante não commitada na inspeção inicial. Nenhum teste repetido nesta etapa.

Feature ativa persistida em `.specify/feature.json`: `specs/003-mudancas-controladas`. `check-prerequisites.sh --json --paths-only` confirmou destino de FEATURE_SPEC/IMPL_PLAN antes de `setup-plan.sh --json`; template copiado em 003. Setup e criação de contracts inicialmente negados pelo sandbox e repetidos com autorização técnica. BRANCH no JSON é contexto, sem branch/commit criado. Fluxo [speckit-plan](../.agents/skills/speckit-plan/SKILL.md), sem hooks de extensão; pesquisa técnica local e revisão auxiliar de leitura previstas pela skill, sem chamadas experimentais.

Artefatos: [plan](../specs/003-mudancas-controladas/plan.md), [research](../specs/003-mudancas-controladas/research.md), [data-model](../specs/003-mudancas-controladas/data-model.md), [contrato](../specs/003-mudancas-controladas/contracts/verificacao.md) e [quickstart](../specs/003-mudancas-controladas/quickstart.md). Desenho escolhido: quatro módulos independentes copiados diretamente de B, edição mínima e diff/AST; verificador local com snapshot/hashes e registros esperado/observado por par; 12 casos em cada variante, sem filtro de seleção. Suíte inicial preservada. Representação e comandos estão planejados, não implementados ou executados.

Constituição conferida antes/depois do desenho, sem violação ou dúvida técnica bloqueante. P-01/P-02/P-03 e adoção formal continuam pendentes; P-04 já tem T12 adotado/verificado em B, expectativas das mudanças permanecem candidatas. Gabarito/seleções não alterados. Próxima ação: revisão do planejamento e solicitação de tarefas quando desejado; nenhuma etapa seguinte iniciada automaticamente. Registros anteriores abaixo são históricos nos alcances superados por D-17.

## Adoção de T12 e fechamento técnico — 19/10/2026

**D-15 — Autorização do pesquisador.** Responsável: usuário/pesquisador. Evidência: pedido explícito nesta conversa, “Confirmo a adoção de T12 no catálogo da bancada”, com entrada ativa, Supervisão + Auditoria, exportar e resultado inicial negar/conflito. Autoriza acrescentar o teste, executar isolado e suíte integrada, atualizar catálogo, rastreabilidade, referência candidata/JSON e artefatos dependentes, preservar histórico e reconciliar estado/handoff/pendências. Justificativa: acrescentar a operação exportar sob conflito herdado, complementando T07. Não atribui aprovação científica ao orientador nem adota formalmente a constituição. Não autoriza implementar/executar variantes, piloto ou chamadas ao LLM experimental.

Expectativas candidatas autorizadas para registro: MC-01 negar/conflito, preservação selecionada; MC-02 permitir/permissao_direta, mudança selecionada; MC-03 negar/conflito, excluído pela política; MC-04 permitir/permissao_direta, mudança selecionada. MC-04 aqui é a retirada de herança já identificada como **MC-04-v2**; mantém-se esse ID no JSON para evitar ambiguidade com a antiga mudança de estado. Não há acumulação: cada mudança parte da mesma versão inicial.

**D-16 — Fechamento de engenharia sob D-15.** Responsável pela execução: assistente, 19/10/2026. Evidências em [evidencias-t12.md](evidencias-t12.md): Python 3.13.3; T12 isolado OK; suíte integrada com 18 métodos OK, sem falhas/erros/ignorados. T01–T11, seis métodos auxiliares, controles e regras preservados; somente T12 foi acrescentado ao código de testes. Nenhuma divergência na versão inicial; resultado negar/conflito conforme RF-03/RF-04, prevalecendo sobre exportar direto de RF-02.

Catálogo vigente T01–T12; 48 pares teste × mudança e 60 expectativas com a versão inicial. Referência candidata 0.2, seleções 2/4/8/5; conjuntos de RFs intactos. Histórico anterior preservado literalmente com hashes em [pré-T12](historico/pre-t12-2026-10-19/LEIA_PRIMEIRO.md). Foram harmonizados requisitos, testes, documento de revisão, materiais 01–06 e guia, JSON, estado, governança operacional e handoff. Bloco de definições comuns em `materiais/07_DEFINICOES_COMUNS.md`, obrigatório e igual às quatro condições, sem respostas; notas candidatas intactas. Schema sem restrição de IDs não exigiu alteração; manifesto continua não congelado. Artefatos das Specs são históricos do incremento e recebem aviso de complemento em D-15, preservando evidências antigas.

P-04: **adoção e engenharia concluídas**, expectativas das mudanças ainda candidatas e sujeitas à revisão humana em P-02. P-01/P-02/P-03 e adoção constitucional permanecem abertas nos seus demais alcances. Próxima ação: revisão humana da referência 0.2, notas, política e medidas; revisor/data a combinar. Variantes não implementadas nem executadas; sem piloto/LLM experimental. Registros abaixo são históricos e seus limites não revogam D-15.

## Fechamento anterior — 18/10/2026

D-14 — Execução técnica pelo assistente sob autorização D-13, em 18/10/2026. Evidências: [quickstart da Spec 002](../specs/002-heranca-incompatibilidade/quickstart.md), relatório bruto final e revisão do diff. T001–T022 concluídas; RF-01–RF-04 integrados, 17 métodos OK, onze casos com decisão/motivo conformes e 55 subtestes. Dez métodos originais e expectativas preservados. Estado precede conflito, direta precede herdada. Domínio válido ampliado; verificação dirigida sem T12. Sem alteração de gabarito, materiais, variantes, piloto ou chamadas experimentais. D-09 e P-01/P-02/P-03/P-04 preservados; engenharia não equivale a validação científica. Nenhuma pendência funcional bloqueante no incremento; próxima etapa exige autorização própria.

## Autorização anterior — 18/10/2026

D-13 — Responsável: usuário/responsável do projeto; evidência: pedido explícito nesta conversa para implementar a Spec 002 seguindo suas 22 tarefas com Python e unittest. Autoriza implementação, testes locais e reconciliação documental; preserva gabarito e T12 como proposta. Não autoriza variantes, piloto ou LLM experimental nem representa aprovação científica ou adoção formal da constituição.

Reconciliação prévia: tasks, estado e handoff já registravam geração de 22 tarefas e análise em 16/10, posteriores ao planejamento D-12. BLOQUEIOS e a próxima ação de D-12 estavam desatualizados. Esses limites são históricos, superados pelo pedido atual apenas no alcance de engenharia. Nenhuma divergência funcional bloqueante identificada.

## Planejamento da Spec 002 — 16/10/2026

D-12 — Responsável pela autorização: usuário/responsável do projeto; evidência: solicitação explícita desta conversa para selecionar Spec 002 e preparar planejamento técnico com Python + unittest, aproveitando organização existente. Autoriza somente cinco artefatos de planejamento, seleção local e reconciliação de estado/handoff/bloqueios/decisões. Sem geração de tarefas, código, testes de aplicação, variantes, piloto ou LLM experimental; não registra aprovação científica.

Seleção pelo mecanismo local documentado em common.sh: .specify/feature.json → specs/002-heranca-incompatibilidade. Destino confirmado por check-prerequisites.sh --json --paths-only antes de setup-plan.sh --json, que copiou o template no destino certo. BRANCH no JSON é identificador de contexto; nenhuma branch criada. Sandbox inicialmente negou escrita do setup e criação de contracts; repetições com permissão técnica concluídas. O apontador é estado local ignorado pelo Git.

Desenho em [plan.md](../specs/002-heranca-incompatibilidade/plan.md): funções puras de efetivos e incompatibilidade; consulta direta preservada; estado → conflito → decisão por permissão, com direta antes de herdada e ausência por último. Interface existente conservada; domínio ativo ampliado apenas na implementação futura. Nenhuma nova decisão funcional necessária ou contradição bloqueante identificada; preferência direta/herdada já consta no contrato completo.

Cinco artefatos produzidos: plan, research, data-model, contracts/autorizacao e quickstart. Revisão documental pré/pós-desenho conforme constituição, sem exceções identificadas. Testes antigos não repetidos e testes novos não executados; RF-03/RF-04 continuam não implementados. T12 fora dos critérios; gabarito e catálogo intactos. Adoção formal da constituição, P-01 parcialmente atendida e P-02/P-03/P-04 continuam pendentes. Próxima ação: revisão e solicitação de tarefas.

Registros anteriores abaixo preservam o histórico; seus limites temporais não revogam D-12.

## Fechamento de engenharia — 16/10/2026

D-11: execução técnica pelo assistente sob autorização D-10; evidências observadas em [evidencias.md](../specs/001-autorizacao-direta/evidencias.md). Python 3.13.3; 10 métodos unittest OK; SC-001–SC-004 atendidos no domínio parcial. T001–T017 concluídas com revisão código/contrato/documentação. RF-03/RF-04 futuros, sem alteração de contrato ou expectativas T05–T08; referência original preservada. Sem piloto ou LLM experimental. Retorno científico permanece limitado a D-09 e proposta P-04.

## Registro vigente — 16/10/2026

D-09: orientador, conforme relato explícito do usuário nesta conversa (data do registro; data da manifestação não informada): recorte da bancada aceito, autorizado prosseguir. Gabarito, notas, prompts, métricas e piloto ainda serão revisados. P-01 parcialmente atendida quanto ao recorte; demais detalhes não recebem aprovação científica por consequência. P-02/P-03 continuam pendentes.

Ajuste solicitado: retirar a herança em MC-04 elimina o conflito em Supervisão + Auditoria, pois Consulta deixa de ser papel efetivo, e pode liberar exportar pela concessão direta de Auditoria. T07 continua correto para visualizar: baseline negar/conflito; sem herança negar/sem_permissao.

P-04: proposta do usuário, ainda não adotada nem executada: T12, ativa, Supervisão + Auditoria, exportar. Baseline negar/conflito; MC-04 sem herança permitir/permissao_direta. Antes de adotar, revisar relevância nas quatro mudanças, inclusões/exclusões, expectativas, conjuntos candidatos, notas/prompts, tamanho da suíte e cálculos/denominadores. Seriam 12 casos e 48 pares teste × mudança em vez de 11/44, sem alterar por si o número de chamadas. Catálogo e referência JSON permanecem preservados.

D-10: usuário, pedido explícito desta conversa em 16/10/2026: implementação da Spec 001, 17 tarefas, Python + unittest e testes locais autorizados. Supera restrições temporais anteriores somente nesse alcance. Sem RF-03/RF-04, piloto ou LLM experimental. Adoção formal da constituição pendente.

Conferência prévia de Spec/plano/tasks/modelo/contrato: sete casos coerentes, concessões próprias distintas da autorização final, estado primeiro e domínio parcial sem guarda adicional. Nenhuma contradição funcional bloqueante identificada; nenhum contrato alterado. Registros abaixo descrevem etapas históricas.

Registro inicial: 14/10/2026. Fontes: solicitação do usuário nesta conversa e [fontes e decisões](../materiais/06_FONTES_E_DECISOES.md). Não há aprovação do orientador registrada nos materiais consultados. Ausência de resposta ou aprovação parcial não aprova os demais pontos.

## Diretrizes com autorização registrada

| ID | Diretriz | Origem e alcance |
|---|---|---|
| D-01 | Preparar somente os seis documentos da baseline, preservando materiais. | Usuário, 14/10/2026; autorização documental, sem implementação ou abertura de Spec. |
| D-02 | Distinguir propostas, pendências e evidências; não declarar gabarito validado ou testes executados. | Usuário, 14/10/2026; vale para toda a baseline. |
| D-03 | Exigir resposta válida, seleção completa e IDs existentes para interpretar redução favoravelmente. | Usuário, 14/10/2026; harmonização com o protocolo candidato. |
| D-04 | Fazer o número de blocos depender das repetições finalmente definidas. | Usuário, 14/10/2026; cinco blocos não são quantidade fixa aprovada. |
| D-05 | Distinguir documentação preparada de liberação para piloto. | Usuário, 14/10/2026; condições de entrada permanecem obrigatórias. |

Estas autorizações não equivalem à aprovação científica do desenho pelo orientador.

## Três grupos de alinhamento com o orientador

| ID | Proposta submetida / decisão necessária | Situação e responsável esperado |
|---|---|---|
| P-01 — Objeto e casos | Manter seleção de IDs no módulo, impacto funcional em dependências, entrega sem framework geral e substituição da antiga MC-04 por retirada da herança (MC-04-v2). | Pendente de alinhamento com orientador; pesquisador registra resposta e ajustes. |
| P-02 — Referência e medidas | Confirmar política conservadora incluindo preservação; precisão, revocação e F1 separados para RF/testes, consistência e redução condicionada. Definir revisor do gabarito e das notas. | Pendente de alinhamento com orientador; revisão humana ainda não concluída. |
| P-03 — Execução | Confirmar D0/D1/E0/E1, uma chamada independente, piloto de 16, proposta de 80 chamadas principais, análise descritiva e congelamento após piloto. | Pendente de alinhamento com orientador; quantidade final depende da viabilidade. |

## Outras propostas e pendências

- Contrato de decisão/motivo, precedência e critérios dos RFs: revisão conforme [requisitos.md](requisitos.md), especialmente antes da implementação correspondente.
- Referência: revisor e data a combinar; registrar divergências e resolução antes do piloto. Notas também exigem revisão de origem e neutralidade.
- Tecnologias, modelo/configuração, isolamento e formatos: escolhas do pesquisador a registrar antes dos respectivos incrementos; sugestões em [arquitetura.md](arquitetura.md).
- Repetições, orçamento e ordem: fixar após avaliação de viabilidade e antes dos resultados principais. Para r repetições, planejar r blocos de 16 combinações; 80 chamadas correspondem somente à proposta r = 5.
- Avanço de etapa: esta entrega não autoriza implementação, abertura de Spec, piloto ou coleta. Futuras ações dependem de autorização no respectivo escopo e dos critérios do [roadmap.md](roadmap.md).

## Como atualizar

Para cada decisão futura, registrar ID, data, responsável pela aprovação, evidência da resposta, decisão e justificativa, ajustes solicitados, documentos/versões afetados e próxima ação. Enquanto não houver esse registro, manter o item como proposta ou pendência. Materiais históricos não são decisões simultaneamente vigentes; a substituição de MC-04 continua candidata.

## Atualização de engenharia — especificação e tarefas (14/10/2026)

| ID | Decisão e evidência | Alcance e efeito |
|---|---|---|
| D-06 | Usuário forneceu o contrato RF-01/RF-02 e solicitou `$speckit-specify` nesta conversa. | Base de engenharia para a Spec 001: estado, concessões próprias e decisão/motivo; RF-03/RF-04 ficam para o próximo incremento. Sem aprovação do orientador ou validação científica. |
| D-07 | Usuário declarou: “Confirmo Python + unittest e a organização mínima proposta como escolhas técnicas para o primeiro incremento.” | Python + biblioteca padrão unittest, sem terceiros; `autorizacao.py` e `tests/test_autorizacao.py`. Versão exata do interpretador a conferir no ambiente; 3.11+ é a compatibilidade proposta no plano. |
| D-08 | Usuário solicitou planejamento e, depois, geração de tarefas e análise de consistência nesta conversa. | Spec e plano existentes; tarefas documentadas, todas pendentes. Não autoriza implementação, execução de testes da aplicação, piloto ou coleta. Substitui as restrições temporais das entregas anteriores apenas nesse alcance. |

Responsável pelas confirmações acima: usuário/responsável do projeto; evidência: solicitações explícitas desta conversa em 14/10/2026. Justificativa técnica e desenho em [plano da Spec 001](../specs/001-autorizacao-direta/plan.md). Assinaturas e representações do contrato são desenho de implementação, sem alegar confirmação específica além da linguagem, ferramenta e organização declaradas pelo usuário.

P-01/P-02/P-03, adoção formal da constituição e revisão humana da referência/notas permanecem pendentes. O contrato completo RF-01–RF-04 não foi reduzido. Próxima ação: revisar tasks e, quando solicitado implementar, cumprir verificações e atualizar evidências reais.
