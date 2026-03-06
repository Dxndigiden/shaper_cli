from __future__ import annotations

from app.canvas.canvas import Canvas
from app.commands.handlers import COMMANDS

_EXIT = object()


def dispatch(canvas: Canvas, raw: str) -> str | object:
    "Парсит строку и выполняе команду."
    parts = raw.strip().split()
    if not parts:
        return ''

    cmd, *tokens = parts

    if cmd == 'exit':
        return _EXIT

    handler = COMMANDS.get(cmd)
    if handler is None:
        return f'Неизвестная команда «{cmd}». Справка help.'

    return handler(canvas, tokens)


def run_repl(canvas: Canvas) -> None:
    "Бесконечный цикл ввода. Введи exit или Ctrl+C."
    print('Векторный редактор. Введи help или exit.')

    while True:
        try:
            raw = input('> ')
        except (EOFError, KeyboardInterrupt):
            print('\nВыход')
            break

        result = dispatch(canvas, raw)

        if result is _EXIT:
            print('Выхход')
            break

        if result:
            print(result)
