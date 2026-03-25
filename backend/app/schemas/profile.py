from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime

class ProfileResponse(BaseModel):
    id: int
    user_id: int
    stream: str
    created_at: datetime

    class Config:
        from_attributes = True