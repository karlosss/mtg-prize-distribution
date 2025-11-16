import re

from models import Standings, StandingsEntry


def _process_row(row: str) -> tuple[str, int]:
    sp = row.split()
    points = int(sp[-5])
    name = " ".join(sp[1:-5])
    return name, points


def parse_standings(raw_standings_lines: list[str]) -> Standings:
    empty_row_regex = re.compile(r"^\s*$")

    standings_start_regex = re.compile(r"^\s*Rank\s+Name\s+Points\s+W/L/D\s+OMW%\s+GW%\s+OGW%\s*$")
    standings_end_regex = re.compile(r"^\s*Terms\s*$")

    entries = []

    started = False
    for row in raw_standings_lines:
        if empty_row_regex.match(row):
            continue

        if not started and not standings_start_regex.match(row):
            continue

        if standings_start_regex.match(row):
            started = True
            continue

        if started and standings_end_regex.match(row):
            break

        name, points = _process_row(row)
        entries.append(StandingsEntry(name, points))

    return Standings(entries)
