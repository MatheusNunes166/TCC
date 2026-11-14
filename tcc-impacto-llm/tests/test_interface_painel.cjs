// Offline interaction checks. A minimal DOM does not validate rendered layout.
const assert = require('node:assert/strict');
const {spawnSync} = require('node:child_process');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const root = path.resolve(__dirname, '..');
const source = spawnSync('python', ['-B', '-c', `
import json, os, socket, sys, tempfile
from pathlib import Path
os.environ.pop('OPENAI_API_KEY', None)
def offline(event, args):
    if event.startswith('socket.'):
        raise RuntimeError('Network forbidden')
sys.addaudithook(offline)
import painel_llm as p
p.api.enviar = lambda *args: (_ for _ in ()).throw(AssertionError('Real API forbidden'))
with tempfile.TemporaryDirectory() as area:
    app = p.Aplicacao(chave=lambda: 'ARTIFICIAL', origem='sintetica',
                     area_captura=Path(area)/'captura', area_avaliacao=Path(area)/'avaliados')
    rows = app.resultados()
    selected = [next(r['id'] for r in rows if r['mudanca']=='MC-02' and r['modelo']=='gpt-6-sol' and r['requisitos']['FP']),
                next(r['id'] for r in rows if r['nota']=='N02')]
    print(json.dumps({'options':app.opcoes(), 'rows':rows,
        'profiles':{key:app.perfil(key) for key in app.profiles},
        'details':{key:app.detalhe(key) for key in selected}}, ensure_ascii=False))
`], {cwd:root, encoding:'utf8', maxBuffer:5*1024*1024,
  env:{...process.env, OPENAI_API_KEY:'', PYTHONDONTWRITEBYTECODE:'1', PYTHONIOENCODING:'utf-8'}});
assert.equal(source.status, 0, source.stderr);
const data = JSON.parse(source.stdout);

class Element {
  constructor(tag, attributes={}) {
    this.tagName=tag; this.attributes=attributes; this.children=[]; this.listeners={};
    this.hidden='hidden' in attributes; this.disabled='disabled' in attributes;
    this.checked='checked' in attributes; this.open='open' in attributes;
    this.className=attributes.class||''; this.dataset={};
    for(const [key,value] of Object.entries(attributes))if(key.startsWith('data-'))this.dataset[key.slice(5)]=value;
    this.classList={contains:name=>this.className.split(/\s+/).includes(name),toggle:(name,force)=>{
      const values=new Set(this.className.split(/\s+/).filter(Boolean));
      const add=force===undefined?!values.has(name):force;
      add?values.add(name):values.delete(name);this.className=[...values].join(' ');
    }};
  }
  get id(){return this.attributes.id;}
  get value(){return this._value??this.attributes.value??(this.tagName==='select'?this.children.find(e=>e.tagName==='option')?.value:this.textContent)??'';}
  set value(value){this._value=value;}
  get textContent(){return this._text??this.children.map(e=>e.textContent).join('');}
  set textContent(value){this._text=String(value);this.children=[];}
  append(...children){this._text=undefined;this.children.push(...children);for(const child of children)child.parent=this;}
  replaceChildren(...children){this.children=[];this.append(...children);}
  setAttribute(key,value){this.attributes[key]=String(value);}
  addEventListener(name,listener){(this.listeners[name]??=[]).push(listener);}
  dispatchEvent(event){for(const listener of this.listeners[event.type]||[])listener(event);}
  click(){if(!this.disabled)this.dispatchEvent({type:'click'});}
  showModal(){this.open=true;}
  close(){this.open=false;}
}
function parse(html){
  const doc=new Element('document'),stack=[doc];
  const cleaned=html.replace(/<(script|style)\b[^>]*>[\s\S]*?<\/\1>/g,'');
  for(const match of cleaned.matchAll(/<([^>]+)>|([^<]+)/g)){
    if(match[2]){const text=new Element('#text');text.textContent=match[2];stack.at(-1).append(text);continue;}
    const token=match[1];if(token.startsWith('!'))continue;
    if(token.startsWith('/')){stack.pop();continue;}
    const tag=token.match(/^\w+/)?.[0];if(!tag)continue;
    const attributes={};
    for(const a of token.slice(tag.length).matchAll(/([^\s=]+)(?:="([^"]*)")?/g))attributes[a[1]]=a[2]??'';
    const element=new Element(tag,attributes);stack.at(-1).append(element);
    if(!['meta','input','br','hr','link','img'].includes(tag))stack.push(element);
  }
  const all=()=>{const result=[];function walk(e){result.push(e);e.children.forEach(walk);}walk(doc);return result;};
  const matches=(e,selector)=>{
    const tag=selector.match(/^\w+/)?.[0];if(tag&&e.tagName!==tag)return false;
    const id=selector.match(/#([\w-]+)/)?.[1];if(id&&e.id!==id)return false;
    const cls=selector.match(/\.([\w-]+)/)?.[1];if(cls&&!e.classList.contains(cls))return false;
    for(const m of selector.matchAll(/\[([^=\]]+)(?:=([^\]]+))?\]/g)){
      const value=m[1]==='open'?(e.open?'':undefined):e.attributes[m[1]];
      if(value===undefined||(m[2]!==undefined&&value!==m[2]))return false;
    }return true;
  };
  doc.getElementById=id=>all().find(e=>e.id===id);
  doc.createElement=tag=>new Element(tag);
  doc.querySelectorAll=selector=>{
    const parts=selector.split(' ');return all().filter(e=>{
      if(!matches(e,parts.at(-1)))return false;
      for(let i=parts.length-2;i>=0;i--){e=e.parent;while(e&&!matches(e,parts[i]))e=e.parent;if(!e)return false;}
      return true;
    });
  };return doc;
}
const html=fs.readFileSync(path.join(root,'apresentacao/interface.html'),'utf8');
const document=parse(html),timers=new Set();
let sends=0,uncertain=false,completed=false;
const demo=structuredClone(Object.values(data.details)[0]);
demo.id='DEMO-ARTIFICIAL';demo.coorte='demonstracao';
const requests=[];
async function fetchLocal(url,options){
  requests.push(url);
  let result;
  if(url==='/api/opcoes')result=data.options;
  else if(url==='/api/resultados')result=completed?[...data.rows,demo]:data.rows;
  else if(url.startsWith('/api/perfil/'))result=data.profiles[decodeURIComponent(url.slice(12))];
  else if(url==='/api/executar'){
    if(uncertain)throw new Error('Falha artificial de conexão');
    sends++;completed=true;result={id:demo.id};
  }else if(url.startsWith('/api/job/'))result={id:demo.id,finalizado:true,etapa:'concluida',mensagem:'Resposta artificial preservada'};
  else if(url.startsWith('/api/resultado/'))result=url.endsWith(demo.id)?demo:data.details[url.slice(15)];
  else throw new Error('Unexpected request '+url);
  assert.ok(result,'No fixture for '+url);return {ok:true,json:async()=>structuredClone(result)};
}
const context=vm.createContext({document,fetch:fetchLocal,crypto:require('node:crypto').webcrypto,
  setTimeout:(fn,delay)=>{const timer=setTimeout(fn,delay);timers.add(timer);return timer;},
  clearTimeout,console,Date,Event});
