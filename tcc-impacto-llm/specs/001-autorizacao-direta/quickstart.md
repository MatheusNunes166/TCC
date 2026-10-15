# Guia futuro de validação — incremento 001

Este guia é parte do planejamento. Os arquivos Python descritos no [plano](plan.md) ainda não foram criados nesta etapa. Nenhum comando abaixo foi executado, nenhuma dependência instalada e nenhum teste realizado.

## Pré-requisitos futuros

Após revisão das propostas, geração de tarefas e autorização para implementar: dispor de Python 3.11+ e dos arquivos planejados `autorizacao.py` e `tests/test_autorizacao.py`. Registrar a versão exata usada. Não é necessário instalar pytest ou pacote de produção na proposta atual.

Executar os comandos a partir da raiz que contém `documentacao`, `materiais`, `.specify` e `specs`, usando `python` associado ao interpretador escolhido:

```powershell
python --version
python -m unittest discover -s tests -p 'test_*.py' -v
```

Não executar agora: não existe implementação a validar. Não interpretar descoberta de zero testes como sucesso; os IDs de aceitação precisam aparecer no relatório.

## Cenários e evidências esperadas

Conferir os sete pares de entrada/saída da [Spec](spec.md) por meio da interface do [contrato](contracts/autorizacao.md). T01–T04/T09 formam o núcleo; T10/T11 verificam apenas estado. Os nomes dos testes devem conter os IDs para rastreabilidade.

Conferir também as três concessões próprias (SC-003) e a verificação auxiliar de precedência descrita no plano (32 combinações não ativas). Esses controles auxiliares não se tornam novos testes T da suíte experimental. Conferir que entradas não são modificadas e que todas as saídas de aceitação possuem decisão e motivo exatos.

Resultado necessário para futura aceitação: cinco casos centrais conformes, dois complementares conformes, três relações de concessões conformes e nenhuma falha nas verificações auxiliares. Registrar comando, versão, data, revisão de código utilizada, contagens reais, falhas e relatório bruto. Não copiar uma saída esperada como se fosse resultado observado.

T05–T08 não integram esta execução parcial e não recebem resultados provisórios. O resultado futuro desses testes de engenharia não valida referência experimental nem libera piloto. Revisar alterações e evidências antes de atualizar estado/handoff e declarar incremento concluído.
