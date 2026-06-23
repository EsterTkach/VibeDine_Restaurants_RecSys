from src.cf_recommender import recommend_for_group_cf


def get_group_recommendations_service(
    user_ids,
    top_k=10,
    per_user_k=50,
    filters=None,
):

    candidate_gmap_ids = FILTER(filters)         #TODO - change FILTER to esty's filtering function

    recommendations = recommend_for_group_cf(
        user_ids=user_ids,
        top_k=top_k,
        per_user_k=per_user_k,
        candidate_gmap_ids=candidate_gmap_ids,
    )

    return {
        "recommendations": recommendations,
    }