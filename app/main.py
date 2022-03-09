# from app.routers import refugee_family_names
from fastapi import FastAPI
from .routers import players, teams, seasons, refugees

from mangum import Mangum

app = FastAPI(
    title="FastAPI-PostgreSQL-AWS-Lambda",
    # openapi_prefix="/prod"
)

# app.include_router(players.router, tags=["Players"])
# app.include_router(teams.router, tags=["Teams"])
# app.include_router(seasons.router, tags=["Seasons"])
# app.include_router(refugee_family_names.router, tags=["Refugee family names"])
app.include_router(refugees.router, tags=["Refugees"])

handler = Mangum(app, lifespan="off")
