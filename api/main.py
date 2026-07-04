from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from api.routes.recommendations import (
    router as recommendations_router
)
from api.routes.users import (
    router as users_router
)
from api.routes.groups import (
    router as groups_router
)
from api.routes.mongo_tests import (
    router as mongoTest_router
)
from api.routes.restaurants import (
    router as restaurants_router
)

app = FastAPI(
    title="VibeDine API",
    description="Restaurant recommendation system",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(recommendations_router)
app.include_router(users_router)
app.include_router(groups_router)
app.include_router(mongoTest_router)
app.include_router(restaurants_router, prefix="/restaurants")


@app.get("/")
def root():
    return {"message": "VibeDine API is running"}
