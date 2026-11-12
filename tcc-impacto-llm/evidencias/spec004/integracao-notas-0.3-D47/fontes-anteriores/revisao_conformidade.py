"""Revisao humana externa de capturas API; sem rede, chave ou alteracao de brutos."""
from datetime import datetime
from pathlib import Path

import avaliacao_ids as a
import coletor_piloto as base


def contexto(lote, avaliacoes, observacoes):
    lote, avaliacoes, observacoes = map(a.caminho_seguro, (lote, avaliacoes, observacoes))
    tracked = []
    def read(path):
        return a.json_estrito(a.ler(path, tracked))
    header = read(lote / 'lote.json')
    plan = read(lote / 'plano-original.json')
    if (header.get('interface') != 'Responses API'
            or (header.get('origem'), header.get('fase')) not in (
                ('real', 'piloto'), ('real', 'exploratoria'), ('sintetica', 'verificacao_sintetica'))
            or header['plano_sha256'] != a.sha((lote / 'plano-original.json').read_bytes())):
        raise ValueError('revisao requer lote API e plano integro')
    if header['fase'] == 'exploratoria' and (plan.get('etapa') != 'extensao-0.3-D41'
        or header.get('etapa') != plan['etapa'] or header.get('referencia_sha256') != plan['referencia_sha256']):
        raise ValueError('revisao exploratoria exige identidade da extensao')
    entries, plans = read(avaliacoes), read(observacoes)
    if not isinstance(entries, list) or not isinstance(plans, list):
        raise ValueError('listas explicitas requeridas')
    expected = {r['observacao_id']: r for r in plan['observacoes']}
    if len(plans) != len(expected) or {p['observacao_id'] for p in plans} != set(expected):
        raise ValueError('denominador deve preservar todas as observacoes planejadas')
    for p in plans:
        r = expected[p['observacao_id']]
        repeat = 'repeticao' if header['origem'] == 'real' else 'repeticao_sintetica'
        if (p['origem'] != header['origem'] or p['fase'] != header['fase']
                or p[repeat] != r['repeticao']
                or any(p[k] != r[k] for k in ('configuracao_id', 'mudanca', 'condicao', 'payload_sha256'))):
            raise ValueError('planejamento/origem/configuracao divergente')
    regs, signatures = [], []
    for entry in entries:
        path = a.relativo(avaliacoes.parent, entry['arquivo'])
        raw = a.ler(path, tracked)
        if a.sha(raw) != entry['sha256']:
            raise ValueError('hash da avaliacao divergente')
        reg = a.json_estrito(raw)
        oid = reg['observacao_id']
        if oid not in expected or any(r['observacao_id'] == oid for r in regs):
            raise ValueError('avaliacao ausente do plano ou duplicada; selecionar uma por observacao API')
        if (reg.get('completo') is not True or reg['origem'] != header['origem']
                or reg['fase'] != header['fase']):
            raise ValueError('avaliacao incompleta ou origem/fase divergente')
        planned = next(p for p in plans if p['observacao_id'] == oid)
        if a.identidade(planned) != a.identidade(reg) or planned['payload_sha256'] != reg['payload_sha256']:
            raise ValueError('identidade/payload da avaliacao diverge do planejamento')
        root = base.relativo(lote, oid + '/T01')
        attempt = base.conferir_fechamento(root)
        attempt_raw = a.ler(root / 'tentativa.json', tracked)
        closing_raw = a.ler(root / 'fechamento.json', tracked)
        if (a.ler(path.parent / 'tentativa-original.json', tracked) != attempt_raw
                or any(attempt[k] != reg[k] for k in ('observacao_id', 'tentativa_id', 'payload_sha256', 'resposta_sha256'))):
            raise ValueError('avaliacao nao corresponde a captura original')
        for file in base.inventariar(root):
            a.ler(base.relativo(root, file['arquivo']), tracked)
        regs.append(reg)
        signatures.append({'observacao_id': oid, 'avaliacao_sha256': a.sha(raw),
            'tentativa_sha256': a.sha(attempt_raw), 'fechamento_sha256': a.sha(closing_raw),
            'payload_sha256': reg['payload_sha256'], 'resposta_sha256': reg['resposta_sha256']})
    captured = {oid for oid in expected if base.relativo(lote, oid + '/T01').exists()}
    if {r['observacao_id'] for r in regs} != captured:
        raise ValueError('lista de avaliacoes deve preservar todas as capturas; excluir por decisao explicita')
    return {'lote': str(lote), 'avaliacoes': str(avaliacoes), 'observacoes': str(observacoes),
            'lote_header_sha256': a.sha((lote / 'lote.json').read_bytes()),
            'avaliacoes_sha256': a.sha(avaliacoes.read_bytes()),
            'observacoes_sha256': a.sha(observacoes.read_bytes()),
            'origem': header['origem'], 'fase': header['fase']}, regs, plans, signatures, tracked


def modelo(lote, avaliacoes, observacoes, saida):
    meta, _, _, signatures, tracked = contexto(lote, avaliacoes, observacoes)
    out = base.protegida(saida, 'avaliados')
    a.revalidar(tracked)
    base.salvar_json(out, {'versao': 'decisoes-conformidade-v1', 'fontes': meta,
        'responsavel': None, 'data': None,
        'observacoes': [{**item, 'decisao': 'pendente', 'justificativa': None} for item in signatures]})
    return out


