"""Emite patch documental D-29; nao altera arquivos ou evidencias anteriores."""
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
BASE='specs/004-preparacao-avaliacao-ids/'
HEAD='> Contrato vigente — 01/11/2026 (D-29): o modelo recebe somente texto preparado, sem ferramentas, repositório, código, comandos, gabarito, resultados de variantes ou histórico. Exigências de identidade/ACL do Windows de T014/T015 substituídas, sem execução ou aprovação retroativa. Permanecem validação de arquivos/caminhos, autorização de conteúdo, integridade, equivalência de condições e avaliação separada. Notas representam conhecimento de analista de testes; texto definitivo e revisão profissional pendentes. Não se avaliam juniores, novos testes ou defeitos reais. Sem modelo escolhido, envio, chamadas externas ou piloto; revisão científica pendente. Histórico preservado em evidencias/spec004/revisao-textual-2026-11-01/originais.'
SECTION='''
## Contrato textual verificável — D-29

Preparação editorial local em `fontes_autorizadas.py`, com seis caminhos fixos e recortes enumerados: instrução/notas/pedidos de materiais/04; definições integrais de materiais/07; contrato inicial de documentacao/requisitos; seis primeiras colunas da tabela T01–T12 de documentacao/qualidade-e-testes (sem coluna de destaques de RF); somente descrição de uma remoção na tabela da Spec 003; schema existente. Documentos mistos são lidos nessa edição local para selecionar os trechos, nunca enviados inteiros. A referência candidata não é lida nessa etapa.

`montagem_entradas.py`, contrato `spec004-v3`, lê pacote plano e `--autorizacao` externa explícita, fixando hashes de manifesto/documentos. Atualizar apenas seu próprio manifesto não autoriza texto alterado. A autorização é registro técnico controlado, não assinatura de autoridade ou detector semântico de qualquer gabarito: confrontar fontes, recortes, conteúdo e bytes. Mudança de fonte/recorte requer nova conferência; revisão profissional continua pendente. Fixtures v2 e comandos anteriores são históricos, preservados e não reexecutados como prova do contrato atual.

Somente `payload.txt` se destina ao modelo. Manifesto, autorização, cópias de documentos, fontes/hashes e `entrega-textual.json` são registros locais; não anexar diretório, código, fontes mistas ou referência. O recibo fixa texto/hash, `ferramentas=[]`, `anexos_ambiente=[]`, sem histórico e `envio_realizado=false`. Entrega real e ausência de ferramentas na plataforma serão conferidas antes do piloto; não foram exercitadas aqui, pois não há chamadas externas. Não se alega isolamento por SO.

Caminhos suportados: CLI com caminho local absoluto com drive ou relativo ao cwd; documentos do pacote filhos diretos com nomes enumerados; avaliador admite subdiretórios relativos declarados com separadores `/` ou `\\`, confinados à raiz. Recusar drive relativo, raiz sem drive no Windows, UNC/dispositivos, streams `arquivo:fluxo`, dispositivos reservados, ponto/espaço final, componentes declarados vazios/`.`/`..` e links/junctions/reparse points. São controles de inclusão indevida, sem contas/permissões ou alegação de isolamento.

S-14 vigente verifica recortes/fontes, autorização independente, conteúdo proibido fictício em negativos, 16 combinações (quatro mudanças × quatro condições), texto exato e notas iguais D1/E1/ausentes D0/E0. Criação de symlink e negação de leitura por identidade são exigências antigas substituídas: não foram aprovadas. Esses objetos não pertencem às entradas suportadas; permanecem controles de recusa, sem exigir criação privilegiada para aceitar o contrato textual. PONT-01/PONT-02 e fórmulas candidatas não mudaram.
'''
COMMANDS='''
CLI vigente (usar diretórios novos, não os exemplos antigos v2):

```powershell
python -B fontes_autorizadas.py --raiz . --saida <editorial-nova>
python -B montagem_entradas.py --pacote <editorial-nova>/pacotes/MC-01-D0 --manifesto <editorial-nova>/pacotes/MC-01-D0/manifesto.json --autorizacao <editorial-nova>/autorizacoes/MC-01-D0.json --saida <preparacao-nova>
```

Avaliação continua na CLI separada com --referencia. Sem parâmetros de modelo/provedor, envio ou chamada externa.
'''
TASKS='''
## Tarefas de substituição — D-29 (IDs anteriores preservados)

- [ ] T049 [US1] Materializar apenas seis fontes/recortes enumerados em `fontes_autorizadas.py`, mantendo notas literais, proveniência e autorização externa; verificar 16 pacotes sem resultados de variantes, gabarito, código ou histórico.
- [ ] T050 [US1] Verificar `payload.txt`/`entrega-textual.json`, bytes/versões, ferramentas/anexos vazios e envio não realizado; demonstrar recusa de conteúdo alterado mesmo com manifesto atualizado em `tests/test_fontes_autorizadas.py` e `tests/test_montagem_entradas.py`.
- [ ] T051 [US4] Verificar caminhos locais suportados e recusas de inclusão indevida e demonstrar avaliação pela CLI separada, referência apenas nessa etapa e originais preservados em `evidencias/spec004/revisao-textual-2026-11-01/`.

Dependência vigente: T049 → T050/T051 → T042 → T043–T048. T014/T015 são exigências históricas substituídas, não provas aprovadas. Total: 51 IDs, 49 tarefas vigentes e 2 substituídas. Fechamento técnico não conclui revisão científica nem entrega real/piloto.
'''

