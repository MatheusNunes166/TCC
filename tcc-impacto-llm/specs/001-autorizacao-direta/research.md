# Pesquisa de desenho — incremento 001

Status: propostas técnicas para revisão, em 14/10/2026. Pesquisa documental e revisão técnica; sem instalação, benchmark ou teste de aplicação. Não há incógnita técnica que impeça apresentar o desenho. Aceite das escolhas pelo responsável do projeto permanece pendente.

## Linguagem e testes

**Decisão proposta**: Python 3.11+ e `unittest` da biblioteca padrão, sem dependências de terceiros. Registrar versão exata do interpretador quando preparar o ambiente.

**Justificativa**: função pequena em memória e conjunto pequeno de cenários não exigem infraestrutura. `unittest` oferece execução automatizada, comparação de resultados e subtestes para verificações tabeladas. Essa opção minimiza instalações; a versão-base retoma Python 3.11+ já mencionado nos materiais, sem afirmar que esteja instalado.

**Alternativas consideradas**: Python + pytest, sugestão histórica não aprovada, oferece parametrização concisa; acrescenta dependência externa sem necessidade funcional neste recorte. Outra linguagem acrescentaria uma decisão sem benefício demonstrado para a bancada atual. Se o pesquisador preferir pytest, revisar o guia e a organização dos testes antes de gerar tarefas; não trocar silenciosamente a proposta.

Fontes oficiais consultadas em 14/10/2026: [unittest](https://docs.python.org/3/library/unittest.html) — execução, descoberta e subtestes; [parametrização do pytest](https://docs.pytest.org/en/stable/how-to/parametrize.html) — alternativa de parametrização. As fontes sustentam as capacidades das ferramentas; a escolha mínima é julgamento de engenharia deste plano, não recomendação científica dessas fontes.

## Organização e representação

**Decisão proposta**: um módulo `autorizacao.py`, um arquivo `tests/test_autorizacao.py`, resultados em dicionário com duas strings e papéis como conjunto imutável. Concessões próprias retornadas como conjunto imutável por função de consulta.

**Justificativa**: mantém regras e testes legíveis, sem empacotamento, serialização ou dependência de arquivos de política. Permite verificar Supervisão sem permissão própria sem atribuir-lhe uma negativa final indevida.

**Alternativas consideradas**: dataclass/enum fornecem tipos mais rígidos, mas não são necessários agora; dicionário com vocabulário documentado é suficiente. JSON externo e camadas de serviço aumentariam arquivos e pontos de falha; não há consumidor ou persistência que os exija nesta etapa.

## Domínio parcial e evolução

**Decisão proposta**: tratar contas ativas dependentes de herança ou conflito como fora do domínio de uso garantido pela função parcial. Cobrir contas não ativas com qualquer conjunto válido e ambas as operações. Para permissão direta com conta ativa, usar Consulta ou Auditoria isoladamente.

**Justificativa**: evita afirmar `negar` para Supervisão visualizar ou `permitir` para Consulta + Auditoria, contrariando a baseline futura. Não adiciona comportamento de erro ou motivo novo que a Spec não define. Sem serviço publicado, não há necessidade de expor a bancada incompleta a entradas não suportadas.

**Alternativas consideradas**: negar automaticamente quando faltar capacidade contradiz a herança futura; permitir automaticamente ignora incompatibilidade; implementar RF-03/RF-04 agora amplia escopo. Uma guarda com exceção também introduziria contrato não solicitado. O risco residual é uso indevido fora da precondição; ele precisa estar visível na documentação da função e no handoff da implementação.

## Pendências preservadas

Revisar e aceitar estas propostas antes das tarefas. A versão exata do ambiente é uma verificação futura, não lacuna de desenho. Não decidir MC-04, modelo, métricas, revisor ou repetições: ver [decisões científicas](../../documentacao/decisoes.md). A revisão técnica não valida referência, constituição ou protocolo.
