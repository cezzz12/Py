from typing import Optional, List, Tuple
from domain.domain import Board, CellState, Position
from repository.repository import BoardRepository

class GameService:
    def __init__(self, repository):
        self._repository = repository
        self.MAX_DEPTH = 5  # Adjust this value to balance performance vs AI strength

    def make_move(self, col: int, player: CellState) -> bool:
        """
        Make a move in the specified column
        Returns True if move was successful, False otherwise
        """
        board = self._repository.get_board()
        if col < 0 or col >= board.cols or board.is_column_full(col):
            return False

        row = board.get_next_empty_row(col)
        if row == -1:
            return False

        board.set_cell(Position(row, col), player)
        return True

    def check_win(self, player: CellState) -> bool:
        """Check if the specified player has won"""
        board = self._repository.get_board()

        for row in range(board.rows):
            for col in range(board.cols - 3):
                if all(board.get_cell(Position(row, col + i)) == player for i in range(4)):
                    return True

        # Check vertical
        for row in range(board.rows - 3):
            for col in range(board.cols):
                if all(board.get_cell(Position(row + i, col)) == player for i in range(4)):
                    return True

        for row in range(board.rows - 3):
            for col in range(board.cols - 3):
                if all(board.get_cell(Position(row + i, col + i)) == player for i in range(4)):
                    return True

        for row in range(3, board.rows):
            for col in range(board.cols - 3):
                if all(board.get_cell(Position(row - i, col + i)) == player for i in range(4)):
                    return True

        return False

    def is_board_full(self) -> bool:
        """Check if the board is full"""
        board = self._repository.get_board()
        return all(board.is_column_full(col) for col in range(board.cols))

    def get_valid_moves(self) -> List[int]:
        """Get list of valid moves (non-full columns)"""
        board = self._repository.get_board()
        return [col for col in range(board.cols) if not board.is_column_full(col)]

    def evaluate_window(self, window: List[CellState], player: CellState) -> int:
        opponent = CellState.PLAYER if player == CellState.COMPUTER else CellState.COMPUTER

        if window.count(player) == 4:
            return 100
        elif window.count(player) == 3 and window.count(CellState.EMPTY) == 1:
            return 5
        elif window.count(player) == 2 and window.count(CellState.EMPTY) == 2:
            return 2
        elif window.count(opponent) == 3 and window.count(CellState.EMPTY) == 1:
            return -4

        return 0

    def evaluate_position(self, player: CellState) -> int:
        """
        Evaluate the current board position for the given player
        Returns a score representing how good the position is
        """
        board = self._repository.get_board()
        score = 0

        # Horizontal windows
        for row in range(board.rows):
            for col in range(board.cols - 3):
                window = [board.get_cell(Position(row, col + i)) for i in range(4)]
                score += self.evaluate_window(window, player)

        # Vertical windows
        for row in range(board.rows - 3):
            for col in range(board.cols):
                window = [board.get_cell(Position(row + i, col)) for i in range(4)]
                score += self.evaluate_window(window, player)

        # Diagonal windows (positive slope)
        for row in range(board.rows - 3):
            for col in range(board.cols - 3):
                window = [board.get_cell(Position(row + i, col + i)) for i in range(4)]
                score += self.evaluate_window(window, player)

        # Diagonal windows (negative slope)
        for row in range(3, board.rows):
            for col in range(board.cols - 3):
                window = [board.get_cell(Position(row - i, col + i)) for i in range(4)]
                score += self.evaluate_window(window, player)

        # Center column preference
        center_col = board.cols // 2
        center_count = sum(1 for row in range(board.rows)
                           if board.get_cell(Position(row, center_col)) == player)
        score += center_count * 3

        return score

    def minimax(self, depth: int, alpha: int, beta: int, maximizing_player: bool) -> Tuple[int, Optional[int]]:
        """
        Implement minimax algorithm with alpha-beta pruning
        Returns (score, column) tuple
        """
        board = self._repository.get_board()
        valid_moves = self.get_valid_moves()

        # Terminal conditions
        if self.check_win(CellState.COMPUTER):
            return (10000, None)
        if self.check_win(CellState.PLAYER):
            return (-10000, None)
        if not valid_moves or depth == 0:
            return (self.evaluate_position(CellState.COMPUTER), None)

        if maximizing_player:
            value = float('-inf')
            column = valid_moves[0]
            for col in valid_moves:
                row = board.get_next_empty_row(col)
                board.set_cell(Position(row, col), CellState.COMPUTER)

                new_score = self.minimax(depth - 1, alpha, beta, False)[0]
                board.set_cell(Position(row, col), CellState.EMPTY)

                if new_score > value:
                    value = new_score
                    column = col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return (value, column)

        else:
            value = float('inf')
            column = valid_moves[0]
            for col in valid_moves:
                row = board.get_next_empty_row(col)
                board.set_cell(Position(row, col), CellState.PLAYER)

                new_score = self.minimax(depth - 1, alpha, beta, True)[0]
                board.set_cell(Position(row, col), CellState.EMPTY)

                if new_score < value:
                    value = new_score
                    column = col
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return (value, column)

    def computer_move(self) -> Optional[int]:
        """
        Make computer move using minimax algorithm
        Returns the column where the computer makes its move
        """
        valid_moves = self.get_valid_moves()
        if not valid_moves:
            return None

        # If this is the first move, play in the center for better performance
        board = self._repository.get_board()
        if all(board.get_cell(Position(row, col)) == CellState.EMPTY
               for row in range(board.rows) for col in range(board.cols)):
            return board.cols // 2

        # Use minimax for all other moves
        _, column = self.minimax(self.MAX_DEPTH, float('-inf'), float('inf'), True)
        return column