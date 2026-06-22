import pandas as pd

from api.ml import config
from api.ml.cf_recommender import recommend_for_user_cf
from api.db.restaurant_repository import get_filtered_restaurants_repo
from api.utils.utils import format_restaurant_for_frontend

def get_popular_restaurants(top_k=10):
    """
    Fallback recommendations for cold-start users.
    Returns most popular restaurants.
    """

    interactions = pd.read_parquet(
        config.INTERACTIONS_FILE
    )

    popular = (
        interactions.groupby("gmap_id")
        .agg(
            avg_rating=("rating", "mean"),
            review_count=("rating", "count"),
        )
        .reset_index()
    )

    # avoid restaurants with very few reviews
    popular = popular[
        popular["review_count"] >= 20
    ]

    # weighted ranking
    popular["score"] = (
        popular["avg_rating"]
        * popular["review_count"]
    )

    popular = popular.sort_values(
        by="score",
        ascending=False
    )

    restaurants = pd.read_parquet(
        config.CBF_FEATURES_FILE
    )

    merged = popular.merge(
        restaurants[
            ["gmap_id", "name"]
        ],
        on="gmap_id",
        how="left"
    )

    recommendations = []

    for _, row in merged.head(top_k).iterrows():

        recommendations.append(
            {
                "gmap_id": row["gmap_id"],
                "name": row["name"],
                "avg_rating": round(
                    float(row["avg_rating"]), 2
                ),
                "review_count": int(
                    row["review_count"]
                ),
            }
        )

    return recommendations

def get_recommendations(
    user_id: str,
    top_k=10
):
    """
    Main recommendation entrypoint.
    Handles cold-start users.
    """

    recommendations = (
        recommend_for_user_cf(
            user_id=user_id,
            top_k=top_k
        )
    )

    if len(recommendations) == 0:

        return {
            "recommendation_type":
            "cold_start_popular",

            "recommendations":
            get_popular_restaurants(
                top_k
            ),
        }

    return {
        "recommendation_type":
        "collaborative_filtering",

        "recommendations":
        recommendations,
    }

def get_popular_by_category(category: str, top_k: int = 10):
    # Some categories in MongoDB might have slightly different naming conventions
    # This handles edge cases (like "Sushi" vs "Sushi restaurant")
    categories_to_search = [category]
    if category.lower() == "sushi":
        categories_to_search = ["Sushi restaurant", "Sushi"]
    elif category.lower() == "italian":
        categories_to_search = ["Italian restaurant", "Italian"]

    raw_restaurants = get_filtered_restaurants_repo(k=top_k, categories=categories_to_search)
    return [format_restaurant_for_frontend(r) for r in raw_restaurants]