import sqlite3
from src.config import Config

conn = sqlite3.connect(Config.SQLITE_DB_PATH)

# conn.execute("PRAGMA foreign_keys = ON")

cursor = conn.cursor()

cursor.executescript("""
               CREATE TABLE IF NOT EXISTS users
               (
                   id            INTEGER PRIMARY KEY AUTOINCREMENT,
                   email         TEXT UNIQUE NOT NULL,
                   password_hash TEXT        NOT NULL,
                   role          TEXT NOT NULL DEFAULT 'user',
                   created_at    DATETIME DEFAULT CURRENT_TIMESTAMP
               );

               CREATE TABLE IF NOT EXISTS prompt_sets
               (
                   id          INTEGER PRIMARY KEY AUTOINCREMENT,
                   name        TEXT NOT NULL,
                   description TEXT,
                   created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
                   updated_at  DATETIME DEFAULT CURRENT_TIMESTAMP
               );

               CREATE TABLE IF NOT EXISTS prompts
               (
                   id            INTEGER PRIMARY KEY AUTOINCREMENT,

                   prompt_set_id INTEGER NOT NULL,

                   prompt_type   TEXT    NOT NULL,
                   content       TEXT    NOT NULL,

                   created_at    DATETIME DEFAULT CURRENT_TIMESTAMP,
                   updated_at    DATETIME DEFAULT CURRENT_TIMESTAMP,

                   FOREIGN KEY (prompt_set_id)
                       REFERENCES prompt_sets (id)
                       ON DELETE CASCADE,
                   UNIQUE (prompt_set_id, prompt_type)
               );

               """)

conn.commit()
conn.close()
