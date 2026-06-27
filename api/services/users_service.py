from api.db.mongo import (
    users_collection,
    user_interactions_collection
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


