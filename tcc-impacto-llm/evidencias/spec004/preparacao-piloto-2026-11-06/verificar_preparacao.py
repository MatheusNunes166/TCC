"""Conferencia documental e montagem offline D35. Nao executa bancada nem LLM.

Uso da raiz ou de outro cwd: python -B <este-arquivo> --saida <pasta-nova>
Saida e exclusiva; nao sobrescreve evidencias de execucoes anteriores.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
import fontes_autorizadas as fontes
import montagem_entradas as montagem


def sha(data):
    return hashlib.sha256(data).hexdigest()


def table(text):
    return [[c.strip() for c in line.strip('|').split('|')]
            for line in text.splitlines() if re.match(r'^\| T\d\d \|', line)]


def output(value):
    decision, reason = value.split('/')
    return {'decisao': {'P':'permitir','N':'negar'}[decision],
            'motivo': {'direta':'permissao_direta','herdada':'permissao_herdada',
                       'sem':'sem_permissao','sem permissão':'sem_permissao',
                       'estado':'estado','conflito':'conflito'}[reason]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--saida', type=Path, required=True)
    args = parser.parse_args()
    out = args.saida.resolve()
    if out.exists():
        raise ValueError('saida deve ser nova')
    out.mkdir(parents=True)
    refpath = ROOT/'materiais/modelos/referencia_candidata_NAO_ENVIAR_AO_LLM.json'
    reference = json.loads(refpath.read_bytes())
    material = (ROOT/'materiais/02_REQUISITOS_TESTES_E_REFERENCIA.md').read_text(encoding='utf-8')
    details = (ROOT/'documentacao/referencia-candidata-proxima-etapa.md').read_text(encoding='utf-8')
    matrix = table(material.split('### Matriz de resultados esperados das quatro variantes')[1])
    assert len(matrix) == 12
    baseline = {r[0]:output(r[1]) for r in matrix}
    selection_report = []
    for i, change in enumerate(reference['mudancas']):
        expected = {r[0]:output(r[i+2]) for r in matrix}
        assert expected == change['expected']
        selected = set(change['tests'])
        changed = {t for t in selected if expected[t] != baseline[t]}
        preserved = selected - changed
        assert changed == set(change['changed'])
        assert preserved == set(change['preserved'])
        section = details.split('## '+change['id']+' — ')[1].split('\n## ')[0]
        justifications = table(section)
        assert len(justifications) == 12
        assert {r[0]:output(r[1]) for r in justifications} == expected
        assert {r[0] for r in justifications if r[2].startswith('Incluir')} == selected
        for row in justifications:
            if row[0] in selected:
                assert ('preservação' in row[2]) == (row[0] in preserved)
        selection_report.append({'mudanca':change['id'],'requisitos':change['rfs'],
                                 'mudanca_comportamento':sorted(changed),'preservacao':sorted(preserved)})
    # Check catalogue inputs and outcomes across all three documents and payload.
    material_catalog = table(material.split('## 2.2 ')[1].split('\n## ')[0])
    detailed_catalog = table(details.split('## Catálogo preservado')[1].split('\n## ')[0])
    docs,_ = fontes.reunir_fontes(ROOT,'MC-01','D0')
    catalog = table(docs['catalogo-baseline.md'].decode('utf-8'))
    assert len(catalog) == len(material_catalog) == len(detailed_catalog) == 12
    for canonical, short, detailed in zip(catalog, material_catalog, detailed_catalog):
        norm = lambda s:s.lower().replace('em revisão','em_revisao')
        assert list(map(norm,canonical[:4])) == list(map(norm,short[:4])) == list(map(norm,detailed[:4]))
        assert {'decisao':canonical[4],'motivo':canonical[5]} == baseline[canonical[0]] == output(short[4]) == output(detailed[4])
    records = fontes.exportar(ROOT, out/'recortes')
    assert len(records) == 16
    prepared = []
    package_report = []
    for record in records:
        package = out/'recortes'/record['pacote']
        authorization = out/'recortes'/record['autorizacao']
        dest = out/'preparados'/record['id']
        result = montagem.preparar(package,package/'manifesto.json',dest,authorization)
        prepared.append(result)
        docs,provenance = fontes.reunir_fontes(ROOT,result['mudanca'],result['condicao'])
        expected_names = set(montagem.NOMES) | ({'notas.md'} if result['condicao'].endswith('1') else set())
        assert set(docs) == expected_names
        for name,data in docs.items():
            assert (dest/'documentos'/name).read_bytes() == data
        payload = (dest/'payload.txt').read_bytes()
        expected_payload = b''.join(f'<<<inicio:{e["papel"]}>>>\n'.encode()+docs[e['arquivo']]+f'\n<<<fim:{e["papel"]}>>>\n'.encode() for e in result['documentos'])
        assert payload == expected_payload
        assert all(x.encode() not in payload for x in ['CANDIDATO_NAO_REVISADO','"expected"','"changed"',
                  'Regressão candidata','def autorizar','D-34','recuperacao-sessoes','TP/FP/FN'])
        # Baseline outcomes are permitted; correct selection/variant outcomes are not.
        package_report.append({'id':record['id'],'payload_sha256':sha(payload),'bytes':len(payload),
                               'notas': 'notas.md' in docs,'fontes':provenance})
    assert montagem.conferir_condicoes(prepared)
    # Compare factual common excerpts to pre-D35 originals in Git, without modifying sources.
    prefix = subprocess.check_output(['git','rev-parse','--show-prefix'],cwd=ROOT,text=True).strip()
    old = lambda name:subprocess.check_output(['git','show','HEAD:'+prefix+name],cwd=ROOT)
    normalize = lambda data:data.replace(b'\r\n',b'\n')
    assert normalize(docs['requisitos-baseline.md']) == normalize(fontes.secao(old('documentacao/requisitos.md'),
                   '## Entradas e saídas','## Situação da baseline completa e do incremento 1'))
    assert normalize(docs['definicoes-comuns.md']) == normalize(old('materiais/07_DEFINICOES_COMUNS.md'))
    assert normalize(docs['schema_saida.json']) == normalize(old('materiais/modelos/schema_saida.json'))
    assert normalize(refpath.read_bytes()) == normalize(old(refpath.relative_to(ROOT).as_posix()))
    old_cat = old('documentacao/qualidade-e-testes.md').decode('utf-8')
    assert [r[:6] for r in table(old_cat.split('## Doze casos da baseline')[1].split('\n## ')[0])] == catalog
    protected = ['autorizacao.py','variantes','tests/test_autorizacao.py','verificacao_variantes.py',
                 'materiais/modelos/referencia_candidata_NAO_ENVIAR_AO_LLM.json','materiais/07_DEFINICOES_COMUNS.md',
                 'materiais/modelos/manifesto_congelamento.json','specs/003-mudancas-controladas/spec.md']
    assert not subprocess.check_output(['git','diff','HEAD','--name-only','--',*protected],cwd=ROOT)
    # Exercise order determinism using artificial seeds; no pilot seed is chosen.
    order_path = ROOT/'materiais/modelos/ordenar_piloto.py'
    spec = importlib.util.spec_from_file_location('ordem_piloto',order_path)
    module = importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    plan = json.loads((ROOT/'materiais/modelos/plano_piloto.json').read_bytes())
    first = module.ordenar(plan,17)
    assert first == module.ordenar(plan,17)
    assert first['observacoes'] != module.ordenar(plan,18)['observacoes']
    assert plan['semente_ordem'] is None and all(r['ordem'] is None for r in plan['observacoes'])
    assert [r['ordem'] for r in first['observacoes']] == list(range(1,17))
    result = {'status':'CONFERIDO_OFFLINE','chamadas_realizadas':0,'python':sys.version,
              'origem':'verificacao_documental_e_montagem','pacotes':package_report,
              'documentos_comuns_equivalentes':True,'notas_iguais_nos_oito_pacotes':True,
              'catalogo_baseline_conferido':12,'expectativas_conferidas_documentalmente':48,
              'selecao_preservada':selection_report,'referencia_sha256':sha(refpath.read_bytes()),
              'divergencias_substantivas_encontradas':[],
              'ordenacao_controles_artificiais':[17,18],'semente_piloto_escolhida':False,
              'aprovacao_individual_expectativas_inferida':False}
    (out/'verificacao.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('16 pacotes, 12 entradas baseline, 48 expectativas documentais e particoes conferidos; zero chamadas.')


if __name__ == '__main__':
    main()
