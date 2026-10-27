# Revisão parcial de engenharia — Spec 004

27/10/2026. D-26/D-27: convenções técnicas candidatas adotadas pelo pesquisador, revisão científica pendente. Sem LLM, piloto, alteração de gabarito ou notas reais.

## Resultado observado e limites

Implementados montagem permitida e avaliador offline, com CLI e originais/versionamento. Política ids-proposta-004-v2: rfs/tests separados, desconhecidos como FP único, duplicatas registradas, inválida/técnica sem seleção observada, imputação opcional separada. PONT-01 rejeita misturas com inventários separados por versão e sem combinado; para pontuar cada grupo, fornecer nova lista homogênea explícita, sem inventar denominadores. PONT-02 bloqueia célula com duplicidade por configuração/mudança/condição/repetição; tentativas técnicas vinculadas não viram repetições. Jaccard informa observações/pares e não calculável com menos de duas elegíveis.

Checkpoint montagem-final: seis métodos, cinco aprovados e um ignorado (symlink real, WinError 1314). Checkpoint avaliacao-confirmacao: 14 métodos aprovados, sem falhas/erros/ignorados. Confrontos detalhados, esperado/observado, comandos, retornos, stdout/stderr, fontes e cópias temporárias estão nas respectivas pastas. Os originais das execuções anteriores continuam preservados; não se somam repetições dos mesmos controles como observações de pesquisa.

matriz.json contém os confrontos por família/subcaso: 15 famílias conformes no escopo offline, S-14 parcial. Quantidade de métodos/arquivos/links não comprova correção. A evidência funcional são os valores e estados efetivamente confrontados com expectativas prévias, incluindo os casos negativos e fracções do contrato. Sem afirmação de cobertura universal.

Demonstração persistente pela CLI em demonstracao-001, com snapshots/comando em demonstracao-comando: quatro pacotes fictícios, conteúdo exato de entrada, respostas originais, referências sintéticas privadas e resumos A/B. Origem sintética explicitada; não são respostas de LLM. O exemplo foi executado antes do endurecimento para lstat sem seguir links; seus hashes identificam essa versão, e os checkpoints finais identificam a versão atual. Não sobrescrever a demonstração original.

## Impedimentos concretos

T014/T015: não foi disponibilizado runner sob identidade separada com leitura negada das zonas de desenvolvimento/referência/avaliação. O token atual lê a candidata; não cumpre a fronteira exigida. Nenhuma conta, ACL, credencial ou elevação foi usada para contornar essa restrição. Provas em isolamento/ambiente.json e capacidades-verificadas.json. Junctions reais demonstram recusa de caminhos, não isolamento por identidade. A criação de symlink real também foi negada pelo Windows (WinError1314); teste explicitamente ignorado, sem simulação apresentada como prova real.

39 tarefas independentes concluídas; T014/T015 e T042–T048 permanecem pendentes. Foram produzidos diagnóstico e documentos parciais, que não concluem tarefas dependentes do isolamento/integração integral. T036 está resolvida documentalmente pelo pedido explícito, sem aprovação científica presumida. Nenhuma etapa experimental liberada.

## Divergências de desenvolvimento preservadas

fundacao-red/avaliacao-red: módulos ausentes, falha esperada dos controles escritos antes do código. avaliacao-primeira: restrição de saída excessiva rejeitava uma pasta nova irmã dos arquivos de entrada; corrigida preservando recusa de sobreposição das fontes/pasta existente. Nesse checkpoint, o caso de observação ausente reutilizava indevidamente uma tentativa cujo vínculo anterior não estava na lista; corrigida a construção da fixture para representar uma observação única, mantendo expectativa 1/2 de completude. Não se ajustou escore para acomodar o observado. avaliacao-segunda/final/confirmacao preservam as verificações posteriores e novos controles de rechecagem/pares/desconhecidos.

## Preservação e pendências científicas

preservacao.json confere SHA-256 de todas as fontes protegidas do inventário inicial: código/testes anteriores, bancada/evidências 003, materiais, notas e gabarito permanecem intactos. Documentos originais anteriores às decisões atuais estão arquivados em preparacao/arquivos-iniciais. Hash comprova preservação, não validade científica. Checklist de qualidade não foi remarcada.

Revisão profissional da referência/política/expectativas T12, conteúdo definitivo/origem/neutralidade das notas, fundamentação/revisão de precisão/revocação/F1/consistência, desenho final do piloto e adoção constitucional permanecem pendentes. T12 já adotado; sem nova adoção. Não há fechamento integral da Spec 004.
