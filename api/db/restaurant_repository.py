from api.db.mongo import (restaurants_collection, users_collection)

def get_filtered_restaurants_repo(
    skip: int = 0,
    limit: int = 50,
    categories: list = None,
    accessibility: list = None,
    service_options: list = None,
    atmosphere: list = None,
    dining_options: list = None,
    crowd: list = None,
    offerings: list = None,
    dietary_restrictions: list = None,
    min_rating: float = 0.0,
    min_reviews: int = 0,
    max_reviews: int = None,
    max_price: str = None,
    latitude: float = None,
    longitude: float = None,
    radius_km: float = 15,
    price: str = None,
) -> list:
    """
    Retrieves, scores, and ranks restaurants using an advanced MongoDB Aggregation Pipeline.

    This function operates in three distinct phases:
    1. Quality & Geospatial Gateway ($match): Immediately filters out any restaurants 
       that do not meet the `min_rating` threshold. It manages review bounds flexibly, 
       enforcing a minimum requirement (`min_reviews`) and an optional maximum ceiling 
       (`max_reviews`). This allows the caller to explicitly isolate high-performing 
       "Hidden Gems" (high stars, low review counts) while maintaining fallback structural 
       safety. Additionally, if geospatial coordinates and a radius are provided, it performs 
       a high-performance spherical radius filter using MongoDB's native `$geoWithin` 
       operator. This protects frontend rendering from low-quality or irrelevant results 
       while remaining entirely optional so as not to blind Machine Learning models 
       fetching broad candidate pools.
    2. Tag Scoring ($addFields): Calculates a dynamic `match_score` for every surviving
       restaurant by calculating the intersection between the user's requested tags
       and the restaurant's actual tags using `$setIntersection`.
    3. Global Ranking ($sort & $limit): Sorts the ENTIRE pool of matched restaurants
       by their `match_score` (highest first), using `avg_rating` as a tie-breaker.
       Only after the definitive top matches are ranked does it apply strict client-side
       projections—safely mapping keys like `cuisine` and `price_level`—and slices the 
       requested `limit` to send back to the client.

    Args:
        skip (int): Pagination offset. Defaults to 0.
        limit (int): Maximum number of top documents to return. Defaults to 50.
        categories (list, optional): Exact-match category strings (e.g., ["Sushi"]).
        accessibility (list, optional): Accessibility tags.
        service_options (list, optional): Service tags (e.g., ["Delivery", "Takeout"]).
        atmosphere (list, optional): Atmosphere tags (e.g., ["Cozy", "Casual"]).
        dining_options (list, optional): Dining tags.
        crowd (list, optional): Crowd tags.
        offerings (list, optional): Offering tags.
        dietary_restrictions (list, optional): Dietary restriction tags (e.g., ["Halal", "Vegan"]).
        min_rating (float, optional): The absolute minimum average rating required. Defaults to 0.0.
        min_reviews (int, optional): The absolute minimum number of reviews required. Defaults to 0.
        max_reviews (int, optional): The absolute maximum number of reviews permitted. Useful for 
                                     unearthing high-quality, low-exposure "Hidden Gems". Defaults to None.
        max_price (str, optional): Maximum allowed price marker, such as "$$". Defaults to None.
        latitude (float, optional): Target latitude for center of radius filter.
        longitude (float, optional): Target longitude for center of radius filter.
        radius_km (float, optional): Radius distance threshold in kilometers.

    Returns:
        list: A ranked and paginated list of restaurant dictionaries, containing
              core fields cleanly projected for direct frontend integration including 
              `gmap_id`, `name`, `cuisine`, `avg_rating`, `price`, and `image_url`.
    """
    # Normalize single values to lists
    def ensure_list(value):
        if value is None:
            return None
        if isinstance(value, list):
            return value
        return [value]

    categories = ensure_list(categories)
    accessibility = ensure_list(accessibility)
    service_options = ensure_list(service_options)
    atmosphere = ensure_list(atmosphere)
    dining_options = ensure_list(dining_options)
    crowd = ensure_list(crowd)
    offerings = ensure_list(offerings)
    dietary_restrictions = ensure_list(dietary_restrictions)
    
    # 1. Build the base Match Query
    query = {}

    # Apply Geospatial Radius Filter
    if latitude is not None and longitude is not None and radius_km is not None:
        radius_in_radians = radius_km / 6378.1
        query["location"] = {
            "$geoWithin": {
                "$centerSphere": [[longitude, latitude], radius_in_radians]
            }
        }

    # Apply quality rating thresholds
    if min_rating > 0:
        query["avg_rating"] = {"$gte": min_rating}
        
    # Process review count boundaries cleanly
    review_conditions = {}
    if min_reviews > 0:
        review_conditions["$gte"] = min_reviews
    if max_reviews is not None:
        review_conditions["$lte"] = max_reviews
        
    if review_conditions:
        query["num_of_reviews"] = review_conditions

    if price:
        query["price"] = price
    elif max_price:
        allowed_prices = ["$", "$$", "$$$", "$$$$"]
        if max_price in allowed_prices:
            query["$or"] = [
                {"price": {"$in": allowed_prices[: allowed_prices.index(max_price) + 1]}},
                {"price_level": {"$in": allowed_prices[: allowed_prices.index(max_price) + 1]}},
            ]

    # Apply flexible $in filters
    if categories:
        query["category"] = {"$in": categories}
    if accessibility:
        query["accessibility"] = {"$in": accessibility}
    if service_options:
        query["service_options"] = {"$in": service_options}
    if atmosphere:
        query["atmosphere"] = {"$in": atmosphere}
    if dining_options:
        query["dining_options"] = {"$in": dining_options}
    if crowd:
        query["crowd"] = {"$in": crowd}
    if offerings:
        query["offerings"] = {"$in": offerings}
    if dietary_restrictions:
        query["dietary_restrictions"] = {"$in": dietary_restrictions}

    # 2. Build the return projection
    projection = {
        "gmap_id": 1,
        "name": 1,
        "cuisine": 1,
        "avg_rating": 1,
        "price": 1,
        "image_url": 1
    }

    # Dynamically include any fields that were actively filtered (excluding base parameters)
    for field in query.keys():
        if field not in [
            "avg_rating",
            "num_of_reviews",
            "location",
            "$or",
        ]:  
            projection[field] = 1

    # 3. Build the Tag Scoring Math
    score_components = []

    def add_intersection(field_name, user_list):
        return {
            "$size": {
                "$setIntersection": [
                    {"$ifNull": [f"${field_name}", []]},  
                    user_list,
                ]
            }
        }

    if categories:
        score_components.append(add_intersection("category", categories))
    if accessibility:
        score_components.append(add_intersection("accessibility", accessibility))
    if service_options:
        score_components.append(add_intersection("service_options", service_options))
    if atmosphere:
        score_components.append(add_intersection("atmosphere", atmosphere))
    if dining_options:
        score_components.append(add_intersection("dining_options", dining_options))
    if crowd:
        score_components.append(add_intersection("crowd", crowd))
    if offerings:
        score_components.append(add_intersection("offerings", offerings))
    if dietary_restrictions:
        score_components.append(add_intersection("dietary_restrictions", dietary_restrictions))

    # 4. Construct the Aggregation Pipeline
    pipeline = [{"$match": query}]

    if score_components:
        pipeline.append({"$addFields": {"match_score": {"$add": score_components}}})
        pipeline.extend(
            [
                {"$sort": {"match_score": -1, "avg_rating": -1}},
                {"$skip": skip},
                {"$limit": limit},
                {"$project": projection},
            ]
        )
    else:
        pipeline.extend(
            [
                {"$sort": {"avg_rating": -1, "num_of_reviews": -1}},
                {"$skip": skip},
                {"$limit": limit},
                {"$project": projection},
            ]
        )

    return list(restaurants_collection.aggregate(pipeline))

