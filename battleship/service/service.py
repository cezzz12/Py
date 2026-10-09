from domain.domain import Board,Position
from repository.repository import GameRepository
import random


class GameService:
    def __init__(self, repository):
        self.repository = repository
        self.BOARD_SIZE = 6
        self.MAX_SHIPS = 2

    def create_new_game(self, game_id):
        player_board = Board(self.BOARD_SIZE)
        computer_board = Board(self.BOARD_SIZE)
        targeting_board = Board(self.BOARD_SIZE)
        self.repository.save_game_state(game_id, player_board, computer_board, targeting_board, False)
        return player_board, targeting_board

    def place_ship(self, game_id, position_str):
        game_state = self.repository.load_game_state(game_id)
        if not game_state or game_state['game_started']:
            return False, "Game has already started!"

        if not Position.is_valid(position_str):
            return False, "Invalid position format!"

        position = Position(position_str[0], position_str[1:])
        player_board = game_state['player_board']

        if player_board.ship_count >= self.MAX_SHIPS:
            player_board.remove_oldest_ship()

        success = player_board.add_ship(position.row, position.col)
        self.repository.save_game_state(game_id, player_board,
                                        game_state['computer_board'],
                                        game_state['targeting_board'],
                                        game_state['game_started'])
        return success, "Ship placed successfully!" if success else "Position already occupied!"

    def start_game(self, game_id):
        game_state = self.repository.load_game_state(game_id)
        if not game_state:
            return False, "Game not found!"

        if game_state['game_started']:
            return False, "Game already started!"

        player_board = game_state['player_board']
        if player_board.ship_count != self.MAX_SHIPS:
            return False, f"Please place exactly {self.MAX_SHIPS} ships!"

        # Place computer ships
        computer_board = game_state['computer_board']
        while computer_board.ship_count < self.MAX_SHIPS:
            row = random.randint(0, self.BOARD_SIZE - 1)
            col = random.randint(0, self.BOARD_SIZE - 1)
            computer_board.add_ship(row, col)

        game_state['game_started'] = True
        self.repository.save_game_state(game_id, player_board, computer_board,
                                        game_state['targeting_board'], True)
        return True, "Game started successfully!"

    def process_attack(self, game_id, position_str):
        game_state = self.repository.load_game_state(game_id)
        if not game_state or not game_state['game_started']:
            return False, "Game not started!", None

        if not Position.is_valid(position_str):
            return False, "Invalid position format!", None

        position = Position(position_str[0], position_str[1:])
        computer_board = game_state['computer_board']
        targeting_board = game_state['targeting_board']
        player_board = game_state['player_board']

        # Player attack
        player_hit = computer_board.register_attack(position.row, position.col)
        targeting_board.grid[position.row][position.col] = 'X' if player_hit else 'O'

        if computer_board.gets_hit_count() >= self.MAX_SHIPS:
            return True, "Player wins!", game_state

        # Computer attack
        while True:
            computer_row = random.randint(0, self.BOARD_SIZE - 1)
            computer_col = random.randint(0, self.BOARD_SIZE - 1)
            if player_board.grid[computer_row][computer_col] not in ['X', 'O']:
                break

        computer_hit = player_board.register_attack(computer_row, computer_col)
        computer_pos = f"{chr(computer_col + ord('A'))}{computer_row}"

        if player_board.gets_hit_count() >= self.MAX_SHIPS:
            return True, f"Computer wins! (attacked {computer_pos})", game_state

        self.repository.save_game_state(game_id, player_board, computer_board,
                                        targeting_board, True)

        result_message = f"Attack at {position_str}: {'Hit' if player_hit else 'Miss'}\n"
        result_message += f"Computer attacks {computer_pos}: {'Hit' if computer_hit else 'Miss'}"
        return False, result_message, game_state
