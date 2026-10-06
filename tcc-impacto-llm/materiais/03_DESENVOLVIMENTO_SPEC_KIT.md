# 3. Desenvolvimento incremental com Spec Kit

**Agora:** preparar e revisar especificação, arquitetura, testes e protocolo. Os comandos abaixo são um roteiro futuro; não foram executados para instalar ferramentas ou implementar a aplicação nesta entrega.

## 3.1 Três coisas diferentes

- **Metodologia incremental:** desenvolver uma capacidade pequena, conferir evidências e atualizar o contexto antes da próxima.
- **Spec Kit:** apoio para converter essa capacidade em especificação, plano e tarefas; Git registra as versões. A ferramenta não garante rastreabilidade ou revisão sozinha.
- **Experimento:** usa o módulo/documentos já estabilizados e mede respostas do LLM. Spec Kit, skills e histórico do desenvolvimento não entram automaticamente no contexto experimental.

Adotamos a sequência do documento de metodologia fornecido. A skill `fechar-spec` recebida pertence originalmente a outro projeto; aproveitar sua rotina de evidência, reconciliação, atualização, arquivo e handoff. Não copiar responsáveis, regras de parada ou nomes daquele projeto como se fossem decisões deste TCC. Não estamos criando ou instalando uma nova skill aqui.

## 3.2 Instalação planejada e versão

Exemplo com Codex CLI como assistente de desenvolvimento; isso não escolhe o provedor/modelo que será avaliado. Preparar Git, Python 3.11+, uv e o agente escolhido. Documentação oficial consultada em 29/09/2026 [F4–F7]. A release v1.0.12 foi localizada; fixá-la é uma proposta técnica a confirmar no ambiente.

No terminal, para uma PASTA NOVA:

```bash
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git@v1.0.12
specify version
specify check
specify init tcc-impacto-llm --integration codex
```

Registrar saídas e versões. Entrar na pasta criada, verificar se existe repositório Git e inicializá-lo se necessário; o versionamento não deve ser presumido só porque houve `specify init`. Não usar opções de sobrescrita sobre o material anterior. Guardar o pacote atual como proposta, sem promovê-lo inteiro a contexto do LLM avaliado.

As etapas do Spec Kit são acionadas no chat do agente, não no shell. Na integração Codex atual, usam `$speckit-constitution`, `$speckit-specify`, `$speckit-clarify`, `$speckit-plan`, `$speckit-tasks`, `$speckit-analyze`, `$speckit-implement` e `$speckit-converge`. Outras integrações/modos podem expor `/speckit-*` ou `/speckit.*`. Conferir o que a versão instalada oferece antes de seguir; tutoriais antigos podem usar `--ai` em lugar de `--integration`.

## 3.3 Preparar o contexto mínimo

| Artefato no futuro projeto | Conteúdo | Quem valida |
|---|---|---|
| `documentacao/escopo.md` | Pergunta, limites, decisões aprovadas e pendências | Pesquisador + orientador nas decisões de pesquisa |
| `documentacao/requisitos.md` | Quatro RFs, política e precedência | Pesquisador; referência revisada por humano combinado |
| `documentacao/arquitetura.md` | Núcleo local, testes, coleta isolada e avaliador | Pesquisador |
| `documentacao/protocolo.md` | Condições, entradas, métricas, falhas e repetições | Pesquisador + orientador |
| `documentacao/decisoes.md` | Data, decisão, justificativa e artefatos afetados | Responsável de cada decisão |
| `AGENTS.md` | Fontes que a IA deve ler; não ampliar escopo nem afirmar testes não executados | Pesquisador |
| `ESTADO_ATUAL.md`, `BLOQUEIOS.md`, `HANDOFF.md` | O que está pronto, o que falta e próxima ação | Pesquisador a cada incremento |

Não duplicar o gabarito dentro dos documentos exportados ao modelo. Usar uma pasta/ambiente de avaliação separado, sem acesso pelo processo que faz chamadas experimentais. Artefatos gerados pelo Spec Kit ficam no local criado pela versão instalada; não criar dezenas de Specs antecipadamente.

## 3.4 Texto inicial para a constituição

Acionar a etapa de constituição com esta orientação adaptada:

