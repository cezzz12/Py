# Attendance and grade student manager

A console student manager that adds records, sorts/displays students, applies attendance-based grade bonuses, and searches names.

## How it works

`Student` defines a record; `StudentRepository` loads/saves the student text file. `StudentService` implements validation and bonus/search rules. `StudentUI` writes activity/results to `results.txt`; `main.py` assembles the layers.

## Architecture

Console/GUI → service/controller → repository → domain records. Modules communicate through their service APIs; data files stay in the project or configured repository path.

| Module | Main types |
|---|---|
| `domain/domain.py` | Student |
| `repository/repository.py` | StudentRepository |
| `service/service.py` | StudentService |
| `ui/ui.py` | StudentUI |

## Run

Requires Python 3.10 or newer. From this project folder:

```sh
python -m venv .venv
# Activate .venv using your shell
python main.py
```

## Verification

Checked on 2026-10-09: syntax: passed, startup: passed.

