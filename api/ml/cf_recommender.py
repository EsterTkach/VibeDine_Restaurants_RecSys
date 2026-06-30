from api.ml import config
import pickle
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from api.services.users_service import get_user_online_likes

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

def get_user_row(user_id):
    """
    allows online interactions to improve recommendations, if available
    Returns the user row from the user-item matrix for a given user_id.
    If the user_id is not found, returns None.
    """
    if user_id not in user_id_to_index:
        print(f"User {user_id} not found")
        return []
    
    user_idx = user_id_to_index[user_id]
    
    user_row = user_item_matrix[user_idx].copy()
    
    # if online_likes is None:
    #     online_likes = []
    #     return None

    online_likes = get_user_online_likes(user_id)["online_likes"]
    if online_likes is not None:

        for gmap_id in online_likes:

            if gmap_id not in item_id_to_index:
                continue

            item_idx = item_id_to_index[gmap_id]
            # treat online like as rating 5
            user_row[0, item_idx] = 5

    return user_item_matrix[user_idx]

def compute_cf_scores(user_id):
    """
    returns:
    dict[gmap_id] = float_score
    """
    if user_id not in user_id_to_index:
        print(f"User {user_id} not found")
        return {}
    
    user_row = get_user_row(user_id)
    liked_indices = user_row.nonzero()[1]

    if len(liked_indices) == 0:
        #should call cold start recommender here, but for now just return empty list
        print(f"No liked restaurants found for user {user_id}")
        return {}
    
    liked_ratings = user_row.data
    """""
    Weighted Item-Based CF prediction:
    score = sum(similarity × rating) / sum(similarity)
    
    Higher user ratings have stronger influence on the recommendation score.
    Item similarities are based on behavior of all users in item_user_matrix.
    """
    similarities = cosine_similarity(item_user_matrix[liked_indices], item_user_matrix)

    # Remove self-similarity:
    # do not let a restaurant contribute to its own score with similarity = 1    
    for i, item_idx in enumerate(liked_indices):
        similarities[i, item_idx] = 0

    numerator = similarities.T @ liked_ratings
    denominator = similarities.sum(axis=0)

    scores = np.divide(
        numerator, denominator, out=np.zeros_like(numerator,dtype=float), where=denominator != 0
    )

    return {index_to_item_id[idx]: float(scores[idx]) for idx in range(len(scores)) if idx not in liked_indices}


### get Top-K restaurant recommendations for a user using Item-Based Collaborative Filtering
def recommend_for_user_cf(user_id, top_k=config.TOP_K, candidate_gmap_ids=None, allow_liked_items=False):
    # allow_liked_items: allow restaurants already liked by the user to appear in recommendations.
    
    if user_id not in user_id_to_index:
         print(f"User {user_id} not found")
         return []

    # user_idx = user_id_to_index[user_id]

    # user_row = user_item_matrix[user_idx]

    user_row = get_user_row(user_id)
    liked_indices = user_row.nonzero()[1]

    if len(liked_indices) == 0:
        #should call cold start recommender here, but for now just return empty list
        print(f"No liked restaurants found for user {user_id}")
        return []

    liked_ratings = user_row.data
    """""
    Weighted Item-Based CF prediction:
    score = sum(similarity × rating) / sum(similarity)
    
    Higher user ratings have stronger influence on the recommendation score.
    Item similarities are based on behavior of all users in item_user_matrix.
    """
    similarities = cosine_similarity(item_user_matrix[liked_indices], item_user_matrix)

    # Remove self-similarity:
    # do not let a restaurant contribute to its own score with similarity = 1    
    for i, item_idx in enumerate(liked_indices):
        similarities[i, item_idx] = 0


    numerator = similarities.T @ liked_ratings
    denominator = similarities.sum(axis=0)

    scores = np.divide(
        numerator, denominator, out=np.zeros_like(numerator,dtype=float), where=denominator != 0
    )

    # Sort first by predicted rating.
    # If multiple restaurants have the same predicted rating,
    # prefer the ones with stronger similarity support.

    #scores = compute_cf_scores(user_id)

    if not scores:
        return []

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


"""
def get_offline_likes(user_id, min_rating=config.MIN_RATING):
    
    Return the number of restaurants the user liked
    according to the offline user-item matrix.


    if user_id not in user_id_to_index:
        return 0

    user_idx = user_id_to_index[user_id]
    user_row = user_item_matrix[user_idx]

##    return int((user_row.data >= min_rating).sum())
"""

def get_popular_restaurants(top_k=config.TOP_K):
    """
    Return the Top-K most popular restaurants
    based on offline positive ratings.
    """

    # Sum positive ratings (4-5) for each restaurant
    popularity_scores = np.asarray(
        user_item_matrix.sum(axis=0)
    ).ravel()

    # Rank restaurants by popularity
    ranked_indices = popularity_scores.argsort()[::-1]

    recommendations = []

    # Build recommendation list
    for idx in ranked_indices[:top_k]:
        gmap_id = index_to_item_id[idx]

        name = (
            restaurant_lookup.loc[gmap_id]["name"]
            if gmap_id in restaurant_lookup.index
            else "Unknown"
        )

        recommendations.append(
            {
                "gmap_id": gmap_id,
                "name": name,
                "popularity_score": round(float(popularity_scores[idx]), 3),
            }
        )

    return recommendations

def get_user_offline_likes(
    user_id: str
):

    if user_id not in user_id_to_index:
        return {
            "user_id":
            user_id,

            "offline_likes":
            []
        }

    user_idx = user_id_to_index[user_id]
    user_row = user_item_matrix[user_idx]

    liked_indices = user_row.nonzero()[1]

    offline_likes = [
        index_to_item_id[index]
        for index in liked_indices
    ]

    return {
        "user_id":
        user_id,

        "offline_likes":
        offline_likes
    }



## get Top-K restaurant recommendations for a user using Item-Based Collaborative Filtering
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





##############
#### test ####
##############

# user_id = "108988860387051139127"
# results = recommend_for_user_cf(user_id, top_k=10)

# print(f"CF recommendations for user {user_id}:")

# for r in results:
#     print(r)
