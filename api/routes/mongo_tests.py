from fastapi import APIRouter, HTTPException, Query
from api.ml.cf_recommender import (
    get_popular_restaurants,
)

from api.db.mongo import (
    users_collection,
)
from api.db.restaurant_repository import get_filtered_restaurants_repo

router = APIRouter(prefix="/mongo", tags=["mongo tests"])


@router.get("/test/getK/{k}")
def get_k_popular_restaurants(
    k: int,
):
    return  {
        "result":get_popular_restaurants(
        k,
    ) }


@router.get("/test/filter/{k}")
def get_filtered_restaurants(
    k: int,
    categories: list[str] = Query(default=[]),
    establishment_types: list[str] = Query(default=[]),
    meal_types: list[str] = Query(default=[]),
    dining_styles: list[str] = Query(default=[]),
    popular_items: list[str] = Query(default=[]),
    dietary_preferences: list[str] = Query(default=[]),
    vibe: list[str] = Query(default=[]),
    is_accessible: bool | None = Query(default=None),
):
    return {
        "result": get_filtered_restaurants_repo(
            limit=k,
            categories=categories or None,
            establishment_types=establishment_types or None,
            meal_types=meal_types or None,
            dining_styles=dining_styles or None,
            popular_items=popular_items or None,
            dietary_preferences=dietary_preferences or None,
            vibe=vibe or None,
            is_accessible=is_accessible,
        )
    }


@router.get("/users")
def get_all_users():
    users = users_collection.find(
        {},
        {
            "_id": 0,
            "user_id": 1,
            "username": 1,
            "email": 1,
        }
    )

    return list(users)