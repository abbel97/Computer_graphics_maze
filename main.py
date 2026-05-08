import pygame
import sys
import random

# Initializing pygame
pygame.init()

# SETTINGS
WIDTH = 800
HEIGHT = 800

ROWS = 20
COLS = 20

CELL_SIZE = WIDTH // COLS

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

RED = (255, 0, 0)
GREEN = (0, 200, 0)
LIGHT_BLUE = (173, 216, 230)
BLUE = (0, 0, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Generator & Solver")

clock = pygame.time.Clock()

# CELL CLASS
class Cell:
    def __init__(self, row, col):

        self.row = row
        self.col = col

        # Walls
        self.top = True
        self.right = True
        self.bottom = True
        self.left = True

        # Maze generation
        self.visited = False

        # Maze solving
        self.solved_visited = False
        self.dead_end = False
        self.in_path = False

    def draw(self):
        x = self.col * CELL_SIZE
        y = self.row * CELL_SIZE

        # Background coloring
        if self.visited:
            pygame.draw.rect(
                screen,GREEN,
                (x, y, CELL_SIZE, CELL_SIZE))

        if self.dead_end:
            pygame.draw.rect(
                screen, LIGHT_BLUE,(x, y, CELL_SIZE, CELL_SIZE))

        if self.in_path:
            pygame.draw.rect(
                screen, BLUE, (x, y, CELL_SIZE, CELL_SIZE))

        # Draw walls
        if self.top:
            pygame.draw.line(
                screen, WHITE,
                (x, y),
                (x + CELL_SIZE, y),
                2 )

        if self.right:
            pygame.draw.line(
                screen,
                WHITE,
                (x + CELL_SIZE, y),
                (x + CELL_SIZE, y + CELL_SIZE),
                2)

        if self.bottom:
            pygame.draw.line(
                screen,
                WHITE,
                (x, y + CELL_SIZE),
                (x + CELL_SIZE, y + CELL_SIZE),
                2)

        if self.left:
            pygame.draw.line(
                screen,
                WHITE,
                (x, y),
                (x, y + CELL_SIZE),
                2)

    # GENERATION NEIGHBORS
    def get_unvisited_neighbors(self):
        neighbors = []

        # UP
        if self.row > 0:
            top = grid[self.row - 1][self.col]

            if not top.visited:
                neighbors.append(top)

        # RIGHT
        if self.col < COLS - 1:
            right = grid[self.row][self.col + 1]

            if not right.visited:
                neighbors.append(right)

        # DOWN
        if self.row < ROWS - 1:
            bottom = grid[self.row + 1][self.col]

            if not bottom.visited:
                neighbors.append(bottom)

        # LEFT
        if self.col > 0:
            left = grid[self.row][self.col - 1]

            if not left.visited:
                neighbors.append(left)
        return neighbors

    # SOLVER NEIGHBORS

    def get_available_neighbors(self):
        neighbors = []

        # UP
        if not self.top and self.row > 0:
            top = grid[self.row - 1][self.col]

            if not top.solved_visited:
                neighbors.append(top)

        # RIGHT
        if not self.right and self.col < COLS - 1:
            right = grid[self.row][self.col + 1]

            if not right.solved_visited:
                neighbors.append(right)

        # DOWN
        if not self.bottom and self.row < ROWS - 1:
            bottom = grid[self.row + 1][self.col]

            if not bottom.solved_visited:
                neighbors.append(bottom)

        # LEFT
        if not self.left and self.col > 0:
            left = grid[self.row][self.col - 1]

            if not left.solved_visited:
                neighbors.append(left)

        return neighbors


# REMOVE WALLS
def remove_walls(current, next_cell):
    dx = current.col - next_cell.col
    dy = current.row - next_cell.row

    # RIGHT
    if dx == -1:
        current.right = False
        next_cell.left = False

    # LEFT
    elif dx == 1:
        current.left = False
        next_cell.right = False

    # DOWN
    elif dy == -1:
        current.bottom = False
        next_cell.top = False

    # UP
    elif dy == 1:
        current.top = False
        next_cell.bottom = False


# CREATE GRID
grid = []

for row in range(ROWS):
    current_row = []

    for col in range(COLS):
        current_row.append(Cell(row, col))
    grid.append(current_row)


# MAZE GENERATION SETUP
generation_stack = []

current = grid[0][0]
current.visited = True

maze_generated = False


# MAZE SOLVER SETUP
start_cell = grid[0][0]
end_cell = grid[ROWS - 1][COLS - 1]

solver_stack = []

solver_current = start_cell
solver_current.solved_visited = True

maze_solved = False

# Creating entrance and exit
start_cell.left = False
end_cell.right = False


# MAIN LOOP
running = True
while running:
    screen.fill(BLACK)

    # Draw maze
    for row in grid:
        for cell in row:
            cell.draw()

    # GENERATE MAZE
    if not maze_generated:
        neighbors = current.get_unvisited_neighbors()

        if neighbors:
            next_cell = random.choice(neighbors)
            generation_stack.append(current)

            remove_walls(current, next_cell)

            current = next_cell
            current.visited = True

        elif generation_stack:
            current = generation_stack.pop()

        else:
            maze_generated = True

    # SOLVE MAZE
    elif not maze_solved:

        if solver_current == end_cell:
            maze_solved = True
            for cell in solver_stack:
                cell.in_path = True

        else:
            neighbors = solver_current.get_available_neighbors()
            if neighbors:
                next_cell = random.choice(neighbors)

                solver_stack.append(solver_current)

                solver_current = next_cell
                solver_current.solved_visited = True

            elif solver_stack:
                solver_current.dead_end = True

                solver_current = solver_stack.pop()

    # DRAWING SOLVER CURRENT POSITION
    x = solver_current.col * CELL_SIZE
    y = solver_current.row * CELL_SIZE

    pygame.draw.circle(
        screen,
        RED,
        (x + CELL_SIZE // 2, y + CELL_SIZE // 2),
        CELL_SIZE // 4
    )

    # EVENTS
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()
    clock.tick(30)

pygame.quit()
sys.exit()