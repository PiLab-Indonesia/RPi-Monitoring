"""
A small alert rules engine:
- Maintains a `device_history` table (id, device_ip, alive, ts)
- When scanner updates device, call 'process_state' to record and evaluate rules
- Simple rule implemented: notify if a previously-alive device becomes down
"""

import time
from .models import Database
from .alerts import Alerts

class AlertRules:
    def __init__(self, db_path='data/rpi_nms.db', telegram_token=None, telegram_chat_id=None):
        self.db = Database(db_path)
        self.alerts = Alerts(token=telegram_token, chat_id=telegram_chat_id)
        self.db.init_db()
        # ensure history table exists
        with self.db.conn() as c:
            c.execute("""
            CREATE TABLE IF NOT EXISTS device_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ip TEXT NOT NULL,
                alive INTEGER NOT NULL,
                ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """)

    def record_state(self, ip: str, alive: bool):
        with self.db.conn() as c:
            c.execute("INSERT INTO device_history (ip, alive) VALUES (?, ?)", (ip, int(alive)))

    def last_state(self, ip: str):
        with self.db.conn() as c:
            r = c.execute("SELECT alive FROM device_history WHERE ip=? ORDER BY ts DESC LIMIT 1 OFFSET 0", (ip,)).fetchone()
            return None if not r else bool(r[0])

    def process_state(self, ip: str, alive: bool):
        prev = self.last_state(ip)
        # record current
        self.record_state(ip, alive)
        # if previously alive and now down -> alert
        if prev is True and alive is False:
            text = f"[RPi-NMS] Device down: {ip}"
            self.alerts.send(text)
            print("[alertrules] alerted:", text)
            return True
        return False
