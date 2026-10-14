# Decisões, propostas e pendências

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
