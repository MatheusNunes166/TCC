"""Bancada parcial RF-01/RF-02, somente com entradas válidas.

Estados: ativa, suspensa, em_revisao; operações: visualizar, exportar.
Papéis: frozenset[str] de Consulta, Auditoria e Supervisão.
autorizar cobre não ativas com qualquer subconjunto; ativas somente com
Consulta ou Auditoria isoladamente. Fora disso não há resultado garantido,
guarda, exceção ou motivo substituto contratado. Saída: dict com exatamente
decisao e motivo strings. RF-03/RF-04 são futuros; a precedência completa
permanece estado → conflito → ausência de permissão.
"""


def obter_permissoes_diretas(papeis: frozenset[str]) -> frozenset[str]:
    """Retorna somente concessões próprias; não decide acesso final."""
    return frozenset(
        operacao
        for papel, operacao in (('Consulta', 'visualizar'), ('Auditoria', 'exportar'))
        if papel in papeis
    )


def autorizar(estado: str, papeis: frozenset[str], operacao: str) -> dict[str, str]:
    """Decide somente no domínio parcial descrito no módulo, sem I/O ou mutação."""
    if estado in ('suspensa', 'em_revisao'):
        return {'decisao': 'negar', 'motivo': 'estado'}
    if operacao in obter_permissoes_diretas(papeis):
        return {'decisao': 'permitir', 'motivo': 'permissao_direta'}
    return {'decisao': 'negar', 'motivo': 'sem_permissao'}
