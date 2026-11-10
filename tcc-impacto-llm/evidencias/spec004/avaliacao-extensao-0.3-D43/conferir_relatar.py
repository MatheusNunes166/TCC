"""Receita offline D-43 para este lote: conferir e relatar, sem coletar/alterar fontes.

As etapas de avaliacao/revisao usam a CLI existente, separadamente.
"""
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from fractions import Fraction
import argparse
import csv
import io
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
EVID = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))


def bloquear_rede(event, args):
    if event in ('socket.connect', 'socket.getaddrinfo', 'socket.gethostbyname'):
        raise RuntimeError('D-43: rede proibida na conferencia e relato offline')


sys.addaudithook(bloquear_rede)
import avaliacao_ids as a
import coletor_api as api
import extensao_exploratoria as ext

LOTE = ROOT / 'captura/extensao-real-0.3-001'
PLANO = ROOT / 'captura/extensao-20261109-003/plano.json'
REF = ROOT / 'materiais/modelos/referencia_candidata_0.3_NAO_ENVIAR_AO_LLM.json'
HASH_REF = '94b6315b935d9817dd833567a0b107a90e88d9be850e93c747e03337450eebc9'
AVAL = ROOT / 'avaliados/extensao-real-0.3-001-avaliacao-001'


def salvar(path, value):
    with path.open('xb') as f:
        f.write(api.bytes_json(value))


def exigir(ok, message):
    if not ok:
        raise ValueError(message)


