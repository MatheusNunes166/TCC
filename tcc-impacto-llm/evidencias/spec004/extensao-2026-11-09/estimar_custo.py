"""Estima cenarios offline a partir dos bytes dos payloads; nao conta tokens reais.

Precos de paginas publicas oficiais consultadas em 09/11/2026 (Standard,
contexto curto). Nenhuma API, tokenizer remoto ou consulta de saldo.
"""
import argparse
import json
import math
from pathlib import Path


def estimar(plano):
    plan = json.loads(plano.read_bytes())
    rows = plan['observacoes']
    prices = {'gpt-6-sol': {'entrada': 2, 'saida': 10},
              'gpt-6-astra': {'entrada': 10, 'saida': 50}}
    scenarios = []
    # Hipoteses de tokenizacao e saida, nao medições do modelo.
    for name, divisor, overhead, reasoning, final in (
        ('central_1024_saida', 4, 128, 768, 256),
        ('limite_saida_4096', 4, 128, 3840, 256),
        ('entrada_mais_densa_e_limite_saida', 2, 128, 3840, 256),
        ('margem_um_token_por_byte', 1, 256, 3840, 256)):
        models = {}
        for model, price in prices.items():
            selected = [r for r in rows if r['modelo'] == model]
            sizes = [len((plano.parent / r['preparacao']).parent.joinpath('payload.txt').read_bytes()) for r in selected]
            inputs = sum(math.ceil(n / divisor) + overhead for n in sizes)
            output = len(selected) * (reasoning + final)
            models[model] = {'observacoes': len(selected), 'payload_bytes_total': sum(sizes),
                'tokens_entrada_estimados': inputs, 'tokens_saida_cenario': output,
                'raciocinio_por_chamada_hipotetico': reasoning, 'final_por_chamada_hipotetico': final,
                'usd': round((inputs * price['entrada'] + output * price['saida']) / 1_000_000, 6)}
        scenarios.append({'nome': name, 'bytes_por_token_hipotetico': divisor,
                          'overhead_hipotetico_tokens_por_chamada': overhead,
                          'modelos': models, 'total_usd': round(sum(m['usd'] for m in models.values()), 6)})
    return {'data_consulta': '2026-11-09', 'moeda': 'USD',
        'fontes_publicas': ['https://developers.openai.com/api/docs/models/gpt-6-sol',
                           'https://developers.openai.com/api/docs/models/gpt-6-astra',
                           'https://developers.openai.com/api/docs/pricing',
                           'https://developers.openai.com/api/docs/guides/reasoning'],
        'precos_por_milhao': prices, 'modalidade': 'Standard; contexto curto; sem descontos de cache',
        'limite_saida': 4096, 'inclui_raciocinio_e_final': True,
        'tokenizacao': 'heuristica explicita por bytes UTF-8, sem tokenizer instalado; nao e contagem exata',
        'hipoteses': '64 tentativas sem retries; sem ferramentas; sem taxas regionais/impostos; sem cache writes solicitados; '
                    'um prompt textual independente. Nao pressupoe saldo anterior ou disponibilidade na conta. '
                    'A API nao recebe service_tier explicito: confirmar Standard na conta antes de uso real.',
        'orcamento_declarado_usd': None, 'teto_cobranca_garantido': False,
        'interrupcao': 'envio real bloqueado nesta preparacao; --limite restringe tentativas, nao dolares; timeout nao cancela faturamento remoto',
        'cenarios': scenarios}


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--plano', type=Path, required=True)
    p.add_argument('--saida', type=Path, required=True)
    args = p.parse_args()
    with args.saida.open('xb') as f:
        f.write((json.dumps(estimar(args.plano), ensure_ascii=False, indent=2) + '\n').encode())
