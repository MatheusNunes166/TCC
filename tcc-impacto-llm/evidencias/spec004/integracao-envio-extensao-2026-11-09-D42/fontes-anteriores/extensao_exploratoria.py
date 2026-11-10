"""D-41: preparacao, simulacao e controles locais da extensao 0.3. Sem envio real.

Reutiliza montador, motor de captura API, fechamento e retomada existentes.
Nao importa avaliador, referencia privada ou chave no caminho de preparacao/captura.
"""
import argparse
import json
from pathlib import Path
import random
import sys
import uuid

import coletor_api as api
import fontes_autorizadas as fontes
import montagem_entradas as montagem

ETAPA = 'extensao-0.3-D41'
MODELOS = ('gpt-6-sol', 'gpt-6-astra')
SEMENTE = 20261109
RAIZ = Path(__file__).resolve().parent
CATALOGO = 'materiais/modelos/catalogo_baseline_0.3.json'
FONTES = ('coletor_api.py', 'coletor_piloto.py', 'montagem_entradas.py',
          'fontes_autorizadas.py', 'extensao_exploratoria.py')


def configuracao(modelo, referencia_sha256):
    if modelo not in MODELOS:
        raise ValueError('modelo desconhecido; sem substituicao ou fallback')
    c = {'modelo_solicitado': modelo, 'esforco_solicitado': 'medium',
         'interface': 'Responses API HTTP direto', 'endpoint': api.ENDPOINT,
         'max_output_tokens': 4096, 'timeout_segundos': 120,
         'tools': [], 'tool_choice': 'none', 'store': False, 'stream': False,
         'retries_automaticos_cliente': 0, 'catalogo_versao': '0.3',
         'referencia_sha256': referencia_sha256, 'etapa': ETAPA,
         'orcamento_declarado_usd': None,
         'limite_orcamento': 'pendente de declaracao; nenhum teto monetario imposto pelo script',
         'limite_saida': '4096 inclui raciocinio e resposta final; proposta comum a ambos os modelos'}
    c['id'] = 'ext-api-' + modelo.removeprefix('gpt-6-') + '-' + api.sha(api.bytes_json(c))[:16]
    return c


def ordem():
    rng = random.Random(SEMENTE)
    rows = []
    for block in (1, 2):
        cells = [(m, c, model) for m in montagem.MUDANCAS
                 for c in montagem.CONDICOES for model in MODELOS]
        rng.shuffle(cells)
        for m, c, model in cells:
            rows.append({'ordem': len(rows) + 1, 'bloco': block, 'repeticao': block,
                         'mudanca': m, 'condicao': c, 'modelo': model,
                         'observacao_id': f'EXT03-{m}-{c}-{model.removeprefix("gpt-6-").upper()}-R{block:02}'})
    return rows


def catalogo_texto(catalogo):
    lines = ['| ID | Estado | Papéis | Operação | Decisão esperada | Motivo esperado |\n',
             '| --- | --- | --- | --- | --- | --- |\n']
    for c in catalogo:
        lines.append('| ' + ' | '.join([c['id'], c['estado'], ' + '.join(c['papeis']),
                     c['operacao'], c['esperado']['decisao'], c['esperado']['motivo']]) + ' |\n')
    return ''.join(lines).encode()


