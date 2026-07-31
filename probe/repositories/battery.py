import uuid
from typing import List, Optional

from sqlalchemy.orm import Session

from ..models.battery import Battery


class BatteryRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, battery_id: uuid.UUID) -> Optional[Battery]:
        return self.db.query(Battery).filter(Battery.battery_id == battery_id).first()

    def get_all(self) -> List[Battery]:
        return self.db.query(Battery).all()

    def create(self, battery: Battery) -> Battery:
        self.db.add(battery)
        self.db.commit()
        self.db.refresh(battery)
        return battery

    def update(self, battery_id: uuid.UUID, **kwargs) -> Optional[Battery]:
        db_battery = self.get_by_id(battery_id)
        if db_battery:
            for key, value in kwargs.items():
                setattr(db_battery, key, value)
            self.db.commit()
            self.db.refresh(db_battery)
        return db_battery

    def delete(self, battery_id: uuid.UUID) -> bool:
        db_battery = self.get_by_id(battery_id)
        if db_battery:
            self.db.delete(db_battery)
            self.db.commit()
            return True
        return False
