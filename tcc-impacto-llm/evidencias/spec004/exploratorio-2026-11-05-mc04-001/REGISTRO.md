# Registro das quatro execuções futuras

05/11/2026. As fichas `registros/D0/registro-planejado.json` etc. reutilizam o [modelo existente](../../../materiais/modelos/registro_execucao.json), com campos adicionais locais para o ensaio. Estão **planejadas/não enviadas**, sem resposta fictícia, datas de envio ou revisão concluída. Não são entradas para a CLI sintética de avaliação.

Preservar cada ficha planejada e preencher uma cópia `registro.json` quando houver execução real. Caminhos nos campos são relativos à raiz deste ensaio (`exploratorio-2026-11-05-mc04-001`). Não sobrescrever os pacotes/recibos preparados ou respostas anteriores.

| Grupo | Campos a preencher com o que efetivamente ocorreu |
|---|---|
| Identificação/fase | run_id/observacao_id, fase=exploratorio, origem=llm_exploratoria após execução; condição, MC-04-v2, repeticao=1, ordem_real, contexto_id. Manter incluído no piloto/principal=false. |
| Ferramenta e modelo | ferramenta, modalidade_envio, modelo_reportado, versão/identificador conhecido; configuração_coleta_id próprio, separado do ID de preparação. |
| Configuração disponível | Parâmetros expostos e valores efetivos; opções não expostas/defaults desconhecidos; uso uniforme de schema/saída forçada; instruções/papéis e limitações observáveis. |
| Contexto independente | ferramentas_efetivas, anexos_efetivos e historico_efetivo; registrar verificação de ausência de acesso adicional ao ambiente, sem alegação de isolamento por SO. |
| Datas | data_inicio_utc, data_fim_utc e instante_utc reais, fuso America/Sao_Paulo; não usar a data da montagem como data da chamada. |
| Texto preparado | payload_arquivo/hash, preparacao_arquivo/ID/hash e manifesto_hash já preenchidos. Continuam apontando para a preparação não enviada. |
| Texto enviado | conteudo_enviado_arquivo e SHA-256 do conteúdo transmitido, por exemplo `registros/D0/conteudo-enviado.txt`; preservar envelope/papéis em campo/arquivo adicional se houver. Diferença frente ao preparado exige desvio explícito, não correção silenciosa. |
| Resposta original | resposta_bruta_arquivo, resposta_sha256, resposta_bytes, resposta_exportada_sem_edicao; exemplo `registros/D0/resposta-original.txt`. Guardar texto integral, inclusive cercas/explicações/recusa ou arquivo recebido vazio; não reserializar como “original”. |
| Estado técnico | status=REGISTRADA e status_tecnico=concluida ou falha_tecnica somente após ocorrência real; tentativas_transporte efetivas, causa_falha_tecnica, erro_tecnico_arquivo e fragmento_arquivo quando existirem. Não inventar resposta ausente. |
| Revisão | revisão_pesquisador: responsável/data/alcance/comentários reais, sem presumir aprovação profissional/científica. Campos de revisão continuam pendentes até registro explícito. |
| Observação operacional | latência, tokens, custo quando reportados; caso contrário, manter indisponíveis com justificativa. Registrar desvio, recusa, interrupção e limitações de exportação. |

A forma de captura ainda depende da ferramenta escolhida. Preservar a exportação original e, quando necessário, uma cópia textual identificada para avaliar. Copiar manualmente só a parte JSON e descartar o restante mudaria o objeto avaliado. Falha com fragmento não é resposta concluída; uma resposta concluída fora do JSON é formato inválido, não falha de execução.

Para consultar tamanho/hash de um arquivo realmente salvo (trocar condição/caminho conforme o caso):

```powershell
Get-FileHash -Algorithm SHA256 evidencias/spec004/exploratorio-2026-11-05-mc04-001/registros/D0/resposta-original.txt
(Get-Item -LiteralPath evidencias/spec004/exploratorio-2026-11-05-mc04-001/registros/D0/resposta-original.txt).Length
```

Executar da raiz do repositório. Esses comandos apenas consultam arquivos, não preenchem fatos ausentes. Repetir para conteúdo enviado e qualquer fragmento preservado. Uma execução por condição não autoriza trocar resposta ruim por nova tentativa nem incorporá-la à coleta principal.
