# Student, discipline and grade registry

A console registry for students, disciplines and grades with interchangeable memory, text and binary repositories.

## How it works

Domain records describe students, disciplines and grades. Repository classes provide lookup and persistence. Separate services coordinate student, discipline and grade operations. The console UI exposes add/remove/list/search. Faker supplies sample data; existing records are preserved during seeding.

## Architecture

Console/GUI → service/controller → repository → domain records. Modules communicate through their service APIs; data files stay in the project or configured repository path.

| Module | Main types |
|---|---|
| `src/domain/domain.py` | Student, Discipline, Grade, ValidationException, NotFoundException |
| `src/repository/repository.py` | BaseRepository, InMemoryRepository, TextFileRepository, BinaryFileRepository |
| `src/services/services.py` | StudentService, DisciplineService, GradeService |
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
python -m unittest -v src.tests.test
```

## Verification

Checked on 2026-10-09: syntax: passed, tests: passed, startup: passed.

## Refinements

- Seeded only missing records so restarting a persistent repository preserves existing data.
- Rejected duplicate IDs before they overwrite existing entities.
- Declared required Python dependencies.

Original assignment/project notes are preserved in [README.original.md](README.original.md).
