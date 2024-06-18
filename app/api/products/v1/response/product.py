from typing import Optional, Any
from pydantic import BaseModel


class Response(BaseModel):
    code: str
    status: str
    message: str
    result: Optional[Any] = None
