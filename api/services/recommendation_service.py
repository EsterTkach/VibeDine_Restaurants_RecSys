import pandas as pd
from api.ml import config
from api.db.restaurant_repository import get_filtered_restaurants_repo
from api.ml.cf_recommender import compute_cf_scores, get_popular_restaurants, get_user_offline_likes, recommend_for_user_cf
from api.services.users_service import get_user_online_likes
from api.utils.utils import extract_gmap_ids, format_restaurant_for_frontend
from api.routes.users import get_onboarding_preferences
from api.ml.cb_recommender import compute_cb_scores, restaurant_lookup
from api.services import hybrid_cache



# def get_popular_restaurants(top_k=10):
#     """
#     Fallback recommendations for cold-start users.
#     Returns most popular restaurants.
#     """

#     interactions = pd.read_parquet(
#         config.INTERACTIONS_FILE
#     )

#     popular = (
#         interactions.groupby("gmap_id")
#         .agg(
#             avg_rating=("rating", "mean"),
#             review_count=("rating", "count"),
#         )
#         .reset_index()
#     )

#     # avoid restaurants with very few reviews
#     popular = popular[
#         popular["review_count"] >= 20
#     ]

#     # weighted ranking
#     popular["score"] = (
#         popular["avg_rating"]
#         * popular["review_count"]
#     )

#     popular = popular.sort_values(
#         by="score",
#         ascending=False
#     )

#     restaurants = pd.read_parquet(
#         config.CBF_FEATURES_FILE
#     )

#     merged = popular.merge(
#         restaurants[
#             ["gmap_id", "name"]
#         ],
#         on="gmap_id",
#         how="left"
#     )

#     recommendations = []

#     for _, row in merged.head(top_k).iterrows():

#         recommendations.append(
#             {
#                 "gmap_id": row["gmap_id"],
#                 "name": row["name"],
#                 "avg_rating": round(
#                     float(row["avg_rating"]), 2
#                 ),
#                 "review_count": int(
#                     row["review_count"]
#                 ),
#             }
#         )

#     return recommendations

POPULAR_FOOD_TO_CATEGORIES_MAP = {
    "Sushi": ["Sushi", "Sushi restaurant", "Japanese", "Japanese restaurant"],
    "Pizza & Pasta": ["Italian", "Italian restaurant", "Pizza restaurant", "Pizza"],
    "Hamburger": ["Hamburger", "Hamburger restaurant", "Burger restaurant"],
    "Ice Cream & Dessert": ["Dessert", "Dessert shop", "Ice cream shop", "Bakery"],
    "Noodles & Ramen": ["Ramen", "Noodle shop", "Japanese", "Asian"],
    "Seafood": ["Seafood", "Seafood restaurant"],
    "Chicken": ["Chicken restaurant", "Fried chicken restaurant"],
    "Steak & BBQ": ["Steak house", "Barbecue restaurant", "BBQ"],
}

CUISINE_TO_CATEGORIES_MAP = {
    "American": ["American", "American restaurant"],
    "Italian": ["Italian", "Italian restaurant", "Pizza restaurant"],
    "Chinese": ["Chinese", "Chinese restaurant"],
    "Japanese": ["Japanese", "Japanese restaurant", "Sushi restaurant"],
    "Mexican & Latin": ["Mexican", "Mexican restaurant", "Latin American restaurant"],
    "Asian Fusion": ["Asian", "Asian restaurant", "Asian fusion restaurant"],
    "Indian": ["Indian", "Indian restaurant"],
    "Mediterranean & Middle East": ["Mediterranean", "Mediterranean restaurant", "Middle Eastern restaurant"],
    "European": ["European", "European restaurant", "French restaurant"],
}

ACCESSIBILITY_MAP = {
    "Required": ["Wheelchair accessible entrance", "Wheelchair accessible seating", "Wheelchair accessible"],
}


