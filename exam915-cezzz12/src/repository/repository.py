from src.domain.domain import Board,Position
class GameRepository:
    def __init__(self):
        self.game_states={}

    def saveGameData(self,game_id,player_board,game_started):
        self.game_states[game_id] = {
            'player_board':player_board,
            'game_started':game_started
        }
    def loadGameData(self,game_id):
        return self.game_states[game_id]