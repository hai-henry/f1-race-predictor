"""
Collect sprint data for Formula 1.
"""

import os

import fastf1
import pandas as pd

RACES_PATH = "data/raw/races(1950-2024).csv"
SPRINT_RESULTS_PATH = "data/raw/sprint_results.csv"


def get_all_sprints(race_path: str) -> pd.DataFrame:
    """
    Grab all sprint races from given csv file of Formula 1 races.

    Args:
        race_path (str): Path to csv of races.

    Returns:
        pd.DataFrame: Dataframe containing only sprint races.
    """
    races = pd.read_csv(race_path)
    sprint_races = races[
        races["EventFormat"].isin(["sprint", "sprint_shootout", "sprint_qualifying"])
    ]
    print("All Sprint races saved.")

    return sprint_races


def get_sprint_results(season: int, round_num: int) -> pd.DataFrame:
    """
    Get sprint race results.

    Args:
        season (int): Season of the sprint
        round_num (int): Round number of the sprint

    Returns:
        pd.DataFrame: Dataframe of sprint session results.
    """
    sprint = fastf1.get_session(season, round_num, "S")
    sprint.load()

    results = sprint.results.copy()
    results["season"] = season
    results["RoundNumber"] = round_num

    return results


def clear_cache():
    """
    Clear the cache.
    """
    clear_cache = input("Do you want to clear the cache? (y/n): ").lower()
    if clear_cache == "y":
        fastf1.Cache.clear_cache("./cache")
        print("Cache cleared.")


def main():
    clear_cache()
    fastf1.Cache.enable_cache("./cache")

    sprints = pd.read_csv("data/raw/sprints.csv")

    # Check for existing results
    if os.path.exists(SPRINT_RESULTS_PATH):
        existing_results = pd.read_csv(SPRINT_RESULTS_PATH)
        processed = set(
            zip(existing_results["season"], existing_results["RoundNumber"])
        )
    else:
        existing_results = pd.DataFrame()
        processed = set()

    # Process sprints and append results
    for _, row in sprints.iterrows():
        season = row["season"]
        round_num = row["RoundNumber"]

        if (season, round_num) in processed:
            print(f"Skipping already processed: Season {season}, Round {round_num}")
            continue

        try:
            sprint_results = get_sprint_results(season, round_num)

            # Ensure season and round are the first columns
            columns_order = ["season", "RoundNumber"] + [
                col
                for col in sprint_results.columns
                if col not in ["season", "RoundNumber"]
            ]
            sprint_results = sprint_results[columns_order]

            sprint_results.to_csv(
                SPRINT_RESULTS_PATH,
                mode="a",
                header=not os.path.exists(SPRINT_RESULTS_PATH),
                index=False,
            )
            print(f"Processed and saved: Season {season}, Round {round_num}")
        except Exception as e:
            print(f"Error: Season {season}, Round {round_num} - {e}")


if __name__ == "__main__":
    main()
