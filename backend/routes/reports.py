from datetime import datetime
from flask import Blueprint, request, current_app
from backend.models import db, HeritageReport, ReportImage, HeritageSite
from backend.services.auth_service import get_current_user, token_required
from backend.services.file_service import save_uploaded_image
from backend.ai.damage_analyzer import analyze_citizen_damage_report
from backend.utils.response import success_response, error_response

reports_bp = Blueprint("reports", __name__, url_prefix="/api/reports")

VALID_ISSUE_TYPES = [
    "Vandalism",
    "Structural Damage",
    "Encroachment",
    "Illegal Construction",
    "Pollution",
    "Garbage",
    "Fire Damage",
    "Flood/Water Damage",
    "Other"
]

@reports_bp.route("", methods=["POST"])
def submit_heritage_report():
    """
    Citizen Heritage Watch Report Submission:
    Accepts issue category, incident date, location, description, and photographic evidence.
    Executes AI preliminary damage assessment and returns unique Tracking UID (HV-2026-XXXXXX).
    """
    user = get_current_user() # May be None if submitted by an anonymous guest citizen

    if request.is_json:
        data = request.get_json() or {}
        heritage_site_id = data.get("heritage_site_id")
        issue_type = str(data.get("issue_type", "")).strip()
        description = str(data.get("description", "")).strip()
        incident_date_str = str(data.get("incident_date", "")).strip()
        location = str(data.get("location", "")).strip()
    else:
        heritage_site_id = request.form.get("heritage_site_id")
        issue_type = (request.form.get("issue_type") or "").strip()
        description = (request.form.get("description") or "").strip()
        incident_date_str = (request.form.get("incident_date") or "").strip()
        location = (request.form.get("location") or "").strip()

    # Validation
    if not heritage_site_id or not issue_type or not description or not location:
        return error_response("Missing required fields: heritage_site_id, issue_type, description, location", status_code=400)

    site = HeritageSite.query.get(heritage_site_id)
    if not site:
        return error_response(f"Heritage site #{heritage_site_id} not found", status_code=404)

    # Date parse
    try:
        incident_date = datetime.strptime(incident_date_str, "%Y-%m-%d").date() if incident_date_str else datetime.utcnow().date()
    except ValueError:
        incident_date = datetime.utcnow().date()

    # Normalize issue type
    if issue_type not in VALID_ISSUE_TYPES:
        matching = [v for v in VALID_ISSUE_TYPES if v.lower() in issue_type.lower()]
        issue_type = matching[0] if matching else "Other"

    # AI-Assisted Damage Preliminary Assessment
    ai_result = analyze_citizen_damage_report(issue_type, description, location)

    report_uid = HeritageReport.generate_report_uid()
    report = HeritageReport(
        report_uid=report_uid,
        user_id=user.id if user else None,
        heritage_site_id=int(heritage_site_id),
        issue_type=issue_type,
        description=description,
        incident_date=incident_date,
        location=location,
        severity=ai_result["severity_estimated"],
        status="Submitted",
        ai_category_detected=ai_result["category_detected"],
        ai_severity_estimated=ai_result["severity_estimated"],
        ai_confidence_score=ai_result["confidence_score"],
        ai_damage_signs=ai_result["damage_signs"],
        ai_urgency=ai_result["urgency"]
    )

    db.session.add(report)
    db.session.flush()

    # Handle image upload
    if "evidence_image" in request.files:
        file = request.files["evidence_image"]
        if file and file.filename != "":
            img_info = save_uploaded_image(file, upload_folder=current_app.config["UPLOAD_FOLDER"])
            report_img = ReportImage(
                report_id=report.id,
                image_url=img_info["url"],
                original_filename=img_info["original_filename"],
                file_size_bytes=img_info["file_size_bytes"],
                mime_type=img_info["mime_type"]
            )
            db.session.add(report_img)

    db.session.commit()

    return success_response(
        data=report.to_dict(),
        message=f"Report successfully submitted! Your Tracking UID is {report_uid}.",
        status_code=201
    )


@reports_bp.route("/analyze-preview", methods=["POST"])
def preview_ai_analysis():
    """
    Live AI damage preview endpoint during form filling.
    """
    data = request.get_json() or {}
    issue_type = data.get("issue_type", "Structural Damage")
    description = data.get("description", "")
    location = data.get("location", "")

    result = analyze_citizen_damage_report(issue_type, description, location)
    return success_response(data=result, message="Preliminary AI assessment calculated")


@reports_bp.route("/track/<string:report_uid>", methods=["GET"])
def track_report_by_uid(report_uid):
    """
    Public citizen report tracking lookup by Tracking UID.
    """
    clean_uid = report_uid.strip().upper()
    report = HeritageReport.query.filter_by(report_uid=clean_uid).first()
    if not report:
        return error_response(f"Report UID '{clean_uid}' not found. Please check your reference code.", status_code=404)

    return success_response(data=report.to_dict(), message="Report tracking details retrieved")


@reports_bp.route("/my", methods=["GET"])
@token_required
def get_my_reports(current_user):
    """
    Get all reports submitted by the currently logged-in citizen.
    """
    reports = HeritageReport.query.filter_by(user_id=current_user.id).order_by(HeritageReport.created_at.desc()).all()
    return success_response(data=[r.to_dict() for r in reports], message=f"Retrieved {len(reports)} reports")
