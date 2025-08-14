from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List
import uvicorn
from .models import Database
from .config import settings

app = FastAPI(title=settings.app_name)
db = Database(settings.db_path)

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

# include extra api routers (auth, admin, reports, metrics)
from .api_auth import router as auth_router
from .api_extra import router as extra_router  # will be added next
from .metrics import router as metrics_router   # will be added next

app.include_router(auth_router)
app.include_router(extra_router)
app.include_router(metrics_router)

if __name__ == '__main__':
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000)
