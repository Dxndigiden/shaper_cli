from __future__ import annotations

import math
from dataclasses import dataclass
from typing import ClassVar

from app.models.base import Point, Shape


@dataclass
class PointShape(Shape):
    "Точка как самостоятельная фигура."

    type_label: ClassVar[str] = 'Точка'
    position: Point

    def __post_init__(self) -> None:
        super().__init__()

    def describe(self) -> str:
        return f'позиция {self.position}'


@dataclass
class Segment(Shape):
    "Отрезок."

    type_label: ClassVar[str] = 'Отрезок'
    start: Point
    end: Point

    def __post_init__(self) -> None:
        super().__init__()

    @property
    def length(self) -> float:
        dx = self.end.x - self.start.x
        dy = self.end.y - self.start.y
        return round(math.hypot(dx, dy), 4)

    def describe(self) -> str:
        return f'{self.start} → {self.end}, длина={self.length}'


@dataclass
class Circle(Shape):
    "Круг."

    type_label: ClassVar[str] = 'Круг'
    center: Point
    radius: float

    def __post_init__(self) -> None:
        if self.radius <= 0:
            raise ValueError('Радиус должен быть > 0')
        super().__init__()

    @property
    def area(self) -> float:
        return round(math.pi * self.radius**2, 4)

    def describe(self) -> str:
        return f'центр {self.center}, r={self.radius}, площадь≈{self.area}'


@dataclass
class Square(Shape):
    "Квадрат."

    type_label: ClassVar[str] = 'Квадрат'
    origin: Point
    side: float

    def __post_init__(self) -> None:
        if self.side <= 0:
            raise ValueError('Сторона должна быть > 0')
        super().__init__()

    @property
    def area(self) -> float:
        return round(self.side**2, 4)

    def describe(self) -> str:
        return f'угол {self.origin}, сторона={self.side}, площадь={self.area}'
