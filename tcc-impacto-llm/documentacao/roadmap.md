# Roadmap incremental

Estado em 14/10/2026: baseline e governança preparadas; Spec 001, planejamento e tarefas existentes, com Python + unittest e organização mínima confirmados pelo usuário. Implementação e pesquisa não iniciadas. O desenho científico permanece candidato. As pendências estão em [decisoes.md](decisoes.md).

## Ciclo de cada capacidade

Seguir a [metodologia descrita nos materiais](../materiais/03_DESENVOLVIMENTO_SPEC_KIT.md): delimitar uma capacidade → esclarecer contratos → especificar, planejar e decompor tarefas quando autorizado → analisar coerência → implementar quando autorizado → verificar → reconciliar o realizado e atualizar contexto, decisões e próxima ação.

Fechar cada incremento com evidências reais vinculadas aos critérios, versões/fontes e limitações. Não encerrar pelo simples preenchimento de tarefas. A etapa atual termina em tarefas e análise documental; nenhuma implementação ou verificação da aplicação foi realizada. Spec Kit é apoio de desenvolvimento, não condição experimental nem mecanismo de validação científica.

## Capacidades e critérios de passagem

| Etapa | Entrega futura delimitada | Evidência necessária para concluir |
|---|---|---|
| 0 — Baseline de engenharia | Estes seis documentos, contratos candidatos e pendências explícitas. | Coerência documental conferida; decisões essenciais registradas para liberar o próximo trabalho. Documentos preparados não significam aprovações obtidas. |
| 1 — Autorização direta e estado | RF-01/RF-02 e saída decisão/motivo. | Contrato confirmado para o incremento; posteriormente T01–T04 e T09 verificados com resultados reais. RF-03/RF-04 continuam capacidades futuras; não executar a suíte completa como se já suportada. |
| 2 — Herança e incompatibilidade | RF-03/RF-04 e baseline completa. | Posteriormente onze casos executados, decisão/motivo corretos e precedência conferida, incluindo conflito herdado e estado sobre conflito. |
| 3 — Mudanças e referência | Quatro variantes independentes e referência rastreável. | MC-04 escolhida; 44 pares teste × mudança conferidos contra expectativas humanas; baseline preservada; revisão, data e resolução das divergências registradas. |
| 4 — Preparação da coleta e avaliação | Montagem permitida, chamadas isoladas, registros brutos e avaliador separado. | Isolamento/payload inspecionados; configuração versionada; parser e métricas conferidos com exemplos sintéticos; falhas e orçamento definidos; notas revisadas. |
| 5 — Piloto e congelamento — pesquisa | Proposta de 16 chamadas: MC-01/MC-03 × quatro condições × duas repetições. | Todos os critérios de entrada e saída do material de piloto atendidos; relatório e ajustes registrados; novo ensaio se necessário; versões e repetições principais congeladas. |
| 6 — Coleta principal e análise — pesquisa | Execuções principais e comparação descritiva. | Integridade e desvios registrados; omissões, excedentes, validade e consistência apresentados por mudança/condição; conclusões limitadas ao recorte. |

As etapas 5 e 6 são atividades de pesquisa, sem exigência de novas funcionalidades se a bancada já atender ao procedimento. Os casos e a estratégia estão em [qualidade-e-testes.md](qualidade-e-testes.md).

## Gates e dimensionamento

A preparação documental não libera o piloto. Antes dele, precisam existir baseline e variantes verificadas, referência revisada, prompts/notas versionados, coleta rastreável, isolamento demonstrado e avaliador conferido. Ver os critérios completos em [piloto e coleta](../materiais/05_PILOTO_E_COLETA.md).

Para r repetições principais, planejar r blocos, cada um com as 16 combinações de quatro mudanças × quatro condições, em ordem aleatorizada e registrada. Total: 16r chamadas. Cinco blocos e 80 chamadas são apenas o cenário candidato r = 5. Fixar r antes da coleta principal; não ajustar por vantagem observada de uma condição.

## Próxima ação e dúvidas do primeiro incremento

A base RF-01/RF-02 foi fornecida pelo usuário e a escolha Python + unittest com organização mínima foi confirmada (D-06/D-07). A próxima ação é revisar [tasks.md](../specs/001-autorizacao-direta/tasks.md) e, quando solicitado implementar, executar a sequência prevista com evidências reais. O material não apresenta contradição técnica que impeça delimitar essa capacidade. Escolha do LLM, quantidade final de repetições e revisão integral da referência não bloqueiam seu planejamento, embora sejam necessárias nas etapas posteriores.

Não há pergunta adicional indispensável para concluir esta baseline. A implementação ainda depende de solicitação para a nova etapa; a criação de tarefas não a executa nem presume aprovação científica.

