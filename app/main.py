from fastapi import FastAPI
from .database import engine, Base
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from .routers import locations, users, api_locations

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Weather API",
    version="1.0.0",
    docs_url="/docs",
    openapi_url="/openapi.json"
)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(users.router)
app.include_router(locations.router)
app.include_router(api_locations.router, prefix="/api")