def _parse_onboarding_preferences(preferences: dict):
    """
    Maps user-facing onboarding preference values to the actual
    MongoDB field values used by get_filtered_restaurants_repo.
    """
    raw_categories = preferences.get("favorite_categories", [])
    atmosphere = preferences.get("favorite_atmospheres", [])
    accessibility_raw = preferences.get("accessibility", "")
    dietary_raw = preferences.get("dietary_restrictions", "")

    # 1. Separate popular food items from cuisine types and map to DB values
    mapped_categories = []
    mapped_popular_items = []

    for item in raw_categories:
        # Strip emoji prefix (e.g., "🍣 Sushi" → "Sushi")
        clean = item.split(" ", 1)[1] if " " in item and not item[0].isalpha() else item

        if clean in POPULAR_FOOD_TO_CATEGORIES_MAP:
            mapped_categories.extend(POPULAR_FOOD_TO_CATEGORIES_MAP[clean])
            mapped_popular_items.append(clean)
        elif clean in CUISINE_TO_CATEGORIES_MAP:
            mapped_categories.extend(CUISINE_TO_CATEGORIES_MAP[clean])
        else:
            mapped_categories.append(clean)

    # 2. Map accessibility
    mapped_accessibility = ACCESSIBILITY_MAP.get(accessibility_raw)

    # 3. Map dietary restrictions (single string → list, skip "None")
    mapped_dietary = None
    if dietary_raw and dietary_raw != "None":
        mapped_dietary = [dietary_raw]

    return {
        "categories": mapped_categories or None,
        "popular_items": mapped_popular_items or None,
        "atmosphere": atmosphere or None,
        "accessibility": mapped_accessibility,
        "dietary_restrictions": mapped_dietary,
    }


def get_onboarding_candidate_gmap_ids(user_id: str, candidate_gmap_ids=None):
    pref = get_onboarding_preferences(user_id)
    preferences = pref.get("preferences", {})

    if not preferences:
        return candidate_gmap_ids

    parsed = _parse_onboarding_preferences(preferences)

    candidate_gmap_ids_by_category = extract_gmap_ids(
        get_filtered_restaurants_repo(
            categories=parsed["categories"],
            popular_items=parsed["popular_items"],
            accessibility=parsed["accessibility"],
            atmosphere=parsed["atmosphere"],
            dietary_restrictions=parsed["dietary_restrictions"],
            limit=1000))

    # Fallback: if strict filters return nothing, relax to categories only
    if not candidate_gmap_ids_by_category and parsed["categories"]:
        candidate_gmap_ids_by_category = extract_gmap_ids(
            get_filtered_restaurants_repo(
                categories=parsed["categories"],
                limit=1000))

    if candidate_gmap_ids is None:
        return candidate_gmap_ids_by_category

    combined = list(
        set(candidate_gmap_ids_by_category) & set(candidate_gmap_ids)
    )

    # If intersection is empty, prefer onboarding candidates over nothing
    return combined if combined else candidate_gmap_ids_by_category


def get_user_onboarding_recommendations(
    user_id: str,
    top_k: int = 10,
    candidate_gmap_ids=None,
    onboarding_candidate_gmap_ids=None,
):
    candidate_ids = onboarding_candidate_gmap_ids

    if candidate_ids is None:
        candidate_ids = get_onboarding_candidate_gmap_ids(user_id, candidate_gmap_ids)
    elif candidate_gmap_ids is not None:
        candidate_ids = list(
            set(candidate_ids) & set(candidate_gmap_ids)
        )

    recommendations = get_popular_restaurants(
        top_k=top_k,
        candidate_gmap_ids=candidate_ids,
    )
    recommendations = remove_duplicate_names(recommendations)

    return recommendations[:top_k]

""" normalize scores and combine cb and cf scores """
def min_max_normalize(score_dict, keys=None):
    if keys is None:
        keys = list(score_dict.keys())
    else:
        keys = list(keys)

    if not keys:
        return {}

    values = [score_dict.get(k, 0.0) for k in keys]

    min_score = min(values)
    max_score = max(values)

    if max_score == min_score:
        return {k: 1.0 if score_dict.get(k, 0.0) > 0 else 0.0 for k in keys}

    return {
        k: (score_dict.get(k, 0.0) - min_score) / (max_score - min_score)
        for k in keys
    }

