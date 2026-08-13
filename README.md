*This project has been created as part of the 42 curriculum by sel-haso.*

# Fly-in

## Description
Fly-in is a drone-routing simulator built in Python. The program reads a map file describing hubs, connections, capacities, and movement restrictions, then simulates a fleet of drones moving from a starting hub to a target hub while respecting all constraints.

The objective is to minimize the total number of simulation turns while obeying:

- zone capacities,
- connection capacities,
- path costs depending on zone types,
- restricted-zone transit rules,
- collision and occupancy constraints.

This project is built around an object-oriented architecture and uses a graph model to explore available routes before the simulation runs turn by turn.

## Project goal
The system is designed to:

- parse structured map files,
- validate all generated objects,
- construct a weighted graph,
- compute candidate paths,
- schedule drone movement without conflicts,
- display the simulation in a visual interface.

The challenge is not only to find a path, but also to schedule movements efficiently so drones can move in parallel without blocking each other.

## Architecture overview
The project is split into several layers:

- `parser.py`: reads the input map file and validates the format.
- `validator.py`: converts raw parsed data into proper `Zone` and `Connection` objects.
- `graph_builder.py`: builds the navigation graph and assigns movement weights.
- `path_finder.py`: searches the graph for viable paths and ranks them by cost.
- `path.py`: identifies route metadata such as total cost, bottleneck, and restricted-zone count.
- `simulator.py`: runs the turn-based simulation and enforces movement constraints.
- `visualizer.py`: renders the map and drones in a dynamic interface.
- `main.py`: launches the program from the command line.

## Instructions
### Installation
Run:

```bash
make install
```

This installs the required Python dependencies such as `pygame`, `flake8`, and `mypy`.

### Running the simulation
```bash
make run
```

Or directly:

```bash
python main.py maps/easy/01_linear_path.txt
```

### Debug mode
```bash
make debug
```

### Cleaning artifacts
```bash
make clean
```

### Linting and typing
```bash
make lint
```

This runs `flake8` and `mypy` with the project’s required checks.

## Algorithm strategy
The route logic is built in a simple layered way:

1. The parser reads the map and checks syntax.
2. The validator converts raw entries into structured objects.
3. The graph builder creates a graph where each edge is weighted by movement cost.
4. The path finder explores all possible routes from start to end and orders them by cost.
5. The simulator assigns drones to valid routes and advances the simulation turn by turn.

The simulation includes the following decisions per turn:

- if a drone can move to an adjacent zone, it may do so,
- if the next zone is restricted, the drone enters a connection-based transit state,
- if the destination is blocked or saturated, the drone waits,
- if the end hub is reached, the drone is marked as delivered.

This approach preserves the project’s original behavior while keeping the data flow readable and straightforward.

## Visualization and user experience
The visualizer is designed to make the simulation easier to understand at a glance. It renders:

- connected zones as a network,
- movement links between them,
- drone markers moving along paths,
- a bottom summary panel with the current turn and active drone information.

The display uses a more polished, modern style compared to a plain graph view: deeper blue background, lighter route lines, stronger zone emphasis, and a clear animation flow. This improves readability and gives a cleaner impression of what is happening in each simulation turn.

The interface also shows the turn counter and current state summary at the bottom of the screen so the viewer can immediately understand what is happening during the run.

## Example input and output
Example map file:

```text
nb_drones: 2
start_hub: start 0 0
hub: mid 2 0
hub: safe 4 0
end_hub: goal 6 0
connection: start-mid
connection: mid-safe
connection: safe-goal
```

The output is a turn-by-turn list of drone movement events, for example:

```text
Turn 1: D1-mid D2-mid
Turn 2: D1-safe D2-safe
Turn 3: D1-goal D2-goal
```

This is a simplified demonstration of the simulation format and the final result expected by the project.

## Resources
### References
- Python official documentation: https://docs.python.org/3/
- Pygame documentation: https://www.pygame.org/docs/
- Mypy documentation: https://mypy.readthedocs.io/
- Graph theory and pathfinding introduction: https://en.wikipedia.org/wiki/Graph_theory

### AI usage
AI was used as a support tool for:

- code review and refactoring suggestions,
- improving naming clarity,
- checking consistency across modules,
- polishing the project README and visualization description.

The core simulation logic, algorithmic decisions, and pathfinding rules were kept under the project’s original implementation and were not replaced by a new strategy.

## Notes
The project remains intentionally simple and beginner-friendly. The goal is to make the code easier to read and understand, while preserving the original behavior, route optimization logic, capacities, and movement constraints described in the project subject.
