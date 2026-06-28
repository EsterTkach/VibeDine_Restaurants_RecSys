from collections import defaultdict

from api.db.restaurant_repository import get_filtered_restaurants_repo
from recommendation_service import (
    get_hybrid_recommendations_for_user,
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
    
    candidate_gmap_ids = None

    if filters:
        filtered_restaurants = get_filtered_restaurants_repo(
            **filters,
        )
        
        candidate_gmap_ids = {
            restaurant["gmap_id"] for restaurant in filtered_restaurants
        }


    # Store recommendations collected from all users
    restaurant_scores = defaultdict(
        lambda: {
            "name": None,
            "score_sum": 0.0,
            "count": 0,
        }
    )

    # Generate hybrid recommendations for each user
    for user_id in user_ids:
        user_recs = get_hybrid_recommendations_for_user(
            user_id=user_id,
            top_k=per_user_k,
            candidate_gmap_ids=candidate_gmap_ids,
        )

        # Collect restaurant scores
        for rec in user_recs:
            gmap_id = rec["gmap_id"]
            restaurant_scores[gmap_id]["name"] = rec["name"]
            restaurant_scores[gmap_id]["score_sum"] += rec["hybrid_score"]
            restaurant_scores[gmap_id]["count"] += 1
            

    # Build final group recommendations
    group_recommendations = []
    group_size = len(user_ids)

    # Calculate group score for each restaurant
    for gmap_id, data in restaurant_scores.items():
        
        # Average hybrid rating
        avg_score = data["score_sum"] / data["count"]
        
        # Percentage of group members that received this recommendation
        coverage = data["count"] / group_size
        
        # Final group ranking score
        group_score = avg_score * coverage

        # Save aggregated result
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

    # Sort by final group score
    group_recommendations.sort(
        key=lambda x: x["group_score"],
        reverse=True,
    )
    
    # Return Top-K recommendations
    return group_recommendations[:top_k]
