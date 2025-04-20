from pymongo import MongoClient
from db.test_data import DOCLADS_DATA
import os

client = MongoClient(os.getenv("MONGO_URL", "mongodb://mongo:27017/"))
db = client["conference"]  
collection = db["doclads"]  

collection.create_index("title")

result = collection.insert_many(DOCLADS_DATA)