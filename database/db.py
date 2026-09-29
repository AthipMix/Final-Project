import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "floodguard.db"


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_db()
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            location TEXT NOT NULL,
            description TEXT,
            status TEXT NOT NULL DEFAULT 'Planning',
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS drainage_assets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER NOT NULL,
            asset_code TEXT NOT NULL UNIQUE,
            asset_type TEXT NOT NULL,
            location TEXT NOT NULL,
            diameter REAL NOT NULL,
            condition TEXT NOT NULL,
            notes TEXT,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(project_id) REFERENCES projects(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS analyses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER NOT NULL,
            rainfall REAL NOT NULL,
            area REAL NOT NULL,
            runoff_coefficient REAL NOT NULL,
            diameter REAL NOT NULL,
            slope REAL NOT NULL,
            roughness REAL NOT NULL,
            runoff REAL NOT NULL,
            pipe_capacity REAL NOT NULL,
            utilization REAL NOT NULL,
            risk_level TEXT NOT NULL,
            notes TEXT,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(project_id) REFERENCES projects(id) ON DELETE CASCADE
        );
        """
    )

    # Seed data only when empty, making the first launch immediately usable.
    project_count = conn.execute("SELECT COUNT(*) FROM projects").fetchone()[0]
    if project_count == 0:
        conn.executemany(
            """
            INSERT INTO projects(name, location, description, status)
            VALUES (?, ?, ?, ?)
            """,
            [
                (
                    "Zone A Flood Prevention",
                    "Nakhon Pathom",
                    "โครงการต้นแบบสำหรับวิเคราะห์ความเสี่ยงน้ำท่วมและระบบระบายน้ำ",
                    "Active",
                ),
                (
                    "Campus Drainage Improvement",
                    "นครปฐม",
                    "ปรับปรุงระบบระบายน้ำบริเวณอาคารเรียนและพื้นที่โดยรอบ",
                    "Planning",
                ),
            ],
        )

    asset_count = conn.execute("SELECT COUNT(*) FROM drainage_assets").fetchone()[0]
    if asset_count == 0:
        project_id = conn.execute("SELECT id FROM projects ORDER BY id LIMIT 1").fetchone()[0]
        conn.execute(
            """
            INSERT INTO drainage_assets
            (project_id, asset_code, asset_type, location, diameter, condition, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                project_id,
                "PIPE-001",
                "Pipe",
                "Zone A - Main Road",
                0.60,
                "Good",
                "ท่อระบายน้ำหลัก",
            ),
        )

    conn.commit()
    conn.close()
