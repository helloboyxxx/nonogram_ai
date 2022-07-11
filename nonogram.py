O = "O"
X = "X"
PROMPT = "#"
EMPTY = None

class Nonogram():
  def __init__(self, height, width, prompt_x, ans):
    if ans == None or len(ans) == 0:  # Do we need to check if the ans is valid?
      raise RuntimeError("Answer not given. Please give an answer set")
    
    self.height = height
    self.width = width

    self.prompt_x = prompt_x
    self.x_set = set()
    self.o_set = set() # At first, player has found no "O"

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
    prompt_x = set()
    ans = set()
    with open(filename) as f: 
      lines = f.read().splitlines()
      height = len(lines)
      width = len(lines[0])
      for idx,line in enumerate(lines):
        # c is the index of the cell within that line
        for c in range(len(line)):
          if line[c] == PROMPT:
            prompt_x.add((idx, c))
          if line[c] == O:
            ans.add((idx, c))

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
      self.o_set.add(cell)
    elif symbol == X:
      self.x_set.add(cell)

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
    self.o_set = set()
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

class NonogramAI():
  def __init__(self, height, width, h_task, v_task, prompt_x):
    # Info of the board
    self.height = height
    self.width = width
    self.h_task = h_task
    self.v_task = v_task

    # Keep tracking status on the board 
    self.x_set = prompt_x
    self.o_set = set()
    self.known_cells = set()  # cells for making move

    # Store data in board
    self.board = []
    for row in range(height):
      line = []
      for col in range(width):
        if (row, col) in self.x_set:
          line.append(X)
        else:
          line.append(EMPTY)
      self.board.append(line)
    
    # Used to keep track of which line to be check next in get_next_line()
    # Maximum = height + width. Equals -1 if no more to check
    self.next_idx = 0
    self.cleared_line = set()  # records the lines indexes that are all cleared
  
  def get_next_line(self):
    """
    This function returns an array of cell positions so that it is easier 
    to fill in known cells.
    Returns a pattern containing a line of symbols (X O and EMPTY) so that it is easier 
    when solving one line.
    Returns a task as well
    Return None, None, None if the game has ends
    """
    # No more to check
    if self.next_idx == -1:
      return None, None, None

    # Use the self.next_idx to get a line
    line = []
    pattern = []
    task = None
    if self.next_idx < self.height:  # Get a row
      row_idx = self.next_idx
      task = self.h_task[row_idx]
      for col_idx in range(self.width):
        line.append((row_idx, col_idx))

    # else, we retrive line from col
    col_idx = self.next_idx - self.height
    task = self.v_task[col_idx]
    for row_idx in range(self.height):
      line.append((row_idx, col_idx))

    # update self.next_idx
    old_idx = self.next_idx
    while True:
      self.next_idx += 1
      if self.next_idx == self.height + self.width:
        self.next_idx = 0
      # Skip already-checked lines
      if self.next_idx in self.cleared_line:  
        continue

      # change to -1 to mark that no more lines needed to be checked
      if self.next_idx == old_idx:
        self.next_idx = -1
        break
      
    assert(task != None)
    assert(0 < self.next_idx < (self.height + self.width))

    return line, pattern, task


  def solve_line(self, line, task):
    """
    Given an array of positions (a line of cells to be checked), this function should 
    be able to figure out cells' position to be added to known_cells.
    Since we have the info of revealed cells, together with
    info from given tasks, we should be able to do this job. 

    Returns a new pattern, a new line a symbols, if able to update any new cells.
    If this line is cleared, add index to self.cleared_line
    """
    pass


  def make_move(self):
    """
    Returns a move if still available. Otherwise returns None.
    """
    move = None
    # No known cell left. Look for another line
    if len(self.known_cells) == 0:
      line, pattern, task = self.get_next_line()
      self.solve_line(pattern, task)
    
    move = self.known_cells.pop()
    return move
