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
    get_hybrid_recommendations_for_group,
)

from api.utils.utils import (
    format_restaurant_for_frontend,
    get_meal_time_string,
    extract_gmap_ids
)

from api.db.restaurant_repository import (
    get_filtered_restaurants_repo,
    get_user_by_id
)

router = APIRouter(
    prefix="/recommend",
    tags=["Recommendations"]
)

@router.get("/home-carousels")
def get_home_carousels(user_id: str = "default_user", top_k: int = 25):
    """
    Returns dynamically structured carousels for the homepage matching the frontend layout. Specific for a user.
    """
    user_profile = get_user_by_id(user_id)
    user_location = user_profile.get("location", {})
    coordinates = user_location.get("coordinates", [None, None])
    long = coordinates[0]
    lat = coordinates[1]
    candidate_gmap_ids_by_radius = extract_gmap_ids(get_filtered_restaurants_repo(latitude=float(lat), longitude=float(long)))
    candidate_gmap_ids_by_mealtime = extract_gmap_ids(get_filtered_restaurants_repo(dining_options=get_meal_time_string()))
    candidate_gmap_ids_by_hidden_gems = extract_gmap_ids(get_filtered_restaurants_repo(min_rating=4.5, max_reviews=30))

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
                "items": [format_restaurant_for_frontend(r) for r in get_hybrid_recommendations_for_user(user_id, top_k=top_k, candidate_gmap_ids=candidate_gmap_ids_by_radius)]
            },
            {
                "id": "popular_at_this_hour",
                "title": "Popular at this hour",
                "items": [format_restaurant_for_frontend(r) for r in get_hybrid_recommendations_for_user(user_id, top_k=top_k, candidate_gmap_ids=candidate_gmap_ids_by_mealtime)]
            },
            {
                "id": "you_might_like",
                "title": "You might like",
                "items": [format_restaurant_for_frontend(r) for r in get_hybrid_recommendations_for_user(user_id, top_k= 2*top_k)[top_k:]]
            },
            {
                "id": "hidden_gems",
                "title": "Hidden gems",
                "items": [format_restaurant_for_frontend(r) for r in get_hybrid_recommendations_for_user(user_id, top_k=top_k, candidate_gmap_ids=candidate_gmap_ids_by_hidden_gems)]
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



@router.get("/group")
def get_group_recommendations(request: GroupRecommendationRequest):
    if not request.user_ids:
        raise HTTPException(status_code=400, detail="user_ids cannot be empty")

    return get_hybrid_recommendations_for_group(
        user_ids=request.user_ids,
        top_k=request.top_k,
        per_user_k=request.per_user_k,
        filters=request.filters,
    )

