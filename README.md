# Maze Generator and Solver

| Name              | ID           |
|-------------------|-------------|
| Abel Tamerat      | UGR/4812/16 |

This project generates and solves a maze using Python and Pygame.

## Features

- Random maze generation
- DFS (Depth First Search)
- Stack-based backtracking
- Animated wall carving
- Animated maze solving
- Dead-end visualization

## Technologies

- Python
- Pygame

## How It Works

The maze is generated using Recursive Backtracking DFS.

Each cell begins with all four walls intact.
A virtual mouse randomly visits neighboring cells and removes walls between them.

The solver then traverses the maze using another DFS algorithm with backtracking.

## Run

```bash
pip install -r requirements.txt
python main.py


