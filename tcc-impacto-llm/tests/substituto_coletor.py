"""Processo artificial de teste; biblioteca padrao, sem rede, sem LLM/gabarito."""
import json
import sys


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else 'valida'
    payload = sys.stdin.buffer.read()
    # Eco literal permite verificar bytes efetivamente entregues ao processo filho.
    with open('stdin-recebido.bin', 'xb') as stream:
        stream.write(payload)
    def emit(event):
        sys.stdout.buffer.write((json.dumps(event, ensure_ascii=True) + '\n').encode())
        sys.stdout.buffer.flush()
    emit({'type': 'thread.started', 'thread_id': __import__('uuid').uuid4().hex})
    emit({'type': 'turn.started'})
    if mode == 'tecnica':
        sys.stderr.buffer.write(b'CONTROLE: falha de transporte artificial\r\n')
        emit({'type': 'turn.failed', 'error': {'message': 'CONTROLE transporte'}})
        return 7
    if mode == 'ferramenta':
        emit({'type': 'item.completed', 'item': {'type': 'command_execution', 'command': 'CONTROLE SEM EXECUCAO'}})
    if mode == 'modelo':
        emit({'type': 'metadata', 'model': 'modelo-artificial-divergente'})
    text = {'invalida': '```json\r\nnao JSON\r\n```\n', 'vazia': '',
            'valida': ' \r\n{"requisitos":[],"testes":[]}\r\n '}.get(mode, '{"requisitos":[],"testes":[]}')
    emit({'type': 'item.completed', 'item': {'type': 'agent_message', 'text': text}})
    emit({'type': 'turn.completed', 'usage': {'input_tokens': None, 'output_tokens': None}})
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
