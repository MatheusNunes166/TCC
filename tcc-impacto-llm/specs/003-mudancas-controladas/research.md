# Pesquisa técnica local — Spec 003

Data: 19/10/2026. Decisões de planejamento; sem implementação/execução de variantes. Fontes: governança, Spec/checklist, código/testes de B e referência 0.2. Revisão auxiliar somente de leitura prevista pela skill speckit-plan, sem consulta externa ou instalação.

## R-01 — origem comum

**Decisão**: B = `aec474bcb54d6dae2afceff8e5b9226991386490`; HEAD da sessão `3cdff8ec1c82b4919bce3761364364754863ca81` acrescenta a Spec. Árvore inicialmente limpa; arquivos essenciais de B idênticos no HEAD.

**Justificativa**: leitura dos blobs confirmou RF-01–RF-04, AST com 18 métodos/T01–T12 e JSON 0.2 com 12 casos/48 expectativas/conjuntos 2/4/8/5. Blobs no plano. Evidência histórica T12 permanece distinta desta conferência estática, sem nova execução.

**Alternativas**: HEAD móvel redefiniria a origem; árvore não commitada perderia procedência. Alteração relevante local futura precisa ser informada antes de incluída na rodada e não se torna B automaticamente.

## R-02 — quatro módulos autônomos

**Decisão**: quatro cópias de autorizacao.py, cada uma extraída novamente de B com uma edição mínima; MC-04 mantém ID canônico MC-04-v2 do JSON.

**Justificativa**: núcleo pequeno e puro; diffs legíveis e sem alteração na API inicial. Nenhuma variante compartilha/importa implementação de outra; não há flags ou estado global de mudança.

**Alternativas**: quatro worktrees/branches acrescentariam árvores/gestão Git; transformação AST em execução exigiria transformador e validação próprios; monkeypatch/flags afetariam isolamento ou baseline; motor de políticas ampliaria o recorte. AST somente audita a edição.

## R-03 — identidade dos bytes executados

**Decisão**: Git via subprocesso em bytes e caminhos relativos à raiz Git real; snapshot novo por tentativa, SHA-256 antes/depois, Python -B sem cache existente. Carregar módulos com importlib.util por caminho absoluto e nomes exclusivos.

**Justificativa**: redirecionamento textual PowerShell pode modificar BOM/CRLF; importação só por nome pode carregar autorizacao inicial ou cache. B identifica origem, mas SHA-256 da fonte real identifica cada edição executada. Executor/testes novos também têm commit, estado e hashes registrados.

**Alternativas**: só B no relatório não identifica variantes; reutilizar diretório apaga divergências ou lê cache; modificar sys.path/global autorizacao pode contaminar a rodada.

## R-04 — catálogo e expectativas específicas

**Decisão**: suíte original intacta no snapshot de B; 12 observados iniciais por catálogo na mesma rodada. Matriz nova percorre catalogo × quatro mudanças e busca expected de cada mudança, comparando dicionário completo.

**Justificativa**: controles e expectativas da baseline não se aplicam integralmente às variantes. Alguns verificam justamente a regra retirada. O catálogo preserva entradas sem duplicação; o campo tests do JSON selecionaria só 19 casos (2+4+8+5), em vez de 48.

**Alternativas**: trocar import da suíte original faz mudanças legítimas parecerem falhas; recodificar entradas/esperados cria fontes duplicadas; derivar esperado da saída elimina independência do oráculo candidato.

## R-05 — auditoria antes da execução

**Decisão**: diff contra B revisado por responsável/data e comparação AST com uma única diferença exata permitida por módulo; fora da expressão, assinaturas/funções/nós iguais. Fonte inválida bloqueia seus 12 pares, sem impedir conferir variantes válidas.

**Justificativa**: 48 resultados corretos não provam ausência de alteração extra não coberta. Auditoria prova procedência; testes confrontam comportamento. Propagação é efeito da edição única, não justificativa para modificar outra regra.

**Alternativas**: só contar linhas não limita semântica; confiar apenas nas saídas mascara alterações não exercitadas; transformar referência em verdade por concordância com código ignora revisão humana.

## R-06 — registro e interface mínimos

**Decisão**: comando local futuro, manifesto/resultados JSON, logs e diffs por tentativa; unittest com subtestes e registro antes da asserção. Resultado, esperado e efeitos contra B separados. Tentativas novas não sobrescrevem as anteriores.

**Justificativa**: atende rastreabilidade sem banco, API ou coletor de LLM. Número de pares vem das 48 chaves, não de “Ran N tests”. Erro mantém observado ausente; retorno inválido preserva bruto. Persistência protegida e código de saída não zero em falha/lacuna.

**Alternativas**: só stdout não relaciona versão/esperado/observado; arquivo único sobrescrito apaga evidência; framework de coleta adicionaria capacidade não solicitada.

## Conclusão da pesquisa técnica

Escolhas técnicas resolvidas por fontes locais; Python + unittest e biblioteca padrão mantidos. P-01/P-02/P-03 e adoção constitucional continuam pendentes. T12 adotado em B, expectativas das variantes ainda candidatas. Conformidade futura não aprova cientificamente referência, política ou MC-04-v2 nem libera piloto. Próximos artefatos são modelo, contrato e guia; nenhuma tarefa ou implementação nesta fase.
