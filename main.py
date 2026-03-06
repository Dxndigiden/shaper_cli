from app.canvas.canvas import Canvas
from app.cli.repl import run_repl


def main() -> None:
    canvas = Canvas()
    run_repl(canvas)


if __name__ == '__main__':
    main()
