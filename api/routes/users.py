from fastapi import (
    APIRouter
)

from uuid import uuid4

from api.db.mongo import (
    users_collection
)

from api.schemas.user import (
    UserSignupRequest
)

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/signup")
def signup(
    request:
    UserSignupRequest
):

    user = {
        "user_id":
        str(uuid4()),

        "username":
        request.username,
    }

    users_collection.insert_one(
        user
    )

    return {
        "message":
        "User created",

        "user_id":
        user["user_id"],
    }

#Test db
@router.get("/test-db")
def test_db():
    return {
        "count":
        users_collection.count_documents({})
    }