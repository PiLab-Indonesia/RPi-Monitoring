"""Isolated SQLite model regression tests; no Raspberry Pi/network required."""
import sqlite3

import pytest

from app.models import Database


@pytest.fixture
def database(tmp_path):
    db = Database(str(tmp_path / "devices.db"))
    db.init_db()
    return db


def test_initial_database_is_empty(database):
    assert database.list_devices() == []


def test_upsert_creates_device_with_boolean_liveness(database):
    database.upsert_device("192.0.2.1", "Primary Pi", True)
    devices = database.list_devices()
    assert len(devices) == 1
    assert devices[0]["ip"] == "192.0.2.1"
    assert devices[0]["name"] == "Primary Pi"
    assert devices[0]["alive"] is True


def test_upsert_same_ip_updates_without_creating_duplicate(database):
    database.upsert_device("192.0.2.2", "Old name", True)
    existing = database.list_devices()[0]["id"]
    database.upsert_device("192.0.2.2", "Updated name", False)
    devices = database.list_devices()
    assert len(devices) == 1
    assert devices[0]["id"] == existing
    assert devices[0]["name"] == "Updated name"
    assert devices[0]["alive"] is False


def test_get_device_returns_one_device_by_id(database):
    database.upsert_device("192.0.2.3", "Living room", False)
    id_ = database.list_devices()[0]["id"]
    assert database.get_device(id_) == {
        "id": id_,
        "ip": "192.0.2.3",
        "name": "Living room",
        "alive": False,
    }


def test_get_device_missing_returns_none(database):
    assert database.get_device(999) is None


def test_unique_ip_constraint_and_other_rows_are_unchanged(database):
    database.upsert_device("192.0.2.4", "Sensor", True)
    with pytest.raises(sqlite3.IntegrityError):
        with database.conn() as conn:
            conn.execute(
                "INSERT INTO devices(ip, name) VALUES (?, ?)",
                ("192.0.2.4", "Duplicate"),
            )
    assert len(database.list_devices()) == 1


def test_upsert_allows_null_name(database):
    database.upsert_device("192.0.2.5", None, True)
    assert database.list_devices()[0]["name"] is None


def test_schema_init_is_repeatable(database):
    database.upsert_device("192.0.2.6", "Retained", True)
    database.init_db()
    assert database.list_devices()[0]["name"] == "Retained"
