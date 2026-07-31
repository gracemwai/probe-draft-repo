from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from repository.device_repository import device_repository
from repository.user_repository import user_repository
from schemas.device import DeviceCreate, DeviceUpdate

def get_device(db: Session, device_id: str):
    device = device_repository.get(db, device_id)
    if not device:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Device not found")
    return device

def list_devices(db: Session):
    return device_repository.get_all(db)

def create_device(db: Session, data: DeviceCreate):

    clean_channel = data.channel.strip()
    clean_status = data.status.strip()
    
    if not clean_channel or not clean_status:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Required hardware configuration values cannot be empty or whitespaces."
        )

    recycler = user_repository.get(db, data.recycler_id)
    if not recycler:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="The managing owner user profile does not exist."
        )

    if recycler.user_type != "recycler":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Security Violation: Only registered recycler entities can manage screening hardware units."
        )
        
    dumped_data = data.model_dump()
    dumped_data["channel"] = clean_channel
    dumped_data["status"] = clean_status
    if data.description:
        dumped_data["description"] = data.description.strip()
    if data.error_code:
        dumped_data["error_code"] = data.error_code.strip()

    return device_repository.create(db, dumped_data)

def update_device(db: Session, device_id: str, data: DeviceUpdate):
    device = get_device(db, device_id)
    return device_repository.update(db, device, data.model_dump(exclude_unset=True))

def delete_device(db: Session, device_id: str):
    device = get_device(db, device_id)
    return device_repository.delete(db, device)
