"""
Scrape race results data from 1950-1950 from fastf1 api.
"""

import random
import time

import fastf1
import fastf1.plotting
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

BEGIN_SCRAPE_SEASON = 1950
END_SCRAPE_SEASON = 2024


races = {
    "season": [],
    "round_num": [],
    "event_name": [],
    "country": [],
    "location": [],
    "event_date": [],
}


def scrape_season(year):
    print(f"Scraping season: {year}")
    season = fastf1.get_event_schedule(year)

    # Use iterrows() to iterate over the DataFrame rows
    for _, gp in season.iterrows():
        try:
            races["season"].append(year)
        except Exception:
            races["season"].append(None)

        try:
            races["round_num"].append(gp["RoundNumber"])
        except Exception:
            races["round_num"].append(None)

        try:
            races["event_name"].append(gp["EventName"])
        except Exception:
            races["event_name"].append(None)

        try:
            races["country"].append(gp["Country"])
        except Exception:
            races["country"].append(None)

        try:
            races["location"].append(gp["Location"])
        except Exception:
            races["location"].append(None)

        try:
            # Clean the event date by removing time
            event_date = pd.to_datetime(gp["Session1Date"]).date()
            races["event_date"].append(event_date)
        except Exception:
            races["event_date"].append(None)

    # Add delay to avoid overwhelming the API
    time.sleep(random.uniform(3, 12))


def main():
    # Set the cache folder inside your project directory
    fastf1.Cache.enable_cache("./cache")

    for year in range(BEGIN_SCRAPE_SEASON, END_SCRAPE_SEASON + 1):
        scrape_season(year)

    non_zero_races = {key: value for key, value in races.items() if len(value) > 0}
    df = pd.DataFrame(non_zero_races)
    df.to_csv("data/raw/fastf1_races(1950-2024).csv", index=False)
    print("Races data saved to fastf1_races(1950-2024).csv")


if __name__ == "__main__":
    main()
