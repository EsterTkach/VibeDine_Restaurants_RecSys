from fastapi import APIRouter, HTTPException

from api.ml.cb_recommender import (
    recommend_similar_restaurants,
)

from api.ml.cf_recommender import (
    recommend_for_user_cf,
)

from api.services.recommendation_service import (
    get_popular_restaurants,
    get_popular_by_category,
    get_recommendations,
)

router = APIRouter(
    prefix="/recommend",
    tags=["Recommendations"]
)

@router.get("/home-carousels")
def get_home_carousels(top_k: int = 10):
    """
    Returns static, non-personalized carousels for the homepage separated by category.
    """
    return {
        "carousels": [
            {
                "id": "popular_restaurants",
                "title": "Popular Restaurants",
                "items": get_popular_restaurants(top_k=top_k)
            },
            {
                "id": "popular_cafes",
                "title": "Popular Cafes",
                # Make sure the string here matches exactly how it's stored in MongoDB
                "items": get_popular_by_category(category="Cafe", top_k=top_k)
            },
            {
                "id": "popular_sushi",
                "title": "Popular Sushi",
                "items": get_popular_by_category(category="Sushi", top_k=top_k)
            },
            {
                "id": "popular_italian",
                "title": "Popular Italian",
                "items": get_popular_by_category(category="Italian", top_k=top_k)
            },
        ]
    }

# Popular restaurants endpoint - returns top 10 popular restaurants similar to the original restaurant based on overall ratings and number of reviews
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