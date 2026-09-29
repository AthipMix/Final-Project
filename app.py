from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from database.db import init_db, get_db
from services.engineering_service import EngineeringService
from services.project_service import ProjectService
from services.report_service import ReportService

app = Flask(__name__)
app.config["SECRET_KEY"] = "flood-drainage-demo-secret"

init_db()

engineering_service = EngineeringService()
project_service = ProjectService()
report_service = ReportService()


@app.context_processor
def inject_globals():
    return {"app_name": "FloodGuard"}


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/dashboard")
def dashboard():
    stats = report_service.get_dashboard_stats()
    risk_summary = report_service.get_risk_summary()
    recent = report_service.get_recent_analyses(6)
    return render_template(
        "dashboard.html",
        stats=stats,
        risk_summary=risk_summary,
        recent=recent,
    )


@app.route("/analysis", methods=["GET", "POST"])
def analysis():
    projects = project_service.get_all_projects()
    result = None

    if request.method == "POST":
        try:
            data = {
                "project_id": int(request.form["project_id"]),
                "rainfall": float(request.form["rainfall"]),
                "area": float(request.form["area"]),
                "runoff_coefficient": float(request.form["runoff_coefficient"]),
                "diameter": float(request.form["diameter"]),
                "slope": float(request.form["slope"]),
                "roughness": float(request.form["roughness"]),
                "notes": request.form.get("notes", "").strip(),
            }

            result = engineering_service.analyze_and_save(data)
            flash("บันทึกผลการวิเคราะห์เรียบร้อยแล้ว", "success")
        except (ValueError, KeyError) as exc:
            flash(f"ข้อมูลไม่ถูกต้อง: {exc}", "danger")

    return render_template("analysis.html", projects=projects, result=result)


@app.route("/api/calculate", methods=["POST"])
def api_calculate():
    try:
        payload = request.get_json(force=True)
        result = engineering_service.calculate(
            rainfall=float(payload["rainfall"]),
            area=float(payload["area"]),
            runoff_coefficient=float(payload["runoff_coefficient"]),
            diameter=float(payload["diameter"]),
            slope=float(payload["slope"]),
            roughness=float(payload["roughness"]),
        )
        return jsonify(result)
    except (ValueError, KeyError, TypeError) as exc:
        return jsonify({"error": str(exc)}), 400


@app.route("/projects")
def projects():
    return render_template("projects.html", projects=project_service.get_all_projects())


@app.route("/projects/create", methods=["POST"])
def create_project():
    try:
        project_service.create_project(
            request.form["name"].strip(),
            request.form["location"].strip(),
            request.form.get("description", "").strip(),
            request.form.get("status", "Planning"),
        )
        flash("สร้างโครงการเรียบร้อยแล้ว", "success")
    except ValueError as exc:
        flash(str(exc), "danger")
    return redirect(url_for("projects"))


@app.route("/projects/<int:project_id>")
def project_detail(project_id):
    project = project_service.get_project(project_id)
    if not project:
        flash("ไม่พบโครงการ", "danger")
        return redirect(url_for("projects"))
    analyses = report_service.get_project_analyses(project_id)
    assets = project_service.get_project_assets(project_id)
    return render_template(
        "project_detail.html",
        project=project,
        analyses=analyses,
        assets=assets,
    )


@app.route("/projects/<int:project_id>/delete", methods=["POST"])
def delete_project(project_id):
    project_service.delete_project(project_id)
    flash("ลบโครงการเรียบร้อยแล้ว", "success")
    return redirect(url_for("projects"))


@app.route("/drainage")
def drainage():
    return render_template(
        "drainage.html",
        assets=project_service.get_all_assets(),
        projects=project_service.get_all_projects(),
    )


@app.route("/drainage/create", methods=["POST"])
def create_asset():
    try:
        project_service.create_asset(
            project_id=int(request.form["project_id"]),
            asset_code=request.form["asset_code"].strip(),
            asset_type=request.form["asset_type"],
            location=request.form["location"].strip(),
            diameter=float(request.form["diameter"]),
            condition=request.form["condition"],
            notes=request.form.get("notes", "").strip(),
        )
        flash("เพิ่ม Drainage Asset เรียบร้อยแล้ว", "success")
    except (ValueError, KeyError) as exc:
        flash(f"ข้อมูลไม่ถูกต้อง: {exc}", "danger")
    return redirect(url_for("drainage"))


@app.route("/drainage/<int:asset_id>/delete", methods=["POST"])
def delete_asset(asset_id):
    project_service.delete_asset(asset_id)
    flash("ลบ Asset เรียบร้อยแล้ว", "success")
    return redirect(url_for("drainage"))


@app.route("/reports")
def reports():
    filters = {
        "risk": request.args.get("risk", ""),
        "project_id": request.args.get("project_id", ""),
    }
    analyses = report_service.get_analyses(filters)
    return render_template(
        "reports.html",
        analyses=analyses,
        projects=project_service.get_all_projects(),
        filters=filters,
    )


@app.route("/settings")
def settings():
    return render_template("settings.html")


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)
