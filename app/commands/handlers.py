from __future__ import annotations

from app.canvas import serializer
from app.canvas.canvas import Canvas
from app.commands.builders import SHAPE_BUILDERS


def cmd_add(canvas: Canvas, tokens: list[str]) -> str:
    "add <тип> [аргументы]"
    if not tokens:
        types = ', '.join(SHAPE_BUILDERS)
        return f'Укажи тип фигуры: {types}'

    shape_type, *args = tokens
    builder = SHAPE_BUILDERS.get(shape_type)

    if builder is None:
        available = ', '.join(SHAPE_BUILDERS)
        return f'Неизвестный тип «{shape_type}». Доступные: {available}'

    try:
        shape = builder(args)
    except ValueError as exc:
        return f'Ошибка: {exc}'

    canvas.add(shape)
    return f'Добавлена фигура: {shape}'


def cmd_remove(canvas: Canvas, tokens: list[str]) -> str:
    "remove <id>"
    if not tokens:
        return 'Укажи id фигуры, информация в комманле list'

    removed = canvas.remove(tokens[0])
    if removed is None:
        return f'Фигура id «{tokens[0]}» не найдена'

    return f'Удалена: {removed}'


def cmd_list(canvas: Canvas, _tokens: list[str]) -> str:
    "list показать все фигцры"
    if canvas.is_empty():
        return 'Список пуст. Нужн что-то через add.'

    lines = ['Фигуры:']
    lines += [f'  {s}' for s in canvas.all()]
    return '\n'.join(lines)


def cmd_save(canvas: Canvas, tokens: list[str]) -> str:
    "save <имя_файла> сохранить фигуры в JSON"
    if not tokens:
        return 'Укажи имя файла, например save shapes.json'

    path = tokens[0]
    try:
        serializer.save(canvas.all(), path)
    except OSError as exc:
        return f'Ошибка при сохранении: {exc}'

    return f'Сохранено {len(canvas.all())} фигур → {path}'


def cmd_load(canvas: Canvas, tokens: list[str]) -> str:
    "load <имя_файла> загрузить фигуры из JSON"
    if not tokens:
        return 'Укажи имя файла, например load shapes.json'

    path = tokens[0]
    try:
        shapes = serializer.load(path)
    except FileNotFoundError:
        return f'Файл «{path}» не найден'
    except (ValueError, KeyError) as exc:
        return f'Ошибка при загрузке: {exc}'

    for shape in shapes:
        canvas.add(shape)

    return f'Загружено {len(shapes)} фгур из {path}'


def cmd_help(_canvas: Canvas, _tokens: list[str]) -> str:
    "help — справка"
    return (
        'Команды:\n'
        '  add point   <x> <y>\n'
        '  add segment <x1> <y1> <x2> <y2>\n'
        '  add circle  <cx> <cy> <r>\n'
        '  add square  <x> <y> <side>\n'
        '  add oval    <cx> <cy> <rx> <ry>\n'
        '  add rect    <x> <y> <width> <height>\n'
        '  list\n'
        '  remove <id>\n'
        '  save   <имя_файла.json>\n'
        '  load   <имя_файла.json>\n'
        '  help\n'
        '  exit'
    )


COMMANDS: dict[str, 'CommandHandler'] = {
    'add': cmd_add,
    'list': cmd_list,
    'remove': cmd_remove,
    'save': cmd_save,
    'load': cmd_load,
    'help': cmd_help,
}

CommandHandler = type(cmd_add)
