import pygame 
import sys
import time

from nonogram import X, O, Nonogram, NonogramAI

def max_task_num(tasks):
  max = 1
  for task in tasks: 
    if len(task) > max:
      max = len(task)
  return max


# Get data from the puzzle file
if len(sys.argv) != 2:
  sys.exit("Usage: python runner.py tree.txt")

# Get enough data to create the game board
height, width, prompt_x, ans, h_task, v_task = Nonogram.load_data(sys.argv[1])

# Create game and AI agent
game = Nonogram(height, width, prompt_x, ans)
ai = NonogramAI(height, width, h_task, v_task, prompt_x)
ai.get_next_line()

# # Keep track of revealed cells and crossed cells
# tiles = game.o_set
# crosses = game.x_set
# lost = False

lost = False

# Constants
WIDTH, HEIGHT = 600, 600
ROWS, COLS = height, width
H_TASK_NUM = max_task_num(h_task) # Maximum task num
V_TASK_NUM = max_task_num(v_task)

# Color
PINK = (237, 90, 154)
BLACK = (10, 10, 10)
WHITE = (255, 255, 255)
GRAY = (180, 180, 180)
BLUE = (97, 77, 247)

screen = pygame.display.set_mode((WIDTH, HEIGHT))  # WIN stands for window
pygame.display.set_caption("Nonogram")  # Will be displayed on the window frame


# Compute board size
# BOARD_PADDING = 30
BOARD_PADDING = 20
board_width = WIDTH - (BOARD_PADDING * 2)
board_height = HEIGHT - (BOARD_PADDING * 2)
cell_size = int(min(board_width / (COLS + H_TASK_NUM), board_height / (ROWS + V_TASK_NUM)))

# Used to draw the plain game board
board_origin = (
  HEIGHT - BOARD_PADDING - (ROWS * cell_size), 
  WIDTH - BOARD_PADDING - (COLS * cell_size)
)
# Used to calculate the position of tasks
task_origin = (
  WIDTH - BOARD_PADDING - ((COLS + H_TASK_NUM) * cell_size),
  HEIGHT - BOARD_PADDING - ((ROWS + V_TASK_NUM) * cell_size) 
)

# Add images
cross = pygame.image.load("assets/images/cross.png")
cross = pygame.transform.scale(cross, (cell_size, cell_size))

FPS = 60
clock = pygame.time.Clock()

# Keep the game running
while True: 
  # Fix the game refreshing rate
  clock.tick(FPS)
  
  # Check if game quit
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      sys.exit()

  screen.fill(WHITE)  # Background color

  # Draw h_tasks
  for i in range(ROWS):
    task_rect = pygame.Rect(
      task_origin[0],
      task_origin[1] + (V_TASK_NUM * cell_size) + (i * cell_size), 
      H_TASK_NUM * cell_size, cell_size
    )
    pygame.draw.rect(screen, WHITE, task_rect)
    pygame.draw.rect(screen, PINK, task_rect, 2)
  
  # Draw v_tasks
  for i in range(COLS):
    task_rect = pygame.Rect(
      task_origin[0] + (H_TASK_NUM * cell_size) + (i * cell_size),
      task_origin[1],
      cell_size, V_TASK_NUM * cell_size
    )
    pygame.draw.rect(screen, WHITE, task_rect)
    pygame.draw.rect(screen, PINK, task_rect, 2)

  # Get info from the game board
  tiles = game.o_set
  crosses = game.x_set

  # Draw board
  cells = []
  for i in range(ROWS):
    row = []
    for j in range(COLS):
      # Draw rectangle for cell
      rect = pygame.Rect(
        board_origin[0] + (j * cell_size),
        board_origin[1] + (i * cell_size),
        cell_size, cell_size
      )
      # Draw rectangle for tile
      tile_rect = pygame.Rect(
        board_origin[0] + j * cell_size + 2,
        board_origin[1] + i * cell_size + 2,
        cell_size - 4, cell_size - 4
      )

      pygame.draw.rect(screen, WHITE, rect)
      pygame.draw.rect(screen, BLUE, rect, 2)  # A thin boarder between cells

      # Display crosses or black tiles if needed
      if (i, j) in crosses: 
        screen.blit(cross, rect)
      elif (i, j) in tiles: 
        pygame.draw.rect(screen, BLACK, tile_rect)
      
      row.append(rect)  # So every small rect is store in a row, then in cells
    cells.append(row)   # Here, cells are used for detecting the collidepoint of the mouse

  # Check if won already
  if game.won():
    print("You have solved this puzzle, you won!!!")
    # Here, we can display text "WIN" if needed

  move = None
  symbol = None

  left, _, right = pygame.mouse.get_pressed()

  # Right-click to add a cross
  if right == 1: 
    mouse = pygame.mouse.get_pos()
    if not lost:
      for i in range(ROWS):
        for j in range(COLS):
          if cells[i][j].collidepoint(mouse) and (i, j) not in crosses:
            move = (i, j)
            symbol = X
  
  # Left-click to add a tile
  elif left == 1:
    mouse = pygame.mouse.get_pos()
    if not lost:
      for i in range(ROWS):
        for j in range(COLS):
          if cells[i][j].collidepoint(mouse) and (i, j) not in tiles:
            move = (i, j)
            symbol = O
    
  # Make move and update board
  if move != None:
    if game.check_move(symbol, move):
      game.update_board(symbol, move)
    else: 
      game.update_board(Nonogram.reverse_symbol(symbol), move)
      print("Wrong move!")  # Add some UI?
      game.hearts -= 1
      time.sleep(1)
    
    if game.hearts == 0:
      lost = True
      game.reset()

  pygame.display.flip()

