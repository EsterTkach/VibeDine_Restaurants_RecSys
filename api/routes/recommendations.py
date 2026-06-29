from fastapi import APIRouter, HTTPException

from api.ml.cb_recommender import (
    compute_cb_scores,
    recommend_similar_restaurants,
)

from api.ml.cf_recommender import (
    compute_cf_scores,
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

from api.utils.utils import (
    format_restaurant_for_frontend
)

router = APIRouter(
    prefix="/recommend",
    tags=["Recommendations"]
)

@router.get("/home-carousels")
def get_home_carousels(user_id: str = "default_user", top_k: int = 10):
    """
    Returns dynamically structured carousels for the homepage matching the frontend layout. Specific for a user.
    """
    return {
        "carousels": [
            {
                "id": "recommended_for_you",
                "title": "Recommended For You",
                "items": [format_restaurant_for_frontend(r) for r in get_hybrid_recommendations_for_user(user_id)]
            },
            {
                "id": "popular_near_you",
                "title": "Popular Near You",
                "items": get_popular_restaurants(top_k=top_k)
            },
            {
                "id": "popular_at_this_hour",
                "title": "Popular at this hour",
                # TODO: Write a small utility to check the current hour on the server 
                # and return specific meal categories (e.g., Breakfast/Dinner tags)
                "items": get_popular_by_category(category="cafe", per_page=top_k)
            },
            {
                "id": "you_might_like",
                "title": "You might like",
                # TODO: Connect this to your Content-Based Recommender (cb_recommender)
                # base recommendations on items the user previously clicked or liked
                "items": get_popular_restaurants(top_k=top_k)
            },
            {
                "id": "hidden_gems",
                "title": "Hidden gems",
                # TODO: Add a service layer function that queries MongoDB for:
                # high overall rating (avg_rating >= 4.2) but low review count (num_of_reviews < 50)
                "items": get_popular_restaurants(top_k=top_k)
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
    # return get_hybrid_recommendations_for_user(
    #     user_id=user_id,
    #     top_k=top_k
    # )
    return get_hybrid_recommendations_for_user(user_id)

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
