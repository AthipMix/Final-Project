from database.db import get_db


class ReportService:

    def get_dashboard_stats(self):
        conn = get_db()
        total_analysis = conn.execute(
            "SELECT COUNT(*) FROM analyses"
        ).fetchone()[0]
        total_projects = conn.execute(
            "SELECT COUNT(*) FROM projects"
        ).fetchone()[0]
        total_assets = conn.execute(
            "SELECT COUNT(*) FROM drainage_assets"
        ).fetchone()[0]
        critical = conn.execute(
            "SELECT COUNT(*) FROM analyses WHERE risk_level = 'Critical'"
        ).fetchone()[0]
        conn.close()

        return {
            "total_analysis": total_analysis,
            "total_projects": total_projects,
            "total_assets": total_assets,
            "critical": critical,
        }

    def get_risk_summary(self):
        conn = get_db()
        rows = conn.execute(
            """
            SELECT risk_level, COUNT(*) AS total
            FROM analyses
            GROUP BY risk_level
            """
        ).fetchall()
        conn.close()

        result = {"Low": 0, "Moderate": 0, "High": 0, "Critical": 0}
        for row in rows:
            result[row["risk_level"]] = row["total"]
        return result

    def get_recent_analyses(self, limit=6):
        conn = get_db()
        rows = conn.execute(
            """
            SELECT a.*, p.name AS project_name
            FROM analyses a
            JOIN projects p ON p.id = a.project_id
            ORDER BY a.id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
        conn.close()
        return rows

    def get_project_analyses(self, project_id):
        conn = get_db()
        rows = conn.execute(
            """
            SELECT a.*, p.name AS project_name
            FROM analyses a
            JOIN projects p ON p.id = a.project_id
            WHERE a.project_id = ?
            ORDER BY a.id DESC
            """,
            (project_id,),
        ).fetchall()
        conn.close()
        return rows

    def get_analyses(self, filters=None):
        filters = filters or {}
        conditions = []
        params = []

        if filters.get("risk"):
            conditions.append("a.risk_level = ?")
            params.append(filters["risk"])

        if filters.get("project_id"):
            conditions.append("a.project_id = ?")
            params.append(filters["project_id"])

        where = f"WHERE {' AND '.join(conditions)}" if conditions else ""

        conn = get_db()
        rows = conn.execute(
            f"""
            SELECT a.*, p.name AS project_name
            FROM analyses a
            JOIN projects p ON p.id = a.project_id
            {where}
            ORDER BY a.id DESC
            """,
            params,
        ).fetchall()
        conn.close()
        return rows
