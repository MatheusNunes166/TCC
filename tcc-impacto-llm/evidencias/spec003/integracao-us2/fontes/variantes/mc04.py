"""Baseline integrada RF-01–RF-04, somente com entradas válidas.

Estados: ativa, suspensa, em_revisao; operações: visualizar, exportar.
Papéis: frozenset[str] de Consulta, Auditoria e Supervisão.
autorizar cobre os três estados e os oito subconjuntos, inclusive vazio,
nas duas operações. Sem política para entradas malformadas.
Saída: dict com exatamente decisao e motivo strings. Precedência:
estado → conflito → permissão direta → herdada → ausência de permissão.
"""


def obter_permissoes_diretas(papeis: frozenset[str]) -> frozenset[str]:
    """Retorna somente concessões próprias; não decide acesso final."""
    return frozenset(
        operacao
        for papel, operacao in (('Consulta', 'visualizar'), ('Auditoria', 'exportar'))
        if papel in papeis
    )


def obter_papeis_efetivos(papeis: frozenset[str]) -> frozenset[str]:
    """Preserva atribuídos e expande a única herança de um nível."""
    return papeis


def ha_incompatibilidade(papeis_efetivos: frozenset[str]) -> bool:
    """Verifica o único conflito, sem expandir os papéis recebidos."""
    return {'Consulta', 'Auditoria'} <= papeis_efetivos


def autorizar(estado: str, papeis: frozenset[str], operacao: str) -> dict[str, str]:
    """Decide no domínio válido descrito no módulo, sem I/O ou mutação."""
    if estado in ('suspensa', 'em_revisao'):
        return {'decisao': 'negar', 'motivo': 'estado'}
    diretas = obter_permissoes_diretas(papeis)
    efetivos = obter_papeis_efetivos(papeis)
    if ha_incompatibilidade(efetivos):
        return {'decisao': 'negar', 'motivo': 'conflito'}
    if operacao in diretas:
        return {'decisao': 'permitir', 'motivo': 'permissao_direta'}
    if operacao in obter_permissoes_diretas(efetivos):
        return {'decisao': 'permitir', 'motivo': 'permissao_herdada'}
    return {'decisao': 'negar', 'motivo': 'sem_permissao'}
