from __future__ import annotations

import json
from pathlib import Path

from requests import RequestException

from scripts.render_bracket_preview import sample_snapshot
from src.renderers.trmnl_renderer import TRMNLRenderer
from src.services.playoff_picture_service import PlayoffPictureService


def build_snapshot() -> dict:
    service = PlayoffPictureService()
    try:
        return service.get_playoff_snapshot()
    except RequestException:
        return sample_snapshot()


def write_payload(payload: dict[str, str]) -> Path:
    output = Path("docs/trmnl_payload.json")
    output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return output


def write_preview_html(payload: dict[str, str]) -> Path:
    html = f"""<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8" />
    <title>TRMNL Payload Preview</title>
    <link rel="stylesheet" href="https://trmnl.com/css/latest/plugins.css">
    <script src="https://trmnl.com/js/latest/plugins.js"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;350;375;400;450;600;700&display=swap" rel="stylesheet">
    {payload["shared"]}
  </head>
  <body class="environment trmnl">
    <div class="screen">
      {payload["markup"]}
    </div>
  </body>
</html>
"""
    output = Path("docs/trmnl_markup_preview.html")
    output.write_text(html, encoding="utf-8")
    return output


def main() -> None:
    snapshot = build_snapshot()
    payload = TRMNLRenderer().render_payload(snapshot)
    payload_path = write_payload(payload)
    preview_path = write_preview_html(payload)
    print(payload_path.resolve())
    print(preview_path.resolve())


if __name__ == "__main__":
    main()
