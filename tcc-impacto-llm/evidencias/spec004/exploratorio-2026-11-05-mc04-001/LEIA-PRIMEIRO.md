# Ensaio exploratório MC-04 — preparação 001

05/11/2026. **PREPARADO, NÃO ENVIADO.** Quatro chamadas previstas, zero realizadas: MC-04-v2 × D0/D1/E0/E1 × uma execução. MC-04 é o rótulo solicitado; o ID canônico existente é MC-04-v2, retirada de Supervisão → Consulta. Cada condição é independente sobre a mesma baseline, sem acumular mudanças.

Este ensaio é separado do piloto e da coleta principal. Todo resultado futuro deve manter `fase=exploratorio`, `incluido_piloto=false` e `incluido_coleta_principal=false`. Não transferir automaticamente respostas, contagens ou resumos para essas etapas. Uma observação por condição não estima efeito nem consistência entre repetições; Jaccard por célula será **não calculável**. A ordem da tabela é apresentação, não ordem de execução escolhida.

## Quatro entradas prontas

| Condição | Único conteúdo destinado ao modelo | Bytes UTF-8 | Registro local |
|---|---|---|---|
| D0 | [texto preparado](preparados/D0/payload.txt) | 6515 | [ficha planejada](registros/D0/registro-planejado.json) |
| D1 | [texto preparado](preparados/D1/payload.txt) | 6967 | [ficha planejada](registros/D1/registro-planejado.json) |
| E0 | [texto preparado](preparados/E0/payload.txt) | 6567 | [ficha planejada](registros/E0/registro-planejado.json) |
| E1 | [texto preparado](preparados/E1/payload.txt) | 7019 | [ficha planejada](registros/E1/registro-planejado.json) |

Foram reutilizados os quatro pacotes editoriais/autorizados de MC-04 da Spec 004 e executada a CLI existente do montador, sem alterar seus módulos. As seis fontes atuais e os recortes foram comparados com as autorizações congeladas antes de montar. [Conferência real](conferencia-condicoes.json), [comparação legível](DIFERENCAS.md), [versões](versoes.json), [planejamento](ensaio.json) e comandos em `comandos/montagem-D0.json` até `montagem-E1.json`. Saídas novas; originais anteriores preservados.

Somente o conteúdo integral de `payload.txt` deve entrar no contexto do modelo. Não enviar diretório, manifesto, autorização, ficha, este roteiro, pacote de revisão humana, referência ou histórico. Os demais arquivos são registros locais de preparação/avaliação. Nenhuma ferramenta de navegação/execução deve estar disponível ao modelo; não se alega isolamento por SO.

## O que você precisa conferir antes das chamadas

Itens abaixo **pendentes**, não declarações de revisão concluída:

- [ ] Ler os quatro textos integrais: requisitos, catálogo da baseline, uma mudança, schema e prompts; conferir ausência de resultados de variantes, seleções candidatas, código e histórico.
- [ ] Ler/comentar as notas rascunho antes de consultar conjuntos candidatos, quando possível; registrar exposição prévia. Conferir utilidade, origem e pistas de respostas, sem editar o bloco nesta rodada. [Pacote de revisão profissional](../../../documentacao/revisao-profissional-spec004-v1/LEIA-PRIMEIRO.md).
- [ ] Conferir os seis pares em DIFERENCAS.md: comuns iguais, notas só D1/E1 e pedidos apenas conforme material 04. Registrar responsável/data/observações na revisão do ensaio e de cada registro, sem atribuir revisão profissional ou aprovação científica.
- [ ] Definir ferramenta/modalidade, modelo e configuração disponível, ordem, forma de colar/transmitir texto integral e preservar a resposta. Registrar o que não for exposto pela ferramenta.
- [ ] Verificar contextos independentes, sem projeto/repositório anexado, memória recuperada, instruções personalizadas adicionais, conectores, busca web, execução ou outras ferramentas. Se a ferramenta não permitir cumprir/verificar esse limite, registrar a limitação antes de enviar.
- [ ] Confirmar a decisão de realizar somente este ensaio exploratório provisório. A presente etapa autoriza preparação, **não envio**; revisão científica, notas definitivas e desenho do piloto continuam pendentes.

## Configurações ainda não definidas

| Campo | Estado atual / o que decidir e registrar |
|---|---|
| Ferramenta e modalidade | Não definidas: identificar aplicação/interface ou API efetivamente usada; não presumir equivalência entre elas. |
| Modelo e versão | Não definidos; registrar nome reportado, versão/data quando disponíveis e limites de identificação. |
| Parâmetros | Temperatura, top_p, seed, limite de saída, modo de raciocínio e demais opções: não definidos. Fixar o que a ferramenta permitir, igual entre condições; declarar não exposto/default desconhecido sem inventar valor. |
| Saída estruturada forçada | Decidir se existe e será usada; mesma modalidade em todas as condições. O schema textual atual já é comum; não habilitar só em uma condição. |
| Entrega e papéis das mensagens | Definir envio do texto integral, sem instruções factuais extras. Se a ferramenta acrescentar mensagens/padrões, registrar seu conteúdo conhecido e limitações; não dividir/mudar blocos de forma diferente entre condições. |
| Contexto e recursos | Configuração efetiva de memória, instruções, busca, conectores, anexos e ferramentas ainda deve ser verificada; quatro contextos novos e independentes. |
| Ordem, datas e identificação | Ordem ainda nula; fixar antes das chamadas. Registrar contexto/execução, início/fim UTC e fuso local, ID da configuração de coleta e desvios. |
| Transporte/falhas e custos | Sem retentativa automática prevista. Registrar falha/fragmento sem substituir resposta; custo/tokens/latência só se disponíveis. Quatro chamadas previstas, não completar tentativas extras silenciosamente. |

`configuracao_preparacao_id=texto-autorizado-D29` identifica os artefatos preparados, **não** ferramenta/modelo/configuração real, ainda desconhecidos. Não usar esse ID como prova de configuração de coleta definida.

## Roteiro curto de envio futuro

1. Após a conferência e definição dos campos, preservar a ficha planejada e criar uma cópia `registros/<condicao>/registro.json` para o que realmente ocorrer. Registrar a ordem fixada e a configuração comum.
2. Abrir um contexto novo, verificar os recursos acima e registrar sua identificação. Não usar esta conversa de desenvolvimento nem conversa que já tenha visto referência/respostas.
3. Transmitir somente o texto integral do payload correspondente, uma vez, sem tradução, reescrita ou pedido complementar. Preservar o conteúdo efetivamente transmitido (e envelope/papéis, se houver) com hash; comparar ao preparado. Em interface de colagem, registrar os limites de observação de normalização/instruções ocultas.
4. Salvar a resposta original integral como recebida/exportada, antes de validar ou remover cercas/explicações. Falha, vazio, recusa e fragmento têm registros distintos; não pedir correção nem escolher uma resposta melhor.
5. Encerrar esse contexto e repetir nos outros três contextos, na ordem registrada. Registrar eventuais desvios. Avaliar depois, em etapa local separada, pela [orientação de avaliação](AVALIAR.md), sem devolver referência ao modelo.

[Campos de registro e preservação](REGISTRO.md). Os recibos atuais mostram `envio_realizado=false`; são registros de preparação, não provas de envio real. Manter esses arquivos originais mesmo depois das chamadas.
