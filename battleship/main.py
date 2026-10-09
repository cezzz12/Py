from repository.repository import GameRepository
from service.service import GameService
from ui.ui import GameUI
def main():
    repository = GameRepository()
    game_service = GameService(repository)
    ui = GameUI()
    game_id = "game1"  # In a real application, this would be generated

    player_board, targeting_board = game_service.create_new_game(game_id)
    ui.display_message("Welcome to Battleship! Place your ships using 'ship <position>' (e.g., ship A0)")
    ui.display_boards(player_board, targeting_board)

    while True:
        command = ui.get_command()
        if not command:
            continue

        if command[0] == "ship" and len(command) == 2:
            success, message = game_service.place_ship(game_id, command[1])
            ui.display_message(message)
            if success:
                state = repository.load_game_state(game_id)
                ui.display_boards(state['player_board'], state['targeting_board'])

        elif command[0] == "start":
            success, message = game_service.start_game(game_id)
            ui.display_message(message)
            if success:
                state = repository.load_game_state(game_id)
                ui.display_boards(state['player_board'], state['targeting_board'])

        elif command[0] == "attack" and len(command) == 2:
            game_over, message, state = game_service.process_attack(game_id, command[1])
            ui.display_message(message)
            if state:
                ui.display_boards(state['player_board'], state['targeting_board'])
            if game_over:
                break

        elif command[0] == "quit":
            break
        else:
            ui.display_message("Invalid command! Available commands: ship <pos>, start, attack <pos>, quit")

if __name__ == "__main__":
    main()