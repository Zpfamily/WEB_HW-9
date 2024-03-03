from models import Author, Quote
from seed import search_quotes
import connect
from connect import connect
from pathlib import Path
import json
from models import Author, Quote
import scrap

Author.drop_collection()
Quote.drop_collection()

scrap.main()

while True:
    command = input("Enter command (name/tag/tags: value) or 'exit' to quit: ")
    if command.lower() == 'exit':
        break
    search_quotes(command)



