import os
import pandas as pd
import numpy as np
import random
import ast
import re
from pymongo import MongoClient
from enums.models_enums import CuisineType, EstablishmentType, MealType, DiningStyle, PopularFoodItem, DietaryPreference, Vibe
from enums.mapping_config import (
    RAW_CATEGORY_MAPPING, IMAGE_MAPPING, EXCLUDED_CATEGORIES,
    ATMOSPHERE_MAPPING, CROWD_MAPPING, DINING_OPTIONS_MAPPING, OFFERINGS_MAPPING,
)


def parse_list_field(raw_value):
    """Safely parse a parquet list/string field into a Python list."""
    if raw_value is None or (isinstance(raw_value, float) and pd.isna(raw_value)):
        return []
    if isinstance(raw_value, (list, np.ndarray)):
        return [str(v).strip() for v in raw_value if v and not (isinstance(v, float) and pd.isna(v))]
    if isinstance(raw_value, str):
        if raw_value.startswith("["):
            try:
                return [str(v).strip() for v in ast.literal_eval(raw_value)]
            except Exception:
                pass
        return [raw_value.strip()]
    return []


def derive_extra_enums(atmosphere_values, crowd_values, dining_option_values, offering_values):
    """Derive additional enums from supplementary parquet columns."""
    extra = set()
    for val in atmosphere_values:
        extra.update(ATMOSPHERE_MAPPING.get(val, []))
    for val in crowd_values:
        extra.update(CROWD_MAPPING.get(val, []))
    for val in dining_option_values:
        extra.update(DINING_OPTIONS_MAPPING.get(val, []))
    for val in offering_values:
        extra.update(OFFERINGS_MAPPING.get(val, []))
    return extra

def get_restaurant_image(matched_enums):
    """ בוחרת תמונה רנדומלית מתוך IMAGE_MAPPING לפי סדר העדיפויות שהגדרנו """
    # Popular Food Items (עדיפות 1)
    for e in matched_enums:
        if isinstance(e, PopularFoodItem):
            key = f"PopularFoodItem.{e.name}"
            if key in IMAGE_MAPPING: 
                return random.choice(IMAGE_MAPPING[key])
                
    # Cuisine Types (עדיפות 2)
    for e in matched_enums:
        if isinstance(e, CuisineType):
            key = f"CuisineType.{e.name}"
            if key in IMAGE_MAPPING: 
                return random.choice(IMAGE_MAPPING[key])
                
    # Establishment Types (עדיפות 3)
    for e in matched_enums:
        if isinstance(e, EstablishmentType):
            key = f"EstablishmentType.{e.name}"
            if key in IMAGE_MAPPING: 
                return random.choice(IMAGE_MAPPING[key])
                
    # ברירת מחדל אם אין שום התאמה
    return random.choice(IMAGE_MAPPING["EstablishmentType.RESTAURANT"])

# ==========================================
# פונקציה חדשה: ארגון ופיצול שעות פעילות
# ==========================================
def parse_hours(raw_hours):
    """
    הופכת את מחרוזת השעות הגולמית למערך של אובייקטים:
    [{"day": "Friday", "open": "7AM", "close": "2PM"}, ...]
    """
    if pd.isna(raw_hours) or not raw_hours:
        return []
    
    parsed_list = []
    # 1. ניסיון להמיר את המחרוזת של ה-Parquet לרשימה אמיתית בפייתון
    if isinstance(raw_hours, str) and raw_hours.startswith('['):
        try:
            parsed_list = ast.literal_eval(raw_hours)
        except Exception:
            return []
    elif isinstance(raw_hours, list) or isinstance(raw_hours, np.ndarray):
        parsed_list = raw_hours
        
    structured_hours = []
    for item in parsed_list:
        if len(item) != 2: 
            continue
            
        day = item[0]
        time_range = item[1]
        
        # טיפול ביום סגור
        if time_range.lower() == "closed":
            structured_hours.append({"day": day, "open": "Closed", "close": "Closed"})
            continue
            
        # פיצול השעות לפי מקף רגיל או מקף ארוך (\u2013)
        parts = re.split(r'[-–—]| to ', time_range)
        
        if len(parts) == 2:
            structured_hours.append({
                "day": day, 
                "open": parts[0].strip(), 
                "close": parts[1].strip()
            })
        else:
            # מקרה קצה - אם יש פורמט לא צפוי, פשוט נשמור את כל המחרוזת
            structured_hours.append({"day": day, "open": time_range, "close": time_range})
            
    return structured_hours
# ==========================================

