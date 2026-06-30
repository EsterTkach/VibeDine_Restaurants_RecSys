from fastapi import (
    APIRouter,
    HTTPException
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

from api.services.users_service import (get_user_online_liked_restaurants,)

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


@router.get("/{user_id}/restaurants/liked")
def get_liked_restaurants(user_id: str):
    print('user_id: ', user_id)
    liked_restaurants = get_user_online_liked_restaurants(user_id)
    print('liked_restaurants: ', liked_restaurants)

    return {
        "user_id": user_id,
        "liked_restaurants": liked_restaurants
    }
