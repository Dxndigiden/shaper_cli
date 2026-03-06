from __future__ import annotations

import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import ClassVar


@dataclass(frozen=True)
class Point:
    "Неизменяемая точка на плоскости."

    x: float
    y: float

    def __str__(self) -> str:
        return f'({self.x}, {self.y})'


class Shape(ABC):
    "Базовый класс — каждая фигура обязана уметь описать себя."

    type_label: ClassVar[str] = 'shape'

    def __init__(self) -> None:
        # короткий uuid чтобы не пугать пользователя длинной строкой
        self.id: str = str(uuid.uuid4())[:8]

    @abstractmethod
    def describe(self) -> str:
        "Строковое описание фигуры."

    def __str__(self) -> str:
        return f'[{self.id}] {self.type_label}: {self.describe()}'
