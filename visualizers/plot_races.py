import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def main():
    # Set the dark theme style
    plt.style.use("dark_background")

    # Custom colors for dark theme
    background_color = "#000000"
    text_color = "white"
    grid_color = "#333333"
    bar_color = "red"

    # Load data
    data = pd.read_csv("data/processed/races(1950-2024)_processed.csv")

    # Count occurences of each Grand Prix
    event_count = data["EventName"].value_counts().reset_index()
    event_count.columns = ["EventName", "Occurences"]  # Rename columns

    # Create figure with dark background
    fig, ax = plt.subplots(figsize=(20, 20))
    fig.patch.set_facecolor(background_color)
    ax.set_facecolor(background_color)

    # Create bar plot
    bars = sns.barplot(
        x="Occurences", y="EventName", data=event_count, color=bar_color, ax=ax
    )

    # Style the plot
    ax.set_title("Occurrences of each Grand Prix", color=text_color, fontsize=16)
    ax.set_xlabel("Occurrences", color=text_color, fontsize=14)
    ax.set_ylabel("Grand Prix", color=text_color, fontsize=14)

    # Style the ticks
    ax.tick_params(colors=text_color, which="both")

    # Style the spines
    for spine in ax.spines.values():
        spine.set_color(grid_color)

    # Add grid for better readability
    ax.grid(True, linestyle="--", alpha=0.3, color=grid_color)

    # Adjust layout
    plt.tight_layout(pad=3)
    plt.subplots_adjust(left=0.3)

    # Save and show
    # plt.savefig("f1_grand_prix_occurrences.png", facecolor=background_color)
    plt.show()


if __name__ == "__main__":
    main()
