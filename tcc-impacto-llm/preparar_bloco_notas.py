"""D-46: preparar/conferir um bloco de notas; nenhum comando de envio ou captura.

Reutiliza o montador, o validador de preparacoes e o corpo API existentes.
Mapeamento de notas, plano e revisao sao privados; somente input e texto entregue.
"""
import argparse
import copy
import difflib
import json
from pathlib import Path
import random
import sys

import coletor_api as api
import extensao_exploratoria as ext
import montagem_entradas as montagem

ROOT = Path(__file__).resolve().parent
ORIGEM = ROOT / 'captura/extensao-20261109-003/plano.json'
VERSAO = 'notas-mc04-0.3-v1-D46'
SEMENTE = 20261111
MODELOS = ('gpt-6-sol', 'gpt-6-astra')
CONDICOES = ('D1', 'E1')
NOTAS = ('N01', 'N02')
FRASES = {
    'N01': 'Uma mudança na herança pode alterar um conflito quando modifica os papéis efetivos.',
    'N02': 'Uma mudança na herança nunca altera um conflito, mesmo quando modifica os papéis efetivos.',
}
REFHASH = '94b6315b935d9817dd833567a0b107a90e88d9be850e93c747e03337450eebc9'
FONTES = ('preparar_bloco_notas.py', 'montagem_entradas.py', 'coletor_piloto.py',
          'coletor_api.py', 'extensao_exploratoria.py')


def exigir(ok, causa):
    if not ok:
        raise ValueError(causa)


def ordem():
    rng = random.Random(SEMENTE)
    rows = []
    for bloco in (1, 2):
        cells = [(m, c, n) for m in MODELOS for c in CONDICOES for n in NOTAS]
        rng.shuffle(cells)
        for model, cond, note in cells:
            rows.append({'observacao_id': f'NOTA03-MC-04-v2-{cond}-{note}-{model[6:].upper()}-R{bloco:02}',
                         'modelo': model, 'mudanca': 'MC-04-v2', 'condicao': cond,
                         'nota_id': note, 'repeticao': bloco, 'bloco': bloco, 'ordem': len(rows) + 1})
    return rows


def fontes_base():
    plan = ext.conferir(ORIGEM)
    exigir(plan['referencia_sha256'] == REFHASH, 'referencia de outra versao')
    docs, sources = {}, {}
    for model in MODELOS:
        for cond in CONDICOES:
            row = next(r for r in plan['observacoes'] if
                       (r['modelo'], r['mudanca'], r['condicao']) == (model, 'MC-04-v2', cond))
            path = api.base.relativo(ORIGEM.parent, row['preparacao'])
            prep = api.base.conferir_preparacao(path)
            exigir(api.sha(path.read_bytes()) == row['preparacao_sha256'], 'origem alterada')
            docs[model, cond] = {e['arquivo']: (path.parent / 'documentos' / e['arquivo']).read_bytes()
                                 for e in prep['documentos']}
            sources[model, cond] = {'arquivo': path.relative_to(ROOT).as_posix(),
                                    'sha256': api.sha(path.read_bytes()), 'configuracao_id': row['configuracao_id']}
    base_notes = {d['notas.md'] for d in docs.values()}
    exigir(len(base_notes) == 1, 'notas anteriores diferentes')
    original = base_notes.pop()
    exigir(original.endswith(b'\n') and not original.endswith(b'\n\n'), 'terminacao inesperada da nota')
    notes = {n: original[:-1] + b' ' + FRASES[n].encode('utf-8') + b'\n' for n in NOTAS}
    return plan, docs, sources, notes


