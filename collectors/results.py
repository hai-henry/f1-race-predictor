"""
Scrape race results data from 1950-2024 from FastF1 API and actively append to CSV file.
"""

import os
import random
import time

import fastf1
import pandas as pd

RACES = pd.read_csv("data/raw/races(1950-2024).csv")
DELAY_RANGE = (2, 5)


def clear_cache():
    """
    Clear the cache.
    """
    clear_cache = input("Do you want to clear the cache? (y/n): ").lower()
    if clear_cache == "y":
        fastf1.Cache.clear_cache("./cache")
        print("Cache cleared.")


def append_data_to_csv(df, filename):
    """
    Append the DataFrame to the CSV file.

    Args:
        df (pd.DataFrame): The DataFrame to append.
        filename (str): The filename to append the data to.
    """
    filepath = f"data/raw/{filename}.csv"
    df.to_csv(
        filepath,
        mode="a",
        header=not os.path.exists(filepath),
        index=False,
    )
    print(f"Data appended to {filename}.")


def fetch_results(races):
    """
    Fetch the results for a given grand prix.

    Args:
        races (pd.DataFrame): The races to fetch the results for.
    """
    for _, row in races.iterrows():
        season = row["season"]
        round_num = row["RoundNumber"]
        grand_prix = row["EventName"]

        print(f"Processing: Season {season}, Round {round_num}, {grand_prix}")

        try:
            session = fastf1.get_session(season, round_num, "R")
            session.load()

            results = session.results.copy()
            results["season"] = season
            results["RoundNumber"] = round_num
            results["EventName"] = grand_prix

            # Reorder columns to ensure season, round_num, and grand_prix are first
            results = results[
                ["season", "RoundNumber", "EventName"]
                + [
                    col
                    for col in results.columns
                    if col not in ["season", "RoundNumber", "EventName"]
                ]
            ]

            append_data_to_csv(results, "results(1950-2024)")
        except Exception as e:
            print(f"Error processing season {season}, round {round_num}: {e}")
        finally:
            time.sleep(
                random.uniform(*DELAY_RANGE)
            )  # Delay to avoid overwhelming the server


def main():
    clear_cache()
    fastf1.Cache.enable_cache("./cache")

    # Load the results dataset, if it exists
    if os.path.exists("data/raw/results(1950-2024).csv"):
        RESULTS = pd.read_csv("data/raw/results(1950-2024).csv")
        # Filter out already processed races
        processed = set(zip(RESULTS["season"], RESULTS["RoundNumber"]))
        RACES = RACES[
            ~RACES[["season", "RoundNumber"]].apply(tuple, axis=1).isin(processed)
        ]
    else:
        RESULTS = pd.DataFrame()
        processed = set()

    if RACES.empty:
        print("No new races to process. Exiting.")
    else:
        fetch_results(RACES)


if __name__ == "__main__":
    main()
