import copy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from unittest.mock import patch

from suporte_spec004 import ControleCase
import montagem_entradas as m

NAMES = ['sistema.txt','definicoes-comuns.md','requisitos-baseline.md',
         'catalogo-baseline.md','mudanca.md','pedido.txt','schema_saida.json']

class TestMontagem(ControleCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)

    def pacote(self, cond='D0', tag='p'):
        p=self.root/tag; p.mkdir()
        names=NAMES.copy()
        if cond in ('D1','E1'): names.insert(5,'notas.md')
        entries=[]
        for name in names:
            raw=({'pedido.txt':b'direto' if cond[0]=='D' else b'estruturado',
                  'notas.md':b'nota sintetica em rascunho\r\n'}.get(name,b'comum sintetico\r\n'))
            (p/name).write_bytes(raw)
            entries.append({'papel':name.split('.')[0], 'arquivo':name,'versao':'controle-1',
                            'sha256':hashlib.sha256(raw).hexdigest(),'tamanho_bytes':len(raw),
                            'revisao_conteudo':{'estado':'conferido_tecnicamente','responsavel':'controle sintetico','data':'2026-10-27'}})
        manifest={'versao_contrato':'spec004-v2','pacote_id':tag,'versao_pacote':'1',
          'configuracao_id':'controle-local-v1','mudanca':'MC-01','condicao':cond,
          'status':'RASCUNHO_PREPARACAO','liberado_para_pesquisa':False,
          'status_notas':'RASCUNHO_NAO_REVISADO' if cond in ('D1','E1') else 'ausentes',
          'origem_notas':'pesquisador' if cond in ('D1','E1') else 'ausentes','documentos':entries}
        self.gravar(p,manifest)
        return p,manifest

    def gravar(self,p,x): (p/'manifesto.json').write_text(json.dumps(x),encoding='utf-8')

    def preparar(self,p,out='out'):
        return m.preparar(p,p/'manifesto.json',self.root/out)

    def test_S14_condicoes_payload_literal(self):
        resultados=[]
        for cond in ('D0','D1','E0','E1'):
            p,manifest=self.pacote(cond,cond)
            r=self.preparar(p,'out'+cond); resultados.append(r)
            expected=b''
            for entry in manifest['documentos']:
                papel=entry['papel']
                expected+=f'<<<inicio:{papel}>>>\n'.encode()+(p/entry['arquivo']).read_bytes()+f'\n<<<fim:{papel}>>>\n'.encode()
            raw=(self.root/('out'+cond)/'payload.txt').read_bytes()
            self.checar('S-14','payload-'+cond,raw.hex(),expected.hex())
            self.checar('S-14','status-'+cond,[r['status'],r['liberado_para_pesquisa'],r['status_notas']],
                ['PREPARADO_LOCAL_NAO_ENVIADO',False,'RASCUNHO_NAO_REVISADO' if cond in ('D1','E1') else 'ausentes'])
            self.assertEqual(b'<<<inicio:notas>>>' in raw,cond in ('D1','E1'))
        self.checar('S-14','equivalencia-condicoes',m.conferir_condicoes(resultados),True)
        wrong=copy.deepcopy(resultados); wrong[3]['documentos'][5]['sha256']='0'*64
        with self.assertRaises(ValueError): m.conferir_condicoes(wrong)
        self.checar('S-14','nota-diferente-diagnosticada',True,True)

    def test_S14_manifestos_negativos(self):
        changes={
          'pendente':lambda x:x['documentos'][0]['revisao_conteudo'].update(estado='pendente'),
          'gabarito-ficticio-reprovado':lambda x:x['documentos'][0]['revisao_conteudo'].update(estado='reprovado'),
          'duplicado':lambda x:x['documentos'].append(copy.deepcopy(x['documentos'][0])),
          'hash':lambda x:x['documentos'][0].update(sha256='0'*64),
          'tamanho':lambda x:x['documentos'][0].update(tamanho_bytes=999),
          'versao':lambda x:x.update(versao_contrato=''),
          'condicao':lambda x:x.update(condicao='D2'),
          'liberacao':lambda x:x.update(liberado_para_pesquisa=True),
          'rascunho':lambda x:x.update(status_notas='APROVADO'),
          'absoluto':lambda x:x['documentos'][0].update(arquivo=str(self.root/'alheio')),
          'traversal':lambda x:x['documentos'][0].update(arquivo='../alheio'),
          'subdiretorio':lambda x:x['documentos'][0].update(arquivo='p/sistema.txt')}
        for i,(name,change) in enumerate(changes.items()):
            with self.subTest(caso=name):
                p,x=self.pacote(tag='p'+str(i)); change(x); self.gravar(p,x)
                with self.assertRaises(ValueError): self.preparar(p,'out'+str(i))
                self.checar('S-14',name,True,True)
        for i,case in enumerate(['extra','ausente','nota-D0','nota-ausente-D1']):
            p,x=self.pacote('D1' if i==3 else 'D0','files'+str(i))
            if case=='ausente': (p/'sistema.txt').unlink()
            elif case=='nota-ausente-D1': (p/'notas.md').unlink()
            else: (p/('notas.md' if case=='nota-D0' else 'extra.txt')).write_text('ficticio')
            with self.assertRaises(ValueError): self.preparar(p,'filesout'+str(i))
            self.checar('S-14',case,True,True)

    def test_S14_links_internos_externos_junction_real(self):
        # Real junctions test logical path rejection, never OS identity isolation.
        if os.name!='nt': self.skipTest('junction Windows')
        for mode in ('interno','externo'):
            p,x=self.pacote(tag='link'+mode)
            target=p/'alvo' if mode=='interno' else self.root/'externo'
            target.mkdir(); (target/'sentinela.txt').write_text('SENTINELA FICTICIA')
            link=p/'atalho'
            cp=subprocess.run(['cmd','/c','mklink','/J',str(link),str(target)],capture_output=True)
            self.assertEqual(cp.returncode,0,cp.stderr)
            try:
                with self.assertRaises(ValueError): m.sem_links(link)
                with self.assertRaises(ValueError): self.preparar(p,'linkout'+mode)
                self.checar('S-14','junction-real-'+mode,True,True)
            finally:
                link.rmdir()  # Removes the verified temporary junction only, never its target.
        p,_=self.pacote(tag='linkmock')
        with patch.object(m,'reparse',return_value=True):
            with self.assertRaises(ValueError): m.sem_links(p)
        self.checar('S-14','bit-reparse-logico',True,True)

    def test_S13_integridade_fechamento_e_pastas(self):
        p,_=self.pacote(); self.preparar(p)
        with self.assertRaises(ValueError): self.preparar(p)
        with self.assertRaises(ValueError): m.preparar(p,p/'manifesto.json',p/'saida')
        p2,_=self.pacote(tag='p2'); original=m.revalidar
        def altera(entries):
            (p2/'sistema.txt').write_bytes(b'alterado')
            return original(entries)
        with patch.object(m,'revalidar',side_effect=altera):
            with self.assertRaises(ValueError): self.preparar(p2,'out2')
        blocked=json.loads((self.root/'out2/preparacao.json').read_text())
        self.checar('S-13','montagem-sem-falso-fechamento',[blocked['completo'],blocked['status']],[False,'BLOQUEADO'])

    def test_S14_cli(self):
        p,_=self.pacote(); root=Path(__file__).resolve().parents[1]
        args=[sys.executable,'-B',str(root/'montagem_entradas.py'),'--pacote',str(p),
              '--manifesto',str(p/'manifesto.json'),'--saida',str(self.root/'cli')]
        cp=subprocess.run(args,capture_output=True)
        self.checar('S-14','cli-local',cp.returncode,0)
        cp=subprocess.run(args,capture_output=True)
        self.checar('S-13','cli-pasta-repetida',cp.returncode,2)
