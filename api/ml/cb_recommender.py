from api.ml import config
import pickle
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

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


### get top K recommanded restaurants by content - by user ("liked" = rated above min_rating)
def recommend_for_user(
    user_id, top_k=config.TOP_K, min_rating=config.MIN_RATING, candidate_gmap_ids=None
):
    user_likes = interactions[
        (interactions["user_id"] == user_id) & (interactions["rating"] >= min_rating)
    ]

    if user_likes.empty:
        print(f"No liked restaurants found for user {user_id}")
        return []

    liked_gmap_ids = user_likes["gmap_id"].tolist()

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
