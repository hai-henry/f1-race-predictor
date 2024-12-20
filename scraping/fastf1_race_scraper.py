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

    for gp in season:
        try:
            races["season"].append(year)
        except Exception as e:
            races["season"].append(None)

        try:
            races["round_num"].append(gp["Round"])
        except Exception as e:
            races["round_num"].append(None)

        try:
            races["event_name"].append(gp["EventName"])
        except Exception as e:
            races["event_name"].append(None)

        try:
            races["country"].append(gp["Country"])
        except Exception as e:
            races["country"].append(None)

        try:
            races["location"].append(gp["Location"])
        except Exception as e:
            races["location"].append(None)

        try:
            races["event_date"].append(gp["EventDate"])
        except Exception as e:
            races["event_date"].append(None)

    time.sleep(random.uniform(3, 12))


def main():
    # Set the cache folder inside your project directory
    fastf1.Cache.enable_cache("./cache")

    for year in range(2024, END_SCRAPE_SEASON + 1):
        scrape_season(year)

    non_zero_races = {key: value for key, value in races.items() if len(value) > 0}
    df = pd.DataFrame(non_zero_races)
    df.to_csv("data/raw/fastf1_races(1950-2024).csv", index=False)
    print("Races data saved to fastf1_races(1950-2024).csv")


if __name__ == "__main__":
    main()
