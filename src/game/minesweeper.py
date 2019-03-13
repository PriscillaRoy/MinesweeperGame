from enum import Enum
import random

class GameStatus(Enum):
  PROGRESS = 0
  LOST = 1
  WON = 2

class CellStatus(Enum):
  UNEXPOSED = 0
  EXPOSED = 1
  SEAL = 2

class Minesweeper():
  def __init__(self):
    self.game_status = GameStatus.PROGRESS
    self.status = [[CellStatus.UNEXPOSED] * 10 for i in range(10)]
    self.mine = [[False] * 10 for i in range(10)]

  def get_status(self, x, y):
    return self.status[x][y]

  def expose(self, x, y):
    if not self.is_in_range(x,y):
      raise IndexError

    if self.mine[x][y] and self.status[x][y] != CellStatus.SEAL:
      self.game_status = GameStatus.LOST

    elif self.status[x][y] == CellStatus.UNEXPOSED:
      self.status[x][y] = CellStatus.EXPOSED

      if self.adjacent_mine_count(x,y) == 0:
        self.expose_neighbors(x, y)

  def toggle_seal(self, x, y):
    if not self.is_in_range(x,y):
      raise IndexError

    if self.status[x][y] == CellStatus.SEAL:
      self.status[x][y] = CellStatus.UNEXPOSED

    elif self.status[x][y] != CellStatus.EXPOSED:
      self.status[x][y] = CellStatus.SEAL

  def expose_neighbors(self,x, y):
    for i in range(x - 1, x + 2):
      for j in range(y - 1, y + 2):
        if self.is_in_range(i, j) and not (x == i and y == j):
          self.expose(i, j)

  def is_in_range(self, x, y):
    return x >= 0 and x < 10 and y >= 0 and y < 10

  def is_mine_at(self,x, y):
    if not self.is_in_range(x, y):
      return False

    return self.mine[x][y]

  def set_mine(self, x, y):
    self.mine[x][y] = True

  def adjacent_mine_count(self, x, y):
    mine_count = 0
    for i in range(x - 1, x + 2):
      for j in range(y - 1, y + 2):
        if self.is_mine_at(i,j) and not (x == i and y == j):
          mine_count+=1

    return mine_count

  def get_game_status(self):
    if self.is_all_mines_sealed() and self.is_all_cells_exposed():
      self.game_status = GameStatus.WON

    return self.game_status

  def is_all_mines_sealed(self):
    for i in range(10):
      for j in range(10):
        if self.is_mine_at(i, j) and self.status[i][j] != CellStatus.SEAL:
          return False
    return True

  def is_all_cells_exposed(self):
    for i in range(10):
      for j in range(10):
        if not self.is_mine_at(i, j) and self.status[i][j] != CellStatus.EXPOSED:
          return False
    return True

  def set_mines(self, seed):
    random.seed(seed)
    mine_count = 0
    while mine_count < 10:
      x = random.randint(0, 9)
      y = random.randint(0, 9)

      if not self.is_mine_at(x, y):
        self.mine[x][y] = True
        mine_count+=1