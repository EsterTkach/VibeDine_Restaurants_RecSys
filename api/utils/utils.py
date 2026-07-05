from api.db.mongo import restaurants_collection
from datetime import datetime

def format_restaurant_for_frontend(restaurant_doc: dict) -> dict:
    """
    Maps database fields to match the strict frontend React Restaurant interface precisely.
    If fields are missing, it uses gmap_id to look up and pull missing data from the database.
    """
    # 1. Extract the only strictly required field
    gmap_id = restaurant_doc.get("gmap_id")
    if not gmap_id:
        raise ValueError("Missing 'gmap_id': This field is strictly required to process restaurant data.")

    # 2. Check if the doc is just a skeleton. 
    # We now check for 'image_url' or 'avg_rating' instead of 'name', 
    # because the ML model returns the name but omits the images/ratings.
    if (
        "image_url" not in restaurant_doc 
        or not restaurant_doc.get("image_url") 
        or "avg_rating" not in restaurant_doc
    ):
        full_doc = restaurants_collection.find_one({"gmap_id": gmap_id})
        if full_doc:
            # Merge the found database record back into our working document
            # full_doc overwrites restaurant_doc for missing/empty fields
            restaurant_doc = {**restaurant_doc, **full_doc}

    # 3. Process Cuisine field safely
    categories = restaurant_doc.get("cuisines", [])
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
        "price": real_price,  
        "image_url": restaurant_doc.get("image_url", ""), 
    }

from enum import Enum


class MealTime(Enum):
    BREAKFAST = "breakfast"
    LUNCH = "lunch"
    DINNER = "dinner"


MEAL_TIME_TITLES = {
    MealTime.BREAKFAST: "Rise & Dine 🌅 Breakfast spots",
    MealTime.LUNCH: "Lunch O'Clock 🍽️ Midday picks",
    MealTime.DINNER: "Dinner Time 🌙 Evening favorites",
}


def get_meal_time() -> MealTime:
    """
    Returns the current MealTime enum based on server hour.

    Time Windows:
    - 05:00 to 11:59 -> BREAKFAST
    - 12:00 to 16:59 -> LUNCH
    - 17:00 to 04:59 -> DINNER
    """
    current_hour = datetime.now().hour

    if 5 <= current_hour < 12:
        return MealTime.BREAKFAST
    elif 12 <= current_hour < 17:
        return MealTime.LUNCH
    else:
        return MealTime.DINNER


def get_meal_time_string() -> str:
    """
    Checks the current server time and returns 'breakfast', 'lunch', or 'dinner'.
    """
    return get_meal_time().value

def extract_gmap_ids(restaurants: list) -> list:
    """
    Extracts a clean list of gmap_id strings from a list of restaurant dictionaries.
    
    Args:
        restaurants (list): The list of dicts returned by get_filtered_restaurants_repo.
        
    Returns:
        list: A list of gmap_id strings ready for the recommendation engine.
    """
    if not restaurants:
        return []
        
    # Standard list comprehension to grab the ID, with a safety check for the key
    return [res["gmap_id"] for res in restaurants if "gmap_id" in res]

def enrich_restaurants(restaurant_list: list, full_docs_dict: dict) -> list:
    """
    Merges ML skeleton restaurant data with full database documents in memory.
    This prevents N+1 database queries when formatting data for the frontend.
    """
    enriched_list = []
    for r in restaurant_list:
        gmap_id = r.get("gmap_id")
        if gmap_id in full_docs_dict:
            # Merge the live DB doc on top of the skeleton
            enriched_list.append({**r, **full_docs_dict[gmap_id]})
        else:
            enriched_list.append(r)
            
    return enriched_list