> Projeto de TCC com um módulo experimental pequeno e coleta controlada. Preserve quatro requisitos, três papéis, um nível de herança e a suíte aprovada. Não acrescente GUI, autenticação real, banco ou novos fatores experimentais. Separe propostas de decisões aprovadas. Cada tarefa deve ter critério de aceitação e evidência. Registre versões, mudanças e limitações. Não trate referência candidata como validada. O processo que consulta o LLM experimental recebe somente arquivos permitidos e nunca o gabarito. Após o congelamento, uma alteração exige nova versão e análise do impacto na coleta.

## 3.5 Roadmap de incrementos

| Incremento | Entrega pequena | Verificação para concluir |
|---|---|---|
| 0 — Documentação | Decisões, contratos, arquitetura e protocolo aprovados no que é essencial | Três decisões do resumo registradas; referência ainda claramente candidata se não revisada |
| 1 — Autorização direta | RF-01 e RF-02, decisão e motivo | Casos de estado e permissão direta exercitados; sem alegar que herança já funciona |
| 2 — Herança e conflito | RF-03 e RF-04; baseline completa | Onze casos executados, motivos corretos e precedência verificada |
| 3 — Variantes controladas | Quatro alterações isoladas e expectativas rastreadas | Conferir os 44 pares teste×mudança; baseline intacta; divergências resolvidas com referência |
| 4 — Coleta e avaliação | Payload isolado, registro bruto, parser e cálculo | Exemplos sintéticos de vazio, todos, exato, parcial, inválido e ID inexistente; nenhum dado real fabricado |
| 5 — Piloto e congelamento | Ensaio, relatório de ajustes e protocolo fechado | Critérios do documento 5 atendidos; quantidade principal fixada |
| 6 — Coleta e análise | Lotes principais e tabelas por condição | Rastreabilidade integral; falhas e desvios declarados; conclusões limitadas |

Incrementos 5 e 6 são atividades de pesquisa; não precisam virar desenvolvimento de novas funcionalidades se a bancada já suporta o procedimento.

## 3.6 Como usar o ciclo em cada incremento de software

1. **Specify:** informe a capacidade escolhida e os arquivos aprovados. Peça critérios observáveis, limites e dúvidas. Não peça “construa todo o TCC”.
2. **Clarify:** resolva ambiguidades reais e registre decisões. A IA pode propor, mas não declarar aprovação do orientador.
3. **Plan:** escolha arquitetura e tecnologias mínimas. Sugestão para avaliar: Python + pytest, arquivos JSON e chamadas por API, sem framework web; é proposta, não decisão anterior recuperada.
4. **Tasks:** decomponha a entrega em tarefas com RF, arquivo e evidência esperada. Diferencie planejamento, implementação e ensaio realizado.
5. **Analyze:** confronte requisitos, plano e tarefas; corrija contradições antes de implementar.
6. **Implement:** somente quando o incremento estiver autorizado e especificado; revisar as alterações e executar as verificações daquele incremento.
7. **Converge/fechamento:** reconciliar o realizado com o especificado, corrigir lacunas e registrar evidências. Usar a disciplina de fechamento do material fornecido: tarefas × provas reais, versões/fontes, documentação, cópia datada, gate, estado e handoff.

Exemplo para abrir o primeiro incremento, sem implementá-lo agora:

> Especifique somente a autorização direta com bloqueio por estado, conforme RF-01/RF-02 aprovados. A saída contém decisão e motivo. Não implemente ainda. Liste critérios de aceitação, dados de teste e ambiguidades. Marque RF-03/RF-04 como capacidade futura; não simplifique seus contratos globais por causa desta entrega parcial.

## 3.7 Arquitetura mínima

![Componentes propostos e separação do gabarito](diagramas/02_arquitetura.png)

O núcleo local recebe um caso e devolve decisão/motivo. Os testes verificam baseline e variantes. O montador de payload lê somente o pacote permitido; um cliente envia chamadas isoladas e um registrador preserva pedido/resposta. O avaliador local lê os registros e a referência separada, calcula métricas e produz tabelas. A interface entre coleta e avaliação são arquivos, não uma conversa compartilhada.

Não confundir a referência privada do avaliador com a documentação necessária ao desenvolvimento. O assistente de desenvolvimento pode ajudar a preparar candidatos, mas a validação humana da referência e a restrição do contexto experimental continuam necessárias.
