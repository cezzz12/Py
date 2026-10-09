# Computer networks quiz application

A console quiz with timed testing, practice mode, review of mistakes and persisted question status.

## How it works

The JSON repository loads question sets and tracks answer status. The controller manages scoring and question selection. The view controller handles menus, prompts and timed sessions. `Collection/` contains additional question banks; the main entry point starts the console view.

## Architecture

Console/GUI → service/controller → repository → domain records. Modules communicate through their service APIs; data files stay in the project or configured repository path.

| Module | Main types |
|---|---|
| `controller/controller.py` | Controller |
| `repository/repository.py` | Repository |
| `view_controller/view_controller.py` | Bcolors, View |

## Run

Requires Python 3.10 or newer. From this project folder:

```sh
python -m venv .venv
# Activate .venv using your shell
python main.py
```

## Verification

Checked on 2026-10-09: syntax: passed, startup: passed.

Original assignment/project notes are preserved in [README.original.md](README.original.md).
