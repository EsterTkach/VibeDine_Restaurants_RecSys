from api.db.mongo import restaurants_collection


def get_k_popular_restaurant_repo(k: int):
    restaurants = list(
        restaurants_collection.find(
            {},
            {"_id": 0, "gmap_id": 1, "name": 1, "avg_rating": 1, "num_of_reviews": 1},
        )
        .sort([("avg_rating", -1), ("num_of_reviews", -1)])
        .limit(k)
    )

    return restaurants


def get_filtered_restaurants_repo(
    k: int,
    categories=None,
    accessibility=None,
    service_options=None,
    atmosphere=None,
    dining_options=None,
    crowd=None,
    offerings=None,
):

    query = {}

    if categories:
        query["category"] = {"$all": categories}

    if accessibility:
        query["accessibility"] = {"$all": accessibility}

    if service_options:
        query["service_options"] = {"$all": service_options}

    if atmosphere:
        query["atmosphere"] = {"$all": atmosphere}

    if dining_options:
        query["dining_options"] = {"$all": dining_options}

    if crowd:
        query["crowd"] = {"$all": crowd}

    if offerings:
        query["offerings"] = {"$all": offerings}

    print(query)
    projection = {"_id": 1, "gmap_id": 1, "name": 1}

    for field in query.keys():
        projection[field] = 1

    return list(restaurants_collection.find(query, projection).limit(k))
