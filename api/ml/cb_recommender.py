from api.ml import config
import pickle
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from collections import defaultdict

from api.services.users_service import get_user_online_likes

"""Content-Based Recommender System for Restaurants"""

### Load trained model
interactions = pd.read_parquet(config.INTERACTIONS_FILE)
with open(config.MODEL_CB_FILE, "rb") as f:
    model = pickle.load(f)

print("Model loaded")

restaurants = model["restaurants"]
tfidf = model["tfidf"]
tfidf_matrix = model["tfidf_matrix"]


### get top K recommanded restaurants by content - by restaurant gmap_id
def recommend_similar_restaurants(
    restaurant_gmap_id, top_k=config.TOP_K, candidate_gmap_ids=None
):
    matches = restaurants[restaurants["gmap_id"] == restaurant_gmap_id]

    if matches.empty:
        print(f"Restaurant '{restaurant_gmap_id}' not found")
        return []

    idx = matches.index.item()

    scores = cosine_similarity(tfidf_matrix[idx], tfidf_matrix).flatten()

    scores = list(enumerate(scores))

    scores = sorted(scores, key=lambda x: x[1], reverse=True)

    recommendations = []
    candidate_set = set(candidate_gmap_ids) if candidate_gmap_ids is not None else None

    for i, score in scores:
        if i == idx:
            continue

        gmap_id = restaurants.iloc[i]["gmap_id"]

        if candidate_set is not None and gmap_id not in candidate_set:
            continue

        recommendations.append(
            {
                "name": restaurants.iloc[i]["name"],
                "gmap_id": gmap_id,
                "similarity_score": round(float(score), 3),
            }
        )

        if len(recommendations) == top_k:
            break

    return recommendations

def compute_cb_scores(user_id):

    online_likes = get_user_online_likes(user_id)[online_likes]
    
    user_likes = interactions[
        (interactions["user_id"] == user_id) & (interactions["rating"] >= config.MIN_RATING)
    ]
    offline_liked_gmap_ids = []

    if not user_likes.empty:
        offline_liked_gmap_ids = user_likes["gmap_id"].tolist()

    # Merge offline likes with online likes
    liked_gmap_ids = list(set(offline_liked_gmap_ids + online_likes))

    if len(liked_gmap_ids) == 0:
        print(f"No liked restaurants found for user {user_id}")
        return []

    # Convert liked restaurant IDs to matrix indices
    liked_indices = restaurants[
        restaurants["gmap_id"].isin(liked_gmap_ids)
    ].index.tolist()

    if len(liked_indices) == 0:
        print("User liked restaurants not found in metadata")
        return []

    user_scores = cosine_similarity(tfidf_matrix[liked_indices], tfidf_matrix).mean(
        axis=0
    )

    cb_scores = {}

    liked_set = set(liked_gmap_ids)

    for idx, score in enumerate(user_scores):
        gmap_id = restaurants.iloc[idx]["gmap_id"]

        if gmap_id in liked_set:
            continue

        cb_scores[gmap_id] = float(score)

    return cb_scores


### get top K recommanded restaurants by content - by user ("liked" = rated above min_rating)
def recommend_for_user(
    user_id,
    top_k=config.TOP_K,
    min_rating=config.MIN_RATING,
    candidate_gmap_ids=None,
    online_likes=None,
):

    if online_likes is None:
        online_likes = []

    user_likes = interactions[
        (interactions["user_id"] == user_id) & (interactions["rating"] >= min_rating)
    ]

    offline_liked_gmap_ids = []

    if not user_likes.empty:
        offline_liked_gmap_ids = user_likes["gmap_id"].tolist()

    # Merge offline likes with online likes
    liked_gmap_ids = list(set(offline_liked_gmap_ids + online_likes))

    if len(liked_gmap_ids) == 0:
        print(f"No liked restaurants found for user {user_id}")
        return []

    # Convert liked restaurant IDs to matrix indices
    liked_indices = restaurants[
        restaurants["gmap_id"].isin(liked_gmap_ids)
    ].index.tolist()

    if len(liked_indices) == 0:
        print("User liked restaurants not found in metadata")
        return []

    user_scores = cosine_similarity(tfidf_matrix[liked_indices], tfidf_matrix).mean(
        axis=0
    )

    ranked_indices = user_scores.argsort()[::-1]

    recommendations = []
    candidate_set = set(candidate_gmap_ids) if candidate_gmap_ids is not None else None

    for idx in ranked_indices:
        # Skip restaurants the user already liked, because we dont want to
        # recommend items that were already used to build the user profile
        if idx in liked_indices:
            continue

        gmap_id = restaurants.iloc[idx]["gmap_id"]

        if candidate_set is not None and gmap_id not in candidate_set:
            continue

        recommendations.append(
            {
                "name": restaurants.iloc[idx]["name"],
                "gmap_id": gmap_id,
                "score": round(float(user_scores[idx]), 3),
            }
        )

        if len(recommendations) == top_k:
            break

    return recommendations


def recommend_for_group_cb(
    user_ids,
    top_k=config.TOP_K,
    per_user_k=50,
    min_rating=config.MIN_RATING,
    candidate_gmap_ids=None,
    online_likes_by_user=None,
):
    """
    Generate group recommendations
    using Content-Based filtering.
    """
    
    if not user_ids:
        print("Group is empty")
        return []

    if online_likes_by_user is None:
        online_likes_by_user = {}

    # Store recommendations collected from all users
    restaurant_scores = defaultdict(
        lambda: {
            "name": None,
            "score_sum": 0.0,
            "count": 0,
        }
    )

    # Generate CB recommendations for each user
    for user_id in user_ids:
        user_recs = recommend_for_user(
            user_id=user_id,
            top_k=per_user_k,
            min_rating=min_rating,
            candidate_gmap_ids=candidate_gmap_ids,
            online_likes=online_likes_by_user.get(user_id, []),
        )

        # Collect restaurant scores
        for rec in user_recs:
            gmap_id = rec["gmap_id"]

            restaurant_scores[gmap_id]["name"] = rec["name"]
            restaurant_scores[gmap_id]["score_sum"] += rec["score"]
            restaurant_scores[gmap_id]["count"] += 1

    # Build final group recommendations
    group_recommendations = []
    group_size = len(user_ids)

    # Calculate final score for each restaurant
    for gmap_id, data in restaurant_scores.items():

        # Average content-based score
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
                "avg_content_score": round(float(avg_score), 3),
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

    return group_recommendations[:top_k]





###############
##### test ####
###############

# results1 = recommend_similar_restaurants("0x80dd2b4c8555edb7:0xfc33d65c4bdbef42", 5)

# print("\nTop similar restaurants:")
# for r in results1:
#     print(r)

# user_id = interactions["user_id"].iloc[5]
# results2 = recommend_for_user(user_id, 5, 3)

# print(f"\nRecommendations for user {user_id}:")
# for r in results2:
#     print(r)
