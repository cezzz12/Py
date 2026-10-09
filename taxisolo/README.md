# Taxi orders and income manager

A file-backed console application for recording driver orders, listing drivers/orders, and calculating driver income.

## How it works

Driver and order domain records are loaded by separate repositories. `TaxiService` validates and records orders and computes income. `TaxiUI` presents the menu; `main.py` creates sample files only when missing.

## Architecture

Console/GUI → service/controller → repository → domain records. Modules communicate through their service APIs; data files stay in the project or configured repository path.

| Module | Main types |
|---|---|
| `domain/domain.py` | Driver, Order |
| `repository/repository.py` | DriverRepository, OrderRepository |
| `service/service.py` | TaxiService |
| `ui/ui.py` | TaxiUI |

## Run

Requires Python 3.10 or newer. From this project folder:

```sh
python -m venv .venv
# Activate .venv using your shell
python main.py
```

## Verification

Checked on 2026-10-09: syntax: passed, startup: passed.

