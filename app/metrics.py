from fastapi import APIRouter, Response
from prometheus_client import Gauge, generate_latest, CONTENT_TYPE_LATEST
from .models import Database

router = APIRouter(tags=["metrics"])
db = Database()

g_total = Gauge('rpi_nms_devices_total', 'Total discovered devices')
g_alive = Gauge('rpi_nms_devices_alive', 'Devices alive')
g_down = Gauge('rpi_nms_devices_down', 'Devices down')

@router.get("/metrics")
def metrics():
    devices = db.list_devices()
    total = len(devices)
    alive = sum(1 for d in devices if d['alive'])
    down = total - alive
    g_total.set(total)
    g_alive.set(alive)
    g_down.set(down)
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
