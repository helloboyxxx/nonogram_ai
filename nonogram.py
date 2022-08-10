from curses.panel import new_panel
import time

from numpy import take

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
    # self.x_set = prompt_x   # should be empty set if there are no prompts at all
    # self.o_set = set()
    self.known_cells = set()  # cells for making move, a set of pairs ((row, col), symbol)

    # Store data in board
    self.board = []
    for row in range(height):
      line = []
      for col in range(width):
        # if (row, col) in self.x_set:
        if (row, col) in prompt_x:
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
    
    # Keep trying to solve lines for some new cells. If there are known cells left, then this loop is skipped
    while len(self.known_cells) == 0:
      line, pattern, task = self.get_next_line()
      # No more moves to make, the game should end
      if line == None and pattern == None and task == None:
        return None
      
      # new_pattern = pattern.copy()
      new_pattern = self.solve_line(pattern, task)  # solve_line will change the original pattern
      self.update_line(line, pattern, new_pattern)

      break
  
    move = self.known_cells.pop()
    return move


  def update_line(self, line, pattern, new_pattern):
    """
    Update the board if there are any changes.
    Also add cells to self.known_cells if we found new cells. 
    Here we compare the two patterns to look for changes
    """
    print(f"NEW PATTERN: \n{new_pattern}")
    print(f"OLD PATTERN: \n{pattern}")
    for symbol_idx in range(len(new_pattern)):
      if new_pattern[symbol_idx] != pattern[symbol_idx]:
        
        row_num = line[symbol_idx][0]
        col_num = line[symbol_idx][1]

        # Add this symbol to known_cells since this is a new cell determined
        self.known_cells.add(((row_num, col_num), new_pattern[symbol_idx]))

        # Update the board, x_set, and o_set
        if new_pattern[symbol_idx] == O:
          self.board[row_num][col_num] = O
          # self.o_set.add((row_num, col_num))

        elif new_pattern[symbol_idx] == X:
          self.board[row_num][col_num] = X
          # self.x_set.add((row_num, col_num))
      
    
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
      if self.next_idx == self.height + self.width:  # Set to zero if reach the sum of height and width
        self.next_idx = 0
      # break if the next line is not cleared
      if self.next_idx not in self.cleared_line:  
        break

      # change to -1 to mark that no more lines are required to be checked
      if self.next_idx == old_idx:
        self.next_idx = -1
        break
      
    assert(task != None)
    assert(0 <= self.next_idx < (self.height + self.width))

    return line, pattern, task


  def solve_line(self, pattern, task):
    """
    Given a pattern, solve_line will return a new pattern if new cells can be marked
    """

    if NonogramAI.is_empty_line(pattern):
      pattern = NonogramAI.fill_empty_line(pattern, task)
    else:
      # I need to classify examples to design this part 
      pass
    
    return pattern


  def is_empty_line(pattern):
    for symbol in pattern:
      if symbol != EMPTY:
        return False
    return True


  def fill_empty_line(pattern, task):
    """
    Since this pattern is empty, we can run some simple functions
    to check if some cells can be determined
    """
    left_pattern, right_pattern = NonogramAI.dumb_fill(pattern, task)
    # print(f"LEFT PATTER: {left_pattern}")
    # print(f"RIGHT PATTER: {right_pattern}")
    pattern = NonogramAI.fill_overlapped(left_pattern, right_pattern)
    return pattern



  def dumb_fill(pattern, task):
    """
    This function will return two patterns.
    left_pattern is filled directly from the left side
    Reference: https://www.bilibili.com/video/BV1qT4y1C7qc?share_source=copy_web&vd_source=0eea0082c768cd021146964be3ae83a8
    """
    fixed_pattern = []
    for task_idx in range(len(task)):
      for _ in range(task[task_idx]):
        fixed_pattern.append(O)
      if task_idx != len(task) - 1:
        fixed_pattern.append(X)

    empty_space = []
    empty_count = len(pattern) - (sum(task) + len(task) - 1)
    for _ in range(empty_count):
      empty_space.append(EMPTY)

    left_pattern = fixed_pattern + empty_space
    right_pattern = empty_space + fixed_pattern    

    return left_pattern, right_pattern


  def fill_overlapped(p1, p2):
    """
    Given two patterns, return a new pattern that only picks the overlapping cells
    """
    pattern = []
    for i in range(len(p1)):
      if p2[i] != EMPTY and p1[i] == p2[i]:
        pattern.append(p1[i])
      else:
        pattern.append(EMPTY)
    return pattern



# I want to try to rewrite the "solve_line" function
'''
  def is_whole(pattern, task):
    """
    helper function of fill_whole_line()
    return True and everything needed if this pattern 
    return 
    """
    pass

  def fill_whole_line(pattern, task): 
    """
    Directly modify pattern to fill in all cells
    Consider len(new_pattern) = 10, task = [4, 5]
    Consider len(new_pattern) = 10, task = [2, 4, 2]
    If we have pattern = [X, EMPTY, EMPTY, EMPTY, X], task = [1, 1], 
    then we should also fill it 
    """
    p_len = len(pattern)
    start_idx = 0   # Where the "middle part" starts
    end_idx = p_len # Where the "middle part" ends
    if len(task) == 1:
      x_count = 0
      # Count number of positions in the middle to be filled:
      for i in range(p_len):
        if pattern[i] == X:
          x_count += 1
        else: 
          break

      start_idx = x_count

      for i in range(p_len - 1, -1, -1):
        if pattern[i] == X:
          x_count += 1
        else: 
          break

      end_idx = p_len - (x_count - start_idx)
      
      print(f"x_count: {x_count}")
      print(f"sum(task) + len(task) - 1: {sum(task) + len(task) - 1}")

      # Check if the "middle" part can be fully filled
      if sum(task) + len(task) - 1 == p_len-x_count: 
        cur_idx = start_idx  # Keep track of which cell to change
        for num in task:
          for i in range(num):  # Fill in consecutive Os
            pattern[cur_idx] = O
            cur_idx += 1
          if cur_idx != end_idx:  # Add an X in between parts
            pattern[cur_idx] = X
            cur_idx += 1
          


  def fill_mid(pattern, diff):
    edge_num = (len(pattern) - diff) / 2
    for i in range(len(pattern)):
      if edge_num <= i < len(pattern) - edge_num:
        pattern[i] = O
    return pattern


  def clear_line(self, pattern, task):
    # Check if count of O is equal to sum of the num in task
    if pattern.count(O) == sum(task):
      # fill the rest of hte pattern with X
      for i in range(len(pattern)):
        if pattern[i] == EMPTY:
          pattern[i] = X
        


  def solve_line(self, pattern, task):
    """
    Given a pattern (a line of symbols), this function should return 
    an updated new pattern (or not changed if cannot add new symbol).
    Since we have the info of revealed cells on the board, together with
    info from given tasks, we should be able to do this job. 
    If this line is cleared, add index to self.cleared_line
    """
    # print(f"PATTERN: \n{pattern}")
    new_pattern = pattern.copy()

    assert(sum(task) + len(task) - 1 <= len(new_pattern))

    # If the task adds up to the whole line
    # task = [1, 3]
    # task = [5]  should be able to include this task as well
    new_pattern = NonogramAI.fill_whole_line(new_pattern, task)

    # Single task but greater than half of p_len
    if len(task) == 1: 
      diff = 2 * task[0] - len(new_pattern)
      if diff > 0:
        new_pattern = NonogramAI.fill_mid(new_pattern, diff)


    # Use clear_line to make sure this line will be no empty place if all tiles are found
    # self.clear_line(new_pattern, task)
    return new_pattern

  '''