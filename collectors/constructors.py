# The Constructors Championship was not awarded until 1958
# This program will calculate the Constructors Championship standings from 1958 to 2024

import os

import pandas as pd

DRIVER_STANDINGS_PATH = "data/raw/driver_standings(1950-2024).csv"
OUTPUT_PATH = "data/raw/constructor_standings(1950-2024).csv"


class Constructor:
    def __init__(self, season, team, drivers, points=0):
        self.season = season
        self.team = team
        self.drivers = drivers
        self.points = points

    def team_info(self):
        return f"Team: {self.team}, Drivers: {', '.join(self.drivers)}, Points: {self.points}"

    def add_points(self, points):
        self.points += points


def main():
    driver_standings = pd.read_csv(DRIVER_STANDINGS_PATH)
    driver_standings = driver_standings[driver_standings["season"] >= 1958]

    for season, season_data in driver_standings.groupby("season"):
        constructor_objects = {}

        for _, driver in season_data.iterrows():
            if driver["TeamName"] in constructor_objects:
                constructor_objects[driver["TeamName"]].add_points(driver["Points"])
            else:
                constructor = Constructor(
                    season=driver["season"],
                    team=driver["TeamName"],
                    drivers=[driver["FullName"]],
                    points=driver["Points"],
                )
                constructor_objects[driver["TeamName"]] = constructor

        constructor_data = [
            {
                "season": constructor.season,
                "Position": position + 1,
                "TeamName": constructor.team,
                "Points": constructor.points,
            }
            for position, constructor in enumerate(
                sorted(
                    constructor_objects.values(), key=lambda x: x.points, reverse=True
                )
            )
        ]
        constructor_df = pd.DataFrame(constructor_data)

        # Append to CSV file; write header only if file doesn't exist
        if not os.path.exists(OUTPUT_PATH):
            constructor_df.to_csv(OUTPUT_PATH, index=False, mode="w", header=True)
        else:
            constructor_df.to_csv(OUTPUT_PATH, index=False, mode="a", header=False)


if __name__ == "__main__":
    main()
