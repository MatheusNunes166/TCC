"""Controles positivos/negativos do parser nativo; sem selecionar custom provider."""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
import coletor_piloto as c
import inspecionar_config as native

for name, values in [
        ('custom-one', ['request_max_retries=1', 'stream_max_retries=1']),
        ('custom-string', ['request_max_retries="zero"'])]:
    overrides = ['model_providers.controle.name="Controle sem chamadas"']
    overrides += ['model_providers.controle.' + value for value in values]
    result = native.consultar(overrides)
    c.salvar_json(OUT / ('config-' + name + '.json'), result)
    print(name, result['retorno'], bool(result['resultado']), flush=True)
