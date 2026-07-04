from fastapi import APIRouter, HTTPException
import time

from api.schemas.restaurant_schema import FilterRequest

from api.ml.cb_recommender import (
    compute_cb_scores,
    recommend_similar_restaurants,
)

from api.ml.cf_recommender import (
    compute_cf_scores,
)

from api.services.recommendation_service import (
    get_hybrid_recommendations_for_user,
    get_hybrid_scores_for_user,
    get_onboarding_candidate_gmap_ids,
    get_popular_restaurants,
    get_popular_by_category,
    get_user_augmented_likes,
    get_user_onboarding_recommendations,
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
    extract_gmap_ids,
    enrich_restaurants
)

from api.db.restaurant_repository import (
    get_filtered_restaurants_repo,
    get_user_by_id,
    get_restaurants_by_gmap_ids
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
    start = time.perf_counter()
    user_profile = get_user_by_id(user_id)
    user_location = user_profile.get("location", {})
    coordinates = user_location.get("coordinates")

    candidate_gmap_ids_by_radius = None
    if (
        coordinates 
        and len(coordinates) == 2
        and coordinates[0] is not None
        and coordinates[1] is not None
    ):
        long = coordinates[0]
        lat = coordinates[1]
        candidate_gmap_ids_by_radius = extract_gmap_ids(
            get_filtered_restaurants_repo(
                latitude=float(lat),
                  longitude=float(long),
                  )
                )
        
    candidate_gmap_ids_by_mealtime = extract_gmap_ids(get_filtered_restaurants_repo(dining_options=get_meal_time_string()))
    candidate_gmap_ids_by_hidden_gems = extract_gmap_ids(get_filtered_restaurants_repo(min_rating=4.5, max_reviews=30))
    is_cold_start = get_user_augmented_likes(user_id) == 0
    onboarding_candidate_gmap_ids = None
    hybrid_scores = None
    print(time.perf_counter() - start)

    start = time.perf_counter()
    if is_cold_start:
        print("User has no augmented likes, fetching onboarding candidate gmap_ids")
        onboarding_candidate_gmap_ids = get_onboarding_candidate_gmap_ids(user_id)
    else:
        hybrid_scores = get_hybrid_scores_for_user(user_id)
    print(f"hybrid scores run time: {time.perf_counter() - start:.2f}s")

    start = time.perf_counter()
    recommended = get_hybrid_recommendations_for_user(
        user_id,
        top_k=top_k,
        onboarding_candidate_gmap_ids=onboarding_candidate_gmap_ids,
        hybrid_scores=hybrid_scores,
    )
    print(f"Recommended: {time.perf_counter() - start:.2f}s")

    start = time.perf_counter()
    popular_near_you = get_hybrid_recommendations_for_user(
        user_id,
        top_k=top_k,
        candidate_gmap_ids=candidate_gmap_ids_by_radius,
        onboarding_candidate_gmap_ids=onboarding_candidate_gmap_ids,
        hybrid_scores=hybrid_scores,
    )
    print(f"Near You: {time.perf_counter() - start:.2f}s")

    start = time.perf_counter()
    popular_at_this_hour = get_hybrid_recommendations_for_user(
        user_id,
        top_k=top_k,
        candidate_gmap_ids=candidate_gmap_ids_by_mealtime,
        onboarding_candidate_gmap_ids=onboarding_candidate_gmap_ids,
        hybrid_scores=hybrid_scores,
    )
    print(f"Popular Now: {time.perf_counter() - start:.2f}s")

    start = time.perf_counter()
    you_might_like = get_hybrid_recommendations_for_user(
        user_id,
        top_k=2 * top_k,
        onboarding_candidate_gmap_ids=onboarding_candidate_gmap_ids,
        hybrid_scores=hybrid_scores,
    )[top_k:]
    print(f"You Might Like: {time.perf_counter() - start:.2f}s")

    start = time.perf_counter()
    hidden_gems = get_hybrid_recommendations_for_user(
        user_id,
        top_k=top_k,
        candidate_gmap_ids=candidate_gmap_ids_by_hidden_gems,
        onboarding_candidate_gmap_ids=onboarding_candidate_gmap_ids,
        hybrid_scores=hybrid_scores,
    )
    print(f"Hidden Gems: {time.perf_counter() - start:.2f}s")

    start = time.perf_counter()

    # 1. Gather every unique gmap_id from all carousels
    all_ml_results = recommended + popular_near_you + popular_at_this_hour + you_might_like + hidden_gems
    unique_gmap_ids = list({r.get("gmap_id") for r in all_ml_results if r.get("gmap_id")})

    # 2. Call your clean repository helper
    full_docs_dict = get_restaurants_by_gmap_ids(unique_gmap_ids)
    
    print(f"Batch DB Fetch: {time.perf_counter() - start:.2f}s")

    return {
        "carousels": [
            {
                "id": "recommended_for_you",
                "title": "Recommended For You",
                "items": [format_restaurant_for_frontend(r) for r in enrich_restaurants(recommended, full_docs_dict)]
            },
            {
                "id": "popular_near_you",
                "title": "Popular Near You",
                "items": [format_restaurant_for_frontend(r) for r in enrich_restaurants(popular_near_you, full_docs_dict)]
            },
            {
                "id": "popular_at_this_hour",
                "title": "Popular at this hour",
                "items": [format_restaurant_for_frontend(r) for r in enrich_restaurants(popular_at_this_hour, full_docs_dict)]
            },
            {
                "id": "you_might_like",
                "title": "You might like",
                "items": [format_restaurant_for_frontend(r) for r in enrich_restaurants(you_might_like, full_docs_dict)]
            },
            {
                "id": "hidden_gems",
                "title": "Hidden gems",
                "items": [format_restaurant_for_frontend(r) for r in enrich_restaurants(hidden_gems, full_docs_dict)]
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

@router.post("/vibe-match/{user_id}")
def get_vibe_match_recommendations(
    user_id: str,
    filters: FilterRequest
):
    filtered_restaurants = get_filtered_restaurants_repo(
        categories=filters.categories,
        accessibility=filters.accessibility,
        service_options=filters.service_options,
        atmosphere=filters.atmosphere,
        dining_options=filters.dining_options,
        crowd=filters.crowd,
        offerings=filters.offerings or filters.dietary_restrictions,
        price=filters.price,
        latitude=filters.latitude,
        longitude=filters.longitude,
        radius_km=filters.radius_km,
        min_rating=filters.min_rating,
        min_reviews=filters.min_reviews,
        max_reviews=filters.max_reviews,
        limit=100
    )

    candidate_gmap_ids = extract_gmap_ids(
        filtered_restaurants
    )

    recommendations = get_hybrid_recommendations_for_user(
        user_id=user_id,
        top_k=filters.top_k,
        candidate_gmap_ids=candidate_gmap_ids
    )

    return {
        "recommendation_type": "vibe_match",
        "filters": filters.dict(),
        "recommendations": [
            format_restaurant_for_frontend(r)
            for r in recommendations
        ]
    }