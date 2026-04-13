# NBA Playoffs TRMNL

A public TRMNL plugin project for displaying the NBA playoff bracket with daily updates on games, series status, and other important postseason information.

## Project Overview

This project is being built as a public plugin for TRMNL to make the NBA playoff picture easy to follow at a glance.

The goal is to present a clean and useful playoff view that updates regularly and highlights the most important information during the postseason.

## Planned V1 Display

The first version of the plugin is intended to show:

- NBA logo on the left
- Full playoff bracket in the center
- Recent playoff and play-in game scores on the right

For the current build, play-in games are treated as part of the overall bracket experience rather than as a separate panel.

The display should update daily to reflect current playoff results, game status, and other relevant information.

## Data Source

This project uses Python and the `nba_api` package to retrieve NBA data.

## Current Status

The repository is currently in the project setup phase.

At this stage:

- the repository has been created
- the Python virtual environment has been set up
- `nba_api` has been installed
- the initial folder structure has been created

Application logic, rendering, and TRMNL integration are still to be built.

## Disclaimer

This project is an unofficial fan-made TRMNL plugin and is not affiliated with, endorsed by, or sponsored by the NBA or its teams.

NBA names, logos, team marks, statistics, schedules, scores, and related intellectual property are owned by their respective rights holders.

This project is intended as a personal, educational, and non-commercial project. Data used by this plugin is sourced from NBA.com through `nba_api`, with attribution to NBA.com where applicable.

## Notes

The hosting and update strategy for TRMNL is still being evaluated. One possible approach is to use GitHub Actions to run scheduled data updates and send processed data to a webhook or hosted endpoint for the plugin.

To reduce unnecessary load on upstream data sources, the project should use caching and avoid excessively frequent requests wherever possible.
