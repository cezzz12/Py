from repository.repository import PlayerRepository
from service.service import TournamentService
from ui.ui import TournamentUI
import os

def create_players_file(file_path):
    if not os.path.exists(file_path):
        players_data = """\
108, Alice, 45
101, Bob, 34
102, Eve, 68
103, Carla, 56
104, James, 55
105, Johnny, 33
106, Miguel, 36
107, Robby, 90
108, Lawrence, 89
109, Hillary, 88
110, Terry, 40
111, Dave, 60
112, Andrea, 59
"""
        with open(file_path, "w") as file:
            file.write(players_data)
        print(f"File created at: {file_path}")

def main():
    file_path = "players.txt"
    create_players_file(file_path)  # Ensure the file is created

    repo = PlayerRepository()
    repo.load_from_file(file_path)

    service = TournamentService(repo)
    ui = TournamentUI(service)

    ui.display_players()
    ui.start_tournament()

if __name__ == "__main__":
    main()
