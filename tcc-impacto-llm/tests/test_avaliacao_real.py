"""Controles artificiais do contrato de importacao real; nenhuma resposta de LLM.

Metadados 'real' sao simulados apenas em temporarios para exercitar esse ramo.
Esses controles nunca pertencem ao piloto ou aos dados reais.
"""
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import avaliacao_ids as a
import montagem_entradas as m
import test_avaliacao_ids as controles


class TestImportacaoReal(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.ref = copy.deepcopy(controles.ESPERADOS['referencia'])

    def entrada(self, content=b'{"requisitos":["RF-02"],"testes":["T04","T12"]}', technical=False):
        controles.TestAvaliacao.entrada(self, content, technical)
        t = json.loads(self.attempt.read_bytes())
        t.pop('repeticao_sintetica')
        t.update(origem='real', fase='piloto', repeticao=1,
                 origem_resposta='CONTROLE ARTIFICIAL do importador, sem chamada',
                 instante_execucao='2026-11-06T00:00:00Z', modelo_reportado='modelo-ficticio-controle',
                 configuracao={'modalidade':'controle-local'}, versoes={'pacote':'controle'},
                 conformidade_protocolo='conforme', desvios=[],
                 entrada_enviada_arquivo='enviada.bin')
        payload = (self.prepdir/'payload.txt').read_bytes()
        (self.root/'enviada.bin').write_bytes(payload)
        t['entrada_enviada_sha256'] = a.sha(payload)
        self.attempt.write_bytes(a.serial(t))
        return t

    def avaliar(self, name='out'):
        return a.avaliar(self.prep, self.attempt, self.refpath, self.root/name, origem='real', fase='piloto')

    def planned(self, r):
        return [{k:r[k] for k in ('origem','fase','observacao_id','configuracao_id',
                                 'mudanca','condicao','repeticao','payload_sha256')}]

    def test_originais_proveniencia_cli_e_diretorio_externo(self):
        self.entrada()
        script = Path(a.__file__).resolve()
        cp = subprocess.run([sys.executable, '-B', str(script), 'avaliar', '--origem', 'real',
                             '--fase', 'piloto', '--preparacao', str(self.prep), '--tentativa',
                             str(self.attempt), '--referencia', str(self.refpath), '--saida',
                             str(self.root/'out')], cwd=self.root, capture_output=True)
        self.assertEqual(cp.returncode, 0, cp.stderr.decode())
        r = json.loads((self.root/'out/avaliacao.json').read_bytes())
        self.assertEqual((r['origem'],r['fase'],r['repeticao']), ('real','piloto',1))
        self.assertNotIn('repeticao_sintetica', r)
        for src, dst in [('resposta.bin','resposta-original.bin'),('enviada.bin','entrada-enviada-original.bin'),
                         ('tentativa.json','tentativa-original.json')]:
            self.assertEqual((self.root/src).read_bytes(), (self.root/'out'/dst).read_bytes())
        manifest = json.loads((self.root/'out/manifesto.json').read_bytes())
        self.assertEqual((manifest['origem'],manifest['fase']), ('real','piloto'))
        summary, code = a.resumir_registros([r], self.planned(r), origem='real', fase='piloto')
        self.assertEqual(code,0)
        self.assertEqual(summary['celulas'][0]['grupos'][0]['contagens']['V'],1)
        (self.root/'lista.json').write_bytes(a.serial([{'arquivo':'out/avaliacao.json',
            'sha256':a.sha((self.root/'out/avaliacao.json').read_bytes())}]))
        (self.root/'planejadas.json').write_bytes(a.serial(self.planned(r)))
        cp = subprocess.run([sys.executable, '-B', str(script), 'resumir', '--origem', 'real',
                             '--fase', 'piloto', '--avaliacoes', 'lista.json', '--observacoes',
                             'planejadas.json', '--saida', 'resumo'], cwd=self.root, capture_output=True)
        self.assertEqual(cp.returncode,0,cp.stderr.decode())
        saved=json.loads((self.root/'resumo/manifesto.json').read_bytes())
        self.assertEqual((saved['origem'],saved['fase']),('real','piloto'))

    def test_invalida_vazia_e_tecnica_distintas(self):
        base = self.root
        for idx, (content, technical, expected) in enumerate([
            (b'nao e JSON\r\n',False,'resposta_formato_invalido'),
            (b'{"requisitos":[],"testes":[]}',False,'avaliada'),
            (None,True,'falha_tecnica')]):
            self.root=base/str(idx);self.root.mkdir()
            t=self.entrada(content,technical)
            if technical:
                t.update(entrada_enviada_arquivo=None,entrada_enviada_sha256=None)
                self.attempt.write_bytes(a.serial(t))
            r, code = self.avaliar()
            self.assertEqual(r['status_avaliacao'],expected)
            self.assertEqual(code,0 if expected=='avaliada' else 1)
            if expected=='avaliada':
                self.assertEqual(r['testes']['S'],[])
                self.assertEqual(r['testes']['metricas_propostas']['revocacao']['fracao'],'0')
            else:self.assertIsNone(r['testes'])
            summary,_=a.resumir_registros([r],self.planned(r),True,origem='real',fase='piloto')
            group=summary['celulas'][0]['grupos'][0]
            self.assertEqual(group['contagens']['I'],int(expected=='resposta_formato_invalido'))
            self.assertEqual(group['contagens']['T'],int(technical))
            self.assertEqual(len(group['imputacoes']),int(expected=='resposta_formato_invalido'))
        self.root=base

    def test_modelo_nao_reportado_permanece_nulo_com_causa(self):
        t = self.entrada()
        t.update(modelo_reportado=None, modelo_reportado_indisponibilidade='CONTROLE: CLI nao expoe modelo efetivo')
        self.attempt.write_bytes(a.serial(t))
        result, code = self.avaliar()
        self.assertEqual(code, 0)
        self.assertIsNone(result['modelo_reportado'])
        self.assertEqual(result['modelo_reportado_indisponibilidade'], t['modelo_reportado_indisponibilidade'])
        del t['modelo_reportado_indisponibilidade']
        self.attempt.write_bytes(a.serial(t))
        result, code = self.avaliar('sem-causa')
        self.assertEqual(code, 2)

    def test_mistura_origem_fase_e_versoes_bloqueada(self):
        self.entrada();r,_=self.avaliar()
        with self.assertRaises(ValueError):a.resumir_registros([r],self.planned(r))
        with self.assertRaises(ValueError):a.resumir_registros([r],self.planned(r),origem='real',fase='principal')
        for field in ('configuracao','versoes'):
            other=copy.deepcopy(r)
            other.update(observacao_id='obs-2',tentativa_id='tent-2',avaliacao_id='ava-2',repeticao=2)
            other[field]['nova']='alterada'
            result,code=a.resumir_registros([r,other],self.planned(r)+self.planned(other),origem='real',fase='piloto')
            self.assertEqual(code,2)
            self.assertEqual(result['celulas'][0]['diagnosticos'],['versoes_distintas'])

    def test_desvio_preservado_sem_resumo_controlado(self):
        t=self.entrada()
        effective=b'prefixo IDE\n'+(self.root/'enviada.bin').read_bytes()
        (self.root/'enviada.bin').write_bytes(effective)
        t['entrada_enviada_sha256']=a.sha(effective);self.attempt.write_bytes(a.serial(t))
        r,code=self.avaliar('nao-declarado');self.assertEqual(code,2)
        t.update(conformidade_protocolo='desvio',desvios=['prefixo adicional'])
        self.attempt.write_bytes(a.serial(t));r,code=self.avaliar('declarado')
        self.assertEqual(code,0)
        self.assertEqual((self.root/'declarado/entrada-enviada-original.bin').read_bytes(),effective)
        summary,code=a.resumir_registros([r],self.planned(r),origem='real',fase='piloto')
        self.assertEqual(code,2)
        self.assertEqual(summary['celulas'][0]['grupos'],[])

    def test_real_recusada_no_modo_sintetico_e_hash_adulterado(self):
        t=self.entrada()
        r,code=a.avaliar(self.prep,self.attempt,self.refpath,self.root/'sintetico')
        self.assertEqual(code,2)
        t['resposta_sha256']='hash-adulterado';self.attempt.write_bytes(a.serial(t))
        r,code=self.avaliar();self.assertEqual(code,2)
        self.assertFalse(r['completo'])
        self.assertIsNone(r['testes'])

    def test_caminhos_locais_com_pai_sem_relaxar_declarados(self):
        child=self.root/'child';child.mkdir()
        self.assertEqual(a.caminho_seguro(child/'..'),self.root)
        self.assertEqual(m.sem_links(child/'..'),self.root)
        with self.assertRaises(ValueError):a.relativo(child,'../resposta.bin')
