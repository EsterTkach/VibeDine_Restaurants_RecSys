import pandas as pd
import random
from faker import Faker
from pymongo import MongoClient

def process_and_upload_users():
    # התחברות למונגו
    client = MongoClient("mongodb+srv://___.mongodb.net/?appName=Cluster0")
    db = client["restaurants_project_db"]
    collection = db["users"]
    
    # ניקוי הטבלה לפני העלאה מחדש
    collection.drop()
    
    # אתחול ספריית Faker באנגלית
    fake = Faker('en_US')
    
    print("Reading interactions Parquet file to extract unique users...")
    # קריאת עמודת ה-user_id בלבד כדי לחסוך בזיכרון
    df_interactions = pd.read_parquet("CF_interaction_matrix_2.parquet", columns=["user_id"])
    
    # חילוץ רשימת המשתמשים הייחודיים
    unique_user_ids = df_interactions["user_id"].dropna().unique()
    total_users = len(unique_user_ids)
    print(f"Found {total_users} unique users. Generating profiles and uploading to Atlas...")
    
    batch = []
    
    for i, user_id in enumerate(unique_user_ids, 1):
        # 1. הגרלת שם מלא באנגלית
        full_name = fake.unique.name()
        
        # 2. יצירת שם משתמש
        base_username = full_name.lower().replace(" ", "_")
        username = f"{base_username}_{random.randint(100, 9999)}"
        
        # 3. קואורדינטות קליפורניה
        lat = round(random.uniform(32.5, 42.0), 6)
        lon = round(random.uniform(-124.5, -114.1), 6)
        
        # 4. יצירת אובייקט ה-GeoJSON למיקום
        location_obj = {
            "type": "Point",
            "coordinates": [lon, lat]  # Longitude תמיד ראשון
        }
        
        # 5. יצירת המסמך למונגו
        user_doc = {
            "_id": str(user_id),
            "user_id": str(user_id),
            "name": full_name,
            "username": username,
            "password": "1234",
            "liked_restaurants": [],
            "friends": [],
            "preferences": [],
            "location": location_obj,             # השדה הגיאוגרפי החדש 
            "avatar_index": random.randint(1, 6)
        }
        
        batch.append(user_doc)
        
        # דחיפה למונגו ב-Batches והדפסת חיווי התקדמות
        if len(batch) >= 5000:
            collection.insert_many(batch)
            batch = []
            print(f"Progress: Uploaded {i} / {total_users} users...")
            
    # הכנסת השארית
    if batch:
        collection.insert_many(batch)
        print(f"Progress: Uploaded {total_users} / {total_users} users...")
        
    print(f"Successfully finished! Total documents in 'users' collection: {collection.count_documents({})}")

if __name__ == "__main__":
    process_and_upload_users()