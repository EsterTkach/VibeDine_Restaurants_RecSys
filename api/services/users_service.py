from api.db.mongo import (
    users_collection,
    restaurants_collection
)


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


def get_user_online_likes(user_id: str):
    online_likes = get_user_online_liked_restaurants(user_id)
    
    online_ids = [
        restaurant["gmap_id"]
        for restaurant in online_likes
        if "gmap_id" in restaurant
    ]
     
    return {"user_id": user_id, "online_likes": online_ids}
