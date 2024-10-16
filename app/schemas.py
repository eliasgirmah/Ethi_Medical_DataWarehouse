from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TransformData(BaseModel):
    message_id: int
    message_date: datetime
    final_message_text: str
    media_path: Optional[str] = None
    has_media: bool

    class Config:
        orm_mode = True  # This allows Pydantic to work with ORM models