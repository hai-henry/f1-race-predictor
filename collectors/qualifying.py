import os
import random
import time

import fastf1
import pandas as pd

DATA_DIR = "data/raw"
QUALIFYING_PATH = f"{DATA_DIR}/qualifying(1950-2024).csv"
RACES_PATH = f"{DATA_DIR}/races(1950-2024).csv"
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
    filepath = f"{DATA_DIR}/{filename}"
    df.to_csv(
        filepath,
        mode="a",
        header=not os.path.exists(filepath),
        index=False,
    )
    print(f"Data appended to {filename}.")


def fetch_qualifying(races):
    """
    Fetch qualifying data for given races.

    Args:
        races (pd.DataFrame): DataFrame containing race details (season, round_num, event_name).
    """
    for _, row in races.iterrows():
        season = row["season"]
        round_num = row["RoundNumber"]
        grand_prix = row["EventName"]

        print(f"Processing qualifying data for Season {season}, Round {round_num}...")

        try:
            session = fastf1.get_session(season, round_num, "Q")
            session.load()

            qualifying_data = session.results.copy()
            qualifying_data["season"] = season
            qualifying_data["RoundNumber"] = round_num
            qualifying_data["EventName"] = grand_prix

            # Reorder columns so season, round_num, and grand_prix are first
            columns_order = ["season", "RoundNumber", "EventName"] + [
                col
                for col in qualifying_data.columns
                if col not in ["season", "RoundNumber", "EventName"]
            ]
            qualifying_data = qualifying_data[columns_order]

            append_data_to_csv(qualifying_data, "qualifying(1950-2024).csv")

        except Exception as e:
            print(
                f"Error processing qualifying for Season {season}, Round {round_num}: {e}"
            )

        time.sleep(random.uniform(*DELAY_RANGE))  # Delay to avoid overloading the API


def main():
    clear_cache()
    fastf1.Cache.enable_cache("./cache")

    # Load existing qualifying data if available
    if os.path.exists(QUALIFYING_PATH):
        print("Loading existing qualifying dataset...")
        qualifying_existing = pd.read_csv(QUALIFYING_PATH)

        # Create a set of processed (season, round_num) pairs
        processed = set(
            zip(qualifying_existing["season"], qualifying_existing["RoundNumber"])
        )
    else:
        print("No existing qualifying dataset found. Starting fresh...")
        processed = set()

    # Load races and filter out processed sessions
    races = pd.read_csv(RACES_PATH)
    races = races[
        ~races[["season", "RoundNumber"]].apply(tuple, axis=1).isin(processed)
    ]
    races = races[races["season"] >= 2020]  # Filter seasons

    if races.empty:
        print("No new races to process. Exiting.")
    else:
        fetch_qualifying(races)


if __name__ == "__main__":
    main()
