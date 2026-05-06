*This project has been created as part of the 42 curriculum by nadoho, tfrances*

# A-MAZE-ING

## Description

A-MAZE-ING is a maze generation and solving project written in Python.
It generates a maze from a configuration file, solves it, and can display
the result in the terminal with colors.

The project also exposes a reusable module, `mazegen.py`, so the maze
generator can be imported and reused in another Python project.

## Instructions

### Requirements

- Python 3.8 or newer
- A virtual environment is recommended

### Build the package

```bash
python3 -m ensurepip --upgrade
python3 -m pip install build
python3 -m build --wheel
```

This creates a wheel file in `dist/`, for example:

```bash
dist/mazegen-1.0.0-py3-none-any.whl
```

### Install the reusable module

```bash
python3 -m pip install dist/mazegen-1.0.0-py3-none-any.whl
```

### Run the project

```bash
python3 a_maze_ing.py config.txt
```

## Configuration file

The configuration file is a plain text file with one `KEY=VALUE` pair per
line.

### Format

```text
WIDTH=<int>
HEIGHT=<int>
ENTRY=<row,col>
EXIT=<row,col>
OUTPUT_FILE=<filename>
PERFECT=<TRUE|FALSE>
SEED=<int>    # optional
```

### Description of each field

- `WIDTH`: number of columns in the maze
- `HEIGHT`: number of rows in the maze
- `ENTRY`: entry cell, written as `row,col`
- `EXIT`: exit cell, written as `row,col`
- `OUTPUT_FILE`: file used to save the generated maze and the solution
- `PERFECT`: `TRUE` for a perfect maze, `FALSE` to allow extra passages
- `SEED`: optional random seed for reproducible generation

### Example

```text
WIDTH=5
HEIGHT=20
ENTRY=3,3
EXIT=2,2
OUTPUT_FILE=maze.txt
PERFECT=TRUE
```

## Maze generation algorithm

The maze is generated using a depth-first search with recursive backtracking.
The algorithm starts from the entry cell, explores unvisited neighbors, and
removes walls between connected cells.

### Why this algorithm

- simple to implement and easy to maintain
- produces valid perfect mazes
- gives a clear path structure that is easy to solve afterward
- works well for this project size and constraints

When `PERFECT=False`, extra passages are opened after generation to create
loops and make the maze less linear.

## Reusable module

The reusable part of the project is the root module `mazegen.py`.

It exposes the class `MazeGenerator`, which can be imported like this:

```python
from mazegen import MazeGenerator

generator = MazeGenerator(width=10, height=8, seed=42, perfect=False)

print(generator.maze)
print(generator.solution)
print(generator.solution_directions)
```

### Available features

- `maze`: generated maze structure
- `solution`: shortest path between entry and exit
- `solution_directions`: path encoded with `N`, `E`, `S`, `W`
- `generate()`: generate a new maze
- `solve()`: compute the solution
- `regenerate()`: rebuild the maze with a new seed or a new `perfect` mode

The internal maze structure is a 2D grid of bitmasks and is not necessarily
the same format as the text output file.

## Team and project management

### Team roles

- nadoho: packaging, reusable module, documentation, integration work
- tfrances: maze generation logic, solving logic, output handling

### Planning

The work was planned in several stages:

1. implement the generator and solver
2. add file output and display logic
3. extract a reusable module
4. create the wheel build configuration
5. fix typing and lint issues
6. finalize documentation

The plan evolved as packaging and type-checking constraints were discovered.

### What worked well

- the maze generation and solving logic stayed separated
- the project could be reused as a standalone module
- the build process produced a valid wheel

### What could be improved

- cleaner separation between CLI code and library code
- more tests for edge cases and invalid configurations
- a richer API for displaying or exporting the maze

### Tools used

- Python
- `mypy`
- `flake8`
- `build`
- `pip`
- `uv`
- VS Code

## Resources

### References

- [Maze Generation — Recursive Backtracking](https://aryanab.medium.com/maze-generation-recursive-backtracking-5981bc5cc766)
- [Python packaging guide](https://packaging.python.org/)
- [PEP 517](https://peps.python.org/pep-0517/)
- [PEP 621](https://peps.python.org/pep-0621/)

### AI usage

AI was used to:

- clarify the packaging requirements
- draft and improve the README structure
- help document the reusable `mazegen.py` module
- assist with explanations of installation and usage

The implementation itself was kept under project control and validated with
local build and lint checks.
