import os

import pandas as pd

RESULTS_PATH = "data/raw/results(1950-2024).csv"
OUTPUT_PATH = "data/raw/driver_standings(1950-2024).csv"
SPRINT_RESULTS_PATH = "data/raw/sprint_results.csv"
BEGIN_SEASON = 1950


class Driver:
    def __init__(self, season, name, country, team, points):
        self.season = season
        self.name = name
        self.country = country
        self.team = team
        self.points = points

    def driver_info(self):
        return f"{self.name}, {self.country}, {self.team}, {self.points}"

    def add_points(self, points):
        self.points += points


def main():
    results = pd.read_csv(RESULTS_PATH)
    results = results[(results["season"] >= BEGIN_SEASON)]

    sprint_results = pd.read_csv(SPRINT_RESULTS_PATH)

    # Combine results and sprint_results into a single DataFrame
    combined_results = pd.concat([results, sprint_results])

    for season, season_data in combined_results.groupby("season"):
        driver_objects = {}

        for _, row in season_data.iterrows():
            driver_name = row["FullName"]

            # Assign points to driver, if points are null assign 0
            points = row["Points"] if pd.notnull(row["Points"]) else 0

            # Check if driver is already in dictionary, if not create new driver object
            if driver_name in driver_objects:
                driver_objects[driver_name].add_points(points)
            else:
                driver = Driver(
                    season=row["season"],
                    name=row["FullName"],
                    country=row["CountryCode"],
                    team=row["TeamName"],
                    points=points,
                )
                driver_objects[driver_name] = driver

        # Create dataframe from driver objects, sorted by points
        drivers_data = [
            {
                "season": driver.season,
                "Position": position + 1,
                "FullName": driver.name,
                "CountryCode": driver.country,
                "Team": driver.team,
                "Points": driver.points,
            }
            for position, driver in enumerate(
                sorted(
                    driver_objects.values(),
                    key=lambda x: x.points,
                    reverse=True,
                )
            )
        ]
        season_df = pd.DataFrame(drivers_data)

        # Append to CSV file; write header only if file doesn't exist
        if not os.path.exists(OUTPUT_PATH):
            season_df.to_csv(OUTPUT_PATH, index=False, mode="w", header=True)
        else:
            season_df.to_csv(OUTPUT_PATH, index=False, mode="a", header=False)


if __name__ == "__main__":
    main()
