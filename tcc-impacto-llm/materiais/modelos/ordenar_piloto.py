"""Gera somente uma proposta de ordem local; nao chama modelos nem aprova piloto."""
import argparse
import json
from pathlib import Path
import random
import sys


def ordenar(plano, semente):
    # Copia profunda: nao modifica o modelo de planejamento.
    plano = json.loads(json.dumps(plano))
    rows = plano['observacoes']
    expected = {(m, c, r) for m in ('MC-01', 'MC-03')
                for c in ('D0', 'D1', 'E0', 'E1') for r in (1, 2)}
    if len(rows) != 16 or {(r['mudanca'], r['condicao'], r['repeticao']) for r in rows} != expected:
        raise ValueError('plano deve conter exatamente as 16 combinacoes propostas')
    if any(r['bloco'] != r['repeticao'] or r['ordem'] is not None or
           r['status'] != 'PLANEJADA_NAO_EXECUTADA' for r in rows):
        raise ValueError('usar plano canonico nao executado, com ordem nula')
    rng = random.Random(semente)
    ordered = []
    for block in (1, 2):
        group = sorted((r for r in rows if r['bloco'] == block),
                       key=lambda r: (r['mudanca'], r['condicao']))
        rng.shuffle(group)
        for row in group:
            row['ordem'] = len(ordered) + 1
            ordered.append(row)
    plano.update(semente_ordem=semente, python_ordem=sys.version,
                 observacoes=ordered, ordem_aprovada=False)
    return plano


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--plano', type=Path, default=Path(__file__).with_name('plano_piloto.json'))
    parser.add_argument('--semente', type=int, required=True)
    parser.add_argument('--saida', type=Path, required=True)
    args = parser.parse_args()
    result = ordenar(json.loads(args.plano.read_text(encoding='utf-8')), args.semente)
    args.saida.parent.mkdir(parents=True, exist_ok=True)
    with args.saida.open('x', encoding='utf-8', newline='\n') as stream:
        json.dump(result, stream, ensure_ascii=False, indent=2)
        stream.write('\n')
    print('16 posicoes propostas; nenhuma chamada ou aprovacao.')


if __name__ == '__main__':
    main()
