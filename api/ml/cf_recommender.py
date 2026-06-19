from api.ml import config
import pickle
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

### Load trained model
with open(config.MODEL_CF_FILE, "rb") as f:
    model = pickle.load(f)

print("CF Model loaded")

user_item_matrix = model["user_item_matrix"]
item_user_matrix = model["item_user_matrix"]
user_id_to_index = model["user_id_to_index"]
index_to_item_id = model["index_to_item_id"]
restaurant_lookup = model["restaurant_lookup"]

#added for hybrid recommender:
item_id_to_index = model["item_id_to_index"] 

def recommend_for_user_cf_augmented(user_id, top_k=config.TOP_K, candidate_gmap_ids=None):

    if user_id not in user_id_to_index:
        print(f"User {user_id} not found")
        return []

    user_idx = user_id_to_index[user_id]

    user_row = user_item_matrix[user_idx].copy()

    online_likes = get_user_online_likes(user_id) #will be implemented in the future

    for gmap_id in online_likes:

        if gmap_id not in item_id_to_index:
            continue

        item_idx = item_id_to_index[gmap_id]
        # treat online like as rating 5
        user_row[0, item_idx] = 5

    liked_indices = user_row.nonzero()[1]

    if len(liked_indices) == 0:
        print(f"No liked restaurants found for user {user_id}")
        return []

    liked_ratings = user_row.data

    similarities = cosine_similarity(item_user_matrix[liked_indices], item_user_matrix)

    for i, item_idx in enumerate(liked_indices):
        similarities[i, item_idx] = 0

    numerator = similarities.T @ liked_ratings
    denominator = similarities.sum(axis=0)

    scores = np.divide(
        numerator, denominator, out=np.zeros_like(numerator), where=denominator != 0
    )

    # Sort first by predicted rating.
    # If multiple restaurants have the same predicted rating,
    # prefer the ones with stronger similarity support.
    ranked_indices = sorted(
        range(len(scores)),
        key=lambda idx: (round(float(scores[idx]), 3), denominator[idx]),
        reverse=True,
    )

    liked_set = set(liked_indices)

    # Create a set of known restaurants (liked by the user)
    known_restaurants = {
        index_to_item_id[idx]
        for idx in liked_indices
    }
    recommendations = []
    candidate_set = set(candidate_gmap_ids) if candidate_gmap_ids is not None else None

    for idx in ranked_indices:
        if idx in liked_set:
            continue

        gmap_id = index_to_item_id[idx]

        if candidate_set is not None and gmap_id not in candidate_set:
            continue

        name = (
            restaurant_lookup.loc[gmap_id]["name"]
            if gmap_id in restaurant_lookup.index
            else "Unknown"
        )

        recommendations.append(
            {
                "gmap_id": gmap_id,
                "name": name,
                "predicted_rating": round(float(scores[idx]), 3),
                "similarity_strength": round(float(denominator[idx]), 3),
            }
        )

        if len(recommendations) == top_k:
            break

    return recommendations


### get Top-K restaurant recommendations for a user using Item-Based Collaborative Filtering
def recommend_for_user_cf(user_id, top_k=config.TOP_K, candidate_gmap_ids=None, allow_liked_items=False):
    # allow_liked_items: allow restaurants already liked by the user to appear in recommendations.
    
    if user_id not in user_id_to_index:
        print(f"User {user_id} not found")
        return []

    user_idx = user_id_to_index[user_id]

    user_row = user_item_matrix[user_idx]

    liked_indices = user_row.nonzero()[1]

    if len(liked_indices) == 0:
        print(f"No liked restaurants found for user {user_id}")
        return []

    liked_ratings = user_row.data

    # Weighted Item-Based CF prediction:
    # score = sum(similarity × rating) / sum(similarity)
    #
    # Higher user ratings have stronger influence on the recommendation score.
    # Item similarities are based on behavior of all users in item_user_matrix.

    similarities = cosine_similarity(item_user_matrix[liked_indices], item_user_matrix)

    # Remove self-similarity:
    # do not let a restaurant contribute to its own score with similarity = 1    
    for i, item_idx in enumerate(liked_indices):
        similarities[i, item_idx] = 0


    numerator = similarities.T @ liked_ratings
    denominator = similarities.sum(axis=0)

    scores = np.divide(
        numerator, denominator, out=np.zeros_like(numerator), where=denominator != 0
    )

    # Sort first by predicted rating.
    # If multiple restaurants have the same predicted rating,
    # prefer the ones with stronger similarity support.
    ranked_indices = sorted(
        range(len(scores)),
        key=lambda idx: (round(float(scores[idx]), 3), denominator[idx]),
        reverse=True,
    )

    liked_set = set(liked_indices)
    recommendations = []
    candidate_set = set(candidate_gmap_ids) if candidate_gmap_ids is not None else None

    for idx in ranked_indices:
        if not allow_liked_items and idx in liked_set:
            continue

        gmap_id = index_to_item_id[idx]

        if candidate_set is not None and gmap_id not in candidate_set:
            continue

        name = (
            restaurant_lookup.loc[gmap_id]["name"]
            if gmap_id in restaurant_lookup.index
            else "Unknown"
        )

        recommendations.append(
            {
                "gmap_id": gmap_id,
                "name": name,
                "predicted_rating": round(float(scores[idx]), 3),
                "similarity_strength": round(float(denominator[idx]), 3),
            }
        )

        if len(recommendations) == top_k:
            break

    return recommendations


###############
##### test ####
###############

# user_id = "108988860387051139127"
# results = recommend_for_user_cf(user_id, top_k=10)

# print(f"CF recommendations for user {user_id}:")

# for r in results:
#     print(r)
