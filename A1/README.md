# Graph algorithms library and console explorer

A directed, weighted graph library with an interactive explorer, shortest paths, connected components and spanning-tree algorithms.

## How it works

`graph.py` owns inbound/outbound adjacency maps and edge costs, plus file I/O and random generation. `bfs.py` and `dijkstra.py` implement shortest-path algorithms. `service.py` includes connected components, Floyd–Warshall and Prim. `ui.py` presents the operations; `tests.py` verifies core graph behavior.

## Architecture

Console/GUI → service/controller → repository → domain records. Modules communicate through their service APIs; data files stay in the project or configured repository path.

| Module | Main types |
|---|---|
| `exceptions.py` | VertexError, EdgeError |
| `graph.py` | Graph |
| `ui.py` | UI |

## Run

Requires Python 3.10 or newer. From this project folder:

```sh
python -m venv .venv
# Activate .venv using your shell
python ui.py
```

## Tests

```sh
python -m unittest -v tests
```

## Verification

Checked on 2026-10-09: syntax: passed, tests: passed, startup: passed.

