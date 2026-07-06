from pydantic import BaseModel


class FilterRequest(BaseModel):
    # Enum-backed tag filters (values must come from enums/models_enums.py)
    categories: list[str] | None = None  # CuisineType values -> restaurant.cuisines
    establishment_types: list[str] | None = None  # EstablishmentType values
    meal_types: list[str] | None = None  # MealType values
    dining_styles: list[str] | None = None  # DiningStyle values
    popular_items: list[str] | None = None  # PopularFoodItem values
    dietary_preferences: list[str] | None = None  # DietaryPreference values
    vibe: list[str] | None = None  # Vibe values

    # Strict boolean flag
    is_accessible: bool | None = None

    # Price / geo
    price: str | None = None
    max_price: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    radius_km: float | None = None

    # Quality thresholds
    min_rating: float = 0.0
    min_reviews: int | None = None
    max_reviews: int | None = None