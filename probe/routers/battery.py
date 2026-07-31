import uuid
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas.battery import BatteryCreate, BatteryRead, BatteryUpdate
from services import battery_service

router = APIRouter(prefix="/batteries", tags=["batteries"])

@router.get("/", response_model=list[BatteryRead])
def list_batteries(db: Session = Depends(get_db)):
    return battery_service.list_batteries(db)

@router.get("/{battery_id}", response_model=BatteryRead)
def get_battery(battery_id: uuid.UUID, db: Session = Depends(get_db)):
    db_battery = battery_service.get_battery(db, battery_id)
    if not db_battery:
        raise HTTPException(status_code=404, detail="Battery record not found")
    return db_battery

@router.post("/", response_model=BatteryRead, status_code=status.HTTP_201_CREATED)
def create_battery(data: BatteryCreate, db: Session = Depends(get_db)):
    try:
        return battery_service.create_battery(db, data)
    except Exception as err:
        raise HTTPException(status_code=400, detail=f"Failed to log battery: {str(err)}")

@router.put("/{battery_id}", response_model=BatteryRead)
def update_battery(battery_id: uuid.UUID, data: BatteryUpdate, db: Session = Depends(get_db)):
    db_battery = battery_service.update_battery(db, battery_id, data)
    if not db_battery:
        raise HTTPException(status_code=404, detail="Battery record not found")
    return db_battery

@router.delete("/{battery_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_battery(battery_id: uuid.UUID, db: Session = Depends(get_db)):
    success = battery_service.delete_battery(db, battery_id)
    if not success:
        raise HTTPException(status_code=404, detail="Battery record not found")
