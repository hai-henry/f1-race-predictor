import requests
from bs4 import BeautifulSoup


def main():
    URL = "https://www.formula1.com/en/results/2024/races"
    page = requests.get(URL)
    soup = BeautifulSoup(page.text, "html")
    print(soup.prettify())
    

if __name__ == "__main__":
    main()
