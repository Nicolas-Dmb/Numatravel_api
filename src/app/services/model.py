from typing import Optional

from pydantic import BaseModel


class ClientError(BaseModel):
    message: str
    url: Optional[str] = None
    userAgent: Optional[str] = None
    timestamp: Optional[str] = None
    stack: Optional[str] = None
