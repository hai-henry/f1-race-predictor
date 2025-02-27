import pandas as pd


def main():
    data = pd.read_csv("data/raw/results(1950-2024).csv")

    # Drop unnecessary columns
    data.drop("HeadshotUrl", axis=1, inplace=True)
    data.drop("TeamColor", axis=1, inplace=True)
    data.drop("DriverId", axis=1, inplace=True)
    data.drop("TeamId", axis=1, inplace=True)

    data.to_csv("data/processed/results(1950-2024)_processed.csv", index=False)

    print("Data cleaned and saved!")


if __name__ == "__main__":
    main()
