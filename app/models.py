import sqlite3
import os
from typing import List, Dict

SCHEMA = """
CREATE TABLE IF NOT EXISTS devices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ip TEXT UNIQUE NOT NULL,
    name TEXT,
    alive INTEGER DEFAULT 0,
    last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

class Database:
    def __init__(self, path: str = 'data/rpi_nms.db'):
        self.path = path
        os.makedirs(os.path.dirname(self.path), exist_ok=True)

    def conn(self):
        return sqlite3.connect(self.path, check_same_thread=False)

    def init_db(self):
        with self.conn() as c:
            c.executescript(SCHEMA)

    def upsert_device(self, ip: str, name: str | None, alive: bool):
        with self.conn() as c:
            c.execute(
                "INSERT INTO devices(ip, name, alive, last_seen) VALUES (?, ?, ?, CURRENT_TIMESTAMP)"
                " ON CONFLICT(ip) DO UPDATE SET name=excluded.name, alive=excluded.alive, last_seen=CURRENT_TIMESTAMP",
                (ip, name, int(alive)),
            )

    def list_devices(self) -> List[Dict]:
        with self.conn() as c:
            rows = c.execute("SELECT id, ip, name, alive FROM devices ORDER BY last_seen DESC").fetchall()
            return [dict(id=r[0], ip=r[1], name=r[2], alive=bool(r[3])) for r in rows]

    def get_device(self, device_id: int):
        with self.conn() as c:
            r = c.execute("SELECT id, ip, name, alive FROM devices WHERE id=?", (device_id,)).fetchone()
            if not r:
                return None
            return dict(id=r[0], ip=r[1], name=r[2], alive=bool(r[3]))
