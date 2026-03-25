from pydantic import BaseModel, EmailStr
from typing import Literal

class SignupRequest(BaseModel):
    email: EmailStr
    password: str
    stream: Literal["science", "commerce", "arts"]

class LoginRequest(BaseModel):
    email: EmailStr
    password: str