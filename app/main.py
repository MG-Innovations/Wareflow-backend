from typing import Annotated

from fastapi import FastAPI
import model
from config import engine
import router
app = FastAPI()


model.Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"Hello": "World"}


app.include_router(router.router,prefix="/product",tags=["product"])