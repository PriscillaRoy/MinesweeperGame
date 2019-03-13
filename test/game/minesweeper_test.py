import unittest
from src.game.minesweeper import Minesweeper
from src.game.minesweeper import CellStatus
from src.game.minesweeper import GameStatus

class TestMinesweeper(unittest.TestCase):

  def setUp(self):
    self.minesweeper = Minesweeper()

  def test_canary(self):
    self.assertTrue(True)

  def test_expose_an_unexposed_cell(self):
    self.minesweeper.expose(3, 2)

    self.assertEqual(CellStatus.EXPOSED, self.minesweeper.get_status(3, 2))

  def test_expose_an_exposed_cell(self):
     self.minesweeper.expose(3, 2)
     self.minesweeper.expose(3, 2)

     self.assertEqual(CellStatus.EXPOSED, self.minesweeper.get_status(3, 2))

  def test_expose_cell_above_column_max(self):
    with self.assertRaises(IndexError):
      self.minesweeper.expose(0, 11)

  def test_expose_cell_below_column_max(self):
    with self.assertRaises(IndexError):
      self.minesweeper.expose(0, -1)

  def test_expose_cell_above_row_max(self):
    with self.assertRaises(IndexError):
      self.minesweeper.expose(11, 0)

  def test_expose_cell_below_row_max(self):
    with self.assertRaises(IndexError):
      self.minesweeper.expose(-1, 0)

  def test_seal_an_unexposed_cell(self):
    self.minesweeper.toggle_seal(3, 2)

    self.assertEqual(CellStatus.SEAL, self.minesweeper.get_status(3, 2))

  def test_expose_a_sealed_cell(self):
    self.minesweeper.toggle_seal(3, 2)
    self.minesweeper.expose(3,2)

    self.assertEqual(CellStatus.SEAL, self.minesweeper.get_status(3, 2))

  def test_seal_cell_above_column_max(self):
    with self.assertRaises(IndexError):
      self.minesweeper.toggle_seal(0, 11)

  def test_seal_cell_below_column_max(self):
    with self.assertRaises(IndexError):
      self.minesweeper.toggle_seal(0, -1)

  def test_seal_cell_above_row_max(self):
    with self.assertRaises(IndexError):
      self.minesweeper.toggle_seal(11, 0)

  def test_seal_cell_below_row_max(self):
    with self.assertRaises(IndexError):
      self.minesweeper.toggle_seal(-1, 0)

  def test_unseal_a_sealed_cell(self):
    self.minesweeper.toggle_seal(3, 2)
    self.minesweeper.toggle_seal(3, 2)

    self.assertEqual(CellStatus.UNEXPOSED, self.minesweeper.get_status(3, 2))

  def test_seal_an_exposed_cell(self):
    self.minesweeper.expose(3, 2)
    self.minesweeper.toggle_seal(3, 2)

    self.assertEqual(CellStatus.EXPOSED, self.minesweeper.get_status(3, 2))

  def test_expose_calls_expose_neighbors(self):
    class MinesweeperStub(Minesweeper):
      def expose_neighbors(self, row, column):
        self.expose_neighbors_called = True

    minesweeper = MinesweeperStub()
    minesweeper.expose(3, 4)

    self.assertTrue(minesweeper.expose_neighbors_called)

  def test_expose_called_on_an_already_exposed_cell_does_not_call_expose_neighbors(self):
    class MinesweeperStub(Minesweeper):
      def expose_neighbors(self, row, column):
        self.expose_neighbors_called = True

    minesweeper = MinesweeperStub()
    minesweeper.expose(3, 4)
    minesweeper.expose_neighbors_called = False
    minesweeper.expose(3, 4)

    self.assertFalse(minesweeper.expose_neighbors_called)

  def test_expose_called_on_a_sealed_cell_does_not_call_expose_neighbors(self):
    class MinesweeperStub(Minesweeper):
      expose_neighbors_called = False

      def expose_neighbors(self, row, column):
        self.expose_neighbors_called = True

    minesweeper = MinesweeperStub()
    minesweeper.toggle_seal(3,4)
    minesweeper.expose(3, 4)

    self.assertFalse(minesweeper.expose_neighbors_called)

  def test_expose_neighbors_calls_expose_on_eight_neighbors(self):
    class MinesweeperStub(Minesweeper):
      expose_called = 0

      def expose(self, row, column):
        self.expose_called += 1

    minesweeper = MinesweeperStub()
    minesweeper.expose_neighbors(3,2)

    self.assertEqual(8, minesweeper.expose_called)

  def test_expose_neighbors_on_top_left_corner_cell_calls_expose_only_on_existing_cells(self):
    class MinesweeperStub(Minesweeper):
      expose_called = 0

      def expose(self, row, column):
        self.expose_called += 1

    minesweeper = MinesweeperStub()
    minesweeper.expose_neighbors(0,0)

    self.assertEqual(3, minesweeper.expose_called)

  def test_expose_neighbors_on_bottom_right_corner_cell_calls_expose_only_on_existing_cells(self):
    class MinesweeperStub(Minesweeper):
      expose_called = 0

      def expose(self, row, column):
        self.expose_called += 1

    minesweeper = MinesweeperStub()
    minesweeper.expose_neighbors(9,9)

    self.assertEqual(3, minesweeper.expose_called)

  def test_mine_is_not_at_positive_row_positive_col(self):
    self.assertFalse(self.minesweeper.is_mine_at(3,2))

  def test_is_mine_at_positive_row_and_positive_col(self):
    self.minesweeper.set_mine(3,2)
    self.assertTrue(self.minesweeper.is_mine_at(3, 2))

  def test_is_mine_at_negative_row_and_positive_col(self):
    self.assertFalse(self.minesweeper.is_mine_at(-1, 4))

  def test_is_mine_at_over_max_row_and_positive_col(self):
    self.assertFalse(self.minesweeper.is_mine_at(10, 5))

  def test_is_mine_at_positive_row_and_negative_col(self):
    self.assertFalse(self.minesweeper.is_mine_at(5, -1))

  def test_is_mine_at_positive_row_and_over_max_col(self):
    self.assertFalse(self.minesweeper.is_mine_at(7, 10))

  def test_expose_adjacent_cell_not_call_expose_neighbors(self):
    class MinesweeperStub(Minesweeper):
      expose_neighbor_called = True

      def expose_neighbors(self, row, column):
        self.expose_neighbor_called = False

    minesweeper = MinesweeperStub()
    minesweeper.set_mine(0, 1)
    minesweeper.expose(0, 0)

    self.assertTrue(minesweeper.expose_neighbor_called)

  def test_adjacent_mine_count_at_with_no_mines(self):
    self.assertEqual(0, self.minesweeper.adjacent_mine_count(3,2))

  def test_adjacent_mine_count_when_cell_is_mine(self):
    self.minesweeper.set_mine(3,4)
    self.assertEqual(0, self.minesweeper.adjacent_mine_count(3, 4))

  def test_adjacent_mine_count_when_one_mine(self):
    self.minesweeper.set_mine(3, 4)
    self.assertEqual(1,self.minesweeper.adjacent_mine_count(3, 5))

  def test_adjacent_mine_count_when_two_mines(self):
    self.minesweeper.set_mine(3, 4)
    self.minesweeper.set_mine(2, 6)

    self.assertEqual(2,self.minesweeper.adjacent_mine_count(3, 5))

  def test_adjacent_mine_count_when_mine_in_corner_up_left(self):
    self.minesweeper.set_mine(0, 1)
    self.assertEqual(1, self.minesweeper.adjacent_mine_count(0, 0))

  def test_adjacent_mine_count_when_mine_in_corner_down_right(self):
    self.minesweeper.set_mine(9, 8)
    self.assertEqual(1, self.minesweeper.adjacent_mine_count(9, 9))

  def test_adjacent_mine_count_when_no_mines_in_corner_up_right(self):
    self.assertEqual(0, self.minesweeper.adjacent_mine_count(0, 9))

  def test_adjacent_mine_count_when_no_mines_in_corner_down_left(self):
    self.assertEqual(0, self.minesweeper.adjacent_mine_count(0, 9))

  def test_get_status_of_in_progress_game(self):
    self.assertEqual(GameStatus.PROGRESS, self.minesweeper.get_game_status())

  def test_get_game_status_of_losing_by_exposing_a_mine(self):
    self.minesweeper.set_mine(5, 5)
    self.minesweeper.expose(5, 5)
    self.assertEqual(GameStatus.LOST, self.minesweeper.get_game_status())

  def test_all_mines_sealed_with_no_mine_sealed(self):
    self.minesweeper.set_mine(0, 1)
    self.assertFalse(self.minesweeper.is_all_mines_sealed())

  def test_all_mines_sealed_with_two_mines_and_one_mine_sealed(self):
    self.minesweeper.set_mine(0, 1)
    self.minesweeper.set_mine(0, 3)
    self.minesweeper.toggle_seal(0, 3)

    self.assertFalse(self.minesweeper.is_all_mines_sealed())

  def test_all_mines_sealed_with_two_mines_and_two_mine_sealed(self):
    self.minesweeper.set_mine(0, 1)
    self.minesweeper.set_mine(0, 3)
    self.minesweeper.toggle_seal(0, 1)
    self.minesweeper.toggle_seal(0, 3)

    self.assertTrue(self.minesweeper.is_all_mines_sealed())

  def test_all_cells_exposed_with_no_exposed_cells(self):
    self.assertFalse(self.minesweeper.is_all_cells_exposed())

  def test_all_cells_exposed_with_all_exposed_cells(self):
    self.minesweeper.expose(0, 0)
    self.assertTrue(self.minesweeper.is_all_cells_exposed())

  def test_all_cells_exposed_with_one_cell_sealed(self):
    self.minesweeper.toggle_seal(3, 4)
    self.minesweeper.expose(0, 0)

    self.assertFalse(self.minesweeper.is_all_cells_exposed())

  def test_all_cells_exposed_with_one_cell_exposed(self):
    class MinesweeperStub(Minesweeper):
      def expose_neighbors(self, row, column):
        pass

    minesweeper = MinesweeperStub()
    minesweeper.expose(0, 0)

    self.assertFalse(minesweeper.is_all_cells_exposed())

  def test_all_cells_exposed_with_one_cell_unexposed(self):
    self.minesweeper.toggle_seal(3, 4)
    self.minesweeper.expose(0, 0)
    self.minesweeper.toggle_seal(3, 4)

    self.assertFalse(self.minesweeper.is_all_cells_exposed())

  def test_game_in_progress_all_mines_seal_and_other_cells_unexposed(self):
    self.minesweeper.set_mine(3, 5)
    self.minesweeper.toggle_seal(3, 5)

    self.assertEqual(GameStatus.PROGRESS, self.minesweeper.get_game_status())

  def test_game_in_progress_all_mines_seal_and_one_empty_cell_sealed(self):
    self.minesweeper.set_mine(3, 5)
    self.minesweeper.toggle_seal(3, 5)
    self.minesweeper.toggle_seal(4, 4)

    self.assertEqual(GameStatus.PROGRESS, self.minesweeper.get_game_status())

  def test_game_in_progress_all_mines_seal_and_one_adjacent_cell_unexposed(self):
    self.minesweeper.set_mine(3, 5)
    self.minesweeper.toggle_seal(3, 5)
    self.minesweeper.toggle_seal(3, 4)
    self.minesweeper.expose(0, 0)
    self.minesweeper.toggle_seal(3, 4)

    self.assertEqual(GameStatus.PROGRESS, self.minesweeper.get_game_status())

  def test_game_won_when_all_10_mines_sealed_and_other_cells_exposed(self):
    self.minesweeper.set_mines(0)

    for x in range(10):
      for y in range(10):
        if self.minesweeper.is_mine_at(x, y):
          self.minesweeper.toggle_seal(x, y)
        else :
          self.minesweeper.expose(x, y)

    self.assertEqual(GameStatus.WON, self.minesweeper.get_game_status())

  def test_set_mines_generates_10_mines_with_seed(self):
    self.minesweeper.set_mines(0)
    mine_count = 0
    for x in range(10):
      for y in range(10):
        if self.minesweeper.is_mine_at(x, y):
          mine_count+=1

    self.assertEqual(10, mine_count)

  def test_set_mines_generates_different_location_for_different_seed(self):
    self.minesweeper.set_mines(0)
    minesweeper_seed_one = Minesweeper()
    minesweeper_seed_one.set_mines(1)

    self.assertNotEqual(self.minesweeper.mine, minesweeper_seed_one.mine)


if __name__ == '__main__':
  unittest.main()
