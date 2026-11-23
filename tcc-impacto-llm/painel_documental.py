"""Extensão do painel único para a coorte documental, preservando o painel v1."""
from pathlib import Path

import documentacao_operacional as doc
import painel_llm as anterior


class Aplicacao(anterior.Aplicacao):
    def __init__(self, *args, area_documental_captura=None, area_documental_avaliacao=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.documental = doc.BlocoDocumental(self.root, self.sender, self.chave, self.origem,
            area_documental_captura, area_documental_avaliacao)

    def opcoes(self):
        return {**super().opcoes(), 'documental': {
            **self.documental.estado(), 'celulas': self.documental.celulas()}}

    def perfil(self, identity):
        if identity == 'documental-proxima':
            return self.documental.previa()
        return super().perfil(identity)

    def iniciar(self, choice):
        with self.lock:
            if isinstance(choice, dict) and 'bloco' in choice:
                return self.documental.iniciar(choice,
                    demo_ocupada=any(not j['finalizado'] for j in self.jobs.values()))
            if self.documental.ocupada():
                raise anterior.ErroPainel('Lote documental em andamento. Aguarde.', 409)
            return super().iniciar(choice)

    def job(self, identity):
        if identity.startswith('DOCOP64-ACAO-'):
            return self.documental.job(identity)
        return super().job(identity)

    def _todos(self):
        return sorted(super()._todos() + self.documental.registros(),
                      key=lambda r: r['instante'], reverse=True)

    def resultados(self):
        records = {r['id']: r for r in self.documental.registros()}
        rows = super().resultados()
        cells = {oid: cell for cell in self.documental.celulas() for oid in cell['observacoes']}
        for row in rows:
            record = records.get(row['id'])
            if record:
                for field in (*doc.FIELDS, 'plano_sha256', 'manifesto_sha256', 'fase', 'status_avaliacao'):
                    row[field] = record.get(field)
                row['celula'] = cells[row['id']]
        return rows

    def detalhe(self, identity):
        record = super().detalhe(identity)
        if record['coorte'] in (doc.COORTE, doc.COORTE_SINTETICA):
            record['celula'] = next(c for c in self.documental.celulas() if identity in c['observacoes'])
        return record

    def pasta(self, identity, side):
        if identity.startswith('DOCOP64-'):
            if side not in ('captura', 'avaliacao') or identity not in {r['observacao_id'] for r in self.documental.rows}:
                raise anterior.ErroPainel('Pasta não permitida.')
            path = (self.documental.capture if side == 'captura' else self.documental.assessed) / identity / 'T01'
            if not path.is_dir():
                raise anterior.ErroPainel('Pasta ainda não criada.')
            anterior.apoio.abrir_pasta(path)
            return
        super().pasta(identity, side)


def servir(root=anterior.ROOT, porta=8765, sem_abrir=False, app=None):
    anterior.servir(root, porta, sem_abrir, app or Aplicacao(root))
