import pygame
from random import choice, randint

# Constants for the screen dimensions and tile size
TILE = 100
GRID_WIDTH = 1000  # Width for the grid (left side)
GRID_HEIGHT = 902  # Height for the grid
CONTROL_PANEL_WIDTH = 200  # Width for the control panel (right side)

# Number of columns and rows based on the grid width and height
cols, rows = GRID_WIDTH // TILE, GRID_HEIGHT // TILE

pygame.init()
sc = pygame.display.set_mode((GRID_WIDTH + CONTROL_PANEL_WIDTH, GRID_HEIGHT))
clock = pygame.time.Clock()

# Load the candy icon image
candy_icon = pygame.image.load('assets/candy.png')
candy_icon = pygame.transform.scale(candy_icon, (TILE // 2, TILE // 2))  # Scale the candy icon to fit the tile size

# Cell class to represent each tile of the grid
class Cell:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
        self.visited = False

    def draw_current_cell(self):
        # Draw the current cell in brown when it's visited
        x, y = self.x * TILE, self.y * TILE
        pygame.draw.rect(sc, pygame.Color("saddlebrown"), (x + 2, y + 2, TILE + 2, TILE + 2))

    def draw(self):
        # Draw the cell
        x, y = self.x * TILE, self.y * TILE
        if self.visited:
            pygame.draw.rect(sc, pygame.Color('black'), (x, y, TILE, TILE))  # Visited cells are black

        # Draw the walls around the cell
        if self.walls['top']:
            pygame.draw.line(sc, pygame.Color('darkorange'), (x, y), (x + TILE, y), 2)
        if self.walls['right']:
            pygame.draw.line(sc, pygame.Color('darkorange'), (x + TILE, y), (x + TILE, y + TILE), 2)
        if self.walls['bottom']:
            pygame.draw.line(sc, pygame.Color('darkorange'), (x + TILE, y + TILE), (x, y + TILE), 2)
        if self.walls['left']:
            pygame.draw.line(sc, pygame.Color('darkorange'), (x, y + TILE), (x, y), 2)

    def check_cell(self, x, y):
        # Ensure that the neighbor is within bounds
        if x < 0 or x >= cols or y < 0 or y >= rows:
            return None
        return grid_cells[x + y * cols]

    def check_neighbours(self):
        # Check all the neighbors and return the unvisited ones
        neighbors = []
        top = self.check_cell(self.x, self.y - 1)
        right = self.check_cell(self.x + 1, self.y)
        bottom = self.check_cell(self.x, self.y + 1)
        left = self.check_cell(self.x - 1, self.y)
        if top and not top.visited:
            neighbors.append(top)
        if right and not right.visited:
            neighbors.append(right)
        if bottom and not bottom.visited:
            neighbors.append(bottom)
        if left and not left.visited:
            neighbors.append(left)
        return choice(neighbors) if neighbors else None


def remove_walls(current, next):
    # Remove walls between the current cell and the next
    dx = current.x - next.x
    if dx == 1:
        current.walls['left'] = False
        next.walls['right'] = False
    elif dx == -1:
        current.walls['right'] = False
        next.walls['left'] = False

    dy = current.y - next.y
    if dy == 1:
        current.walls['top'] = False
        next.walls['bottom'] = False
    elif dy == -1:
        current.walls['bottom'] = False
        next.walls['top'] = False


# Function to reset the maze
def reset_maze():
    global grid_cells, current_cell, stack, maze_completed, candies
    grid_cells = [Cell(col, row) for row in range(rows) for col in range(cols)]
    current_cell = grid_cells[0]
    stack = []
    maze_completed = False
    candies = []  # Reset the candies


def generate_candies():
    global candies
    candies = []
    for _ in range(20):
        # Generate random positions for candies (x, y)
        x = randint(0, cols - 1)
        y = randint(0, rows - 1)
        candies.append((x, y))  # Store as (x, y) positions


# Create grid of cells
grid_cells = [Cell(col, row) for row in range(rows) for col in range(cols)]
current_cell = grid_cells[0]
stack = []
maze_completed = False
candies = []  # This will store the positions of the candies

class Button:
    def __init__(self, x, y, width, height, color, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.font = None
        self.set_font()

    def set_font(self):
        # Dynamically adjust the font size based on button dimensions
        font_size = min(self.rect.width, self.rect.height) // 2  # Adjust the factor as needed
        self.font = pygame.font.SysFont(None, font_size)

    def draw(self):
        pygame.draw.rect(sc, self.color, self.rect)
        # Adjust the font if the size of the button changes
        self.set_font()
        text_surface = self.font.render(self.text, True, pygame.Color('white'))
        text_rect = text_surface.get_rect(center=self.rect.center)
        sc.blit(text_surface, text_rect)

    def is_pressed(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False

# Create the reset button in the control panel area
reset_button = Button(GRID_WIDTH + 50, 20, CONTROL_PANEL_WIDTH - 100, 50, pygame.Color('green'), "Reset Maze")
# Create the "Generate Candies" button
generate_candies_button = Button(GRID_WIDTH + 50, 80, CONTROL_PANEL_WIDTH - 100, 50, pygame.Color('purple'), "Generate Candies")

while True:
    sc.fill(pygame.Color('darkslategray'))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # Check if the reset button is pressed
        if reset_button.is_pressed(event):
            reset_maze()

        # Check if the generate candies button is pressed
        if generate_candies_button.is_pressed(event):
            generate_candies()

    # Draw the reset and generate candies buttons
    reset_button.draw()
    generate_candies_button.draw()

    # Draw all cells and their walls in the grid (on the left side of the screen)
    [cell.draw() for cell in grid_cells]
    current_cell.visited = True
    current_cell.draw_current_cell()

    # Draw candies using the candy icon
    for candy in candies:
        x, y = candy
        # Draw the candy icon in the center of the grid cell
        sc.blit(candy_icon, (x * TILE + TILE // 4, y * TILE + TILE // 4))

    # Find the next unvisited neighbor and move there
    next_cell = current_cell.check_neighbours()
    if next_cell:
        next_cell.visited = True
        stack.append(current_cell)
        remove_walls(current_cell, next_cell)
        current_cell = next_cell
    elif stack:
        # If no unvisited neighbor, backtrack
        current_cell = stack.pop()

    # Stop the maze generation once all cells are visited
    if not stack and not any(cell.visited == False for cell in grid_cells):
        maze_completed = True

    pygame.display.flip()
    clock.tick(30)

    # Continue showing the maze even after it's completed
    if maze_completed:
        continue
