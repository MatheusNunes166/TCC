# Operação do bloco documental de 64 observações

Decisão do pesquisador em 22/11/2026: incluir D0, D1, E0 e E1. A implementação
e os controles foram feitos offline. As chamadas reais serão iniciadas pelo
pesquisador na interface. Isso não registra aprovação científica do orientador,
revisão dos textos pelo pesquisador ou conformidade das respostas futuras.

Na pasta `tcc-impacto-llm`, execute:

```text
python apresentar.py
```

Em **Executar → Modo de execução**, selecione **Pesquisa documental • 64
observações • D0/D1/E0/E1**. Essa é uma coorte própria; **Demonstração livre**
continua disponível separadamente. Os controles de modelo e perfil da
demonstração não mudam o plano documental.

1. Consulte plano, configurações, próxima posição, concluídas, falhas e pendentes.
   **Ver payload da próxima posição** mostra os bytes textuais preparados e seu
   hash. Abertura, prévia, consulta e filtros não fazem chamadas.
2. Clique em **Executar próxima observação • 1 chamada paga**. A primeira ação
   admite somente uma chamada. Confira o original, modelo solicitado/reportado,
   tokens, completude e eventuais desvios antes de continuar, sem escolher pelo
   acerto da seleção.
3. Depois da primeira, escolha o **Limite deste envio** e clique em **Continuar
   lote • N chamadas pagas**. O número inclui apenas posições ainda não iniciadas.
   O servidor respeita esse limite e a ordem registrada. Pode parar antes do limite
   diante de falha técnica, formato inválido, divergência de modelo ou erro de
   avaliação; nunca envia posições extras para compensar a ocorrência.
4. Em **Resultados → Origem**, selecione **Pesquisa documental • 64 observações**.
   Em **Mais filtros**, use documentação, repetição, notas, situação e IDs de
   requisitos/testes relacionados, além dos filtros principais. Abra uma linha
   para consultar referência e seleção, acertos/omissões/excedentes, P/R/F1,
   correspondência exata, original, payload, metadados e pastas. A tabela de
   consistência usa somente repetições válidas da mesma célula e mantém N=2.

Configure `OPENAI_API_KEY` somente no ambiente do processo servidor antes de
abri-lo. A chave não é recebida pela página nem salva nos registros. Sem chave,
a consulta e a prévia continuam disponíveis. Não se exige orçamento positivo;
o limite é de chamadas solicitadas, sem garantia de teto monetário.

Se a comunicação da página falhar após o clique, use **Consultar estado** ou
recarregue o painel. Não repita o clique para tentar obter a mesma observação.
Há idempotência por ação e trava do sistema operacional entre processos.
Qualquer posição reservada antes de envio fica fora da fila de pendentes,
mesmo se faltar seu fechamento. Uma conexão interrompida conserva o fragmento
e o estado remoto desconhecido; nenhuma retentativa automática é feita.

O plano mantém medium, 4096 tokens máximos de saída, timeout de 120 s,
`tools=[]`, `tool_choice=none`, `store=false`, `stream=false` e zero retries.
Cada observação recebe uma requisição independente, sem conversa anterior.
O clique grava plano/manifesto, hashes dos payloads, limite e horário UTC real
do servidor. O navegador apresenta horários em America/Sao_Paulo.

## Desenho e arquivos

- MC-02 e MC-04-v2 × GPT-6 Sol e GPT-6 Astra × D0/D1/E0/E1 × CONSOLIDADA e
  OPERACIONAL × duas repetições: **64 posições, 32 células de N=2, dois blocos
  balanceados de 32 e 16 payloads únicos**. Modelo e repetição não alteram o texto.
- D0/E0 não contêm notas. D1/E1 usam a mesma nota original, sem N01/N02.
  Os pedidos diretos e estruturados são os perfis históricos literais.
- CONSOLIDADA reproduz os perfis preservados. OPERACIONAL troca somente
  `requisitos-baseline` pelos cinco documentos preparados; política comum,
  catálogo com quinze casos/seis colunas, mudança, nota aplicável, pedido e
  schema permanecem literais. A referência privada não entra na requisição.
- [Plano 002](../captura/documentacao-operacional-0.3-002/plano.json),
  [manifesto](../captura/documentacao-operacional-0.3-002/manifesto.json) e
  [diferenças](../captura/documentacao-operacional-0.3-002/diferencas.json).
  A preparação 001 de 32 posições e seu produtor permanecem literais e
  conferíveis como antecedente não executado; a proposta de retirar colunas
  não será executada. O [guia privado original](revisao-documentacao-operacional.md)
  continua como evidência do antecedente; sua seção D0/D1 descreve apenas o 001.
- Capturas futuras: `captura/documentacao-operacional-64-real-001/`.
  Avaliações futuras: `avaliados/documentacao-operacional-64-real-001/`.
  Identidades `DOCOP64-...`, fase `exploratoria_documental`, coorte
  `documentacao_operacional_64`. As demonstrações continuam `DEMO-...`.

O tratamento reúne distribuição, redação, explicações e extensão documental;
não isola cada componente nem garante maior dificuldade. A seleção das duas
mudanças é posterior a resultados conhecidos, sem amostragem aleatória de
sistemas/tarefas. Empates, piora e melhora serão preservados. Não se ajustam
textos, referência ou repetições pelo desempenho.

## Captura, avaliação e conformidade

Entrada, requisição/headers públicos, envelope HTTP ou fragmento, texto original,
modelo solicitado/reportado, tokens, horários, falhas e hashes são preservados.
O fechamento da captura precede a abertura da referência e a avaliação offline.
O adaptador reutiliza transporte, extração, comparação e Jaccard existentes;
não altera suas fórmulas. Inválidas/falhas permanecem sem métricas imputadas.
Modelo reportado divergente é conservado como desvio, sem trocar a identidade
do modelo solicitado. Células incluem documentação, modelo, mudança, condição,
nota, coorte, origem, fase e plano; nunca juntam lotes históricos ou demonstrações.

As contagens e a consistência são descrições pendentes de revisão. A pasta
`conformidade/` da avaliação contém fichas separadas, com responsável, data,
decisão e justificativa pendentes, ligadas aos hashes da captura e avaliação.
O envio, HTTP bem sucedido e o escore não aprovam conformidade. Decisões
humanas históricas permanecem em seus arquivos originais. Não se exclui
resposta por seu desempenho. Nenhuma decisão humana foi preenchida nesta integração.

Se a avaliação offline falhar, a captura continua preservada. Há método
`BlocoDocumental.avaliar` para avaliar uma captura fechada sem transporte;
uma avaliação parcial é conservada e exige diagnóstico em vez de sobrescrita.
Uma captura interrompida não é recriada como nova tentativa automaticamente.

## Verificação

```text
python -B preparar_documentacao_operacional_v2.py conferir
python apresentar.py verificar
python -B tests/validar_integracao_documental.py
node tests/test_interface_painel.cjs
```

O teste opcional `python -B tests/validar_documental_navegador.py` usa Chrome
local via CDP e o pacote Python `websocket-client` já instalado neste ambiente.
O painel em si usa somente a biblioteca padrão. O teste usa chave fictícia,
transporte substituto, bloqueio de rede externa e área identificada como
SINTÉTICA em `evidencias/spec004/integracao-documental-64-2026-11-22/`.
Esses registros não aparecem na coorte real. O teste não consulta o provedor.
Resultados efetivos e limitações estão em [VERIFICACAO](../apresentacao/VERIFICACAO.md).
