from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from uuid import UUID


from ..repositories import SensorReadingRepository, BatteryRepository, DeviceRepository
from ..schemas.sensor_reading import SensorReadingCreate, SensorReadingUpdate

R_NEW = 0.020   
R_DEAD = 0.120  

def get_sensor_reading(db: Session, sensor_reading_id: UUID):
  
    reading = SensorReadingRepository.get_by_id(db, sensor_reading_id)
    if not reading:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Telemetry entry not found")
    return reading

def list_sensor_readings(db: Session):
    return SensorReadingRepository.get_all(db)

def create_sensor_reading(db: Session, data: SensorReadingCreate, v_rest: float, v_load: float):
    device = DeviceRepository.get_by_id(db, data.device_id)
    battery = BatteryRepository.get_by_id(db, data.battery_id)
    if not device or not battery:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Hardware Authentication Failure: Unmapped device or battery parameters."
        )

    if data.temp > 55.0:
    
        BatteryRepository.update(db, battery, {"status": "INACTIVE"})
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
        battery_updates = {"category": "A", "status": "AVAILABLE"}
    elif 50.0 <= soh_percentage <= 65.0:
        battery_updates = {"category": "B", "status": "AVAILABLE"}
    else:
        battery_updates = {"category": "C", "status": "PROCESSING"}

    BatteryRepository.update(db, battery, battery_updates)

    dumped_data = data.model_dump()
    dumped_data["state_of_health"] = soh_percentage
    dumped_data["voltage"] = v_load 
    
    return SensorReadingRepository.create(db, dumped_data)

def update_sensor_reading(db: Session, sensor_reading_id: UUID, data: SensorReadingUpdate):
    reading = get_sensor_reading(db, sensor_reading_id)
    return SensorReadingRepository.update(db, reading, data.model_dump(exclude_unset=True))

def delete_sensor_reading(db: Session, sensor_reading_id: UUID):
    reading = get_sensor_reading(db, sensor_reading_id)
    return SensorReadingRepository.delete(db, reading)
