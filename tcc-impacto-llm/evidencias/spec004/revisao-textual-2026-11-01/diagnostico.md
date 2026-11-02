# Diagnóstico da revisão textual — D-29/D-30

01/11/2026. Responsável técnico: assistente sob pedido do pesquisador; revisão científica não realizada.

| Situação | Esperado, observado e resolução |
|---|---|
| Contrato anterior incompatível com limite confirmado | T014/T015 exigiam runner Windows restrito inexistente; não executadas. D-29 substitui a exigência por pacote textual verificável sem ferramentas do modelo. Mantidas desmarcadas, sem prova de SO aprovada. |
| Recortes novos antes do código | recortes-red registra falha por módulo ausente; os controles foram escritos antes do exportador. recortes-primeira registra quatro métodos aprovados após implementação, com esperados literais. |
| Autorização pelo próprio manifesto | Atualizar documento/manifesto não deve autorizar conteúdo diferente. Catálogo externo fixa manifesto/documentos; negativo com texto proibido fictício e próprio manifesto atualizado é bloqueado. Não se promete proteção contra substituição simultânea da autorização. |
| Caminhos Windows | Guardas ampliados para UNC/dispositivo, drive relativo, ADS e aliases. Positivos reais e negativos em montagem-revisada/entrada-avaliador conformes; nenhuma mudança de política de pontuação. |
| Symlink real | Criação retorna WinError1314; teste ignorado, sem contorno ou simulação como prova. Exigência de criação privilegiada substituída; links continuam entradas recusadas. Junctions reais internas/externas verificadas. |
| Primeira auditoria de snapshots | auditar-primeira.py exigia versão final do avaliador também no teste editorial anterior, que não importa/exercita avaliador. AssertionError em `recortes-primeira/avaliacao_ids.py`; escopo corrigido em auditar.py, que compara somente fontes exercitadas nessa execução e todas as fontes finais nas execuções posteriores. Nenhum teste, esperado, pontuação ou snapshot anterior alterado. |
| Aplicação documental | Primeira emissão de patch foi truncada pelo limite de saída da ferramenta e recusada antes da aplicação. Patch integral reaplicado; sem alteração parcial da tentativa rejeitada. Não é resultado funcional. |
| Entrega ao LLM | Não exercitada porque chamadas/modelo/piloto estão fora da autorização. Recibo local explicita envio não realizado; falta prova futura da plataforma e dos bytes efetivamente enviados. Não impede engenharia offline delimitada nem autoriza experimento. |

Não há divergência funcional observada nos confrontos atuais. Isso não demonstra cobertura universal ou adequação científica. Comandos, respostas sintéticas originais, payloads e fontes executadas estão nas tentativas identificadas do [relatório](relatorio.md); não se substituiu esperado pelo observado nem se alterou gabarito/notas.
