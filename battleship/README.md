# Battleship console game

A six-by-six Battleship game against the computer, with ship placement, attacks and separate targeting/player boards.

## How it works

`Board` tracks ships and attacks and `Position` parses coordinates such as A0. `GameRepository` stores each game state in memory. `GameService` handles setup and turns, including computer moves. `GameUI` displays boards using texttable; `main.py` dispatches commands.

## Architecture

Console/GUI → service/controller → repository → domain records. Modules communicate through their service APIs; data files stay in the project or configured repository path.

| Module | Main types |
|---|---|
| `domain/domain.py` | Board, Position |
| `repository/repository.py` | GameRepository |
| `service/service.py` | GameService |
| `ui/ui.py` | GameUI |

## Run

Requires Python 3.10 or newer. From this project folder:

```sh
python -m venv .venv
# Activate .venv using your shell
python -m pip install -r requirements.txt
python main.py
```

Use `ship A0`, `ship B1`, `start`, then `attack C2`. Coordinates range A–F and 0–5. Use `quit` to exit.

## Verification

Checked on 2026-10-09: syntax: passed, startup: passed.

## Refinements

- Declared required Python dependencies.
- Aligned repository method names and state keys with the game service.
- Aligned board/position method names and attack markers with the implemented domain.
- Validated two-character board coordinates against the six-by-six board.

