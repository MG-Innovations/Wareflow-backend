from fastapi import FastAPI
from api import router
from config import engine
from api.products.models.product import Base

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"Hello": "World"}

# Include the main router
app.include_router(router)
