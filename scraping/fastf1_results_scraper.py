"""
Scrape race results data from 1950-1950 from FastF1 API.
"""

import random
import time

import fastf1
import pandas as pd

results = {
    "season": [],
    "round": [],
    "grand_prix": [],
    "position": [],
    "classified_position": [],
    "grid_position": [],
    "time": [],
    "status": [],
    "points": [],
    "abbreviation": [],
    "first_name": [],
    "last_name": [],
    "full_name": [],
    "driver_number": [],
    "driver_id": [],
    "team_name": [],
    "team_id": [],
    "country_code": [],
}

RACES = pd.read_csv("data/raw/races/fastf1_races(1950-2024).csv")

# TODO: Account for failures. eg. 2017 Abu Dhabi Grand Prix failed to scrape


def main():
    fastf1.Cache.enable_cache("./cache")

    for index, row in RACES.iterrows():
        season = row["season"]
        round_num = row["round_num"]
        grand_prix = row["event_name"]

        session = fastf1.get_session(season, round_num, "R")
        session.load()
        print(season, round_num, grand_prix)

        for _, row in session.results.iterrows():
            try:
                results["season"].append(season)
            except Exception:
                results["season"].append(None)

            try:
                results["round"].append(round_num)
            except Exception:
                results["round"].append(None)

            try:
                results["grand_prix"].append(grand_prix)
            except Exception:
                results["grand_prix"].append(None)

            try:
                results["position"].append(row["Position"])
            except Exception:
                results["position"].append(None)

            try:
                results["classified_position"].append(row["ClassifiedPosition"])
            except Exception:
                results["classified_position"].append(None)

            try:
                results["grid_position"].append(row["GridPosition"])
            except Exception:
                results["grid_position"].append(None)

            try:
                # Remove "0 days" from the time string
                raw_time = row["Time"]
                if pd.notnull(raw_time):  # Check if the time is not null
                    if isinstance(raw_time, pd.Timedelta):  # If it's a Timedelta object
                        formatted_time = str(raw_time).replace("0 days ", "")
                    else:
                        formatted_time = str(raw_time).replace("0 days ", "")
                else:
                    formatted_time = None
                results["time"].append(formatted_time)
            except Exception:
                results["time"].append(None)

            try:
                results["status"].append(row["Status"])
            except Exception:
                results["status"].append(None)

            try:
                results["points"].append(row["Points"])
            except Exception:
                results["points"].append(None)

            try:
                results["abbreviation"].append(row["Abbreviation"])
            except Exception:
                results["abbreviation"].append(None)

            try:
                results["first_name"].append(row["FirstName"])
            except Exception:
                results["first_name"].append(None)

            try:
                results["last_name"].append(row["LastName"])
            except Exception:
                results["last_name"].append(None)

            try:
                results["full_name"].append(row["FullName"])
            except Exception:
                results["full_name"].append(None)

            try:
                results["driver_number"].append(row["DriverNumber"])
            except Exception:
                results["driver_number"].append(None)

            try:
                results["driver_id"].append(row["DriverId"])
            except Exception:
                results["driver_id"].append(None)

            try:
                results["team_name"].append(row["TeamName"])
            except Exception:
                results["team_name"].append(None)

            try:
                results["team_id"].append(row["TeamId"])
            except Exception:
                results["team_id"].append(None)

            try:
                results["country_code"].append(row["CountryCode"])
            except Exception:
                results["country_code"].append(None)

        # time.sleep(random.uniform(3, 12))  # Delay to avoid overwhelming the server

    # Convert only non-zero keys in races to DataFrame
    non_zero_results = {key: value for key, value in results.items() if len(value) > 0}
    df = pd.DataFrame(non_zero_results)
    df.to_csv("data/raw/results/fastf1_results(1950-2024).csv", index=False)
    print("Results data saved to fastf1_results(1950-2024).csv")


if __name__ == "__main__":
    main()
