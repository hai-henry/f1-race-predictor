import os
import random
import time

import fastf1
import pandas as pd

# TODO: Collect qualifying data for all races from 1950-2024
# TODO: Actively add qualifying data to the dataset as collected like results


# Load the races dataset to get season and round
RACES = pd.read_csv("data/raw/races/races(1950-2024).csv")
RACES = RACES.loc[RACES["round_num"] != 0]  # Dropping pre-season testing


def main():
    # Extract relevant columns
    qualifying_data = RACES[["season", "round_num"]]

    # Save to a new CSV file for verification
    qualifying_data.to_csv("data/raw/qualifying(1950-2024).csv", index=False)

    print("Qualifying rounds data saved to qualifying(1950-2024).csv")


if __name__ == "__main__":
    main()
