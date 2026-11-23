"""Conferências técnicas do recorte operacional. Zero chamadas LLM."""
import collections
import copy
import itertools
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import autorizacao
from variantes import mc01,mc02,mc03,mc04
import preparar_documentacao_operacional as prep


def tabela(text):
    rows=[[part.strip() for part in line.split('|')[1:-1]]
          for line in text.splitlines() if line.startswith('|')]
    return rows[2:]


def fatos_declarados(docs):
    """Extrai valores dos documentos realmente montados, sem gabarito privado."""
    own={role:(set() if value=='nenhuma' else {value})
         for role,value in tabela(docs['02-cadastro-de-papeis.md'])}
    inheritance={a:{b} for a,b in tabela(docs['03-configuracao-de-heranca.md'])}
    conflicts=[{a,b} for a,b in tabela(docs['04-configuracao-de-incompatibilidades.md'])]
    returns=[(int(rank),condition,{'decisao':decision,'motivo':reason})
             for rank,condition,decision,reason in tabela(docs['05-contrato-de-execucao.md'])]
    return own,inheritance,conflicts,sorted(returns)


def retorno_declarativo(facts,state,roles,operation):
    own,inheritance,conflicts,returns=facts
    included=set().union(*(inheritance.get(r,set()) for r in roles))
    effective=set(roles)|included
    granted=lambda group:any(operation in own[r] for r in group)
    satisfied={
      'estado diferente de ativa':state!='ativa',
      'existe incompatibilidade no conjunto efetivo':any(pair<=effective for pair in conflicts),
      'operação possui concessão direta':granted(roles),
      'operação possui concessão herdada':granted(included),
      'nenhuma condição anterior satisfeita':True}
    return next(value for _,condition,value in returns if satisfied[condition])


