"""
Scrape race schedule data from 1950-2024 from FastF1 API and actively append to CSV file.
"""

import os
import random
import time

import fastf1
import pandas as pd

BEGIN_SCRAPE_SEASON = 1950
END_SCRAPE_SEASON = 2024

RACES_PATH = "data/raw/races(1950-2024).csv"
DELAY_RANGE = (1, 5)


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


def fetch_races():
    """
    Fetch race schedules for all seasons from BEGIN_SCRAPE_SEASON to END_SCRAPE_SEASON.
    """
    # Load existing races data if available
    if os.path.exists(RACES_PATH):
        print("Loading existing races dataset...")
        races_existing = pd.read_csv(RACES_PATH)

        # Create a set of processed seasons
        processed = set(races_existing["season"].unique())
    else:
        print("No existing races dataset found. Starting fresh...")
        processed = set()

    for year in range(BEGIN_SCRAPE_SEASON, END_SCRAPE_SEASON + 1):
        if year in processed:
            print(f"Skipping Season {year}: Already processed.")
            continue

        print(f"Processing Season {year}...")
        try:
            schedule = fastf1.get_event_schedule(year)

            schedule_df = schedule.copy()
            schedule_df["season"] = year

            # Reorder columns to ensure "season" comes first
            schedule_df = schedule_df[
                ["season"] + [col for col in schedule_df.columns if col != "season"]
            ]

            append_data_to_csv(schedule_df, "races(1950-2024)")
        except Exception as e:
            print(f"Error processing Season {year}: {e}")
        finally:
            time.sleep(
                random.uniform(*DELAY_RANGE)
            )  # Delay to avoid overloading the API


def main():
    clear_cache()
    fastf1.Cache.enable_cache("./cache")

    fetch_races()


if __name__ == "__main__":
    main()
