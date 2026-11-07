# Preparação v2-LF — preservação de bytes, 06/11/2026

Versão vigente: **D36-2026-11-06-v2-lf**, 16 pacotes. Ponto de entrada: [ESTADO_ATUAL](../../../ESTADO_ATUAL.md); política e escopo: [D-36](../../../documentacao/decisoes.md) e [contrato](../../../specs/004-preparacao-avaliacao-ids/contracts/preparacao-avaliacao.md). A correção altera somente preservação/codificação/quebras de linha e metadados derivados. Conteúdo experimental D-35, notas 0.2-local, requisitos, catálogo, mudanças, condições, referência/conjuntos candidatos e métricas preservados.

## Causa confirmada e preparação anterior
Estado inicial: branch `main`, HEAD `8920756d9a82daa244add102c299ed53f0655ad8`, árvore limpa, `core.autocrlf=true` de `C:/Program Files/Git/etc/gitconfig`. Sem `.gitattributes` de preservação. A composição antiga incorporava recortes CRLF e delimitadores LF; os hashes registrados descreviam os arquivos locais mistos. Ao adicionar ao Git, a conversão de CRLF para LF alterou os bytes dos 16 payloads.

A comparação com os blobs locais desse commit confirmou **16 divergências de hash em 16 payloads**; converter CRLF para LF do payload local reproduz integralmente cada blob Git. Exemplo MC-01-D0: 6.765 bytes locais registrados, 6.739 no Git, diferença de 26 CR. Conteúdo textual equivalente. Não houve consulta externa ao GitHub. [Diagnóstico por payload](diagnostico-anterior.json).

A [preparação anterior D-35](../preparacao-piloto-2026-11-06/RELATORIO.md) é histórica por essa falha de preservação. Seus 367 arquivos, inclusive hashes, manifestos, relatórios e evidências, foram mantidos literalmente, sem correção retrospectiva. Inventário agregado de todos os **4.162 arquivos de evidências anteriores**, 39 arquivos históricos e 39 arquivos de conteúdo experimental confere entre início/fim (grupos se sobrepõem; não somar). [Estado inicial](estado-inicial.json), [preservação final](preservacao-final.json).

## Política adotada
- Novos documentos exportados: `utf8-sem-bom-lf-v1`, UTF-8 sem BOM, CRLF/CR → LF, sem trim, reformatação ou alteração de redação/linha terminal. Normalização explícita **antes** de calcular hashes/tamanhos e gerar vínculos.
- `artefatos/recortes/fontes-originais/`: cópias literais das seis fontes autorizadas. `fontes[].sha256/tamanho_bytes` refere-se a esses originais. Cada documento exportado distingue `recorte_antes_normalizacao` de `sha256/tamanho_bytes` após transformação.
- O montador conserva literalmente os documentos já exportados e os delimitadores LF. Declaração dessa política com CR/BOM num documento é recusada; pacotes históricos não são normalizados automaticamente.
- [`.gitattributes`](../../../.gitattributes): `-text -filter -ident` somente nesta pasta v2-LF e nos caminhos futuros `captura/` e `avaliados/`. Os documentos gerados já chegam LF; Git conserva seus bytes. Capturas futuras conservam literalmente outras quebras de linha, BOM ou bytes não UTF-8. A avaliação/recebimento não foi alterada. Outras pastas históricas não recebem essas regras.

As seis fontes, documentos antigos e dados brutos não foram regravados. Cópias literais do exportador/montador usados estão em `artefatos/fontes-ferramentas/`, permitindo conferir o hash do produtor sem depender da quebra de linha do código-fonte num checkout.

## Pacotes vigentes
[Índice](artefatos/recortes/indice.json), [inventário de hashes e tamanhos](artefatos/inventario.json). Cada link abaixo abre o payload completo preparado, não enviado.

