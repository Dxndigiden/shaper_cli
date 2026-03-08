from __future__ import annotations

from app.models.base import Point
from app.models.shapes import (
    Circle,
    Oval,
    PointShape,
    Rectangle,
    Segment,
    Square,
)


def _floats(tokens: list[str], names: list[str]) -> list[float]:
    if len(tokens) < len(names):
        missing = ', '.join(names[len(tokens) :])
        raise ValueError(f'Не хватает аргументов: {missing}')
    try:
        return [float(t) for t in tokens[: len(names)]]
    except ValueError:
        raise ValueError('Аргументы должны быть числами')


def build_point(tokens: list[str]) -> PointShape:
    "point x y"
    x, y = _floats(tokens, ['x', 'y'])
    return PointShape(position=Point(x, y))


def build_segment(tokens: list[str]) -> Segment:
    "segment x1 y1 x2 y2"
    x1, y1, x2, y2 = _floats(tokens, ['x1', 'y1', 'x2', 'y2'])
    return Segment(start=Point(x1, y1), end=Point(x2, y2))


def build_circle(tokens: list[str]) -> Circle:
    "circle cx cy r"
    cx, cy, r = _floats(tokens, ['cx', 'cy', 'r'])
    return Circle(center=Point(cx, cy), radius=r)


def build_square(tokens: list[str]) -> Square:
    "square x y side"
    x, y, side = _floats(tokens, ['x', 'y', 'side'])
    return Square(origin=Point(x, y), side=side)


def build_oval(tokens: list[str]) -> Oval:
    "oval cx cy rx ry"
    cx, cy, rx, ry = _floats(tokens, ['cx', 'cy', 'rx', 'ry'])
    return Oval(center=Point(cx, cy), rx=rx, ry=ry)


def build_rectangle(tokens: list[str]) -> Rectangle:
    "rect x y width height"
    x, y, w, h = _floats(tokens, ['x', 'y', 'width', 'height'])
    return Rectangle(origin=Point(x, y), width=w, height=h)


ShapeBuilder = type(build_point)

SHAPE_BUILDERS: dict[str, 'ShapeBuilder'] = {
    'point': build_point,
    'segment': build_segment,
    'circle': build_circle,
    'square': build_square,
    'oval': build_oval,
    'rect': build_rectangle,
}
