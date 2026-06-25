from api.ml.cf_recommender import recommend_for_group_cf
from api.ml.cb_recommender import recommend_for_group_cb
from api.db.restaurant_repository import (
    build_online_likes_by_user,
    get_filtered_restaurants_repo,
)


def get_group_cf_recommendations_service(
    user_ids,
    top_k=10,
    per_user_k=50,
    filters=None,
):

    candidate_gmap_ids = None

    if filters:
        filtered_restaurants = get_filtered_restaurants_repo(
            **filters,
        )
        
        candidate_gmap_ids = {
            restaurant["gmap_id"] for restaurant in filtered_restaurants
        }

    online_likes_by_user = build_online_likes_by_user(user_ids=user_ids)

    recommendations = recommend_for_group_cf(
        user_ids=user_ids,
        top_k=top_k,
        per_user_k=per_user_k,
        candidate_gmap_ids=candidate_gmap_ids,
        online_likes_by_user=online_likes_by_user,
    )

    return {
        "recommendations": recommendations,
    }


def get_group_cb_recommendations_service(
    user_ids,
    top_k=10,
    per_user_k=50,
    min_rating=3,
    filters=None,
):

    candidate_gmap_ids = None

    if filters:
        filtered_restaurants = get_filtered_restaurants_repo(
            **filters,
        )
        
        candidate_gmap_ids = {
            restaurant["gmap_id"] for restaurant in filtered_restaurants
        }

    online_likes_by_user = build_online_likes_by_user(user_ids=user_ids)

    recommendations = recommend_for_group_cb(
        user_ids=user_ids,
        top_k=top_k,
        per_user_k=per_user_k,
        min_rating=min_rating,
        candidate_gmap_ids=candidate_gmap_ids,
        online_likes_by_user=online_likes_by_user,
    )

    return {
        "recommendations": recommendations,
    }
