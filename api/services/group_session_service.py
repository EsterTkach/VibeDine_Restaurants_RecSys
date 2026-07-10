from uuid import uuid4

from fastapi import HTTPException

from copy import deepcopy

from api.db.restaurant_repository import get_filtered_restaurants_repo
from api.services.groups_service import (
    _filters_to_dict,
    get_hybrid_recommendations_for_group,
    get_hybrid_recommendations_for_group_with_user_candidates,
)


PRICE_LEVELS = ["$", "$$", "$$$", "$$$$"]
DEFAULT_RADIUS_KM = 15
MIN_RADIUS_KM = 1

group_recommendation_sessions = {}


def _first_recommendation(recommendations):
    return recommendations[0] if recommendations else None


def create_group_recommendation_session(
    user_ids,
    top_k=1,
    per_user_k=50,
    filters=None,
):
    if not user_ids:
        raise HTTPException(status_code=400, detail="user_ids cannot be empty")

    original_filters = _filters_to_dict(filters)

    session_id = str(uuid4())
    group_recommendation_sessions[session_id] = {
        "session_id": session_id,
        "user_ids": user_ids,
        "filters_per_user": {user_id: deepcopy(original_filters) for user_id in user_ids},
        "excluded_restaurant_ids": set(),
    }

    recommendations = get_hybrid_recommendations_for_group(
        user_ids=user_ids,
        top_k=top_k,
        per_user_k=per_user_k,
        filters=filters,
    )

    return {
        "session_id": session_id,
        "recommendation": _first_recommendation(recommendations),
    }


def apply_group_session_feedback(
    session_id,
    current_restaurant,
    affected_user_ids,
    reason,
    top_k=1,
    per_user_k=50,
):
    session = group_recommendation_sessions.get(session_id)

    if session is None:
        raise HTTPException(status_code=404, detail="session not found")

    if not current_restaurant:
        raise HTTPException(status_code=400, detail="current_restaurant is required")

    session["excluded_restaurant_ids"].add(str(current_restaurant))

    session_user_ids = set(session["user_ids"])
    unknown_user_ids = set(affected_user_ids) - session_user_ids
    if unknown_user_ids:
        raise HTTPException(
            status_code=400,
            detail=f"unknown affected_user_ids: {sorted(unknown_user_ids)}",
        )

    for user_id in affected_user_ids:
        filters = session["filters_per_user"][user_id]

        if reason == "Too expensive":
            current_price = filters.get("max_price") or filters.get("price") or "$$$$"
            if current_price in PRICE_LEVELS and PRICE_LEVELS.index(current_price) > 0:
                new_price = PRICE_LEVELS[PRICE_LEVELS.index(current_price) - 1]
            else:
                new_price = "$"

            filters.pop("price", None)
            filters["max_price"] = new_price

        elif reason == "Too far away":
            current_radius = filters.get("radius_km") or DEFAULT_RADIUS_KM
            filters["radius_km"] = max(MIN_RADIUS_KM, current_radius / 2)

    candidate_gmap_ids_by_user = {}
    excluded_restaurant_ids = session["excluded_restaurant_ids"]

    for user_id in session["user_ids"]:
        filtered_restaurants = get_filtered_restaurants_repo(
            **session["filters_per_user"][user_id],
            limit=1000,
        )

        candidate_gmap_ids_by_user[user_id] = {
            restaurant["gmap_id"]
            for restaurant in filtered_restaurants
            if restaurant.get("gmap_id") not in excluded_restaurant_ids
        }

    recommendations = get_hybrid_recommendations_for_group_with_user_candidates(
        user_ids=session["user_ids"],
        candidate_gmap_ids_by_user=candidate_gmap_ids_by_user,
        top_k=top_k,
        per_user_k=per_user_k,
    )

    return {
        "session_id": session_id,
        "recommendation": _first_recommendation(recommendations),
    }
