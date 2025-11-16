from dataclasses import dataclass


@dataclass
class StandingsEntry:
    player_name: str
    points: int


@dataclass
class Standings:
    entries: list[StandingsEntry]


@dataclass
class PairingsEntry:
    player_a_name: str
    player_b_name: str
    player_a_wins: int | None
    player_b_wins: int | None


@dataclass
class Pairings:
    entries: list[PairingsEntry]


@dataclass
class PrizeEntitlementEntry:
    player_name: str
    booster_count: int


@dataclass
class PrizeEntitlement:
    entries: list[PrizeEntitlementEntry]