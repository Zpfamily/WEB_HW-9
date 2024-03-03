import requests
import json
from bs4 import BeautifulSoup
import os


def scrape_quotes(base_url):
    quotes = []
    url = base_url
    while url:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        for quote in soup.find_all(class_="quote"):
            text = quote.find(class_="text").get_text()
            author = quote.find(class_="author").get_text()
            tags = [tag.get_text() for tag in quote.find_all(class_="tag")]
            quotes.append({"quote": text, "author": author, "tags": tags})
        next_button = soup.find(class_="next")
        url = next_button.find("a")["href"] if next_button else None
        # If 'next_button' exists, it contains a relative URL, so we need to join it with the base URL
        if url and not url.startswith("http"):
            url = base_url + url
    return quotes



def save_to_json(data, filename):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def main():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    quotes = scrape_quotes("http://quotes.toscrape.com/")
    quotes_filename = os.path.join(current_directory, "quotes.json")
    save_to_json(quotes, quotes_filename)

    # Створення файлу з інформацією про авторів
    authors = [{"fullname": quote["author"]} for quote in quotes]
    authors_filename = os.path.join(current_directory, "authors.json")
    save_to_json(authors, authors_filename)
    
if __name__ == "__main__":
    main()

    
