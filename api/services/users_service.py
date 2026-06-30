from api.db.mongo import (
    users_collection,
    user_interactions_collection,
    restaurants_collection
)

def get_user_online_likes(
    user_id: str
):

    user_interactions = user_interactions_collection.find_one(
        {
            "user_id":
            user_id
        }
    )

    if not user_interactions:
        return {
            "user_id":
            user_id,

            "online_likes":
            []
        }

    return {
        "user_id":
        user_id,

        "online_likes":
        user_interactions.get(
            "liked_restaurants",
            []
        )
    }

def get_user_online_liked_restaurants(user_id: str):
    print('user_id: ', user_id)
    user = users_collection.find_one(
        {"user_id": user_id}
    )
    print('user: ', user)

    if not user:
        return []

    liked_restaurant_ids = user.get("liked_restaurants", [])
    print('liked_restaurant_ids: ', liked_restaurant_ids)

    if not liked_restaurant_ids:
        return []

    liked_restaurants = list(
        restaurants_collection.find(
            {
                "gmap_id": {
                    "$in": liked_restaurant_ids
                }
            },
            {
                "_id": 0,
                "gmap_id": 1,
                "name": 1,
                "image_url":1
            }
        )
    )

    return liked_restaurants
