from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from repository.booking_repository import booking_repository
from repository.user_repository import user_repository
from repository.battery_repository import battery_repository
from schemas.booking import BookingCreate, BookingUpdate

def get_booking(db: Session, booking_id: str):
    booking = booking_repository.get(db, booking_id)
    if not booking:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking record not found")
    return booking

def list_bookings(db: Session):
    return booking_repository.get_all(db)

def create_booking(db: Session, data: BookingCreate):
 
    if not data.status.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Initial workflow tracking state cannot be empty."
        )

    buyer = user_repository.get(db, data.user_id)
    if not buyer or buyer.user_type != "second_life_buyer":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Access Denied: Account role unauthorized to initialize purchasing transactions."
        )

    battery = battery_repository.get(db, data.battery_id)
    if not battery:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Target hardware entity profile not found."
        )
        
    if battery.status != "available":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Transaction Conflict: Asset locked by another operational session."
        )

    battery_repository.update(db, battery, {"status": "reserved"})

    dumped_data = data.model_dump()
    dumped_data["status"] = data.status.strip()
    return booking_repository.create(db, dumped_data)

def update_booking(db: Session, booking_id: str, data: BookingUpdate):
    booking = get_booking(db, booking_id)
    return booking_repository.update(db, booking, data.model_dump(exclude_unset=True))

def delete_booking(db: Session, booking_id: str):
    booking = get_booking(db, booking_id)
    return booking_repository.delete(db, booking)
