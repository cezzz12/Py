# Space attack console game

A grid-based space game with Earth, asteroids and alien ships, driven by start/fire commands.

## How it works

`src/domain` models boards and positions. `GameRepository` stores game state. `GameService` generates the board and processes attacks/computer behavior. `GameUI` renders it using texttable; the package entry point dispatches commands.

## Architecture

Console/GUI → service/controller → repository → domain records. Modules communicate through their service APIs; data files stay in the project or configured repository path.

| Module | Main types |
|---|---|
| `src/domain/domain.py` | Board, Position |
| `src/repository/repository.py` | GameRepository |
| `src/service/service.py` | GameService |
| `src/ui/ui.py` | GameUI |

## Run

Requires Python 3.10 or newer. From this project folder:

```sh
python -m venv .venv
# Activate .venv using your shell
python -m pip install -r requirements.txt
python -m src.start
```

Use `start`, `fire A0`, and `quit` as prompted.

## Verification

Checked on 2026-10-09: syntax: passed, startup: passed.

## Refinements

- Made entry-point imports consistent with the package imports used by the game modules.
- Declared required Python dependencies.

Original assignment/project notes are preserved in [README.original.md](README.original.md).
