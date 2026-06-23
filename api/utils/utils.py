def format_restaurant_for_frontend(restaurant_doc: dict) -> dict:
    """Maps database fields to match the frontend React keys precisely."""
    
    # Safe cuisine extraction
    categories = restaurant_doc.get("category", ["Food"])
    cuisine = categories[0] if isinstance(categories, list) and len(categories) > 0 else "Restaurant"

    # Fallback price calculation just in case the real one is missing
    price_tags = ["$", "$$", "$$$", "$$$$"]
    num_reviews = restaurant_doc.get("num_of_reviews", 10)
    price_idx = (num_reviews % 3) + 1 

    return {
        "id": restaurant_doc.get("gmap_id") or str(restaurant_doc.get("_id", "1")),
        "name": restaurant_doc.get("name", "Unknown Spot"),
        "cuisine": cuisine,
        "rating": restaurant_doc.get("avg_rating", 4.0),
        # Prioritizes real data, falls back to the mock logic/links if missing
        "price": restaurant_doc.get("price") or price_tags[price_idx],
        "image": restaurant_doc.get("image_url") or "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4", 
    }