class TestDocumentacaoOperacional(unittest.TestCase):
    def test_substituicao_somente_do_bloco_rf_e_catalogo_completo(self):
        payloads,sources,docs=prep.montar()
        self.assertEqual(len(docs),5)
        for change,condition in itertools.product(prep.MUDANCAS,prep.CONDICOES):
            a=payloads[f'{change}-{condition}-CONSOLIDADA']
            b=payloads[f'{change}-{condition}-OPERACIONAL']
            self.assertEqual(prep.sha(a),sources[f'{change}:{condition}']['payload_origem_sha256'])
            text=a.decode();match=prep.RF.search(text)
            newtext=b.decode();first=newtext.index('<<<inicio:01-especificacao-funcional>>>')
            last=newtext.index('<<<fim:05-contrato-de-execucao>>>')+len('<<<fim:05-contrato-de-execucao>>>')
            self.assertEqual(text[:match.start()],newtext[:first])
            self.assertEqual(text[match.end():],newtext[last:])
            original=dict(prep.BLOCOS.findall(text));modified=dict(prep.BLOCOS.findall(newtext))
            for name,content in original.items():
                if name!='requisitos-baseline':self.assertEqual(content,modified[name],name)
            catalog=modified['catalogo-baseline']
            self.assertIn('Decisão esperada',catalog);self.assertIn('Motivo esperado',catalog)
            self.assertEqual(len(tabela(catalog)),15)
            self.assertNotIn('requisitos-baseline',modified)
        joined='\n'.join(docs.values())
        for hint in ('herda visualizar','Não herda exportar','inclusive se Consulta vier da herança','T07','T12','MC-04'):
            self.assertNotIn(hint,joined)

    def test_fatos_declarados_sustentam_240_decisoes_motivos(self):
        _,_,docs=prep.montar();facts=fatos_declarados(docs)
        self.assertEqual({r[0] for r in tabela(docs['01-especificacao-funcional.md'])},
                         {'RF-01','RF-02','RF-03','RF-04'})
        roles=list(facts[0]);groups=[frozenset(r for r,on in zip(roles,bits) if on)
                                   for bits in itertools.product((False,True),repeat=3)]
        implementations={'BASELINE':autorizacao.autorizar,'MC-01':mc01.autorizar,
                         'MC-02':mc02.autorizar,'MC-03':mc03.autorizar,'MC-04-v2':mc04.autorizar}
        count=0
        for change,implementation in implementations.items():
            configured=copy.deepcopy(facts)
            if change=='MC-01':configured[0]['Auditoria'].remove('exportar')
            if change=='MC-02':configured[2].clear()
            if change=='MC-03':configured[0]['Consulta'].remove('visualizar')
            if change=='MC-04-v2':configured[1].clear()
            for state,group,operation in itertools.product(('ativa','suspensa','em_revisao'),groups,('visualizar','exportar')):
                with self.subTest(versao=change,estado=state,papeis=group,operacao=operation):
                    self.assertEqual(retorno_declarativo(configured,state,group,operation),implementation(state,group,operation))
                count+=1
        self.assertEqual(count,240)

    def test_fatos_de_domino_niveis_precedencia_e_ids_preservados(self):
        payloads,_,docs=prep.montar();source=prep.RF.search(payloads['MC-02-D0-CONSOLIDADA'].decode())[2]
        self.assertIn(source.split('## Regras e aceitação planejada')[0].strip(),docs['01-especificacao-funcional.md'])
        self.assertIn('A expansão possui um nível',docs['03-configuracao-de-heranca.md'])
        self.assertIn('Não há expansão multinível nem ciclos',docs['03-configuracao-de-heranca.md'])
        self.assertIn('O conjunto efetivo',docs['02-cadastro-de-papeis.md'])
        self.assertIn('papéis efetivos',docs['04-configuracao-de-incompatibilidades.md'])
        returns=fatos_declarados(docs)[3]
        self.assertEqual([v['motivo'] for _,_,v in returns],
                         ['estado','conflito','permissao_direta','permissao_herdada','sem_permissao'])

    def test_balanceamento_notas_modelos_e_ordem_reproduzivel(self):
        payloads,sources,_=prep.montar();plan=prep.plano(payloads,sources);rows=plan['observacoes']
        self.assertEqual(len(rows),32)
        self.assertEqual(len({r['observacao_id'] for r in rows}),32)
        counts=collections.Counter((r['mudanca'],r['condicao'],r['documentacao_id'],r['modelo_solicitado']) for r in rows)
        self.assertEqual(len(counts),16);self.assertEqual(set(counts.values()),{2})
        self.assertEqual(collections.Counter(r['bloco'] for r in rows),{1:16,2:16})
        for change,level in itertools.product(prep.MUDANCAS,prep.DOCUMENTACOES):
            a=dict(prep.BLOCOS.findall(payloads[f'{change}-D0-{level}'].decode()))
            b=dict(prep.BLOCOS.findall(payloads[f'{change}-D1-{level}'].decode()))
            self.assertNotIn('notas',a);self.assertIn('notas',b)
            for name,content in a.items():self.assertEqual(content,b[name])
            original=dict(prep.BLOCOS.findall(payloads[f'{change}-D1-CONSOLIDADA'].decode()))
            self.assertEqual(b['notas'],original['notas'])
        self.assertEqual(plan,prep.plano(payloads,sources))
        self.assertFalse(plan['envio_autorizado'])

    def test_preparacao_sem_chave_referencia_privada_ou_transporte(self):
        read=Path.read_bytes
        def guarded(path):
            self.assertNotIn('NAO_ENVIAR_AO_LLM',path.name)
            return read(path)
        with tempfile.TemporaryDirectory() as temp,patch.object(Path,'read_bytes',guarded), \
             patch('coletor_api.enviar',side_effect=AssertionError('rede proibida')), \
             patch('coletor_api.chave_api',side_effect=AssertionError('chave proibida')):
            folder=Path(temp)/'preparado';result=prep.preparar(folder)
            self.assertEqual(result['documentos_operacionais'],5)
            self.assertEqual(result['chamadas_executadas'],0)
            self.assertEqual(prep.conferir(folder),result)
            with self.assertRaises(ValueError):prep.preparar(folder)
            file=folder/'documentos-operacionais/02-cadastro-de-papeis.md'
            file.write_text(file.read_text().replace('visualizar','exportar'))
            with self.assertRaisesRegex(ValueError,'Bytes divergentes'):prep.conferir(folder)

    def test_rejeita_origem_fora_de_versao_e_promocao_do_plano(self):
        payloads,_,_=prep.montar();payload=payloads['MC-02-D0-CONSOLIDADA']
        with self.assertRaises(ValueError):prep.operacionalizar(payload+payload)
        with self.assertRaises(ValueError):prep.operacionalizar(payload.replace(b'Consulta concede visualizar',b'Consulta concede exportar'))
        with tempfile.TemporaryDirectory() as temp:
            folder=Path(temp)/'pacote';prep.preparar(folder)
            plan=prep.ler(folder/'plano.json');plan['envio_autorizado']=True
            (folder/'plano.json').write_bytes(prep.serial(plan))
            meta=prep.ler(folder/'manifesto.json');meta['arquivos']['plano.json']=prep.sha((folder/'plano.json').read_bytes())
            (folder/'manifesto.json').write_bytes(prep.serial(meta))
            with self.assertRaises(ValueError):prep.conferir(folder)


if __name__=='__main__':unittest.main()
