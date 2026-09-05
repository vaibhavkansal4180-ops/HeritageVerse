from flask import Blueprint, request
from sqlalchemy import func
from backend.models import db, User, State, HeritageSite, HeritageReport, ReportImage, HeritageImage, Alert, AdminAction
from backend.services.auth_service import admin_required
from backend.utils.response import success_response, error_response

admin_bp = Blueprint("admin", __name__, url_prefix="/api/admin")

VALID_STATUSES = {
    "Submitted",
    "Under Review",
    "Verified",
    "Action Required",
    "Resolved",
    "Rejected"
}

@admin_bp.route("/stats", methods=["GET"])
@admin_required
def get_admin_dashboard_stats(current_user):
    """Calculates comprehensive preservation platform statistics for the Admin Command Center."""
    total_sites = HeritageSite.query.count()
    total_states = State.query.count()
    total_reports = HeritageReport.query.count()
    
    # Reports Breakdown
    pending_reports = HeritageReport.query.filter(HeritageReport.status.in_(["Submitted", "Under Review"])).count()
    verified_reports = HeritageReport.query.filter_by(status="Verified").count()
    action_required_reports = HeritageReport.query.filter_by(status="Action Required").count()
    resolved_reports = HeritageReport.query.filter_by(status="Resolved").count()
    rejected_reports = HeritageReport.query.filter_by(status="Rejected").count()

    # Alerts Breakdown
    total_alerts = Alert.query.count()
    active_alerts = Alert.query.filter(Alert.status.in_(["Active", "Acknowledged", "Assigned"])).count()
    critical_alerts = Alert.query.filter_by(priority="CRITICAL", status="Active").count()

    # Health Profile
    healthy_sites = HeritageSite.query.filter(HeritageSite.current_health_score >= 85).count()
    high_risk_sites = HeritageSite.query.filter(HeritageSite.current_health_score < 70).count()
    critical_sites = HeritageSite.query.filter(HeritageSite.current_health_score < 50).count()

    total_users = User.query.count()

    return success_response(
        data={
            "total_sites": total_sites,
            "total_states": total_states,
            "total_reports": total_reports,
            "pending_reports": pending_reports,
            "verified_reports": verified_reports,
            "action_required_reports": action_required_reports,
            "resolved_reports": resolved_reports,
            "rejected_reports": rejected_reports,
            "total_alerts": total_alerts,
            "active_alerts": active_alerts,
            "critical_alerts": critical_alerts,
            "healthy_sites": healthy_sites,
            "high_risk_sites": high_risk_sites,
            "critical_sites": critical_sites,
            "total_users": total_users
        },
        message="Admin preservation statistics retrieved."
    )


@admin_bp.route("/reports", methods=["GET"])
@admin_required
def get_all_reports(current_user):
    """Retrieve all citizen damage reports with filtering for administration."""
    status_filter = request.args.get("status")
    query = HeritageReport.query
    
    if status_filter and status_filter.lower() != "all":
        query = query.filter_by(status=status_filter)
        
    reports = query.order_by(HeritageReport.created_at.desc()).all()
    return success_response(
        data=[r.to_dict() for r in reports],
        message=f"Retrieved {len(reports)} report(s)."
    )


@admin_bp.route("/reports/<int:report_id>", methods=["PUT"])
@admin_required
def update_report_status(current_user, report_id):
    """Admin updates report status and adds official preservation remarks."""
    report = HeritageReport.query.get(report_id)
    if not report:
        return error_response(f"Report with ID {report_id} not found.", status_code=404)

    data = request.get_json() or {}
    new_status = data.get("status")
    admin_remarks = data.get("admin_remarks")

    if new_status:
        if new_status not in VALID_STATUSES:
            return error_response(f"Invalid status. Must be one of: {', '.join(VALID_STATUSES)}")
        report.status = new_status

    if admin_remarks is not None:
        report.admin_remarks = admin_remarks.strip()

    # Log action to audit trail
    log_entry = AdminAction(
        user_id=current_user.id,
        action_type=f"Report Moderated: {report.status}",
        target_entity="Report",
        target_id=report.id,
        notes=f"Updated status to '{report.status}'. Remarks: {report.admin_remarks or 'None'}"
    )
    db.session.add(log_entry)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return error_response(f"Failed to update report: {str(e)}", status_code=500)

    return success_response(
        data=report.to_dict(),
        message=f"Report #{report.report_uid} status successfully updated to '{report.status}'."
    )


@admin_bp.route("/heritage", methods=["POST"])
@admin_required
def create_heritage_site(current_user):
    """Admin creates a new monitored heritage monument entry."""
    data = request.get_json() or {}
    
    state_id = data.get("state_id")
    name = data.get("name", "").strip()
    city = data.get("city", "").strip()
    description = data.get("description", "").strip()

    if not state_id or not name or not city or not description:
        return error_response("State ID, Name, City, and Description are required.")

    state = State.query.get(state_id)
    if not state:
        return error_response(f"State ID {state_id} does not exist.", status_code=404)

    site = HeritageSite(
        state_id=state_id,
        name=name,
        city=city,
        historical_period=data.get("historical_period"),
        heritage_category=data.get("heritage_category", "Monuments & Forts"),
        description=description,
        cultural_significance=data.get("cultural_significance"),
        architecture=data.get("architecture"),
        latitude=data.get("latitude"),
        longitude=data.get("longitude"),
        preservation_status=data.get("preservation_status", "Well Preserved"),
        current_health_score=data.get("current_health_score", 82),
        risk_level=data.get("risk_level", "Low"),
        carrying_capacity_daily=data.get("carrying_capacity_daily", 5000),
        image_url=data.get("image_url", "/assets/images/placeholder.jpg"),
        is_featured=bool(data.get("is_featured", False))
    )

    try:
        db.session.add(site)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return error_response(f"Failed to create heritage site: {str(e)}", status_code=500)

    return success_response(
        data=site.to_dict(include_details=True),
        message=f"Heritage site '{site.name}' added to preservation network.",
        status_code=201
    )


@admin_bp.route("/audit-logs", methods=["GET"])
@admin_required
def get_audit_logs(current_user):
    """Retrieve administrator preservation actions audit trail."""
    logs = AdminAction.query.order_by(AdminAction.created_at.desc()).limit(50).all()
    return success_response(data=[l.to_dict() for l in logs], message="Audit trail logs retrieved")


@admin_bp.route("/init-seed", methods=["POST", "GET"])
def initialize_database_seed():
    """Initializes and seeds the database with official heritage baseline records if empty or on refresh."""
    from backend.seed import seed_database
    refresh = request.args.get("refresh", "false").lower() in ("true", "1", "yes")
    site_count = HeritageSite.query.count()
    if site_count == 0 or refresh:
        seed_database(drop_existing=False)
        site_count = HeritageSite.query.count()
        return success_response(
            data={"seeded": True, "site_count": site_count},
            message=f"Database successfully synchronized and seeded with {site_count} heritage monuments."
        )
    return success_response(
        data={"seeded": False, "site_count": site_count},
        message=f"Database already initialized with {site_count} monitored heritage sites."
    )


