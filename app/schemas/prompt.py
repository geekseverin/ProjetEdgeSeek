from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class PromptCreate(BaseModel):
    symptoms: str

class PromptRead(BaseModel):
    id: int
    symptoms: str
    ai_response: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
