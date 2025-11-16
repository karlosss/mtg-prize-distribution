from collections import defaultdict

from models import Standings, PrizeEntitlementEntry, PrizeEntitlement


def _get_votes_per_group(players_with_points: dict[int, set[str]], points_multiplier_step: float) -> list[float]:
    pts = list(sorted(players_with_points.keys(), reverse=True))

    votes_per_group = [p*i for p, i in zip(pts, reversed([1+x*points_multiplier_step for x, _ in enumerate(pts)]))]
    return votes_per_group


def calculate_prize_distribution(final_standings: Standings, booster_count: int, min_match_pts_for_prizes: int, match_points_multiplier_step: float) -> PrizeEntitlement:
    prizes_only_standings = Standings([e for e in final_standings.entries if e.points >= min_match_pts_for_prizes])

    players_with_points = defaultdict(set)

    for e in prizes_only_standings.entries:
        players_with_points[e.points].add(e.player_name)

    votes_per_group = _get_votes_per_group(players_with_points, match_points_multiplier_step)
    print("votes per point group: ", votes_per_group)

    groups = list(map(lambda p: players_with_points[p], sorted(players_with_points.keys(), key=lambda k: -k)))
    group_sizes = [len(g) for g in groups]
    print("point group sizes: ", group_sizes)

    total_votes = sum([a * b for a, b in zip(votes_per_group, group_sizes)])
    boosters_per_vote = booster_count / total_votes
    print("total votes: ", total_votes)
    print("boosters per vote: ", boosters_per_vote)

    exact_entitlements = [boosters_per_vote * votes for votes in votes_per_group]
    base_entitlements = [int(boosters_per_vote * votes) for votes in votes_per_group]
    remainders = [e-b for e, b in zip(exact_entitlements, base_entitlements)]
    print("exact entitlements: ", exact_entitlements)
    print("base entitlements: ", base_entitlements)

    remaining_boosters = booster_count - sum([a * b for a, b in zip(base_entitlements, group_sizes)])
    print("remaining boosters: ", remaining_boosters)

    remainders_order = [r[1] for r in list(sorted([(-r, i) for i, r in enumerate(remainders)]))]

    i = 0
    noop_cnt = 0
    while True:
        group_i = remainders_order[i]
        needed_boosters = group_sizes[group_i]
        if needed_boosters <= remaining_boosters and (group_i == 0 or base_entitlements[group_i] < base_entitlements[group_i - 1]):
            base_entitlements[group_i] += 1
            remaining_boosters -= needed_boosters
            noop_cnt = -1
            print(f"assigning {needed_boosters} boosters to group {group_i}, remaining boosters: {remaining_boosters}")
        noop_cnt += 1
        i += 1
        i = i % len(groups)
        if noop_cnt > len(groups):
            break

    print("final entitlements: ", base_entitlements)
    print("remaining boosters: ", remaining_boosters)
    print("assigned boosters: ", sum([b*s for b, s in zip(base_entitlements, group_sizes)]))
    print("=========================")

    entries = []
    for g, e in zip(groups, base_entitlements):
        for pl in g:
            entries.append(PrizeEntitlementEntry(pl, e))

    return PrizeEntitlement(entries)
