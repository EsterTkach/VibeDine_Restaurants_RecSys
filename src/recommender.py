import pandas as pd
import pickle
from sklearn.metrics.pairwise import cosine_similarity

interactions = pd.read_parquet("data/CF_interaction_matrix.parquet")

### Load trained model

with open("models/content_based_model.pkl", "rb") as f:
    model = pickle.load(f)

print("Model loaded")

restaurants = model["restaurants"]
tfidf = model["tfidf"]
tfidf_matrix = model["tfidf_matrix"]


### get topK recommanded restaurants by content - by restaurant name
def recommend_similar_restaurants(restaurant_name, top_k=5):
    matches = restaurants[restaurants["name"] == restaurant_name]

    if matches.empty:
        print(f"Restaurant '{restaurant_name}' not found")
        return []

    idx = matches.index[0]  # NOTICE- כרגע לוקח לפי המסעדה הראושנה בשם זה

    scores = cosine_similarity(tfidf_matrix[idx], tfidf_matrix).flatten()

    scores = list(enumerate(scores))

    scores = sorted(scores, key=lambda x: x[1], reverse=True)

    top_scores = scores[1 : top_k + 1]

    recommendations = []

    for i, score in top_scores:
        recommendations.append(
            {
                "name": restaurants.iloc[i]["name"],
                "gmap_id": restaurants.iloc[i]["gmap_id"],
                "similarity_score": round(score, 3),
            }
        )

    return recommendations


### get topK recommanded restaurants by content - by user ("liked" = rated above min_rating)
def recommend_for_user(user_id, top_k=10, min_rating=4):
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

    for idx in ranked_indices:
        # Skip restaurants the user already liked, because we dont want to
        # recommend items that were already used to build the user profile
        if idx in liked_indices:
            continue

        recommendations.append(
            {
                "name": restaurants.iloc[idx]["name"],
                "gmap_id": restaurants.iloc[idx]["gmap_id"],
                "score": round(float(user_scores[idx]), 3),
            }
        )

        if len(recommendations) == top_k:
            break

    return recommendations




##### test #####

# results1 = recommend_similar_restaurants("Vons Chicken", 5)

# print("\nTop similar restaurants:")
# for r in results1:
#     print(r)

# user_id = interactions["user_id"].iloc[0]

# results2 = recommend_for_user(user_id, 5, 3)

# print(f"\nRecommendations for user {user_id}:")
# for r in results2:
#     print(r)
