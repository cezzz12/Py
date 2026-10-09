from src.domain.domain import Board,Position
from src.repository.repository import GameRepository
import random
import math

class GameService:
    def __init__(self, repository):
        self.repository = repository
        self.BOARD_SIZE = 7
        self.ALIEN_SHIPS = 2
        self.ASTEROIDS = 8

    def create_new_game(self, game_id):
        player_board = Board(self.BOARD_SIZE)
        self.repository.saveGameData(game_id, player_board, False)
        return player_board

    def start_game(self, game_id):
        game_state = self.repository.loadGameData(game_id)
        if not game_state:
            return False, "Game not found!"

        if game_state['game_started']:
            return False, "Game already started!"

        player_board = game_state['player_board']
        player_board.add_Earth(3,3)
        while player_board.AlienShip_count < self.ALIEN_SHIPS:
            row = random.randint(0, self.BOARD_SIZE-1)
            col = random.randint(0, self.BOARD_SIZE - 1)
            if abs(row-4)==4 or abs(col-3)==4:
                player_board.add_AlienShip(row, col)

        if player_board.AlienShip_count != self.ALIEN_SHIPS:
            return False, f"There must be exactly {self.ALIEN_SHIPS} ships!"

        row1 = random.randint(0, self.BOARD_SIZE - 1)
        col1 = random.randint(0, self.BOARD_SIZE - 1)
        player_board.add_Asteroid(row1, col1)
        rows=[]
        cols=[]
        rows.append(row1)
        cols.append(col1)
        while player_board.Asteroid_count < self.ASTEROIDS:
            row=random.randint(0,self.BOARD_SIZE-1)
            col=random.randint(0,self.BOARD_SIZE-1)
            player_board.add_Asteroid(row,col)

        if player_board.Asteroid_count != self.ASTEROIDS:
            return False, f"There must be exactly {self.ASTEROIDS} asteroids!"



        game_state['game_started'] = True
        self.repository.saveGameData(game_id, player_board, True)
        return True, "Game started successfully!"

    def process_attack(self, game_id, position_str):
        '''

        :param game_id:
        :param position_str: coordinates where we hit
        :return: game over true-continue false-stop
        message
        game state -the updated board

        '''
        game_state = self.repository.loadGameData(game_id)
        if not game_state or not game_state['game_started']:
            return False, "Game not started!", None

        if not Position.is_valid(position_str):
            return False, "Invalid position format!", None

        position = Position(position_str[0], position_str[1:])
        player_board = game_state['player_board']

        player_hit = player_board.register_attack(position.row, position.col)
        if player_hit:
            player_board.grid[position.row][position.col] = '-'
            self.ALIEN_SHIPS-=1
            if self.ALIEN_SHIPS == 0:
                return True,print("Hit.Alien Ship Destroyed.Player Won"),game_state
            if self.ALIEN_SHIPS == 1:
                return False,print("Hit.Alien Ship Destroyed"),game_state
        else:
            player_board.grid[position.row][position.col] = '-'
            return False,print("Miss.Alien Ship Moves"),game_state







