from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DowntimeCreate(BaseModel):
    machine_id: str
    start_time: datetime
    end_time: Optional[datetime] = None
    reason: Optional[str] = None

class DowntimeResponse(DowntimeCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True