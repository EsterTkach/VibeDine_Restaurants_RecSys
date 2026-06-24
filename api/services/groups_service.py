from src.cf_recommender import recommend_for_group_cf
from src.cb_recommender import recommend_for_group_cb


def get_group_cf_recommendations_service(
    user_ids,
    top_k=10,
    per_user_k=50,
    filters=None,
):

    # TODO - change FILTER to esty's filtering function

    candidate_gmap_ids = None

    if filters:
        filtered_restaurants = FILTER(filters)
        candidate_gmap_ids = {r["gmap_id"] for r in filtered_restaurants}

    recommendations = recommend_for_group_cf(
        user_ids=user_ids,
        top_k=top_k,
        per_user_k=per_user_k,
        candidate_gmap_ids=candidate_gmap_ids,
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

    # TODO - change FILTER to esty's filtering function

    candidate_gmap_ids = None

    if filters:
        filtered_restaurants = FILTER(filters)
        candidate_gmap_ids = {r["gmap_id"] for r in filtered_restaurants}

    recommendations = recommend_for_group_cb(
        user_ids=user_ids,
        top_k=top_k,
        per_user_k=per_user_k,
        min_rating=min_rating,
        candidate_gmap_ids=candidate_gmap_ids,
    )

    return {
        "recommendations": recommendations,
    }