def preparar(saida):
    out = api.base.protegida(saida, 'captura')
    if out.exists():
        raise ValueError('saida existente; preservar tentativa anterior')
    public = api.base.ler(RAIZ / CATALOGO)
    if public['versao'] != '0.3' or [c['id'] for c in public['catalogo']] != [f'T{i:02}' for i in range(1, 16)]:
        raise ValueError('catalogo publico nao e 0.3 completo')
    catalog = catalogo_texto(public['catalogo'])
    if catalog != (RAIZ / 'materiais/modelos/catalogo_baseline_0.3.md').read_bytes():
        raise ValueError('catalogos JSON/MD divergentes')
    refhash = public['referencia_sha256']
    configs = [configuracao(model, refhash) for model in MODELOS]
    out.mkdir(parents=True)
    source_hashes = {}
    for relative in (*fontes.FONTES, CATALOGO, 'materiais/modelos/catalogo_baseline_0.3.md'):
        raw = (RAIZ / relative).read_bytes()
        api.salvar(out / 'fontes-originais' / relative, raw)
        source_hashes[relative] = api.sha(raw)
    order = ordem()
    order_meta = {'semente_local': SEMENTE, 'algoritmo': 'random.Random(20261109).shuffle; um gerador, dois blocos sequenciais',
                  'enumeracao': 'mudancas MC-01,MC-02,MC-03,MC-04-v2; condicoes D0,D1,E0,E1; modelos sol,astra',
                  'python': sys.version, 'observacoes': order}
    api.salvar_json(out / 'ordem.json', order_meta)
    prepared = {}
    for config in configs:
        for change in montagem.MUDANCAS:
            for cond in montagem.CONDICOES:
                docs, provenance = fontes.reunir_fontes(RAIZ, change, cond)
                docs['catalogo-baseline.md'] = catalog
                key = f'{config["modelo_solicitado"]}/{change}-{cond}'
                package = out / 'pacotes' / key
                names = list(montagem.NOMES)
                if cond in ('D1', 'E1'):
                    names.insert(5, 'notas.md')
                entries = []
                for name in names:
                    blob = fontes.normalizar_documento(docs[name])
                    api.salvar(package / name, blob)
                    entries.append({'papel': name.split('.')[0], 'arquivo': name,
                                    'versao': 'catalogo-0.3' if name == 'catalogo-baseline.md' else 'recorte-D36-lf-2026-11-06',
                                    'sha256': api.sha(blob), 'tamanho_bytes': len(blob),
                                    'revisao_conteudo': {'estado': 'conferido_tecnicamente',
                                    'responsavel': 'assistente; preparacao autorizada D-41', 'data': '2026-11-09',
                                    'alcance': 'catalogo ampliado conforme contratos; demais textos preservados; revisao cientifica pendente'}})
                manifest = {'versao_contrato': montagem.CONTRATO, 'pacote_id': 'EXT03-' + key.replace('/', '-'),
                            'versao_pacote': ETAPA, 'politica_bytes': fontes.POLITICA_BYTES,
                            'configuracao_id': config['id'], 'mudanca': change, 'condicao': cond,
                            'catalogo_versao': '0.3', 'referencia_versao': '0.3', 'referencia_sha256': refhash,
                            'status': 'RASCUNHO_PREPARACAO', 'liberado_para_pesquisa': False,
                            'documentos': entries,
                            'status_notas': 'RASCUNHO_NAO_REVISADO' if cond in ('D1', 'E1') else 'ausentes',
                            'versao_notas': '0.2-local' if cond in ('D1', 'E1') else None}
                api.salvar_json(package / 'manifesto.json', manifest)
                auth = out / 'autorizacoes' / (key + '.json')
                api.salvar_json(auth, {'versao': 'autorizacao-textual-v1', 'status': 'CONFERIDO_TECNICAMENTE_RASCUNHO',
                    'manifesto_sha256': api.sha((package / 'manifesto.json').read_bytes()),
                    'documentos': [{'arquivo': e['arquivo'], 'sha256': e['sha256']} for e in entries],
                    'fontes': provenance, 'catalogo_publico_sha256': source_hashes[CATALOGO],
                    'revisao_cientifica': 'pendente do pesquisador; sem aprovacao externa'})
                dest = out / 'preparados' / key
                prep = montagem.preparar(package, package / 'manifesto.json', dest, auth)
                prep.update({k: manifest[k] for k in ('catalogo_versao', 'referencia_versao', 'referencia_sha256')})
                # Somente o novo registro, ainda nao referenciado por hash. Montador historico intacto.
                (dest / 'preparacao.json').write_bytes(api.bytes_json(prep))
                prepared[(change, cond, config['modelo_solicitado'])] = dest / 'preparacao.json'
    rows = []
    for r in order:
        p = prepared[(r['mudanca'], r['condicao'], r['modelo'])]
        prep = api.base.conferir_preparacao(p)
        rows.append({**r, 'configuracao_id': prep['configuracao_id'],
                     'preparacao': p.relative_to(out).as_posix(), 'preparacao_sha256': api.sha(p.read_bytes()),
                     'payload_sha256': prep['payload_sha256'], 'status': 'PLANEJADA_NAO_EXECUTADA',
                     'origem': 'real', 'fase': 'exploratoria'})
    plan = {'etapa': ETAPA, 'status': 'PREPARADO_NAO_ENVIADO', 'catalogo_versao': '0.3',
            'referencia_versao': '0.3', 'referencia_sha256': refhash,
            'configuracoes': {c['id']: c for c in configs}, 'observacoes': rows,
            'fontes_sha256': {f: api.sha((RAIZ / f).read_bytes()) for f in FONTES},
            'fontes_editoriais_sha256': source_hashes,
            'ordem_sha256': api.sha((out / 'ordem.json').read_bytes()),
            'orcamento_declarado_usd': None, 'envio_autorizado': False,
            'restricao': 'preparacao offline; revisao e autorizacao especifica antes de qualquer chamada'}
    api.salvar_json(out / 'plano.json', plan)
    conferir(out / 'plano.json')
    return out / 'plano.json'


