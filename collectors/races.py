"""
Scrape races data from 1950-2024 from FastF1 API and actively append to CSV file.
"""

import os
import random
import time

import fastf1
import pandas as pd

BEGIN_SCRAPE_SEASON = 1950
END_SCRAPE_SEASON = 2024

# Load the races dataset, skipping processed rows
RACES_PATH = "data/raw/races/races(1950-2024).csv"
if os.path.exists(RACES_PATH):
    EXISTING_RACES = pd.read_csv(RACES_PATH)
    processed = set(zip(EXISTING_RACES["season"], EXISTING_RACES["round_num"]))
else:
    EXISTING_RACES = pd.DataFrame()
    processed = set()

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


def fetch_season(year):
    """
    Fetch the race data for a given season.

    Args:
        year (int): The year to fetch the race data for.
    """
    print(f"Fetching season: {year}")
    season = fastf1.get_event_schedule(year)

    new_data_added = False

    # Iterate over the grand prixs in the season
    for _, gp in season.iterrows():
        race_id = (year, gp["RoundNumber"])
        if race_id in processed:
            continue  # Skip already processed races

        new_data_added = True  # If we process any race, mark new data added

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
                # Special cases (season and event_date)
                if race_key == "season":
                    value = year
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

    if not new_data_added:
        print(f"No new data found for {year}.")
    else:
        append_data_to_csv(races, "races(1950-2024)")

    time.sleep(random.uniform(3, 10))  # Time delay between requests


def clear_cache():
    """
    Clear the cache.
    """
    clear_cache = input("Do you want to clear the cache? (y/n): ").lower()
    if clear_cache == "y":
        fastf1.Cache.clear_cache("./cache")
        print("Cache cleared.")


def append_data_to_csv(dictionary, filename):
    """
    Append the race data to the CSV file.

    Args:
        dictionary (dict): The dictionary to append.
        filename (str): The filename to append the data to.
    """
    df = pd.DataFrame(dictionary)
    df.to_csv(
        f"data/raw/races/{filename}.csv",
        mode="a",
        header=not os.path.exists(f"data/raw/races/{filename}.csv"),
        index=False,
    )
    print(f"Data appended to {filename}.csv")


def main():
    clear_cache()
    fastf1.Cache.enable_cache("./cache")

    for year in range(BEGIN_SCRAPE_SEASON, END_SCRAPE_SEASON + 1):
        fetch_season(year)

    if not races["season"]:
        print("No new races to process. Exiting.")


if __name__ == "__main__":
    main()
