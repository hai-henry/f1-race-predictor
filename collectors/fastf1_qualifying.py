import fastf1

# TODO: Collect qualifying data for all races from 1950-2024
# TODO: Actively add qualifying data to the dataset as collected like results


def main():
    session = fastf1.get_session(2024, 1, "Q")
    session.load()
    print(session.results)
    session.results.drop(
        columns=["HeadshotUrl"], inplace=True
    )  # Drop HeadshotUrl from session results
    session.results.to_csv(
        "data/raw/qualifying/fastf1_qualifying(2024).csv", index=False
    )


if __name__ == "__main__":
    main()
