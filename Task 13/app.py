import time
import uuid

from flask import Flask, jsonify, render_template, request, send_file
from dotenv import load_dotenv

from database.storage import get_or_load_state, resume_store, save_analysis_state
from prompts.stage_schemas import NEXT_STAGE
from prompts.system_prompts import SYSTEM_PROMPTS
from rag.retriever import retrieve_kb_context
from reports.pdf_report import build_analysis_report_pdf
from resume.parser import extract_resume_text
from utils.grok_client import call_grok
from utils.uuid_utils import UUID_RE


load_dotenv()

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", asset_version=str(int(time.time())))


@app.route("/upload", methods=["POST"])
def upload_resume():
    if "resume" not in request.files:
        return jsonify({"error": "No file uploaded."}), 400

    uploaded_file = request.files["resume"]
    if not uploaded_file or uploaded_file.filename == "":
        return jsonify({"error": "Invalid file."}), 400

    try:
        file_bytes = uploaded_file.read()
        resume_text = extract_resume_text(uploaded_file.filename, file_bytes)
        if not resume_text:
            return jsonify({"error": "Could not extract text from resume."}), 400

        interests = (request.form.get("interests") or "").strip()
        goal = (request.form.get("goal") or "").strip()

        analysis_id = str(uuid.uuid4())
        resume_store[analysis_id] = {
            "resume_text": resume_text,
            "interests": interests,
            "goal": goal,
            "results": {},
        }

        ats_result = call_grok("ats", resume_text)
        resume_store[analysis_id]["results"]["ats"] = ats_result
        save_analysis_state(analysis_id, resume_store[analysis_id])

        return jsonify(
            {
                "analysis_id": analysis_id,
                "stage": "ats",
                "result": ats_result,
                "next_stage": NEXT_STAGE["ats"],
            }
        )
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    except Exception as exc:
        return jsonify({"error": "Upload failed: %s" % exc}), 500


def build_fallback_career_paths(state):
    resume_text = str(state.get("resume_text") or "")
    text = resume_text.lower()

    missing_skills = []
    try:
        missing_skills = ((state.get("results") or {}).get("skill_gap") or {}).get("missing_skills") or []
    except Exception:
        missing_skills = []

    def pick_missing(limit=6):
        if isinstance(missing_skills, list):
            return [str(x) for x in missing_skills[:limit]]
        return []

    paths = []

    if any(k in text for k in ["scikit", "tensorflow", "pytorch", "pandas", "machine learning", "ml "]):
        paths.append(
            {
                "path": "Machine Learning Engineer",
                "why_fit": ["Resume indicates ML tooling/projects (Python + ML stack)."],
                "missing_skills": pick_missing(),
                "projects_to_build": [
                    "Train + serve a model via Flask/FastAPI with Swagger docs and tests.",
                    "Add model evaluation metrics and basic monitoring plan.",
                ],
                "next_4_weeks_plan": [
                    "Week 1: solidify evaluation/metrics + clean project structure.",
                    "Week 2: containerize inference API (Docker).",
                    "Week 3: add CI (GitHub Actions) + tests (pytest).",
                    "Week 4: deploy to a cloud free tier (Cloud Run/ECS) and document.",
                ],
            }
        )

    if any(k in text for k in ["kotlin", "flask", "api", "firebase", "backend", "rest"]):
        paths.append(
            {
                "path": "Backend Engineer",
                "why_fit": ["Resume indicates backend development experience (APIs/services)."],
                "missing_skills": pick_missing(),
                "projects_to_build": [
                    "CRUD API with auth + PostgreSQL + tests + Swagger.",
                    "Deploy a containerized backend to cloud (Cloud Run/ECS).",
                ],
                "next_4_weeks_plan": [
                    "Week 1: REST API design + SQL basics.",
                    "Week 2: Dockerize service + local compose.",
                    "Week 3: CI/CD pipeline + unit/integration tests.",
                    "Week 4: deploy + monitoring/logging basics.",
                ],
            }
        )

    if any(k in text for k in ["etl", "airflow", "pipeline", "kafka", "spark", "warehouse"]):
        paths.append(
            {
                "path": "Data Engineer",
                "why_fit": ["Resume suggests interest/experience in data pipelines."],
                "missing_skills": pick_missing(),
                "projects_to_build": [
                    "ETL pipeline: public API -> storage -> cleaned tables in Postgres.",
                    "Airflow DAG with retries + alerting (local Docker Compose).",
                ],
                "next_4_weeks_plan": [
                    "Week 1: SQL + data modeling basics.",
                    "Week 2: build ETL in Python + logging.",
                    "Week 3: orchestrate with Airflow (Docker).",
                    "Week 4: add CI + documentation + sample dashboards.",
                ],
            }
        )

    if not paths:
        paths.append(
            {
                "path": "Backend Engineer",
                "why_fit": ["Default recommendation: backend path is broadly compatible with most resumes."],
                "missing_skills": pick_missing(),
                "projects_to_build": ["CRUD API + PostgreSQL + tests + Swagger."],
                "next_4_weeks_plan": ["Week 1-4: build, test, containerize, deploy, document."],
            }
        )

    return {
        "top_paths": paths[:3],
        "final_recommendation": "Top match: %s. Use interests/goal fields for higher precision." % paths[0]["path"],
    }


