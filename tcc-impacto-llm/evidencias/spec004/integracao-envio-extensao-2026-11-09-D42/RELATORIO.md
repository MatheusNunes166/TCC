# Integração mínima do envio da extensão 0.3 — D-42

09/11/2026. Implementação autorizada pelo pesquisador, **sem chamadas reais, teste de conexão, coleta, commit ou push**. [D-42](../../../documentacao/decisoes.md) registra o pedido e a decisão de orçamento. A árvore já continha trabalho local não commitado de D-41; foi preservado e inventariado em [estado-inicial.json](estado-inicial.json), com cópias literais das fontes anteriores.

## Alteração e versão operacional

`extensao_exploratoria.py iniciar` exige `--enviar-real`, quantidade por invocação em `--limite` e usa `--continuar` para retomar. Delega ao mesmo `coletor_api.capturar`, com o conferidor da extensão e configuração selecionada por observação. O motor API v1.3-D42 mantém transporte, bytes, captura de falhas, fechamento e ausência de retries automáticos. A retomada confere os arquivos/identidade/configuração/origem/fase e não reenvia conclusões; falha ambígua, desvio ou alteração de fonte/plano bloqueiam a continuação automática.

Registros reais têm `origem=real`, `fase=exploratoria`, `etapa=extensao-0.3-D41`, integração D-42, ordem/bloco, configuração e hashes do plano/referência. A etapa D-41 identifica o desenho original; a integração D-42 identifica a nova capacidade de envio. Controles continuam sintéticos. A fase exploratória foi aceita na avaliação em lote e na revisão de conformidade, que reutilizam o avaliador e o resumo existentes em comandos separados. Nenhum gabarito é aberto na captura; pendências de conformidade continuam bloqueando o resumo controlado.

Novo [plano 003](../../../captura/extensao-20261109-003/plano.json), gerado **pelo preparador** a partir do 002, sem editar arquivos anteriores:

```powershell
python -B "D:\TCC-Projeto\TCC\tcc-impacto-llm\extensao_exploratoria.py" preparar --origem "D:\TCC-Projeto\TCC\tcc-impacto-llm\captura\extensao-20261109-002\plano.json" --saida "D:\TCC-Projeto\TCC\tcc-impacto-llm\captura\extensao-20261109-003"
```

Esse comando **já foi executado offline**; seu destino existe e não deve ser sobrescrito. `ordem.json` foi copiado literalmente, inclusive Python/algoritmo/semente anteriores. Permanecem os 64 IDs/itens, ordem, dois blocos, repetições, os mesmos 16 textos nas 32 preparações e referência 0.3 (`94b6315b935d9817dd833567a0b107a90e88d9be850e93c747e03337450eebc9`). Sol e Astra continuam em medium, limite comum 4096, timeout 120 s, mesmo envio textual sem ferramentas/histórico. As observações continuam `PLANEJADA_NAO_EXECUTADA`; nenhuma chamada foi realizada nesta implementação.

Identidades novas: `ext-api-sol-c876e81f01df3a17` e `ext-api-astra-9d2e238e64485a09`. Fontes, configurações, manifestos/preparações recebem hashes próprios; os hashes dos textos e da ordem são iguais aos do 002. O plano anterior literal está em `plano-anterior.json`. O conferidor novo recusa planos anteriores sem regravar seus hashes.

Arquivos desta integração: `extensao_exploratoria.py`, `coletor_api.py`, `revisao_conformidade.py`, ajuste do teste de flag em `tests/test_extensao_exploratoria.py`, novos `tests/test_envio_extensao.py`, plano/preparações 003, evidências desta pasta, `.gitattributes`, estado, README, arquitetura, decisões e operação API. **`coletor_piloto.py` e sua trava Codex CLI ficaram literalmente intactos**, assim como núcleo, variantes, catálogo/referência, notas e textos experimentais. A adaptação do lote exploratório fica na rota API, conservando o auxiliar histórico.

## Orçamento e comandos para o pesquisador

