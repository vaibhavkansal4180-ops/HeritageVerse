from flask import Blueprint, request
from backend.models import db, Alert
from backend.services.alert_service import AlertService
from backend.services.auth_service import token_required, admin_required
from backend.utils.response import success_response, error_response

alerts_bp = Blueprint("alerts", __name__, url_prefix="/api/alerts")

@alerts_bp.route("", methods=["GET"])
def get_alerts():
    """
    List early warning alerts with filtering by priority, status, or heritage site.
    """
    status = request.args.get("status", "all")
    priority = request.args.get("priority", "all")
    site_id = request.args.get("site_id", type=int)

    alerts = AlertService.get_all_alerts(status=status, priority=priority, site_id=site_id)
    return success_response(
        data=[a.to_dict() for a in alerts],
        message=f"Retrieved {len(alerts)} alerts"
    )


@alerts_bp.route("/<int:alert_id>", methods=["GET"])
def get_single_alert(alert_id):
    """
    Get detailed alert data by ID.
    """
    alert = Alert.query.get_or_404(alert_id)
    return success_response(data=alert.to_dict(), message="Alert details retrieved")


@alerts_bp.route("/<int:alert_id>/action", methods=["PUT"])
@admin_required
def take_alert_action(current_user, alert_id):
    """
    Officer / Administrator Rapid Action Dispatch:
    Acknowledge, assign officer/team, adjust priority, mark resolved, and add action notes.
    """
    data = request.get_json() or {}
    try:
        updated_alert = AlertService.update_alert_action(
            alert_id=alert_id,
            user_id=current_user.id,
            action_data=data
        )
        return success_response(
            data=updated_alert.to_dict(),
            message=f"Alert {updated_alert.alert_uid} status successfully updated to '{updated_alert.status}'"
        )
    except Exception as e:
        db.session.rollback()
        return error_response(f"Failed to update alert: {str(e)}", status_code=500)