def process_and_upload():
    # התחברות למונגו
    client = MongoClient("mongodb+srv://yuvalnamirbarr:xAaOYUtq4GQTN3t8@cluster0.yodtpzx.mongodb.net/?appName=Cluster0")
    db = client["restaurants_project_db"]
    collection = db["restaurants"]
    
    # ניקוי הטבלה הריצה
    collection.drop()
    
    print("Reading Parquet file...")
    df = pd.read_parquet(os.path.join(os.path.dirname(__file__), "CBF_item_features_2.parquet"))
    
    batch = []
    print("Processing restaurant rows...")
    
    for _, row in df.iterrows():
        # --- חילוץ בטוח של קטגוריות ---
        raw_categories = row.get("category")
        category_list = []
        
        if isinstance(raw_categories, (list, np.ndarray)):
            category_list = [str(c).strip() for c in raw_categories if pd.notna(c)]
        elif isinstance(raw_categories, str):
            category_list = [c.strip() for c in raw_categories.split(",")]
            
        matched_enums = set()
        should_skip = False
        
        for cat in category_list:
            # אם מצאנו קטגוריה שמופיעה ברשימה השחורה (קניונים/שווקים) - נדליק נורה אדומה ונעצור
            if cat in EXCLUDED_CATEGORIES:
                should_skip = True
                break
                
            if cat in RAW_CATEGORY_MAPPING:
                matched_enums.update(RAW_CATEGORY_MAPPING[cat])
                
        # אם הנורה האדומה דולקת (זה קניון/שוק) - מדלגים מיד לשורה הבאה בקובץ
        if should_skip:
            continue
                
        # אם אין התאמה (חנות אופניים/בנק) - נדלג
        if not matched_enums:
            continue
            
        # --- פישוט שדה הנגישות לערך בולאני ---
        raw_accessibility = row.get("accessibility")
        is_accessible = False
        if isinstance(raw_accessibility, (list, np.ndarray)) and len(raw_accessibility) > 0:
            is_accessible = True
        elif isinstance(raw_accessibility, str) and len(raw_accessibility) > 0:
            is_accessible = True
            
        # --- פתרון דרישה 1: טיפול במחירים עם התפלגות סטטיסטית ---
        raw_price = row.get("price")
        if pd.isna(raw_price) or not raw_price or str(raw_price).lower() == 'null':
            # השלמת נתונים רנדומלית לפי: 50% $, 48% $$, 2% $$$
            final_price = random.choices(["$", "$$", "$$$"], weights=[50, 48, 2], k=1)[0]
        else:
            final_price = raw_price
            
        # --- פתרון דרישה 2: בניית מערך השעות המאורגן ---
        structured_hours = parse_hours(row.get("hours"))
            
        # --- בחירת תמונה מייצגת ---
        image_url = get_restaurant_image(matched_enums)
        
        # --- קריאת שדות נוספים מהפרקט ---
        atmosphere_values = parse_list_field(row.get("atmosphere"))
        crowd_values = parse_list_field(row.get("crowd"))
        dining_option_values = parse_list_field(row.get("dining_options"))
        offering_values = parse_list_field(row.get("offerings"))

        extra_enums = derive_extra_enums(atmosphere_values, crowd_values, dining_option_values, offering_values)
        all_enums = matched_enums | extra_enums

        # --- יצירת אובייקט GeoJSON למיקום ---
        lat = float(row["latitude"]) if pd.notna(row.get("latitude")) else None
        lon = float(row["longitude"]) if pd.notna(row.get("longitude")) else None

        location_obj = None
        if lat is not None and lon is not None:
            location_obj = {
                "type": "Point",
                "coordinates": [lon, lat]  # שימו לב: Longitude קודם ל-Latitude
            }

        # --- יצירת המסמך ---
        mongo_doc = {
            "_id": str(row["gmap_id"]),
            "gmap_id": str(row["gmap_id"]),
            "name": str(row["name"]) if pd.notna(row.get("name")) else "",
            "location": location_obj,
            "avg_rating": float(row["avg_rating"]) if pd.notna(row.get("avg_rating")) else 0.0,
            "num_of_reviews": int(row["num_of_reviews"]) if pd.notna(row.get("num_of_reviews")) else 0,
            "price": final_price,
            "is_accessible": is_accessible,
            "image_url": image_url,
            "hours": structured_hours,

            # פיצול ה-Enums למערכים במונגו (כולל נתונים מכל עמודות הפרקט)
            "cuisines": list(set(e.value for e in all_enums if isinstance(e, CuisineType))),
            "establishment_types": list(set(e.value for e in all_enums if isinstance(e, EstablishmentType))),
            "meal_types": list(set(e.value for e in all_enums if isinstance(e, MealType))),
            "dining_styles": list(set(e.value for e in all_enums if isinstance(e, DiningStyle))),
            "popular_items": list(set(e.value for e in all_enums if isinstance(e, PopularFoodItem))),
            "dietary_preferences": list(set(e.value for e in all_enums if isinstance(e, DietaryPreference))),
            "vibe": list(set(e.value for e in all_enums if isinstance(e, Vibe))),
        }
        
        batch.append(mongo_doc)
        
        # העלאה ב-Batches
        if len(batch) >= 1000:
            collection.insert_many(batch)
            batch = []
            
    if batch:
        collection.insert_many(batch)
        
    print(f"Successfully processed and uploaded restaurants to Atlas! (Total documents: {collection.count_documents({})})")

if __name__ == "__main__":
    process_and_upload()
