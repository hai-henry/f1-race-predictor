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
    driver_standings = driver_standings[driver_standings["season"] >= 2024]

    # print(driver_standings)

    constructor_objects = {}

    for _, driver in driver_standings.iterrows():
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

    # Print constructor objects

    constructor_data = [
        {
            "season": constructor.season,
            "Position": position + 1,
            "TeamName": constructor.team,
            "Points": constructor.points,
        }
        for position, constructor in enumerate(
            sorted(constructor_objects.values(), key=lambda x: x.points, reverse=True)
        )
    ]
    constructor_df = pd.DataFrame(constructor_data)

    print(constructor_df)


if __name__ == "__main__":
    main()