| Mudança | D0 | D1 | E0 | E1 |
|---|---|---|---|---|
| MC-01 | [D0](artefatos/preparados/MC-01-D0/payload.txt) | [D1](artefatos/preparados/MC-01-D1/payload.txt) | [E0](artefatos/preparados/MC-01-E0/payload.txt) | [E1](artefatos/preparados/MC-01-E1/payload.txt) |
| MC-02 | [D0](artefatos/preparados/MC-02-D0/payload.txt) | [D1](artefatos/preparados/MC-02-D1/payload.txt) | [E0](artefatos/preparados/MC-02-E0/payload.txt) | [E1](artefatos/preparados/MC-02-E1/payload.txt) |
| MC-03 | [D0](artefatos/preparados/MC-03-D0/payload.txt) | [D1](artefatos/preparados/MC-03-D1/payload.txt) | [E0](artefatos/preparados/MC-03-E0/payload.txt) | [E1](artefatos/preparados/MC-03-E1/payload.txt) |
| MC-04-v2 | [D0](artefatos/preparados/MC-04-v2-D0/payload.txt) | [D1](artefatos/preparados/MC-04-v2-D1/payload.txt) | [E0](artefatos/preparados/MC-04-v2-E0/payload.txt) | [E1](artefatos/preparados/MC-04-v2-E1/payload.txt) |

A geração comparou todos os documentos e payloads novos com os correspondentes D-35 após somente normalização de BOM/EOL: igualdade integral. Mesmas notas 0.2-local só em D1/E1, mesmas distinções direto/estruturado, mesmos documentos comuns e mesmos delimitadores. Nenhuma mudança textual, instrução adicional, seleção ou métrica nova. Fontes mistas contendo referência/histórico ficam fora dos payloads: o verificador reaplica os seis seletores autorizados e confronta cada bloco; os controles negativos de recortes permanecem ativos. Não se alega detector semântico universal de vazamento.

## Prova de transporte Git
Ambiente efetivo: **Windows, PowerShell, Python 3.13.3 e Git 2.49.0.windows.1**. Um repositório temporário isolado incluiu os **arquivos novos** da v2-LF, o verificador, as ferramentas atualizadas e `.gitattributes`. O snapshot foi criado com `core.autocrlf=true`; apenas nele houve stage/commit. Identidade de commit explicitamente artificial (`Verificacao offline D36`), sem assinatura/publicação. Configurações de sistema/global foram isoladas nos subprocessos; ajustes de checkout foram somente locais aos repositórios temporários. Nenhuma configuração do projeto/sistema foi alterada.

Snapshot temporário: `c355e299aafe23e3428b87dc7e5450f6e2743f6e`. Local mantido para inspeção: `saidas-locais/transporte-git-lf-v2-001/snapshot`. O snapshot cobre integralmente os pacotes/inventário atuais; relatórios derivados desta prova foram escritos depois da execução, não são sua própria entrada.

| Checkout limpo | core.autocrlf | core.eol | Arquivos hash/tamanho | Pacotes lidos/remontados | Divergências |
|---|---|---|---:|---:|---:|
| [false-lf](checkouts/false-lf.json) | false | lf | 361 | 16 | 0 |
| [true-crlf](checkouts/true-crlf.json) | true | crlf | 361 | 16 | 0 |
| [input-lf](checkouts/input-lf.json) | input | lf | 361 | 16 | 0 |
| [false-crlf](checkouts/false-crlf.json) | false | crlf | 361 | 16 | 0 |

Por checkout: 361 arquivos inventariados, incluindo **120 documentos exportados + 120 cópias**, 16 payloads e todos os manifestos/autorizações/preparações/índice/fontes/ferramentas. O próprio `inventario.json` é um arquivo adicional: seu hash externo é idêntico na cópia original, snapshot e quatro checkouts, totalizando **362 arquivos de artefatos preservados**. Os 361 registros produzem 1.444 conferências de hash/tamanho nos quatro checkouts; não são 1.444 arquivos experimentais distintos.

Em cada cópia recuperada, foram conferidos hash/tamanho de todos os arquivos inventariados; documentos autorizados; vínculos de manifesto/autorização/preparação; hash do montador produtor arquivado; composição dos payloads; equivalência entre condições/mudanças; mesmas notas onde previstas e ausência em D0/E0; blocos permitidos sem gabarito/histórico/resultados de variantes. O montador existente leu e recompôs todos os 16 pacotes, sem erro de integridade: **64 recomposições após checkout**. Atributos efetivos foram registrados para payload novo, caminhos de capturas e exemplo histórico (sem aplicação retroativa das novas regras).

