import sys

import time

from nonogram import Nonogram, NonogramAI
if len(sys.argv) != 2:
    sys.exit("Usage: python runner.py tree.txt")



# Get enough data to create the game board
height, width, prompt_x, ans, h_task, v_task = Nonogram.load_data(sys.argv[1])

start_time = time.time()

# Create game and AI agent
game = Nonogram(height, width, prompt_x, ans)
ai = NonogramAI(height, width, h_task, v_task, prompt_x)

# Stop when win the game
while True:
  if game.won():
    print("win")
    break
  move_info = ai.make_move()
  move = move_info[0]
  symbol = move_info[1]

  # When this move is correct, update the board directly
  # Otherwise, display correct symbol and kill one heart
  if game.check_move(symbol, move):
    game.update_board(symbol, move)
  else: 
    game.update_board(Nonogram.reverse_symbol(symbol), move)
    game.hearts -= 1
  
  # # Restart this puzzle when lose
  # if game.hearts == 0:
  #   game.reset()

end_time = time.time()

print(f'程序运行时间: { (end_time - start_time)*1000 } 毫秒')