 from __future__ import annotations

from pprint import pprint

from src.services.playoff_picture_service import PlayoffPictureService


def main() -> None:
    service = PlayoffPictureService()
    snapshot = service.get_playoff_snapshot()

    east_series = snapshot["bracket"]["east"]
    west_series = snapshot["bracket"]["west"]
    recent_games = snapshot["recent_games"]
    warnings = snapshot.get("warnings", [])

    print("East series:", len(east_series))
    print("West series:", len(west_series))
    print("Recent playoff/play-in games:", len(recent_games))

    if warnings:
        print("\nWarnings:")
        for warning in warnings:
            print("-", warning)

    if east_series:
        print("\nSample East slot:")
        pprint(east_series[0])

    if recent_games:
        print("\nSample recent game:")
        pprint(recent_games[0])


if __name__ == "__main__":
    main()