const script=html.match(/<script>([\s\S]*?)<\/script>/)[1].replace('__TOKEN_TCC__','"ARTIFICIAL"');
const evaluate=code=>vm.runInContext(code,context);
const $=id=>document.getElementById(id);
const wait=()=>new Promise(resolve=>setImmediate(resolve));
async function until(condition){for(let i=0;i<100;i++){if(condition())return;await wait();}throw new Error('Interaction did not settle');}
function select(id,value){$(id).value=value;$(id).dispatchEvent({type:'change'});}
(async()=>{
 try{
  evaluate(script);await until(()=>$('result-count').textContent.startsWith('0 execuções'));
  assert.equal(sends,0);assert.equal(data.rows.length,80);assert.equal(Object.keys(data.profiles).length,20);
  $('preview').click();await until(()=>!$('preview-box').classList.contains('hidden'));
  assert.ok($('preview-text').textContent.includes('<<<inicio:sistema>>>'));assert.equal(sends,0);
  select('filter-cohort','comparacao');assert.equal($('result-rows').children.length,64);
  select('filter-model','gpt-6-sol');assert.equal($('result-rows').children.length,32);
  select('filter-change','MC-02');assert.equal($('result-rows').children.length,8);
  select('filter-status','excedente');assert.equal($('result-rows').children.length,4);
  select('filter-rf','RF-02');assert.equal($('result-rows').children.length,4);
  select('filter-test',data.rows.find(r=>r.mudanca==='MC-02').testes.ids_esperados[0]);assert.equal($('result-rows').children.length,4);
  await evaluate(`openDetail(${JSON.stringify(Object.keys(data.details)[0])})`);
  assert.ok($('detail-rows').textContent.includes('Excedente'));
  $('dim-tests').click();assert.ok($('detail-rows').textContent.includes('Preservação'));
  document.querySelectorAll('#detail details')[0].open=true;
  await evaluate(`openDetail(${JSON.stringify(Object.keys(data.details)[1])})`);
  assert.equal(document.querySelectorAll('#detail details[open]').length,0);
  assert.ok($('detail-note-text').textContent.includes('nunca altera um conflito'));
  for(const id of ['filter-model','filter-change','filter-status','filter-rf','filter-test'])select(id,'');
  select('filter-cohort','notas');assert.equal($('result-rows').children.length,16);
  select('filter-note','N02');assert.equal($('result-rows').children.length,8);
  select('filter-condition','E1');assert.equal($('result-rows').children.length,4);
  $('run').click();$('run').click();$('run').dispatchEvent({type:'click'});
  await until(()=>evaluate('state.last!==null'));assert.equal(sends,1);
  uncertain=true;$('run').click();await until(()=>$('progress-text').textContent.includes('Recarregue'));
  assert.equal($('run').disabled,true);$('run').dispatchEvent({type:'click'});await wait();assert.equal(sends,1);
  evaluate('state.busy=false;state.options.chave_disponivel=false;updateForm()');
  assert.equal($('run').disabled,true);assert.equal($('preview').disabled,false);
  console.log('OK: 80 originais, 20 perfis; filtros, detalhes, notas, preview, clique duplicado, falha de POST e ausência de chave. DOM artificial; zero chamadas reais.');
 }finally{for(const timer of timers)clearTimeout(timer);}
})().catch(error=>{console.error(error);process.exitCode=1;});
