import sys

from pyparsing import col
# import pygame
# import time

from nonogram import Nonogram, NonogramAI

      

if len(sys.argv) != 2:
    sys.exit("Usage: python runner.py tree.txt")

# Get enough data to create the game board
height, width, prompt_x, ans, h_task, v_task = Nonogram.load_data(sys.argv[1])

# Create game and AI agent
game = Nonogram(height, width, prompt_x, ans)
ai = NonogramAI(height, width, h_task, v_task, prompt_x)

# Stop when win the game
while True:
  game.print_board()

  # usage: [symbol] [row_num] [col_num]
  move_input = input(("ur move: ")).split()

  move = None
  symbol = None
  if move_input[0] == "ai":
    move_info = ai.make_move()
    move = move_info[0]
    symbol = move_info[1]

  else:
    symbol = move_input[0]
    row_num = int(move_input[1])
    col_num = int(move_input[2])
    move = (row_num, col_num)

  # When this move is correct, update the board directly
  # Otherwise, display correct symbol and kill one heart
  if game.check_move(symbol, move):
    game.update_board(symbol, move)
  else: 
    game.update_board(Nonogram.reverse_symbol(symbol), move)
    game.hearts -= 1
  
  # Restart this puzzle when lose
  if game.hearts == 0:
    game.reset()

  # Quit loop when this puzzle is solved
  if game.won():
    print("You have solved this puzzle, you won!!!")
    break

