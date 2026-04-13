from __future__ import annotations

from typing import Any

from nba_api.stats.endpoints import leaguegamefinder, playoffpicture
from nba_api.stats.library.http import STATS_HEADERS
from nba_api.stats.library.parameters import SeasonType, SeasonTypePlayoffs
from requests import RequestException


DEFAULT_HEADERS = {
    **STATS_HEADERS,
    "User-Agent": "NBA-Playoffs-TRMNL/0.1 (+https://github.com/QABoahene/nba-playoff-picture-trmnl)",
    "Referer": "https://stats.nba.com/",
}


class NBAClient:
    """Thin wrapper around nba_api endpoints used by the plugin."""

    def __init__(self, *, timeout: int = 30, headers: dict[str, str] | None = None):
        self.timeout = timeout
        self.headers = headers or DEFAULT_HEADERS

    def get_playoff_picture(self, *, season_id: str | None = None) -> dict[str, Any]:
        endpoint = playoffpicture.PlayoffPicture(
            season_id=season_id or playoffpicture.SeasonID.default,
            headers=self.headers,
            timeout=self.timeout,
        )
        return endpoint.get_normalized_dict()

    def get_league_games(
        self,
        *,
        season_type: str,
        season: str | None = None,
        date_from: str = "",
        date_to: str = "",
    ) -> list[dict[str, Any]]:
        endpoint = leaguegamefinder.LeagueGameFinder(
            player_or_team_abbreviation="T",
            season_nullable=season or leaguegamefinder.SeasonNullable.default,
            season_type_nullable=season_type,
            date_from_nullable=date_from,
            date_to_nullable=date_to,
            headers=self.headers,
            timeout=self.timeout,
        )
        return endpoint.get_normalized_dict().get("LeagueGameFinderResults", [])

    def get_recent_postseason_games(
        self,
        *,
        season: str | None = None,
        date_from: str = "",
        date_to: str = "",
    ) -> tuple[dict[str, list[dict[str, Any]]], list[str]]:
        games = {"playoffs": [], "playin": []}
        warnings: list[str] = []

        try:
            games["playoffs"] = self.get_league_games(
                season_type=SeasonTypePlayoffs.playoffs,
                season=season,
                date_from=date_from,
                date_to=date_to,
            )
        except RequestException as exc:
            warnings.append(f"Playoff games request failed: {exc}")

        try:
            games["playin"] = self.get_league_games(
                season_type=SeasonType.playin,
                season=season,
                date_from=date_from,
                date_to=date_to,
            )
        except RequestException as exc:
            warnings.append(f"Play-in games request failed: {exc}")

        return games, warnings
