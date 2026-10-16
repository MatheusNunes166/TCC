# Guia futuro de verificação — Spec 002

Planejamento, não relatório de execução. RF-03/RF-04 ainda não implementados; nenhum teste executado nesta etapa. Não confundir os dez métodos existentes aprovados no incremento 1 com a integração futura.

## Preparação após autorização

Confirmar Python 3.11+ (3.13.3 usado no incremento 1), implementar segundo tarefas futuras e manter organização existente. Sem dependências a instalar. A partir da raiz tcc-impacto-llm, comandos futuros:

```powershell
python --version
python -m unittest discover -s tests -p 'test_*.py' -v
```

Não executar agora. Os arquivos atuais não contêm T05–T08; a suíte antiga sozinha não demonstra conformidade da Spec 002.

## Verificações exigidas

- Integrar T05/T06/T07/T08 aos sete IDs anteriores, comparar os onze dicionários inteiros da [Spec](spec.md); sem mudanças de expectativa ou casos ignorados.
- Conservar 32 subtestes de estado, três concessões próprias com retornos imutáveis/entradas preservadas/repetição e controle Auditoria/visualizar.
- Conferir ativa sem papéis e Supervisão + Consulta nas duas operações: quatro controles auxiliares; mesma resposta em chamadas repetidas e nenhuma mutação.
- Conferir efetivos nos oito subconjuntos com expectativas explícitas e independentes: vazio→vazio; Consulta→Consulta; Auditoria→Auditoria; Supervisão→Supervisão+Consulta; Consulta+Auditoria→mesmo; Consulta+Supervisão→mesmo; Auditoria+Supervisão→três; três→três.
- Conferir predicado de incompatibilidade nos oito subconjuntos já efetivos: verdadeiro somente nos que contêm Consulta e Auditoria. Entrada do auxiliar não é solicitação de autorização e não executa T12.
- Revisar que estado encerra antes de consultas, conflito antes de permissão, direta antes de herdada e ausência somente após considerar herança.

Manter dez métodos existentes e acrescentar quatro para T05–T08; antes dos controles novos, 14 métodos. Registrar contagem final real, separando métodos, cenários e subtestes. Aceitação não depende de uma contagem inventada de métodos.

## Evidências futuras

Registrar versão, data, comandos, revisão/diff, relatório bruto, contagens por categoria e falhas/resolução. Exigir onze IDs descobertos, 11/11 conformes e nenhum erro/falha/ignorado. Atualizar tarefas somente com evidências reais e revisar contrato/documentação antes de fechar.

O teste antes da implementação deve identificar capacidades ausentes ou divergência real, distinguindo erro de ambiente/importação e descoberta vazia. Os testes da integração devem ser executados após implementação; evidência do incremento 1 comprova somente o estado anterior.

## Limites

Não executar matriz completa de autorizar que inclua T12, nem criar seu teste de aceitação. T12 continua proposto fora da suíte; domínio futuro o abrange semanticamente, mas não há adoção do cenário. Nenhuma variante, piloto ou LLM experimental. Catálogo 11/44 e referência original preservados; resultados de engenharia não validam gabarito.

## Registro operacional desta etapa

Spec ativa selecionada em .specify/feature.json. Resolvido antes de gerar: `check-prerequisites.sh --json --paths-only` retornou FEATURE_SPEC e IMPL_PLAN na Spec 002. `setup-plan.sh --json` copiou template no mesmo destino; primeira tentativa negada pelo sandbox, repetição autorizada bem-sucedida. Criação da pasta contracts também exigiu permissão técnica. Nenhum bloqueio funcional identificado ou teste de aplicação executado.
