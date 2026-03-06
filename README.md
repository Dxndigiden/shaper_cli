# shaper_cli 🔷

Векторный редактор в терминале. 
Создавай фигуры, удаляй, смотри список — всё через CLI.

## Что умеет

- ➕ Добавлять фигуры — точка, отрезок, круг, квадрат
- 🗑️ Удалять фигуры по id
- 📋 Выводить список вcех фигур
- 📐 Считать длину отрезка и площадь фигур автоматически

## Установка и запуск

Нужен только Python 3.10+, зависимости только для тестов (pip install pytest).

```bash
git clone https://github.com/Dxndigiden/shaper_cli.git
cd shaper_cli
python main.py
```

## Использование

```
> add point 10 20
> add segment 0 0 3 4
> add circle 5 5 3
> add square 0 0 4
> list
> remove <id>
> exit
```

## Тесты

```bash

pytest
```

Автор — [Dxndigiden](https://github.com/Dxndigiden)