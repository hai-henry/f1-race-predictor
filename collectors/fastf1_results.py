"""
Scrape race results data from 1950-2024 from FastF1 API.
"""

# TODO: Actively append data to csv file just incase of errors, when recontinuing, start from where it left off instead of re-fetching all dataz3

import os
import random
import time

import fastf1
import pandas as pd

# Initialize the results dictionary
results = {
    "season": [],
    "round": [],
    "grand_prix": [],
    "pos": [],
    "classified_pos": [],
    "time": [],
    "status": [],
    "points": [],
    "grid_pos": [],
    "abbrv": [],
    "first_name": [],
    "last_name": [],
    "full_name": [],
    "driver_num": [],
    "driver_id": [],
    "country_code": [],
    "team_name": [],
    "team_id": [],
}

# Load RACES dataset, skipping processed rows
RACES = pd.read_csv("data/raw/races/fastf1_races(1950-2024).csv")
RACES = RACES[(RACES["season"] >= 2024) & (RACES["round_num"] > 23)]


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
    Save the results data to a CSV file.

    Args:
        dictionary (dict): The dictionary to save.
        filename (str): The filename to save the data to.
    """
    df = pd.DataFrame(dictionary)
    df.to_csv(f"data/raw/results/{filename}.csv", index=False)
    print(f"Results data saved to {filename}.csv")


def fetch_results(races):
    """
    Fetch the results for a given grand prix.

    Args:
        races (pd.DataFrame): The races to fetch the results for.
    """
    # Iterate over the grand prixs in the season
    for _, row in races.iterrows():
        season = row["season"]
        round_num = row["round_num"]
        grand_prix = row["event_name"]

        session = fastf1.get_session(season, grand_prix, "R")
        session.load()
        print(season, round_num, grand_prix)

        fields = {
            "season": season,
            "round": round_num,
            "grand_prix": grand_prix,
            "pos": "Position",
            "classified_pos": "ClassifiedPosition",
            "grid_pos": "GridPosition",
            "time": "Time",
            "status": "Status",
            "points": "Points",
            "abbrv": "Abbreviation",
            "first_name": "FirstName",
            "last_name": "LastName",
            "full_name": "FullName",
            "driver_num": "DriverNumber",
            "driver_id": "DriverId",
            "team_name": "TeamName",
            "team_id": "TeamId",
            "country_code": "CountryCode",
        }

        # Iterate over the drivers in the session
        for _, driver_data in session.results.iterrows():
            # Iterate over the fields in the dictionary
            for key, column_name in fields.items():
                try:
                    # Special case for time
                    if key == "time":
                        raw_time = (
                            driver_data[column_name]
                            if column_name in driver_data
                            else None
                        )
                        if pd.notnull(raw_time):  # Check if time is not null
                            formatted_time = str(raw_time).replace("0 days ", "")
                            results[key].append(formatted_time)
                        else:
                            results[key].append(None)
                    elif key in ["season", "round", "grand_prix"]:
                        results[key].append(column_name)
                    else:
                        # If column name is in driver_data, append the value, else append None
                        results[key].append(
                            driver_data[column_name]
                            if column_name in driver_data
                            else None
                        )
                except Exception as e:
                    print(f"Error processing {key}: {e}")
                    results[key].append(None)

        time.sleep(random.uniform(3, 10))  # Delay to avoid overwhelming the server


def main():
    clear_cache()
    fastf1.Cache.enable_cache("./cache")

    fetch_results(RACES)
    save_data(results, "fastf1_results(1950-2024)")


if __name__ == "__main__":
    main()
