from fastapi import FastAPI

from api.routes.recommendations import (
    router as recommendations_router
)
from api.routes.users import (
    router as users_router
)
from api.routes.mongo_tests import (
    router as mongoTest_router
)

app = FastAPI(
    title="VibeDine API",
    description="Restaurant recommendation system",
    version="1.0.0"
)

routers = [
    recommendations_router,
    users_router,
    mongoTest_router
]

for router in routers:
    app.include_router(router)


@app.get("/")
def root():
    return {"message": "VibeDine API is running"}

