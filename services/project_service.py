from database.db import get_db


class ProjectService:

    def get_all_projects(self):
        conn = get_db()
        rows = conn.execute(
            """
            SELECT p.*,
                   COUNT(DISTINCT a.id) AS analysis_count,
                   COUNT(DISTINCT d.id) AS asset_count
            FROM projects p
            LEFT JOIN analyses a ON a.project_id = p.id
            LEFT JOIN drainage_assets d ON d.project_id = p.id
            GROUP BY p.id
            ORDER BY p.id DESC
            """
        ).fetchall()
        conn.close()
        return rows

    def get_project(self, project_id):
        conn = get_db()
        row = conn.execute(
            "SELECT * FROM projects WHERE id = ?", (project_id,)
        ).fetchone()
        conn.close()
        return row

    def create_project(self, name, location, description, status):
        if not name or not location:
            raise ValueError("กรุณาระบุชื่อโครงการและสถานที่")

        conn = get_db()
        conn.execute(
            """
            INSERT INTO projects(name, location, description, status)
            VALUES (?, ?, ?, ?)
            """,
            (name, location, description, status),
        )
        conn.commit()
        conn.close()

    def delete_project(self, project_id):
        conn = get_db()
        conn.execute("DELETE FROM projects WHERE id = ?", (project_id,))
        conn.commit()
        conn.close()

    def get_all_assets(self):
        conn = get_db()
        rows = conn.execute(
            """
            SELECT d.*, p.name AS project_name
            FROM drainage_assets d
            JOIN projects p ON p.id = d.project_id
            ORDER BY d.id DESC
            """
        ).fetchall()
        conn.close()
        return rows

    def get_project_assets(self, project_id):
        conn = get_db()
        rows = conn.execute(
            """
            SELECT * FROM drainage_assets
            WHERE project_id = ?
            ORDER BY id DESC
            """,
            (project_id,),
        ).fetchall()
        conn.close()
        return rows

    def create_asset(
        self, project_id, asset_code, asset_type, location,
        diameter, condition, notes
    ):
        if not asset_code or not location:
            raise ValueError("กรุณาระบุ Asset Code และ Location")
        if diameter <= 0:
            raise ValueError("Diameter ต้องมากกว่า 0")

        conn = get_db()
        try:
            conn.execute(
                """
                INSERT INTO drainage_assets
                (project_id, asset_code, asset_type, location, diameter, condition, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    project_id,
                    asset_code,
                    asset_type,
                    location,
                    diameter,
                    condition,
                    notes,
                ),
            )
            conn.commit()
        except Exception:
            conn.rollback()
            raise ValueError("Asset Code นี้มีอยู่แล้ว")
        finally:
            conn.close()

    def delete_asset(self, asset_id):
        conn = get_db()
        conn.execute("DELETE FROM drainage_assets WHERE id = ?", (asset_id,))
        conn.commit()
        conn.close()
