from api.ml import config
import pickle
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

from api.services.users_service import get_user_online_likes

"""Content-Based Recommender System for Restaurants"""

### Load trained model
interactions = pd.read_parquet(config.INTERACTIONS_FILE)
with open(config.MODEL_CB_FILE, "rb") as f:
    model = pickle.load(f)

print("Model loaded")

restaurants = model["restaurants"]
restaurant_lookup = restaurants.set_index("gmap_id").to_dict("index")
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

    online_likes = get_user_online_likes(user_id)["online_likes"]
    
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
        return {}

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


