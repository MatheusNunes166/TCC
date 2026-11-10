# Tabelas descritivas — conformidade pendente

Referencia candidata 0.3; 64 respostas reais, sem misturar piloto/controles. Todas as celulas: N=2 planejadas, C=2 concluidas, V=2 validas, I=0 invalidas, T=0 falhas. Nenhuma conformidade aprovada.

A/O/E = acertos (TP)/omissoes (FN)/excedentes (FP), somados nas duas respostas. P/R/F1 = medias por resposta valida, denominador V=2, usando as formulas existentes; nao sao razoes das somas de A/O/E. Exata = respostas iguais a referencia/V. J = Jaccard entre as duas repeticoes, um par por celula; nao mede acerto. Valores fracionarios sao exatos.

## gpt-6-sol

| Mudanca | Condicao | Formato V/C | RF A/O/E | RF P/R/F1 | RF exata | RF J (1 par) | Testes A/O/E | Testes P/R/F1 | Testes exata | Testes J (1 par) |
|---|---|---|---|---|---|---|---|---|---|---|
| MC-01 | D0 | 2/2 | 2/0/0 | 1 ; 1 ; 1 | 2/2 | 1 | 8/0/0 | 1 ; 1 ; 1 | 2/2 | 1 |
| MC-01 | D1 | 2/2 | 2/0/0 | 1 ; 1 ; 1 | 2/2 | 1 | 8/0/0 | 1 ; 1 ; 1 | 2/2 | 1 |
| MC-01 | E0 | 2/2 | 2/0/0 | 1 ; 1 ; 1 | 2/2 | 1 | 8/0/0 | 1 ; 1 ; 1 | 2/2 | 1 |
| MC-01 | E1 | 2/2 | 2/0/0 | 1 ; 1 ; 1 | 2/2 | 1 | 8/0/0 | 1 ; 1 ; 1 | 2/2 | 1 |
| MC-02 | D0 | 2/2 | 2/0/2 | 2/3 ; 1 ; 3/4 | 1/2 | 1/3 | 12/0/0 | 1 ; 1 ; 1 | 2/2 | 1 |
| MC-02 | D1 | 2/2 | 2/0/0 | 1 ; 1 ; 1 | 2/2 | 1 | 12/0/0 | 1 ; 1 ; 1 | 2/2 | 1 |
| MC-02 | E0 | 2/2 | 2/0/4 | 1/3 ; 1 ; 1/2 | 0/2 | 1 | 12/0/0 | 1 ; 1 ; 1 | 2/2 | 1 |
| MC-02 | E1 | 2/2 | 2/0/2 | 2/3 ; 1 ; 3/4 | 1/2 | 1/3 | 12/0/0 | 1 ; 1 ; 1 | 2/2 | 1 |
| MC-03 | D0 | 2/2 | 4/0/0 | 1 ; 1 ; 1 | 2/2 | 1 | 18/0/0 | 1 ; 1 ; 1 | 2/2 | 1 |
| MC-03 | D1 | 2/2 | 4/0/0 | 1 ; 1 ; 1 | 2/2 | 1 | 18/0/0 | 1 ; 1 ; 1 | 2/2 | 1 |
| MC-03 | E0 | 2/2 | 4/0/0 | 1 ; 1 ; 1 | 2/2 | 1 | 18/0/0 | 1 ; 1 ; 1 | 2/2 | 1 |
| MC-03 | E1 | 2/2 | 4/0/0 | 1 ; 1 ; 1 | 2/2 | 1 | 18/0/0 | 1 ; 1 ; 1 | 2/2 | 1 |
| MC-04-v2 | D0 | 2/2 | 4/0/0 | 1 ; 1 ; 1 | 2/2 | 1 | 16/0/0 | 1 ; 1 ; 1 | 2/2 | 1 |
| MC-04-v2 | D1 | 2/2 | 4/0/0 | 1 ; 1 ; 1 | 2/2 | 1 | 16/0/0 | 1 ; 1 ; 1 | 2/2 | 1 |
| MC-04-v2 | E0 | 2/2 | 4/0/0 | 1 ; 1 ; 1 | 2/2 | 1 | 16/0/0 | 1 ; 1 ; 1 | 2/2 | 1 |
| MC-04-v2 | E1 | 2/2 | 4/0/0 | 1 ; 1 ; 1 | 2/2 | 1 | 16/0/0 | 1 ; 1 ; 1 | 2/2 | 1 |