def conferir():
    # Antes de avaliar: inventario literal dos originais e das avaliacoes anteriores.
    inventory = {}
    for area in ('captura', 'avaliados', 'materiais', 'variantes'):
        for p in sorted((ROOT / area).rglob('*')):
            if p.is_file():
                api.montagem.sem_links(p)
                inventory[p.relative_to(ROOT).as_posix()] = a.sha(p.read_bytes())
    for name in ('coletor_api.py', 'coletor_piloto.py', 'extensao_exploratoria.py',
                 'avaliacao_ids.py', 'montagem_entradas.py', 'revisao_conformidade.py', 'fontes_autorizadas.py'):
        inventory[name] = a.sha((ROOT / name).read_bytes())
    salvar(EVID / 'estado-inicial.json', {'head': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT).decode().strip(),
        'alteracoes_locais_anteriores': subprocess.check_output(['git', 'status', '--short'], cwd=ROOT).decode(),
        'sha256_originais': inventory, 'rede': False})
    exigir(not AVAL.exists(), 'saida de avaliacao ja existe; escolher outra sem sobrescrever')
    rawplan = PLANO.read_bytes()
    exigir((LOTE / 'plano-original.json').read_bytes() == rawplan, 'plano copiado no lote diverge do plano 003')
    plan = ext.conferir(PLANO)
    header = api.base.ler(LOTE / 'lote.json')
    exigir(header['plano_sha256'] == a.sha(rawplan), 'hash do plano diverge do lote')
    exigir((header['origem'], header['fase'], header['etapa']) == ('real', 'exploratoria', ext.ETAPA), 'identidade de lote divergente')
    exigir(header['coletor_sha256'] == a.sha((ROOT / 'coletor_api.py').read_bytes()), 'fonte do coletor difere da captura')
    rawref = REF.read_bytes()
    exigir(a.sha(rawref) == HASH_REF == plan['referencia_sha256'] == header['referencia_sha256'], 'referencia nao corresponde ao hash solicitado/plano/lote')
    reference = a.json_estrito(rawref)
    exigir(reference['versao'] == '0.3' and len(reference['catalogo']) == 15 and
           {c['id'] for c in reference['catalogo']} == {f'T{i:02}' for i in range(1, 16)}, 'referencia nao contem catalogo 0.3 com quinze IDs')
    for change in reference['mudancas']:
        a.referencia_da_mudanca(reference, change['id'])
    rows = plan['observacoes']
    ids = {r['observacao_id'] for r in rows}
    exigir(len(rows) == len(ids) == 64, 'nao ha 64 identidades unicas no plano')
    exigir({p.name for p in LOTE.iterdir() if p.is_dir()} == ids, 'pastas de observacoes ausentes/extras')
    exigir({p.name for p in LOTE.iterdir() if p.is_file()} == {'lote.json', 'plano-original.json'}, 'arquivos extras ou lock no lote')
    counts = Counter((r['modelo'], r['mudanca'], r['condicao']) for r in rows)
    exigir(len(counts) == 32 and set(counts.values()) == {2}, 'duas repeticoes por combinacao nao confirmadas')
    records, response_ids, request_ids, attempts = [], set(), set(), set()
    last_end = None
    closing_links = 0
    for row in rows:
        root = LOTE / row['observacao_id'] / 'T01'
        exigir({p.name for p in root.parent.iterdir()} == {'T01'}, 'tentativas/pastas extras: ' + row['observacao_id'])
        reg = api.base.conferir_fechamento(root)
        closing = api.base.ler(root / 'fechamento.json')['arquivos']
        exigir(len(closing) == len({f['arquivo'] for f in closing}), 'arquivo repetido no fechamento')
        closing_links += len(closing)
        for key in ('observacao_id', 'configuracao_id', 'mudanca', 'condicao', 'payload_sha256',
                    'preparacao_sha256', 'ordem', 'bloco', 'repeticao'):
            exigir(reg[key] == row[key], 'identidade divergente: ' + row['observacao_id'] + '/' + key)
        exigir((reg['origem'], reg['fase'], reg['etapa'], reg['integracao']) ==
               ('real', 'exploratoria', ext.ETAPA, ext.INTEGRACAO), 'origem/fase/etapa divergente')
        exigir(reg['plano_sha256'] == a.sha(rawplan) and reg['referencia_sha256'] == HASH_REF, 'vinculos plano/referencia divergentes')
        config = plan['configuracoes'][row['configuracao_id']]
        exigir(reg['configuracao'] == config and config['modelo_solicitado'] == row['modelo']
               and config['esforco_solicitado'] == 'medium' and config['max_output_tokens'] == 4096, 'configuracao divergente')
        exigir(reg['versoes'] == {'coletor': api.VERSAO, 'coletor_sha256': header['coletor_sha256']}, 'versao funcional divergente')
        source = api.base.relativo(PLANO.parent, row['preparacao'])
        archived = root / 'preparacao/preparacao.json'
        prep = api.base.conferir_preparacao(archived)
        exigir(archived.read_bytes() == source.read_bytes() and prep['preparacao_id'] == reg['preparacao_id'], 'preparacao arquivada difere da utilizada')
        for item in prep['arquivos']:
            exigir((archived.parent / item['arquivo']).read_bytes() == (source.parent / item['arquivo']).read_bytes(), 'documento de preparacao divergente')
        payload = (root / 'entrada.bin').read_bytes()
        exigir(payload == (archived.parent / 'payload.txt').read_bytes()
               and a.sha(payload) == reg['entrada_enviada_sha256'] == row['payload_sha256'], 'entrada enviada divergente')
        body = (root / 'requisicao.json').read_bytes()
        exigir(body == api.requisicao(payload, config) and a.sha(body) == reg['requisicao_sha256'], 'requisicao diverge do payload/configuracao')
        http = api.base.ler(root / 'http-requisicao.json')
        exigir(http['url'] == api.ENDPOINT and http['metodo'] == 'POST' and http['corpo_sha256'] == a.sha(body)
               and http['corpo_tamanho'] == len(body) and http['headers'] == api.headers_publicos(body), 'envelope de requisicao divergente')
        raw = (root / 'resposta-http.bin').read_bytes()
        transport = api.base.ler(root / 'transporte.json')
        exigir(transport['corpo_sha256'] == a.sha(raw) and transport['corpo_tamanho'] == len(raw)
               and transport['http_status'] == reg['http_status'] and transport['request_id'] == reg['request_id']
               and transport['falha'] == reg['falha_transporte'], 'envelope de transporte divergente')
        parsed = api.interpretar(raw, reg['http_status'], config)
        exigir(parsed['texto'] == (root / 'resposta.bin').read_bytes() and a.sha(parsed['texto']) == reg['resposta_sha256']
               and len(parsed['texto']) == reg['resposta_tamanho'], 'extracao/bytes da resposta divergentes')
        exigir(parsed['usage'] == reg['usage'] and parsed['response_id'] == reg['response_id']
               and parsed['modelo_reportado'] == reg['modelo_reportado'] == row['modelo'], 'modelo/usage/response_id divergente')
        exigir(parsed['desvios'] == reg['desvios'], 'desvios registrados diferem do envelope')
        exigir(parsed['concluida'] and reg['estado_tecnico'] == 'concluida' and reg['fragmento'] is False
               and reg['http_status'] == 200 and reg['falha_transporte'] is None, 'resultado nao concluido/HTTP/falha')
        exigir(reg['retentativas_cliente'] == transport['retentativas_cliente'] == 0
               and reg['tentativa_anterior'] is None, 'retentativa inesperada')
        for value, seen in ((reg['response_id'], response_ids), (reg['request_id'], request_ids), (reg['tentativa_id'], attempts)):
            exigir(isinstance(value, str) and value and value not in seen, 'identificador remoto/tentativa ausente ou repetido')
            seen.add(value)
        start, end = map(datetime.fromisoformat, (reg['instante_execucao'], reg['instante_fim']))
        exigir(start.tzinfo is not None and end.tzinfo is not None and end >= start
               and (last_end is None or start >= last_end), 'ordem temporal divergente da ordem planejada')
        last_end = end
        usage = reg['usage']
        exigir(all(type(usage.get(k)) is int and usage[k] >= 0 for k in ('input_tokens', 'output_tokens', 'total_tokens'))
               and usage['input_tokens'] + usage['output_tokens'] == usage['total_tokens'], 'contagem de tokens incoerente')
        exigir(0 <= usage.get('output_tokens_details', {}).get('reasoning_tokens', 0) <= usage['output_tokens'], 'raciocinio fora da saida total')
        records.append(reg)
    result = {'conforme_tecnicamente': True, 'conformidade_protocolo_aprovada': False,
        'plano': str(PLANO), 'plano_sha256': a.sha(rawplan), 'referencia': str(REF), 'referencia_sha256': HASH_REF,
        'observacoes': len(records), 'modelos': dict(Counter(r['modelo_reportado'] for r in records)),
        'vinculos_fechamentos_conferidos': closing_links,
        'conformidade_registrada': dict(Counter(r['conformidade_protocolo'] for r in records)),
        'desvios_detectados': sum(bool(r['desvios']) for r in records),
        'ordem_temporal_conforme_plano': True, 'originais_inventariados': len(inventory),
        'repeticoes_por_celula': 2, 'request_ids_unicos': len(request_ids), 'response_ids_unicos': len(response_ids),
        'rede': False, 'primeira_execucao': records[0]['instante_execucao'], 'ultima_conclusao': records[-1]['instante_fim']}
    salvar(EVID / 'integridade.json', result)
    print(json.dumps(result, indent=2))