def preparar(saida):
    out = api.base.protegida(saida, 'captura')
    exigir(not out.exists(), 'saida existente; preservar e escolher outro destino')
    old, base_docs, sources, notes = fontes_base()
    out.mkdir(parents=True)
    for note, blob in notes.items():
        api.salvar(out / 'notas' / (note + '.md'), blob)
    preps = {}
    configs = copy.deepcopy(old['configuracoes'])
    for model in MODELOS:
        for cond in CONDICOES:
            source = sources[model, cond]
            for note in NOTAS:
                ident = f'{model}/{cond}-{note}'
                package = out / 'pacotes' / ident
                docs = {**base_docs[model, cond], 'notas.md': notes[note]}
                names = list(montagem.NOMES)
                names.insert(5, 'notas.md')
                entries = []
                for name in names:
                    blob = docs[name]
                    api.salvar(package / name, blob)
                    entries.append({'arquivo': name, 'papel': name.split('.')[0],
                                    'versao': VERSAO if name == 'notas.md' else 'bytes-preservados-plano-003',
                                    'sha256': api.sha(blob), 'tamanho_bytes': len(blob),
                                    'revisao_conteudo': {'estado': 'conferido_tecnicamente',
                                        'responsavel': 'assistente; preparacao offline autorizada D-46',
                                        'data': '2026-11-11',
                                        'alcance': 'composicao e diferenca localizada; revisao humana pendente'}})
                manifest = {'versao_contrato': montagem.CONTRATO, 'pacote_id': 'NOTA03-' + ident.replace('/', '-'),
                            'versao_pacote': VERSAO, 'politica_bytes': 'utf8-sem-bom-lf-v1',
                            'configuracao_id': source['configuracao_id'], 'mudanca': 'MC-04-v2', 'condicao': cond,
                            'status': 'RASCUNHO_PREPARACAO', 'liberado_para_pesquisa': False,
                            'documentos': entries, 'status_notas': 'RASCUNHO_NAO_REVISADO',
                            'versao_notas': VERSAO, 'catalogo_versao': '0.3', 'referencia_versao': '0.3',
                            'referencia_sha256': REFHASH}
                api.salvar_json(package / 'manifesto.json', manifest)
                auth = out / 'autorizacoes' / (ident + '.json')
                api.salvar_json(auth, {'versao': 'autorizacao-textual-v1',
                    'status': 'CONFERIDO_TECNICAMENTE_RASCUNHO',
                    'manifesto_sha256': api.sha((package / 'manifesto.json').read_bytes()),
                    'documentos': [{'arquivo': e['arquivo'], 'sha256': e['sha256']} for e in entries],
                    'preparacao_origem': source, 'revisao_cientifica': 'candidata; para revisao do pesquisador'})
                dest = out / 'preparados' / ident
                prep = montagem.preparar(package, package / 'manifesto.json', dest, auth)
                prep.update(catalogo_versao='0.3', referencia_versao='0.3', referencia_sha256=REFHASH,
                            bloco_exploratorio=VERSAO, nota_id=note)
                # Somente registro novo, antes de publicar seu primeiro hash.
                (dest / 'preparacao.json').write_bytes(api.bytes_json(prep))
                api.base.conferir_preparacao(dest / 'preparacao.json')
                request = out / 'requisicoes' / (ident + '.json')
                api.salvar(request, api.requisicao((dest / 'payload.txt').read_bytes(), configs[source['configuracao_id']]))
                preps[model, cond, note] = (dest / 'preparacao.json', request)
    ordered = ordem()
    api.salvar_json(out / 'ordem.json', {'semente_local': SEMENTE,
        'algoritmo': 'random.Random(20261111).shuffle; um gerador, dois blocos sequenciais',
        'enumeracao': {'modelos': MODELOS, 'condicoes': CONDICOES, 'notas': NOTAS},
        'python': sys.version, 'observacoes': ordered})
    rows = []
    for row in ordered:
        path, req = preps[row['modelo'], row['condicao'], row['nota_id']]
        prep = api.base.ler(path)
        rows.append({**row, 'configuracao_id': prep['configuracao_id'],
                     'preparacao': path.relative_to(out).as_posix(), 'preparacao_sha256': api.sha(path.read_bytes()),
                     'payload_sha256': prep['payload_sha256'], 'requisicao': req.relative_to(out).as_posix(),
                     'requisicao_sha256': api.sha(req.read_bytes()), 'status': 'PLANEJADA_NAO_EXECUTADA',
                     'origem': 'real', 'fase': 'exploratoria', 'conformidade_protocolo': 'pendente'})
    plan = {'versao': VERSAO, 'etapa': 'notas-mc04-0.3-D46', 'status': 'PREPARADO_NAO_ENVIADO',
        'envio_autorizado': False, 'revisao_humana': 'pendente', 'observacoes': rows, 'N_planejado': 16,
        'configuracoes': configs, 'origem_arquivo': ORIGEM.relative_to(ROOT).as_posix(),
        'origem_sha256': api.sha(ORIGEM.read_bytes()), 'ordem_sha256': api.sha((out / 'ordem.json').read_bytes()),
        'catalogo_versao': '0.3', 'referencia_versao': '0.3', 'referencia_sha256': REFHASH,
        'referencia_arquivo': 'materiais/modelos/referencia_candidata_0.3_NAO_ENVIAR_AO_LLM.json',
        'orcamento_novo_declarado_usd': None,
        'configuracoes_limite': 'Configuracoes antigas literais; USD 2 nelas e historico, nao autoriza gasto neste bloco.',
        'fontes_sha256': {name: api.sha((ROOT / name).read_bytes()) for name in FONTES},
        'mapa_notas_privado': {'N01': 'coerente', 'N02': 'incorreta; contradicao deliberada'},
        'chave_analitica': ['versao', 'modelo', 'condicao', 'nota_id'],
        'denominadores': '16 novas planejadas; 8 celulas de 2; nunca combinar com as 64 anteriores',
        'limite_interpretacao': 'Somente selecao, omissoes e excedentes de requisitos/testes; IDs nao demonstram reconhecimento explicito de contradicao.'}
    api.salvar_json(out / 'plano.json', plan)
    diffs = diferencas(out, rows)
    api.salvar_json(out / 'diferencas-payloads.json', diffs)
    api.salvar(out / 'REVISAO-PRIVADA.md', guia(out, plan, notes).encode('utf-8'))
    inventory = [{'arquivo': p.relative_to(out).as_posix(), 'sha256': api.sha(p.read_bytes())}
                 for p in sorted(out.rglob('*')) if p.is_file()]
    api.salvar_json(out / 'manifesto-bloco.json', {'versao': VERSAO, 'natureza': 'PREPARACAO_PRIVADA_NAO_ENVIADA',
                                                'arquivos': inventory})
    conferir(out / 'plano.json')
    return out / 'plano.json'