## gpt-6-astra

| Mudanca | Condicao | Formato V/C | RF A/O/E | RF P/R/F1 | RF exata | RF J (1 par) | Testes A/O/E | Testes P/R/F1 | Testes exata | Testes J (1 par) |
|---|---|---|---|---|---|---|---|---|---|---|
| MC-01 | D0 | 2/2 | 2/0/0 | 1 ; 1 ; 1 | 2/2 | 1 | 8/0/0 | 1 ; 1 ; 1 | 2/2 | 1 |
| MC-01 | D1 | 2/2 | 2/0/0 | 1 ; 1 ; 1 | 2/2 | 1 | 8/0/0 | 1 ; 1 ; 1 | 2/2 | 1 |
| MC-01 | E0 | 2/2 | 2/0/0 | 1 ; 1 ; 1 | 2/2 | 1 | 8/0/0 | 1 ; 1 ; 1 | 2/2 | 1 |
| MC-01 | E1 | 2/2 | 2/0/0 | 1 ; 1 ; 1 | 2/2 | 1 | 8/0/0 | 1 ; 1 ; 1 | 2/2 | 1 |
| MC-02 | D0 | 2/2 | 2/0/0 | 1 ; 1 ; 1 | 2/2 | 1 | 12/0/0 | 1 ; 1 ; 1 | 2/2 | 1 |
| MC-02 | D1 | 2/2 | 2/0/0 | 1 ; 1 ; 1 | 2/2 | 1 | 12/0/0 | 1 ; 1 ; 1 | 2/2 | 1 |
| MC-02 | E0 | 2/2 | 2/0/0 | 1 ; 1 ; 1 | 2/2 | 1 | 12/0/0 | 1 ; 1 ; 1 | 2/2 | 1 |
| MC-02 | E1 | 2/2 | 2/0/0 | 1 ; 1 ; 1 | 2/2 | 1 | 12/0/0 | 1 ; 1 ; 1 | 2/2 | 1 |
| MC-03 | D0 | 2/2 | 4/0/0 | 1 ; 1 ; 1 | 2/2 | 1 | 18/0/0 | 1 ; 1 ; 1 | 2/2 | 1 |
| MC-03 | D1 | 2/2 | 4/0/0 | 1 ; 1 ; 1 | 2/2 | 1 | 18/0/0 | 1 ; 1 ; 1 | 2/2 | 1 |
| MC-03 | E0 | 2/2 | 4/0/0 | 1 ; 1 ; 1 | 2/2 | 1 | 18/0/0 | 1 ; 1 ; 1 | 2/2 | 1 |
| MC-03 | E1 | 2/2 | 4/0/0 | 1 ; 1 ; 1 | 2/2 | 1 | 18/0/0 | 1 ; 1 ; 1 | 2/2 | 1 |
| MC-04-v2 | D0 | 2/2 | 4/0/0 | 1 ; 1 ; 1 | 2/2 | 1 | 16/0/0 | 1 ; 1 ; 1 | 2/2 | 1 |
| MC-04-v2 | D1 | 2/2 | 4/0/0 | 1 ; 1 ; 1 | 2/2 | 1 | 16/0/0 | 1 ; 1 ; 1 | 2/2 | 1 |
| MC-04-v2 | E0 | 2/2 | 4/0/0 | 1 ; 1 ; 1 | 2/2 | 1 | 16/0/0 | 1 ; 1 ; 1 | 2/2 | 1 |
| MC-04-v2 | E1 | 2/2 | 4/0/0 | 1 ; 1 ; 1 | 2/2 | 1 | 16/0/0 | 1 ; 1 ; 1 | 2/2 | 1 |

P/R/F1 estao na ordem precisao ; revocacao ; F1. Os IDs divergentes constam de `divergencias-ids.json`; os valores por resposta permanecem nas 64 avaliacoes individuais. O resumo controlado em `resumo/resumo.json` continua bloqueado, sem alteracao das conformidades originais.
