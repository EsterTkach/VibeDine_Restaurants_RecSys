import pandas as pd

from api.ml import config
from api.db.restaurant_repository import get_filtered_restaurants_repo
from api.ml.cf_recommender import compute_cf_scores, get_user_offline_likes, recommend_for_user_cf
from api.services.users_service import get_user_online_likes
from api.utils.utils import format_restaurant_for_frontend
from api.routes.users import get_onboarding_preferences


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


"""fix: not done yet"""
def get_user_onboarding_recommendations(user_id: str, top_k: int = 10):

    pref = get_onboarding_preferences(user_id)
    #need to continue, based on 
    for category in pref["categories"]:
        restaurants = get_popular_by_category(
            category=category,
            page=1,
            per_page=top_k
        )
        if restaurants:
            return restaurants
        

def get_hybrid_recommendations_for_user(
    user_id: str,
    top_k=10,
    candidate_gmap_ids=None,
):
    """
    Returns recommendations for a user.
    If the user has no online likes, returns offline likes.
    If the user has no offline likes, returns popular restaurants.
    """
    alpha = get_user_alpha(user_id)

    if alpha == 0.0:
        return get_user_onboarding_recommendations(user_id, top_k=top_k)
    
    cf_scores = compute_cf_scores(user_id)
    cb_scores = compute_cb_scores(user_id) #will implement

    

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



#Test db
def test_db():
    return {
        "count":
        users_collection.count_documents({})
    }

#we dont need is_user_coldstart for sure

def is_user_coldstart(user_id):
    """
    Check if a user is cold-start based on their offline and online likes.
    A user is considered cold-start if they have no likes in both the offline
    and online datasets.
    """

    # Check offline likes
    offline_likes_count = len(get_user_offline_likes(user_id)["offline_likes"])

    # Check online likes
    online_likes_count = len(get_user_online_likes(user_id)["online_likes"])

    # If both counts are zero, the user is cold-start
    return offline_likes_count == 0 and online_likes_count == 0

def get_user_alpha(user_id):
    """
    Determine the user's alpha value based on their offline and online likes.
    Alpha is a measure of how much weight to give to the offline vs online
    recommendations. A user with more online likes will have a higher alpha,
    while a user with more offline likes will have a lower alpha.
    """

    # Get counts of offline and online likes
    offline_likes_count = len(get_user_offline_likes(user_id)["offline_likes"])
    online_likes_count = len(get_user_online_likes(user_id)["online_likes"])

    # If both counts are zero, return None (cold-start user)
    if offline_likes_count == 0 and online_likes_count == 0:
        return None

    # Calculate alpha as the ratio of online likes to total likes
    n = offline_likes_count + online_likes_count
    
    if n <= 5: #cold-start user - pure cb
        alpha = 0.0 
    elif n <= 20: 
        alpha = 0.4
    elif n <= 100: #warm user - hybrid, cf dominates
        alpha = 0.7
    else:
        alpha = 0.85

    return alpha