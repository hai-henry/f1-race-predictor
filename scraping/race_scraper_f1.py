"""
Scrape race data from 1950-2024 from the Formula 1 website.
"""

import random
import re
import time
from datetime import datetime

import pandas as pd
import requests
from bs4 import BeautifulSoup

BEGIN_SCRAPE_SEASON = 1950
END_SCRAPE_SEASON = 2024
EXPECTED_COMPONENTS_LENGTH = 6

# Headers for the HTTP request
HEADERS = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.9",
    "Dnt": "1",
    "Origin": "https://www.formula1.com",
    "Priority": "u=1, i",
    "Referer": "https://www.formula1.com/",
    "Sec-Ch-Ua": '"Chromium";v="131", "Not_A Brand";v="24"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "macOS",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
}

# Base URL for Formula 1 results
BASE_URL = "https://www.formula1.com/en/results/{year}/races"

races = {
    "season": [],
    "grand_prix": [],
    "date": [],
    "winner": [],
    "constructor": [],
    "laps": [],
    "time": [],
    "url": [],
}


def scrape_season(year):
    """
    Scrape race data for a given season.

    Args:
        year (int): Season year
    """

    print(f"Scraping season: {year}")
    url = BASE_URL.format(year=year)

    # Attempt to get the response
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
    except requests.RequestException as e:
        print(f"Error fetching data for year {year}: {e}")
        return

    # Target the rows with the specified class, rows are white and grey on the website
    rows = soup.find_all("tr", class_=re.compile("bg-(brand-white|grey-10)"))
    for row in rows:
        # For each row, find the cells with paragraph tags
        data_cells = row.find_all(
            "p",
            class_="f1-text font-titillium tracking-normal font-normal non-italic normal-case leading-none f1-text__micro text-fs-15px",
        )

        url_to_append = f"https://www.formula1.com/en/results/{year}/"
        for cell in data_cells:
            race_url_element = cell.find(
                "a",
                class_="underline underline-offset-normal decoration-1 decoration-greyLight hover:decoration-brand-primary",
            )
            if race_url_element:
                race_url = race_url_element["href"]
                url_to_append += race_url
                break

        # Clean each cell's text
        components = [cell.text.strip().replace("\xa0", " ") for cell in data_cells]

        if len(components) >= EXPECTED_COMPONENTS_LENGTH:
            try:
                races["season"].append(year)
            except Exception:
                races["season"].append(None)

            try:
                races["grand_prix"].append(components[0])
            except Exception:
                races["grand_prix"].append(None)

            try:
                # Format the date to YYYY-MM-DD
                original_date = components[1]
                formatted_date = datetime.strptime(original_date, "%d %b %Y").strftime(
                    "%Y-%m-%d"
                )
                races["date"].append(formatted_date)
            except Exception:
                races["date"].append(None)

            try:
                races["winner"].append(components[2])
            except Exception:
                races["winner"].append(None)

            try:
                races["constructor"].append(components[3])
            except Exception:
                races["constructor"].append(None)

            try:
                races["laps"].append(components[4])
            except Exception:
                races["laps"].append(None)

            try:
                races["time"].append(components[5])
            except Exception:
                races["time"].append(None)

            try:
                races["url"].append(url_to_append)
            except Exception:
                races["url"].append(None)
        else:
            print(f"Skipping row due to unexpected structure: {components}")

    time.sleep(random.uniform(3, 12))  # Delay to avoid overwhelming the server


def main():
    for year in range(BEGIN_SCRAPE_SEASON, END_SCRAPE_SEASON + 1):
        scrape_season(year)

    # Convert only non-zero keys in races to DataFrame
    non_zero_races = {key: value for key, value in races.items() if len(value) > 0}
    df = pd.DataFrame(non_zero_races)
    df.to_csv("data/raw/races(1950-2024).csv", index=False)
    print("Races data saved to races(1950-2024).csv")


if __name__ == "__main__":
    main()
