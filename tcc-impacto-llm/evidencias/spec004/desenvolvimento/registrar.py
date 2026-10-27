"""Executa comandos locais e preserva fontes, controles e stdout/stderr por tentativa."""
from pathlib import Path
import hashlib
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone

ROOT=Path(__file__).resolve().parents[3]

if __name__=='__main__':
    output=(ROOT/sys.argv[1]).absolute()
    if not output.is_relative_to(ROOT/'evidencias/spec004'):raise SystemExit('saida fora de spec004')
    output.mkdir(parents=True,exist_ok=False)
    source=output/'fontes';source.mkdir()
    paths=[ROOT/p for p in ['montagem_entradas.py','avaliacao_ids.py','tests/test_montagem_entradas.py','tests/test_avaliacao_ids.py','tests/suporte_spec004.py']]
    paths+=list((ROOT/'tests/fixtures/spec004').rglob('*'))
    hashes={}
    for p in paths:
        if p.is_file():
            rel=p.relative_to(ROOT);q=source/rel;q.parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(p,q);hashes[rel.as_posix()]=hashlib.sha256(q.read_bytes()).hexdigest()
    env=os.environ.copy();env['SPEC004_CONTROLES']=str(output/'controles.jsonl')
    env['SPEC004_TEMPORARIOS']=str(output/'temporarios')
    command=[sys.executable,'-B',*sys.argv[2:]]
    p=subprocess.run(command,cwd=ROOT,env=env,capture_output=True)
    (output/'stdout.txt').write_bytes(p.stdout);(output/'stderr.txt').write_bytes(p.stderr)
    record={'comando':command,'cwd':str(ROOT),'instante_utc':datetime.now(timezone.utc).isoformat(),
      'python':sys.version,'retorno':p.returncode,'origem':'sintetica','fontes_sha256':hashes,
      'limite':'Nao comprova isolamento de identidade; nao e resultado de LLM.'}
    (output/'comando.json').write_text(json.dumps(record,indent=2,ensure_ascii=True)+'\n',encoding='utf-8')
    print(json.dumps({'saida':str(output),'retorno':p.returncode}))
    raise SystemExit(p.returncode)
