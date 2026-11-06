# Avaliação local futura — somente exploratória

05/11/2026. **Não executada nesta preparação: ainda não há respostas reais.** Referência candidata 0.2 e política de pontuação `ids-proposta-004-v2` continuam provisórias, com revisão científica pendente. Não enviar a referência ao modelo.

## Limitação concreta da CLI existente

`python -B avaliacao_ids.py avaliar --preparacao ... --tentativa ... --referencia ... --saida ...` é a CLI existente com persistência completa, mas seu contrato implementado exige `origem=sintetica`, `modelo_reportado=null` e `repeticao_sintetica`. Ela não aceita registros reais de modelo. **Não usar essa CLI para o ensaio, não falsificar origem e não remover o modelo para contornar a validação.** `resumir` também pertence a esse fluxo sintético; não agregar as respostas exploratórias por ele.

A função já existente `avaliacao_ids.avaliar_resposta` compara os bytes com a referência sem impor origem sintética. Pode ser usada localmente pelo comando abaixo, com proveniência exploratória explícita e preservação manual dos originais. Isso reutiliza parser/comparador, sem alterar módulos ou criar outra Spec/infraestrutura; não amplia a CLI de importação nem constitui liberação de coleta. Não haverá resumo de Jaccard: uma observação por célula é insuficiente.

## Comando para uma resposta registrada

Da raiz `tcc-impacto-llm`, somente após salvar a resposta original e preencher `registro.json` com hashes/dados reais. Trocar `cond = 'D0'` por D1, E0 ou E1 para os demais registros. O comando usa a função existente e cria uma saída **nova**, recusando sobrescrita. Não executá-lo sobre as fichas planejadas.

```powershell
@'
import json, hashlib
from pathlib import Path
from datetime import datetime, timezone
from avaliacao_ids import avaliar_resposta, relativo, caminho_seguro, json_estrito
cond = 'D0'
root = caminho_seguro(Path.cwd())
trial = caminho_seguro(root/'evidencias/spec004/exploratorio-2026-11-05-mc04-001')
sha = lambda data: hashlib.sha256(data).hexdigest()
regpath = trial/'registros'/cond/'registro.json'
regraw = regpath.read_bytes(); reg = json_estrito(regraw)
assert reg['status'] == 'REGISTRADA' and reg['fase'] == 'exploratorio'
assert reg['origem'] == 'llm_exploratoria' and reg['condicao'] == cond
assert reg['mudanca'] == 'MC-04-v2' and reg['repeticao'] == 1
assert reg['incluido_coleta_principal'] is False and reg['incluido_piloto'] is False
assert reg['ferramenta'] and reg['modelo_reportado'] and reg['configuracao_coleta_id']
assert reg['data_inicio_utc'] and reg['data_fim_utc']
prepraw = relativo(trial, reg['preparacao_arquivo']).read_bytes()
prep = json_estrito(prepraw)
assert sha(prepraw) == reg['preparacao_sha256'] and prep['preparacao_id'] == reg['preparacao_id']
payload = relativo(trial, reg['payload_arquivo']).read_bytes()
sent = relativo(trial, reg['conteudo_enviado_arquivo']).read_bytes()
assert sha(payload) == prep['payload_sha256'] == reg['payload_sha256']
assert sha(sent) == reg['conteudo_enviado_sha256'] == reg['payload_sha256']
state = reg['status_tecnico']; assert state in ('concluida', 'falha_tecnica')
raw = None
if reg['resposta_bruta_arquivo'] is not None:
    raw = relativo(trial, reg['resposta_bruta_arquivo']).read_bytes()
    assert sha(raw) == reg['resposta_sha256'] and len(raw) == reg['resposta_bytes']
if state == 'concluida':
    assert raw is not None and reg['fragmento_arquivo'] is None
else:
    assert reg['causa_falha_tecnica']
versions = json_estrito((trial/'versoes.json').read_bytes())
refraw = (root/versions['referencia']['arquivo']).read_bytes()
assert sha(refraw) == versions['referencia']['sha256']
assert sha((root/'avaliacao_ids.py').read_bytes()) == versions['avaliador']['sha256']
result = avaliar_resposta(raw, json_estrito(refraw), 'MC-04-v2', state)
output = {'fase':'exploratorio', 'origem':'llm_exploratoria',
          'incluido_coleta_principal':False, 'incluido_piloto':False,
          'run_id':reg['run_id'], 'configuracao_coleta_id':reg['configuracao_coleta_id'],
          'instante_avaliacao_utc':datetime.now(timezone.utc).isoformat(),
          'registro_sha256':sha(regraw), 'payload_sha256':sha(payload),
          'conteudo_enviado_sha256':sha(sent), 'resposta_sha256':reg['resposta_sha256'],
          'causa_tecnica':reg['causa_falha_tecnica'],
          'versoes':versions, 'resultado':result}
with (regpath.parent/'avaliacao-exploratoria-001.json').open('x',encoding='utf-8',newline='\n') as stream:
    json.dump(output,stream,ensure_ascii=True,indent=2);stream.write('\n')
print(result['status_avaliacao'])
'@ | python -X utf8 -B -
```

Se não houve envio por falha anterior à transmissão, preservar o registro/erro e indicar avaliação não aplicável; não fabricar `conteudo_enviado` para passar nas conferências. Se enviado difere do preparado, registrar desvio e interromper essa avaliação vinculada, mantendo ambos os originais. Qualquer nova avaliação exige outro nome/ID e vínculo explícito à anterior, sem reescrever sua saída.

Esse comando não transporta nem envia conteúdo. Não substitui a auditoria de captura e não possui o fluxo completo de importação/fechamento da CLI sintética. O registro, os arquivos brutos e a configuração real devem permanecer juntos, separados da coleta principal. Futuro suporte de importação real pela CLI exigiria decisão própria; não foi implementado aqui.

## Consultar acertos, omissões e seleções excedentes

Após a avaliação local, da raiz do repositório:

```powershell
$r = Get-Content -Raw -Encoding utf8 evidencias/spec004/exploratorio-2026-11-05-mc04-001/registros/D0/avaliacao-exploratoria-001.json | ConvertFrom-Json
$r.resultado | Select-Object status_avaliacao, json_sintatico, formato_contrato, causa
$r.resultado.requisitos | Format-List acertos, omissoes, excedentes, desconhecidos, duplicatas, TP, FP, FN
$r.resultado.testes | Format-List acertos, omissoes, excedentes, desconhecidos, duplicatas, TP, FP, FN
```

Repetir por condição, sem combinar RFs e testes. `excedentes` são seleções além do conjunto esperado; `desconhecidos` são IDs inexistentes e já pertencem aos excedentes, sem dupla contagem. Duplicatas exatas contam uma vez e permanecem relatadas. Listas vazias válidas geram omissões; resposta inválida ou falha técnica não gera conjuntos/escores observados (campos nulos). Não substituir nulos por seleção vazia ou por zero.

P/R/F1 e outras medidas aparecem em `metricas_propostas`, ainda candidatas. A referência não é ajustada às respostas, e a concordância com ela não certifica adequação científica ou detecção de defeitos. Nenhuma das quatro respostas futuras deve entrar automaticamente no piloto ou na coleta principal.
