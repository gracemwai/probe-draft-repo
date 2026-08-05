import uuid

from sqlalchemy.orm import Session

from probe.models.device import Device


class DeviceRepository:
    def __init__(self):
        self.model = Device

    def get(self, db: Session, id: uuid.UUID):
        return db.get(self.model, id)

    def get_all(self, db: Session):
        return db.query(self.model).all()

    def create(self, db: Session, data: dict):
        device = self.model(**data)
        db.add(device)
        db.commit()
        db.refresh(device)
        return device

    def update(self, db: Session, db_obj: Device, data: dict):
        for field, value in data.items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, db_obj: Device):
        db.delete(db_obj)
        db.commit()

device_repository = DeviceRepository()