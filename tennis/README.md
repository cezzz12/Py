# Tennis tournament organizer

A console tournament organizer that ranks players, runs qualification matches and advances winners through an elimination draw.

## How it works

The player repository loads records and sorts by strength. `TournamentService` pairs players and resolves user-selected match winners. `TournamentUI` builds the main draw from qualification winners and seeded players. Qualification reduces the field to a power of two; each match winner gains strength.

## Architecture

Console/GUI → service/controller → repository → domain records. Modules communicate through their service APIs; data files stay in the project or configured repository path.

| Module | Main types |
|---|---|
| `domain/domain.py` | Player |
| `repository/repository.py` | PlayerRepository |
| `service/service.py` | TournamentService |
| `ui/ui.py` | TournamentUI |

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

- Corrected qualification rounds for power-of-two fields and validated match-winner input.
- Handled an empty qualification group without returning the whole player list.
- Removed qualification losers from the main draw so players cannot enter twice.

