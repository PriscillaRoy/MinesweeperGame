import tkinter
from tkinter import messagebox
from src.game.minesweeper import Minesweeper
from src.game.minesweeper import CellStatus
from src.game.minesweeper import GameStatus
from datetime import datetime
import platform

class MineweeperUI:
  def __init__(self, root):
    self.ui_window = root
    self.ui_window.title("Minesweeper")

    self.minesweeper = Minesweeper()
    self.minesweeper.set_mines((int(round(datetime.now().timestamp() * 1000))))

    self.cells= []
    self.grid_init()

  def grid_init(self):
    right_click_type = self.button_os_config()
    for row in range(0, 10):
      self.cells.append([])
      for column in range(0, 10):
        cell = tkinter.Button(self.ui_window, text=" ", width=5, height=3,
                              command=lambda row=row, column=column, left_button = True: self.button_clicked(row, column, left_button))
        cell.bind(right_click_type, lambda event, row=row, column=column, left_button = False: self.button_clicked(row, column, left_button))
        cell.grid(row=row + 1, column=column)
        self.cells[row].append(cell)

  def button_os_config(self):
    if platform.system() == "Darwin":
      return "<Button-2>"
    else:
      return "<Button-3>"

  def button_clicked(self,row, column, left_button):
    if left_button:
      self.minesweeper.expose(row, column)
    else:
      self.minesweeper.toggle_seal(row, column)

    self.update_grid()

    if self.minesweeper.get_game_status() == GameStatus.LOST:
      self.show_mines()
      messagebox.showinfo("Game Over", "You have step on a mine! ")
      if platform.system() == "Windows":
        exit()

    elif self.minesweeper.get_game_status() == GameStatus.WON:
      messagebox.showinfo("Congratulations!", "You are a minesweeper master! ")
      if platform.system() == "Windows":
        exit()


  def show_mines(self):

    for row in range(10):
      for column in range(10):
        if self.minesweeper.is_mine_at(row,column):
          self.cells[row][column]["text"] = "*"
          if platform.system() == "Darwin":
            self.cells[row][column].config(highlightbackground="red", highlightthickness=1)
          else:
            self.cells[row][column].config(background='red')

  def update_grid(self):

    for row in range(10):
      for column in range(10):

        if platform.system() == "Darwin":
          if self.minesweeper.get_status(row,column) == CellStatus.EXPOSED:
            adjacent_value = self.minesweeper.adjacent_mine_count(row, column)
            if adjacent_value > 0: self.cells[row][column]["text"] = str(adjacent_value)
            self.cells[row][column].config(highlightbackground="Yellow", highlightthickness=1)
          elif self.minesweeper.get_status(row, column) == CellStatus.SEAL:
            self.cells[row][column].config(highlightbackground="green", highlightthickness=1)
          else:
            self.cells[row][column].config(highlightbackground="#DCDCDC", highlightthickness=1)

        else:
          if self.minesweeper.get_status(row, column) == CellStatus.EXPOSED:
            adjacent_value = self.minesweeper.adjacent_mine_count(row, column)
            if adjacent_value > 0: self.cells[row][column]["text"] = str(adjacent_value)
            self.cells[row][column].config(background='Yellow')

          elif self.minesweeper.get_status(row, column) == CellStatus.SEAL:
            self.cells[row][column].config(background='green')
          else:
            self.cells[row][column].config(background='#DCDCDC')

    

class Main:
  def __init__(self):
    root = tkinter.Tk()
    MineweeperUI(root)
    root.mainloop()
