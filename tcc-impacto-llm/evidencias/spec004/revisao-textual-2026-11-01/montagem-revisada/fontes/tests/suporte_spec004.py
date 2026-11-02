"""Oraculos de controle, sem dependencia da implementacao sob teste."""
import json
import os
import shutil
import uuid
from pathlib import Path
import unittest

FIXTURES = Path(__file__).parent/'fixtures/spec004'
ESPERADOS = json.loads((FIXTURES/'esperados.json').read_text(encoding='utf-8'))

class ControleCase(unittest.TestCase):
    def tearDown(self):
        if target := os.environ.get('SPEC004_TEMPORARIOS'):
            if hasattr(self,'temp'):
                out=Path(target)/(self.id()+'-'+uuid.uuid4().hex)
                out.parent.mkdir(parents=True,exist_ok=True)
                shutil.copytree(self.temp.name,out,symlinks=True)

    def checar(self, familia, caso, observado, esperado):
        record = {'origem':'sintetica', 'familia':familia, 'caso':caso,
                  'observado':observado, 'esperado':esperado,
                  'conforme':observado == esperado}
        if target := os.environ.get('SPEC004_CONTROLES'):
            with Path(target).open('a', encoding='utf-8') as stream:
                stream.write(json.dumps(record, ensure_ascii=True, sort_keys=True)+'\n')
        self.assertEqual(observado, esperado, f'{familia}/{caso}')
