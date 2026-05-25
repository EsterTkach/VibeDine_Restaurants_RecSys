from fastapi import FastAPI

from api.routes.recommendations import (
    router as recommendations_router
)
from api.routes.users import (
    router as users_router
)

app = FastAPI(
    title="VibeDine API",
    description="Restaurant recommendation system",
    version="1.0.0"
)

app.include_router(
    recommendations_router
)

app.include_router(
    users_router
)

@app.get("/")
def root():
    return {"message": "VibeDine API is running"}

