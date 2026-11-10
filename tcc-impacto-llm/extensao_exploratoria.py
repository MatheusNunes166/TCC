"""Extensao 0.3: preparacao, simulacao, controle e envio explicito (--enviar-real).

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
INTEGRACAO = 'envio-extensao-D42-v1'
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
         'integracao': INTEGRACAO, 'orcamento_declarado_usd': '2',
         'limite_orcamento': 'USD 2 de planejamento; risco aceito pelo pesquisador; sem controle automatico ou garantia de teto',
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


def preparar(saida, origem=None):
    out = api.base.protegida(saida, 'captura')
    if out.exists():
        raise ValueError('saida existente; preservar tentativa anterior')
    previous = None
    editorial_root = RAIZ
    if origem is not None:
        origem = montagem.sem_links(origem)
        previous = api.base.ler(origem)
        editorial_root = origem.parent / 'fontes-originais'
        orderraw = (origem.parent / 'ordem.json').read_bytes()
        oldorder = montagem._json(orderraw)['observacoes']
        if (previous.get('etapa') != ETAPA or previous.get('referencia_versao') != '0.3'
            or len(previous.get('observacoes', [])) != 64 or oldorder != ordem()
            or api.sha(orderraw) != previous.get('ordem_sha256')):
            raise ValueError('plano anterior de outra extensao/ordem/referencia')
        for row, expected in zip(previous['observacoes'], oldorder):
            if (any(row[k] != value for k, value in expected.items())
                or row['origem'] != 'real' or row['fase'] != 'exploratoria'
                or row['status'] != 'PLANEJADA_NAO_EXECUTADA'):
                raise ValueError('identidade/ordem anterior divergente')
            config = previous['configuracoes'][row['configuracao_id']]
            if (config['modelo_solicitado'] != row['modelo'] or config['esforco_solicitado'] != 'medium'
                or config['max_output_tokens'] != 4096):
                raise ValueError('configuracao anterior divergente')
        for name, h in previous['fontes_editoriais_sha256'].items():
            if api.sha(api.base.relativo(editorial_root, name).read_bytes()) != h:
                raise ValueError('fonte editorial anterior alterada')
    public = api.base.ler(editorial_root / CATALOGO)
    if public['versao'] != '0.3' or [c['id'] for c in public['catalogo']] != [f'T{i:02}' for i in range(1, 16)]:
        raise ValueError('catalogo publico nao e 0.3 completo')
    catalog = catalogo_texto(public['catalogo'])
    if catalog != (editorial_root / 'materiais/modelos/catalogo_baseline_0.3.md').read_bytes():
        raise ValueError('catalogos JSON/MD divergentes')
    refhash = public['referencia_sha256']
    if previous is not None and refhash != previous['referencia_sha256']:
        raise ValueError('referencia anterior divergente do catalogo preservado')
    configs = [configuracao(model, refhash) for model in MODELOS]
    out.mkdir(parents=True)
    source_hashes = {}
    for relative in (*fontes.FONTES, CATALOGO, 'materiais/modelos/catalogo_baseline_0.3.md'):
        raw = (editorial_root / relative).read_bytes()
        api.salvar(out / 'fontes-originais' / relative, raw)
        source_hashes[relative] = api.sha(raw)
    order = ordem() if previous is None else oldorder
    order_meta = {'semente_local': SEMENTE, 'algoritmo': 'random.Random(20261109).shuffle; um gerador, dois blocos sequenciais',
                  'enumeracao': 'mudancas MC-01,MC-02,MC-03,MC-04-v2; condicoes D0,D1,E0,E1; modelos sol,astra',
                  'python': sys.version, 'observacoes': order}
    if previous is None:
        api.salvar_json(out / 'ordem.json', order_meta)
    else:
        api.salvar(out / 'ordem.json', orderraw)
        api.salvar(out / 'plano-anterior.json', origem.read_bytes())
    prepared = {}
    for config in configs:
        for change in montagem.MUDANCAS:
            for cond in montagem.CONDICOES:
                if previous is None:
                    docs, provenance = fontes.reunir_fontes(RAIZ, change, cond)
                else:
                    row = next(r for r in previous['observacoes'] if
                               (r['mudanca'], r['condicao'], r['modelo']) == (change, cond, config['modelo_solicitado']))
                    source = api.base.relativo(origem.parent, row['preparacao'])
                    if api.sha(source.read_bytes()) != row['preparacao_sha256']:
                        raise ValueError('hash da preparacao anterior divergente')
                    oldprep = api.base.conferir_preparacao(source)
                    if (any(oldprep[k] != row[k] for k in ('configuracao_id', 'mudanca', 'condicao', 'payload_sha256'))
                        or oldprep.get('referencia_sha256') != refhash):
                        raise ValueError('vinculos da preparacao anterior divergentes')
                    docs = {item['arquivo']: (source.parent / 'documentos' / item['arquivo']).read_bytes()
                            for item in oldprep['documentos']}
                    provenance = api.base.ler(source.parent / 'autorizacao-original.json')['fontes']
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
                if previous is not None and prep['payload_sha256'] != oldprep['payload_sha256']:
                    raise ValueError('nova preparacao alterou o texto experimental anterior')
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
    if previous is not None:
        fields = ('observacao_id', 'ordem', 'bloco', 'repeticao', 'mudanca', 'condicao', 'modelo', 'payload_sha256')
        if any(any(new[k] != old[k] for k in fields) for new, old in zip(rows, previous['observacoes'])):
            raise ValueError('alteracao de ordem/identidades/textos durante a nova preparacao')
    plan = {'etapa': ETAPA, 'integracao': INTEGRACAO, 'status': 'PREPARADO_NAO_ENVIADO', 'catalogo_versao': '0.3',
            'referencia_versao': '0.3', 'referencia_sha256': refhash,
            'configuracoes': {c['id']: c for c in configs}, 'observacoes': rows,
            'fontes_sha256': {f: api.sha((RAIZ / f).read_bytes()) for f in FONTES},
            'fontes_editoriais_sha256': source_hashes,
            'ordem_sha256': api.sha((out / 'ordem.json').read_bytes()),
            'orcamento_declarado_usd': '2', 'envio_autorizado': True,
            'restricao': 'envio somente por invocacao explicita com --enviar-real; USD 2 nao e teto garantido'}
    if previous is not None:
        plan['plano_anterior_sha256'] = api.sha((out / 'plano-anterior.json').read_bytes())
    api.salvar_json(out / 'plano.json', plan)
    conferir(out / 'plano.json')
    return out / 'plano.json'


def conferir(path):
    path = montagem.sem_links(path)
    plan = api.base.ler(path)
    if (plan.get('etapa') != ETAPA or plan.get('integracao') != INTEGRACAO or plan.get('catalogo_versao') != '0.3'
        or plan.get('referencia_versao') != '0.3' or plan.get('envio_autorizado') is not True
        or plan.get('status') != 'PREPARADO_NAO_ENVIADO' or plan.get('orcamento_declarado_usd') != '2'):
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
    if 'plano_anterior_sha256' in plan:
        previousraw = (path.parent / 'plano-anterior.json').read_bytes()
        previous = montagem._json(previousraw)
        fields = ('observacao_id', 'ordem', 'bloco', 'repeticao', 'mudanca', 'condicao', 'modelo', 'payload_sha256')
        if (api.sha(previousraw) != plan['plano_anterior_sha256'] or len(previous['observacoes']) != 64
            or previous['referencia_sha256'] != plan['referencia_sha256']
            or previous['ordem_sha256'] != plan['ordem_sha256']
            or any(any(new[k] != old[k] for k in fields) for new, old in zip(plan['observacoes'], previous['observacoes']))):
            raise ValueError('vinculo/ordem/textos do plano anterior divergentes')
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


def iniciar(plano, lote, limite, continuar=False, enviar_real=False, sender=None):
    if not enviar_real:
        raise ValueError('envio exige --enviar-real; nenhuma chamada realizada')
    return api.capturar(plano, lote, limite, continuar=continuar, real=True,
                        sender=api.enviar if sender is None else sender, conferidor=conferir)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='comando', required=True)
    p = sub.add_parser('preparar')
    p.add_argument('--saida', type=Path, required=True)
    p.add_argument('--origem', type=Path, help='plano anterior: preservar literalmente ordem e textos')
    p = sub.add_parser('simular')
    p.add_argument('--plano', type=Path, required=True)
    for name in ('controle', 'iniciar'):
        p = sub.add_parser(name, help='controle artificial offline' if name == 'controle' else 'envio API real; exige --enviar-real')
        p.add_argument('--plano', type=Path, required=True)
        p.add_argument('--lote', type=Path, required=True)
        p.add_argument('--limite', type=int, required=name == 'iniciar', default=64 if name == 'controle' else None)
        p.add_argument('--continuar', action='store_true')
        if name == 'iniciar':
            p.add_argument('--enviar-real', action='store_true')
    args = parser.parse_args(argv)
    try:
        if args.comando == 'preparar':
            print(preparar(args.saida, args.origem))
        elif args.comando == 'simular':
            plan = conferir(args.plano)
            print(json.dumps({'observacoes': len(plan['observacoes']), 'blocos': [32, 32],
                'configuracoes': plan['configuracoes'], 'rede': False, 'envio_exige_flag': True}, indent=2))
        elif args.comando == 'controle':
            return controle(args.plano, args.lote, args.limite, args.continuar)
        else:
            return iniciar(args.plano, args.lote, args.limite, args.continuar, args.enviar_real)
        return 0
    except (ValueError, OSError, KeyError, TypeError) as error:
        print(str(error), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