def diferencas(out, rows):
    docs = {}
    for r in rows:
        key = r['modelo'], r['condicao'], r['nota_id']
        p = api.base.relativo(out, r['preparacao']).parent
        docs[key] = {x.name: x.read_bytes() for x in (p / 'documentos').iterdir()}
    comparisons = []
    def add(tipo, left, right, expected):
        changed = sorted(n for n in docs[left] if docs[left][n] != docs[right][n])
        exigir(changed == [expected], 'diferenca indevida: ' + tipo)
        a, b = docs[left][expected].decode(), docs[right][expected].decode()
        comparisons.append({'tipo': tipo, 'antes': left, 'depois': right, 'documentos_diferentes': changed,
                            'diff': ''.join(difflib.unified_diff(a.splitlines(True), b.splitlines(True),
                                                              fromfile='antes/' + expected, tofile='depois/' + expected))})
    for model in MODELOS:
        for cond in CONDICOES:
            add('nota', (model, cond, 'N01'), (model, cond, 'N02'), 'notas.md')
        for note in NOTAS:
            add('estrutura', (model, 'D1', note), (model, 'E1', note), 'pedido.txt')
    for cond in CONDICOES:
        for note in NOTAS:
            exigir(docs[MODELOS[0], cond, note] == docs[MODELOS[1], cond, note], 'texto varia entre modelos')
    return {'natureza': 'PRIVADO_NAO_ENVIAR', 'comparacoes': comparisons,
            'entre_modelos': 'payloads identicos; requisicoes diferem somente no campo model',
            'entre_repeticoes': 'mesmo payload e mesma requisicao'}


