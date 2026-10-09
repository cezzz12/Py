# Train ticket and income manager

A file-backed console application for train routes, ticket sales, total income and route reports.

## How it works

Domain records describe routes and validate fields. `RouteRepository` owns route data; `RouteService` prices/sells tickets and builds reports. `UserInterface` presents the menu. The entry point uses the bundled `routes` file relative to the project directory.

## Architecture

Console/GUI → service/controller → repository → domain records. Modules communicate through their service APIs; data files stay in the project or configured repository path.

| Module | Main types |
|---|---|
| `domain/domain.py` | Route, RouteValidator, RouteException |
| `repository/repository.py` | RouteRepository, RepositoryException |
| `service/service.py` | RouteService, ServiceException, ServiceValidator |
| `ui/ui.py` | UserInterface |

## Run

Requires Python 3.10 or newer. From this project folder:

```sh
python -m venv .venv
# Activate .venv using your shell
python main.py
```

## Verification

Checked on 2026-10-09: syntax: passed, startup: passed.

## Refinements

- Located bundled data relative to the entry point instead of the original user directory.
- Guarded the entry point so importing the module does not start an input loop.
- Added a clean exit option to the train application.

