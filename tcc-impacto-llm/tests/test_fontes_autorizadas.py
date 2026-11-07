"""Verifica recortes autorizados, sem avaliador nem referencia de selecao."""
import hashlib
import json
from pathlib import Path
import tempfile
from unittest.mock import patch

from suporte_spec004 import ControleCase
import fontes_autorizadas as f
import montagem_entradas as m

class TestFontes(ControleCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name);self.repo=self.root/'repo'
        samples={
          'materiais/04_NOTAS_E_PROMPTS.md':'''PROIBIDO_HISTORICO
## 4.2 Nota candidata única, comum a todas as mudanças
> Nota de controle literal, rascunho.
## 4.3 Como preparar e revisar as notas
PROIBIDO_GABARITO
## 4.4 Pacote comum — montagem futura
1. Mensagem de sistema: responda somente com os IDs.
## 4.5 Pedido direto — D0 e D1
> Selecione IDs.
## 4.6 Pedido estruturado — E0 e E1
> Examine e selecione IDs.
## 4.7 Contrato de saída
PROIBIDO_RESULTADOS
''',
          'materiais/07_DEFINICOES_COMUNS.md':'Definicoes comuns sem exemplos resolvidos.\r\n',
          'documentacao/requisitos.md':'''PROIBIDO_HISTORICO
## Entradas e saídas
Entrada e saida da baseline.
## Regras e aceitação planejada
RF-01 e RF-02 e RF-03 e RF-04.
## Ordem global
Precedencia.
## Situação da baseline completa e do incremento 1
PROIBIDO_RESULTADOS
''',
          'documentacao/qualidade-e-testes.md':'''PROIBIDO_RESULTADOS
## Doze casos da baseline
| ID | Estado | Papeis | Operacao | Decisao | Motivo | Destaques |
|---|---|---|---|---|---|---|
| T01 | ativa | Consulta | visualizar | permitir | permissao_direta | PROIBIDO_PISTA |
## Variantes e avaliação futura
PROIBIDO_GABARITO
''',
          'specs/003-mudancas-controladas/spec.md':'''PROIBIDO_HISTORICO
### Mudanças e regras de origem
| MC-01 | MC-01 | Retirar concessao. | PROIBIDO_RESULTADO |
| MC-02 | MC-02 | Retirar conflito. | PROIBIDO_RESULTADO |
| MC-03 | MC-03 | Retirar outra concessao. | PROIBIDO_RESULTADO |
| MC-04 | MC-04-v2 | Retirar heranca. | PROIBIDO_RESULTADO |
### Fontes de aceitação e rastreabilidade
PROIBIDO_GABARITO
''',
          'materiais/modelos/schema_saida.json':'{"type":"object"}\n'}
        for name,value in samples.items():
            p=self.repo/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(value.encode())

    def test_S14_recortes_sem_conteudo_proibido(self):
        for change in ['MC-01','MC-02','MC-03','MC-04-v2']:
            docs,sources=f.reunir_fontes(self.repo,change,'D1')
            self.checar('S-14','sem-proibidos-'+change,any(b'PROIBIDO_' in value for value in docs.values()),False)
            self.assertEqual(docs['notas.md'],b'> Nota de controle literal, rascunho.\n')
            self.assertEqual(len(sources),6)
            self.assertEqual(len(docs),8)
        docs,_=f.reunir_fontes(self.repo,'MC-01','D0')
        self.checar('S-14','sem-nota-D0','notas.md' in docs,False)

    def test_S14_somente_seis_fontes_abertas(self):
        visited=[];original=Path.read_bytes
        def spy(path):
            visited.append(path.relative_to(self.repo).as_posix());return original(path)
        with patch.object(Path,'read_bytes',spy):f.reunir_fontes(self.repo,'MC-01','E1')
        self.checar('S-14','fontes-abertas',sorted(visited),sorted(f.FONTES))

    def test_S14_marcador_duplicado_bloqueia_recorte(self):
        p=self.repo/'documentacao/requisitos.md'
        p.write_bytes(p.read_bytes()+b'\n## Entradas e sa\xc3\xaddas\n')
        with self.assertRaises(ValueError):f.reunir_fontes(self.repo,'MC-01','D0')
        self.checar('S-14','seletor-ambiguo-bloqueado',True,True)

    def test_S14_exportacao_autorizacao_e_texto_exato(self):
        output=self.root/'editorial'
        records=f.exportar(self.repo,output,configuracao_id='controle-configuracao-explicita')
        self.assertEqual(len(records),16)
        prepared=[]
        for r in records:
            p=output/r['pacote'];auth=output/r['autorizacao']
            result=m.preparar(p,p/'manifesto.json',self.root/'preparados'/r['id'],auth)
            self.assertEqual(result['configuracao_id'],'controle-configuracao-explicita')
            delivery=json.loads((self.root/'preparados'/r['id']/'entrega-textual.json').read_bytes())
            data=(self.root/'preparados'/r['id']/'payload.txt').read_bytes()
            self.checar('S-14','entrega-'+r['id'],[delivery['ferramentas'],delivery['envio_realizado'],delivery['payload_sha256']],[[],False,hashlib.sha256(data).hexdigest()])
            self.assertNotIn(b'PROIBIDO_',data)
            self.assertNotIn(b'autorizacao_sha256',data)
            prepared.append(result)
        self.checar('S-14','dezesseis-controles-comuns',m.conferir_condicoes(prepared),True)

    def test_normalizacao_antes_dos_hashes_sem_alterar_fontes(self):
        source=self.repo/'materiais/07_DEFINICOES_COMUNS.md'
        original=b'\xef\xbb\xbf  definicoes\r\nlinha\rfinal  \n'
        source.write_bytes(original)
        output=self.root/'normalizados'
        f.exportar(self.repo,output)
        expected=b'  definicoes\nlinha\nfinal  \n'
        package=output/'pacotes/MC-01-D0'
        manifest=json.loads((package/'manifesto.json').read_bytes())
        entry=next(e for e in manifest['documentos'] if e['arquivo']=='definicoes-comuns.md')
        self.assertEqual((package/'definicoes-comuns.md').read_bytes(),expected)
        self.assertEqual(entry['sha256'],hashlib.sha256(expected).hexdigest())
        self.assertEqual(entry['tamanho_bytes'],len(expected))
        self.assertEqual(entry['recorte_antes_normalizacao'],{
            'sha256':hashlib.sha256(original).hexdigest(),'tamanho_bytes':len(original)})
        self.assertEqual(source.read_bytes(),original)
        self.assertEqual((output/'fontes-originais/materiais/07_DEFINICOES_COMUNS.md').read_bytes(),original)
        self.assertEqual(f.normalizar_documento(expected),expected)
        # Mesmo com hashes/autorizacao refeitos, declarar LF nao aceita CRLF.
        bad=b'  definicoes\r\nlinha\r\nfinal  \r\n'
        (package/'definicoes-comuns.md').write_bytes(bad)
        entry.update(sha256=f.sha(bad),tamanho_bytes=len(bad))
        (package/'manifesto.json').write_bytes((json.dumps(manifest)+'\n').encode())
        authpath=output/'autorizacoes/MC-01-D0.json'
        auth=json.loads(authpath.read_bytes())
        auth.update(manifesto_sha256=f.sha((package/'manifesto.json').read_bytes()),
                    documentos=[{'arquivo':e['arquivo'],'sha256':e['sha256']} for e in manifest['documentos']])
        authpath.write_bytes((json.dumps(auth)+'\n').encode())
        with self.assertRaisesRegex(ValueError,'politica UTF-8'):
            m.preparar(package,package/'manifesto.json',self.root/'recusado',authpath)