def conferir(path):
    path = montagem.sem_links(path)
    out = path.parent
    plan = api.base.ler(path)
    exigir(plan['versao'] == VERSAO and plan['etapa'] == 'notas-mc04-0.3-D46'
           and plan['status'] == 'PREPARADO_NAO_ENVIADO'
           and plan['envio_autorizado'] is False and plan['revisao_humana'] == 'pendente', 'etapa/envio/revisao divergente')
    exigir(plan['mapa_notas_privado'] == {'N01': 'coerente', 'N02': 'incorreta; contradicao deliberada'}
           and plan['chave_analitica'] == ['versao', 'modelo', 'condicao', 'nota_id']
           and plan['orcamento_novo_declarado_usd'] is None, 'fator/alcance privado alterado')
    inventory = api.base.ler(out / 'manifesto-bloco.json')['arquivos']
    names = [e['arquivo'] for e in inventory]
    exigir(len(names) == len(set(names)), 'manifesto duplicado')
    exigir({p.relative_to(out).as_posix() for p in out.rglob('*') if p.is_file()}
           == set(names) | {'manifesto-bloco.json'}, 'arquivo extra/ausente no bloco')
    for e in inventory:
        exigir(api.sha(api.base.relativo(out, e['arquivo']).read_bytes()) == e['sha256'], 'hash divergente: ' + e['arquivo'])
    old, base_docs, sources, notes = fontes_base()
    exigir(plan['configuracoes'] == old['configuracoes'], 'configuracao alterada')
    exigir(plan['origem_arquivo'] == ORIGEM.relative_to(ROOT).as_posix()
           and plan['origem_sha256'] == api.sha(ORIGEM.read_bytes()), 'origem alterada')
    exigir(plan['referencia_sha256'] == REFHASH
           == api.sha(api.base.relativo(ROOT, plan['referencia_arquivo']).read_bytes()), 'referencia alterada')
    exigir(plan['fontes_sha256'] == {n: api.sha((ROOT / n).read_bytes()) for n in FONTES}, 'fonte funcional alterada')
    raworder = (out / 'ordem.json').read_bytes()
    om = montagem._json(raworder)
    exigir(api.sha(raworder) == plan['ordem_sha256'] and om['semente_local'] == SEMENTE
           and om['observacoes'] == ordem(), 'ordem alterada')
    rows = plan['observacoes']
    exigir(plan['N_planejado'] == len(rows) == len({r['observacao_id'] for r in rows}) == 16, 'denominador/IDs divergentes')
    payloads, prepared, cells = set(), set(), {}
    for r, expected in zip(rows, ordem()):
        exigir(all(r[k] == v for k, v in expected.items()), 'identidade/fator/repeticao alterado')
        exigir(r['status'] == 'PLANEJADA_NAO_EXECUTADA' and r['conformidade_protocolo'] == 'pendente'
               and r['origem'] == 'real' and r['fase'] == 'exploratoria', 'estado/origem alterado')
        p = api.base.relativo(out, r['preparacao'])
        exigir(api.sha(p.read_bytes()) == r['preparacao_sha256'], 'hash da preparacao divergente')
        prep = api.base.conferir_preparacao(p)
        exigir(all(prep[k] == r[k] for k in ('configuracao_id', 'mudanca', 'condicao', 'payload_sha256', 'nota_id')),
               'preparacao nao corresponde a observacao')
        exigir(prep['referencia_sha256'] == REFHASH and prep['referencia_versao'] == '0.3'
               and prep['bloco_exploratorio'] == VERSAO, 'versao da preparacao divergente')
        expected_docs = {**base_docs[r['modelo'], r['condicao']], 'notas.md': notes[r['nota_id']]}
        actual = {q.name: q.read_bytes() for q in (p.parent / 'documentos').iterdir()}
        exigir(actual == expected_docs, 'recorte/nota/documento indevido')
        ident = f'{r["modelo"]}/{r["condicao"]}-{r["nota_id"]}'
        package = out / 'pacotes' / ident
        exigir((package / 'manifesto.json').read_bytes() == (p.parent / 'manifesto-original.json').read_bytes()
               and (out / 'autorizacoes' / (ident + '.json')).read_bytes()
               == (p.parent / 'autorizacao-original.json').read_bytes()
               and all((package / n).read_bytes() == blob for n, blob in expected_docs.items()),
               'pacote/autorizacao diferente do snapshot preparado')
        exigir(r['configuracao_id'] == sources[r['modelo'], r['condicao']]['configuracao_id'], 'modelo/configuracao misturado')
        payload = (p.parent / 'payload.txt').read_bytes()
        exigir(all(label not in payload for label in (b'N01', b'N02', b'nota incorreta', b'nota coerente', b'REVISAO-PRIVADA')),
               'rotulo privado entregue')
        request_path = api.base.relativo(out, r['requisicao'])
        body = api.requisicao(payload, plan['configuracoes'][r['configuracao_id']])
        exigir(request_path.read_bytes() == body and api.sha(body) == r['requisicao_sha256'], 'requisicao divergente')
        payloads.add(api.sha(payload))
        prepared.add(r['preparacao'])
        cells.setdefault((r['modelo'], r['condicao'], r['nota_id']), set()).add(r['repeticao'])
    exigir(len(payloads) == 4 and len(prepared) == 8 and len(cells) == 8
           and all(rs == {1, 2} for rs in cells.values()), 'balanceamento divergente')
    for n in NOTAS:
        exigir((out / 'notas' / (n + '.md')).read_bytes() == notes[n], 'nota de revisao divergente')
    exigir(api.base.ler(out / 'diferencas-payloads.json') == json.loads(json.dumps(diferencas(out, rows))), 'diff divergente')
    return {'completo': True, 'versao': VERSAO, 'envio_autorizado': False, 'executadas': 0,
            'N_planejado': 16, 'celulas': 8, 'repeticoes_por_celula': 2,
            'preparacoes': 8, 'payloads_unicos': 4, 'requisicoes_preparadas': 8,
            'comparacoes_de_diferencas': 8, 'vinculos_manifesto': len(inventory),
            'plano_sha256': api.sha(path.read_bytes()), 'manifesto_sha256': api.sha((out / 'manifesto-bloco.json').read_bytes()),
            'notas_sha256': {n: api.sha(b) for n, b in notes.items()},
            'limite': 'preparacao offline; sem resultado de modelo ou aprovacao humana'}


