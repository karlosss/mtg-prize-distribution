import random
from collections import defaultdict, Counter
from copy import deepcopy

from calculate_prize_distribution import calculate_prize_distribution
from models import Standings, Pairings, StandingsEntry, PairingsEntry


def _simulate(most_recent_pts_per_player: dict[str, int], undecided_matches: list[PairingsEntry], draw_chance: float) -> Standings:
    d = deepcopy(most_recent_pts_per_player)
    for m in undecided_matches:
        if random.random() < draw_chance:
            d[m.player_a_name] += 1
            d[m.player_b_name] += 1
            continue

        if random.random() < 0.5:
            d[m.player_a_name] += 3
        else:
            d[m.player_b_name] += 3

    predicted_standings_entries = []
    for pl, pts in d.items():
        predicted_standings_entries.append(StandingsEntry(pl, pts))

    predicted_standings_entries.sort(key=lambda e: -e.points)

    return Standings(predicted_standings_entries)


def _create_simulations(last_standings: Standings, current_pairings: Pairings, num_simulations: int, draw_chance: float) -> list[Standings]:
    predicted_standings = {}

    for e in last_standings.entries:
        predicted_standings[e.player_name] = e.points

    matches_to_randomize = []

    for m in current_pairings.entries:
        if m.player_a_wins is None:
            matches_to_randomize.append(m)
            continue

        if m.player_a_wins > m.player_b_wins:
            predicted_standings[m.player_a_name] += 3
        elif m.player_b_wins > m.player_a_wins:
            predicted_standings[m.player_b_name] += 3
        else:
            predicted_standings[m.player_a_name] += 1
            predicted_standings[m.player_b_name] += 1

    return [_simulate(predicted_standings, matches_to_randomize, draw_chance) for _ in range(num_simulations)]


def predict_standings(last_standings: Standings, current_pairings: Pairings, num_simulations: int, draw_chance: float, booster_count: int, min_match_pts_for_prizes: int, match_points_multiplier_step: float) -> None:
    simulations = _create_simulations(last_standings, current_pairings, num_simulations, draw_chance)

    boos_for_player = defaultdict(list)

    for s in simulations:
        entitlement = calculate_prize_distribution(s, booster_count, min_match_pts_for_prizes, match_points_multiplier_step)
        for e in entitlement.entries:
            boos_for_player[e.player_name].append(e.booster_count)

    agg = {k: Counter(v) for k, v in boos_for_player.items()}
    for pl, inf in sorted(agg.items()):
        print(pl, end=" ")
        for boos, occurrences in sorted(inf.items()):
            print(f"{boos} ({occurrences}) ", end="")
        print()
