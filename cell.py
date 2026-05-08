import pygame

#settings
WIDTH = 800
COLS = 20
CELL_SIZE = WIDTH // COLS

WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
BLUE = (0, 100, 255)
YELLOW = (255, 255, 0)

#Cell class
class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col

        self.top = True
        self.right = True
        self.bottom = True
        self.left = True

        self.visited = False
        self.solved_visited = False
        self.dead_end = False
        self.in_path = False

    def draw(self, screen):
        x = self.col * CELL_SIZE
        y = self.row * CELL_SIZE

        if self.visited:
            pygame.draw.rect(screen, GREEN,
                             (x, y, CELL_SIZE, CELL_SIZE))
        if self.dead_end:
            pygame.draw.rect(screen, BLUE,
                             (x, y, CELL_SIZE, CELL_SIZE))
        if self.in_path:
            pygame.draw.rect(screen, YELLOW,
                             (x, y, CELL_SIZE, CELL_SIZE))
        if self.top:
            pygame.draw.line(screen, WHITE,
                             (x, y),
                             (x + CELL_SIZE, y), 2)

        if self.right:
            pygame.draw.line(screen, WHITE,
                             (x + CELL_SIZE, y),
                             (x + CELL_SIZE, y + CELL_SIZE), 2)
        if self.bottom:
            pygame.draw.line(screen, WHITE,
                             (x, y + CELL_SIZE),
                             (x + CELL_SIZE, y + CELL_SIZE), 2)

        if self.left:
            pygame.draw.line(screen, WHITE,
                             (x, y),
                             (x, y + CELL_SIZE), 2)

    #Generating Neighbors
    def get_unvisited_neighbors(self, grid):
        neighbors = []

        rows = len(grid)
        cols = len(grid[0])

        if self.row > 0: #UP
            top = grid[self.row - 1][self.col]
            if not top.visited:
                neighbors.append(top)

        if self.col < cols - 1: #RIGHT
            right = grid[self.row][self.col + 1]
            if not right.visited:
                neighbors.append(right)

        if self.row < rows - 1: #DOWN
            bottom = grid[self.row + 1][self.col]
            if not bottom.visited:
                neighbors.append(bottom)

        if self.col > 0: #LEFT
            left = grid[self.row][self.col - 1]
            if not left.visited:
                neighbors.append(left)
        return neighbors

    #Solver Meighbors
    def get_available_neighbors(self, grid):
        neighbors = []

        rows = len(grid)
        cols = len(grid[0])

        #UP
        if not self.top and self.row > 0:
            top = grid[self.row - 1][self.col]
            if not top.solved_visited:
                neighbors.append(top)

        #RIGHT
        if not self.right and self.col < cols - 1:
            right = grid[self.row][self.col + 1]
            if not right.solved_visited:
                neighbors.append(right)

        #DOWN
        if not self.bottom and self.row < rows - 1:
            bottom = grid[self.row + 1][self.col]
            if not bottom.solved_visited:
                neighbors.append(bottom)

        #LEFT
        if not self.left and self.col > 0:
            left = grid[self.row][self.col - 1]
            if not left.solved_visited:
                neighbors.append(left)

        return neighbors