import fastf1
import pandas as pd

RACES_PATH = "data/raw/races(1950-2024).csv"


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

    return sprint.results


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

    sprints = get_all_sprints(RACES_PATH)
    sprints.to_csv("data/raw/sprints.csv", index=False)


if __name__ == "__main__":
    main()
