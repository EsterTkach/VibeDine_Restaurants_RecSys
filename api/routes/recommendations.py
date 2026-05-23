from fastapi import APIRouter, HTTPException

from src.cb_recommender import (
    recommend_similar_restaurants,
)

from src.cf_recommender import (
    recommend_for_user_cf,
)

from api.services.recommendation_service import (
    get_popular_restaurants,
    get_recommendations,
)

router = APIRouter(
    prefix="/recommend",
    tags=["Recommendations"]
)


@router.get("/cb/{restaurant_name}")
def get_similar_restaurants(
    restaurant_name: str,
    top_k: int = 10
):
    results = recommend_similar_restaurants(
        restaurant_name=restaurant_name,
        top_k=top_k
    )

    if not results:
        raise HTTPException(
            status_code=404,
            detail="Restaurant not found"
        )

    return {
        "restaurant": restaurant_name,
        "recommendations": results
    }


@router.get("/cf/{user_id}")
def get_user_recommendations(
    user_id: str,
    top_k: int = 10
):
    return get_recommendations(
        user_id=user_id,
        top_k=top_k
    )