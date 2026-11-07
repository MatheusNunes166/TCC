# Roadmap incremental

D-37, 07/11/2026: coletor mínimo implementado/verificado offline, com ordem registrada e captura/avaliação separadas. A passagem à etapa 5 continua bloqueada pelos controles experimentais da CLI; [evidências e limites](../captura/controles-coletor-2026-11-07/RELATORIO.md). Nenhum piloto executado.

Estado, capacidades e pendências: [ponto de entrada](../ESTADO_ATUAL.md). Registros datados anteriores preservados em [histórico](historico/pre-piloto-2026-11-06/LEIA_PRIMEIRO.md).

## Ciclo de cada capacidade

Seguir a [metodologia descrita nos materiais](../materiais/03_DESENVOLVIMENTO_SPEC_KIT.md): delimitar uma capacidade → esclarecer contratos → especificar, planejar e decompor tarefas quando autorizado → analisar coerência → implementar quando autorizado → verificar → reconciliar o realizado e atualizar contexto, decisões e próxima ação.

Fechar cada incremento com evidências reais vinculadas aos critérios, versões/fontes e limitações. Não encerrar pelo simples preenchimento de tarefas. As etapas de engenharia 1–3 foram executadas; a etapa atual prepara materiais e avaliação offline para o piloto. Spec Kit é apoio de desenvolvimento, não condição experimental nem mecanismo de validação científica.

## Capacidades e critérios de passagem

| Etapa | Entrega delimitada | Evidência necessária para concluir |
|---|---|---|
| 0 — Baseline de engenharia | Estes seis documentos, contratos candidatos e pendências explícitas. | Coerência documental conferida; decisões essenciais registradas para liberar o próximo trabalho. Documentos preparados não significam aprovações obtidas. |
| 1 — Autorização direta e estado | RF-01/RF-02 e saída decisão/motivo. | Contrato e implementação verificados na Spec 001; RF-03/RF-04 integrados na Spec 002. Evidências existentes vinculadas no estado central. |
| 2 — Herança e incompatibilidade | RF-03/RF-04 e baseline completa. | Doze casos da versão inicial executados após D-15, incluindo T12, decisão/motivo corretos e precedência conferida, incluindo conflito herdado e estado sobre conflito. |
| 3 — Mudanças e referência | Quatro variantes independentes e referência rastreável. | MC-04 escolhida; 48 pares teste × mudança (60 expectativas incluindo a versão inicial) conferidos contra expectativas humanas; baseline preservada; revisão, data e resolução das divergências registradas. |
| 4 — Preparação da coleta e avaliação | Montagem permitida, chamadas isoladas, registros brutos e avaliador separado. | Isolamento/payload inspecionados; configuração versionada; parser e métricas conferidos com exemplos sintéticos; falhas e orçamento definidos; notas revisadas. |
| 5 — Piloto e congelamento — pesquisa | Proposta de 16 chamadas: MC-01/MC-03 × quatro condições × duas repetições. | Todos os critérios de entrada e saída do material de piloto atendidos; relatório e ajustes registrados; novo ensaio se necessário; versões e repetições principais congeladas. |
| 6 — Coleta principal e análise — pesquisa | Execuções principais e comparação descritiva. | Integridade e desvios registrados; omissões, excedentes, validade e consistência apresentados por mudança/condição; conclusões limitadas ao recorte. |

As etapas 5 e 6 são atividades de pesquisa, sem exigência de novas funcionalidades se a bancada já atender ao procedimento. Os casos e a estratégia estão em [qualidade-e-testes.md](qualidade-e-testes.md).

## Gates e dimensionamento

A preparação documental não libera o piloto. Antes dele, precisam existir baseline e variantes verificadas, referência revisada, prompts/notas versionados, coleta rastreável, fronteira textual e ausência de acesso adicional verificadas e avaliador conferido. Ver os critérios completos em [piloto e coleta](../materiais/05_PILOTO_E_COLETA.md).

Para r repetições principais, planejar r blocos, cada um com as 16 combinações de quatro mudanças × quatro condições, em ordem aleatorizada e registrada. Total: 16r chamadas. Cinco blocos e 80 chamadas são apenas o cenário candidato r = 5. Fixar r antes da coleta principal; não ajustar por vantagem observada de uma condição.

Próxima ação e pendências vigentes: [estado central](../ESTADO_ATUAL.md). As próximas ações antigas do primeiro incremento constam no histórico preservado.
