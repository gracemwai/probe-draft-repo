from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

class SensorReadingBase(BaseModel):
    device_id: UUID
    battery_id: UUID
    temp: float
    voltage: float
    current: float
    state_of_health: float
    
class SensorReadingCreate(SensorReadingBase):
    pass

class SensorReadingUpdate(BaseModel):
    device_id: UUID | None = None
    battery_id: UUID | None = None
    temp: float | None = None
    voltage: float | None = None
    current: float | None = None
    state_of_health: float | None = None
      
class SensorReadingRead(SensorReadingBase):
    model_config = ConfigDict(from_attributes=True)
    
    sensor_reading_id: UUID
    created_at: datetime
