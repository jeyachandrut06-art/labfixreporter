import os

from flask import Flask, jsonify, render_template, request
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
    raise RuntimeError(
        "Missing SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY in your .env file."
    )

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_SERVICE_ROLE_KEY
)

app = Flask(__name__)


@app.get("/")
def home():
    return render_template("index.html")


@app.get("/api/health")
def health():
    try:
        supabase.table("reports").select("id").limit(1).execute()

        return jsonify({
            "status": "ok",
            "database": "connected"
        })

    except Exception as exc:
        return jsonify({
            "status": "error",
            "database": "not connected",
            "message": str(exc)
        }), 500


@app.post("/api/reports")
def create_report():
    try:
        data = request.get_json() or {}

        required_fields = [
            "student_name",
            "lab_name",
            "pc_number",
            "problem_type",
            "description"
        ]

        for field in required_fields:
            value = str(data.get(field, "")).strip()

            if not value:
                return jsonify({
                    "error": f"{field} is required."
                }), 400

        report = {
            "student_name": str(data["student_name"]).strip(),
            "lab_name": str(data["lab_name"]).strip(),
            "pc_number": str(data["pc_number"]).strip(),
            "problem_type": str(data["problem_type"]).strip(),
            "description": str(data["description"]).strip()
        }

        result = (
            supabase
            .table("reports")
            .insert(report)
            .execute()
        )

        if not result.data:
            return jsonify({
                "error": "The report was not inserted into the database."
            }), 500

        report_id = result.data[0]["id"]

        return jsonify({
            "success": True,
            "report_id": report_id,
            "redirect_url": f"/submitted/{report_id}"
        }), 201

    except Exception as exc:
        print("SUPABASE INSERT ERROR:", repr(exc), flush=True)

        return jsonify({
            "error": str(exc)
        }), 500


@app.get("/submitted/<int:report_id>")
def submitted_report(report_id):
    try:
        result = (
            supabase
            .table("reports")
            .select("*")
            .eq("id", report_id)
            .single()
            .execute()
        )

        if not result.data:
            return "Report not found", 404

        return render_template(
            "submitted.html",
            report=result.data
        )

    except Exception as exc:
        return f"Error loading report: {exc}", 500


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )