from collections import defaultdict

from api.db.restaurant_repository import get_filtered_restaurants_repo
from api.services.recommendation_service import (
    get_hybrid_recommendations_for_user,
    get_user_augmented_likes,
)


def _filters_to_dict(filters):
    if filters is None:
        return {}

    if hasattr(filters, "model_dump"):
        return filters.model_dump(exclude_none=True)

    if hasattr(filters, "dict"):
        return filters.dict(exclude_none=True)

    return filters


def _get_non_cold_start_user_ids(user_ids):
    return [
        user_id
        for user_id in user_ids
        if get_user_augmented_likes(user_id) > 0
    ]


def aggregate_group_recommendations(user_ids, recommendations_by_user, top_k=10):
    if not user_ids:
        print("Group is empty")
        return []

    restaurant_scores = defaultdict(
        lambda: {
            "name": None,
            "score_sum": 0.0,
            "count": 0,
        }
    )

    for user_id in user_ids:
        user_recs = recommendations_by_user.get(user_id, [])

        for rec in user_recs:
            if "hybrid_score" not in rec:
                continue

            gmap_id = rec["gmap_id"]
            restaurant_scores[gmap_id]["name"] = rec["name"]
            restaurant_scores[gmap_id]["score_sum"] += rec["hybrid_score"]
            restaurant_scores[gmap_id]["count"] += 1

    group_recommendations = []
    group_size = len(user_ids)

    for gmap_id, data in restaurant_scores.items():
        avg_score = data["score_sum"] / data["count"]
        coverage = data["count"] / group_size
        group_score = avg_score * coverage

        group_recommendations.append(
            {
                "gmap_id": gmap_id,
                "name": data["name"],
                "avg_hybrid_score": round(float(avg_score), 3),
                "users_supported": data["count"],
                "coverage": round(float(coverage), 3),
                "group_score": round(float(group_score), 3),
            }
        )

    group_recommendations.sort(
        key=lambda x: x["group_score"],
        reverse=True,
    )

    return group_recommendations[:top_k]


def get_hybrid_recommendations_for_group_with_user_candidates(
    user_ids,
    candidate_gmap_ids_by_user,
    top_k=10,
    per_user_k=50,
):
    user_ids = _get_non_cold_start_user_ids(user_ids)
    if not user_ids:
        print("No non-cold-start users in group")
        return []

    recommendations_by_user = {}

    for user_id in user_ids:
        recommendations_by_user[user_id] = get_hybrid_recommendations_for_user(
            user_id=user_id,
            top_k=per_user_k,
            candidate_gmap_ids=candidate_gmap_ids_by_user.get(user_id),
        )

    return aggregate_group_recommendations(
        user_ids=user_ids,
        recommendations_by_user=recommendations_by_user,
        top_k=top_k,
    )


def get_hybrid_recommendations_for_group(
    user_ids,
    top_k=10,
    per_user_k=50,
    filters=None,
):
    """
    Generate group recommendations using the hybrid recommender.

    For each user:
    - Generate personal hybrid recommendations
    - Collect restaurant scores

    Then:
    - Average scores per restaurant
    - Multiply by coverage
    - Return Top-K group recommendations
    """
    
    if not user_ids:
        print("Group is empty")
        return []

    user_ids = _get_non_cold_start_user_ids(user_ids)
    if not user_ids:
        print("No non-cold-start users in group")
        return []
    
    candidate_gmap_ids = None

    if filters:
        filter_kwargs = _filters_to_dict(filters)
        filtered_restaurants = get_filtered_restaurants_repo(
            **filter_kwargs,
        )
        
        candidate_gmap_ids = {
            restaurant["gmap_id"] for restaurant in filtered_restaurants
        }


    recommendations_by_user = {}

    # Generate hybrid recommendations for each user
    for user_id in user_ids:
        recommendations_by_user[user_id] = get_hybrid_recommendations_for_user(
            user_id=user_id,
            top_k=per_user_k,
            candidate_gmap_ids=candidate_gmap_ids,
        )

    return aggregate_group_recommendations(
        user_ids=user_ids,
        recommendations_by_user=recommendations_by_user,
        top_k=top_k,
    )
