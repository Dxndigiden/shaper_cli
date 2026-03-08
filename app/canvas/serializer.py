from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from app.models.base import Point, Shape
from app.models.shapes import (
    Circle,
    Oval,
    PointShape,
    Rectangle,
    Segment,
    Square,
)

_LABEL_TO_CLASS: dict[str, type[Shape]] = {
    cls.type_label: cls
    for cls in (PointShape, Segment, Circle, Square, Rectangle, Oval)
}


def _shape_to_dict(shape: Shape) -> dict:
    "Фигура в словарь."
    return {
        'type': shape.type_label,
        'id': shape.id,
        'data': asdict(shape),
    }


def _dict_to_shape(raw: dict) -> Shape:
    "Словарь в фигуру."
    label = raw['type']
    cls = _LABEL_TO_CLASS.get(label)
    if cls is None:
        raise ValueError(f'Ошибка при загрузке: {label}')

    data = raw['data']

    point_fields = {
        k: Point(**v)
        for k, v in data.items()
        if isinstance(v, dict) and 'x' in v and 'y' in v
    }

    plain_fields = {k: v for k, v in data.items() if k not in point_fields}

    shape = cls(**point_fields, **plain_fields)

    shape.id = raw['id']
    return shape


def save(shapes: list[Shape], path: str | Path) -> None:
    "Сохранение в JSON."
    payload = [_shape_to_dict(s) for s in shapes]
    Path(path).write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8'
    )


def load(path: str | Path) -> list[Shape]:
    "Загрузка из JSON."
    raw = Path(path).read_text(encoding='utf-8')
    return [_dict_to_shape(item) for item in json.loads(raw)]
