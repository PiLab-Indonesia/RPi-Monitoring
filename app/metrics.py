"""Prometheus metrics for device state in the local monitoring database."""
from fastapi import APIRouter, Response
from prometheus_client import CONTENT_TYPE_LATEST, CollectorRegistry, Gauge, generate_latest

from .models import Database


def create_metrics_router(db: Database) -> APIRouter:
    """Bind a /metrics endpoint to the database used by the API.

    Metrics reflect a fresh SQLite snapshot on every scrape. A private
    registry avoids exposing unrelated process-wide metrics or stale gauges.
    """
    router = APIRouter()

    @router.get("/metrics", include_in_schema=False)
    def metrics():
        with db.conn() as conn:
            total, alive = conn.execute(
                "SELECT COUNT(*), COALESCE(SUM(CASE WHEN alive != 0 THEN 1 ELSE 0 END), 0)"
                " FROM devices"
            ).fetchone()

        registry = CollectorRegistry()
        Gauge("rpi_devices_total", "Number of monitored devices", registry=registry).set(total)
        Gauge("rpi_devices_alive", "Number of reachable devices", registry=registry).set(alive)
        Gauge("rpi_devices_down", "Number of unreachable devices", registry=registry).set(total - alive)
        return Response(content=generate_latest(registry), media_type=CONTENT_TYPE_LATEST)

    return router
