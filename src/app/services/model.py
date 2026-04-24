from typing import Optional

from pydantic import BaseModel


class ClientError(BaseModel):
    message: str
    url: Optional[str] = None
    timestamp: Optional[str] = None
    stack: Optional[str] = None
    pathname: Optional[str] = None
    isMetaRoute: Optional[bool] = None
    hasCookieConsent: Optional[str] = None
    fbp: Optional[str] = None
    fbc: Optional[str] = None
    referrer: Optional[str] = None
    # window.error specific
    file: Optional[str] = None
    line: Optional[int] = None
    column: Optional[int] = None
    # unhandledrejection specific
    type: Optional[str] = None
