import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)

db = client["vibedine"]

users_collection = db["users"]
user_interactions_collection = db["user_interactions"]
