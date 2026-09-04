from flask import Blueprint, request
from backend.models import (
    db, HeritageSite, HeritageReport, RiskAssessment,
    EnvironmentalData, TouristPressure, EncroachmentObservation,
    ConditionTimeline, Alert
)
from backend.services.health_score_service import HealthScoreService
from backend.ai.preservation_assistant import generate_site_preservation_brief
from backend.utils.response import success_response, error_response

preservation_bp = Blueprint("preservation", __name__, url_prefix="/api/preservation")

@preservation_bp.route("/dashboard", methods=["GET"])
def get_command_center_dashboard():
    """
    Returns executive preservation intelligence metrics, risk distribution,
    health distribution, and active early warning alerts for the Command Center.
    """
    try:
        sites = HeritageSite.query.all()
        total_sites = len(sites)

        # Health Categories
        healthy_sites = [s for s in sites if s.current_health_score >= 85]
        attention_sites = [s for s in sites if 70 <= s.current_health_score < 85]
        high_risk_sites = [s for s in sites if 50 <= s.current_health_score < 70]
        critical_sites = [s for s in sites if s.current_health_score < 50]

        # Reports Stats
        all_reports = HeritageReport.query.all()
        open_reports = [r for r in all_reports if r.status in ["Submitted", "Under Review", "Verified", "Action Required"]]
        pending_verification = [r for r in all_reports if r.status in ["Submitted", "Under Review"]]

        # Alerts Stats
        all_alerts = Alert.query.all()
        active_alerts = [a for a in all_alerts if a.status in ["Active", "Acknowledged", "Assigned"]]
        critical_alerts = [a for a in active_alerts if a.priority == "CRITICAL"]

        # Issue category breakdown
        categories_map = {}
        for r in all_reports:
            cat = r.issue_type
            categories_map[cat] = categories_map.get(cat, 0) + 1

        # Encroachment & Environmental counts
        total_encroachments = EncroachmentObservation.query.count()
        critical_env_count = EnvironmentalData.query.filter(EnvironmentalData.exposure_risk_status.in_(["High Risk", "Critical Warning"])).count()

        data = {
            "summary": {
                "total_monitored_sites": total_sites,
                "healthy_sites": len(healthy_sites),
                "attention_sites": len(attention_sites),
                "high_risk_sites": len(high_risk_sites),
                "critical_sites": len(critical_sites),
                "open_reports_count": len(open_reports),
                "pending_verification_count": len(pending_verification),
                "active_alerts_count": len(active_alerts),
                "critical_alerts_count": len(critical_alerts),
                "total_encroachments_detected": total_encroachments,
                "critical_environmental_warnings": critical_env_count
            },
            "health_distribution": {
                "Healthy (85-100)": len(healthy_sites),
                "Attention (70-84)": len(attention_sites),
                "High Risk (50-69)": len(high_risk_sites),
                "Critical (<50)": len(critical_sites)
            },
            "issue_categories": categories_map,
            "critical_monuments": [
                s.to_dict() for s in sorted(sites, key=lambda x: x.current_health_score)[:6]
            ],
            "active_early_warnings": [a.to_dict() for a in sorted(active_alerts, key=lambda x: 0 if x.priority == "CRITICAL" else (1 if x.priority == "HIGH" else 2))[:8]],
            "recent_citizen_reports": [r.to_dict() for r in sorted(all_reports, key=lambda x: x.created_at, reverse=True)[:6]]
        }

        return success_response(data=data, message="Preservation Intelligence dashboard retrieved successfully")
    except Exception as e:
        return error_response(f"Failed to load dashboard metrics: {str(e)}", status_code=500)


@preservation_bp.route("/site/<int:site_id>/dossier", methods=["GET"])
def get_site_preservation_dossier(site_id):
    """
    Returns full comprehensive preservation dossier for a heritage monument:
    Health score breakdown, AI Assistant brief, Risk matrix, Encroachments, Environmental readings,
    Tourist pressure, Condition timeline, Citizen reports, and Active alerts.
    """
    site = HeritageSite.query.get_or_404(site_id)
    site_dict = site.to_dict(include_details=True)

    # Calculate real-time health score & factor math
    health_math = HealthScoreService.calculate_health_score(site)
    site_dict["health_score_breakdown"] = health_math

    # Generate AI Preservation Decision Support Brief
    ai_brief = generate_site_preservation_brief(site_dict)
    site_dict["ai_preservation_assistant"] = ai_brief

    return success_response(data=site_dict, message=f"Preservation dossier for '{site.name}' retrieved")


@preservation_bp.route("/site/<int:site_id>/health", methods=["GET"])
def get_site_health_breakdown(site_id):
    """
    Returns transparent 0-100 Health Score computation with factor-wise mathematical contributions.
    """
    site = HeritageSite.query.get_or_404(site_id)
    health_math = HealthScoreService.calculate_health_score(site)
    return success_response(data=health_math, message=f"Health score breakdown for '{site.name}'")


@preservation_bp.route("/site/<int:site_id>/ai-assistant", methods=["GET"])
def get_site_ai_assistant(site_id):
    """
    Context-aware AI decision support: Top threats, Priority rationale,
    First issue to address, Evidence trail, On-site checklist, and Action plan.
    """
    site = HeritageSite.query.get_or_404(site_id)
    site_dict = site.to_dict(include_details=True)
    ai_brief = generate_site_preservation_brief(site_dict)
    return success_response(data=ai_brief, message=f"AI preservation briefing for '{site.name}'")


@preservation_bp.route("/encroachments", methods=["GET"])
def get_all_encroachments():
    """
    Returns national registry of 100m/300m protected buffer zone encroachment observations.
    """
    site_id = request.args.get("site_id", type=int)
    query = EncroachmentObservation.query
    if site_id:
        query = query.filter_by(heritage_site_id=site_id)
    
    observations = query.order_by(EncroachmentObservation.created_at.desc()).all()
    return success_response(data=[o.to_dict() for o in observations], message="Encroachment observations retrieved")
