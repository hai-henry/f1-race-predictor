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


def fetch_season(year):
    """
    Fetch the race races for a given season.

    Args:
        year (int): The year to fetch the race data for.
    """
    print(f"Scraping season: {year}")
    season = fastf1.get_event_schedule(year)

    # Iterate over the grand prixs in the season
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
                races[race_key].append(value)  # Append the value to the dictionary
            except Exception:
                races[race_key].append(None)  # Append None if there's an error

    time.sleep(random.uniform(3, 10))  # Time delay between requests


def clear_cache():
    """
    Clear the cache.
    """
    clear_cache = input("Do you want to clear the cache? (y/n): ").lower()
    if clear_cache == "y":
        fastf1.Cache.clear_cache("./cache")
        print("Cache cleared.")


def save_data(dictionary, filename):
    """
    Save the race data to a CSV file.

    Args:
        dictionary (dict): The dictionary to save.
        filename (str): The filename to save the data to.
    """
    df = pd.DataFrame(dictionary)
    df.to_csv(f"data/raw/races/{filename}.csv", index=False)
    print(f"Races data saved to {filename}.csv")


def main():
    clear_cache()

    # Set the cache folder inside your project directory
    fastf1.Cache.enable_cache("./cache")

    for year in range(BEGIN_SCRAPE_SEASON, END_SCRAPE_SEASON + 1):
        fetch_season(year)

    save_data(races, "fastf1_races(1950-2024)")


if __name__ == "__main__":
    main()