**USD 2 para planejamento da rodada inteira**, com risco de ultrapassagem explicitamente aceito pelo pesquisador. O valor aparece nas duas configurações como metadado comum; não são dois orçamentos a somar. Não se implementou contador, parada monetária ou garantia de teto; `--limite` conta novas tentativas por invocação. Não foi consultado ou presumido saldo ou disponibilidade. A chave futura vem de `OPENAI_API_KEY`, sem gravar seu valor nas capturas.

Primeira observação somente, `EXT03-MC-04-v2-E1-SOL-R01` (Sol/medium):

```powershell
python -B "D:\TCC-Projeto\TCC\tcc-impacto-llm\extensao_exploratoria.py" iniciar --plano "D:\TCC-Projeto\TCC\tcc-impacto-llm\captura\extensao-20261109-003\plano.json" --lote "D:\TCC-Projeto\TCC\tcc-impacto-llm\captura\extensao-real-0.3-001" --limite 1 --enviar-real
```

Continuação para **uma próxima observação pendente**, sem reenviar a primeira concluída:

```powershell
python -B "D:\TCC-Projeto\TCC\tcc-impacto-llm\extensao_exploratoria.py" iniciar --plano "D:\TCC-Projeto\TCC\tcc-impacto-llm\captura\extensao-20261109-003\plano.json" --lote "D:\TCC-Projeto\TCC\tcc-impacto-llm\captura\extensao-real-0.3-001" --limite 1 --continuar --enviar-real
```

Esses dois comandos **não foram executados**. O lote indicado ainda não foi criado. A continuação exige o mesmo plano/lote; seu limite pode ser escolhido por invocação sem mudar o desenho. Avaliação e revisão de conformidade permanecem separadas, conforme [operação API](../../../documentacao/operacao-api.md#envio-da-extensão-03--d-42). A referência continua candidata; a habilitação de engenharia não atribui aprovação científica externa.

## Evidências offline

Os [sete testes novos](../../../tests/test_envio_extensao.py) passaram na primeira execução: 64 envios reais **simulados**, seleção de ambos os modelos por posição, pausa/retomada sem duplicação, bloqueio sem flag, limites inválidos, recusa do plano anterior e da mistura sintético/real, falhas/modelo divergente sem retry/fallback, avaliação separada e modelo pendente de revisão. Todas as capturas simuladas existiram somente em diretórios temporários; não são dados de pesquisa. HTTP foi substituído e a credencial era fictícia.

[Regressões afetadas e resultado final](verificacao-001/resultado.json), [log](verificacao-001/unittest.txt), [receita offline](verificar_offline.py). O audit hook bloqueia conexões/DNS; não usa chave real. A conferência compara os 64 itens/ordem/payloads e referência entre 002/003 e todos os arquivos anteriores inventariados, usando as fontes anteriores guardadas para os arquivos modificados. `git diff --check` verifica as alterações sem commit/stage/push. A simulação do plano 003 e a ajuda do comando `iniciar` também foram exercitadas sem rede.

**Resultado real:** Python 3.13.3, **52 métodos aprovados, zero falhas, erros ou ignorados**, em 229,093 s. Incluem os sete novos, os doze da extensão anterior e regressões API, transporte, revisão e trava CLI. **8.543 arquivos anteriores conferidos sem divergências**, incluindo os originais arquivados das quatro fontes/testes atualizados; coletor CLI intacto. Os controles também mantiveram as 75 comparações locais da bancada e a interpretação anterior dos 16 textos do piloto. Os 64 envios simulados foram retomados sem duplicação e avaliados separadamente, com revisão ainda pendente; o lote real de pesquisa não existe nesta entrega.

[Conferência final de bytes e links](conferencia-final.json). Hash do plano 003: `e00fd77c23e3b018cb3781e5ebee9b0d1b765e36e7c53fdf9eba8588e45c2e3e`. Não há novo critério científico, aprovação externa, controle monetário automático ou requisito de confirmação adicional introduzido por esta integração.
