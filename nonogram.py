O = "O"
X = "X"
PROMPT = "#"
EMPTY = None

class Nonogram():
  def __init__(self, height, width, prompt_x, ans=None):
    if ans == None:
      raise RuntimeError("Answer not given. Please give an answer set")
    
    self.height = height
    self.width = width
    self.x_set = prompt_x
    self.ans = ans  # Records the positions of black blocks, the "O"s

    # Initialize an empty board
    self.board = []
    for i in range(self.height):
      row = []
      for j in range(self.width):
        row.append(EMPTY)
      self.board.append(row)

    # Update the board according to "known_x"
    # print("X_SET: ")
    # print(self.x_set)
    for i in range(self.height):
      for j in range(self.width):
        if (i, j) in self.x_set:
          self.board[i][j] = X
    # At first, player has found no "O"
    self.o_set = set()

  def count_task(filename):
    pass

  def load_data(filename):
    """
    Reads data from txt that stores the puzzle
    """
    prompt_x = []
    ans = []
    height = None
    width = None
    with open(filename, "r") as f: 
      lines = f.readlines()
      height = len(lines)
      width = len(lines[0])
      for idx,line in enumerate(lines):
        # c is the index of the cell within that line
        for c in range(len(line)):
          if line[c] == PROMPT:
            prompt_x.append((idx, c))
          if line[c] == O:
            ans.append((idx, c))   
    return height, width, prompt_x, ans

  def update_board(self, cell, symbol):
    """
      Cell is given as a pair, representing the location of the given symbol
    """
    if symbol != X and symbol != O: 
      raise RuntimeError("Wrong symbol")
    row = cell[0]
    col = cell[1]
    if self.board[row][col] != EMPTY:
      raise RuntimeError(f"Position ({row}, {col}) has been occupied")

    self.board[row][col] = symbol


  def check_move(self, cell, symbol):
    if self.board[cell] != EMPTY:
      raise RuntimeError(f"Position ({cell[0]}, {cell[1]}) has been occupied")
    print("TO BE CHECKED")



  def print_board(self):
    for i in range(self.height):
      for j in range(self.width):
        if self.board[i][j] == EMPTY:
          print("_ ", end="")
        else: 
          print(self.board[i][j], end=" ")
      print()
  


    

  def won(self):
    """
    Checks if all cells are filled, and all are correct
    """
    # Check if o_set(player's decision) equals ans(answer)
    if self.o_set != self.ans: 
      return False
    # Check if num of X and O adds up to total cells num
    if len(self.x_set) + len(self.o_set) != self.height * self.width:
      return False

    return True


