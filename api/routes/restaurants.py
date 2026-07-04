from fastapi import APIRouter, HTTPException
from api.db.restaurant_repository import get_restaurant_by_gmap_id

router = APIRouter()


@router.get("/{gmap_id}")
def get_restaurant(gmap_id: str):
    restaurant = get_restaurant_by_gmap_id(gmap_id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    restaurant.pop("_id", None)
    return restaurant
