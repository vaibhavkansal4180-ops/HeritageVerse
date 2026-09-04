from datetime import datetime
import uuid
from backend.models import db

class RiskAssessment(db.Model):
    __tablename__ = "risk_assessments"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    heritage_site_id = db.Column(db.Integer, db.ForeignKey("heritage_sites.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Hazard Dimensions
    structural_risk = db.Column(db.String(20), default="Low")     # Low, Moderate, High, Critical
    structural_score = db.Column(db.Integer, default=85)          # 0-100 (100 is best)
    encroachment_risk = db.Column(db.String(20), default="Low")
    encroachment_score = db.Column(db.Integer, default=90)
    
    # Natural Disaster Risks
    flood_risk = db.Column(db.String(20), default="Low")
    fire_risk = db.Column(db.String(20), default="Low")
    earthquake_risk = db.Column(db.String(20), default="Low")
    weather_risk = db.Column(db.String(20), default="Low")
    disaster_score = db.Column(db.Integer, default=82)
    
    # Environmental & Visitor
    environmental_score = db.Column(db.Integer, default=85)
    tourist_pressure_score = db.Column(db.Integer, default=80)
    
    # Overall Computed Health Score (0 - 100)
    overall_health_score = db.Column(db.Integer, default=84)
    assessed_by = db.Column(db.String(100), default="Preservation Intelligence Engine")
    last_assessed_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "heritage_site_id": self.heritage_site_id,
            "structural_risk": self.structural_risk,
            "structural_score": self.structural_score,
            "encroachment_risk": self.encroachment_risk,
            "encroachment_score": self.encroachment_score,
            "flood_risk": self.flood_risk,
            "fire_risk": self.fire_risk,
            "earthquake_risk": self.earthquake_risk,
            "weather_risk": self.weather_risk,
            "disaster_score": self.disaster_score,
            "environmental_score": self.environmental_score,
            "tourist_pressure_score": self.tourist_pressure_score,
            "overall_health_score": self.overall_health_score,
            "assessed_by": self.assessed_by,
            "last_assessed_at": self.last_assessed_at.isoformat() if self.last_assessed_at else None
        }


class EnvironmentalData(db.Model):
    __tablename__ = "environmental_data"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    heritage_site_id = db.Column(db.Integer, db.ForeignKey("heritage_sites.id", ondelete="CASCADE"), nullable=False, index=True)
    
    temperature_c = db.Column(db.Float, default=28.5)
    humidity_pct = db.Column(db.Float, default=55.0)
    rainfall_mm = db.Column(db.Float, default=12.0)
    air_quality_aqi = db.Column(db.Integer, default=95)
    aqi_category = db.Column(db.String(50), default="Moderate") # Good, Moderate, Poor, Unhealthy, Severe
    flood_water_level_m = db.Column(db.Float, default=0.2)
    exposure_risk_status = db.Column(db.String(50), default="Normal") # Normal, Moderate Risk, High Risk, Critical Warning
    data_source = db.Column(db.String(50), default="DEMO_DATA")       # LIVE_API, DEMO_DATA, USER_ENTERED
    recorded_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "heritage_site_id": self.heritage_site_id,
            "temperature_c": self.temperature_c,
            "humidity_pct": self.humidity_pct,
            "rainfall_mm": self.rainfall_mm,
            "air_quality_aqi": self.air_quality_aqi,
            "aqi_category": self.aqi_category,
            "flood_water_level_m": self.flood_water_level_m,
            "exposure_risk_status": self.exposure_risk_status,
            "data_source": self.data_source,
            "recorded_at": self.recorded_at.isoformat() if self.recorded_at else None
        }


class TouristPressure(db.Model):
    __tablename__ = "tourist_pressure"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    heritage_site_id = db.Column(db.Integer, db.ForeignKey("heritage_sites.id", ondelete="CASCADE"), nullable=False, index=True)
    
    daily_visitors = db.Column(db.Integer, default=2400)
    monthly_visitors = db.Column(db.Integer, default=72000)
    carrying_capacity = db.Column(db.Integer, default=5000)
    occupancy_ratio = db.Column(db.Float, default=0.48) # daily_visitors / carrying_capacity
    pressure_level = db.Column(db.String(20), default="Moderate") # Low, Moderate, High, Critical
    trend = db.Column(db.String(20), default="Stable")             # Rising, Stable, Declining
    recorded_date = db.Column(db.Date, default=datetime.utcnow().date)

    def to_dict(self):
        return {
            "id": self.id,
            "heritage_site_id": self.heritage_site_id,
            "daily_visitors": self.daily_visitors,
            "monthly_visitors": self.monthly_visitors,
            "carrying_capacity": self.carrying_capacity,
            "occupancy_ratio": round(self.occupancy_ratio, 2),
            "pressure_level": self.pressure_level,
            "trend": self.trend,
            "recorded_date": self.recorded_date.isoformat() if self.recorded_date else None
        }


