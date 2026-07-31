import uuid
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas.device import DeviceCreate, DeviceRead, DeviceUpdate
from services import device_service

router = APIRouter(prefix="/devices", tags=["devices"])

@router.get("/", response_model=list[DeviceRead])
def list_devices(db: Session = Depends(get_db)):
    return device_service.list_devices(db)

@router.get("/{device_id}", response_model=DeviceRead)
def get_device(device_id: uuid.UUID, db: Session = Depends(get_db)):
    db_device = device_service.get_device(db, device_id)
    if not db_device:
        raise HTTPException(status_code=404, detail="Device record not found")
    return db_device

@router.post("/", response_model=DeviceRead, status_code=status.HTTP_201_CREATED)
def create_device(data: DeviceCreate, db: Session = Depends(get_db)):
    try:
        return device_service.create_device(db, data)
    except Exception as err:
        raise HTTPException(status_code=400, detail=f"Failed to log device: {str(err)}")

@router.put("/{device_id}", response_model=DeviceRead)
def update_device(device_id: uuid.UUID, data: DeviceUpdate, db: Session = Depends(get_db)):
    db_device = device_service.update_device(db, device_id, data)
    if not db_device:
        raise HTTPException(status_code=404, detail="Device record not found")
    return db_device

@router.delete("/{device_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_device(device_id: uuid.UUID, db: Session = Depends(get_db)):
    success = device_service.delete_device(db, device_id)
    if not success:
        raise HTTPException(status_code=404, detail="Device record not found")
