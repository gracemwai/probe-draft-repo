import uuid
from typing import List, Optional

from sqlalchemy.orm import Session

from ..models.booking import Booking


class BookingRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, booking_id: uuid.UUID) -> Optional[Booking]:
        return self.db.query(Booking).filter(Booking.booking_id == booking_id).first()

    def get_all(self) -> List[Booking]:
        return self.db.query(Booking).all()

    def create(self, booking: Booking) -> Booking:
        self.db.add(booking)
        self.db.commit()
        self.db.refresh(booking)
        return booking

    def update(self, booking_id: uuid.UUID, **kwargs) -> Optional[Booking]:
        db_booking = self.get_by_id(booking_id)
        if db_booking:
            for key, value in kwargs.items():
                setattr(db_booking, key, value)
            self.db.commit()
            self.db.refresh(db_booking)
        return db_booking

    def delete(self, booking_id: uuid.UUID) -> bool:
        db_booking = self.get_by_id(booking_id)
        if db_booking:
            self.db.delete(db_booking)
            self.db.commit()
            return True
        return False
