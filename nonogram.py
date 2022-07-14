import time

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
    with open(filename) as f:
      # read board info
      lines = f.read().splitlines()
      height = len(lines)
      width = len(lines[0])
      # initialize h and v task lists
      h_task = []
      v_task = []
      # add info in h task lists 
      for a in range(height):
        h_task.append([])
        num = 0
        for b in range(width):
          if lines[a][b] == O:
            num = num + 1
            if b == width - 1:
              h_task[a].append(num)
          elif num != 0:
            h_task[a].append(num)
            num = 0
      # add info in v task lists
      for j in range(width):
        v_task.append([])
        num = 0
        for i in range(height):
          if lines[i][j] == O:
            num = num + 1
            if i == height - 1:
              v_task[j].append(num)
          elif num != 0:
            v_task[j].append(num)
            num = 0
    """
    example of v_task and h_task to test pygame_runner:
    v_task = [ [2, 1], [1, 2], [1, 3], [3, 1], [2, 1] ]
    h_task = [ [5], [1, 2], [3], [1], [5] ]
    """
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
    return True

  def print_board(self):
    # print(f"{self.hearts} hearts left")
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
    self.known_cells = set()  # cells for making move, a set of pairs ((row, col), symbol)

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
  
  def print_board(self):
    print("BOARD: ")
    for row in self.board:
      print(row)


  def make_move(self):
    """
    Returns a move if still available. Otherwise returns None.
    """
    move = None
    # No known cell left. Look for another line
    if len(self.known_cells) == 0:
      # Keep trying to solve lines for some new cells
      while len(self.known_cells) == 0:
        time.sleep(0.1)
        line, pattern, task = self.get_next_line()
        # No more moves to make, the game should end
        if line == None and pattern == None and task == None:
          return None
        
        new_pattern = self.solve_line(pattern, task)
        # print(f"NEW PATTERN: \n{new_pattern}")
        # print(f"OLD PATTERN: \n{pattern}")
        self.update_line(line, pattern, new_pattern)
    move = self.known_cells.pop()
    return move


  def update_line(self, line, pattern, new_pattern):
    # print(f"NEW PATTERN: \n{new_pattern}")
    # print(f"OLD PATTERN: \n{pattern}")
    for symbol_idx in range(len(new_pattern)):
      if new_pattern[symbol_idx] != pattern[symbol_idx]:
        
        row_num = line[symbol_idx][0]
        col_num = line[symbol_idx][1]

        # Add this symbol to known_cells since this is a new cell determined
        # self.known_cells.add((row_num, col_num))
        self.known_cells.add(((row_num, col_num), new_pattern[symbol_idx]))

        # Update the board, x_set, and o_set
        if new_pattern[symbol_idx] == O:
          self.board[row_num][col_num] = O
          self.o_set.add((row_num, col_num))

        elif new_pattern[symbol_idx] == X:
          self.board[row_num][col_num] = X
          self.x_set.add((row_num, col_num))
      
    
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

    # Get a row
    if self.next_idx < self.height:
      row_idx = self.next_idx
      task = self.h_task[row_idx]
      pattern = self.board[row_idx]
      for col_idx in range(self.width):
        line.append((row_idx, col_idx))
    # Get a col
    else: 
      col_idx = self.next_idx - self.height
      task = self.v_task[col_idx]
      for row_idx in range(self.height):
        line.append((row_idx, col_idx))
        pattern.append(self.board[row_idx][col_idx])

    # update self.next_idx
    old_idx = self.next_idx
    while True:
      self.next_idx += 1
      if self.next_idx == self.height + self.width:
        self.next_idx = 0
      # Skip already-checked lines
      if self.next_idx not in self.cleared_line:  
        break

      # change to -1 to mark that no more lines needed to be checked
      if self.next_idx == old_idx:
        self.next_idx = -1
        break
      
    assert(task != None)
    assert(0 <= self.next_idx < (self.height + self.width))

    return line, pattern, task


  def fill_whole_line(p_len, task): 
    """
    Returns a pattern completely filled. 
    Consider p_len = 10, task = [4, 5]
    Consider p_len = 10, task = [2, 4, 2]
    """
    pattern = []
    for num_idx in range(len(task)): 
      for i in range(task[num_idx]):
        pattern.append(O)
      if num_idx != len(task) - 1:  # not the last element
        pattern.append(X)
    return pattern


  def fill_mid(pattern, diff):
    new_pattern = pattern.copy()
    edge_num = (len(pattern) - diff) / 2
    for i in range(len(pattern)):
      if edge_num <= i < len(pattern) - edge_num:
        new_pattern[i] = O
    return new_pattern


  def clear_line(self, pattern, task):
    pass


  def solve_line(self, pattern, task):
    """
    Given a pattern (a line of symbols), this function should return 
    an updated new pattern (or not changed if cannot add new symbol).
    Since we have the info of revealed cells on the board, together with
    info from given tasks, we should be able to do this job. 
    If this line is cleared, add index to self.cleared_line
    """
    # pattern: [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY]
    # print(f"OLD PATTERN: \n{pattern}")

    p_len = len(pattern)
    assert(sum(task) + len(task) - 1 <= p_len)

    # If the task adds up to the whole line
    # task = [1, 3]
    # task = [5]  should be able to include this task as well
    if sum(task) + len(task) - 1 == p_len:
      pattern = NonogramAI.fill_whole_line(p_len, task)

    # Single task but greater than half of p_len
    elif len(task) == 1: 
      diff = 2 * task[0] - p_len
      if diff > 0:
        pattern = NonogramAI.fill_mid(pattern, diff)


    # Use clear_line to make sure this line will be no empty place if all tiles are found
    self.clear_line(pattern, task)
    return pattern