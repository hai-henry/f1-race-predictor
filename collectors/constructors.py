import pandas as pd

DRIVER_STANDINGS_PATH = "data/raw/driver_standinds(1950-2024)"


def main():
    driver_standings = pd.read_csv(
        DRIVER_STANDINGS_PATH
    )  # Idea is to add the points of driver's in the same team together


if __name__ == "__main__":
    main()
