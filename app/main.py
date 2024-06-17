from typing import Annotated
from starlette.middleware.cors import CORSMiddleware 
from core.router import api_router
from db.init_db import init_db
from db.session import SessionLocal
from core.config import settings
from fastapi import FastAPI 
app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)


@app.on_event("startup")
def on_startup():
    init_db()

if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin)
                       for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

@app.get("/")
def read_root():
    return {"Hello": "World"}


app.include_router(api_router, prefix=settings.API_V1_STR)