Dois controles **artificiais**, criados apenas no snapshot temporário, verificaram preservação literal de entrada/resposta com CRLF, CR, BOM e byte não UTF-8 nos caminhos futuros de captura/avaliação. Ambos permaneceram idênticos nas quatro cópias; não são respostas do modelo ou dados de pesquisa.

[Resumo do transporte](transporte.json), [comandos exatos, retornos, stdout/stderr e atributos](comandos-transporte.json), [verificação antes do transporte](verificacao-local.json). Não foram exercitados Linux, macOS ou transporte remoto GitHub; não se presume aprovação nesses ambientes. A prova é local, pelos blobs/commits novos e arquivos efetivamente recuperados em checkouts limpos, não apenas pela árvore de trabalho original.

## Comandos executados e repetição
Da raiz do projeto:

```powershell
python -B evidencias/spec004/preparacao-piloto-2026-11-06-v2-lf/verificar_preservacao.py gerar --saida evidencias/spec004/preparacao-piloto-2026-11-06-v2-lf/artefatos
python -B evidencias/spec004/preparacao-piloto-2026-11-06-v2-lf/verificar_preservacao.py verificar --artefatos evidencias/spec004/preparacao-piloto-2026-11-06-v2-lf/artefatos --recompor-em saidas-locais/verificacao-lf-v2-local-001 --relatorio evidencias/spec004/preparacao-piloto-2026-11-06-v2-lf/verificacao-local.json
python -B evidencias/spec004/preparacao-piloto-2026-11-06-v2-lf/verificar_preservacao.py transporte --temporario saidas-locais/transporte-git-lf-v2-001
```

Para repetir, usar diretórios novos e `--relatorios` novo; nenhum comando sobrescreve evidência anterior. O último comando usa `git init`, `git add`, `git commit` exclusivamente no snapshot temporário, seguido de `git clone --no-hardlinks --no-checkout`, configurações locais e `git checkout --detach` em cada cópia. Não usa reset, limpeza destrutiva, renormalização em massa ou remoto.

Verificações dirigidas: **8 métodos aprovados**, cinco de fontes/exportação (incluindo BOM/CRLF/CR, hashes antes/depois e recusa de falsa declaração LF) e três do montador (composição literal histórica, autorização externa e integridade no fechamento). [Comandos](testes.json), [fontes](testes-1-stderr.txt), [montagem](testes-2-stderr.txt). Nenhuma bancada de baseline/variantes ou suíte de métricas foi reexecutada. `git diff --check` passou.

## Arquivos alterados
- [fontes_autorizadas.py](../../../fontes_autorizadas.py): normalização antes dos hashes, proveniência e fontes literais, nova versão de exportação.
- [montagem_entradas.py](../../../montagem_entradas.py): propaga/verifica a política declarada sem transformar bytes.
- [test_fontes_autorizadas.py](../../../tests/test_fontes_autorizadas.py): regressão da normalização/proveniência e recusa de CRLF sob política LF.
- [`.gitattributes`](../../../.gitattributes): proteção específica de transporte.
- [Contrato](../../../specs/004-preparacao-avaliacao-ids/contracts/preparacao-avaliacao.md), [decisões](../../../documentacao/decisoes.md), [estado central](../../../ESTADO_ATUAL.md), [AGENTS](../../../AGENTS.md) e [HANDOFF](../../../HANDOFF.md): política, versão vigente e limites.
- Esta pasta: nova evidência, script de verificação, 16 pacotes, fontes literais, inventário e relatórios. A pasta anterior não foi alterada.

## Fechamento e pendências do piloto
[Preservação final](preservacao-final.json) confirma HEAD/branch, entradas do índice e configurações do projeto/sistema iguais ao início, e os inventários protegidos sem mudança. **Nenhum stage, commit ou push no projeto; nenhum LLM, piloto/coleta ou alteração de dados brutos.** O commit temporário serve somente à prova local de transporte.

A pendência de preservação de bytes foi corrigida no escopo Windows verificado. Continuam as conferências já existentes: pesquisador conferir os payloads v2-LF e registrar alcance da revisão da referência/medidas; definir configuração suportada, orçamento e ordem; verificar conversa nova com conteúdo completo na primeira mensagem, ferramentas/acesso ao projeto desativados e captura literal. Não se inferiu nova aprovação científica ou autorização para iniciar chamadas.
