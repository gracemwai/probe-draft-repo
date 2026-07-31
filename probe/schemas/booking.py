from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

class BookingBase(BaseModel):
    user_id: UUID
    battery_id: UUID
    status: str
    
class BookingCreate(BookingBase):
    pass

class BookingUpdate(BaseModel):
    user_id: UUID | None = None
    battery_id: UUID | None = None
    status: str | None = None
      
class BookingRead(BookingBase):
    model_config = ConfigDict(from_attributes=True)
    
    booking_id: UUID
    created_at: datetime
