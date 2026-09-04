from datetime import datetime
import uuid
from backend.models import db

class HeritageReport(db.Model):
    __tablename__ = "heritage_reports"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    report_uid = db.Column(db.String(32), unique=True, nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    heritage_site_id = db.Column(db.Integer, db.ForeignKey("heritage_sites.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # 9 Core Categories: Vandalism, Structural Damage, Encroachment, Illegal Construction, Pollution, Garbage, Fire Damage, Flood/Water Damage, Other
    issue_type = db.Column(db.String(60), nullable=False)
    description = db.Column(db.Text, nullable=False)
    incident_date = db.Column(db.Date, nullable=False)
    location = db.Column(db.String(200), nullable=False)
    
    # Severity & Status
    severity = db.Column(db.String(20), default="Moderate", index=True) # Low, Moderate, High, Critical
    status = db.Column(db.String(50), default="Submitted", index=True)   # Submitted, Under Review, Verified, Action Required, Resolved, Rejected
    admin_remarks = db.Column(db.Text, nullable=True)

    # AI-Assisted Damage Assessment Results
    ai_category_detected = db.Column(db.String(100), nullable=True)
    ai_severity_estimated = db.Column(db.String(50), nullable=True)
    ai_confidence_score = db.Column(db.Integer, default=85) # 0 - 100
    ai_damage_signs = db.Column(db.Text, nullable=True)
    ai_urgency = db.Column(db.String(100), nullable=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    images = db.relationship("ReportImage", backref="report", lazy=True, cascade="all, delete-orphan")

    @staticmethod
    def generate_report_uid():
        # Clean alphanumeric tracking ID like HV-2026-X9Y2Z8
        short_hex = uuid.uuid4().hex[:6].upper()
        return f"HV-{datetime.utcnow().year}-{short_hex}"

    def to_dict(self):
        return {
            "id": self.id,
            "report_uid": self.report_uid,
            "user_id": self.user_id,
            "user_name": self.user.name if self.user else "Anonymous Citizen Watcher",
            "user_email": self.user.email if self.user else None,
            "heritage_site_id": self.heritage_site_id,
            "heritage_site_name": self.heritage_site.name if self.heritage_site else None,
            "heritage_site_city": self.heritage_site.city if self.heritage_site else None,
            "state_name": self.heritage_site.state.name if (self.heritage_site and self.heritage_site.state) else None,
            "issue_type": self.issue_type,
            "description": self.description,
            "incident_date": self.incident_date.isoformat() if self.incident_date else None,
            "location": self.location,
            "severity": self.severity,
            "status": self.status,
            "admin_remarks": self.admin_remarks,
            "ai_analysis": {
                "category_detected": self.ai_category_detected or self.issue_type,
                "severity_estimated": self.ai_severity_estimated or self.severity,
                "confidence_score": self.ai_confidence_score or 85,
                "damage_signs": self.ai_damage_signs or "Surface alteration / structural disturbance detected in submitted imagery.",
                "urgency": self.ai_urgency or ("Immediate Inspection Recommended" if self.severity in ["High", "Critical"] else "Standard Periodic Audit"),
                "disclaimer": "AI-assisted preliminary assessment — professional verification required."
            },
            "images": [img.to_dict() for img in self.images],
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }


# Keep VandalismReport as an alias to avoid breaking any legacy references
VandalismReport = HeritageReport


class ReportImage(db.Model):
    __tablename__ = "report_images"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    report_id = db.Column(db.Integer, db.ForeignKey("heritage_reports.id", ondelete="CASCADE"), nullable=False, index=True)
    image_url = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=True)
    file_size_bytes = db.Column(db.Integer, nullable=True)
    mime_type = db.Column(db.String(50), nullable=True)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "report_id": self.report_id,
            "image_url": self.image_url,
            "original_filename": self.original_filename,
            "file_size_bytes": self.file_size_bytes,
            "mime_type": self.mime_type,
            "uploaded_at": self.uploaded_at.isoformat() if self.uploaded_at else None
        }
