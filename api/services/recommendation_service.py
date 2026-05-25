import pandas as pd

from src import config
from src.cf_recommender import recommend_for_user_cf


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