from __future__ import annotations


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{title}</title>
  <style>
    :root {{
      --bg: #f1ede4;
      --panel: #f8f5ee;
      --ink: #151515;
      --muted: #7b756d;
      --west: #cc4b4c;
      --east: #2d5b9f;
      --accent: #c5a254;
      --line: #d8d1c4;
      --line-strong: #c9c0b0;
      --card: #ffffff;
    }}

    * {{
      box-sizing: border-box;
    }}

    body {{
      margin: 0;
      font-family: "Avenir Next", "Helvetica Neue", sans-serif;
      background:
        radial-gradient(circle at top left, rgba(204, 75, 76, 0.08), transparent 26%),
        radial-gradient(circle at top right, rgba(45, 91, 159, 0.08), transparent 28%),
        var(--bg);
      color: var(--ink);
    }}

    .page {{
      width: 800px;
      height: 480px;
      margin: 0 auto;
      padding: 8px 10px 10px;
      overflow: hidden;
      background:
        linear-gradient(180deg, rgba(255,255,255,0.28), rgba(255,255,255,0.02)),
        var(--panel);
    }}

    .header {{
      margin-bottom: 8px;
      padding-bottom: 6px;
      border-bottom: 1px solid rgba(21, 21, 21, 0.08);
    }}

    .title {{
      font-size: 17px;
      font-weight: 900;
      letter-spacing: 0.02em;
      text-transform: uppercase;
      line-height: 1;
    }}

    .subtitle {{
      display: none;
    }}

    .layout {{
      display: grid;
      grid-template-rows: 1fr auto;
      gap: 8px;
      height: calc(100% - 30px);
    }}

    .bracket-layout {{
      display: grid;
      grid-template-columns: 124px 88px 72px 86px 72px 88px 124px;
      gap: 6px;
      align-items: start;
      min-height: 0;
      position: relative;
    }}

    .round-column {{
      display: grid;
      gap: 6px;
      align-content: start;
      min-height: 0;
      z-index: 1;
    }}

    .round-title {{
      font-size: 8px;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      color: var(--muted);
      margin-bottom: 0;
    }}

    .card {{
      background: var(--card);
      border: 1px solid var(--line);
      border-radius: 10px;
      padding: 6px 7px;
      box-shadow: 0 1px 0 rgba(21, 21, 21, 0.02);
      position: relative;
    }}

    .card-head {{
      display: flex;
      justify-content: flex-start;
      gap: 6px;
      margin-bottom: 4px;
      font-size: 7px;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      color: var(--muted);
      line-height: 1.15;
    }}

    .first-round {{
      margin-top: 40px;
    }}

    .semifinals {{
      margin-top: 126px;
    }}

    .conference-finals {{
      margin-top: 168px;
    }}

    .bracket-svg {{
      position: absolute;
      inset: 0 0 82px 0;
      width: 100%;
      height: 100%;
      pointer-events: none;
      z-index: 0;
      overflow: visible;
    }}

    .bracket-line {{
      fill: none;
      stroke: var(--line-strong);
      stroke-width: 1.25;
      stroke-linecap: square;
      stroke-linejoin: miter;
    }}

    .connector {{
      position: absolute;
    }}

    .team {{
      display: grid;
      grid-template-columns: 14px 16px 1fr 10px;
      gap: 6px;
      align-items: center;
      padding: 4px 0;
      border-top: 1px solid rgba(215, 209, 200, 0.75);
    }}

    .team:first-of-type {{
      border-top: 0;
    }}

    .team.emphasized {{
      color: var(--ink);
      font-weight: 800;
      background: linear-gradient(90deg, rgba(21, 21, 21, 0.03), transparent 72%);
      border-radius: 6px;
    }}

    .team:not(.emphasized) {{
      color: #706b64;
    }}

    .seed {{
      font-size: 9px;
      font-weight: 700;
      letter-spacing: 0.04em;
      width: 16px;
    }}

    .logo {{
      width: 16px;
      height: 16px;
      flex: 0 0 16px;
      object-fit: contain;
    }}

    .logo-placeholder {{
      width: 16px;
      height: 16px;
      flex: 0 0 16px;
      border-radius: 999px;
      background: rgba(127, 122, 115, 0.18);
    }}

    .abbr {{
      font-size: 12px;
      font-weight: 800;
      line-height: 1;
      letter-spacing: 0.03em;
    }}

    .wins {{
      justify-self: end;
      font-size: 12px;
      font-weight: 900;
      line-height: 1;
    }}

    .finals {{
      align-self: start;
      text-align: center;
      padding: 12px 8px;
      border-radius: 14px;
      background:
        linear-gradient(180deg, rgba(197, 162, 84, 0.14), transparent 42%),
        var(--card);
      border: 1px solid rgba(197, 162, 84, 0.35);
      margin-top: 218px;
      z-index: 1;
    }}

    .finals h2 {{
      margin: 0 0 6px;
      font-size: 11px;
      text-transform: uppercase;
      letter-spacing: 0.08em;
    }}

    .finals .team-name {{
      font-size: 10px;
      font-weight: 800;
      padding: 5px 0;
    }}

    .scores {{
      background: rgba(255, 255, 255, 0.68);
      color: var(--ink);
      border-radius: 14px;
      padding: 8px 10px;
      height: 72px;
      overflow: hidden;
      border: 1px solid var(--line);
      display: grid;
      grid-template-columns: 110px 1fr;
      gap: 10px;
      align-items: start;
    }}

    .scores h3 {{
      margin: 0;
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: 0.08em;
    }}

    .scores-list {{
      display: grid;
      grid-template-columns: repeat(5, minmax(0, 1fr));
      gap: 10px;
      min-width: 0;
    }}

    .score-item {{
      padding: 0;
      border-top: 0;
      min-width: 0;
    }}

    .score-item:first-of-type {{
      border-top: 0;
      padding-top: 0;
    }}

    .score-label {{
      color: #caa64b;
      font-size: 7px;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      margin-bottom: 2px;
    }}

    .score-matchup {{
      font-size: 10px;
      font-weight: 700;
      line-height: 1.15;
    }}

    .score-subtext {{
      margin-top: 2px;
      color: var(--muted);
      font-size: 8px;
      line-height: 1.2;
    }}
  </style>
