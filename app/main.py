# from app.routers import refugee_family_names
from fastapi import FastAPI
from .routers import players, teams, seasons, refugees

from mangum import Mangum

app = FastAPI(
    title="Robota Express API",
    # openapi_prefix="/prod"
)


@app.get("/", tags=["Root"])
def read_root() -> dict:
    return {"message": "welcome to Robota Express API! Go to /docs for the swagger"}


# app.include_router(players.router, tags=["Players"])
# app.include_router(teams.router, tags=["Teams"])
# app.include_router(seasons.router, tags=["Seasons"])
app.include_router(refugees.router, tags=["Refugees"])

# handler = Mangum(app, lifespan="off")
