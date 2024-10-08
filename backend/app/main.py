from starlette.middleware.cors import CORSMiddleware
from app.core.router import api_router
from app.db.init_db import init_db
from app.core.config import settings
from fastapi import FastAPI


app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)


@app.get("/")
async def root():
    # logger.debug('this is a debug message')
    return {"message": "Hello World"}


@app.on_event("startup")
def on_startup():
    init_db()


if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.get("/")
def read_root():
    return {"Hello": "World"}


app.include_router(api_router, prefix=settings.API_V1_STR)
