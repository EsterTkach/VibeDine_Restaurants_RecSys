import os
from pathlib import Path
from dotenv import load_dotenv
from pymongo import MongoClient

BASE_DIR = Path(__file__).resolve().parents[1]  # תיקיית api
load_dotenv(BASE_DIR / ".env") # Need to be removed after docker was accepted

MONGO_URI = os.getenv("MONGO_URI") or "mongodb://localhost:27017"

client = MongoClient(MONGO_URI)

db = client["restaurants_project_db"]

users_collection = db["users"]
restaurants_collection = db["restaurants"]
user_interactions_collection = db["user_interactions"]

#print(client.list_database_names())
