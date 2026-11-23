"""Preparação documental de 64 posições. Antecedente v1 permanece literal."""
from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path
import random

import preparar_documentacao_operacional as anterior

ROOT = anterior.ROOT
PASTA = 'captura/documentacao-operacional-0.3-002'
ANTECEDENTE = 'captura/documentacao-operacional-0.3-001'
VERSAO = 'documentacao-operacional-0.3-v2-64'
CONDICOES = ('D0', 'D1', 'E0', 'E1')
MUDANCAS = anterior.MUDANCAS
MODELOS = anterior.MODELOS
DOCUMENTACOES = anterior.DOCUMENTACOES
CONFIGURACAO = {'esforco_solicitado': 'medium', 'max_output_tokens': 4096,
    'timeout_segundos': 120, 'endpoint': 'https://api.openai.com/v1/responses',
    'tools': [], 'tool_choice': 'none', 'store': False, 'stream': False,
    'retries_automaticos_cliente': 0, 'orcamento_usd': None}
sha, serial, ler, salvar = anterior.sha, anterior.serial, anterior.ler, anterior.salvar


def montar(root=ROOT):
    root = Path(root)
    profiles = anterior.perfis_preservados(root)
    payloads, sources, documents = {}, {}, None
    for change, condition in itertools.product(MUDANCAS, CONDICOES):
        note = 'sem' if condition.endswith('0') else 'original'
        profile = profiles[f'{change}:{condition}:{note}']
        original = profile['payload']
        modified, docs = anterior.operacionalizar(original)
        if documents is not None and documents != docs:
            raise ValueError('Documentos diferentes entre perfis.')
        documents = docs
        for level, raw in zip(DOCUMENTACOES, (original, modified)):
            payloads[f'{change}-{condition}-{level}'] = raw
        sources[f'{change}:{condition}'] = {
            'requisicao_origem': profile['origem'].relative_to(root).as_posix(),
            'requisicao_sha256': profile['origem_sha256'],
            'payload_origem_sha256': profile['payload_sha256'],
            'referencia_sha256': profile['referencia_sha256']}
    # Nota original única, sem generalização incorreta de D0 para E0.
    for change, level in itertools.product(MUDANCAS, DOCUMENTACOES):
        blocks = {c: dict(anterior.BLOCOS.findall(payloads[f'{change}-{c}-{level}'].decode()))
                  for c in CONDICOES}
        if any('notas' in blocks[c] for c in ('D0', 'E0')):
            raise ValueError('Condição sem notas contém notas.')
        if blocks['D1']['notas'] != blocks['E1']['notas']:
            raise ValueError('D1 e E1 devem usar a mesma nota original.')
        for direct, structured in (('D0', 'E0'), ('D1', 'E1')):
            if {k: v for k, v in blocks[direct].items() if k != 'pedido'} != {
                    k: v for k, v in blocks[structured].items() if k != 'pedido'}:
                raise ValueError('Estrutura alterou blocos além do pedido.')
    return payloads, sources, documents


