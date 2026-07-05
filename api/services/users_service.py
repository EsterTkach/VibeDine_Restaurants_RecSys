from api.db.mongo import (
    users_collection,
    user_interactions_collection,
    restaurants_collection
)

def _get_all_liked_ids(user_id: str) -> list:
    """Merge liked_restaurants from both users_collection and user_interactions_collection."""
    interactions = user_interactions_collection.find_one({"user_id": user_id})
    interaction_likes = set(interactions.get("liked_restaurants", []) if interactions else [])

    user = users_collection.find_one({"user_id": user_id})
    user_likes = set(user.get("liked_restaurants", []) if user else [])

    return list(interaction_likes | user_likes)

def get_user_online_likes(user_id: str):
    liked_ids = _get_all_liked_ids(user_id)
    return {"user_id": user_id, "online_likes": liked_ids}

def get_user_online_liked_restaurants(user_id: str):
    user = users_collection.find_one(
        {"user_id": user_id},
        {
            "_id": 0,
            "liked_restaurants": 1,
        },
    )

    if not user:
        return []

    online_ids = user.get("liked_restaurants", [])

    if not online_ids:
        return []

    restaurants = list(
        restaurants_collection.find(
            {"gmap_id": {"$in": online_ids}},
            {
                "_id": 0,
                "gmap_id": 1,
                "name": 1,
                "image_url": 1,
            },
        )
    )

    restaurants_by_id = {
        restaurant["gmap_id"]: restaurant for restaurant in restaurants
    }

    return [
        restaurants_by_id[gmap_id]
        for gmap_id in online_ids
        if gmap_id in restaurants_by_id
    ]

