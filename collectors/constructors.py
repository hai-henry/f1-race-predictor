import pandas as pd

DRIVER_STANDINGS_PATH = "data/raw/driver_standinds(1950-2024)"
class Constructor:
    def __init__(self, season, team, drivers, points=0):
        self.season = season
        self.team = team
        self.driver = drivers
        self.points = points
        

    def team_info(self):
        return f"{self.team}, {self.drivers}, {self.team}, {self.points}"

    def add_points(self, points):
        self.points += points

def main():
    driver_standings = pd.read_csv(
        DRIVER_STANDINGS_PATH
    )  # Idea is to add the points of driver's in the same team together

    for _, row in driver_standings.iterrows():
        

if __name__ == "__main__":
    main()
