from src.domain.domain import Board,Position
from src.repository.repository import GameRepository
from src.service.service import GameService
from texttable import Texttable

class GameUI:
    @staticmethod
    def display_boards(player_board):
        def create_table(board):
            table = Texttable()
            header = [''] + [chr(i + ord('A')) for i in range(board.size)]
            table.header(header)
            for i in range(board.size):
                row = [str(i)] + board.grid[i]
                table.add_row(row)

            return table

        print("\nPlayer board:")
        print(create_table(player_board).draw())

    @staticmethod
    def get_command():
        return input("Enter command: ").lower().split()

    @staticmethod
    def display_message(message):
        print(message)



