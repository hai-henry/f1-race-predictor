import pandas as pd


def main():
    # Load data
    data = pd.read_csv("data/raw/races(1950-2024).csv")

    data = data[data["RoundNumber"] != 0]

    # Save data
    data.to_csv("data/processed/races(1950-2024)_processed.csv", index=False)
    print("Data cleaned and saved!")


if __name__ == "__main__":
    main()
