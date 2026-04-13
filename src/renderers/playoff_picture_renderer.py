from __future__ import annotations

from typing import Any


class PlayoffPictureRenderer:
    """Converts service output into a layout-ready structure for previews and templates."""

    def render(self, snapshot: dict[str, Any]) -> dict[str, Any]:
        bracket = snapshot["bracket"]
        recent_games = snapshot.get("recent_games", [])
        warnings = snapshot.get("warnings", [])

        return {
            "header": {
                "title": "NBA Playoffs",
                "subtitle": "",
            },
            "west": {
                "first_round": self._round_cards(bracket["west"]),
                "semifinals": self._placeholder_round("Conference Semifinals"),
                "conference_finals": self._placeholder_round("Conference Finals", count=1),
            },
            "finals": self._finals_card(),
            "east": {
                "conference_finals": self._placeholder_round("Conference Finals", count=1),
                "semifinals": self._placeholder_round("Conference Semifinals"),
                "first_round": self._round_cards(bracket["east"]),
            },
            "recent_games": self._recent_games_panel(recent_games, warnings, max_games=5),
        }

    def _round_cards(self, slots: list[dict[str, Any] | None]) -> list[dict[str, Any]]:
        cards = []
        for slot in slots:
            if not slot:
                cards.append(self._empty_matchup_card())
                continue

            cards.append(
                {
                    "top_team": self._team_line(
                        slot["high_seed"],
                        wins=slot["series_record"]["high_seed_wins"],
                        emphasized=True,
                    ),
                    "bottom_team": self._team_line(
                        slot["low_seed"],
                        wins=slot["series_record"]["low_seed_wins"],
                        emphasized=False,
                    ),
                }
            )

        return cards

    def _team_line(
        self, team: dict[str, Any], *, wins: int | str, emphasized: bool
    ) -> dict[str, Any]:
        return {
            "seed": team["seed_label"],
            "abbreviation": team["abbreviation"],
            "display_name": team["display_name"],
            "logo_url": self._logo_url(team.get("team_id")),
            "wins": wins,
            "emphasized": emphasized,
        }

    def _placeholder_round(self, title: str, count: int = 2) -> list[dict[str, Any]]:
        return [
            {
                "top_team": {
                    "seed": "--",
                    "abbreviation": "TBD",
                    "display_name": "TBD",
                    "logo_url": "",
                    "wins": "--",
                    "emphasized": True,
                },
                "bottom_team": {
                    "seed": "--",
                    "abbreviation": "TBD",
                    "display_name": "TBD",
                    "logo_url": "",
                    "wins": "--",
                    "emphasized": False,
                },
            }
            for _ in range(count)
        ]

    def _finals_card(self) -> dict[str, Any]:
        return {
            "title": "NBA Finals",
            "top_team": "TBD",
            "bottom_team": "TBD",
            "status_text": "Conference champions advance here",
        }

    def _recent_games_panel(
        self,
        recent_games: list[dict[str, Any]],
        warnings: list[str],
        *,
        max_games: int,
    ) -> dict[str, Any]:
        if recent_games:
            items = [
                {
                    "label": game["stage"].upper(),
                    "matchup": f"{game['away']['team']} {game['away']['points']} - {game['home']['points']} {game['home']['team']}",
                    "subtext": f"{game['game_date']} · {game['stage'].upper()}",
                }
                for game in recent_games[:max_games]
            ]
        else:
            items = [
                {
                    "label": "RECENT SCORES",
                    "matchup": "Recent playoff scores unavailable",
                    "subtext": warnings[0] if warnings else "No recent games found",
                }
            ]

        return {
            "title": "Recent Scores",
            "items": items,
        }

    def _empty_matchup_card(self) -> dict[str, Any]:
        return {
            "top_team": {
                "seed": "--",
                "abbreviation": "TBD",
                "display_name": "TBD",
                "logo_url": "",
                "wins": "--",
                "emphasized": True,
            },
            "bottom_team": {
                "seed": "--",
                "abbreviation": "TBD",
                "display_name": "TBD",
                "logo_url": "",
                "wins": "--",
                "emphasized": False,
            },
        }

    def _logo_url(self, team_id: Any) -> str:
        if not team_id:
            return ""
        return f"https://cdn.nba.com/logos/nba/{team_id}/primary/L/logo.svg"
