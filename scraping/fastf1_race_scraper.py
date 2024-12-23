"""
Scrape race results data from 1950-1950 from FastF1 API.
"""

import random
import time

import fastf1
import pandas as pd

BEGIN_SCRAPE_SEASON = 1950
END_SCRAPE_SEASON = 2024


races = {
    "season": [],
    "round_num": [],
    "event_name": [],
    "country": [],
    "location": [],
    "event_date": [],
    "session_one": [],
    "session_two": [],
    "session_three": [],
    "session_four": [],
    "session_five": [],
}


def scrape_season(year):
    print(f"Scraping season: {year}")
    season = fastf1.get_event_schedule(year)

    for _, gp in season.iterrows():
        for race_key, column_name in {
            "season": None,
            "round_num": "RoundNumber",
            "event_name": "EventName",
            "country": "Country",
            "location": "Location",
            "event_date": "Session1Date",
            "session_one": "Session1",
            "session_two": "Session2",
            "session_three": "Session3",
            "session_four": "Session4",
            "session_five": "Session5",
        }.items():
            try:
                if race_key == "season":
                    value = year  # Special case for "season"
                elif race_key == "event_date":
                    value = (
                        pd.to_datetime(gp[column_name]).date()
                        if pd.notnull(gp[column_name])
                        else None
                    )
                else:
                    value = gp[column_name]
                races[race_key].append(value)
            except Exception:
                races[race_key].append(None)


def clear_cache():
    clear_cache = input("Do you want to clear the cache? (y/n): ").lower()
    if clear_cache == "y":
        fastf1.Cache.clear_cache("./cache")
        print("Cache cleared.")


def save_data(dictionary):
    non_zero = {key: value for key, value in dictionary.items() if len(value) > 0}
    df = pd.DataFrame(non_zero)
    df.to_csv("data/raw/races/fastf1_races_sessions(1950-2024).csv", index=False)
    print("Races data saved to fastf1_races_sessions(1950-2024).csv")


def main():
    clear_cache()

    # Set the cache folder inside your project directory
    fastf1.Cache.enable_cache("./cache")

    for year in range(BEGIN_SCRAPE_SEASON, END_SCRAPE_SEASON + 1):
        scrape_season(year)

    save_data(races)


if __name__ == "__main__":
    main()
