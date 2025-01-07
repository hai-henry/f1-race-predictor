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

    constructor_objects = {}

    # Group by season and team to processess each season separately
    for (season, team_name), group in driver_standings.groupby(["season", "TeamName"]):
        drivers = group["FullName"].tolist()
        total_points = group["Points"].sum()

        if team_name in constructor_objects:
            constructor_objects[team_name].add_points(total_points)
        else:
            constructor = Constructor(
                season=season,
                team=team_name,
                drivers=drivers,
                points=total_points,
            )
            constructor_objects[team_name] = constructor

    # Convert to dataframe
    constructors_data = [
        {
            "season": constructor.season,
            "TeamName": constructor.team,
            "Drivers": ", ".join(constructor.drivers),
            "Points": constructor.points,
        }
        for constructor in constructor_objects.values()
    ]

    constructors_df = pd.DataFrame(constructors_data)

    constructors_df.to_csv(OUTPUT_PATH, index=False)


if __name__ == "__main__":
    main()
