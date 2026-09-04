from datetime import datetime
from backend.models import db

class HeritageSite(db.Model):
    __tablename__ = "heritage_sites"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    state_id = db.Column(db.Integer, db.ForeignKey("states.id", ondelete="CASCADE"), nullable=False, index=True)
    name = db.Column(db.String(150), nullable=False, index=True)
    city = db.Column(db.String(100), nullable=False)
    historical_period = db.Column(db.String(100), nullable=True) # e.g. Mughal, Chola, Rajput, Ancient Maurya
    heritage_category = db.Column(db.String(100), default="Monuments & Forts") # Monuments & Forts, Sacred & Temple Architecture, Cave & Rock-Cut Shrines, Archaeological Excavations, Colonial & Urban Heritage
    description = db.Column(db.Text, nullable=False)
    cultural_significance = db.Column(db.Text, nullable=True)
    architecture = db.Column(db.Text, nullable=True)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    preservation_status = db.Column(db.String(50), default="Well Preserved") # Well Preserved, Minor Restoration Required, Major Conservation Needed, Under Active Restoration, Critical
    current_health_score = db.Column(db.Integer, default=82) # 0 - 100
    risk_level = db.Column(db.String(20), default="Low") # Low, Moderate, High, Critical
    carrying_capacity_daily = db.Column(db.Integer, default=5000)
    image_url = db.Column(db.String(255), nullable=True)
    is_featured = db.Column(db.Boolean, default=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    images = db.relationship("HeritageImage", backref="heritage_site", lazy=True, cascade="all, delete-orphan")
    reports = db.relationship("HeritageReport", backref="heritage_site", lazy=True, cascade="all, delete-orphan")
    risk_assessments = db.relationship("RiskAssessment", backref="heritage_site", lazy=True, cascade="all, delete-orphan")
    environmental_records = db.relationship("EnvironmentalData", backref="heritage_site", lazy=True, cascade="all, delete-orphan")
    tourist_pressures = db.relationship("TouristPressure", backref="heritage_site", lazy=True, cascade="all, delete-orphan")
    encroachments = db.relationship("EncroachmentObservation", backref="heritage_site", lazy=True, cascade="all, delete-orphan")
    timelines = db.relationship("ConditionTimeline", backref="heritage_site", lazy=True, cascade="all, delete-orphan")
    alerts = db.relationship("Alert", backref="heritage_site", lazy=True, cascade="all, delete-orphan")

    def to_dict(self, include_details=False):
        data = {
            "id": self.id,
            "state_id": self.state_id,
            "state_name": self.state.name if self.state else None,
            "state_code": self.state.map_identifier if self.state else None,
            "name": self.name,
            "city": self.city,
            "historical_period": self.historical_period,
            "heritage_category": self.heritage_category or "Monuments & Forts",
            "description": self.description,
            "cultural_significance": self.cultural_significance,
            "architecture": self.architecture,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "preservation_status": self.preservation_status,
            "current_health_score": self.current_health_score,
            "risk_level": self.risk_level,
            "carrying_capacity_daily": self.carrying_capacity_daily,
            "image_url": self.image_url,
            "is_featured": self.is_featured,
            "reports_count": len(self.reports),
            "active_alerts_count": len([a for a in self.alerts if a.status in ["Active", "Acknowledged", "Assigned"]]),
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

        if include_details:
            data["gallery"] = [img.to_dict() for img in self.images]
            latest_risk = self.risk_assessments[-1].to_dict() if self.risk_assessments else None
            latest_env = self.environmental_records[-1].to_dict() if self.environmental_records else None
            latest_tourist = self.tourist_pressures[-1].to_dict() if self.tourist_pressures else None
            
            data["latest_risk_assessment"] = latest_risk
            data["latest_environmental"] = latest_env
            data["latest_tourist_pressure"] = latest_tourist
            data["encroachments"] = [e.to_dict() for e in self.encroachments]
            data["timeline"] = [t.to_dict() for t in sorted(self.timelines, key=lambda x: x.year if x.year else 0)]
            data["alerts"] = [a.to_dict() for a in self.alerts]
            data["recent_reports"] = [r.to_dict() for r in sorted(self.reports, key=lambda x: x.created_at, reverse=True)[:5]]

        return data


class HeritageImage(db.Model):
    __tablename__ = "heritage_images"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    heritage_site_id = db.Column(db.Integer, db.ForeignKey("heritage_sites.id", ondelete="CASCADE"), nullable=False, index=True)
    image_url = db.Column(db.String(255), nullable=False)
    caption = db.Column(db.String(255), nullable=True)
    is_primary = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "heritage_site_id": self.heritage_site_id,
            "image_url": self.image_url,
            "caption": self.caption,
            "is_primary": self.is_primary,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
