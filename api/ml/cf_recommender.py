from api.ml import config
import pickle
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from api.services.users_service import get_user_online_likes
from scipy.sparse import lil_matrix

### Load trained model
with open(config.MODEL_CF_FILE, "rb") as f:
    model = pickle.load(f)

print("CF Model loaded")

user_item_matrix = model["user_item_matrix"]
item_user_matrix = model["item_user_matrix"]
user_id_to_index = model["user_id_to_index"]
index_to_item_id = model["index_to_item_id"]
restaurant_lookup = model["restaurant_lookup"]

# added for hybrid recommender:
item_id_to_index = model["item_id_to_index"]

# Pre-compute global popularity ranking once at module load
_popularity_scores = np.asarray(user_item_matrix.sum(axis=0)).ravel()
_popularity_ranked_indices = _popularity_scores.argsort()[::-1]

# Build a pre-sorted list of (gmap_id, score) for fast filtering
_popular_ranked_list = []
for _idx in _popularity_ranked_indices:
    _gid = index_to_item_id[_idx]
    _popular_ranked_list.append((_gid, float(_popularity_scores[_idx])))

print(f"Popularity ranking pre-computed: {len(_popular_ranked_list)} restaurants")


def get_user_row(user_id):
    """
    allows online interactions to improve recommendations, if available
    Return the user's offline CF row augmented with online likes.

    For a new user who is not in the offline model,
    create an empty temporary row and fill it with online likes.
    """

    # Existing user: start from the offline user-item row
    if user_id in user_id_to_index:
        user_idx = user_id_to_index[user_id]
        user_row = user_item_matrix[user_idx].copy().tolil()

    # New user: create an empty temporary row
    else:
        user_row = lil_matrix(
            (1, user_item_matrix.shape[1]),
            dtype=float,
        )

    # Add online likes
    online_likes = get_user_online_likes(user_id).get(
        "online_likes",
        [],
    )

    for gmap_id in online_likes:
        if gmap_id not in item_id_to_index:
            continue

        item_idx = item_id_to_index[gmap_id]

        # Treat an online like as a strong positive rating
        user_row[0, item_idx] = 5.0

    return user_row.tocsr()


def compute_cf_scores(user_id):
    """
    returns:
    dict[gmap_id] = float_score
    """

    user_row = get_user_row(user_id)

    liked_indices = user_row.indices

    if len(liked_indices) == 0:
        # should call cold start recommender here, but for now just return empty list
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
        numerator,
        denominator,
        out=np.zeros_like(numerator, dtype=float),
        where=denominator != 0,
    )
    
    liked_set = set(liked_indices)

    return {
        index_to_item_id[idx]: float(scores[idx])
        for idx in range(len(scores))
        if idx not in liked_set
    }


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


def get_popular_restaurants(top_k=config.TOP_K, candidate_gmap_ids=None):
    """
    Return the Top-K most popular restaurants
    based on offline positive ratings.
    Uses pre-computed popularity ranking for O(n) filtering.
    """
    candidate_set = set(candidate_gmap_ids) if candidate_gmap_ids is not None else None

    recommendations = []

    for gmap_id, score in _popular_ranked_list:
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
                "popularity_score": round(score, 3),
            }
        )
        if len(recommendations) == (top_k * 3):
            break

    return recommendations


def get_user_offline_likes(user_id: str):

    if user_id not in user_id_to_index:
        return {"user_id": user_id, "offline_likes": []}

    user_idx = user_id_to_index[user_id]
    user_row = user_item_matrix[user_idx]

    liked_indices = user_row.indices

    offline_likes = [index_to_item_id[index] for index in liked_indices]

    return {"user_id": user_id, "offline_likes": offline_likes}
