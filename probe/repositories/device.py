import uuid
from typing import List, Optional

from sqlalchemy.orm import Session

from ..models.device import Device


class DeviceRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, device_id: uuid.UUID) -> Optional[Device]:
        return self.db.query(Device).filter(Device.device_id == device_id).first()

    def get_all(self) -> List[Device]:
        return self.db.query(Device).all()

    def create(self, device: Device) -> Device:
        self.db.add(device)
        self.db.commit()
        self.db.refresh(device)
        return device

    def update(self, device_id: uuid.UUID, **kwargs) -> Optional[Device]:
        db_device = self.get_by_id(device_id)
        if db_device:
            for key, value in kwargs.items():
                setattr(db_device, key, value)
            self.db.commit()
            self.db.refresh(db_device)
        return db_device

    def delete(self, device_id: uuid.UUID) -> bool:
        db_device = self.get_by_id(device_id)
        if db_device:
            self.db.delete(db_device)
            self.db.commit()
            return True
        return False
