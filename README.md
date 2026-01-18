# Prize distribution calculator

This is a simple tool to help with prize distribution in Magic: The Gathering tournaments which run in EventLink.

## Specification

This tool is helpful in situations where there is a fixed number of booster packs in the prize pool 
(for example 3 per player) and the packs are distributed based on achieved match points:

- If any two players have equal match points, they receive equal amounts of booster packs.
- A player with more match points will receive at least as many booster packs as all players with less match points.

The tool supports discarding players who did not achieve enough match points to win prizes, as well as parametrizing
the "steepness" of the prize distribution - the "steeper" the distribution, the more it favors top players.

The tool also supports estimating the prize distribution during the last round of the tournament - this is useful
when a player already finished their last round's match and wants to grab prizes and leave. In this case, the tool
looks at the standings from the previous round, pairings of the last round amd match results of the last round's
matches that have already finished, and then runs stochastic simulations (by default 10 000, but can be parametrized)
of the not-yet-finished matches. Each simulation consists of randomly guessing the result of each open match, assigning
prizes to the players, and then reporting in how many of those simulations a player received a particular amount
of booster packs. Then, it should be relatively safe to give out the least amount of packs that occurred during the simulations. 

### Calculation method

The problem of assigning booster packs to players is similar to assigning seats in parliaments based on election results.
A method that assigns indivisible items (parliament seats or booster packs) based on proportions is generally called an
[apportionment method](https://en.wikipedia.org/wiki/Mathematics_of_apportionment).

In case of assigning booster packs, we first discard all players that did not manage to make enough match points to win prizes.

Then, players are separated into groups (sets) where each of those groups consists of all the players with equal match points.

After that, the match points for each group correspond to the number of "votes" in the apportionment method. The number
of match points of each group is then multiplied by a multiplier. The group with least points is multiplied by 1. Each
of the following groups is multiplied by the previous multiplier + a configurable step (default 0.4). This step is
configurable and the higher the step, the "steeper" the prize distribution will be.

Example: Some amount of players achieved 8 match points, some 9, some 10, some 11 and some 12. Say the step is 0.5. Therefore,
the original points `[8, 9, 10, 11, 12]` will be transformed into `[8*(1+0*0.5), 9*(1+1*0.5), 10*(1+2*0.5), 11*(1+3*0.5), 12*(1+4*0.5)]` which
equals to `[8, 13.5, 20, 27.5, 36]`.

After the multiplication, the [Largest Remainder Method](https://en.wikipedia.org/wiki/Quota_method) is applied: first,
the quota, or the amount of booster packs per a multiplied match point, is calculated. Then, each player is assigned
a whole amount of booster packs, computed as the multiplied match points achieved times the quota, rounded down
to the nearest integer. The remaining booster packs are then divided in order from the group that has the largest
remainder.

Because all players with the same match points have to receive the same amount of booster packs, it might happen
that a group cannot be assigned additional booster packs, because there are more players with this amount of
match points than remaining booster packs. In this case, the group is skipped and the algorithm tries the next group
in order. A group is also skipped if assigning an extra pack to this group would result in players in this group having
more booster packs than a player in a higher ranked group.

Packs that cannot be fairly assigned are not assigned to anyone.

## Installation

- Install some decently new Python 3.
- Clone the repository
- run `main.py` in the CLI.

## Usage

### Prize distribution after the tournament

- Go to the final standings page in EventLink
- Select all (Ctrl+A), copy (Ctrl+C), paste the contents to an empty file and save it.
- `python main.py distribute -s <path_to_standings_file> -m <minimum_amount_of_match_points_required_to_win_prizes> -b <number_of_boosters_in_the_prizepool>`
  - for example `python main.py distribute -s C:\Desktop\standings.txt -m 8 -b 150`
- For 2HG, there is an option to enforce that every team gets even number of booster packs.

The output shows some debug information, but more importantly the name of each player together with the number of booster
packs they should receive.

### Final standings and distribution prediction (Does not work for 2HG)

- Copy data from EventLink in the same way as in the previous step, except this time do the same with the current pairings page too
- `python main.py distribute -s <path_to_standings_file> -p <path_to_pairings_file> -m <minimum_amount_of_match_points_required_to_win_prizes> -b <number_of_boosters_in_the_prizepool>`
  - for example `python main.py distribute -s C:\Desktop\standings.txt -p C:\Desktop\pairings.txt -m 8 -b 150`

The output again shows some debug information, and for each player number of booster packs they receive, followed by a number
in parentheses, denoting in how many simulations the player received this amount of booster packs.
