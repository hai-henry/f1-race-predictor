"""
Collect sprint data for Formula 1.
"""

import os

import fastf1
import pandas as pd

RACES_PATH = "data/raw/races(1950-2024).csv"
SPRINT_RESULTS_PATH = "data/raw/sprint_results.csv"
SPRINT_QUALIFYING_PATH = "data/raw/sprint_qualifying.csv"


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


def get_sprint_qualifying_results(season: int, round_num: int) -> pd.DataFrame:
    """
    Get sprint qualifying (formerly known as shootout) results.

    Args:
        season (int): Season of the sprint qualifying
        round_num (int): Round number of the sprint qualifying

    Returns:
        pd.DataFrame: Dataframe of sprint qualifying session results.
    """
    # Determine the identifier based on the season
    identifier = "SS" if season < 2024 else "SQ"

    sprint_qualify = fastf1.get_session(season, round_num, identifier)
    sprint_qualify.load()

    results = sprint_qualify.results.copy()
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


def process_sprints(sprints: pd.DataFrame):
    """
    Process sprint races and append results to the sprint_results.csv.

    Args:
        sprints (pd.DataFrame): Dataframe containing sprint race metadata.
    """
    # Check for existing sprint results
    if os.path.exists(SPRINT_RESULTS_PATH):
        existing_sprint_results = pd.read_csv(SPRINT_RESULTS_PATH)
        processed_sprints = set(
            zip(
                existing_sprint_results["season"],
                existing_sprint_results["RoundNumber"],
            )
        )
    else:
        processed_sprints = set()

    for _, row in sprints.iterrows():
        season = row["season"]
        round_num = row["RoundNumber"]

        if (season, round_num) in processed_sprints:
            print(
                f"Skipping already processed sprint: Season {season}, Round {round_num}"
            )
            continue

        try:
            sprint_results = get_sprint_results(season, round_num)

            # Reorder columns to start with season and RoundNumber
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
            print(
                f"Processed and saved sprint results: Season {season}, Round {round_num}"
            )
        except Exception as e:
            print(f"Error processing sprint: Season {season}, Round {round_num} - {e}")


def process_sprint_qualifying(sprints: pd.DataFrame):
    """
    Process sprint qualifying races and append results to the sprint_qualifying.csv.

    Args:
        sprints (pd.DataFrame): Dataframe containing sprint race metadata.
    """
    # Check for existing sprint qualifying results
    if os.path.exists(SPRINT_QUALIFYING_PATH):
        existing_sprint_qual_results = pd.read_csv(SPRINT_QUALIFYING_PATH)
        processed_qualifying = set(
            zip(
                existing_sprint_qual_results["season"],
                existing_sprint_qual_results["RoundNumber"],
            )
        )
    else:
        processed_qualifying = set()

    for _, row in sprints.iterrows():
        season = row["season"]
        round_num = row["RoundNumber"]

        if (season, round_num) in processed_qualifying:
            print(
                f"Skipping already processed sprint qualifying: Season {season}, Round {round_num}"
            )
            continue

        try:
            sprint_qual_results = get_sprint_qualifying_results(season, round_num)

            # Reorder columns to start with season and RoundNumber
            columns_order = ["season", "RoundNumber"] + [
                col
                for col in sprint_qual_results.columns
                if col not in ["season", "RoundNumber"]
            ]
            sprint_qual_results = sprint_qual_results[columns_order]

            sprint_qual_results.to_csv(
                SPRINT_QUALIFYING_PATH,
                mode="a",
                header=not os.path.exists(SPRINT_QUALIFYING_PATH),
                index=False,
            )
            print(
                f"Processed and saved sprint qualifying results: Season {season}, Round {round_num}"
            )
        except Exception as e:
            print(
                f"Error processing sprint qualifying: Season {season}, Round {round_num} - {e}"
            )


def main():
    clear_cache()
    fastf1.Cache.enable_cache("./cache")

    # Load sprint races
    sprints = pd.read_csv("data/raw/sprints.csv")

    # Process sprint results
    process_sprints(sprints)

    # Process sprint qualifying results
    process_sprint_qualifying(sprints)


if __name__ == "__main__":
    main()
