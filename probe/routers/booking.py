import uuid
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas.booking import BookingCreate, BookingRead, BookingUpdate
from services import booking_service

router = APIRouter(prefix="/bookings", tags=["bookings"])

@router.get("/", response_model=list[BookingRead])
def list_bookings(db: Session = Depends(get_db)):
    return booking_service.list_bookings(db)

@router.get("/{booking_id}", response_model=BookingRead)
def get_booking(booking_id: uuid.UUID, db: Session = Depends(get_db)):
    db_booking = booking_service.get_booking(db, booking_id)
    if not db_booking:
        raise HTTPException(status_code=404, detail="Booking record not found")
    return db_booking

@router.post("/", response_model=BookingRead, status_code=status.HTTP_201_CREATED)
def create_booking(data: BookingCreate, db: Session = Depends(get_db)):
    try:
        return booking_service.create_booking(db, data)
    except Exception as err:
        raise HTTPException(status_code=400, detail=f"Failed to create booking: {str(err)}")

@router.put("/{booking_id}", response_model=BookingRead)
def update_booking(booking_id: uuid.UUID, data: BookingUpdate, db: Session = Depends(get_db)):
    db_booking = booking_service.update_booking(db, booking_id, data)
    if not db_booking:
        raise HTTPException(status_code=404, detail="Booking record not found")
    return db_booking

@router.delete("/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_booking(booking_id: uuid.UUID, db: Session = Depends(get_db)):
    success = booking_service.delete_booking(db, booking_id)
    if not success:
        raise HTTPException(status_code=404, detail="Booking record not found")
