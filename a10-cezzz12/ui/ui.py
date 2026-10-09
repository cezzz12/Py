from domain.domain import CellState,Position
from service.service import GameService

class ConsoleUI:
    def __init__(self, service: GameService):
        self._service = service

    def display_board(self) -> None:
        """Display the current state of the board"""
        board = self._service._repository.get_board()
        print("\n")
        for row in range(board.rows):
            print("|", end=" ")
            for col in range(board.cols):
                cell = board.get_cell(Position(row, col))
                if cell == CellState.EMPTY:
                    print(".", end=" ")
                elif cell == CellState.PLAYER:
                    print("X", end=" ")
                else:
                    print("O", end=" ")
            print("|")
        print("-" * (board.cols * 2 + 3))
        print(" ", end=" ")
        for i in range(board.cols):
            print(i, end=" ")
        print("\n")

    def get_player_move(self) -> int:
        """Get and validate player's move"""
        while True:
            try:
                col = int(input("Enter column number (0-6): "))
                return col
            except ValueError:
                print("Please enter a valid number")

    def play_game(self) -> None:
        """Main game loop"""
        print("Welcome to Connect Four!")
        print("You are X, computer is O")

        while True:
            self.display_board()

            # Player's turn
            while True:
                col = self.get_player_move()
                if self._service.make_move(col, CellState.PLAYER):
                    break
                print("Invalid move! Try again.")

            if self._service.check_win(CellState.PLAYER):
                self.display_board()
                print("You win!")
                break

            if self._service.is_board_full():
                self.display_board()
                print("It's a draw!")
                break

            # Computer's turn
            print("Computer is thinking...")
            col = self._service.computer_move()
            if col is not None:
                self._service.make_move(col, CellState.COMPUTER)
                print(f"Computer placed in column {col}")

            if self._service.check_win(CellState.COMPUTER):
                self.display_board()
                print("Computer wins!")
                break

            if self._service.is_board_full():
                self.display_board()
                print("It's a draw!")
                break