from flask import Blueprint
from sqlalchemy import func
from backend.models import db, State, HeritageSite, HeritageReport, Alert, EncroachmentObservation
from backend.utils.response import success_response

stats_bp = Blueprint("stats", __name__, url_prefix="/api/stats")

@stats_bp.route("/preservation", methods=["GET"])
def get_preservation_stats():
    """Returns public national preservation intelligence and monitoring metrics."""
    total_sites = HeritageSite.query.count()
    states_covered = State.query.count()
    
    # Health Profile
    healthy_sites = HeritageSite.query.filter(HeritageSite.current_health_score >= 85).count()
    attention_sites = HeritageSite.query.filter(HeritageSite.current_health_score.between(70, 84)).count()
    high_risk_sites = HeritageSite.query.filter(HeritageSite.current_health_score.between(50, 69)).count()
    critical_sites = HeritageSite.query.filter(HeritageSite.current_health_score < 50).count()
    
    reports_submitted = HeritageReport.query.count()
    reports_resolved = HeritageReport.query.filter_by(status="Resolved").count()
    reports_under_action = HeritageReport.query.filter(
        HeritageReport.status.in_(["Verified", "Action Required"])
    ).count()

    active_alerts = Alert.query.filter(Alert.status.in_(["Active", "Acknowledged", "Assigned"])).count()
    encroachments_detected = EncroachmentObservation.query.count()

    # Preservation status distribution
    status_counts = db_status_distribution()

    return success_response(
        data={
            "heritage_sites_count": total_sites,
            "states_covered_count": states_covered,
            "healthy_monuments_count": healthy_sites,
            "attention_required_count": attention_sites,
            "high_risk_count": high_risk_sites,
            "critical_risk_count": critical_sites,
            "reports_submitted_count": reports_submitted,
            "reports_resolved_count": reports_resolved,
            "reports_under_action_count": reports_under_action,
            "active_early_warnings_count": active_alerts,
            "encroachments_detected_count": encroachments_detected,
            "preservation_status_breakdown": status_counts
        },
        message="Preservation dashboard metrics retrieved."
    )

def db_status_distribution():
    rows = db.session.query(
        HeritageSite.preservation_status, 
        func.count(HeritageSite.id)
    ).group_by(HeritageSite.preservation_status).all()
    
    return {status or "Unknown": count for status, count in rows}
