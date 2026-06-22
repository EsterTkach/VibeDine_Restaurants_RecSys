from fastapi import (
    APIRouter
)

from uuid import uuid4

from api.db.mongo import (
    users_collection,
    user_interactions_collection
)

from api.schemas.user import (
    UserSignupRequest,
    UserLoginRequest,
    OnboardingPreferencesRequest,
    RestaurantInteractionRequest
)

from api.ml.cf_recommender import (
    user_item_matrix,
    user_id_to_index,
    index_to_item_id
)

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/signup")
def signup(
    request:
    UserSignupRequest
):

    user = {
        "user_id":
        str(uuid4()),

        "username":
        request.username,

        "password":
        request.password,
    }

    users_collection.insert_one(
        user
    )

    return {
        "message":
        "User created",

        "user_id":
        user["user_id"],
    }

@router.post("/login")
def login(
    request:
    UserLoginRequest
):

    user = users_collection.find_one(
        {
            "username":
            request.username,

            "password":
            request.password,
        }
    )

    if not user:
        return {
            "message":
            "Invalid username or password"
        }

    return {
        "message":
        "Login successful",

        "user_id":
        user["user_id"],
    }

@router.post("/{user_id}/onboarding-preferences")
def save_onboarding_preferences(
    user_id: str,
    request:
    OnboardingPreferencesRequest
):

    users_collection.update_one(
        {
            "user_id":
            user_id
        },
        {
            "$set": {
                "onboarding_preferences":
                request.preferences
            }
        }
    )

    return {
        "message":
        "Onboarding preferences saved",

        "user_id":
        user_id,
    }


@router.get("/{user_id}/onboarding-preferences")
def get_onboarding_preferences(
    user_id: str
):

    user = users_collection.find_one(
        {
            "user_id":
            user_id
        }
    )

    if not user:
        return {
            "message":
            "User not found"
        }

    return {
        "user_id":
        user_id,

        "preferences":
        user.get(
            "onboarding_preferences",
            {}
        ),
    }

@router.post("/restaurants/{restaurant_id}/like")
def like_restaurant(
    restaurant_id: str,
    request:
    RestaurantInteractionRequest
):
    user_id = request.user_id

    user_interactions_collection.update_one(
        {
            "user_id":
            user_id
        },
        {
            "$addToSet": {
                "liked_restaurants":
                restaurant_id
            }
        },
        upsert=True
    )

    return {
        "message":
        "Restaurant liked",

        "user_id":
        user_id,

        "restaurant_id":
        restaurant_id,
    }


@router.delete("/restaurants/{restaurant_id}/like")
def unlike_restaurant(
    restaurant_id: str,
    request:
    RestaurantInteractionRequest
):
    user_id = request.user_id

    user_interactions_collection.update_one(
        {
            "user_id":
            user_id
        },
        {
            "$pull": {
                "liked_restaurants":
                restaurant_id
            }
        }
    )

    return {
        "message":
        "Restaurant unliked",

        "user_id":
        user_id,

        "restaurant_id":
        restaurant_id,
    }


@router.post("/{user_id}/restaurants/{restaurant_id}/save")
def save_restaurant(
    user_id: str,
    restaurant_id: str
):

    user_interactions_collection.update_one(
        {
            "user_id":
            user_id
        },
        {
            "$addToSet": {
                "saved_restaurants":
                restaurant_id
            }
        },
        upsert=True
    )

    return {
        "message":
        "Restaurant saved",

        "user_id":
        user_id,

        "restaurant_id":
        restaurant_id,
    }


@router.post("/{user_id}/restaurants/{restaurant_id}/view")
def record_restaurant_view(
    user_id: str,
    restaurant_id: str
):

    user_interactions_collection.update_one(
        {
            "user_id":
            user_id
        },
        {
            "$addToSet": {
                "viewed_restaurants":
                restaurant_id
            }
        },
        upsert=True
    )

    return {
        "message":
        "Restaurant view recorded",

        "user_id":
        user_id,

        "restaurant_id":
        restaurant_id,
    }

@router.get("/{user_id}/offline-likes")
def get_user_offline_likes(
    user_id: str
):

    if user_id not in user_id_to_index:
        return {
            "user_id":
            user_id,

            "offline_likes":
            []
        }

    user_idx = user_id_to_index[user_id]
    user_row = user_item_matrix[user_idx]

    liked_indices = user_row.nonzero()[1]

    offline_likes = [
        index_to_item_id[index]
        for index in liked_indices
    ]

    return {
        "user_id":
        user_id,

        "offline_likes":
        offline_likes
    }

@router.get("/{user_id}/online-likes")
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

@router.get("/{user_id}/augmented-likes")
def get_augmented_likes(
    user_id: str
):

    offline_response = get_user_offline_likes(
        user_id
    )

    online_response = get_user_online_likes(
        user_id
    )

    offline_likes = set(
        offline_response["offline_likes"]
    )

    online_likes = set(
        online_response["online_likes"]
    )

    all_likes = list(
        offline_likes.union(
            online_likes
        )
    )

    return {
        "user_id":
        user_id,

        "offline_likes":
        list(offline_likes),

        "online_likes":
        list(online_likes),

        "augmented_likes":
        all_likes
    }

#Test db
@router.get("/test-db")
def test_db():
    return {
        "count":
        users_collection.count_documents({})
    }