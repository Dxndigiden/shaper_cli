from __future__ import annotations

from app.models.base import Shape


class Canvas:
    "Хранилище фигур и CRUD-операции."

    def __init__(self) -> None:
        self._shapes: list[Shape] = []

    def _find(self, shape_id: str) -> Shape | None:
        return next((s for s in self._shapes if s.id == shape_id), None)

    def add(self, shape: Shape) -> Shape:
        self._shapes.append(shape)
        return shape

    def remove(self, shape_id: str) -> Shape | None:
        shape = self._find(shape_id)
        if shape:
            self._shapes.remove(shape)
        return shape

    def all(self) -> list[Shape]:
        return list(self._shapes)

    def is_empty(self) -> bool:
        return not self._shapes
