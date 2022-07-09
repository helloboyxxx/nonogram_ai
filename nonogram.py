from dataclasses import dataclass
from itertools import count

O = "O"
X = "X"
PROMPT = "#"
EMPTY = None

class Nonogram():
  def __init__(self, height, width, prompt_x, ans, h_task, v_task):
    if ans == None or len(ans) == 0:  # Do we need to check if the ans is valid?
      raise RuntimeError("Answer not given. Please give an answer set")
    
    self.height = height
    self.width = width

    self.prompt_x = prompt_x
    self.x_set = []
    self.o_set = [] # At first, player has found no "O"

    self.board = []

    self.ans = ans  # Records the positions of black blocks, the "O"s
    self.hearts = 3  # Records the rest of player's lives

    self.reset()


  def reverse_symbol(symbol):
    if symbol == O:
      return X
    elif symbol == X:
      return O
    return None

  def count_task(filename):
    """
    Given the filename, this function should count and calculate the "tasks".
    This function returns two lists, vertical task and horizontal task. 
    Each lists stores every single task as a list. So it should look like:
    h_task = [ [2, 1], [3, 1], [1, 3], [3, 1], [2, 1] ]
    v_task = [ [5], [2, 2], [3], [1], [5] ]
    These are the data from tree.txt
    """
    # raise NotImplementedError

    v_task = [ [2, 1], [1, 1, 1], [1, 3], [3, 1], [2, 1] ]
    h_task = [ [5], [1, 2], [3], [1], [5] ]

    return h_task, v_task

  def load_data(filename):
    """
    Reads data from txt that stores the puzzle
    """
    height = None
    width = None
    prompt_x = []
    ans = []
    with open(filename) as f: 
      lines = f.read().splitlines()
      height = len(lines)
      width = len(lines[0])
      for idx,line in enumerate(lines):
        # c is the index of the cell within that line
        for c in range(len(line)):
          if line[c] == PROMPT:
            prompt_x.append((idx, c))
          if line[c] == O:
            ans.append((idx, c))

    # TODO
    h_task, v_task = Nonogram.count_task(filename)
    return height, width, prompt_x, ans, h_task, v_task

  def update_board(self, symbol, cell):
    """
      Cell is given as a pair, representing the location of the given symbol
    """
    if symbol != X and symbol != O: 
      raise RuntimeError("Wrong symbol")
    row = cell[0]
    col = cell[1]
    if self.board[row][col] != EMPTY:
      # raise RuntimeError(f"Position ({row}, {col}) has been occupied")
      print(f"Position ({row}, {col}) has been occupied")
      return

    self.board[row][col] = symbol
    if symbol == O:
      self.o_set.append(cell)
    elif symbol == X:
      self.x_set.append(cell)

  def clear_line(self):
    """
    This is a game feature of the game app on iPhone,
    that one line will be automatically cleared if all tiles are correctly revealed
    So all crosses that are not clicked should be also added to the x_set
    """
    pass

  def check_move(self, symbol, cell):
    """
    Given the moves made by player, return True if this move is correct,
    return False if this move is wrong
    """
    if self.board[cell[0]][cell[1]] != EMPTY:
      # raise RuntimeError(f"Position ({cell[0]}, {cell[1]}) has been occupied")
      print(f"Position ({cell[0]}, {cell[1]}) has been occupied")
      return True
    
    # TODO
    print("TO BE CHECKED")

    return True

  def print_board(self):
    print(f"{self.hearts} hearts left")
    for i in range(self.height):
      for j in range(self.width):
        if self.board[i][j] == EMPTY:
          print("_ ", end="")  # Represent the empty cell
        else: 
          print(self.board[i][j], end=" ")  # Print the symbol on the board
      print()
  
  def reset(self):
    self.x_set = self.prompt_x
    self.o_set = []
    self.board = []
    self.hearts = 3

    # Initialize an empty board
    for i in range(self.height):
      row = []
      for j in range(self.width):
        row.append(EMPTY)
      self.board.append(row)

    # Update the board according to "prompt_x", 
    for i in range(self.height):
      for j in range(self.width):
        if (i, j) in self.prompt_x:
          self.board[i][j] = X

  def won(self):
    """
    Checks if all cells are filled, and all are correct
    """
    # Check if o_set(player's decision) equals ans(answer)
    if self.o_set != self.ans: 
      return False

    # Compare o_set with ans
    for cell in self.o_set:
      if cell not in self.ans:
        return False

    return True


