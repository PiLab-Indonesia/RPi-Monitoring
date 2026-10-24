"""Configuration regression tests: typed env, dotenv, and shared database path."""
import importlib

import pytest

from app import config


def test_defaults_without_env_file(monkeypatch):
    for key in ("APP_NAME", "DB_PATH", "SCAN_INTERVAL_MINUTES", "TELEGRAM_TOKEN"):
        monkeypatch.delenv(key, raising=False)
    settings = config.Settings(_env_file=None)
    assert settings.app_name == "RPi-NMS"
    assert settings.db_path == "data/rpi_nms.db"
    assert settings.scan_interval_minutes == 5
    assert settings.telegram_token is None


def test_environment_variables_override_defaults(monkeypatch, tmp_path):
    db_path = tmp_path / "configured" / "devices.db"
    monkeypatch.setenv("DB_PATH", str(db_path))
    monkeypatch.setenv("APP_NAME", "Testing RPi")
    monkeypatch.setenv("SCAN_INTERVAL_MINUTES", "17")
    monkeypatch.setenv("TELEGRAM_TOKEN", "dummy-test-value")
    loaded = config.Settings(_env_file=None)
    assert loaded.db_path == str(db_path)
    assert loaded.app_name == "Testing RPi"
    assert loaded.scan_interval_minutes == 17
    assert loaded.telegram_token == "dummy-test-value"


def test_invalid_scan_interval_is_rejected(monkeypatch):
    monkeypatch.setenv("SCAN_INTERVAL_MINUTES", "not-an-integer")
    with pytest.raises(ValueError):
        config.Settings(_env_file=None)


def test_dotenv_file_and_environment_precedence(monkeypatch, tmp_path):
    pytest.importorskip("dotenv")
    env_file = tmp_path / ".env"
    env_file.write_text(
        "APP_NAME=From file\nDB_PATH=from_file.db\nSCAN_INTERVAL_MINUTES=12\n",
        encoding="utf-8",
    )
    monkeypatch.delenv("DB_PATH", raising=False)
    monkeypatch.delenv("SCAN_INTERVAL_MINUTES", raising=False)
    monkeypatch.setenv("APP_NAME", "From environment")
    loaded = config.Settings(_env_file=env_file)
    assert loaded.db_path == "from_file.db"
    assert loaded.scan_interval_minutes == 12
    assert loaded.app_name == "From environment"


def test_main_api_uses_shared_settings(monkeypatch, tmp_path):
    db_path = tmp_path / "api" / "devices.db"
    monkeypatch.setenv("APP_NAME", "My Raspberry Pis")
    monkeypatch.setenv("DB_PATH", str(db_path))
    new_settings = config.Settings(_env_file=None)
    monkeypatch.setattr(config, "settings", new_settings)
    from app import main
    module = importlib.reload(main)
    assert module.db.path == str(db_path)
    assert module.app.title == "My Raspberry Pis"
    module.db.init_db()
    assert db_path.is_file()


def test_discovery_uses_configured_db_unless_explicitly_overridden(monkeypatch, tmp_path):
    db_path = tmp_path / "discover" / "db.sqlite"
    monkeypatch.setattr(config.settings, "db_path", str(db_path))
    from app.autodiscover import ArpDiscover
    instance = ArpDiscover()
    assert instance.db.path == str(db_path)
    assert db_path.exists()
    custom = tmp_path / "custom" / "db.sqlite"
    assert ArpDiscover(db_path=str(custom)).db.path == str(custom)