"""""
return a combined dict of cb and cf scores, normalized, with a weight alpha for cf and (1-alpha) for cb
"""""
def combine_hybrid_scores(cb_scores, cf_scores, alpha=0.5):

    all_gmap_ids = set(cb_scores.keys()) | set(cf_scores.keys())
    cb_norm = min_max_normalize(cb_scores, keys=all_gmap_ids)
    cf_norm = min_max_normalize(cf_scores, keys=all_gmap_ids)

    hybrid_scores = {}

    for gmap_id in all_gmap_ids:
        cb_score = cb_norm.get(gmap_id, 0.0)
        cf_score = cf_norm.get(gmap_id, 0.0)

        hybrid_scores[gmap_id] = alpha * cf_score + (1 - alpha) * cb_score

    return hybrid_scores, cb_norm, cf_norm

def get_hybrid_scores_for_user(user_id: str):
    cached = hybrid_cache.get(user_id)
    if cached is not None:
        print(f"Cache hit for user {user_id}")
        return cached

    cb_scores = compute_cb_scores(user_id)
    cf_scores = compute_cf_scores(user_id)
    alpha = get_user_alpha(user_id)

    print(f"alpha={alpha} for user {user_id}")
    print(f"CB restaurants={len(cb_scores)}")
    print(f"CF restaurants={len(cf_scores)}")

    hybrid_scores = combine_hybrid_scores(cb_scores, cf_scores, alpha)[0]
    print(f"Hybrid restaurants={len(hybrid_scores)}")

    hybrid_cache.set(user_id, hybrid_scores)
    return hybrid_scores


def rank_hybrid_recommendations(hybrid_scores, top_k=10, candidate_gmap_ids=None):
    candidate_set = set(candidate_gmap_ids) if candidate_gmap_ids is not None else None
    recommendations = []
    for gmap_id, score in hybrid_scores.items():
        if candidate_set is not None and gmap_id not in candidate_set:
            continue
        restaurant = restaurant_lookup.get(gmap_id)
        if restaurant is None:
            continue

        recommendations.append(
            {
                "gmap_id": gmap_id,
                "name": restaurant["name"],
                "hybrid_score": round(float(score), 3),
            }
        )
        if len(recommendations) == (top_k * 3):
            break

    recommendations.sort(key=lambda x: x["hybrid_score"], reverse=True)
    restaurants = remove_duplicate_names(recommendations)
    return restaurants[:top_k]


def get_hybrid_recommendations_for_user(
    user_id: str,
    top_k=10,
    candidate_gmap_ids=None,
    onboarding_candidate_gmap_ids=None,
    hybrid_scores=None,
):
    """
    Returns recommendations for a user.
    If the user has no online likes, returns offline likes.
    If the user has no offline likes, returns popular restaurants.
    """
    if get_user_augmented_likes(user_id) == 0:
        print(f"User {user_id} is cold-start, returning onboarding recommendations")
        return get_user_onboarding_recommendations(
            user_id,
            top_k=top_k,
            candidate_gmap_ids=candidate_gmap_ids,
            onboarding_candidate_gmap_ids=onboarding_candidate_gmap_ids,
        )
    
    if hybrid_scores is None:
        hybrid_scores = get_hybrid_scores_for_user(user_id)

    return rank_hybrid_recommendations(
        hybrid_scores,
        top_k=top_k,
        candidate_gmap_ids=candidate_gmap_ids,
    )


    

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




def get_user_augmented_likes(user_id):
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
    return offline_likes_count + online_likes_count

def get_user_alpha(user_id):
    """
    Determine the user's alpha value based on their offline and online likes.
    Alpha is a measure of how much weight to give to the offline vs online
    recommendations. A user with more online likes will have a higher alpha,
    while a user with more offline likes will have a lower alpha.
    """

    # Get counts of offline and online likes
    alpha = 0.0
    n = get_user_augmented_likes(user_id)

    # Calculate alpha as the ratio of online likes to total likes
    if n <= 5: #cold-start user - pure cb
        alpha = 0.0 
    elif n <= 20: 
        alpha = 0.4
    elif n <= 100: #warm user - hybrid, cf dominates
        alpha = 0.7
    else:
        alpha = 0.85

    return alpha

def remove_duplicate_names(restaurants):
    seen = set()
    unique = []

    for restaurant in restaurants:
        name = restaurant["name"].strip().lower()

        if name in seen:
            continue

        seen.add(name)
        unique.append(restaurant)

    return unique
