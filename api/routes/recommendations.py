from fastapi import APIRouter, HTTPException

from api.ml.cb_recommender import (
    recommend_similar_restaurants,
)

from api.ml.cf_recommender import (
    recommend_for_user_cf,
)

from api.services.recommendation_service import (
    get_hybrid_recommendations_for_user,
    get_popular_restaurants,
    get_popular_by_category,
    get_user_onboarding_recommendations,
    get_hybrid_recommendations_for_user,
)

from api.schemas.group_schema import (
    GroupRecommendationRequest,
)

from api.services.groups_service import (
    get_group_cf_recommendations_service,
    get_group_cb_recommendations_service,
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
                "items": get_popular_by_category(category="cafe", per_page=top_k)
            },
            {
                "id": "popular_sushi",
                "title": "Popular Sushi",
                "items": get_popular_by_category(category="sushi", per_page=top_k)
            },
            {
                "id": "popular_italian",
                "title": "Popular Italian",
                "items": get_popular_by_category(category="italian", per_page=top_k)
            },
            {
                "id": "popular_dessert",
                "title": "Popular Desserts",
                "items": get_popular_by_category(category="dessert", per_page=top_k)
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
    return get_hybrid_recommendations_for_user(
        user_id=user_id,
        top_k=top_k
    )

@router.post("/cf/group")
def get_group_cf_recommendations(request: GroupRecommendationRequest):
    if not request.user_ids:
        raise HTTPException(status_code=400, detail="user_ids cannot be empty")

    return get_group_cf_recommendations_service(
        user_ids=request.user_ids,
        top_k=request.top_k,
        per_user_k=request.per_user_k,
        filters=request.filters,
    )


@router.post("/cb/group")
def get_group_cb_recommendations(request: GroupRecommendationRequest):

    if not request.user_ids:
        raise HTTPException(status_code=400, detail="user_ids cannot be empty")

    return get_group_cb_recommendations_service(
        user_ids=request.user_ids,
        top_k=request.top_k,
        per_user_k=request.per_user_k,
        filters=request.filters,
    )
