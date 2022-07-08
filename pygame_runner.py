import pygame 
import sys
import time

from nonogram import Nonogram


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


# Constants
WIDTH, HEIGHT = 500, 500
ROWS, COLS = height, width

PINK = (255, 224, 230)
BLACK = (10, 10, 10)
WHITE = (255, 255, 255)
GRAY = (180, 180, 180)

screen = pygame.display.set_mode((WIDTH, HEIGHT))  # WIN stands for window
pygame.display.set_caption("Nonogram")


# Compute board size
BOARD_PADDING = 20
board_width = WIDTH - (BOARD_PADDING * 2)
board_height = HEIGHT - (BOARD_PADDING * 2)
cell_size = int(min(board_width / COLS, board_height / ROWS))
board_origin = (BOARD_PADDING, BOARD_PADDING)


# Add images
cross = pygame.image.load("assets/images/cross.png")
cross = pygame.transform.scale(cross, (cell_size, cell_size))
# box = pygame.image.load("assets/images/mine.png")
# box = pygame.transform.scale(box, (cell_size, cell_size))


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

  # Draw board
  cells = []
  for i in range(ROWS):
    row = []
    for j in range(COLS):
      # Draw rectangle for cell
      rect = pygame.Rect(
        board_origin[0] + (j * cell_size) - 2,
        board_origin[1] + (i * cell_size) - 2,
        cell_size, cell_size
      )
      # Draw rectangle for box
      box_rect = pygame.Rect(
        board_origin[0] + j * cell_size,
        board_origin[1] + i * cell_size,
        cell_size - 4, cell_size - 4
      )

      pygame.draw.rect(screen, WHITE, rect)
      pygame.draw.rect(screen, GRAY, rect, 1)  # A thin boarder between cells

      # Display crosses or black boxes if needed
      if (i, j) in crosses: 
        screen.blit(cross, rect)
      elif (i, j) in boxes: 
        pygame.draw.rect(screen, BLACK, box_rect)


  
  pygame.display.flip()

