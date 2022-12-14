from pymongo import MongoClient
from .credentials import database, instance

client = MongoClient(f"mongodb+srv://{database}/?retryWrites=true&w=majority")
db = client[instance]

