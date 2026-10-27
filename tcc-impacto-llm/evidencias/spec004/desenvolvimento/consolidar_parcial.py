"""Consolidacao honesta do escopo independente; nao fecha Spec 004 integralmente."""
from pathlib import Path
import hashlib
import json

ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/'evidencias/spec004/revisao-parcial'

def dump(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('x',encoding='utf-8',newline='\n') as f:json.dump(value,f,indent=2,ensure_ascii=True);f.write('\n')

if __name__=='__main__':
    OUT.mkdir(exist_ok=False)
    inventory=json.loads((ROOT/'evidencias/spec004/preparacao/inventario.json').read_bytes())
    changed=[]
    for name,digest in inventory['protegidos_sha256'].items():
        p=ROOT/name
        if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=digest:changed.append(name)
    if changed:raise RuntimeError('Artefatos protegidos alterados: '+str(changed))
    dump(OUT/'preservacao.json',{'protegidos_sha256':inventory['protegidos_sha256'],'alterados':changed,
      'limite':'Hash demonstra preservacao; nao comprova correcao funcional.'})
    records=[]
    for phase in ['montagem-final','avaliacao-confirmacao']:
        folder=ROOT/'evidencias/spec004'/phase
        cmd=json.loads((folder/'comando.json').read_bytes())
        if cmd['retorno']!=0:raise RuntimeError('Suite nao conforme: '+phase)
        records+=[json.loads(line) for line in (folder/'controles.jsonl').read_text(encoding='utf-8').splitlines()]
    if any(r['conforme'] is not True for r in records):raise RuntimeError('Controle divergente no checkpoint atual')
    planned=json.loads((ROOT/'tests/fixtures/spec004/subcasos-previstos.json').read_bytes())
    matrix=[]
    for i in range(1,17):
        family=f'S-{i:02}';observed=[r for r in records if r['familia']==family]
        if not observed:raise RuntimeError('Familia sem evidencia: '+family)
        matrix.append({'familia':family,'origem':'sintetica','estado':'parcial' if i==14 else 'conforme_no_escopo_offline',
          'previstos':planned[family],'registros_de_confronto':observed,
          'pendencias':['Runner sob identidade separada com negacao real nao provisionado (T014/T015)',
                         'Criacao de symlink real negada: WinError 1314; sem escalada/contorno'] if i==14 else []})
    dump(OUT/'matriz.json',{'origem':'sintetica','fechamento_integral':False,'familias':matrix,
      'chamadas_llm':0,'piloto':False,'politica':'ids-proposta-004-v2'})
    dump(OUT/'estado-tarefas.json',{'concluidas':[f'T{i:03}' for i in list(range(1,14))+list(range(16,42))],
      'pendentes':['T014','T015']+[f'T{i:03}' for i in range(42,49)],
      'nota':'Execucoes parciais e atualizacoes documentais nao concluem T042-T048, pois suas dependencias integrais continuam pendentes.'})
    dump(ROOT/'evidencias/spec004/isolamento/capacidades-verificadas.json',{
      'runner_isolado':'nao provisionado; token atual le referencia, ver ambiente.json',
      'junctions_internas_externas':'criadas e rejeitadas em controles reais temporarios (sem prova de isolamento de identidade)',
      'symlinks_reais':'criacao negada pelo Windows, WinError1314; um metodo ignorado',
      'reparse_generico':'validacao logica de lstat/bit e teste controlado; nao substitui prova de identidade',
      'tarefas_pendentes':['T014','T015'],'contorno_realizado':False})
    reports={
      'us1-logica':'montagem-final, com 5 metodos aprovados e 1 ignorado por WinError1314; junctions reais e quatro payloads confrontados com bytes literais. Demonstracao persistente em demonstracao-001/preparacoes. S-14 permanece parcial.',
      'us2-preservacao':'avaliacao-confirmacao, controles S-11/S-13: originais exatos, ausencia/fragmento, pasta repetida, escrita parcial, fonte alterada/removida, reavaliacao vinculada. Copies temporarias e valores esperado/observado preservados no checkpoint.',
      'us3-avaliacao':'avaliacao-confirmacao: S-01-S-13, listas/frações/invalidade e erros confrontados com literais. Saidas persistentes da CLI em demonstracao-001/avaliacoes. Nenhum gabarito ajustado.',
      'us4-resumos':'avaliacao-confirmacao: S-15/S-16, PONT-01/PONT-02, observacoes/pares/denominadores e fracoes exatas. CLI dos cenarios A/B em demonstracao-001/resumos. Nenhuma chamada externa.'}
    for name,text in reports.items():
        folder=ROOT/'evidencias/spec004'/name;folder.mkdir(exist_ok=False)
        (folder/'relatorio.md').write_text('# Evidencia parcial — '+name+'\n\n'+text+'\n\nOrigem sintetica. Nao e aprovacao cientifica nem fechamento integral. Consulte ../revisao-parcial/matriz.json e os comandos/fontes originais.\n',encoding='utf-8')
    (OUT/'relatorio.md').write_text('''# Revisão parcial de engenharia — Spec 004

27/10/2026. D-26/D-27: convenções técnicas candidatas adotadas pelo pesquisador, revisão científica pendente. Sem LLM, piloto, alteração de gabarito ou notas reais.

## Resultado observado e limites

Implementados montagem permitida e avaliador offline, com CLI e originais/versionamento. Política ids-proposta-004-v2: rfs/tests separados, desconhecidos como FP único, duplicatas registradas, inválida/técnica sem seleção observada, imputação opcional separada. PONT-01 rejeita misturas com inventários separados por versão e sem combinado; para pontuar cada grupo, fornecer nova lista homogênea explícita, sem inventar denominadores. PONT-02 bloqueia célula com duplicidade por configuração/mudança/condição/repetição; tentativas técnicas vinculadas não viram repetições. Jaccard informa observações/pares e não calculável com menos de duas elegíveis.

Checkpoint montagem-final: seis métodos, cinco aprovados e um ignorado (symlink real, WinError 1314). Checkpoint avaliacao-confirmacao: 14 métodos aprovados, sem falhas/erros/ignorados. Confrontos detalhados, esperado/observado, comandos, retornos, stdout/stderr, fontes e cópias temporárias estão nas respectivas pastas. Os originais das execuções anteriores continuam preservados; não se somam repetições dos mesmos controles como observações de pesquisa.

matriz.json contém os confrontos por família/subcaso: 15 famílias conformes no escopo offline, S-14 parcial. Quantidade de métodos/arquivos/links não comprova correção. A evidência funcional são os valores e estados efetivamente confrontados com expectativas prévias, incluindo os casos negativos e fracções do contrato. Sem afirmação de cobertura universal.

Demonstração persistente pela CLI em demonstracao-001, com snapshots/comando em demonstracao-comando: quatro pacotes fictícios, conteúdo exato de entrada, respostas originais, referências sintéticas privadas e resumos A/B. Origem sintética explicitada; não são respostas de LLM. O exemplo foi executado antes do endurecimento para lstat sem seguir links; seus hashes identificam essa versão, e os checkpoints finais identificam a versão atual. Não sobrescrever a demonstração original.

## Impedimentos concretos

T014/T015: não foi disponibilizado runner sob identidade separada com leitura negada das zonas de desenvolvimento/referência/avaliação. O token atual lê a candidata; não cumpre a fronteira exigida. Nenhuma conta, ACL, credencial ou elevação foi usada para contornar essa restrição. Provas em isolamento/ambiente.json e capacidades-verificadas.json. Junctions reais demonstram recusa de caminhos, não isolamento por identidade. A criação de symlink real também foi negada pelo Windows (WinError1314); teste explicitamente ignorado, sem simulação apresentada como prova real.

39 tarefas independentes concluídas; T014/T015 e T042–T048 permanecem pendentes. Foram produzidos diagnóstico e documentos parciais, que não concluem tarefas dependentes do isolamento/integração integral. T036 está resolvida documentalmente pelo pedido explícito, sem aprovação científica presumida. Nenhuma etapa experimental liberada.

## Divergências de desenvolvimento preservadas

fundacao-red/avaliacao-red: módulos ausentes, falha esperada dos controles escritos antes do código. avaliacao-primeira: restrição de saída excessiva rejeitava uma pasta nova irmã dos arquivos de entrada; corrigida preservando recusa de sobreposição das fontes/pasta existente. Nesse checkpoint, o caso de observação ausente reutilizava indevidamente uma tentativa cujo vínculo anterior não estava na lista; corrigida a construção da fixture para representar uma observação única, mantendo expectativa 1/2 de completude. Não se ajustou escore para acomodar o observado. avaliacao-segunda/final/confirmacao preservam as verificações posteriores e novos controles de rechecagem/pares/desconhecidos.

## Preservação e pendências científicas

preservacao.json confere SHA-256 de todas as fontes protegidas do inventário inicial: código/testes anteriores, bancada/evidências 003, materiais, notas e gabarito permanecem intactos. Documentos originais anteriores às decisões atuais estão arquivados em preparacao/arquivos-iniciais. Hash comprova preservação, não validade científica. Checklist de qualidade não foi remarcada.

Revisão profissional da referência/política/expectativas T12, conteúdo definitivo/origem/neutralidade das notas, fundamentação/revisão de precisão/revocação/F1/consistência, desenho final do piloto e adoção constitucional permanecem pendentes. T12 já adotado; sem nova adoção. Não há fechamento integral da Spec 004.
''',encoding='utf-8')
    print('Evidencia parcial consolidada: 39 tarefas independentes; 9 pendentes; nenhuma fonte protegida alterada.')
