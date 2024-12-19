import requests
import pandas as pd
from bs4 import BeautifulSoup

races = {'season': [], 'grand_prix': [], 'date': [], 'winner': [], 'team': [], 'laps': [], 'time': [], 'url': []}

def main():
    URL = "https://www.formula1.com/en/results/2024/races"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
  
    # Find all anchor tags with the specified class
    races = soup.find_all("a", class_="underline underline-offset-normal decoration-1 decoration-greyLight hover:decoration-brand-primary")
    
    # Link to append to the href, takes you to the results of GP
    append_link = "https://www.formula1.com/en/results/2024"

    # Extract the and race name
    for gp in races:
      grand_prix = gp.text  # Get the text inside the anchor tag
      href = grand_prix.get("href") # Get the href attribute
      print(f"Race: {grand_prix}, URL: {append_link}/{href}") # Print the race name and URL
    

if __name__ == "__main__":
    main()
