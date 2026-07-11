from fastapi import (
    APIRouter,
    HTTPException,
    Query
)

from uuid import uuid4

from api.db.mongo import (
    users_collection,
    restaurants_collection
)

from api.schemas.user import (
    UserSignupRequest,
    UserLoginRequest,
    OnboardingPreferencesRequest,
    RestaurantInteractionRequest,
    AddFriendRequest
)

from api.ml.cf_recommender import get_user_offline_likes

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
    new_user_id = str(uuid4())

    user = {
        "_id": new_user_id,
        "user_id": new_user_id,
        "name": request.name,
        "username": request.username,
        "password": request.password,
        "liked_restaurants": [],
        "friends": [],
        "preferences": [],
        "location": request.location.model_dump(),
        "avatar_index": request.avatar_index,
    }

    existing_user = users_collection.find_one({"username": request.username})
    if existing_user:
        raise HTTPException(status_code=409, detail="Username already exists")

    users_collection.insert_one(user)

    return {
        "message": "User created",
        "user_data": {
            "user_id": user["user_id"],
            "username": user["username"],
            "avatar_index": user["avatar_index"],
            "name": user["name"],
        },
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
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    return {
        "message": "Login successful",
        "user_data": {
            "user_id": user["user_id"],
            "username": user["username"],
            "avatar_index": user["avatar_index"],
            "name": user["name"],
        },
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

    users_collection.update_one(
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

    users_collection.update_one(
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


@router.get("/{user_id}/restaurants/likes/online")
def get_online_liked_restaurants(user_id: str):
    online_likes_restaurants = get_user_online_liked_restaurants(user_id)

    return {"user_id": user_id, "online_liked_restaurants": online_likes_restaurants}


@router.get("/{user_id}/restaurants/likes/offline")
def get_offline_liked_restaurants(user_id: str):
    offline_likes_ids = get_user_offline_likes(user_id)

    offline_likes_restaurants = list(
        restaurants_collection.find(
            {"gmap_id": {"$in": offline_likes_ids["offline_likes"]}},
            {"_id": 0, "gmap_id": 1, "name": 1, "image_url": 1},
        )
    )

    return {"user_id": user_id, "offline_liked_restaurants": offline_likes_restaurants}
