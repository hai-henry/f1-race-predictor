import pandas as pd


def main():
    # Load status data
    data = pd.read_csv("data/raw/status(1950-2024).csv")

    # Load Races
    races = pd.read_csv("data/processed/races(1950-2024)_processed.csv")

    # Count occurences of races
    race_counts = races["EventName"].value_counts().reset_index()
    race_counts.columns = ["EventName", "Count"]

    # Keep only Status
    dangerous_statuses = [
        "Accident",
        "Collision",
        "Spun off",
        "Fatal accident",
        "Injury",
        "Injured",
        "Driver unwell",
        "Physical",
        "Debris",
        "Damage",
        "Collision damage",
        "Safety concerns",
        "Safety",
        "Fire",
        "Heat shield fire",
        "Engine fire",
        "Wheel",
        "Wheel nut",
        "Wheel bearing",
        "Tyre",
        "Tyre puncture",
        "Puncture",
        "Broken wing",
        "Rear wing",
        "Front wing",
        "Suspension",
        "Brakes",
        "Brake duct",
        "Steering",
        "Throttle",
        "Handling",
        "Track rod",
    ]

    # Filter data
    data = data[data["Status"].isin(dangerous_statuses)]

    # Group be event name, calculate the frequency of dangers per event and add new column
    data = data.groupby("EventName").size().reset_index(name="Dangers")

    # Merge data with race_counts, sort by race_counts
    data = pd.merge(data, race_counts, on="EventName")

    # Add column with frequency of accidents and collisions per event
    data["Dangers_Frequency"] = data["Dangers"] / data["Count"]

    # Sort by frequency
    data = data.sort_values(by="Dangers_Frequency", ascending=False)
    print(data)

    # Save data
    data.to_csv("data/raw/danger_frequency.csv", index=False)


if __name__ == "__main__":
    main()
