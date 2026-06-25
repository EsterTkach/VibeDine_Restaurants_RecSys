from fastapi import APIRouter, HTTPException, Query
from api.ml.cf_recommender import (
    get_popular_restaurants,
)

from api.db.restaurant_repository import get_k_popular_restaurant_repo, get_filtered_restaurants_repo

router = APIRouter(prefix="/mongo", tags=["mongo tests"])


@router.get("/test/getK/{k}")
def get_k_popular_restaurants(
    k: int,
):
    return  {
        "result":get_popular_restaurants(
        k,
    ) }


@router.get("/test/filter/{k}")
def get_filtered_restaurants(
    k: int,
    categories: list[str] = Query(default=[]),
    accessibility: list[str] = Query(default=[]),
    service_options: list[str] = Query(default=[]),
    atmosphere: list[str] = Query(default=[]),
    dining_options: list[str] = Query(default=[]),
    crowd: list[str] = Query(default=[]),
    offerings: list[str] = Query(default=[]),
):
    return {
        "result": get_filtered_restaurants_repo(
            k,
            categories,
            accessibility,
            service_options,
            atmosphere,
            dining_options,
            crowd,
            offerings,
        )
    }

