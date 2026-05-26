from pydantic import BaseModel


class UserSignupRequest(
    BaseModel
):
    username: str
    