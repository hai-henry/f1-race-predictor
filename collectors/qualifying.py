import os
import random
import time

import fastf1
import pandas as pd

DATA_DIR = "data/raw"
QUALIFYING_PATH = f"{DATA_DIR}/qualifying(1950-2024).csv"
RACES_PATH = f"{DATA_DIR}/races(1950-2024).csv"
DELAY_RANGE = (3, 10)


def clear_cache():
    """
    Clear the cache.
    """
    clear_cache = input("Do you want to clear the cache? (y/n): ").lower()
    if clear_cache == "y":
        fastf1.Cache.clear_cache("./cache")
        print("Cache cleared.")


def initialize_qualifying():
    """
    Initialize qualify directory.
    """
    return {
        "season": [],
        "round_num": [],
        "grand_prix": [],
        "position": [],
        "driver_num": [],
        "full_name": [],
        "q1": [],
        "q2": [],
        "q3": [],
    }


def append_data_to_csv(dictionary, filename):
    """
    Append the race data to the CSV file.

    Args:
        dictionary (dict): The dictionary to append.
        filename (str): The filename to append the data to.
    """
    df = pd.DataFrame(dictionary)
    df.to_csv(
        f"data/raw/{filename}.csv",
        mode="a",
        header=not os.path.exists(f"data/raw/{filename}.csv"),
        index=False,
    )
    print(f"Data appended to {filename}.csv")


def clean_time(raw_time):
    """
    Clean the time string by removing 'days' and formatting correctly.

    Args:
        raw_time (str): The raw time string (e.g., '0 days 00:01:30.031000').

    Returns:
        str: The cleaned time string (e.g., '00:01:30.031000'), or None if invalid.
    """
    if pd.notnull(raw_time):
        return (
            str(raw_time).replace("0 days ", "").split(".")[0]
        )  # Remove days and keep up to seconds
    return None


def fetch_qualifying(races):
    """
    Fetch qualifying data for given races.

    Args:
        races (dataframe): Dataframe containing qualifying details (season, round_num, event_name, drivers, qualifying times).
    """
    qualifying = initialize_qualifying()
    for _, row in races.iterrows():
        season = row["season"]
        round_num = row["round_num"]
        grand_prix = row["event_name"]

        print(f"Processing qualifying data for Season {season}, Round {round_num}...")

        try:
            session = fastf1.get_session(season, round_num, "Q")
            session.load()

            for _, driver in session.results.iterrows():
                qualifying["season"].append(season)
                qualifying["round_num"].append(round_num)
                qualifying["grand_prix"].append(grand_prix)
                qualifying["position"].append(driver.get("Position", None))
                qualifying["driver_num"].append(driver.get("DriverNumber", None))
                qualifying["full_name"].append(driver.get("FullName", None))
                qualifying["q1"].append(clean_time(driver.get("Q1", None)))
                qualifying["q2"].append(clean_time(driver.get("Q2", None)))
                qualifying["q3"].append(clean_time(driver.get("Q3", None)))

            append_data_to_csv(qualifying, "qualifying(1950-2024)")

            # Reset qualifying dictionary for the next session
            qualifying = initialize_qualifying()
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
            zip(qualifying_existing["season"], qualifying_existing["round_num"])
        )
    else:
        print("No existing qualifying dataset found. Starting fresh...")
        qualifying_existing = pd.DataFrame()
        processed = set()

    # Load races and filter out processed sessions
    races = pd.read_csv(RACES_PATH)
    races = races[~races[["season", "round_num"]].apply(tuple, axis=1).isin(processed)]
    races = races[races["season"] == 2024]

    if races.empty:
        print("No new races to process. Exiting.")
    else:
        fetch_qualifying(races)


if __name__ == "__main__":
    main()
