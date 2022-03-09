# from app.routers import refugee_family_names
from fastapi import FastAPI
from .routers import refugees, keywords, equivalentkeywords

from mangum import Mangum

app = FastAPI(
    title="Robota Express API",
    # methods=['GET', 'POST']
    # openapi_prefix="/prod"
)


@app.get("/", tags=["Root"])
def read_root() -> dict:
    return {"message": "welcome to Robota Express API! Go to /docs for the swagger"}

app.include_router(refugees.router, tags=["Refugees"])
app.include_router(keywords.router, tags=["Keywords"])
app.include_router(equivalentkeywords.router, tags=["Equivalent Keywords"])

# handler = Mangum(app, lifespan="off")