def plano(payloads, sources, root=ROOT):
    root = Path(root)
    rng, rows = random.Random(anterior.SEMENTE), []
    for repetition in (1, 2):
        cells = list(itertools.product(MUDANCAS, MODELOS, CONDICOES, DOCUMENTACOES))
        rng.shuffle(cells)
        for change, model, condition, level in cells:
            name = f'{change}-{condition}-{level}'
            rows.append({'observacao_id': f'DOCOP64-{name}-{model[6:].upper()}-R{repetition:02}',
                'ordem': len(rows) + 1, 'bloco': repetition, 'repeticao': repetition,
                'mudanca': change, 'modelo_solicitado': model, 'condicao': condition,
                'documentacao_id': level, 'nota_id': 'sem' if condition.endswith('0') else 'original',
                'payload': f'payloads/{name}.txt', 'payload_sha256': sha(payloads[name]),
                'status': 'PLANEJADA_NAO_EXECUTADA', 'conformidade_protocolo': 'pendente'})
    return {'versao': VERSAO, 'coorte': 'documentacao_operacional_64',
        'fase': 'exploratoria_documental', 'quantidade_planejada': 64, 'celulas': 32,
        'repeticoes_por_celula': 2, 'blocos': 2, 'posicoes_por_bloco': 32,
        'payloads_unicos': 16, 'semente': anterior.SEMENTE,
        'algoritmo': 'random.Random(20261122).shuffle por bloco; produto mudança/modelo/condição/documentação',
        'decisao': {'id': 'D-54', 'responsavel': 'Matheus Henrique Braun Nunes',
            'data': '2026-11-22', 'evidencia': 'Solicitação atual: quero incluir D0, D1, E0 e E1; 64 observações.',
            'aprovacao_cientifica_orientador': False},
        'status': 'PREPARADO_OFFLINE_NAO_EXECUTADO', 'envio': 'SOMENTE_CLIQUE_EXPLICITO_NA_INTERFACE',
        'antecedente': {'pasta': ANTECEDENTE, 'estado': 'PREPARADO_NAO_EXECUTADO',
            'plano_sha256': sha((root / ANTECEDENTE / 'plano.json').read_bytes()),
            'manifesto_sha256': sha((root / ANTECEDENTE / 'manifesto.json').read_bytes()),
            'produtor_sha256': sha(Path(anterior.__file__).read_bytes())},
        'catalogo': '0.3 INTEGRAL: quinze casos e seis colunas',
        'tratamento': 'Distribuição, redação, explicações e extensão documental em conjunto; sem garantia de maior dificuldade.',
        'selecao_tarefas': 'Pós-exploratória, após conhecer resultados anteriores; não amostra aleatória.',
        'configuracao': CONFIGURACAO, 'fontes': sources, 'observacoes': rows}


def arquivos_esperados(root=ROOT):
    anterior.conferir(Path(root) / ANTECEDENTE, root)
    payloads, sources, docs = montar(root)
    files = {f'payloads/{name}.txt': raw for name, raw in payloads.items()}
    files.update({f'documentos-operacionais/{name}': text.encode() for name, text in docs.items()})
    files['plano.json'] = serial(plano(payloads, sources, root))
    files['diferencas.json'] = serial([{'perfil': name, 'consolidada_sha256': sha(raw),
        'operacional_sha256': sha(payloads[name.replace('CONSOLIDADA', 'OPERACIONAL')]),
        'bytes_adicionais': len(payloads[name.replace('CONSOLIDADA', 'OPERACIONAL')]) - len(raw),
        'caracteres_adicionais': len(payloads[name.replace('CONSOLIDADA', 'OPERACIONAL')].decode()) - len(raw.decode()),
        'bloco_substituido': 'requisitos-baseline', 'demais_blocos': 'LITERAIS'}
        for name, raw in payloads.items() if name.endswith('CONSOLIDADA')])
    return files


def manifesto(files):
    return {'versao': VERSAO, 'arquivos': {n: sha(b) for n, b in files.items()},
        'preparador_sha256': sha(Path(__file__).read_bytes()), 'chamadas_na_preparacao': 0}


def preparar(pasta, root=ROOT):
    folder = anterior.sem_links(Path(pasta))
    if folder.exists():
        raise ValueError('Destino existente: preservar e usar versão nova.')
    files = arquivos_esperados(root)
    for name, raw in files.items():
        salvar(folder / name, raw)
    salvar(folder / 'manifesto.json', serial(manifesto(files)))
    return conferir(folder, root)


def conferir(pasta, root=ROOT):
    folder, files = anterior.sem_links(Path(pasta)), arquivos_esperados(root)
    if ler(folder / 'manifesto.json') != manifesto(files):
        raise ValueError('Manifesto ou produtor divergente.')
    actual = {p.relative_to(folder).as_posix() for p in folder.rglob('*') if p.is_file()}
    if actual != set(files) | {'manifesto.json'}:
        raise ValueError('Inventário divergente.')
    for name, raw in files.items():
        if anterior.sem_links(folder / name).read_bytes() != raw:
            raise ValueError('Bytes divergentes: ' + name)
    return {'status': 'OK_PREPARACAO_OFFLINE', 'payloads': 16, 'posicoes': 64,
        'celulas': 32, 'N': 2, 'blocos': [32, 32], 'chamadas_na_preparacao': 0}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('acao', choices=('preparar', 'conferir'))
    parser.add_argument('--pasta', default=PASTA)
    args = parser.parse_args()
    print(json.dumps((preparar if args.acao == 'preparar' else conferir)(args.pasta), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
