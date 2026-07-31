import uuid
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas.sensor_reading import SensorReadingCreate, SensorReadingRead, SensorReadingUpdate
from services import sensor_reading_service

router = APIRouter(prefix="/sensor-readings", tags=["sensor-readings"])

@router.get("/", response_model=list[SensorReadingRead])
def list_sensor_readings(db: Session = Depends(get_db)):
    return sensor_reading_service.list_sensor_readings(db)

@router.get("/{sensor_reading_id}", response_model=SensorReadingRead)
def get_sensor_reading(sensor_reading_id: uuid.UUID, db: Session = Depends(get_db)):
    db_reading = sensor_reading_service.get_sensor_reading(db, sensor_reading_id)
    if not db_reading:
        raise HTTPException(status_code=404, detail="Sensor reading record not found")
    return db_reading

@router.post("/", response_model=SensorReadingRead, status_code=status.HTTP_201_CREATED)
def create_sensor_reading(data: SensorReadingCreate, db: Session = Depends(get_db)):
    try:
        return sensor_reading_service.create_sensor_reading(db, data)
    except Exception as err:
        raise HTTPException(status_code=400, detail=f"Failed to log sensor reading: {str(err)}")

@router.put("/{sensor_reading_id}", response_model=SensorReadingRead)
def update_sensor_reading(sensor_reading_id: uuid.UUID, data: SensorReadingUpdate, db: Session = Depends(get_db)):
    db_reading = sensor_reading_service.update_sensor_reading(db, sensor_reading_id, data)
    if not db_reading:
        raise HTTPException(status_code=404, detail="Sensor reading record not found")
    return db_reading

@router.delete("/{sensor_reading_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_sensor_reading(sensor_reading_id: uuid.UUID, db: Session = Depends(get_db)):
    success = sensor_reading_service.delete_sensor_reading(db, sensor_reading_id)
    if not success:
        raise HTTPException(status_code=404, detail="Sensor reading record not found")
