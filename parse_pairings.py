import re

from models import Pairings, PairingsEntry


def parse_pairings(raw_pairings_lines: list[str]) -> Pairings:
    empty_row_regex = re.compile(r"^\s*$")

    pairing_start_regex = re.compile(r"^\s*Table\s+Player #1\s+Match Results\s+Player #2\s*$")
    pairing_end_regex = re.compile(r"^\s*(Begin the timer when all players are seated in their matches\.|Terms)\s*$")

    wins_or_table_regex = re.compile(r"^\s*(\d+|_)\s*$")

    ignore_regexes = [
        re.compile(r"^\s*\d+.\d+.\d+\s*$"),
    ]

    parsed = []

    started = False
    for row in raw_pairings_lines:
        if empty_row_regex.match(row):
            continue

        if not started and not pairing_start_regex.match(row):
            continue

        if pairing_start_regex.match(row):
            started = True
            continue

        if started and pairing_end_regex.match(row):
            break

        if started and wins_or_table_regex.match(row):
            parsed.append(row.strip())
            continue

        if started and all([not r.match(row) for r in ignore_regexes]):
            parsed.append(" ".join(row.split()))

    entries = []

    for i in range(0, len(parsed), 5):
        if i+5 > len(parsed):
            p1, p1w, p2w, p2 = parsed[i:i + 4]
        else:
            _, p1, p1w, p2w, p2 = parsed[i:i+5]
        p1wins = None if p1w == '_' else int(p1w)
        p2wins = None if p2w == '_' else int(p2w)
        entries.append(PairingsEntry(p1, p2, p1wins, p2wins))

    return Pairings(entries)