@app.route("/analyze/<stage>", methods=["POST"])
def analyze_stage(stage):
    if stage not in SYSTEM_PROMPTS or stage == "ats":
        return jsonify({"error": "Invalid stage."}), 400

    body = request.get_json(silent=True) or {}
    analysis_id = body.get("analysis_id")
    if not analysis_id or not isinstance(analysis_id, str):
        return jsonify({"error": "Missing analysis_id. Please upload first."}), 400

    if not UUID_RE.match(analysis_id):
        return jsonify({"error": "Invalid analysis_id."}), 400

    state = get_or_load_state(analysis_id)
    if not state:
        return jsonify({"error": "No resume in memory. Please upload first."}), 400

    try:
        extra = None
        if stage == "career_paths":
            query_parts = [state.get("resume_text") or ""]
            if state.get("interests"):
                query_parts.append(state.get("interests") or "")
            if state.get("goal"):
                query_parts.append(state.get("goal") or "")
            query = " ".join(query_parts).strip()
            retrieved = retrieve_kb_context(query, k=6)
            extra = {
                "interests": state.get("interests") or "",
                "goal": state.get("goal") or "",
                "retrieved_context": retrieved,
            }

        result = call_grok(stage, state["resume_text"], extra=extra)

        if stage == "career_paths":
            top_paths = result.get("top_paths") if isinstance(result, dict) else None
            if not isinstance(top_paths, list) or not top_paths:
                result = build_fallback_career_paths(state)
            if isinstance(result, dict) and extra:
                result["_rag_context_chars"] = len(str(extra.get("retrieved_context") or ""))

        state["results"][stage] = result
        save_analysis_state(analysis_id, state)

        return jsonify(
            {
                "analysis_id": analysis_id,
                "stage": stage,
                "result": result,
                "next_stage": NEXT_STAGE.get(stage),
            }
        )
    except Exception as exc:
        return jsonify({"error": "Analysis failed: %s" % exc}), 500


@app.route("/analysis/<analysis_id>", methods=["GET"])
def get_analysis(analysis_id):
    if not UUID_RE.match(analysis_id):
        return jsonify({"error": "Invalid analysis_id."}), 400
    state = get_or_load_state(analysis_id)
    if not state:
        return jsonify({"error": "Not found."}), 404
    return jsonify({"analysis_id": analysis_id, "results": state.get("results") or {}})


@app.route("/download-report/<analysis_id>.pdf", methods=["GET"])
def download_report_pdf(analysis_id):
    if not UUID_RE.match(analysis_id):
        return jsonify({"error": "Invalid analysis_id."}), 400
    state = get_or_load_state(analysis_id)
    if not state:
        return jsonify({"error": "Not found."}), 404

    buffer = build_analysis_report_pdf(analysis_id, state)
    return send_file(
        buffer,
        mimetype="application/pdf",
        as_attachment=True,
        download_name="resume_analysis_%s.pdf" % analysis_id,
    )


if __name__ == "__main__":
    app.run(debug=True)

