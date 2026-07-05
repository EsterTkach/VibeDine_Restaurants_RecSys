from pydantic import BaseModel
from typing import Literal, Tuple

class Location(BaseModel):
    type: Literal["Point"]
    coordinates: Tuple[float, float]


class UserSignupRequest(BaseModel):
    username: str
    password: str
    name: str
    location : Location
    avatar_index: int


class UserLoginRequest(BaseModel):
    username: str
    password: str

class RestaurantInteractionRequest(BaseModel):
    user_id: str

class OnboardingPreferences(BaseModel):
    favorite_categories: list[str]
    favorite_atmospheres: list[str]
    accessibility: str
    dietary_restrictions: str

class OnboardingPreferencesRequest(BaseModel):
    preferences: OnboardingPreferences

class AddFriendRequest(BaseModel):
    friend_id: str