class EncroachmentObservation(db.Model):
    __tablename__ = "encroachment_observations"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    heritage_site_id = db.Column(db.Integer, db.ForeignKey("heritage_sites.id", ondelete="CASCADE"), nullable=False, index=True)
    
    monitored_zone = db.Column(db.String(150), nullable=False) # e.g. "100m Prohibited Buffer Zone (North-East Perimeter)"
    baseline_image_url = db.Column(db.String(255), nullable=True)
    baseline_date = db.Column(db.Date, nullable=False)
    latest_image_url = db.Column(db.String(255), nullable=True)
    latest_date = db.Column(db.Date, nullable=False)
    detected_change = db.Column(db.Text, nullable=False) # Description of change detected
    change_area_sqm = db.Column(db.Float, default=120.0)
    risk_level = db.Column(db.String(20), default="Moderate") # Low, Moderate, High, Critical
    confidence_pct = db.Column(db.Integer, default=88)
    verified_by_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "heritage_site_id": self.heritage_site_id,
            "heritage_site_name": self.heritage_site.name if self.heritage_site else None,
            "monitored_zone": self.monitored_zone,
            "baseline_image_url": self.baseline_image_url,
            "baseline_date": self.baseline_date.isoformat() if self.baseline_date else None,
            "latest_image_url": self.latest_image_url,
            "latest_date": self.latest_date.isoformat() if self.latest_date else None,
            "detected_change": self.detected_change,
            "change_area_sqm": self.change_area_sqm,
            "risk_level": self.risk_level,
            "confidence_pct": self.confidence_pct,
            "verified_by_admin": self.verified_by_admin,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


class ConditionTimeline(db.Model):
    __tablename__ = "condition_timeline"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    heritage_site_id = db.Column(db.Integer, db.ForeignKey("heritage_sites.id", ondelete="CASCADE"), nullable=False, index=True)
    
    year = db.Column(db.Integer, nullable=False)
    period_label = db.Column(db.String(50), nullable=True) # e.g. "2024 Q3", "2025 Annual Audit"
    condition_status = db.Column(db.String(50), default="Good") # Good, Attention Required, High Risk, Critical
    health_score = db.Column(db.Integer, default=85)
    event_type = db.Column(db.String(80), nullable=False) # Report Logged, Damage Verified, Environmental Alert, Encroachment Detected, Disaster Event, Admin Action, Restoration Completed
    summary = db.Column(db.Text, nullable=False)
    action_taken = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "heritage_site_id": self.heritage_site_id,
            "year": self.year,
            "period_label": self.period_label or str(self.year),
            "condition_status": self.condition_status,
            "health_score": self.health_score,
            "event_type": self.event_type,
            "summary": self.summary,
            "action_taken": self.action_taken,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


class Alert(db.Model):
    __tablename__ = "alerts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    alert_uid = db.Column(db.String(32), unique=True, nullable=False, index=True)
    heritage_site_id = db.Column(db.Integer, db.ForeignKey("heritage_sites.id", ondelete="CASCADE"), nullable=False, index=True)
    
    alert_type = db.Column(db.String(80), nullable=False) # Structural Alert, Citizen Surge Alert, Encroachment Alert, Disaster Risk Alert, Environmental Warning, Health Score Drop
    priority = db.Column(db.String(20), default="MODERATE", index=True) # LOW, MODERATE, HIGH, CRITICAL
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    trigger_reason = db.Column(db.Text, nullable=False)
    recommended_action = db.Column(db.Text, nullable=False)
    
    status = db.Column(db.String(30), default="Active", index=True) # Active, Acknowledged, Assigned, Resolved
    assigned_to = db.Column(db.String(150), nullable=True)
    action_notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    resolved_at = db.Column(db.DateTime, nullable=True)

    @staticmethod
    def generate_alert_uid():
        short_hex = uuid.uuid4().hex[:6].upper()
        return f"ALT-{datetime.utcnow().year}-{short_hex}"

    def to_dict(self):
        return {
            "id": self.id,
            "alert_uid": self.alert_uid,
            "heritage_site_id": self.heritage_site_id,
            "heritage_site_name": self.heritage_site.name if self.heritage_site else None,
            "heritage_site_city": self.heritage_site.city if self.heritage_site else None,
            "state_name": self.heritage_site.state.name if (self.heritage_site and self.heritage_site.state) else None,
            "alert_type": self.alert_type,
            "priority": self.priority,
            "title": self.title,
            "description": self.description,
            "trigger_reason": self.trigger_reason,
            "recommended_action": self.recommended_action,
            "status": self.status,
            "assigned_to": self.assigned_to,
            "action_notes": self.action_notes,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "resolved_at": self.resolved_at.isoformat() if self.resolved_at else None
        }


class AdminAction(db.Model):
    __tablename__ = "admin_actions"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    action_type = db.Column(db.String(100), nullable=False) # Alert Acknowledged, Report Status Modified, Risk Override, Restoration Dispatched
    target_entity = db.Column(db.String(50), nullable=False) # Report, Alert, Site
    target_id = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "action_type": self.action_type,
            "target_entity": self.target_entity,
            "target_id": self.target_id,
            "notes": self.notes,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
