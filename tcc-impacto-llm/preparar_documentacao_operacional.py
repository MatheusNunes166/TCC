"""Consolidada x operacional: preparar/conferir textos, sem captura ou envio.

Troca somente o bloco de requisitos por cinco documentos. Catálogo completo,
política, mudança, pedido, notas e schema permanecem literais. Nunca lê chave
ou referência privada. O plano não é aceito automaticamente pelo painel.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path
import random
import re

from montagem_entradas import sem_links
from painel_llm import ROOT, perfis_preservados

VERSAO = 'documentacao-operacional-0.3-v1'
FONTE_RF_SHA256 = '0d1e465d42d36b241933e688965b5dc562711e7670198b7869b4b06bef5ae4cb'
MUDANCAS = ('MC-02','MC-04-v2')
CONDICOES = ('D0','D1')
MODELOS = ('gpt-6-sol','gpt-6-astra')
DOCUMENTACOES = ('CONSOLIDADA','OPERACIONAL')
SEMENTE = 20261122
RF = re.compile(r'(<<<inicio:requisitos-baseline>>>\n)([\s\S]*?)(<<<fim:requisitos-baseline>>>)')
BLOCOS = re.compile(r'<<<inicio:([^>]+)>>>\n([\s\S]*?)<<<fim:\1>>>')


def sha(data):
    return hashlib.sha256(data).hexdigest()


def serial(data):
    return (json.dumps(data,ensure_ascii=False,indent=2,sort_keys=True)+'\n').encode()


def salvar(path,raw):
    path=sem_links(Path(path));path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('xb') as stream:stream.write(raw)


def ler(path):
    return json.loads(sem_links(Path(path)).read_bytes())


def documentos(conteudo_rf):
    if sha(conteudo_rf.encode())!=FONTE_RF_SHA256:
        raise ValueError('Requisitos de origem fora da versão auditada.')
    entrada_saida=conteudo_rf.split('## Regras e aceitação planejada')[0].strip()
    regras=[]
    for line in conteudo_rf.splitlines():
        if line.startswith('| RF-'):
            cells=[s.strip() for s in line.split('|')[1:-1]]
            regras.append(f'| {cells[0]} | {cells[1]} |')
    if len(regras)!=4:raise ValueError('IDs funcionais divergentes.')
    return {
      '01-especificacao-funcional.md':('# Especificação funcional\n\n'+entrada_saida+'\n\n'
          '## Requisitos\n\n| ID | Regra |\n| --- | --- |\n'+'\n'.join(regras)+'\n'),
      '02-cadastro-de-papeis.md':'''# Cadastro de papéis

O conjunto informado na entrada contém os papéis atribuídos. As concessões
próprias dos papéis atribuídos são permissões diretas. O conjunto efetivo
contém os atribuídos e os papéis incluídos pela configuração de herança.

| Papel | Concessões próprias |
| --- | --- |
| Consulta | visualizar |
| Auditoria | exportar |
| Supervisão | nenhuma |
''',
      '03-configuracao-de-heranca.md':'''# Configuração de herança

A expansão possui um nível. Não há expansão multinível nem ciclos.
As permissões herdadas são obtidas das concessões próprias dos papéis
incluídos. As relações configuradas são somente as da tabela.

| Papel de origem | Papel incluído |
| --- | --- |
| Supervisão | Consulta |
''',
      '04-configuracao-de-incompatibilidades.md':'''# Configuração de incompatibilidades

A validação considera o conjunto de papéis efetivos. Há incompatibilidade
quando os dois membros de um par configurado estão presentes nesse conjunto.
Os pares configurados são somente os da tabela.

| Papel A | Papel B |
| --- | --- |
| Consulta | Auditoria |
''',
      '05-contrato-de-execucao.md':'''# Contrato de execução

O processamento primeiro verifica o estado. Para a conta que prossegue,
obtém as permissões diretas e realiza a expansão configurada antes de
verificar incompatibilidades e decidir sobre a operação.

Aplicar o primeiro retorno cuja condição seja satisfeita, na prioridade indicada.

| Prioridade | Condição | Decisão | Motivo |
| --- | --- | --- | --- |
| 1 | estado diferente de ativa | negar | estado |
| 2 | existe incompatibilidade no conjunto efetivo | negar | conflito |
| 3 | operação possui concessão direta | permitir | permissao_direta |
| 4 | operação possui concessão herdada | permitir | permissao_herdada |
| 5 | nenhuma condição anterior satisfeita | negar | sem_permissao |

Um incremento parcial de RF-01/RF-02 não pode redefinir o contrato global
ou alegar suporte a RF-03/RF-04.
'''}


def operacionalizar(payload):
    if b'\r' in payload or payload.startswith(b'\xef\xbb\xbf'):
        raise ValueError('Payload deve ser UTF-8/LF sem BOM.')
    text=payload.decode();matches=list(RF.finditer(text))
    if len(matches)!=1:raise ValueError('Bloco de requisitos deve ser único.')
    match=matches[0];docs=documentos(match[2])
    replacement='\n'.join(f'<<<inicio:{name[:-3]}>>>\n{content}\n<<<fim:{name[:-3]}>>>'
                          for name,content in docs.items())
    return (text[:match.start()]+replacement+text[match.end():]).encode(),docs


def montar(root=ROOT):
    root=Path(root);profiles=perfis_preservados(root)
    payloads,sources,all_docs={},{},None
    for change,condition in itertools.product(MUDANCAS,CONDICOES):
        note='sem' if condition=='D0' else 'original'
        profile=profiles[f'{change}:{condition}:{note}']
        original=profile['payload'];modified,docs=operacionalizar(original)
        if all_docs is not None and docs!=all_docs:
            raise ValueError('Documentos operacionais diferentes entre condições.')
        all_docs=docs
        for level,data in zip(DOCUMENTACOES,(original,modified)):
            payloads[f'{change}-{condition}-{level}']=data
        sources[f'{change}:{condition}']={
            'requisicao_origem':profile['origem'].relative_to(root).as_posix(),
            'requisicao_sha256':profile['origem_sha256'],
            'payload_origem_sha256':profile['payload_sha256'],
            'referencia_sha256':profile['referencia_sha256']}
    return payloads,sources,all_docs


def plano(payloads,sources):
    rng=random.Random(SEMENTE);observations=[]
    for repetition in (1,2):
        cells=list(itertools.product(MUDANCAS,CONDICOES,DOCUMENTACOES,MODELOS))
        rng.shuffle(cells)
        for change,condition,level,model in cells:
            name=f'{change}-{condition}-{level}'
            observations.append({'observacao_id':f'DOCOP03-{name}-{model[6:].upper()}-R{repetition:02}',
                'ordem':len(observations)+1,'bloco':repetition,'repeticao':repetition,
                'mudanca':change,'condicao':condition,'documentacao_id':level,
                'nota_id':'sem' if condition=='D0' else 'original',
                'modelo_solicitado':model,'payload':f'payloads/{name}.txt',
                'payload_sha256':sha(payloads[name])})
    return {'versao':VERSAO,'status':'PREPARADO_OFFLINE_NAO_ENVIADO',
        'desenho':'ADOTADO_PELO_PESQUISADOR_NESTA_CONVERSA',
        'conferencia_dos_novos_textos':'PENDENTE','integracao_captura':'PENDENTE',
        'envio_autorizado':False,'revisao_cientifica_externa':'NAO_ATRIBUIDA',
        'fase_proposta':'exploratoria_documentacao_operacional','catalogo_versao':'0.3',
        'fator_documentacao':{'CONSOLIDADA':'Requisitos e critérios explicativos literais da origem',
            'OPERACIONAL':'Cinco documentos com regras, cadastros, configurações e contrato; sem explicações de consequências particulares'},
        'catalogo':'INTEGRAL_COM_RESULTADOS_BASELINE_EM_AMBAS',
        'semente':SEMENTE,'quantidade_planejada':32,
        'configuracao_proposta':{'esforco_solicitado':'medium','max_output_tokens':4096,
            'timeout_segundos':120,'tools':[],'tool_choice':'none','store':False,'stream':False,
            'retries_automaticos_cliente':0,'orcamento_usd':None,
            'modalidade':'Responses API HTTP direto, integração específica pendente'},
        'fontes':sources,'observacoes':observations}


def arquivos_esperados(root=ROOT):
    payloads,sources,docs=montar(root)
    result={f'payloads/{name}.txt':raw for name,raw in payloads.items()}
    result.update({f'documentos-operacionais/{name}':text.encode() for name,text in docs.items()})
    result['plano.json']=serial(plano(payloads,sources))
    return result


def preparar(pasta,root=ROOT):
    folder=sem_links(Path(pasta))
    if folder.exists():raise ValueError('Destino existente: preservar e escolher um novo.')
    files=arquivos_esperados(root)
    for name,raw in files.items():salvar(folder/name,raw)
    salvar(folder/'manifesto.json',serial({'versao':VERSAO,
        'arquivos':{name:sha(raw) for name,raw in files.items()},
        'preparador_sha256':sha(Path(__file__).read_bytes()),'chamadas_executadas':0}))
    return conferir(folder,root)


def conferir(pasta,root=ROOT):
    folder=sem_links(Path(pasta));files=arquivos_esperados(root)
    manifest={'versao':VERSAO,'arquivos':{name:sha(raw) for name,raw in files.items()},
              'preparador_sha256':sha(Path(__file__).read_bytes()),'chamadas_executadas':0}
    if ler(folder/'manifesto.json')!=manifest:raise ValueError('Manifesto/versão divergentes.')
    if {p.relative_to(folder).as_posix() for p in folder.rglob('*') if p.is_file()}!=set(files)|{'manifesto.json'}:
        raise ValueError('Inventário divergente.')
    for name,raw in files.items():
        if sem_links(folder/name).read_bytes()!=raw:raise ValueError('Bytes divergentes: '+name)
    return {'status':'OK_PREPARACAO_OFFLINE','documentos_operacionais':5,'payloads':8,
            'observacoes_planejadas':32,'celulas':16,'repeticoes_por_celula':2,
            'chamadas_executadas':0,'envio_autorizado':False,
            'conferencia_dos_novos_textos':'PENDENTE','integracao_captura':'PENDENTE'}


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('acao',choices=('preparar','conferir'));parser.add_argument('--pasta',required=True)
    args=parser.parse_args(argv)
    try:
        function=preparar if args.acao=='preparar' else conferir
        print(json.dumps(function(args.pasta),ensure_ascii=False,indent=2))
    except (ValueError,OSError) as error:parser.exit(2,str(error)+'\n')


if __name__=='__main__':main()
