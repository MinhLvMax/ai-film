import sqlite3
from src.config import Config


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(Config.SQLITE_DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn
