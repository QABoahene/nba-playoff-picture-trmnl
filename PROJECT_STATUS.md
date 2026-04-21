# Project Status

## What This Project Is

`NBA Playoffs TRMNL` is a public TRMNL plugin project intended to show:

- NBA playoff bracket
- playoff/play-in context
- recent postseason scores

The project uses Python and `nba_api`.

## Repo / Environment Setup Completed

- local git repo initialized and connected to GitHub
- virtual environment created at `.venv`
- `nba_api` installed via `requirements.txt`
- base project folder structure created
- `README.md` updated with project overview and disclaimer language

## Current Folder / Code Areas

- `src/clients/`
  - `nba_client.py`
  - wraps `nba_api` calls
- `src/services/`
  - `playoff_picture_service.py`
  - normalizes API output into bracket/scores structures
- `src/renderers/`
  - `playoff_picture_renderer.py`
  - HTML preview-oriented renderer
  - `trmnl_renderer.py`
  - real TRMNL payload renderer
- `src/templates/`
  - `playoff_preview_template.py`
  - local mock preview template
- `scripts/`
  - `smoke_test_playoff_data.py`
  - `render_bracket_preview.py`
  - `build_trmnl_payload.py`
- `docs/`
  - generated preview and payload artifacts

## What Was Built

### 1. Data Layer

Created `src/clients/nba_client.py` to:

- call `PlayoffPicture`
- call postseason game endpoints
- use a custom user agent / headers

Created `src/services/playoff_picture_service.py` to:

- build fixed bracket slot structures
- normalize east/west matchups
- attach display-friendly fields like seed labels and abbreviations
- collect recent games when available
- degrade gracefully when score endpoints fail

## Important Data Findings

- `PlayoffPicture` returned usable structure for bracket-style data
- recent scores endpoints have been unreliable / timing out
- bracket data itself may not be trustworthy for real current-season production use without verification
  - example issue previously observed: implausible team placements

This means the rendering pipeline is usable, but the long-term production data source still needs validation or replacement.

### 2. Local Mock Preview

Built a local HTML preview workflow to test bracket layout ideas:

- `src/renderers/playoff_picture_renderer.py`
- `src/templates/playoff_preview_template.py`
- `scripts/render_bracket_preview.py`

This preview helped define:

- bracket spacing
- card density
- information hierarchy
- how much content might fit on a TRMNL-style screen

Important:

- this mock preview is only a design aid
- it is **not** the final TRMNL implementation path

### 3. Real TRMNL Rendering Path

Started the real TRMNL-facing implementation using TRMNL docs rather than the mock HTML.

Created:

- `src/renderers/trmnl_renderer.py`
- `scripts/build_trmnl_payload.py`

This currently generates:

- `docs/trmnl_payload.json`
- `docs/trmnl_markup_preview.html`

The TRMNL renderer outputs:

- `markup`
- `markup_half_horizontal`
- `markup_half_vertical`
- `markup_quadrant`
- `shared`

The implementation was based on TRMNL docs and framework expectations.

## Files Most Relevant Next Time

- `src/clients/nba_client.py`
- `src/services/playoff_picture_service.py`
- `src/renderers/trmnl_renderer.py`
- `scripts/build_trmnl_payload.py`
- `docs/trmnl_payload.json`

## Current State

What is working:

- repo and environment setup
- bracket-oriented data normalization
- fallback sample-based previews
- TRMNL payload generation scaffold

What is not fully solved:

- reliable recent playoff/play-in scores source
- confidence in the playoff bracket source for real production use
- final hosted endpoint / deployment flow for TRMNL
- final production TRMNL layout tuning

## Recommended Next Step

The next highest-value work is:

1. validate or replace the bracket data source
2. validate a better recent-scores source
3. inspect `docs/trmnl_markup_preview.html`
4. wire `scripts/build_trmnl_payload.py` into the eventual hosted/plugin response flow

## Useful Commands

Activate env:

```bash
source .venv/bin/activate
```

Smoke test data:

```bash
PYTHONPATH=. python scripts/smoke_test_playoff_data.py
```

Render old HTML mock preview:

```bash
PYTHONPATH=. python scripts/render_bracket_preview.py
```

Build TRMNL payload + preview:

```bash
PYTHONPATH=. python scripts/build_trmnl_payload.py
```

## Short Resume Note

If you come back later, start by opening:

- `PROJECT_STATUS.md`
- `src/renderers/trmnl_renderer.py`
- `src/services/playoff_picture_service.py`

Then decide whether to fix the data source first or move directly into the hosted TRMNL plugin response flow.
