import pandas as pd


def main():
    # Load data
    data = pd.read_csv("data/raw/races(1950-2024).csv")

    data = data[data["RoundNumber"] != 0]

    # Change Brazilian Grand Prix to current name: São Paulo Grand Prix
    data["EventName"] = data["EventName"].replace(
        "Brazilian Grand Prix", "São Paulo Grand Prix"
    )

    # Save data
    data.to_csv("data/processed/races(1950-2024)_processed.csv", index=False)
    print("Data cleaned and saved!")


if __name__ == "__main__":
    main()
