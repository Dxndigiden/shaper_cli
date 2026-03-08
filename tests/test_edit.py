import math
import os
import tempfile

from pytest import raises

from app.canvas import serializer
from app.canvas.canvas import Canvas
from app.cli.repl import _EXIT, dispatch
from app.models.base import Point
from app.models.shapes import (
    Circle,
    Oval,
    PointShape,
    Rectangle,
    Segment,
    Square,
)


def test_point_str():
    assert str(Point(1, 2)) == '(1, 2)'


def test_segment_length():
    s = Segment(start=Point(0, 0), end=Point(3, 4))
    assert s.length == 5.0


def test_circle_area():
    import math

    c = Circle(center=Point(0, 0), radius=1)
    assert abs(c.area - math.pi) < 0.001


def test_circle_bad_radius():
    with raises(ValueError):
        Circle(center=Point(0, 0), radius=0)


def test_square_area():
    s = Square(origin=Point(0, 0), side=4)
    assert s.area == 16.0


def test_square_bad_side():
    with raises(ValueError):
        Square(origin=Point(0, 0), side=-1)


def test_canvas_add_and_list():
    c = Canvas()
    shape = c.add(PointShape(position=Point(0, 0)))
    assert shape in c.all()


def test_canvas_remove():
    c = Canvas()
    shape = c.add(Circle(center=Point(0, 0), radius=5))
    removed = c.remove(shape.id)
    assert removed is shape
    assert c.is_empty()


def test_canvas_remove_missing():
    c = Canvas()
    assert c.remove('nope') is None


def test_dispatch_add_point():
    c = Canvas()
    result = dispatch(c, 'add point 1 2')
    assert 'Точка' in result
    assert not c.is_empty()


def test_dispatch_unknown_command():
    c = Canvas()
    result = dispatch(c, 'fly')
    assert 'Неизвестная команда' in result


def test_dispatch_exit():
    c = Canvas()
    assert dispatch(c, 'exit') is _EXIT


def test_dispatch_remove():
    c = Canvas()
    dispatch(c, 'add square 0 0 3')
    shape_id = c.all()[0].id
    result = dispatch(c, f'remove {shape_id}')
    assert 'Удалена' in result
    assert c.is_empty()


def test_dispatch_list_empty():
    c = Canvas()
    result = dispatch(c, 'list')
    assert 'Список пуст' in result


def test_oval_area():
    assert (
        abs(Oval(center=Point(0, 0), rx=3, ry=4).area - math.pi * 12) < 0.001
    )


def test_oval_bad_axes():
    try:
        Oval(center=Point(0, 0), rx=-1, ry=4)
        assert False
    except ValueError:
        pass


def test_rectangle_area_and_perimeter():
    r = Rectangle(origin=Point(0, 0), width=3, height=4)
    assert r.area == 12.0
    assert r.perimeter == 14.0


def test_rectangle_bad_side():
    try:
        Rectangle(origin=Point(0, 0), width=0, height=4)
        assert False
    except ValueError:
        pass


def test_save_and_load_roundtrip():
    c = Canvas()
    c.add(PointShape(position=Point(1, 2)))
    c.add(Circle(center=Point(0, 0), radius=5))
    c.add(Rectangle(origin=Point(1, 1), width=3, height=4))
    c.add(Oval(center=Point(2, 2), rx=3, ry=1))

    with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
        path = f.name
    try:
        serializer.save(c.all(), path)
        loaded = serializer.load(path)
    finally:
        os.unlink(path)

    assert len(loaded) == 4
    assert [s.type_label for s in loaded] == [
        'Точка',
        'Круг',
        'Прямоугольник',
        'Овал',
    ]
    assert [s.id for s in c.all()] == [s.id for s in loaded]


def test_dispatch_save_load():
    c = Canvas()
    dispatch(c, 'add circle 0 0 5')
    dispatch(c, 'add oval 1 1 2 3')

    with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
        path = f.name
    try:
        assert 'Сохранено 2' in dispatch(c, f'save {path}')
        c2 = Canvas()
        assert 'Загружено 2' in dispatch(c2, f'load {path}')
        assert len(c2.all()) == 2
    finally:
        os.unlink(path)


def test_dispatch_load_missing_file():
    assert 'не найден' in dispatch(Canvas(), 'load несуществующий.json')
