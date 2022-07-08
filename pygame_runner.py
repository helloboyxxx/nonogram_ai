from curses.ascii import HT
from tkinter.tix import ROW
import pygame 
import sys
import time

from nonogram import Nonogram

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
# ai = MinesweeperAI(height=HEIGHT, width=WIDTH)
game = Nonogram(height, width, prompt_x, ans, h_task, v_task)

# Keep track of revealed cells and crossed cells
boxes = set()
crosses = set()
lost = False

boxes.add((1, 1))
crosses.add((2, 2))


# Constants
WIDTH, HEIGHT = 600, 600
ROWS, COLS = height, width
H_TASK_NUM = max_task_num(h_task) # Space for task to display
V_TASK_NUM = max_task_num(v_task)

PINK = (237, 90, 154)
BLACK = (10, 10, 10)
WHITE = (255, 255, 255)
GRAY = (180, 180, 180)
BLUE = (97, 77, 247)

screen = pygame.display.set_mode((WIDTH, HEIGHT))  # WIN stands for window
pygame.display.set_caption("Nonogram")


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
  
  for i in range(COLS):
    task_rect = pygame.Rect(
      task_origin[0] + (H_TASK_NUM * cell_size) + (i * cell_size),
      task_origin[1],
      cell_size, V_TASK_NUM * cell_size
    )
    pygame.draw.rect(screen, WHITE, task_rect)
    pygame.draw.rect(screen, PINK, task_rect, 2)

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
      # Draw rectangle for box
      box_rect = pygame.Rect(
        board_origin[0] + j * cell_size + 2,
        board_origin[1] + i * cell_size + 2,
        cell_size - 4, cell_size - 4
      )

      pygame.draw.rect(screen, WHITE, rect)
      pygame.draw.rect(screen, BLUE, rect, 2)  # A thin boarder between cells

      # Display crosses or black boxes if needed
      if (i, j) in crosses: 
        screen.blit(cross, rect)
      elif (i, j) in boxes: 
        pygame.draw.rect(screen, BLACK, box_rect)

  pygame.display.flip()

