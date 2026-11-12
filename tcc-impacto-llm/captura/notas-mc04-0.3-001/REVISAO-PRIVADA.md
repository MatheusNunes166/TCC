# Revisão privada do bloco de notas — D-46

**NÃO ENVIAR ESTE GUIA, PLANO OU MAPA AO MODELO.** Preparação candidata offline; zero chamadas.

MC-04-v2 × Sol/Astra medium × direta/estruturada × duas notas × duas repetições = **16 planejadas**. D1/E1 identificam somente a estrutura com notas; `nota_id` é fator separado e obrigatório na análise. Oito células de N=2, dois blocos de oito, semente local 20261111. Não misturar com as 64 anteriores nem agregar repetições de N01/N02 como uma única célula.

## Par final, candidato à revisão humana

### N01 — coerente (rótulo privado)

> Observações simuladas de análise de testes: hábitos de outros sistemas de autorização podem induzir suposições incompatíveis com uma política fechada. Uma dependência pode mudar o valor produzido por uma regra cujo texto permanece intacto; compartilhar um cenário, por si só, não demonstra esse impacto. Restrições de maior precedência podem ocultar uma alteração na saída final, sem retirar a relevância de um caso abrangido pela política de seleção. Uma decisão igual pode esconder mudança de motivo; conservar ambos também pode ser relevante, quando a entrada está abrangida pela política. Confundir papéis atribuídos com efetivos, ou usar a variante para decidir a aplicabilidade, pode omitir interações previstas na versão inicial. Uma mudança na herança pode alterar um conflito quando modifica os papéis efetivos.

SHA-256: `e4f699fde739544eb851358e27aa9abeef0ec3584d97af9293d248441f71a68d`.

### N02 — incorreta (rótulo privado)

> Observações simuladas de análise de testes: hábitos de outros sistemas de autorização podem induzir suposições incompatíveis com uma política fechada. Uma dependência pode mudar o valor produzido por uma regra cujo texto permanece intacto; compartilhar um cenário, por si só, não demonstra esse impacto. Restrições de maior precedência podem ocultar uma alteração na saída final, sem retirar a relevância de um caso abrangido pela política de seleção. Uma decisão igual pode esconder mudança de motivo; conservar ambos também pode ser relevante, quando a entrada está abrangida pela política. Confundir papéis atribuídos com efetivos, ou usar a variante para decidir a aplicabilidade, pode omitir interações previstas na versão inicial. Uma mudança na herança nunca altera um conflito, mesmo quando modifica os papéis efetivos.

SHA-256: `cde836ed09080c10ad9fe1f591e9a2186c074205f88feec33d68210e25d98b33`.

O par conserva integralmente a nota 0.2-local anterior, exceto a quebra final, à qual se acrescentam um espaço e a afirmação candidata. Somente essa afirmação difere entre as novas notas. N02 contradiz deliberadamente o contrato: retirar a herança altera papéis efetivos e pode eliminar o conflito dependente dessa expansão. A referência candidata 0.3 permanece a mesma para ambos os braços; a nota não redefine o gabarito. O restante do conteúdo, a instrução de sistema e a advertência comum de usar o material fornecido são idênticos; nenhuma advertência exclusiva foi acrescentada.

## Diferenças dos payloads

- N01 → N02, com modelo/estrutura fixos: somente a afirmação final de `notas.md`.
- Direta D1 → estruturada E1, com modelo/nota fixos: somente `pedido.txt`, literal do plano 003.
- Sol → Astra: payload idêntico; no corpo da requisição muda somente `model`.
- R01 → R02: payload e corpo idênticos; IDs/ordem/repetição ficam fora do input.

Os oito diffs efetivamente calculados estão em [diferencas-payloads.json](diferencas-payloads.json). Em todos os pacotes permanecem sistema, definições, requisitos, catálogo 0.3 com resultados da baseline, MC-04-v2 e schema originais. O modelo recebe somente o payload, sem nomes de pasta, IDs de nota ou mapa.

## Saída, interpretação e execução futura

Preservar JSON com `requisitos` e `testes`; avaliar seleção, omissões e excedentes pelas mesmas fórmulas. IDs sozinhos não demonstram reconhecimento explícito da contradição. O par difere também em comprimento (pode/nunca, quando/mesmo quando); com duas repetições por célula, o resultado futuro será exploratório. Não há braço sem nota neste bloco e as 64 respostas anteriores não são controle intercambiável.

Configurações anteriores foram copiadas literalmente: modelos/medium, 4096, timeout 120 s, ferramentas vazias, sem histórico/retries, mesma modalidade de saída textual. A declaração USD 2 nelas é histórica; não se transfere autorização nem orçamento para este bloco (`orcamento_novo_declarado_usd=null`).

`preparar_bloco_notas.py` oferece somente `preparar` e `conferir`; não captura nem envia. O plano tem etapa própria e `envio_autorizado=false`; a CLI antiga da extensão 64 recusa este plano. Antes de executar futuramente, faltam revisão humana do par/pacotes/ordem, autorização própria e integração específica da captura/avaliação para preservar o fator nota e a fase exploratória. Os montadores e o corpo API já foram reutilizados; não se declara o envio integrado.

A conformidade anterior não é alterada por esta preparação. Não se preenchem aprovações humanas.

## Ordem planejada completa

| Ordem | Bloco | Observação |
|---:|---:|---|
| 1 | 1 | NOTA03-MC-04-v2-D1-N02-ASTRA-R01 |
| 2 | 1 | NOTA03-MC-04-v2-D1-N01-SOL-R01 |
| 3 | 1 | NOTA03-MC-04-v2-D1-N01-ASTRA-R01 |
| 4 | 1 | NOTA03-MC-04-v2-E1-N02-SOL-R01 |
| 5 | 1 | NOTA03-MC-04-v2-D1-N02-SOL-R01 |
| 6 | 1 | NOTA03-MC-04-v2-E1-N01-ASTRA-R01 |
| 7 | 1 | NOTA03-MC-04-v2-E1-N01-SOL-R01 |
| 8 | 1 | NOTA03-MC-04-v2-E1-N02-ASTRA-R01 |
| 9 | 2 | NOTA03-MC-04-v2-D1-N01-ASTRA-R02 |
| 10 | 2 | NOTA03-MC-04-v2-E1-N02-ASTRA-R02 |
| 11 | 2 | NOTA03-MC-04-v2-D1-N02-SOL-R02 |
| 12 | 2 | NOTA03-MC-04-v2-E1-N02-SOL-R02 |
| 13 | 2 | NOTA03-MC-04-v2-D1-N02-ASTRA-R02 |
| 14 | 2 | NOTA03-MC-04-v2-D1-N01-SOL-R02 |
| 15 | 2 | NOTA03-MC-04-v2-E1-N01-ASTRA-R02 |
| 16 | 2 | NOTA03-MC-04-v2-E1-N01-SOL-R02 |
