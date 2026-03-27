from pydantic import BaseModel, EmailStr, Field
from typing import Literal, Optional

class SignupRequest(BaseModel):
    name: Optional[str] = None
    email: EmailStr
    password: str = Field(min_length=6)
    stream: Literal["science", "commerce", "arts"]

class LoginRequest(BaseModel):
    email: EmailStr
    password: str