</head>
<body>
  <div class="page">
    <div class="header">
      <div>
        <div class="title">{title}</div>
        <div class="subtitle">{subtitle}</div>
      </div>
    </div>
    <div class="layout">
      <div class="bracket-layout">
        <svg class="bracket-svg" viewBox="0 0 672 420" preserveAspectRatio="none" aria-hidden="true">
          <path class="bracket-line" d="M124 62 H150 V100 H182" />
          <path class="bracket-line" d="M124 188 H150 V150 H182" />
          <path class="bracket-line" d="M124 262 H150 V300 H182" />
          <path class="bracket-line" d="M124 388 H150 V350 H182" />

          <path class="bracket-line" d="M270 124 H296 V186 H318" />
          <path class="bracket-line" d="M270 326 H296 V264 H318" />

          <path class="bracket-line" d="M390 186 H414 V220 H434" />

          <path class="bracket-line" d="M548 62 H522 V100 H490" />
          <path class="bracket-line" d="M548 188 H522 V150 H490" />
          <path class="bracket-line" d="M548 262 H522 V300 H490" />
          <path class="bracket-line" d="M548 388 H522 V350 H490" />

          <path class="bracket-line" d="M402 220 H434 V186 H454" />
          <path class="bracket-line" d="M402 220 H434 V264 H454" />

          <path class="bracket-line" d="M402 220 H390" />
        </svg>
        <div class="round-column first-round">
          <div class="round-title">First Round</div>
          {west_first_round}
        </div>
        <div class="round-column semifinals">
          <div class="round-title">Semifinals</div>
          {west_semifinals}
        </div>
        <div class="round-column conference-finals">
          <div class="round-title">Conference Finals</div>
          {west_conference_finals}
        </div>
        <div class="card finals">
          <h2>{finals_title}</h2>
          <div class="team-name">{finals_top_team}</div>
          <div class="team-name">{finals_bottom_team}</div>
          <div class="subtitle">{finals_status}</div>
        </div>
        <div class="round-column conference-finals">
          <div class="round-title">Conference Finals</div>
          {east_conference_finals}
        </div>
        <div class="round-column semifinals">
          <div class="round-title">Semifinals</div>
          {east_semifinals}
        </div>
        <div class="round-column first-round">
          <div class="round-title">First Round</div>
          {east_first_round}
        </div>
      </div>
      <aside class="scores">
        <h3>{scores_title}</h3>
        <div class="scores-list">
          {recent_scores}
        </div>
      </aside>
    </div>
  </div>
</body>
</html>
"""
