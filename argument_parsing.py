import argparse

parser = argparse.ArgumentParser(description="Prize distribution helper")
subparsers = parser.add_subparsers(
    title="modes",
    dest="mode",
    metavar="<mode>",
    required=True,
    help="Operational mode. Choose one of: predict, distribute."
)

# Predict mode
predict = subparsers.add_parser(
    "predict",
    help="Run simulations to predict outcomes. Does not work for 2HG."
)
predict.add_argument(
    "-p", "--pairings-file-path",
    required=True,
    type=str,
    metavar="<pairings_file_path>",
    help="Path to the pairing file (required)."
)
predict.add_argument(
    "-s", "--standings-file-path",
    required=True,
    type=str,
    metavar="<standings_file_path>",
    help="Path to the current standings file (required)."
)
predict.add_argument(
    "-n", "--num-simulations",
    default=10000,
    type=int,
    metavar="<num_simulations>",
    help="Number of simulations to run (default: 1000)."
)
predict.add_argument(
    "-d", "--draw-chance",
    default=0.10,
    type=float,
    metavar="<draw_chance>",
    help="Chance of a draw in a match (0–1, default: 0.1)."
)
predict.add_argument(
    "-m", "--min-match-points-for-prize",
    required=True,
    type=int,
    metavar="<min_match_points_for_prize>",
    help="Minimum number of match points required to win prizes."
)
predict.add_argument(
    "-b", "--num-boosters-in-prizepool",
    required=True,
    type=int,
    metavar="<num_boosters_in_prizepool>",
    help="Number of boosters in prizepool."
)
predict.add_argument(
    "-x", "--multiplier-step",
    default=0.40,
    type=float,
    metavar="<multiplier_step>",
    help="Match points multiplier step increment (default: 0.4)."
)

# Distribute mode
distribute = subparsers.add_parser(
    "distribute",
    help="Calculate prize distribution."
)
distribute.add_argument(
    "-s", "--standings-file-path",
    required=True,
    type=str,
    metavar="<standings_file_path>",
    help="Path to the current standings file (required)."
)
distribute.add_argument(
    "-m", "--min-match-points-for-prize",
    required=True,
    type=int,
    metavar="<min_match_points_for_prize>",
    help="Minimum number of match points required to win prizes."
)
distribute.add_argument(
    "-b", "--num-boosters-in-prizepool",
    required=True,
    type=int,
    metavar="<num_boosters_in_prizepool>",
    help="Number of boosters in prizepool."
)
distribute.add_argument(
    "-x", "--multiplier-step",
    default=0.40,
    type=float,
    metavar="<multiplier_step>",
    help="Match points multiplier step increment (default: 0.4)."
)
distribute.add_argument(
    "-e", "--even",
    action="store_true",
    help="Enforces each player gets even number of booster packs (useful for 2HG)"
)
