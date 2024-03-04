import requests
import json
from bs4 import BeautifulSoup
import os


def scrape_quotes(base_url):
    quotes = []
    authors = []
    url = base_url
    while url:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        for quote in soup.find_all(class_="quote"):
            text = quote.find(class_="text").get_text()
            author = quote.find(class_="author").get_text()
            tags = [tag.get_text() for tag in quote.find_all(class_="tag")]
            quotes.append({"quote": text, "author": author, "tags": tags})
            # Scrape author's birth date, place, and description
            author_page_url = base_url + 'author/' + author.replace(" ", "-")
            author_response = requests.get(author_page_url)
            author_soup = BeautifulSoup(author_response.text, "html.parser")
            birth_date = author_soup.find("span", class_="author-born-date").get_text()
            birth_place = author_soup.find("span", class_="author-born-location").get_text()
            description = author_soup.find("div", class_="author-description").get_text().strip()
            author_info = {"fullname": author, "born_date": birth_date, "born_location": birth_place, "description": description}
            authors.append(author_info)
        next_button = soup.find(class_="next")
        url = base_url + next_button.find("a")["href"] if next_button else None
    return quotes, authors


def save_to_json(data, filename):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def main():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    quotes, authors = scrape_quotes("http://quotes.toscrape.com/")
    
    quotes_filename = os.path.join(current_directory, "quotes.json")
    save_to_json(quotes, quotes_filename)

    authors_filename = os.path.join(current_directory, "authors.json")
    save_to_json(authors, authors_filename)


if __name__ == "__main__":
    main()
