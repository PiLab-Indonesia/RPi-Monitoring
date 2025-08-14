"""
Simple one-shot migration runner to create device_history if missing.
Run: python -m app.migrations.0001_add_history
"""
from ..models import Database

def migrate():
    db = Database('data/rpi_nms.db')
    db.init_db()
    with db.conn() as c:
        c.execute("""
        CREATE TABLE IF NOT EXISTS device_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip TEXT NOT NULL,
            alive INTEGER NOT NULL,
            ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)
    print("migration 0001 applied")

if __name__ == '__main__':
    migrate()
