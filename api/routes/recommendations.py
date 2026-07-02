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


def _dedupe_recommendations(recommendations):
    seen = set()
    unique = []

    for recommendation in recommendations:
        gmap_id = recommendation.get("gmap_id")
        if not gmap_id or gmap_id in seen:
            continue

        seen.add(gmap_id)
        unique.append(recommendation)

    return unique


def _with_fallbacks(primary, fallback, ultimate_fallback, top_k):
    recommendations = primary or fallback or ultimate_fallback or []
    return _dedupe_recommendations(recommendations)[:top_k]


def _get_nearby_candidate_gmap_ids(coordinates):
    if (
        not coordinates
        or len(coordinates) != 2
        or coordinates[0] is None
        or coordinates[1] is None
    ):
        return None

    long = float(coordinates[0])
    lat = float(coordinates[1])

    for radius_km in [15, 30, 50, 100]:
        candidates = extract_gmap_ids(
            get_filtered_restaurants_repo(
                latitude=lat,
                longitude=long,
                radius_km=radius_km,
                limit=250,
            )
        )

        if candidates:
            print(f"Near You candidates={len(candidates)} radius_km={radius_km}")
            return candidates

    print("Near You candidates=0 after radius expansion")
    return []


def _get_mealtime_candidate_gmap_ids():
    meal_time = get_meal_time_string()
    dining_options = list({meal_time, meal_time.title()})

    candidates = extract_gmap_ids(
        get_filtered_restaurants_repo(
            dining_options=dining_options,
            limit=250,
        )
    )

    print(f"Meal-time candidates={len(candidates)} dining_options={dining_options}")
    return candidates


@router.get("/home-carousels")
def get_home_carousels(user_id: str = "default_user", top_k: int = 25):
    """
    Returns dynamically structured carousels for the homepage matching the frontend layout. Specific for a user.
    """
    start = time.perf_counter()
    user_profile = get_user_by_id(user_id)
    user_location = user_profile.get("location", {})
    coordinates = user_location.get("coordinates")
    print(time.perf_counter() - start)
    candidate_gmap_ids_by_radius = _get_nearby_candidate_gmap_ids(coordinates)
        
    candidate_gmap_ids_by_mealtime = _get_mealtime_candidate_gmap_ids()
    candidate_gmap_ids_by_hidden_gems = extract_gmap_ids(
        get_filtered_restaurants_repo(
            min_rating=4.5,
            max_reviews=30,
            limit=250,
        )
    )

    is_cold_start = get_user_augmented_likes(user_id) == 0
    onboarding_candidate_gmap_ids = None
    hybrid_scores = None
    if is_cold_start:
        print("User has no augmented likes, fetching onboarding candidate gmap_ids")
        onboarding_candidate_gmap_ids = get_onboarding_candidate_gmap_ids(user_id)
    else:
        hybrid_scores = get_hybrid_scores_for_user(user_id)

    start = time.perf_counter()
    recommended = get_hybrid_recommendations_for_user(
        user_id,
        top_k=top_k,
        onboarding_candidate_gmap_ids=onboarding_candidate_gmap_ids,
        hybrid_scores=hybrid_scores,
    )
    ultimate_fallback = get_popular_restaurants(top_k=top_k)
    recommended = _with_fallbacks(
        primary=recommended,
        fallback=None,
        ultimate_fallback=ultimate_fallback,
        top_k=top_k,
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
    popular_near_you = _with_fallbacks(
        primary=popular_near_you,
        fallback=recommended,
        ultimate_fallback=ultimate_fallback,
        top_k=top_k,
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
    popular_at_this_hour = _with_fallbacks(
        primary=popular_at_this_hour,
        fallback=recommended,
        ultimate_fallback=ultimate_fallback,
        top_k=top_k,
    )
    print(f"Popular Now: {time.perf_counter() - start:.2f}s")

    start = time.perf_counter()
    you_might_like = get_hybrid_recommendations_for_user(
        user_id,
        top_k=2 * top_k,
        onboarding_candidate_gmap_ids=onboarding_candidate_gmap_ids,
        hybrid_scores=hybrid_scores,
    )[top_k:]
    you_might_like = _with_fallbacks(
        primary=you_might_like,
        fallback=recommended,
        ultimate_fallback=ultimate_fallback,
        top_k=top_k,
    )
    print(f"You Might Like: {time.perf_counter() - start:.2f}s")

    start = time.perf_counter()
    hidden_gems = get_hybrid_recommendations_for_user(
        user_id,
        top_k=top_k,
        candidate_gmap_ids=candidate_gmap_ids_by_hidden_gems,
        onboarding_candidate_gmap_ids=onboarding_candidate_gmap_ids,
        hybrid_scores=hybrid_scores,
    )
    hidden_gems = _with_fallbacks(
        primary=hidden_gems,
        fallback=recommended,
        ultimate_fallback=ultimate_fallback,
        top_k=top_k,
    )
    print(f"Hidden Gems: {time.perf_counter() - start:.2f}s")  
    return {
        "carousels": [
            {
                "id": "recommended_for_you",
                "title": "Recommended For You",
                "items": [format_restaurant_for_frontend(r) for r in recommended]
            },
            {
                "id": "popular_near_you",
                "title": "Popular Near You",
                "items": [format_restaurant_for_frontend(r) for r in popular_near_you]
            },
            {
                "id": "popular_at_this_hour",
                "title": "Popular at this hour",
                "items": [format_restaurant_for_frontend(r) for r in popular_at_this_hour]
            },
            {
                "id": "you_might_like",
                "title": "You might like",
                "items": [format_restaurant_for_frontend(r) for r in you_might_like]
            },
            {
                "id": "hidden_gems",
                "title": "Hidden gems",
                "items": [format_restaurant_for_frontend(r) for r in hidden_gems]
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
