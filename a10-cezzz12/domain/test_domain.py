import unittest
from domain.domain import Board, CellState, Position


class TestBoard(unittest.TestCase):
    def setUp(self):
        self.board = Board()

    def test_initial_board_empty(self):
        for row in range(self.board.rows):
            for col in range(self.board.cols):
                self.assertEqual(self.board.get_cell(Position(row, col)), CellState.EMPTY)

    def test_set_cell(self):
        pos = Position(0, 0)
        self.board.set_cell(pos, CellState.PLAYER)
        self.assertEqual(self.board.get_cell(pos), CellState.PLAYER)

    def test_is_column_full(self):
        col = 0
        self.assertFalse(self.board.is_column_full(col))

        # Fill column
        for row in range(self.board.rows):
            self.board.set_cell(Position(row, col), CellState.PLAYER)

        self.assertTrue(self.board.is_column_full(col))

    def test_get_next_empty_row(self):
        col = 0
        self.assertEqual(self.board.get_next_empty_row(col), self.board.rows - 1)

        # Add one piece
        self.board.set_cell(Position(self.board.rows - 1, col), CellState.PLAYER)
        self.assertEqual(self.board.get_next_empty_row(col), self.board.rows - 2)
