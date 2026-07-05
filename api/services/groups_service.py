from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed

from api.db.restaurant_repository import get_filtered_restaurants_repo
from api.ml.cf_recommender import get_popular_restaurants
from api.services.recommendation_service import (
    get_hybrid_recommendations_for_user,
    get_user_augmented_likes,
)
from api.utils.utils import format_restaurant_for_frontend


def _filters_to_dict(filters):
    if filters is None:
        return {}

    if hasattr(filters, "model_dump"):
        return filters.model_dump(exclude_none=True)

    if hasattr(filters, "dict"):
        return filters.dict(exclude_none=True)

    return filters


def _fallback_popular_recommendations(top_k=10):
    """
    Fallback for group recommendations: return popular restaurants
    formatted with group-compatible fields.
    """
    popular = get_popular_restaurants(top_k=top_k)
    fallback_results = []
    for rec in popular:
        formatted = format_restaurant_for_frontend(rec)
        fallback_results.append({
            "gmap_id": rec["gmap_id"],
            "name": rec["name"],
            "avg_rating": formatted.get("avg_rating"),
            "price": formatted.get("price"),
            "image_url": formatted.get("image_url"),
            "cuisines": [],
            "avg_hybrid_score": rec.get("popularity_score", 0.0),
            "users_supported": 0,
            "coverage": 0.0,
            "group_score": rec.get("popularity_score", 0.0),
        })
    return fallback_results[:top_k]


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
            "avg_rating": None,
            "price": None,
            "image_url": None,
            "cuisines": [],
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
            restaurant_scores[gmap_id]["avg_rating"] = rec.get("avg_rating")
            restaurant_scores[gmap_id]["price"] = rec.get("price")
            restaurant_scores[gmap_id]["image_url"] = rec.get("image_url")
            restaurant_scores[gmap_id]["cuisines"] = rec.get("cuisines", [])
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
                "avg_rating": data["avg_rating"],
                "price": data["price"],
                "image_url": data["image_url"],
                "cuisines": data["cuisines"],
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
        print("No non-cold-start users in group, returning popular fallback")
        return _fallback_popular_recommendations(top_k)

    recommendations_by_user = {}

    def _fetch_with_candidates(uid):
        return uid, get_hybrid_recommendations_for_user(
            user_id=uid,
            top_k=per_user_k,
            candidate_gmap_ids=candidate_gmap_ids_by_user.get(uid),
        )

    with ThreadPoolExecutor(max_workers=len(user_ids)) as pool:
        futures = {pool.submit(_fetch_with_candidates, uid): uid for uid in user_ids}
        for future in as_completed(futures):
            uid, recs = future.result()
            recommendations_by_user[uid] = recs

    results = aggregate_group_recommendations(
        user_ids=user_ids,
        recommendations_by_user=recommendations_by_user,
        top_k=top_k,
    )

    if not results:
        print("Group aggregation returned no results, returning popular fallback")
        return _fallback_popular_recommendations(top_k)

    return results


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
        print("Group is empty, returning popular fallback")
        return _fallback_popular_recommendations(top_k)

    user_ids = _get_non_cold_start_user_ids(user_ids)
    if not user_ids:
        print("No non-cold-start users in group, returning popular fallback")
        return _fallback_popular_recommendations(top_k)
    
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

    def _fetch_for_user(uid):
        return uid, get_hybrid_recommendations_for_user(
            user_id=uid,
            top_k=per_user_k,
            candidate_gmap_ids=candidate_gmap_ids,
        )

    with ThreadPoolExecutor(max_workers=len(user_ids)) as pool:
        futures = {pool.submit(_fetch_for_user, uid): uid for uid in user_ids}
        for future in as_completed(futures):
            uid, recs = future.result()
            recommendations_by_user[uid] = recs

    results = aggregate_group_recommendations(
        user_ids=user_ids,
        recommendations_by_user=recommendations_by_user,
        top_k=top_k,
    )

    if not results:
        print("Group aggregation returned no results, returning popular fallback")
        return _fallback_popular_recommendations(top_k)

    return results
