from pydantic import BaseModel


class UserSignupRequest(BaseModel):
    username: str
    password: str

class UserLoginRequest(BaseModel):
    username: str
    password: str

class OnboardingPreferencesRequest(BaseModel):
    preferences: dict

class RestaurantInteractionRequest(BaseModel):
    user_id: str