def guia(out, plan, notes):
    text = ['# Revisão privada do bloco de notas — D-46\n\n',
        '**NÃO ENVIAR ESTE GUIA, PLANO OU MAPA AO MODELO.** Preparação candidata offline; zero chamadas.\n\n',
        'MC-04-v2 × Sol/Astra medium × direta/estruturada × duas notas × duas repetições = **16 planejadas**. '
        'D1/E1 identificam somente a estrutura com notas; `nota_id` é fator separado e obrigatório na análise. '
        'Oito células de N=2, dois blocos de oito, semente local 20261111. '
        'Não misturar com as 64 anteriores nem agregar repetições de N01/N02 como uma única célula.\n\n',
        '## Par final, candidato à revisão humana\n\n']
    for n, description in (('N01', 'coerente'), ('N02', 'incorreta')):
        text += [f'### {n} — {description} (rótulo privado)\n\n', notes[n].decode(), '\n',
                 f'SHA-256: `{api.sha(notes[n])}`.\n\n']
    text += ['O par conserva integralmente a nota 0.2-local anterior, exceto a quebra final, à qual se acrescentam '
        'um espaço e a afirmação candidata. Somente essa afirmação difere entre as novas notas. '
        'N02 contradiz deliberadamente o contrato: retirar a herança altera papéis efetivos e pode eliminar '
        'o conflito dependente dessa expansão. A referência candidata 0.3 permanece a mesma para ambos os braços; '
        'a nota não redefine o gabarito. O restante do conteúdo, a instrução de sistema e a advertência comum de '
        'usar o material fornecido são idênticos; nenhuma advertência exclusiva foi acrescentada.\n\n',
        '## Diferenças dos payloads\n\n',
        '- N01 → N02, com modelo/estrutura fixos: somente a afirmação final de `notas.md`.\n',
        '- Direta D1 → estruturada E1, com modelo/nota fixos: somente `pedido.txt`, literal do plano 003.\n',
        '- Sol → Astra: payload idêntico; no corpo da requisição muda somente `model`.\n',
        '- R01 → R02: payload e corpo idênticos; IDs/ordem/repetição ficam fora do input.\n\n',
        'Os oito diffs efetivamente calculados estão em [diferencas-payloads.json](diferencas-payloads.json). '
        'Em todos os pacotes permanecem sistema, definições, requisitos, catálogo 0.3 com resultados da baseline, '
        'MC-04-v2 e schema originais. O modelo recebe somente o payload, sem nomes de pasta, IDs de nota ou mapa.\n\n',
        '## Saída, interpretação e execução futura\n\n',
        'Preservar JSON com `requisitos` e `testes`; avaliar seleção, omissões e excedentes pelas mesmas fórmulas. '
        'IDs sozinhos não demonstram reconhecimento explícito da contradição. O par difere também em comprimento '
        '(pode/nunca, quando/mesmo quando); com duas repetições por célula, o resultado futuro será exploratório. '
        'Não há braço sem nota neste bloco e as 64 respostas anteriores não são controle intercambiável.\n\n',
        'Configurações anteriores foram copiadas literalmente: modelos/medium, 4096, timeout 120 s, ferramentas '
        'vazias, sem histórico/retries, mesma modalidade de saída textual. A declaração USD 2 nelas é histórica; '
        'não se transfere autorização nem orçamento para este bloco (`orcamento_novo_declarado_usd=null`).\n\n',
        '`preparar_bloco_notas.py` oferece somente `preparar` e `conferir`; não captura nem envia. '
        'O plano tem etapa própria e `envio_autorizado=false`; a CLI antiga da extensão 64 recusa este plano. '
        'Antes de executar futuramente, faltam revisão humana do par/pacotes/ordem, autorização própria e '
        'integração específica da captura/avaliação para preservar o fator nota e a fase exploratória. '
        'Os montadores e o corpo API já foram reutilizados; não se declara o envio integrado.\n\n',
        'A conformidade anterior não é alterada por esta preparação. Não se preenchem aprovações humanas.\n\n',
        '## Ordem planejada completa\n\n', '| Ordem | Bloco | Observação |\n|---:|---:|---|\n']
    text += [f'| {r["ordem"]} | {r["bloco"]} | {r["observacao_id"]} |\n' for r in plan['observacoes']]
    return ''.join(text)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='comando', required=True)
    sub.add_parser('preparar').add_argument('--saida', required=True)
    sub.add_parser('conferir').add_argument('--plano', required=True)
    args = parser.parse_args(argv)
    def offline(event, values):
        if event in ('socket.connect', 'socket.getaddrinfo', 'socket.gethostbyname'):
            raise RuntimeError('D-46: rede proibida')
    sys.addaudithook(offline)
    try:
        path = preparar(args.saida) if args.comando == 'preparar' else args.plano
        print(json.dumps(conferir(path), ensure_ascii=True, indent=2))
        return 0
    except (OSError, ValueError, KeyError) as error:
        print(str(error), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
