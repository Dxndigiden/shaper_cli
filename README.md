# shaper_cli 🔷

Векторный редактор в терминале. 
Создавай фигуры, удаляй, смотри, сохраняй и загружай список - всё через CLI.

## Что умеет

- ➕ Добавлять фигуры — точка, отрезок, круг, квадрат, овал, прямоугольник
- 🗑️ Удалять фигуры по id
- 📋 Выводить список вcех фигур
- 📐 Считать длину отрезка и площадь фигур автоматически
- 💾 Сохранять и загружать в json файл
- 📖 Выводить справку

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
> add oval 0 0 4 2
> add rect 0 2 2 8
> remove <id>
> list
> save <имя_файла.json>
> load <имя_файла.json>
> help
> exit
```

## Тесты

```bash

pytest
```

Автор — [Dxndigiden](https://github.com/Dxndigiden)