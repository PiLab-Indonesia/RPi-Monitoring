"""Functional regression tests for Prometheus scraping without live devices."""
from fastapi import FastAPI
from fastapi.testclient import TestClient
from prometheus_client.parser import text_string_to_metric_families

from app.metrics import create_metrics_router
from app.models import Database


def create_client(tmp_path):
    db = Database(str(tmp_path / "metrics.db"))
    db.init_db()
    app = FastAPI()
    app.include_router(create_metrics_router(db))
    return db, TestClient(app)


def parse_gauges(response):
    return {
        sample.name: sample.value
        for metric in text_string_to_metric_families(response.text)
        for sample in metric.samples
        if sample.name.startswith("rpi_devices_")
    }


def test_metrics_empty_database(tmp_path):
    _, client = create_client(tmp_path)
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "text/plain" in response.headers["content-type"]
    assert parse_gauges(response) == {
        "rpi_devices_total": 0,
        "rpi_devices_alive": 0,
        "rpi_devices_down": 0,
    }


def test_metrics_mixed_device_states(tmp_path):
    db, client = create_client(tmp_path)
    db.upsert_device("192.0.2.1", "alpha", True)
    db.upsert_device("192.0.2.2", "beta", False)
    db.upsert_device("192.0.2.3", "gamma", True)
    response = client.get("/metrics")
    assert response.status_code == 200
    assert parse_gauges(response) == {
        "rpi_devices_total": 3,
        "rpi_devices_alive": 2,
        "rpi_devices_down": 1,
    }


def test_metrics_refresh_after_state_change(tmp_path):
    db, client = create_client(tmp_path)
    db.upsert_device("192.0.2.1", "alpha", True)
    assert parse_gauges(client.get("/metrics"))["rpi_devices_alive"] == 1
    db.upsert_device("192.0.2.1", "alpha", False)
    assert parse_gauges(client.get("/metrics")) == {
        "rpi_devices_total": 1,
        "rpi_devices_alive": 0,
        "rpi_devices_down": 1,
    }


def test_metrics_concurrent_scrapes_are_independent(tmp_path):
    db, client = create_client(tmp_path)
    db.upsert_device("192.0.2.1", "alpha", True)
    for _ in range(3):
        response = client.get("/metrics")
        assert response.status_code == 200
        assert parse_gauges(response)["rpi_devices_total"] == 1


def test_metrics_not_listed_in_openapi(tmp_path):
    _, client = create_client(tmp_path)
    assert "/metrics" not in client.get("/openapi.json").json()["paths"]
