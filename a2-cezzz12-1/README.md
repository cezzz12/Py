# Bakery inventory manager (C)

A C console application for managing materials, suppliers, quantities and expiration dates. Its placement in the Py repository follows the requested source-folder mapping.

## How it works

`domain.c` defines material records; `vector.c` provides dynamic storage and destruction callbacks. `repository.c` owns records; `service.c` implements inventory operations and history; `ui.c` provides menus. CMake builds the C11 executable.

## Architecture

User input → UI → service → repository → domain records/storage.

## Build and run

Requires CMake 3.16 or newer and a C11 compiler.

Run these commands from this project folder:

```sh
cmake -S . -B build -DCMAKE_BUILD_TYPE=Debug
cmake --build build
./build/a2-cezzz12-1
```

On Windows the executable has a `.exe` extension; multi-configuration generators may place it under `build/Debug/`. Run from the project folder so bundled text files can be located.

## Tests

Build the `material_tests` target and run `ctest --test-dir build --output-on-failure`.

## Verification

Checked on 2026-10-09: build: passed, tests: passed, runtime: passed.

## Refinements

- Made CMake portable; removed local Qt paths/deployment assumptions and unused dependencies.
- Built tests as separate translation units rather than including .c files, preventing duplicate internal helper definitions.

Original assignment/project notes are preserved in [README.original.md](README.original.md).
