from pydantic import BaseModel
from typing import Optional, Any

class Response(BaseModel):
    code: str
    status: str
    message: str
    result: Optional[Any] = None
