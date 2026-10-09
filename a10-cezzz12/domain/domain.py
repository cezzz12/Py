from enum import Enum
from dataclasses import dataclass


class CellState(Enum):
    EMPTY = 0
    PLAYER = 1
    COMPUTER = 2


@dataclass
class Position:
    row: int
    col: int


class Board:
    def __init__(self, rows=6, cols=7):
        self.rows = rows
        self.cols = cols
        self.board = [[CellState.EMPTY for _ in range(cols)] for _ in range(rows)]

    def get_cell(self, position: Position) -> CellState:
        """Get the state of a cell at given position"""
        return self.board[position.row][position.col]

    def set_cell(self, position: Position, state: CellState) -> None:
        """Set the state of a cell at given position"""
        self.board[position.row][position.col] = state

    def is_column_full(self, col: int) -> bool:
        """Check if a column is full"""
        return self.board[0][col] != CellState.EMPTY

    def get_next_empty_row(self, col: int) -> int:
        """Get the next empty row in a column"""
        for row in range(self.rows - 1, -1, -1):
            if self.board[row][col] == CellState.EMPTY:
                return row
        return -1