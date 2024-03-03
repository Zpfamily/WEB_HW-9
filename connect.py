from mongoengine import connect
import configparser
from pathlib import Path
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi



configpath = Path(__file__).resolve().parent / "config.ini"

config = configparser.ConfigParser()

config.read(configpath)


mongo_user = config.get('DB', 'USER')
mongodb_pass = config.get('DB', 'PASS')
db_name = config.get('DB', 'DB_NAME')
domain = config.get('DB', 'DOMAIN')


connect(host = f"mongodb+srv://{mongo_user}:{mongodb_pass}@{domain}.{db_name}?retryWrites=true&w=majority&appName=vassabi", ssl=True)
