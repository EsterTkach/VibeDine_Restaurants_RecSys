from pydantic import BaseModel

from api.schemas.restaurant_schema import FilterRequest

class GroupRecommendationRequest(BaseModel):
    user_ids: list[str]
    top_k: int = 10
    per_user_k: int = 50
    filters: FilterRequest | None = None