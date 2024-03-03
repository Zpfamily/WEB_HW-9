from models import Author, Quote
import connect
import json
from pathlib import Path


def load_data_from_json(file_path, model):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            for item in data:
                # Якщо модель - цитата, то спочатку знаходимо або створюємо автора
                if model == Quote:
                    author_name = item.pop('author')  # Видаляємо поле автора з даних цитати
                    author = Author.objects(fullname=author_name).first()  # Шукаємо автора за ім'ям
                    if not author:  # Якщо автор не знайдено, створюємо нового
                        author = Author(fullname=author_name).save()
                    item['author'] = author  # Встановлюємо автора як посилання
                model(**item).save()
            print(f"Data from {file_path} loaded successfully into {model.__name__} collection.")
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
    except Exception as e:
        print(f"Error occurred while loading data from {file_path}: {e}")


def search_quotes(command):

    current_directory = Path(__file__).resolve().parent
    
    authors_path = current_directory / "authors.json"
    quotes_path = current_directory / "quotes.json"

    load_data_from_json(authors_path,Author)
    load_data_from_json(quotes_path, Quote)
    
        
    print("Received command:", command)
    parts = command.split(':')
    if len(parts) != 2:
        print("Invalid command format.")
        return

    category, value = parts
    category = category.strip()
    value = value.strip()

    try:
        if category == 'name':
            # Search for quotes by author fullname
            author = Author.objects(fullname=value).first()
            if author:
                quotes = Quote.objects(author=author)
                if quotes:
                    for quote in quotes:
                        print(f'"{quote.quote}" - {author.fullname}')
                else:
                    print(f"No quotes found for author {value}")
            else:
                print(f"No author found with name {value}")
        elif category == 'tag':
            # Search for quotes by tag
            quotes = Quote.objects(tags__in=[value])
            if quotes:
                for quote in quotes:
                    print(f'"{quote.quote}" - {quote.author.fullname}')
            else:
                print(f"No quotes found for tag {value}")
        elif category == 'tags':
            # Search for quotes by multiple tags
            tags = value.split(',')
            quotes = Quote.objects(tags__in=tags)
            if quotes:
                for quote in quotes:
                    print(f'"{quote.quote}" - {quote.author.fullname}')
            else:
                print("No quotes found for the provided tags")
        else:
            print("Invalid command category:", category)
    except Exception as e:
        print("Error occurred during query execution:", e)



























