from datetime import datetime
from backend.models import db, Alert, AdminAction, HeritageSite

class AlertService:
    """
    Early Warning Alert Engine & Rapid Action Dispatch.
    """

    @classmethod
    def get_all_alerts(cls, status=None, priority=None, site_id=None):
        query = Alert.query
        if status and status != "all":
            query = query.filter_by(status=status)
        if priority and priority != "all":
            query = query.filter_by(priority=priority)
        if site_id:
            query = query.filter_by(heritage_site_id=site_id)
        
        return query.order_by(Alert.created_at.desc()).all()

    @classmethod
    def update_alert_action(cls, alert_id: int, user_id: int, action_data: dict) -> Alert:
        alert = Alert.query.get_or_404(alert_id)
        
        new_status = action_data.get("status")
        assigned_to = action_data.get("assigned_to")
        action_notes = action_data.get("action_notes")
        new_priority = action_data.get("priority")

        if new_status:
            alert.status = new_status
            if new_status == "Resolved":
                alert.resolved_at = datetime.utcnow()
        if assigned_to:
            alert.assigned_to = assigned_to
        if new_priority:
            alert.priority = new_priority
        if action_notes:
            alert.action_notes = action_notes

        # Log to Admin Audit Trail
        log_entry = AdminAction(
            user_id=user_id,
            action_type=f"Alert {alert.status}: {alert.alert_type}",
            target_entity="Alert",
            target_id=alert.id,
            notes=f"Updated status to '{alert.status}' by Officer/Admin. Assigned: {alert.assigned_to or 'Unassigned'}. Notes: {action_notes or 'None'}"
        )
        db.session.add(log_entry)
        db.session.commit()

        return alert

    @classmethod
    def create_alert(cls, site_id: int, alert_type: str, priority: str, title: str, description: str, trigger_reason: str, recommended_action: str) -> Alert:
        alert = Alert(
            alert_uid=Alert.generate_alert_uid(),
            heritage_site_id=site_id,
            alert_type=alert_type,
            priority=priority,
            title=title,
            description=description,
            trigger_reason=trigger_reason,
            recommended_action=recommended_action,
            status="Active"
        )
        db.session.add(alert)
        db.session.commit()
        return alert
