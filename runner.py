import sys
# import pygame
# import time

from nonogram import Nonogram

      

if len(sys.argv) != 2:
    sys.exit("Usage: python runner.py tree.txt")

# Get enough data to create the game board
height, width, prompt_x, ans, h_task, v_task = Nonogram.load_data(sys.argv[1])

# Initialize this game board
game = Nonogram(height, width, prompt_x, ans, h_task, v_task)



# Stop when win the game
while True:
  game.print_board()

  # usage: [symbol] [row_num] [col_num]
  move = input(("ur move: ")).split()

  symbol = move[0]
  row_num = int(move[1])
  col_num = int(move[2])

  # When this move is correct, update the board directly
  # Otherwise, display correct symbol and kill one heart
  if game.check_move(symbol, (row_num, col_num)):
    game.update_board(symbol, (row_num, col_num))
  else: 
    game.update_board(Nonogram.reverse_symbol(symbol), (row_num, col_num))
    game.hearts -= 1
  
  # Restart this puzzle when lose
  if game.hearts == 0:
    game.reset()

  # Quit loop when this puzzle is solved
  if game.won():
    print("You have solved this puzzle, you won!!!")
    break

