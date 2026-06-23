from pydantic import BaseModel

class GroupRecommendationRequest(BaseModel):
    user_ids: list[str]
    top_k: int = 10
    per_user_k: int = 50
    filters: dict | None = None