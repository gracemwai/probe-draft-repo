import uuid
from typing import List, Optional

from sqlalchemy.orm import Session

from ..models.sensor_reading import SensorReading


class SensorReadingRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, reading_id: uuid.UUID) -> Optional[SensorReading]:
        return self.db.query(SensorReading).filter(SensorReading.sensor_reading_id == reading_id).first()

    def get_all(self) -> List[SensorReading]:
        return self.db.query(SensorReading).all()

    def create(self, sensor_reading: SensorReading) -> SensorReading:
        self.db.add(sensor_reading)
        self.db.commit()
        self.db.refresh(sensor_reading)
        return sensor_reading

    def update(self, reading_id: uuid.UUID, **kwargs) -> Optional[SensorReading]:
        db_reading = self.get_by_id(reading_id)
        if db_reading:
            for key, value in kwargs.items():
                setattr(db_reading, key, value)
            self.db.commit()
            self.db.refresh(db_reading)
        return db_reading

    def delete(self, reading_id: uuid.UUID) -> bool:
        db_reading = self.get_by_id(reading_id)
        if db_reading:
            self.db.delete(db_reading)
            self.db.commit()
            return True
        return False
