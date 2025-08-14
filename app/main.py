from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import uvicorn
from .models import Database, Device

app = FastAPI(title="RPi Network Monitoring System")
db = Database('data/rpi_nms.db')

class DeviceOut(BaseModel):
    id: int
    ip: str
    name: str | None
    alive: bool

@app.on_event("startup")
async def startup_event():
    db.init_db()

@app.get("/", summary="Health")
async def health():
    return {"status": "ok", "version": __import__("app").__version__}

@app.get("/devices", response_model=List[DeviceOut])
async def list_devices():
    devices = db.list_devices()
    return [DeviceOut(**d) for d in devices]

@app.get("/devices/{device_id}")
async def get_device(device_id: int):
    d = db.get_device(device_id)
    if not d:
        raise HTTPException(status_code=404, detail="device not found")
    return d

if __name__ == '__main__':
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000)