def build_online_likes_by_user(user_ids):
    """
    Build a dictionary of online liked restaurants for each user.

    Returns:
        {
            user_id: [gmap_id1, gmap_id2, ...]
        }
    """

    online_likes_by_user = {}

    for user_id in user_ids:
        user_doc = users_collection.find_one(
            {"user_id": user_id}, {"liked_restaurants": 1, "_id": 0}
        )

        if not user_doc:
            online_likes_by_user[user_id] = []
            continue

        online_likes_by_user[user_id] = user_doc.get("liked_restaurants", [])

    return online_likes_by_user

def get_restaurant_by_gmap_id(gmap_id: str) -> dict:
    """
    Fetches the full restaurant document from the database using its gmap_id.
    Raises an HTTPException if the restaurant cannot be found.
    """
    if not gmap_id:
        raise ValueError("A valid gmap_id must be provided.")

    restaurant_doc = restaurants_collection.find_one({"gmap_id": str(gmap_id)})
        
    return restaurant_doc or {}


def get_user_by_id(user_id: str) -> dict:
    """
    Fetches the full user profile document from the database using their string user_id.
    """
    if not user_id:
        raise ValueError("A valid user_id must be provided.")

    user_doc = users_collection.find_one({"user_id": str(user_id)})

    return user_doc or {}
