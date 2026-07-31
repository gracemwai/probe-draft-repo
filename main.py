from database import Base, engine
from fastapi import FastAPI
import probe.models as models

Base.metadata.create_all(bind=engine)
app = FastAPI(title="probe API", version="1.0.0")

from routers import (
    user_router,
    device_router,
    battery_router,
    sensor_reading_router,
    booking_router
)

app = FastAPI()

app.include_router(user_router)
app.include_router(device_router)
app.include_router(battery_router)
app.include_router(sensor_reading_router)
app.include_router(booking_router)
