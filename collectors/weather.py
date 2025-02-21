# Weather data only collected for seasons 2018 onwards
# FastF1 API does not provide weather data for seasons before 2018

import os
import random
import time

import fastf1
import pandas as pd

# File paths and constants
RACES_PATH = "data/raw/races(1950-2024).csv"
WEATHER_OUTPUT_PATH = "data/raw/weather_test.csv"
DELAY_RANGE = (1, 5)


def clear_cache():
    """
    Prompt the user to clear the FastF1 cache.
    """
    clear = input("Do you want to clear the cache? (y/n): ").lower()
    if clear == "y":
        fastf1.Cache.clear_cache("./cache")
        print("Cache cleared.")


def append_data_to_csv(df, filepath):
    """
    Append a DataFrame to a CSV file.
    The header is written only if the file doesn't already exist.
    """
    df.to_csv(filepath, mode="a", header=not os.path.exists(filepath), index=False)
    print(f"Data appended to {filepath}.")


def create_placeholder_weather(season, round_num, event_name, columns):
    """
    Create a placeholder DataFrame with NA values for weather data.

    Args:
        season (int): The season.
        round_num (int): The round number.
        event_name (str): The event name.
        columns (list): List of expected columns.

    Returns:
        pd.DataFrame: A one-row DataFrame with NA values.
    """
    placeholder = {col: None for col in columns}
    placeholder["season"] = season
    placeholder["RoundNumber"] = round_num
    placeholder["EventName"] = event_name
    # Convert dictionary to DataFrame with one row
    return pd.DataFrame([placeholder])


def main():
    clear_cache()
    fastf1.Cache.enable_cache("./cache")

    # Load the races dataset
    races = pd.read_csv(RACES_PATH)
    races = races[races["season"] >= 2018]  # Filter

    # Check if the weather output CSV already exists.
    if os.path.exists(WEATHER_OUTPUT_PATH):
        print("Loading existing weather dataset...")
        existing_weather = pd.read_csv(WEATHER_OUTPUT_PATH)
        processed = set(
            zip(existing_weather["season"], existing_weather["RoundNumber"])
        )
    else:
        print("No existing weather dataset found. Starting fresh...")
        processed = set()

    # Define the expected columns for weather data.
    # Here we use the current columns of a successful session, or you can define them manually.
    expected_columns = [
        "season",
        "RoundNumber",
        "EventName",
        "AirTemp",
        "TrackTemp",
        "Humidity",
        "WindSpeed",
        "WindDirection",
        "Pressure",
    ]  # adjust as needed

    # Iterate through each race in the races DataFrame
    for _, row in races.iterrows():
        season = row["season"]
        round_num = row["RoundNumber"]
        event_name = row["EventName"]

        # Skip race if weather data already processed
        if (season, round_num) in processed:
            print(f"Skipping Season {season}, Round {round_num} (already processed).")
            continue

        print(
            f"Processing weather data for Season {season}, Round {round_num} ({event_name})..."
        )
        try:
            # Get the race session with weather data enabled
            session = fastf1.get_session(season, round_num, "R")
            session.load(weather=True)
            weather_data = session.weather_data.copy()  # Get weather data as DataFrame

            # Add additional columns to track the race
            weather_data["season"] = season
            weather_data["RoundNumber"] = round_num
            weather_data["EventName"] = event_name

            # Reorder columns so that season, RoundNumber, and EventName appear first
            cols_order = ["season", "RoundNumber", "EventName"] + [
                col
                for col in weather_data.columns
                if col not in ["season", "RoundNumber", "EventName"]
            ]
            weather_data = weather_data[cols_order]

            # Append the weather data to the CSV file
            append_data_to_csv(weather_data, WEATHER_OUTPUT_PATH)
            processed.add((season, round_num))
        except Exception as e:
            print(f"Error processing Season {season}, Round {round_num}: {e}")
            # Create a placeholder row with NA values for the weather data
            placeholder_df = create_placeholder_weather(
                season, round_num, event_name, expected_columns
            )
            append_data_to_csv(placeholder_df, WEATHER_OUTPUT_PATH)
            processed.add((season, round_num))

        # Delay between requests to avoid overwhelming the API
        time.sleep(random.uniform(*DELAY_RANGE))


if __name__ == "__main__":
    main()
