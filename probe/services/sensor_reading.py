from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from repository.sensor_reading_repository import sensor_reading_repository
from repository.battery_repository import battery_repository
from repository.device_repository import device_repository
from schemas.sensor_reading import SensorReadingCreate, SensorReadingUpdate

R_NEW = 0.020   
R_DEAD = 0.120  

def get_sensor_reading(db: Session, sensor_reading_id: str):
    reading = sensor_reading_repository.get(db, sensor_reading_id)
    if not reading:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Telemetry entry not found")
    return reading

def list_sensor_readings(db: Session):
    return sensor_reading_repository.get_all(db)

def create_sensor_reading(db: Session, data: SensorReadingCreate, v_rest: float, v_load: float):
   
    device = device_repository.get(db, data.device_id)
    battery = battery_repository.get(db, data.battery_id)
    if not device or not battery:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Hardware Authentication Failure: Unmapped device or battery parameters."
        )

    if data.temp > 55.0:
      
        battery_repository.update(db, battery, {"status": "Hazardous/Isolate"})
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Emergency Cutoff: High-temperature hazard detected. Slot offline and asset quarantined."
        )

    if data.current <= 0:
        soh_percentage = 0.0
    else:
        r_i = (v_rest - v_load) / data.current
        soh_fraction = (R_DEAD - r_i) / (R_DEAD - R_NEW)
        soh_percentage = max(0.0, min(100.0, soh_fraction * 100.0))

    if soh_percentage > 65.0:
        battery_updates = {"category": "A", "status": "available"}
    elif 50.0 <= soh_percentage <= 65.0:
        battery_updates = {"category": "B", "status": "available"}
    else:
        battery_updates = {"category": "C", "status": "testing_aborted"}

    battery_repository.update(db, battery, battery_updates)

    dumped_data = data.model_dump()
    dumped_data["state_of_health"] = soh_percentage
    dumped_data["voltage"] = v_load 
    
    return sensor_reading_repository.create(db, dumped_data)

def update_sensor_reading(db: Session, sensor_reading_id: str, data: SensorReadingUpdate):
    reading = get_sensor_reading(db, sensor_reading_id)
    return sensor_reading_repository.update(db, reading, data.model_dump(exclude_unset=True))

def delete_sensor_reading(db: Session, sensor_reading_id: str):
    reading = get_sensor_reading(db, sensor_reading_id)
    return sensor_reading_repository.delete(db, reading)
