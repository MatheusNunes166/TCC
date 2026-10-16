# Handoff — 14/10/2026

## Handoff vigente — 16/10/2026

Spec 001 concluída para engenharia, T001–T017 comprovadas em [evidencias.md](specs/001-autorizacao-direta/evidencias.md). Código: autorizacao.py; testes: tests/test_autorizacao.py. Para reproduzir: `python -m unittest discover -s tests -p 'test_*.py' -v` na raiz; Python usado 3.13.3, 10 métodos OK, sem terceiros. Revisão sem divergência funcional ou mudança de contrato.

Ler D-09/D-10/P-04: orientador aceitou recorte, mas gabarito/notas/prompts/métricas/piloto serão revisados. MC-04 elimina conflito herdado e pode liberar exportar. T07/visualizar preservado; T12/exportar proposto, não adotado/executado. Revisar relevância nas quatro mudanças e cálculos/tamanho se adotado. Não alterar gabarito silenciosamente. Próxima capacidade RF-03/RF-04 mediante novo pedido. Preservar domínio parcial e precedência; nenhum piloto/LLM autorizado. Instruções de 14/10 abaixo são históricas e superadas somente neste alcance.

Siga a ordem de leitura de [AGENTS.md](AGENTS.md), depois leia Spec, plano, research, modelo de dados, contrato, quickstart e [tasks.md](specs/001-autorizacao-direta/tasks.md) da Spec 001.

Python + unittest e organização mínima estão confirmados (D-07 em [decisoes.md](documentacao/decisoes.md)). Spec/plano/tarefas existem; todas as tarefas continuam pendentes. A próxima ação concreta é revisar tarefas e, quando houver solicitação de implementação, começar pela preparação local e RF-01, depois RF-02, executando verificações previstas e preservando evidências.

O pedido atual não autoriza implementar ou executar testes da aplicação. Não retomar a criação de outra Spec nem reabrir a escolha Python/unittest sem motivo novo. Preservar o domínio parcial e os resultados originais T05–T08. Atualizar estado e documentos com evidências reais antes de fechar o incremento. Pendências científicas em [BLOQUEIOS.md](BLOQUEIOS.md) não são resolvidas pela confirmação técnica.
