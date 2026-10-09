from domain.domain import Board,Position
class GameRepository:
    def __init__(self):
        self.game_states={}

    def save_game_state(self,game_id,player_board,computer_board,target_board,game_started):
        self.game_states[game_id] = {
            'player_board':player_board,
            'computer_board':computer_board,
            'targeting_board':target_board,
            'game_started':game_started
        }
    def load_game_state(self,game_id):
        return self.game_states.get(game_id)