import pytest

from app.canvas.canvas import Canvas
from app.cli.repl import _EXIT, dispatch
from app.models.base import Point
from app.models.shapes import Circle, PointShape, Segment, Square


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
    with pytest.raises(ValueError):
        Circle(center=Point(0, 0), radius=0)


def test_square_area():
    s = Square(origin=Point(0, 0), side=4)
    assert s.area == 16.0


def test_square_bad_side():
    with pytest.raises(ValueError):
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
