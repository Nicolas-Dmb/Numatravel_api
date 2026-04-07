from typing import Optional

from pydantic import BaseModel, Field


class Contact(BaseModel):
    first_name: str = Field(alias="firstName")
    last_name: str = Field(alias="lastName")
    email: str = Field(alias="email")
    message: str = Field(alias="message")
    phone: Optional[str] = Field(default=None, alias="phone")
