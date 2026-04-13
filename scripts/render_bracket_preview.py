from __future__ import annotations

from pathlib import Path

from requests import RequestException

from src.renderers.playoff_picture_renderer import PlayoffPictureRenderer
from src.services.playoff_picture_service import PlayoffPictureService
from src.templates.playoff_preview_template import HTML_TEMPLATE


def render_matchup_card(card: dict[str, object]) -> str:
    top_team = card["top_team"]
    bottom_team = card["bottom_team"]
    top_logo = (
        f'<img class="logo" src="{top_team["logo_url"]}" alt="{top_team["abbreviation"]} logo" />'
        if top_team["logo_url"]
        else '<span class="logo-placeholder"></span>'
    )
    bottom_logo = (
        f'<img class="logo" src="{bottom_team["logo_url"]}" alt="{bottom_team["abbreviation"]} logo" />'
        if bottom_team["logo_url"]
        else '<span class="logo-placeholder"></span>'
    )
    return f"""
    <section class="card">
      <div class="team {'emphasized' if top_team['emphasized'] else ''}">
        <span class="seed">{top_team['seed']}</span>
        {top_logo}
        <span class="abbr">{top_team['abbreviation']}</span>
        <span class="wins">{top_team['wins']}</span>
      </div>
      <div class="team {'emphasized' if bottom_team['emphasized'] else ''}">
        <span class="seed">{bottom_team['seed']}</span>
        {bottom_logo}
        <span class="abbr">{bottom_team['abbreviation']}</span>
        <span class="wins">{bottom_team['wins']}</span>
      </div>
    </section>
    """


def render_score_item(item: dict[str, str]) -> str:
    return f"""
    <div class="score-item">
      <div class="score-label">{item['label']}</div>
      <div class="score-matchup">{item['matchup']}</div>
      <div class="score-subtext">{item['subtext']}</div>
    </div>
    """


def build_html(view_model: dict[str, object]) -> str:
    return HTML_TEMPLATE.format(
        title=view_model["header"]["title"],
        subtitle=view_model["header"]["subtitle"],
        west_first_round="".join(
            render_matchup_card(card) for card in view_model["west"]["first_round"]
        ),
        west_semifinals="".join(
            render_matchup_card(card) for card in view_model["west"]["semifinals"]
        ),
        west_conference_finals="".join(
            render_matchup_card(card)
            for card in view_model["west"]["conference_finals"]
        ),
        east_conference_finals="".join(
            render_matchup_card(card)
            for card in view_model["east"]["conference_finals"]
        ),
        east_semifinals="".join(
            render_matchup_card(card) for card in view_model["east"]["semifinals"]
        ),
        east_first_round="".join(
            render_matchup_card(card) for card in view_model["east"]["first_round"]
        ),
        finals_title=view_model["finals"]["title"],
        finals_top_team=view_model["finals"]["top_team"],
        finals_bottom_team=view_model["finals"]["bottom_team"],
        finals_status=view_model["finals"]["status_text"],
        scores_title=view_model["recent_games"]["title"],
        recent_scores="".join(
            render_score_item(item) for item in view_model["recent_games"]["items"]
        ),
    )


def sample_snapshot() -> dict[str, object]:
    def team(seed: int, abbreviation: str, wins: int, losses: int) -> dict[str, object]:
        return {
            "seed_label": f"#{seed}",
            "abbreviation": abbreviation,
            "display_name": f"#{seed} {abbreviation}",
            "record": {"wins": wins, "losses": losses},
        }

    def slot(key: str, top_seed: int, top_abbr: str, bottom_seed: int, bottom_abbr: str, series: str) -> dict[str, object]:
        top_wins, bottom_wins = series.split("-")
        return {
            "slot_key": key,
            "status_text": f"Series {series}",
            "series_record": {
                "display": series,
                "high_seed_wins": int(top_wins),
                "low_seed_wins": int(bottom_wins),
            },
            "high_seed": team(top_seed, top_abbr, 58 - top_seed, 24 + top_seed),
            "low_seed": team(bottom_seed, bottom_abbr, 48 - bottom_seed, 34 + bottom_seed),
        }

    return {
        "bracket": {
            "east": [
                slot("east_1_8", 1, "BOS", 8, "MIA", "3-1"),
                slot("east_4_5", 4, "IND", 5, "MIL", "2-2"),
                slot("east_2_7", 2, "CLE", 7, "ORL", "3-0"),
                slot("east_3_6", 3, "NYK", 6, "DET", "2-1"),
            ],
            "west": [
                slot("west_1_8", 1, "OKC", 8, "SAC", "3-0"),
                slot("west_4_5", 4, "DEN", 5, "LAL", "2-2"),
                slot("west_2_7", 2, "MIN", 7, "PHX", "2-1"),
                slot("west_3_6", 3, "DAL", 6, "GS", "3-1"),
            ],
        },
        "recent_games": [
            {"stage": "playoffs", "away": {"team": "MIL", "points": 101}, "home": {"team": "IND", "points": 109}, "game_date": "2026-04-13"},
            {"stage": "playoffs", "away": {"team": "LAL", "points": 112}, "home": {"team": "DEN", "points": 114}, "game_date": "2026-04-13"},
            {"stage": "playin", "away": {"team": "MIA", "points": 99}, "home": {"team": "CHI", "points": 96}, "game_date": "2026-04-12"},
        ],
        "warnings": ["Using sample preview data because live NBA requests are unavailable."],
    }


def main() -> None:
    service = PlayoffPictureService()
    renderer = PlayoffPictureRenderer()

    try:
        snapshot = service.get_playoff_snapshot()
    except RequestException:
        snapshot = sample_snapshot()

    view_model = renderer.render(snapshot)
    html = build_html(view_model)

    output_path = Path("docs/playoff_preview.html")
    output_path.write_text(html, encoding="utf-8")
    print(output_path.resolve())


if __name__ == "__main__":
    main()
