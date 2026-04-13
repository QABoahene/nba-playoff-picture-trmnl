from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any

from nba_api.stats.static import teams
from src.clients.nba_client import NBAClient


BRACKET_SLOT_ORDER = (
    ("east_1_8", 1, 8),
    ("east_4_5", 4, 5),
    ("east_2_7", 2, 7),
    ("east_3_6", 3, 6),
    ("west_1_8", 1, 8),
    ("west_4_5", 4, 5),
    ("west_2_7", 2, 7),
    ("west_3_6", 3, 6),
)

TEAM_METADATA_BY_ID = {team["id"]: team for team in teams.get_teams()}


class PlayoffPictureService:
    """Builds plugin-ready structures from raw NBA API responses."""

    def __init__(self, client: NBAClient | None = None):
        self.client = client or NBAClient()

    def get_playoff_snapshot(
        self, *, season_id: str | None = None, game_date: str | None = None
    ) -> dict[str, Any]:
        playoff_picture = self.client.get_playoff_picture(season_id=season_id)
        postseason_games, warnings = self.client.get_recent_postseason_games(
            date_from=self._build_recent_games_start_date(game_date),
            date_to=game_date or "",
        )

        return {
            "bracket": self._build_bracket(
                playoff_picture.get("EastConfPlayoffPicture", []),
                playoff_picture.get("EastConfStandings", []),
                playoff_picture.get("WestConfPlayoffPicture", []),
                playoff_picture.get("WestConfStandings", []),
            ),
            "recent_games": self._build_recent_games(postseason_games),
            "warnings": warnings,
        }

    def _build_bracket(
        self,
        east_series_rows: list[dict[str, Any]],
        east_standings_rows: list[dict[str, Any]],
        west_series_rows: list[dict[str, Any]],
        west_standings_rows: list[dict[str, Any]],
    ) -> dict[str, Any]:
        east_slots = self._build_conference_slots(
            "east", east_series_rows, east_standings_rows
        )
        west_slots = self._build_conference_slots(
            "west", west_series_rows, west_standings_rows
        )

        slots = {}
        slots.update(east_slots)
        slots.update(west_slots)

        return {
            "slots": slots,
            "slot_order": [slot_name for slot_name, _, _ in BRACKET_SLOT_ORDER],
            "east": [
                east_slots[slot_name]
                for slot_name, _, _ in BRACKET_SLOT_ORDER
                if slot_name.startswith("east_")
            ],
            "west": [
                west_slots[slot_name]
                for slot_name, _, _ in BRACKET_SLOT_ORDER
                if slot_name.startswith("west_")
            ],
        }

    def _build_conference_slots(
        self,
        conference: str,
        series_rows: list[dict[str, Any]],
        standings_rows: list[dict[str, Any]],
    ) -> dict[str, Any]:
        standings_by_team_id = {
            row["TEAM_ID"]: {
                "rank": row["RANK"],
                "team": row["TEAM"],
                "team_id": row["TEAM_ID"],
                "abbreviation": self._team_abbreviation(row["TEAM_ID"]),
                "wins": row["WINS"],
                "losses": row["LOSSES"],
                "clinched_playoffs": row.get("CLINCHED_PLAYOFFS"),
                "clinched_play_in": row.get("Clinched_Play_In"),
            }
            for row in standings_rows
        }

        series_by_matchup: dict[tuple[int, int], dict[str, Any]] = {}
        for row in series_rows:
            high_seed_id = row["HIGH_SEED_TEAM_ID"]
            low_seed_id = row["LOW_SEED_TEAM_ID"]

            series_by_matchup[(row["HIGH_SEED_RANK"], row["LOW_SEED_RANK"])] = {
                "conference": row["CONFERENCE"],
                "slot_key": f"{conference}_{row['HIGH_SEED_RANK']}_{row['LOW_SEED_RANK']}",
                "high_seed": self._build_team_display(
                    rank=row["HIGH_SEED_RANK"],
                    team_name=row["HIGH_SEED_TEAM"],
                    team_id=high_seed_id,
                    standing=standings_by_team_id.get(high_seed_id),
                ),
                "low_seed": self._build_team_display(
                    rank=row["LOW_SEED_RANK"],
                    team_name=row["LOW_SEED_TEAM"],
                    team_id=low_seed_id,
                    standing=standings_by_team_id.get(low_seed_id),
                ),
                "series_record": {
                    "high_seed_wins": row["HIGH_SEED_SERIES_W"],
                    "low_seed_wins": row["HIGH_SEED_SERIES_L"],
                    "display": f"{row['HIGH_SEED_SERIES_W']}-{row['HIGH_SEED_SERIES_L']}",
                },
                "games_remaining": row["HIGH_SEED_SERIES_REMAINING_G"],
                "status_text": self._series_status_text(
                    row["HIGH_SEED_SERIES_W"],
                    row["HIGH_SEED_SERIES_L"],
                    row["HIGH_SEED_SERIES_REMAINING_G"],
                ),
            }

        slots = {}
        for slot_name, high_seed_rank, low_seed_rank in BRACKET_SLOT_ORDER:
            if not slot_name.startswith(f"{conference}_"):
                continue
            slots[slot_name] = series_by_matchup.get((high_seed_rank, low_seed_rank))

        return slots

    def _build_team_display(
        self,
        *,
        rank: int,
        team_name: str,
        team_id: int,
        standing: dict[str, Any] | None,
    ) -> dict[str, Any]:
        abbreviation = self._team_abbreviation(team_id)
        return {
            "rank": rank,
            "seed_label": f"#{rank}",
            "team": team_name,
            "team_id": team_id,
            "abbreviation": abbreviation,
            "display_name": f"#{rank} {abbreviation}",
            "record": standing,
        }

    def _build_recent_games(
        self,
        postseason_games: dict[str, list[dict[str, Any]]],
        max_games: int = 6,
    ) -> list[dict[str, Any]]:
        merged_games: dict[str, dict[str, Any]] = {}
        for stage, rows in postseason_games.items():
            for row in rows:
                game_id = row["GAME_ID"]
                game = merged_games.setdefault(
                    game_id,
                    {
                        "game_id": game_id,
                        "game_date": row["GAME_DATE"],
                        "stage": stage,
                        "matchup": row["MATCHUP"],
                        "teams": [],
                    },
                )
                game["teams"].append(row)

        recent_games = []
        for game in merged_games.values():
            if len(game["teams"]) != 2:
                continue

            away_team = next(
                (row for row in game["teams"] if "@ " in row["MATCHUP"]),
                game["teams"][0],
            )
            home_team = next(
                (row for row in game["teams"] if "vs. " in row["MATCHUP"]),
                game["teams"][-1],
            )

            recent_games.append(
                {
                    "game_id": game["game_id"],
                    "game_date": game["game_date"],
                    "stage": game["stage"],
                    "matchup": game["matchup"],
                    "away": {
                        "team": away_team["TEAM_ABBREVIATION"],
                        "points": away_team["PTS"],
                        "result": away_team["WL"],
                    },
                    "home": {
                        "team": home_team["TEAM_ABBREVIATION"],
                        "points": home_team["PTS"],
                        "result": home_team["WL"],
                    },
                }
            )

        recent_games.sort(key=lambda game: game["game_date"], reverse=True)
        return recent_games[:max_games]

    def _series_status_text(
        self, high_seed_wins: int, low_seed_wins: int, games_remaining: int
    ) -> str:
        if games_remaining == 0:
            if high_seed_wins > low_seed_wins:
                return "Series complete"
            if low_seed_wins > high_seed_wins:
                return "Upset complete"
        return f"Series {high_seed_wins}-{low_seed_wins}"

    def _team_abbreviation(self, team_id: int) -> str:
        team = TEAM_METADATA_BY_ID.get(team_id)
        return team["abbreviation"] if team else str(team_id)

    def _build_recent_games_start_date(self, game_date: str | None) -> str:
        if not game_date:
            return ""

        parsed_date = datetime.strptime(game_date, "%m/%d/%Y")
        return (parsed_date - timedelta(days=7)).strftime("%m/%d/%Y")
