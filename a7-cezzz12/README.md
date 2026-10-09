# Student registry with persistence and undo

A student registry supporting memory, text-file and binary-file repositories, filtering by group, and undo of the last operation.

## How it works

`src/domain` defines students. Repository implementations store the same student model using three persistence strategies. `StudentService` validates unique IDs and performs filtering/undo. `src/ui` implements the menus and the launcher. Binary storage uses pickle and should only load files created by this application.

## Architecture

Console/GUI → service/controller → repository → domain records. Modules communicate through their service APIs; data files stay in the project or configured repository path.

| Module | Main types |
|---|---|
| `src/domain/domain.py` | Student |
| `src/repository/repository.py` | StudentRepositoryInMemory, StudentRepositoryTextFile, StudentRepositoryBinary |
| `src/services/services.py` | StudentService |
| `src/ui/ui.py` | UserInterface |

## Run

Requires Python 3.10 or newer. From this project folder:

```sh
python -m venv .venv
# Activate .venv using your shell
python -m src.ui.main
```

## Tests

```sh
python -m unittest -v src.ui.tests
```

## Verification

Checked on 2026-10-09: syntax: passed, tests: passed, startup: passed.

## Refinements

- Replaced an obsolete launcher using nonexistent classes with the implemented UI entry point.
- Added menu exit and prevented repeated undo from accidentally removing earlier records.
- Preserved existing file data on restart instead of replacing lists containing fewer than ten students.
- Updated stale tests to exercise the actual service API, duplicate validation, filter/undo and persistence after restart.

Original assignment/project notes are preserved in [README.original.md](README.original.md).
