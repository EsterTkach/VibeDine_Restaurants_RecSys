from fastapi import (
    APIRouter,
    HTTPException,
    Query
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
    RestaurantInteractionRequest,
    AddFriendRequest
)

from api.services.users_service import (get_user_online_liked_restaurants,)
from api.services.hybrid_cache import invalidate as invalidate_hybrid_cache

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
    existing_user = users_collection.find_one(
    {"username": request.username})
    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="Username already exists"
        )

    users_collection.insert_one(
        user
    )
    print("Inserted user:", user)

    return {
        "message":
        "User created",
        "user_id":
        user["user_id"],
        "username":
        user["username"],
    }

@router.post("/login")
def login(
    request:
    UserLoginRequest
):
    print("Username:", request.username)
    print("Password:", request.password)

    user = users_collection.find_one(
        {
            "username":
            request.username,

            "password":
            request.password,
        }
    )
    print("User found:", user)

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    return {
        "message":
        "Login successful",

        "user_id":
        user["user_id"],
        "username":
        user["username"],
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
                request.preferences.model_dump()
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

    invalidate_hybrid_cache(user_id)

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

    invalidate_hybrid_cache(user_id)

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


@router.get("/search")
def search_users(
    username: str = Query(..., min_length=1),
    user_id: str = Query(...)
):
    results = users_collection.find(
        {
            "username": {"$regex": username, "$options": "i"},
            "user_id": {"$ne": user_id}
        },
        {"_id": 0, "user_id": 1, "name": 1, "username": 1, "avatar_index": 1}
    ).limit(20)
    return [
        {
            "user_id": u["user_id"],
            "name": u.get("name") or u.get("username", ""),
            "username": u.get("username", ""),
            "avatar_index": u.get("avatar_index", 0),
        }
        for u in results
    ]


@router.get("/{user_id}/friends")
def get_friends(user_id: str):
    user = users_collection.find_one({"user_id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    friend_ids = user.get("friends", [])
    if not friend_ids:
        return []

    friends = users_collection.find(
        {"user_id": {"$in": friend_ids}},
        {"_id": 0, "user_id": 1, "name": 1, "username": 1, "avatar_index": 1}
    )
    return [
        {
            "user_id": f["user_id"],
            "name": f.get("name") or f.get("username", ""),
            "username": f.get("username", ""),
            "avatar_index": f.get("avatar_index", 0),
        }
        for f in friends
    ]


@router.post("/{user_id}/friends")
def add_friend(user_id: str, request: AddFriendRequest):
    result = users_collection.update_one(
        {"user_id": user_id},
        {"$addToSet": {"friends": request.friend_id}}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found — please log out and log in again")
    return {"message": "Friend added"}


@router.delete("/{user_id}/friends/{friend_id}")
def remove_friend(user_id: str, friend_id: str):
    result = users_collection.update_one(
        {"user_id": user_id},
        {"$pull": {"friends": friend_id}}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "Friend removed"}


@router.get("/{user_id}/restaurants/liked")
def get_liked_restaurants(user_id: str):
    print('user_id: ', user_id)
    liked_restaurants = get_user_online_liked_restaurants(user_id)
    print('liked_restaurants: ', liked_restaurants)

    return {
        "user_id": user_id,
        "liked_restaurants": liked_restaurants
    }
