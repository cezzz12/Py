import random

from domain.domain import Player


class PlayerRepository:
    def __init__(self):
        self.players = []

    def load_from_file(self,file_path):
        with open(file_path, "r") as file:
            for line in file:
                parts = line.split(",")
                player = Player(int(parts[0]), parts[1], int(parts[2]))
                self.players.append(player)
    def get_all_players(self):
        return self.players
    def sort_players_by_strength_desc(self):
        self.players.sort(key=lambda p: p.strength, reverse=True)
    def get_lowest_strength_players(self, count):
        return self.players[-count:] if count > 0 else []