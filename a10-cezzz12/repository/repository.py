from domain.domain import Board
class BoardRepository:
    def __init__(self):
        self._board = Board()

    def get_board(self) -> Board:
        """Get the current game board"""
        return self._board

    def reset_board(self) -> None:
        """Reset the game board"""
        self._board = Board()
