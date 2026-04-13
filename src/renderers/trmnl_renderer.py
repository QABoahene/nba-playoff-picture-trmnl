from __future__ import annotations

from typing import Any


class TRMNLRenderer:
    """Render the project snapshot into TRMNL marketplace response payloads."""

    def render_payload(self, snapshot: dict[str, Any]) -> dict[str, str]:
        return {
            "markup": self._render_full_view(snapshot),
            "markup_half_horizontal": self._render_half_horizontal_view(snapshot),
            "markup_half_vertical": self._render_half_vertical_view(snapshot),
            "markup_quadrant": self._render_quadrant_view(snapshot),
            "shared": self._render_shared_markup(),
        }

    def _render_full_view(self, snapshot: dict[str, Any]) -> str:
        west_cards = "".join(
            self._render_matchup_card(card)
            for card in snapshot["bracket"]["west"]
            if card is not None
        )
        east_cards = "".join(
            self._render_matchup_card(card)
            for card in snapshot["bracket"]["east"]
            if card is not None
        )
        scores = "".join(
            self._render_score_row(game) for game in snapshot.get("recent_games", [])[:5]
        ) or '<div class="np-scores-empty">Recent playoff scores unavailable</div>'

        return f"""
<div class="view view--full">
  <div class="layout">
    <div class="np-board">
      <div class="np-bracket">
        <section class="np-conference">
          <span class="label label--small label--gray">West</span>
          <div class="np-card-stack">
            {west_cards}
          </div>
        </section>
        <section class="np-finals">
          <span class="label label--small label--underline">NBA Finals</span>
          <div class="np-finals-card">
            <div class="np-finals-team">TBD</div>
            <div class="np-finals-team">TBD</div>
          </div>
        </section>
        <section class="np-conference">
          <span class="label label--small label--gray">East</span>
          <div class="np-card-stack">
            {east_cards}
          </div>
        </section>
      </div>
      <section class="np-scores">
        <span class="label label--small label--underline">Recent Scores</span>
        <div class="np-scores-grid">
          {scores}
        </div>
      </section>
    </div>
  </div>
  <div class="title_bar">
    <span class="title">NBA Playoffs</span>
  </div>
</div>
""".strip()

    def _render_half_horizontal_view(self, snapshot: dict[str, Any]) -> str:
        top_west = next((card for card in snapshot["bracket"]["west"] if card), None)
        top_east = next((card for card in snapshot["bracket"]["east"] if card), None)
        return f"""
<div class="view view--half_horizontal">
  <div class="layout">
    <div class="columns">
      <div class="column">
        <span class="label label--small label--gray">West Lead Series</span>
        {self._render_compact_series(top_west)}
      </div>
      <div class="column">
        <span class="label label--small label--gray">East Lead Series</span>
        {self._render_compact_series(top_east)}
      </div>
    </div>
  </div>
  <div class="title_bar">
    <span class="title">NBA Playoffs</span>
  </div>
</div>
""".strip()

    def _render_half_vertical_view(self, snapshot: dict[str, Any]) -> str:
        score = snapshot.get("recent_games", [])
        content = (
            self._render_score_row(score[0], compact=True)
            if score
            else '<div class="np-scores-empty">Scores unavailable</div>'
        )
        return f"""
<div class="view view--half_vertical">
  <div class="layout">
    <div class="np-mini-panel">
      <span class="label label--small label--underline">Recent Score</span>
      {content}
    </div>
  </div>
  <div class="title_bar">
    <span class="title">NBA Playoffs</span>
  </div>
</div>
""".strip()

    def _render_quadrant_view(self, snapshot: dict[str, Any]) -> str:
        top_series = next(
            (card for side in ("west", "east") for card in snapshot["bracket"][side] if card),
            None,
        )
        return f"""
<div class="view view--quadrant">
  <div class="layout">
    <div class="np-mini-panel">
      <span class="label label--small label--underline">Featured Series</span>
      {self._render_compact_series(top_series)}
    </div>
  </div>
  <div class="title_bar">
    <span class="title">NBA Playoffs</span>
  </div>
</div>
""".strip()

    def _render_matchup_card(self, card: dict[str, Any]) -> str:
        return f"""
<article class="np-matchup-card">
  {self._render_team_line(card["high_seed"], card["series_record"]["high_seed_wins"])}
  {self._render_team_line(card["low_seed"], card["series_record"]["low_seed_wins"])}
</article>
""".strip()

    def _render_team_line(self, team: dict[str, Any], wins: int) -> str:
        logo = self._logo_image(team.get("team_id"), team["abbreviation"])
        return f"""
<div class="np-team-line">
  <span class="np-seed">{team["seed_label"]}</span>
  {logo}
  <span class="np-team">{team["abbreviation"]}</span>
  <span class="np-wins">{wins}</span>
</div>
""".strip()

    def _render_compact_series(self, card: dict[str, Any] | None) -> str:
        if not card:
            return '<div class="np-scores-empty">Series unavailable</div>'
        return f"""
<article class="np-matchup-card np-matchup-card--compact">
  {self._render_team_line(card["high_seed"], card["series_record"]["high_seed_wins"])}
  {self._render_team_line(card["low_seed"], card["series_record"]["low_seed_wins"])}
</article>
""".strip()

    def _render_score_row(self, game: dict[str, Any], compact: bool = False) -> str:
        cls = "np-score-row np-score-row--compact" if compact else "np-score-row"
        away = game["away"]
        home = game["home"]
        return f"""
<div class="{cls}">
  <span class="label label--small label--gray">{game["game_date"]}</span>
  <div class="np-score-matchup">{away["team"]} {away["points"]} · {home["team"]} {home["points"]}</div>
  <span class="label label--small">{game["stage"].upper()}</span>
</div>
""".strip()

    def _logo_image(self, team_id: int | None, abbreviation: str) -> str:
        if not team_id:
            return '<span class="np-logo np-logo--placeholder"></span>'
        return (
            f'<img class="image np-logo" src="https://cdn.nba.com/logos/nba/{team_id}/primary/L/logo.svg" '
            f'alt="{abbreviation} logo" />'
        )

    def _render_shared_markup(self) -> str:
        return """
<style>
  .np-board { display:flex; flex-direction:column; height:100%; gap:12px; }
  .np-bracket { display:grid; grid-template-columns: 1fr 120px 1fr; gap:16px; align-items:start; }
  .np-conference { display:flex; flex-direction:column; gap:8px; }
  .np-card-stack { display:flex; flex-direction:column; gap:8px; }
  .np-matchup-card { border:1px solid var(--stroke); border-radius:12px; padding:8px 10px; background:var(--color-bg); }
  .np-matchup-card--compact { padding:6px 8px; }
  .np-team-line { display:grid; grid-template-columns: 28px 18px 1fr 14px; gap:8px; align-items:center; padding:6px 0; }
  .np-team-line + .np-team-line { border-top:1px solid var(--stroke); }
  .np-seed, .np-wins { font-size:12px; font-weight:700; }
  .np-team { font-size:18px; font-weight:800; line-height:1; }
  .np-logo { width:16px; height:16px; object-fit:contain; }
  .np-logo--placeholder { display:inline-block; border-radius:999px; background:var(--stroke); }
  .np-finals { display:flex; flex-direction:column; gap:8px; justify-self:center; align-self:center; width:100%; }
  .np-finals-card { border:1px solid var(--stroke); border-radius:14px; padding:12px 10px; text-align:center; }
  .np-finals-team { font-size:18px; font-weight:800; padding:8px 0; }
  .np-scores { display:flex; flex-direction:column; gap:8px; border-top:1px solid var(--stroke); padding-top:10px; }
  .np-scores-grid { display:grid; grid-template-columns: repeat(5, 1fr); gap:8px; }
  .np-score-row { border:1px solid var(--stroke); border-radius:10px; padding:8px; min-height:58px; display:flex; flex-direction:column; justify-content:space-between; }
  .np-score-row--compact { min-height:auto; }
  .np-score-matchup { font-size:13px; font-weight:700; line-height:1.2; }
  .np-scores-empty { font-size:13px; color:var(--color-text-subtle); }
  .np-mini-panel { display:flex; flex-direction:column; gap:8px; width:100%; }
</style>
""".strip()
