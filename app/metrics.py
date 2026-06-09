"""
app/metrics.py — Prometheus metrics endpoint for RPi NMS.

Exposes /metrics with three gauges:
  rpi_nms_devices_total  — total registered devices
  rpi_nms_devices_alive  — devices currently marked alive
  rpi_nms_devices_down   — devices currently marked down (not alive)

Add prometheus-client to your requirements to use this module.
"""

from fastapi import APIRouter
from fastapi.responses import PlainTextResponse
from prometheus_client import (
    CollectorRegistry,
    Gauge,
    generate_latest,
    CONTENT_TYPE_LATEST,
)
from .models import Database
from .config import settings

router = APIRouter(tags=["metrics"])

# Per-request registry so we re-compute on every scrape
_registry = CollectorRegistry()

_g_total = Gauge(
    "rpi_nms_devices_total",
    "Total number of registered devices",
    registry=_registry,
)
_g_alive = Gauge(
    "rpi_nms_devices_alive",
    "Number of devices currently alive",
    registry=_registry,
)
_g_down = Gauge(
    "rpi_nms_devices_down",
    "Number of devices currently down (not alive)",
    registry=_registry,
)


@router.get(
    "/metrics",
    response_class=PlainTextResponse,
    summary="Prometheus metrics",
    description="Returns device counts as Prometheus text exposition format.",
)
async def prometheus_metrics() -> PlainTextResponse:
    """Scrape endpoint for Prometheus."""
    db = Database(settings.db_path)
    devices = db.list_devices()

    total = len(devices)
    alive = sum(1 for d in devices if d["alive"])
    down = total - alive

    _g_total.set(total)
    _g_alive.set(alive)
    _g_down.set(down)

    data = generate_latest(_registry)
    return PlainTextResponse(content=data, media_type=CONTENT_TYPE_LATEST)
