from pydantic import BaseModel


class UserSignupRequest(BaseModel):
    username: str
    password: str

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