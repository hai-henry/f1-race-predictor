"""
Scrape race results data from 1950-2024 from FastF1 API and actively append to CSV file.
"""

import os
import random
import time

import fastf1
import pandas as pd

# Load the races dataset, skipping processed rows
RACES = pd.read_csv("data/raw/races/races(1950-2024).csv")

# Load the results dataset, if it exists
if os.path.exists("data/raw/results/results(1950-2024).csv"):
    RESULTS = pd.read_csv("data/raw/results/results(1950-2024).csv")
    # Filter out already processed races
    processed = set(zip(RESULTS["season"], RESULTS["round"]))
    RACES = RACES[~RACES[["season", "round_num"]].apply(tuple, axis=1).isin(processed)]
else:
    RESULTS = pd.DataFrame()
    processed = set()


def initialize_results():
    return {
        "season": [],
        "round": [],
        "grand_prix": [],
        "pos": [],
        "classified_pos": [],
        "grid_pos": [],
        "time": [],
        "status": [],
        "points": [],
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
    Append the results data to the CSV file.

    Args:
        dictionary (dict): The dictionary to append.
        filename (str): The filename to append the data to.
    """
    df = pd.DataFrame(dictionary)
    df.to_csv(
        f"data/raw/results/{filename}.csv",
        mode="a",
        header=not os.path.exists(f"data/raw/results/{filename}.csv"),
        index=False,
    )
    print(f"Data appended to {filename}.csv")


def fetch_results(races):
    """
    Fetch the results for a given grand prix.

    Args:
        races (pd.DataFrame): The races to fetch the results for.
    """
    # Iterate over the grand prixs in the season
    for _, row in races.iterrows():
        results = initialize_results()  # Initialize a fresh dictionary for each race
        season = row["season"]
        round_num = row["round_num"]
        grand_prix = row["event_name"]

        print(f"Processing: Season {season}, Round {round_num}, {grand_prix}")

        try:
            session = fastf1.get_session(season, grand_prix, "R")
            session.load()

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
                        # Handle the time field separately
                        if key == "time":
                            raw_time = driver_data.get(column_name, None)
                            if pd.notnull(raw_time):
                                formatted_time = str(raw_time).replace("0 days ", "")
                                results[key].append(formatted_time)
                            else:
                                results[key].append(None)
                        elif key in ["season", "round", "grand_prix"]:
                            results[key].append(column_name)
                        else:
                            results[key].append(driver_data.get(column_name, None))
                    except Exception as e:
                        print(f"Error processing {key}: {e}")
                        results[key].append(None)

            # Actively append the fetched data to the CSV
            append_data_to_csv(results, "results(1950-2024)")
        except Exception as e:
            print(f"Error processing season {season}, round {round_num}: {e}")
        finally:
            time.sleep(random.uniform(3, 10))  # Delay to avoid overwhelming the server


def main():
    clear_cache()
    fastf1.Cache.enable_cache("./cache")

    if RACES.empty:
        print("No new races to process. Exiting.")
    else:
        fetch_results(RACES)


if __name__ == "__main__":
    main()
