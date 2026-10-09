# Connect Four with console and Tkinter interfaces

A Connect Four game with interchangeable console and graphical interfaces.

## How it works

`domain` defines cell state, positions and the board. `repository` owns the current board; `service` applies moves and computer-play decisions. `ui` implements console interaction and `gui.py` implements Tkinter interaction. Board and service unit tests are included.

## Architecture

Console/GUI → service/controller → repository → domain records. Modules communicate through their service APIs; data files stay in the project or configured repository path.

| Module | Main types |
|---|---|
| `domain/domain.py` | CellState, Position, Board |
| `gui.py` | GUI |
| `repository/repository.py` | BoardRepository |
| `service/service.py` | GameService |
| `ui/ui.py` | ConsoleUI |

## Run

Requires Python 3.10 or newer. From this project folder:

```sh
python -m venv .venv
# Activate .venv using your shell
python main.py
```

Choose console or GUI from the menu. The graphical interface requires Tkinter (`python3-tk` on some Linux installations).

## Tests

```sh
python -m unittest -v domain.test_domain service.test_service
```

## Verification

Checked on 2026-10-09: syntax: passed, tests: passed, startup: passed.

## Refinements

- Loaded Tkinter only when the graphical interface is selected, allowing console use without GUI libraries.

Original assignment/project notes are preserved in [README.original.md](README.original.md).
