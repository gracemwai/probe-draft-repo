import uuid
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from probe.schemas.sensor_reading import SensorReadingCreate, SensorReadingRead, SensorReadingUpdate

from probe.services.sensor_reading import (
    get_sensor_reading,
    list_sensor_readings,
    create_sensor_reading,
    update_sensor_reading,
    delete_sensor_reading
)

router = APIRouter(prefix="/sensor-readings", tags=["sensor-readings"])

@router.get("/", response_model=list[SensorReadingRead])
def route_list_sensor_readings(db: Session = Depends(get_db)):
    return list_sensor_readings(db)

@router.get("/{sensor_reading_id}", response_model=SensorReadingRead)
def route_get_sensor_reading(sensor_reading_id: uuid.UUID, db: Session = Depends(get_db)):
    db_reading = get_sensor_reading(db, sensor_reading_id)
    if not db_reading:
        raise HTTPException(status_code=404, detail="Sensor reading record not found")
    return db_reading

@router.post("/", response_model=SensorReadingRead, status_code=status.HTTP_201_CREATED)
def route_create_sensor_reading(v_rest: float, v_load: float, data: SensorReadingCreate, db: Session = Depends(get_db)):
    try:
        return create_sensor_reading(db, data, v_rest, v_load)
    except Exception as err:
        raise HTTPException(status_code=400, detail=f"Failed to log sensor reading: {str(err)}")

@router.put("/{sensor_reading_id}", response_model=SensorReadingRead)
def route_update_sensor_reading(sensor_reading_id: uuid.UUID, data: SensorReadingUpdate, db: Session = Depends(get_db)):
    db_reading = update_sensor_reading(db, sensor_reading_id, data)
    if not db_reading:
        raise HTTPException(status_code=404, detail="Sensor reading record not found")
    return db_reading

@router.delete("/{sensor_reading_id}", status_code=status.HTTP_204_NO_CONTENT)
def route_delete_sensor_reading(sensor_reading_id: uuid.UUID, db: Session = Depends(get_db)):
    success = delete_sensor_reading(db, sensor_reading_id)
    if not success:
        raise HTTPException(status_code=404, detail="Sensor reading record not found")
