from src.repository.repository import GameRepository
from src.service.service import GameService
from src.ui.ui import GameUI
def main():
    repository = GameRepository()
    game_service = GameService(repository)
    ui = GameUI()
    game_id = "game1"

    player_board= game_service.create_new_game(game_id)
    ui.display_boards(player_board)

    while True:
        command = ui.get_command()
        if not command:
            continue

        elif command[0] == "start":
            success, message = game_service.start_game(game_id)
            ui.display_message(message)
            if success:
                state = repository.loadGameData(game_id)
                ui.display_boards(state['player_board'])

        elif command[0] == "fire" and len(command) == 2:
            game_over, message, state = game_service.process_attack(game_id, command[1])
            ui.display_message(message)
            if state:
                ui.display_boards(state['player_board'])
            if game_over:
                break

        elif command[0] == "quit":
            break
        else:
            ui.display_message("Invalid command! Available commands: start, attack <pos>, quit")

if __name__ == "__main__":
    main()