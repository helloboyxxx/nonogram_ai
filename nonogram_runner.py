from nonogram import *
import sys

# Get data from the puzzle file
if len(sys.argv) != 2:
  sys.exit("Usage: python runner.py tree.txt")

# Get enough data to create the game board
height, width, prompt_x, ans, h_task, v_task = Nonogram.load_data(sys.argv[1])

game = Nonogram(height, width, prompt_x, ans)
ai = NonogramAI(height, width, h_task, v_task, prompt_x)

pattern = ai.solve_line(pattern=[EMPTY] * 10, task=[3, 4])
print(pattern)

