from pydantic import BaseModel


class FilterRequest(BaseModel):
    categories: list[str] | None = None
    accessibility: list[str] | None = None
    service_options: list[str] | None = None
    atmosphere: list[str] | None = None
    dining_options: list[str] | None = None
    crowd: list[str] | None = None
    offerings: list[str] | None = None
    dietary_restrictions: list[str] | None = None

    price: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    radius_km: float | None = None

    min_rating: float = 0.0
    #min_reviews: int = 0