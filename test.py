from nonogram import *
import sys

if len(sys.argv) != 2:
    sys.exit("Usage: python runner.py tree.txt")

# Get enough data to create the game board
height, width, prompt_x, ans, h_task, v_task = Nonogram.load_data(sys.argv[1])

# Create game and AI agent
game = Nonogram(height, width, prompt_x, ans)
ai = NonogramAI(height, width, h_task, v_task, prompt_x)

pattern_1 = [None] * 10
task_1 = [4, 5]

pattern_2 = [None] * 10
task_2 = [10]

pattern_3 = [None] * 10
task_3 = [2, 3, 3]

NonogramAI.fill_whole_line(pattern_1, task_1)
print(pattern_1)

NonogramAI.fill_whole_line(pattern_2, task_2)
print(pattern_2)

NonogramAI.fill_whole_line(pattern_2, task_2)
print(pattern_2)