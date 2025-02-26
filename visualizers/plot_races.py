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

    # Select top 10 Grand Prix
    top_ten_events = event_count.head(10)

    # Create figure with dark background
    fig, ax = plt.subplots(figsize=(8, 6))
    fig.patch.set_facecolor(background_color)
    ax.set_facecolor(background_color)

    # Create bar plot
    bars = sns.barplot(
        x="Occurences", y="EventName", data=top_ten_events, color=bar_color, ax=ax
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
    plt.tight_layout(pad=10)
    plt.subplots_adjust(left=0.2)

    # Add counts on the sides of the bars
    for p in ax.patches:
        ax.text(
            p.get_width() + 1,
            p.get_y() + p.get_height() / 2,
            int(p.get_width()),
            fontsize=12,
            color="white",
            ha="left",
            va="center",
        )

    # Final touches
    # Expand x-axis limits for padding
    max_occurrences = top_ten_events["Occurences"].max()
    ax.set_xlim(0, max_occurrences + 10)

    print(event_count)
    # Save and show
    # plt.savefig("f1_grand_prix_occurrences.png", facecolor=background_color)
    plt.show()


if __name__ == "__main__":
    main()