def relatar():
    integrity = api.base.ler(EVID / 'integridade.json')
    exigir(integrity['conforme_tecnicamente'], 'conferencia tecnica nao concluida')
    entries = api.base.ler(AVAL / 'lista.json')
    planned = api.base.ler(AVAL / 'observacoes.json')
    template = api.base.ler(AVAL / 'revisao-conformidade-pendente.json')
    exigir(template['responsavel'] is None and template['data'] is None
           and len(template['observacoes']) == 64
           and all(r['decisao'] == 'pendente' and r['justificativa'] is None for r in template['observacoes']),
           'modelo de revisao foi preenchido; preservar pendencia nesta entrega')
    refs = set()
    records = []
    for entry in entries:
        path = api.base.relativo(AVAL, entry['arquivo'])
        raw = path.read_bytes()
        exigir(a.sha(raw) == entry['sha256'], 'avaliacao alterada')
        reg = a.json_estrito(raw)
        exigir(reg['completo'] and reg['origem'] == 'real' and reg['fase'] == 'exploratoria'
               and reg['conformidade_protocolo'] == 'pendente', 'origem/fase/conformidade divergente')
        exigir(reg['referencia']['versao'] == '0.3' and reg['referencia']['sha256'] == HASH_REF, 'referencia divergente na avaliacao')
        refs.add(tuple(a._versao(reg)[:4]))
        records.append(reg)
    exigir(len(records) == len(planned) == 64 and len(refs) == 1
           and {r['observacao_id'] for r in records} == {r['observacao_id'] for r in planned}, 'avaliacoes ausentes/duplicadas/versoes misturadas')
    cells, diffs, tablerows = [], [], []
    def metrics(rs, ps):
        # Mesmas formulas do avaliador. Nao altera conformidade nem chama o
        # gate de resumo como se houvesse aprovacao humana.
        group, code = a._grupo(rs, ps, False)
        valid = [r for r in rs if r['status_avaliacao'] == 'avaliada']
        counts = {}
        for dim in ('requisitos', 'testes'):
            counts[dim] = {k: sum(r[dim][k] for r in valid) for k in ('TP', 'FN', 'FP')}
            counts[dim].update(correspondencias_exatas=sum(r[dim]['metricas_propostas']['correspondencia_exata'] for r in valid),
                               denominador_exatas=len(valid),
                               respostas_com_duplicatas=sum(bool(r[dim]['duplicatas']) for r in valid),
                               respostas_com_desconhecidos=sum(bool(r[dim]['desconhecidos']) for r in valid))
        return group, counts
    for model in ext.MODELOS:
        for change in ext.montagem.MUDANCAS:
            for cond in ext.montagem.CONDICOES:
                rs = sorted([r for r in records if (r['configuracao']['modelo_solicitado'], r['mudanca'], r['condicao']) == (model, change, cond)], key=lambda r: r['repeticao'])
                ps = [p for p in planned if (p['configuracao_id'], p['mudanca'], p['condicao']) == (rs[0]['configuracao_id'], change, cond)]
                exigir(len(rs) == len(ps) == 2 and {r['repeticao'] for r in rs} == {1, 2}, 'denominador/repeticoes de celula invalido')
                group, counts = metrics(rs, ps)
                pair_equal = {dim: int(rs[0][dim]['S'] == rs[1][dim]['S']) if group['contagens']['V'] == 2 else None
                              for dim in ('requisitos', 'testes')}
                cell = {'modelo': model, 'mudanca': change, 'condicao': cond,
                        'observacoes': [r['observacao_id'] for r in rs], 'descritivo': group,
                        'contagens_ids': counts, 'pares_selecao_igual': pair_equal, 'pares_previstos': 1}
                cells.append(cell)
                row = {'modelo': model, 'mudanca': change, 'condicao': cond, **group['contagens']}
                for dim, prefix in (('requisitos', 'RF'), ('testes', 'T')):
                    row.update({prefix + '_' + k: v for k, v in counts[dim].items()})
                    row.update({prefix + '_' + k: (v['fracao'] if v else None) for k, v in group['validas'][dim].items()})
                    j = group['jaccard'][dim]
                    row[prefix + '_jaccard'] = j['valor']['fracao'] if j['valor'] else None
                    row[prefix + '_pares'] = j['numero_pares']
                    row[prefix + '_pares_iguais'] = pair_equal[dim]
                tablerows.append(row)
                for reg in rs:
                    if reg['status_avaliacao'] != 'avaliada':
                        diffs.append({'observacao_id': reg['observacao_id'], 'status': reg['status_avaliacao']})
                        continue
                    for dim in ('requisitos', 'testes'):
                        if not reg[dim]['metricas_propostas']['correspondencia_exata']:
                            diffs.append({'observacao_id': reg['observacao_id'], 'modelo': model,
                                          'mudanca': change, 'condicao': cond, 'repeticao': reg['repeticao'], 'dimensao': dim,
                                          **{k: reg[dim][k] for k in ('S', 'G', 'acertos', 'omissoes', 'excedentes', 'duplicatas', 'desconhecidos')},
                                          'avaliacao_arquivo': str(AVAL / reg['observacao_id'] / 'T01/avaliacao.json')})
    totals = {}
    for model in ext.MODELOS:
        modelcells = [c for c in cells if c['modelo'] == model]
        numbers = {k: sum(c['descritivo']['contagens'][k] for c in modelcells)
                   for k in modelcells[0]['descritivo']['contagens']}
        # Consistencia so entre repeticoes da mesma celula. Medias por modelo
        # sao ponderadas por V; nao executar _grupo em celulas diferentes.
        group = {'contagens': numbers, 'validas': {}}
        counts = {}
        for dim in ('requisitos', 'testes'):
            group['validas'][dim] = {
                name: a.numero(sum(Fraction(c['descritivo']['validas'][dim][name]['fracao'])
                                   * c['descritivo']['contagens']['V'] for c in modelcells) / numbers['V'])
                if numbers['V'] else None for name in ('precisao', 'revocacao', 'f1')}
            counts[dim] = {k: sum(c['contagens_ids'][dim][k] for c in modelcells)
                           for k in modelcells[0]['contagens_ids'][dim]}
        totals[model] = {'descritivo': group, 'contagens_ids': counts}
    tokens = {}
    for model in ext.MODELOS:
        regs = [api.base.ler(LOTE / r['observacao_id'] / 'T01/tentativa.json') for r in records
                if r['configuracao']['modelo_solicitado'] == model]
        total = {'observacoes': len(regs), 'input_tokens': 0, 'output_tokens': 0,
                 'total_tokens': 0, 'reasoning_tokens_subconjunto_saida': 0,
                 'cached_tokens_subconjunto_entrada': 0, 'cache_write_tokens_reportados_subconjunto_entrada': 0}
        for reg in regs:
            u = reg['usage']
            for k in ('input_tokens', 'output_tokens', 'total_tokens'):
                total[k] += u[k]
            total['reasoning_tokens_subconjunto_saida'] += u.get('output_tokens_details', {}).get('reasoning_tokens', 0)
            total['cached_tokens_subconjunto_entrada'] += u.get('input_tokens_details', {}).get('cached_tokens', 0)
            total['cache_write_tokens_reportados_subconjunto_entrada'] += u.get('input_tokens_details', {}).get('cache_write_tokens', 0)
        exigir(total['input_tokens'] + total['output_tokens'] == total['total_tokens'], 'total de tokens incoerente')
        tokens[model] = total
    result = {'natureza': 'DESCRITIVO_CONFORMIDADE_PENDENTE', 'origem': 'real', 'fase': 'exploratoria',
              'referencia_sha256': HASH_REF, 'referencia_versao': '0.3', 'N_planejado': 64,
              'N_avaliacoes': len(records), 'conformidade_pendente': 64, 'conformidade_aprovada': 0,
              'criterios_alterados': False, 'politica': a.POLITICA,
              'agregacao_PRF': 'media aritmetica por resposta valida (macro), conforme _grupo existente; sem imputacao',
              'acertos_omissoes_excedentes': 'somados nas duas respostas por celula; nao sao denominadores da media macro',
              'consistencia': 'um par por celula; Jaccard de conjuntos; igualdade nao significa acerto',
              'celulas': cells, 'por_modelo': totals, 'divergencias': diffs, 'tokens': tokens}
    salvar(AVAL / 'descritivo-pendente.json', result)
    stream = io.StringIO(newline='')
    writer = csv.DictWriter(stream, fieldnames=list(tablerows[0]), lineterminator='\n')
    writer.writeheader()
    writer.writerows(tablerows)
    with (AVAL / 'tabelas-descritivas.csv').open('xb') as f:
        f.write(stream.getvalue().encode('utf-8'))
    salvar(AVAL / 'divergencias-ids.json', diffs)
    salvar(AVAL / 'tokens-por-modelo.json', tokens)
    lines = ['# Tabelas descritivas — conformidade pendente\n\n',
        'Referencia candidata 0.3; 64 respostas reais, sem misturar piloto/controles. Todas as celulas: N=2 planejadas, C=2 concluidas, V=2 validas, I=0 invalidas, T=0 falhas. Nenhuma conformidade aprovada.\n\n',
        'A/O/E = acertos (TP)/omissoes (FN)/excedentes (FP), somados nas duas respostas. P/R/F1 = medias por resposta valida, denominador V=2, usando as formulas existentes; nao sao razoes das somas de A/O/E. Exata = respostas iguais a referencia/V. J = Jaccard entre as duas repeticoes, um par por celula; nao mede acerto. Valores fracionarios sao exatos.\n\n']
    for model in ext.MODELOS:
        lines += ['## ' + model + '\n\n',
                  '| Mudanca | Condicao | Formato V/C | RF A/O/E | RF P/R/F1 | RF exata | RF J (1 par) | Testes A/O/E | Testes P/R/F1 | Testes exata | Testes J (1 par) |\n',
                  '|---|---|---|---|---|---|---|---|---|---|---|\n']
        for r in tablerows:
            if r['modelo'] != model:
                continue
            def aoe(prefix):
                return '/'.join(str(r[prefix + '_' + k]) for k in ('TP', 'FN', 'FP'))
            def prf(prefix):
                return '/'.join(str(r[prefix + '_' + k]) for k in ('precisao', 'revocacao', 'f1'))
            values = [r['mudanca'], r['condicao'], '2/2', aoe('RF'), prf('RF'),
                      str(r['RF_correspondencias_exatas']) + '/2', str(r['RF_jaccard']),
                      aoe('T'), prf('T'), str(r['T_correspondencias_exatas']) + '/2', str(r['T_jaccard'])]
            # Separar fracoes de precisao/revocacao/F1 visualmente.
            values[4] = ' ; '.join(str(r['RF_' + k]) for k in ('precisao', 'revocacao', 'f1'))
            values[8] = ' ; '.join(str(r['T_' + k]) for k in ('precisao', 'revocacao', 'f1'))
            lines.append('| ' + ' | '.join(values) + ' |\n')
        lines.append('\n')
    lines += ['P/R/F1 estao na ordem precisao ; revocacao ; F1. Os IDs divergentes constam de `divergencias-ids.json`; os valores por resposta permanecem nas 64 avaliacoes individuais. O resumo controlado em `resumo/resumo.json` continua bloqueado, sem alteracao das conformidades originais.\n']
    with (AVAL / 'TABELAS.md').open('xb') as f:
        f.write(''.join(lines).encode())
    original = api.base.ler(EVID / 'estado-inicial.json')['sha256_originais']
    mismatches = [name for name, h in original.items() if not (ROOT / name).is_file() or a.sha((ROOT / name).read_bytes()) != h]
    exigir(not mismatches, 'originais alterados: ' + repr(mismatches))
    salvar(EVID / 'preservacao.json', {'arquivos_anteriores_conferidos': len(original), 'divergencias': mismatches,
                                      'coletor_planos_notas_prompts_referencia_preservados': True})
    print(json.dumps({'avaliacoes': len(records), 'divergencias': diffs, 'tokens': tokens,
                      'conformidade_pendente': 64, 'originais_preservados': len(original)}, indent=2))


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('acao', choices=('conferir', 'relatar'))
    args = p.parse_args()
    try:
        conferir() if args.acao == 'conferir' else relatar()
    except (ValueError, OSError, KeyError) as error:
        print(str(error), file=sys.stderr)
        raise SystemExit(2)