def validar_decisoes(decisions, meta, signatures, regs):
    if decisions.get('versao') != 'decisoes-conformidade-v1' or decisions.get('fontes') != meta:
        raise ValueError('decisoes de outras fontes/origem/configuracao')
    if not a.texto(decisions.get('responsavel')) or not a.texto(decisions.get('data')):
        raise ValueError('revisao exige responsavel e data')
    try:
        date = datetime.fromisoformat(decisions['data'])
        if date.tzinfo is None or date.utcoffset() is None:
            raise ValueError('data da revisao deve conter fuso')
    except (ValueError, TypeError) as error:
        raise ValueError('data de revisao invalida; usar ISO 8601 com fuso') from error
    rows = decisions.get('observacoes')
    if not isinstance(rows, list) or len(rows) != len(signatures):
        raise ValueError('revisar explicitamente cada observacao disponivel')
    byid = {r['observacao_id']: r for r in rows}
    if len(byid) != len(rows) or set(byid) != {s['observacao_id'] for s in signatures}:
        raise ValueError('decisoes duplicadas/ausentes/nao planejadas')
    for signature, reg in zip(signatures, regs):
        row = byid[signature['observacao_id']]
        if any(row.get(k) != v for k, v in signature.items()):
            raise ValueError('decisao nao vincula os hashes atuais da observacao')
        if row.get('decisao') not in ('incluir', 'excluir', 'pendente') or not a.texto(row.get('justificativa')):
            raise ValueError('decisao e justificativa obrigatorias, inclusive pendente')
        if row['decisao'] == 'incluir' and (reg.get('desvios') or reg.get('conformidade_protocolo') == 'desvio'):
            raise ValueError('desvio registrado nao pode ser promovido a conforme por esta revisao; excluir')
    return byid


def registrar(decisoes, saida):
    decisions_path = a.caminho_seguro(decisoes)
    raw = decisions_path.read_bytes()
    decisions = a.json_estrito(raw)
    sources = decisions['fontes']
    meta, regs, _, signatures, tracked = contexto(sources['lote'], sources['avaliacoes'], sources['observacoes'])
    validar_decisoes(decisions, meta, signatures, regs)
    tracked.append((decisions_path, a.sha(raw)))
    a.revalidar(tracked)
    out = base.protegida(saida, 'avaliados')
    if out.exists():
        raise ValueError('revisao ja existe; usar arquivo novo')
    original_path = out.with_name(out.stem + '-decisoes-originais.json')
    base.salvar(original_path, raw)
    base.salvar_json(out, {'versao': 'revisao-conformidade-v1', 'decisoes_sha256': a.sha(raw),
                          'decisoes_arquivo': original_path.name, 'decisoes': decisions})
    return out


def resumir(revisao, saida):
    review_path = a.caminho_seguro(revisao)
    review_raw = review_path.read_bytes()
    review = a.json_estrito(review_raw)
    if review.get('versao') != 'revisao-conformidade-v1':
        raise ValueError('revisao incompatível')
    decisions = review['decisoes']
    original_path = a.relativo(review_path.parent, review['decisoes_arquivo'])
    original_raw = original_path.read_bytes()
    if a.sha(original_raw) != review['decisoes_sha256'] or a.json_estrito(original_raw) != decisions:
        raise ValueError('revisao difere da decisao original preservada')
    sources = decisions['fontes']
    meta, regs, plans, signatures, tracked = contexto(sources['lote'], sources['avaliacoes'], sources['observacoes'])
    byid = validar_decisoes(decisions, meta, signatures, regs)
    tracked.append((review_path, a.sha(review_raw)))
    tracked.append((original_path, a.sha(original_raw)))
    out = base.protegida(saida, 'avaliados')
    out = a.nova_saida(out, [review_path])
    a.salvar(out / 'revisao-original.json', review_raw, tracked)
    pending = [oid for oid, r in byid.items() if r['decisao'] == 'pendente']
    excluded = [oid for oid, r in byid.items() if r['decisao'] == 'excluir']
    included = [oid for oid, r in byid.items() if r['decisao'] == 'incluir']
    result = {'completo': False, 'origem': meta['origem'], 'fase': meta['fase'], 'celulas': [],
        'revisao_sha256': a.sha(review_raw), 'responsavel': decisions['responsavel'], 'data': decisions['data'],
        'incluidas': included, 'excluidas': [byid[oid] for oid in excluded], 'pendentes': pending,
        'N_planejado_original': len(plans), 'avaliacoes_originais': signatures,
        'limite': 'conformidade revisada nao altera validade/pontuacao nem os registros originais'}
    if pending:
        result['causa'] = 'revisao pendente; resumo controlado bloqueado'
        code = 2
    else:
        # Visao transitoria expressamente revisada. Nunca persistida como nova
        # avaliacao "conforme" nem usada para substituir os dados capturados.
        eligible = [{**r, 'conformidade_protocolo': 'conforme'} for r in regs if r['observacao_id'] in included]
        summary, code = a.resumir_registros(eligible, plans, origem=meta['origem'], fase=meta['fase'])
        result.update(summary)
        for cell in result['celulas']:
            key = (cell['configuracao_id'], cell['mudanca'], cell['condicao'])
            original_regs = [r for r in regs if a.identidade(r)[:3] == key]
            original_plans = [p for p in plans if a.identidade(p)[:3] == key]
            original, _ = a._grupo(original_regs, original_plans, False)
            cell['contagens_operacionais_originais'] = original['contagens']
            for group in cell['grupos']:
                ex = [byid[r['observacao_id']] for r in original_regs if r['observacao_id'] in excluded]
                group['exclusoes_conformidade'] = ex
                group['ausentes'] = [oid for oid in group['ausentes'] if oid not in excluded]
                group['N_planejado_original'] = len(original_plans)
                group['N_excluidas_conformidade'] = len(ex)
                group['denominador_metricas'] = 'respostas validas incluidas pela revisao; N planejado original preservado'
    return a.finalizar(out, result, code, tracked, 'resumo.json')[1]