def conferir(path):
    path = montagem.sem_links(path)
    plan = api.base.ler(path)
    if (plan.get('etapa') != ETAPA or plan.get('catalogo_versao') != '0.3'
        or plan.get('referencia_versao') != '0.3' or plan.get('envio_autorizado') is not False
        or plan.get('status') != 'PREPARADO_NAO_ENVIADO' or plan.get('orcamento_declarado_usd') is not None):
        raise ValueError('plano de outra etapa/versao/estado')
    if len(plan.get('referencia_sha256', '')) != 64:
        raise ValueError('referencia sem identidade SHA-256')
    if plan['fontes_sha256'] != {f: api.sha((RAIZ / f).read_bytes()) for f in FONTES}:
        raise ValueError('fontes funcionais mudaram; preparar nova identidade')
    for f, h in plan['fontes_editoriais_sha256'].items():
        if api.sha(api.base.relativo(path.parent / 'fontes-originais', f).read_bytes()) != h:
            raise ValueError('fonte editorial preservada mudou')
    public = api.base.ler(path.parent / 'fontes-originais' / CATALOGO)
    if public['referencia_sha256'] != plan['referencia_sha256']:
        raise ValueError('referencia/catalogo de outra versao')
    expected_configs = [configuracao(model, plan['referencia_sha256']) for model in MODELOS]
    if plan['configuracoes'] != {c['id']: c for c in expected_configs}:
        raise ValueError('modelo/configuracao/limite alterado; sem fallback')
    orderraw = (path.parent / 'ordem.json').read_bytes()
    om = montagem._json(orderraw)
    if (api.sha(orderraw) != plan['ordem_sha256'] or om['observacoes'] != ordem()
        or om['semente_local'] != SEMENTE):
        raise ValueError('ordem/semente divergente')
    rows = plan['observacoes']
    if len(rows) != 64:
        raise ValueError('extensao exige exatamente 64 observacoes novas')
    preps, hashes = {}, {}
    for row, original in zip(rows, om['observacoes']):
        if (any(row[k] != v for k, v in original.items())
            or row['status'] != 'PLANEJADA_NAO_EXECUTADA'
            or row['origem'] != 'real' or row['fase'] != 'exploratoria'):
            raise ValueError('identidade/posicao/bloco/fase alterado')
        p = api.base.relativo(path.parent, row['preparacao'])
        if api.sha(p.read_bytes()) != row['preparacao_sha256']:
            raise ValueError('hash da preparacao divergente')
        prep = preps.setdefault(str(p), None)
        if prep is None:
            prep = api.base.conferir_preparacao(p)
            preps[str(p)] = prep
        for k in ('configuracao_id', 'mudanca', 'condicao', 'payload_sha256'):
            if row[k] != prep[k]:
                raise ValueError('vinculo preparacao/configuracao divergente')
        if (prep.get('referencia_versao') != '0.3' or prep.get('referencia_sha256') != plan['referencia_sha256']
            or row['configuracao_id'] != configuracao(row['modelo'], plan['referencia_sha256'])['id']):
            raise ValueError('mistura de versao/configuracao')
        manifest = api.base.ler(p.parent / 'manifesto-original.json')
        if any(manifest[k] != prep[k] for k in ('catalogo_versao', 'referencia_versao', 'referencia_sha256')):
            raise ValueError('vinculo de versao com manifesto divergente')
        if (p.parent / 'documentos/catalogo-baseline.md').read_bytes() != catalogo_texto(public['catalogo']):
            raise ValueError('catalogo de outra versao')
        key = (row['mudanca'], row['condicao'])
        if hashes.setdefault(key, row['payload_sha256']) != row['payload_sha256']:
            raise ValueError('payloads diferentes entre modelos/repeticoes')
    if len(preps) != 32 or len(hashes) != 16:
        raise ValueError('preparacoes/payloads nao sao 32/16')
    montagem.conferir_condicoes(list(preps.values()))
    return plan


def artificial(body, key, timeout):
    """Envelope sem rede: nunca e resposta de modelo ou dado da pesquisa."""
    req = montagem._json(body)
    return 200, api.bytes_json({'id': 'ARTIFICIAL-' + uuid.uuid4().hex, 'model': req['model'],
        'status': 'completed', 'tools': [], 'tool_choice': 'none',
        'output': [{'type': 'message', 'role': 'assistant', 'status': 'completed',
                    'content': [{'type': 'output_text', 'text': '{"requisitos":[],"testes":["T13","T14","T15"]}'}]}]}), None


def controle(plano, lote, limite=64, continuar=False, resposta=artificial):
    return api.capturar(plano, lote, limite, continuar=continuar, conferidor=conferir, controle_http=resposta)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='comando', required=True)
    p = sub.add_parser('preparar')
    p.add_argument('--saida', type=Path, required=True)
    p = sub.add_parser('simular')
    p.add_argument('--plano', type=Path, required=True)
    p = sub.add_parser('controle')
    p.add_argument('--plano', type=Path, required=True)
    p.add_argument('--lote', type=Path, required=True)
    p.add_argument('--limite', type=int, default=64)
    p.add_argument('--continuar', action='store_true')
    args = parser.parse_args(argv)
    try:
        if args.comando == 'preparar':
            print(preparar(args.saida))
        elif args.comando == 'simular':
            plan = conferir(args.plano)
            print(json.dumps({'observacoes': len(plan['observacoes']), 'blocos': [32, 32],
                'configuracoes': plan['configuracoes'], 'rede': False, 'envio_autorizado': False}, indent=2))
        else:
            return controle(args.plano, args.lote, args.limite, args.continuar)
        return 0
    except (ValueError, OSError, KeyError, TypeError) as error:
        print(str(error), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
