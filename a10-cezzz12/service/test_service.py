import unittest
from domain.domain import CellState
from repository.repository import BoardRepository
from service.service import GameService


class TestGameService(unittest.TestCase):
    def setUp(self):
        self.repository = BoardRepository()
        self.service = GameService(self.repository)

    def test_make_move(self):
        # Valid move
        self.assertTrue(self.service.make_move(0, CellState.PLAYER))

        # Invalid column
        self.assertFalse(self.service.make_move(-1, CellState.PLAYER))
        self.assertFalse(self.service.make_move(7, CellState.PLAYER))

    def test_check_win_horizontal(self):
        # Create horizontal win
        for col in range(4):
            self.service.make_move(col, CellState.PLAYER)

        self.assertTrue(self.service.check_win(CellState.PLAYER))

    def test_check_win_vertical(self):
        # Create vertical win
        col = 0
        for _ in range(4):
            self.service.make_move(col, CellState.PLAYER)

        self.assertTrue(self.service.check_win(CellState.PLAYER))

    def test_check_win_diagonal(self):
        # Create diagonal win
        for i in range(4):
            for _ in range(i):
                self.service.make_move(i, CellState.COMPUTER)
            self.service.make_move(i, CellState.PLAYER)

        self.assertTrue(self.service.check_win(CellState.PLAYER))

    def test_computer_move_blocks_win(self):
        # Set up potential win for player
        for col in range(3):
            self.service.make_move(col, CellState.PLAYER)

        # Computer should block the win
        computer_move = self.service.computer_move()
        self.assertEqual(computer_move, 3)


if __name__ == '__main__':
    unittest.main()