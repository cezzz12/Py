# Complex-number command-line manager

A command-driven application for adding, inserting, removing, replacing, filtering and listing complex numbers, with undo history.

## How it works

`src/functions.py` contains operations on lists of complex numbers. `src/ui.py` parses commands and maintains history. `src/start.py` launches the UI; `src/test.py` exercises core operations. `texttable` formats list output.

## Architecture

Console/GUI → service/controller → repository → domain records. Modules communicate through their service APIs; data files stay in the project or configured repository path.

## Run

Requires Python 3.10 or newer. From this project folder:

```sh
python -m venv .venv
# Activate .venv using your shell
python -m pip install -r requirements.txt
python src/start.py
```

## Tests

```sh
cd src
python test.py
```

## Verification

Checked on 2026-10-09: syntax: passed, tests: passed, startup: passed.

## Refinements

- Removed an unused documentation dependency from the runtime imports.
- Declared required Python dependencies.

Original assignment/project notes are preserved in [README.original.md](README.original.md).
