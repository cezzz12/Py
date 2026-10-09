class TournamentUI:
    def __init__(self, service):
        self.service = service

    def display_players(self):
        players = self.service.display_players_sorted()
        print("Players sorted by strength:")
        for player in players:
            print(player)

    def start_tournament(self):
        players = self.service.display_players_sorted()
        qualification_winners = self.service.play_qualification_round()

        tournament_players = qualification_winners + players[:len(players) - 2 * len(qualification_winners)]
        round_number = 1

        while len(tournament_players) > 1:
            print(f"\nRound {round_number}: {len(tournament_players)} players remaining")
            tournament_players = self.service.play_tournament_round(tournament_players)
            round_number += 1

        print(f"\nThe winner of the tournament is {tournament_players[0].name}!")
