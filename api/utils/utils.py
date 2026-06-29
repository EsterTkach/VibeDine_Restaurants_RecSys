from api.db.mongo import (restaurants_collection)
from datetime import datetime

def format_restaurant_for_frontend(restaurant_doc: dict) -> dict:
    """
    Maps database fields to match the strict frontend React Restaurant interface precisely.
    If fields are missing, it uses gmap_id to look up and pull missing data from the database.
    """
    # 1. Extract the only strictly necessary field
    gmap_id = restaurant_doc.get("gmap_id")
    if not gmap_id:
        raise ValueError("Missing 'gmap_id': This field is strictly required to process restaurant data.")

    # 2. Check if the doc is just a skeleton. If missing core info, query the full record.
    # We check for 'name' as a proxy indicator for whether the doc has been fully hydrated yet.
    if "name" not in restaurant_doc or not restaurant_doc.get("name"):
        full_doc = restaurants_collection.find_one({"gmap_id": gmap_id})
        if full_doc:
            # Merge the found database record back into our working document
            restaurant_doc = {**full_doc, **restaurant_doc}

    # 3. Process Cuisine/Category field safely
    categories = restaurant_doc.get("category", [])
    if isinstance(categories, str):
        cuisine_value = categories
    else:
        cuisine_value = categories[0] if isinstance(categories, list) and len(categories) > 0 else ""

    # 4. Process Price Level field safely
    real_price = restaurant_doc.get("price_level") or restaurant_doc.get("price") or ""

    # 5. Return payload perfectly matched to your strict frontend interface keys
    return {
        "gmap_id": str(gmap_id),
        "name": restaurant_doc.get("name", "Unknown Spot"),
        "cuisine": cuisine_value,
        "avg_rating": float(restaurant_doc.get("avg_rating", 0.0)),
        "price_level": real_price,  
        "image_url": restaurant_doc.get("image_url", ""), 
    }

def get_meal_time_string() -> str:
    """
    Checks the current server time and returns 'breakfast', 'lunch', or 'dinner'.
    
    Time Windows:
    - 05:00 to 11:59 -> breakfast
    - 12:00 to 16:59 -> lunch
    - 17:00 to 04:59 -> dinner (captures evening and late-night)
    """
    # Get the current server hour (0 to 23)
    current_hour = datetime.now().hour

    if 5 <= current_hour < 12:
        return "breakfast"
    elif 12 <= current_hour < 17:
        return "lunch"
    else:
        return "dinner"