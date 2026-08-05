import uuid

from sqlalchemy.orm import Session

from probe.models.sensor_reading import SensorReading


class SensorReadingRepository:
    def __init__(self):
        self.model = SensorReading

    def get(self, db: Session, id: uuid.UUID):
        return db.get(self.model, id)

    def get_all(self, db: Session):
        return db.query(self.model).all()

    def create(self, db: Session, data: dict):
        sensor_reading = self.model(**data)
        db.add(sensor_reading)
        db.commit()
        db.refresh(sensor_reading)
        return sensor_reading

    def update(self, db: Session, db_obj: SensorReading, data: dict):
        for field, value in data.items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, db_obj: SensorReading):
        db.delete(db_obj)
        db.commit()

sensor_reading_repository = SensorReadingRepository()