import pandas as pd

from api.ml import config
from api.ml.cf_recommender import recommend_for_user_cf_augmented
from api.db.restaurant_repository import (get_filtered_restaurants_repo, get_user_online_likes)
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

    user_online_likes= get_user_online_likes(user_id)

    recommendations = recommend_for_user_cf_augmented(
        user_id=user_id,
        top_k=top_k,
        online_likes=user_online_likes,
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

EXACT_CATEGORY_MAP = {
    "sushi": ["Sushi", "Sushi restaurant", "Sushi takeaway", "Conveyor belt sushi restaurant", "japanese", "japanese restaurant"],
    "italian": ["Italian", "Italian restaurant", "Pizza restaurant", "Pizza"],
    "dessert": ["Dessert", "Dessert shop", "Dessert restaurant", "Ice cream shop", "Bakery"],
    "cafe": ["Cafe", "Coffee shop", "Espresso bar"],
    "burger": ["Hamburger", "Hamburger restaurant", "Burger restaurant"],
    "bar": ["Bar", "Coctail bar", "Bar and restaurant"]
}

def get_popular_by_category(category: str, page: int = 1, per_page: int = 15):
    """
    Fetches the top matching restaurants for a category. 
    Enforces quality limits because it's rendering a direct frontend browsing tier.
    """
    safe_category = category.lower()
    
    if safe_category in EXACT_CATEGORY_MAP:
        categories_to_search = EXACT_CATEGORY_MAP[safe_category]
    else:
        categories_to_search = [
            category,
            category.title(),
            f"{category.title()} restaurant",
        ]

    # Calculate pagination offsets
    skip_value = (page - 1) * per_page

    # Execute the query with strict crowd-pleasing quality guidelines
    raw_restaurants = get_filtered_restaurants_repo(
        skip=skip_value,
        limit=per_page,
        categories=categories_to_search,
        min_rating=4.0,
        min_reviews=30
    )
    
    return [format_restaurant_for_frontend(r) for r in raw_restaurants]