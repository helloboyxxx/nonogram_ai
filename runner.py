import sys
from nonogram import Nonogram

      
def main():
  if len(sys.argv) != 2:
      sys.exit("Usage: python runner.py tree.txt")
  
  height, width, prompt_x, ans = Nonogram.load_data(sys.argv[1])

  game = Nonogram(height, width, prompt_x, ans)
  while not game.won():
    game.print_board()

    # usage: [symbol] [row_num] [col_num]
    move = input(("ur move: ")).split()

    symbol = move[0]
    row_num = int(move[1])
    col_num = int(move[2])

    game.check_move((row_num, col_num, symbol))
    
    game.update_board((row_num, col_num), symbol)



if __name__ == "__main__":
  main()