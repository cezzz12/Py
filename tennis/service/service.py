import random
class TournamentService:
    def __init__(self, repository):
        self.repository = repository

    def display_players_sorted(self):
        self.repository.sort_players_by_strength_desc()
        return self.repository.get_all_players()

    def play_qualification_round(self):
        players = self.repository.get_all_players()
        count_to_eliminate = len(players) - self._nearest_power_of_two(len(players))
        qualification_players = self.repository.get_lowest_strength_players(count_to_eliminate * 2)

        pairs = self._pair_players_randomly(qualification_players)
        winners = []
        for pair in pairs:
            winner = self._play_match(pair)
            winners.append(winner)
        return winners

    def play_tournament_round(self, players):
        pairs = self._pair_players_randomly(players)
        winners = []
        for pair in pairs:
            winner = self._play_match(pair)
            winners.append(winner)
        return winners

    def _play_match(self, pair):
        print(f"Match: {pair[0]} vs {pair[1]}")
        while True:
            choice = input(f"Enter winner (1 for {pair[0].name}, 2 for {pair[1].name}): ")
            if choice in {"1", "2"}:
                winner_index = int(choice) - 1
                break
            print("Choose 1 or 2.")
        winner = pair[winner_index]
        winner.increase_strength()
        return winner

    def _pair_players_randomly(self, players):
        random.shuffle(players)
        return [(players[i], players[i + 1]) for i in range(0, len(players), 2)]

    def _nearest_power_of_two(self, n):
        power = 1
        while power < n:
            power *= 2
        return power if power == n else power // 2
