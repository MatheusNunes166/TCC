# Conferência das quatro condições

05/11/2026. Conferência técnica realizada; **revisão do pesquisador permanece pendente**. Nenhum envio ou resultado de LLM.

Foram comparados bytes dos documentos com recortes das seis fontes autorizadas e com os pacotes/autorização existentes; depois, recomposto o payload independentemente pela ordem/delimitadores do contrato. O resultado coincide byte a byte com cada arquivo montado. O montador existente também confirmou o conjunto completo de condições.

## Conteúdo comum

Mesmos bytes em D0/D1/E0/E1: `sistema.txt`, `definicoes-comuns.md`, `requisitos-baseline.md`, `catalogo-baseline.md`, `mudanca.md` e `schema_saida.json`. Não há mudanças adicionais nas instruções de sistema ou nas regras. O catálogo inclui saídas esperadas da baseline, material permitido; não inclui saídas de variantes ou seleções de IDs.

`notas.md` está integralmente ausente em D0/E0, inclusive seus delimitadores. D1/E1 recebem exatamente a mesma nota atual, sem rótulo extra dentro do texto. Hash do bloco literal: `5f82ec8421a7ec27a92a718d27deb2a74cdb7538e12a80c662f27038c2f3cc34`. Rascunho não revisado; origem declarada: pesquisador no papel de analista, conforme materiais/04 §4.1, não depoimento de profissional externo.

## Pedidos literais

Direto, igual em D0/D1 (material 04 §4.5):

> Identifique os requisitos impactados pela mudança e selecione os testes existentes relevantes conforme as definições e a política de seleção fornecidas. Retorne somente os dois conjuntos de identificadores no JSON exigido.

Estruturado, igual em E0/E1 (material 04 §4.6):

> Organize a análise em etapas: examine a regra alterada; verifique as dependências funcionais; determine os requisitos impactados; aplique a política de seleção aos casos existentes; confira as duas listas. Retorne somente os dois conjuntos de identificadores no JSON exigido.

## Diferenças observadas nos seis pares

| Par | Únicos documentos diferentes | Resultado técnico |
|---|---|---|
| D0 × D1 | notas.md | Conforme |
| D0 × E0 | pedido.txt | Conforme |
| D0 × E1 | notas.md, pedido.txt | Conforme |
| D1 × E0 | notas.md, pedido.txt | Conforme |
| D1 × E1 | pedido.txt | Conforme |
| E0 × E1 | notas.md | Conforme |

Metadados de condição, IDs de preparação, instante e hashes também diferem legitimamente entre pastas; não entram no payload. Nenhuma instrução complementar foi inventada para substituir notas ausentes. [Confrontos e hashes completos](conferencia-condicoes.json). Quantidade de arquivos/pares não é prova por si: a conferência foi sobre o conteúdo, as diferenças previstas e a igualdade dos bytes.
