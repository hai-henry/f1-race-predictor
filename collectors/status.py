import pandas as pd


def main():
    data = pd.read_csv("data/processed/results(1950-2024)_processed.csv")

    # Group by 'season' and 'round' and count the occurrences of 'status'
    status_count = (
        data.groupby(["season", "RoundNumber", "EventName", "Status"])
        .size()
        .reset_index(name="count")
    )

    print(status_count)

    status_count.to_csv("data/raw/status(1950-2024).csv", index=False)


if __name__ == "__main__":
    main()
