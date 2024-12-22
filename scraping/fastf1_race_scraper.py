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
# TODO: Clean up code


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

        try:
            races["session_one"].append(gp["Session1"])
        except Exception:
            races["session_one"].append(None)

        try:
            races["session_two"].append(gp["Session2"])
        except Exception:
            races["session_two"].append(None)

        try:
            races["session_three"].append(gp["Session3"])
        except Exception:
            races["session_three"].append(None)

        try:
            races["session_four"].append(gp["Session4"])
        except Exception:
            races["session_four"].append(None)

        try:
            races["session_five"].append(gp["Session5"])
        except Exception:
            races["session_five"].append(None)

    time.sleep(random.uniform(3, 12))  # Add delay to avoid overwhelming the API


def main():
    # Set the cache folder inside your project directory
    fastf1.Cache.enable_cache("./cache")

    for year in range(BEGIN_SCRAPE_SEASON, END_SCRAPE_SEASON + 1):
        scrape_season(year)

    non_zero_races = {key: value for key, value in races.items() if len(value) > 0}
    df = pd.DataFrame(non_zero_races)
    df.to_csv("data/raw/fastf1_races_sessions(1950-2024).csv", index=False)
    print("Races data saved to fastf1_races_sessions(1950-2024).csv")


if __name__ == "__main__":
    main()
