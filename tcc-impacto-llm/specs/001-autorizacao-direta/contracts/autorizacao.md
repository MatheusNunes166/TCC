# Contrato local proposto — autorização parcial

> Atualização vigente — 16/10/2026: RF-01/RF-02 implementados e verificados com Python 3.13.3 + unittest, sem terceiros. Sete casos de aceitação conformes, três concessões próprias, 32 combinações de estado e controle Auditoria/visualizar; 10 métodos, zero falhas/erros/ignorados. Evidências em `specs/001-autorizacao-direta/evidencias.md` (caminho desde a raiz). D-09/D-10 registram recorte aceito e autorização. Domínio ativo parcial somente Consulta ou Auditoria isoladamente; RF-03/RF-04 permanecem futuros. Afirmações de ausência de autorização/implementação nos registros de 14/10 abaixo são históricas, superadas somente nesse alcance. Constituição não formalmente adotada; referência, notas, prompts, métricas e piloto pendentes. Nenhum piloto ou LLM experimental executado.


Estado: desenho para revisão; nenhum módulo ou função implementado. Este é um contrato de chamada local, sem protocolo HTTP, interface ou serialização JSON obrigatória.

## Funções propostas

| Função | Entrada | Saída |
|---|---|---|
| `autorizar(estado, papeis, operacao)` | Estado string, papéis `frozenset[str]`, operação string. | Dicionário com exatamente `decisao` e `motivo`, ambos strings. |
| `obter_permissoes_diretas(papeis)` | Papéis `frozenset[str]` do vocabulário válido. | `frozenset[str]` de operações próprias dos papéis atribuídos, sem expansão de herança. |

São funções puras propostas: mesmas entradas produzem mesmos resultados no domínio garantido; sem I/O, consulta externa, estado global mutável ou alteração dos argumentos. A consulta de concessões não devolve referência mutável à política.

## Precondições e domínio garantido

- Vocabulário: estados `ativa`, `suspensa`, `em_revisao`; papéis `Consulta`, `Auditoria`, `Supervisão`; operações `visualizar`, `exportar`. Nenhuma conversão automática de grafia.
- Para `autorizar`, contas suspensas/em revisão são cobertas com qualquer subconjunto válido de papéis, inclusive vazio, e ambas as operações.
- Para `autorizar`, contas ativas são cobertas neste incremento com exatamente um dos papéis Consulta ou Auditoria. Esta limitação de uso/aceitação não é regra de acesso definitiva.
- A função de concessões próprias pode consultar qualquer conjunto válido, inclusive Supervisão isoladamente; ela não é decisão final de acesso.

Contas ativas com Supervisão ou combinações que dependam de RF-03/RF-04 não têm resposta garantida por este contrato parcial. Não definir negativa, permissão, exceção ou motivo substituto para esses cenários nesta etapa. Não usar a função parcial como autorização de produção; ela é a bancada incompleta delimitada na Spec.

## Decisão e motivo

| Situação abrangida | `decisao` | `motivo` |
|---|---|---|
| Estado não ativo | `negar` | `estado` |
| Ativa no recorte direto, operação concedida | `permitir` | `permissao_direta` |
| Ativa no recorte direto, operação sem concessão | `negar` | `sem_permissao` |

Consulta possui apenas visualizar; Auditoria possui apenas exportar; Supervisão não possui operações próprias. Os sete exemplos de aceitação são os da [Spec](../spec.md), sem alteração de IDs, entradas ou expectativas.

Os motivos `conflito` e `permissao_herdada` permanecem reservados no vocabulário completo. No próximo incremento, a obtenção de concessões próprias deve permanecer distinta da expansão de herança, e a decisão por permissão deve ocorrer depois de verificar conflito. Não consolidar a ausência temporária desses passos como regra de negócio. Em especial, o acesso herdado de Supervisão a visualizar e o conflito Consulta + Auditoria permanecem previstos no [contrato completo](../../../documentacao/requisitos.md).

## Verificação da interface

Comparar o dicionário inteiro nos testes de aceitação, incluindo nomes exatos das chaves e motivos. Para concessões próprias, comparar as três relações com valores esperados explícitos nos testes, independentes da tabela interna. A guarda de estado deve prevalecer para todas as entradas não ativas válidas, sem depender da consulta às regras futuras.
