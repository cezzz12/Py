# Student registry with command history and statistics

A student/discipline/grade console registry with undo/redo and statistics for failing students, best students and best disciplines.

## How it works

`src/command.py` defines reversible add/remove commands and history stacks. Services construct domain records and send mutations through the command manager. `StatisticsService` computes aggregates from repository data. Memory, text and binary repositories implement storage; the UI presents commands and statistics.

## Architecture

Console/GUI → service/controller → repository → domain records. Modules communicate through their service APIs; data files stay in the project or configured repository path.

| Module | Main types |
|---|---|
| `src/command.py` | Command, CommandManager, AddEntityCommand, RemoveEntityCommand |
| `src/domain/domain.py` | Student, Discipline, Grade, ValidationException, NotFoundException |
| `src/repository/repository.py` | BaseRepository, InMemoryRepository, TextFileRepository, BinaryFileRepository |
| `src/services/services.py` | StudentService, DisciplineService, GradeService, StatisticsService |
| `src/ui/ui.py` | ConsoleUI |

## Run

Requires Python 3.10 or newer. From this project folder:

```sh
python -m venv .venv
# Activate .venv using your shell
python -m pip install -r requirements.txt
python -m src.main
```

## Tests

```sh
python -m unittest -v src.test.test
```

## Verification

Checked on 2026-10-09: syntax: passed, tests: passed, startup: passed.

## Refinements

- Seeded only missing records so restarting a persistent repository preserves existing data.
- Rejected duplicate IDs before they overwrite existing entities.
- Declared required Python dependencies.
- Aligned service signatures with the launcher/UI and validated grade references and range.
- Connected statistics menu actions to the implemented statistics service.

Original assignment/project notes are preserved in [README.original.md](README.original.md).
