# Flight scheduling console application

A file-backed flight schedule manager with flight validation and airport-activity reporting.

## How it works

Domain types define flights and validate times. `FlightRepository` reads records from `flights`; `FlightService` implements changes and reporting. `UserInterface` presents the menu. The entry point locates the data file relative to its own directory.

## Architecture

Console/GUI → service/controller → repository → domain records. Modules communicate through their service APIs; data files stay in the project or configured repository path.

| Module | Main types |
|---|---|
| `domain/domain.py` | Flight, FlightValidator, FlightException |
| `repository/repository.py` | FlightRepository |
| `service/service.py` | FlightService, ServiceValidator, ServiceException |
| `ui/ui.py` | UserInterface |

## Run

Requires Python 3.10 or newer. From this project folder:

```sh
python -m venv .venv
# Activate .venv using your shell
python start.py
```

## Verification

Checked on 2026-10-09: syntax: passed, startup: passed.

## Refinements

- Located bundled data relative to the entry point instead of the original user directory.
- Guarded the entry point so importing the module does not start an input loop.
- Repaired the malformed sample arrival time that prevented the application from starting.

