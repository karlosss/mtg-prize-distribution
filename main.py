from argument_parsing import parser
from calculate_prize_distribution import calculate_prize_distribution
from parse_pairings import parse_pairings
from parse_standings import parse_standings
from predict_standings import predict_standings

args = parser.parse_args()
print(args)

if args.mode == "distribute":
    with open(args.standings_file_path) as f:
        raw_standings = f.readlines()

    standings = parse_standings(raw_standings)

    entitlement = calculate_prize_distribution(standings, args.num_boosters_in_prizepool, args.min_match_points_for_prize, args.multiplier_step)

    for e in entitlement.entries:
        if e.booster_count > 0:
            print(e.player_name, e.booster_count)

if args.mode == "predict":
    with open(args.standings_file_path) as f:
        raw_standings = f.readlines()
    with open(args.pairings_file_path) as f:
        raw_pairings = f.readlines()

    standings = parse_standings(raw_standings)
    pairings = parse_pairings(raw_pairings)

    predict_standings(standings, pairings, args.num_simulations, args.draw_chance, args.num_boosters_in_prizepool, args.min_match_points_for_prize, args.multiplier_step)

