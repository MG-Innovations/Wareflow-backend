from db.base import Base 
from db.session import engine

def init_db() -> None:
    Base.metadata.create_all(bind=engine)   # type: ignore

    