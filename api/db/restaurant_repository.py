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
    min_rating: float = 0.0,
    min_reviews: int = 0,
) -> list:
    """
    Retrieves, scores, and ranks restaurants using an advanced MongoDB Aggregation Pipeline.

    This function operates in three distinct phases:
    1. Quality Gateway ($match): Immediately drops any restaurants that do not meet
       the `min_rating` or `min_reviews` thresholds. This protects frontend rendering
       from low-quality results while remaining entirely optional (default 0) so as
       not to blind Machine Learning models fetching broad candidate pools.
    2. Tag Scoring ($addFields): Calculates a dynamic `match_score` for every surviving
       restaurant by calculating the intersection between the user's requested tags
       and the restaurant's actual tags using `$setIntersection`.
    3. Global Ranking ($sort & $limit): Sorts the ENTIRE pool of matched restaurants
       by their `match_score` (highest first), using `avg_rating` as a tie-breaker.
       Only after the definitive top matches are ranked does it slice the requested
       `limit` to send back to the client.

    Args:
        skip (int): Pagination offset. Defaults to 0.
        limit (int): Maximum number of top documents to return. Defaults to 50.
        categories (list, optional): Exact-match category strings (e.g., ["Sushi", "Sushi restaurant"]).
        accessibility (list, optional): Accessibility tags.
        service_options (list, optional): Service tags (e.g., ["Delivery", "Takeout"]).
        atmosphere (list, optional): Atmosphere tags (e.g., ["Cozy", "Casual"]).
        dining_options (list, optional): Dining tags.
        crowd (list, optional): Crowd tags.
        offerings (list, optional): Offering tags.
        min_rating (float, optional): The absolute minimum average rating required. Defaults to 0.0.
        min_reviews (int, optional): The absolute minimum number of reviews required. Defaults to 0.

    Returns:
        list: A ranked and paginated list of restaurant dictionaries, containing
              core fields like `_id`, `name`, `avg_rating`, and `match_score`.
    """
    # 1. Build the base Match Query
    query = {}

    # Apply quality thresholds ONLY if they are explicitly requested
    if min_rating > 0:
        query["avg_rating"] = {"$gte": min_rating}
    if min_reviews > 0:
        query["num_of_reviews"] = {"$gte": min_reviews}

    # Apply flexible $in filters (Restaurant must match at least ONE tag in the provided list)
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

    # 2. Build the Projection (Fields to return)
    projection = {
        "_id": 1,
        "gmap_id": 1,
        "name": 1,
        "avg_rating": 1,
        "num_of_reviews": 1,
        "category": 1,
        "price": 1,
    }

    # Dynamically include any fields that were actively filtered
    for field in query.keys():
        if field not in [
            "avg_rating",
            "num_of_reviews",
        ]:  # Prevent projection duplication errors
            projection[field] = 1

    # 3. Build the Tag Scoring Math
    score_components = []

    def add_intersection(field_name, user_list):
        return {
            "$size": {
                "$setIntersection": [
                    {
                        "$ifNull": [f"${field_name}", []]
                    },  # Fallback to empty array if DB field is missing
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

    # 4. Construct the Aggregation Pipeline
    pipeline = [{"$match": query}]

    if score_components:
        pipeline.append({"$addFields": {"match_score": {"$add": score_components}}})
        pipeline.extend(
            [
                # Sort by highest tag match score, break ties with highest rating
                {"$sort": {"match_score": -1, "avg_rating": -1}},
                {"$skip": skip},
                {"$limit": limit},
                {"$project": projection},
            ]
        )
    else:
        # Fallback if no specific tags were requested (e.g., just looking for highly rated places)
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