def modify(line,name):
    if '**FR-002 —' in line:
        return '- **FR-002 — separação de contextos**: o LLM DEVE receber somente o texto preparado com materiais autorizados, sem ferramentas ou acesso adicional ao ambiente. Edição local recorta fontes enumeradas; montagem lê pacote/autorização explícitos, sem referência. O avaliador acessa a referência separadamente e não a devolve ao pacote. Não exigir nem alegar isolamento por SO.'
    if '**SC-001**' in line:
        return '- **SC-001**: todos os blocos têm fonte/recorte autorizado e identidade verificável; S-14 recusa inclusões indevidas, confere equivalência das condições/notas e preservação do texto e contrato de entrega sem ferramentas/anexos. Provas de identidade restrita foram substituídas, não executadas/aprovadas (FR-001–FR-003).'
    if line.startswith('Dois processos sem importação'):
        return 'Preparação, montagem e avaliação têm responsabilidades separadas; somente o avaliador lê a referência. O modelo recebe só o texto preparado, sem ferramentas de leitura do ambiente. Identidade restrita/sentinelas de leitura negada foram substituídas por D-29, sem execução ou aprovação retroativa.'
    if line.startswith(('Para verificação real de isolamento no Windows','**Limite:** nenhum usuário/ACL','Separadamente, S-14 de fronteira','Zonas de execução futuras:')):
        return '> **Exigência histórica substituída por D-29, não executada/aprovada:** '+line
    if line.startswith('| Montagem |'):
        return '| Montagem | Pacote e autorização externa explícita | Preparação/texto exato novos | Referência, recuperação de fontes adicionais e rede |'
    if line.startswith('| S-14 '):
        if line.count('|')==4:
            return '| S-14 vigente | Fontes/recortes, autorização, caminhos locais, 16 pacotes, notas equivalentes e entrega textual. | Bloquear inclusões indevidas; provas antigas de identidade/criação privilegiada substituídas, não aprovadas. |'
        return '| S-14 vigente | Verificar fontes/recortes enumerados, autorização e negativos de inclusão indevida; 16 pacotes/condições/notas/texto exato. Exigências antigas de identidade/criação privilegiada substituídas por D-29, não aprovadas. |'
    if name=='tasks.md':
        if line.startswith('**Impedimento de ambiente separado**'):
            return '**Exigência substituída por D-29:** T014/T015 não foram executadas/aprovadas e deixam de bloquear o contrato textual. Seus registros permanecem históricos; T049–T051 substituem a garantia. Envio real ao modelo sem ferramentas permanece pendente antes do piloto.'
        if line.startswith(('- [ ] T014 ','- [ ] T015 ')):
            return line+' **[SUBSTITUÍDA D-29, NÃO EXECUTADA/APROVADA; ver T049–T051].**'
        if line.startswith('**Pré-condição:** capacidades e controles'):
            return '**Pré-condição vigente:** convenções D-26/D-29 e verificações textuais T049–T051 evidenciadas. Não há gate de identidade do Windows. Fechamento somente de engenharia offline; envio real/piloto/revisão científica continuam pendentes.'
        if line.startswith('- [ ] T042 '):
            return '- [ ] T042 [US4] Consolidar verificações necessárias do contrato textual em `evidencias/spec004/revisao-textual-2026-11-01/`, confrontando fontes, recortes, condições, caminhos, bytes e avaliação separada; reutilizar controles de métricas inalterados com versões/fontes identificadas, sem aprovar prova de SO substituída.'
        if line.startswith('- [ ] T048 '):
            return '- [ ] T048 Revisar `specs/004-preparacao-avaliacao-ids/tasks.md` e relatório atual, marcar aceitação evidenciada, manter T014/T015 como substituídas não executadas e registrar revisão humana/científica, notas definitivas, entrega real e piloto pendentes antes da pesquisa.'
    return line

if __name__=='__main__':
    patch=['*** Begin Patch']
    for name in ['spec.md','plan.md','research.md','data-model.md','contracts/preparacao-avaliacao.md','quickstart.md','tasks.md']:
        path=ROOT/BASE/name;lines=path.read_text(encoding='utf-8-sig').splitlines()
        patch += ['*** Update File: '+path.as_posix(),'@@',' '+lines[0],'+','+'+HEAD]
        for line in lines[1:]:
            new=modify(line,name)
            if new!=line:patch += ['@@','-'+line]+['+'+p for p in new.splitlines()]
        section=SECTION+(COMMANDS if name in ('contracts/preparacao-avaliacao.md','quickstart.md') else '')+(TASKS if name=='tasks.md' else '')
        last=next(l for l in reversed(lines) if l)
        patch+=['@@',' '+last]+['+'+l for l in section.splitlines()]
    patch+=['*** End Patch'];print('\n'.join(patch))
