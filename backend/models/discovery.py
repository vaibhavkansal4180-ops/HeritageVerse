from datetime import datetime
from backend.models import db

class MonumentHistoryEvent(db.Model):
    __tablename__ = "monument_history_events"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    heritage_site_id = db.Column(db.Integer, db.ForeignKey("heritage_sites.id", ondelete="CASCADE"), nullable=False, index=True)
    
    year = db.Column(db.Integer, nullable=True)                  # Numeric year for sorting (e.g. 1250, 1632, 1984)
    year_display = db.Column(db.String(50), nullable=False)      # Formatted display (e.g. "1250 CE", "1632–1653 CE", "1984 CE")
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    
    # Categories: Construction, Historical Event, Cultural Event, Architectural Change, Restoration, Conservation, Modern Status
    category = db.Column(db.String(80), default="Historical Event", index=True)
    
    source_name = db.Column(db.String(200), default="Archaeological Survey of India & UNESCO Archives")
    source_url = db.Column(db.String(255), nullable=True)
    source_type = db.Column(db.String(50), default="CURATED")   # OFFICIAL, ACADEMIC, CURATED, COMMUNITY, SIMULATED
    verification_status = db.Column(db.String(50), default="VERIFIED") # VERIFIED, CURATED, UNDER_REVIEW
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "heritage_site_id": self.heritage_site_id,
            "year": self.year,
            "year_display": self.year_display,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "source_name": self.source_name,
            "source_url": self.source_url,
            "source_type": self.source_type,
            "verification_status": self.verification_status,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


class HeritageCraft(db.Model):
    __tablename__ = "heritage_crafts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    heritage_site_id = db.Column(db.Integer, db.ForeignKey("heritage_sites.id", ondelete="CASCADE"), nullable=False, index=True)
    state_id = db.Column(db.Integer, db.ForeignKey("states.id", ondelete="SET NULL"), nullable=True)
    
    name = db.Column(db.String(150), nullable=False)             # e.g. "Pietra Dura Marble Inlay", "Stone Carving & Chlorite Sculpting"
    category = db.Column(db.String(80), default="Stone Craft")  # Stone Craft, Textile, Metalwork, Pottery, Painting, Woodwork
    description = db.Column(db.Text, nullable=False)
    materials_and_technique = db.Column(db.Text, nullable=True)
    cultural_significance = db.Column(db.Text, nullable=True)
    artisan_cluster_location = db.Column(db.String(200), nullable=True) # e.g. "Taj Ganj Artisan Quarter, Agra"
    image_url = db.Column(db.String(255), nullable=True)
    source_name = db.Column(db.String(200), default="National Handicrafts Registry & Living Traditions Documentation")
    source_type = db.Column(db.String(50), default="CURATED")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "heritage_site_id": self.heritage_site_id,
            "heritage_site_name": self.heritage_site.name if self.heritage_site else None,
            "state_id": self.state_id,
            "name": self.name,
            "category": self.category,
            "description": self.description,
            "materials_and_technique": self.materials_and_technique,
            "cultural_significance": self.cultural_significance,
            "artisan_cluster_location": self.artisan_cluster_location,
            "image_url": self.image_url,
            "source_name": self.source_name,
            "source_type": self.source_type,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


class CulturalTradition(db.Model):
    __tablename__ = "cultural_traditions"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    heritage_site_id = db.Column(db.Integer, db.ForeignKey("heritage_sites.id", ondelete="CASCADE"), nullable=False, index=True)
    state_id = db.Column(db.Integer, db.ForeignKey("states.id", ondelete="SET NULL"), nullable=True)
    
    title = db.Column(db.String(150), nullable=False)           # e.g. "Konark Dance & Music Festival", "Taj Mahotsav"
    tradition_type = db.Column(db.String(80), default="Festival") # Festival, Performing Art, Ritual Practice, Folklore & Oral Tradition
    season_or_timing = db.Column(db.String(100), nullable=True) # e.g. "December Annually (Winter Solstice)", "February Springtime"
    description = db.Column(db.Text, nullable=False)
    community_role = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(255), nullable=True)
    source_name = db.Column(db.String(200), default="Living Cultural Heritage Documentation")
    source_type = db.Column(db.String(50), default="CURATED")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "heritage_site_id": self.heritage_site_id,
            "heritage_site_name": self.heritage_site.name if self.heritage_site else None,
            "state_id": self.state_id,
            "title": self.title,
            "tradition_type": self.tradition_type,
            "season_or_timing": self.season_or_timing,
            "description": self.description,
            "community_role": self.community_role,
            "image_url": self.image_url,
            "source_name": self.source_name,
            "source_type": self.source_type,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


class HeritageTrail(db.Model):
    __tablename__ = "heritage_trails"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(150), nullable=False, unique=True)
    slug = db.Column(db.String(100), nullable=False, unique=True, index=True)
    theme = db.Column(db.String(100), nullable=False)           # e.g. "Imperial Mughal Architecture", "Dravidian Temple Geometry"
    description = db.Column(db.Text, nullable=False)
    historical_era = db.Column(db.String(100), nullable=True)
    estimated_duration = db.Column(db.String(80), default="2 Days")
    difficulty = db.Column(db.String(50), default="Leisurely Exploration")
    featured_image_url = db.Column(db.String(255), nullable=True)
    is_featured = db.Column(db.Boolean, default=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    stops = db.relationship("TrailStop", backref="trail", lazy=True, cascade="all, delete-orphan", order_by="TrailStop.stop_order")

    def to_dict(self, include_stops=True):
        data = {
            "id": self.id,
            "title": self.title,
            "slug": self.slug,
            "theme": self.theme,
            "description": self.description,
            "historical_era": self.historical_era,
            "estimated_duration": self.estimated_duration,
            "difficulty": self.difficulty,
            "featured_image_url": self.featured_image_url,
            "is_featured": self.is_featured,
            "total_stops": len(self.stops),
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
        if include_stops:
            data["stops"] = [s.to_dict() for s in self.stops]
        return data


class TrailStop(db.Model):
    __tablename__ = "trail_stops"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    trail_id = db.Column(db.Integer, db.ForeignKey("heritage_trails.id", ondelete="CASCADE"), nullable=False, index=True)
    heritage_site_id = db.Column(db.Integer, db.ForeignKey("heritage_sites.id", ondelete="CASCADE"), nullable=False, index=True)
    
    stop_order = db.Column(db.Integer, nullable=False, default=1)
    stop_title = db.Column(db.String(150), nullable=False)
    narrative_focus = db.Column(db.Text, nullable=False)
    recommended_time_hours = db.Column(db.Float, default=3.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    site = db.relationship("HeritageSite", backref="trail_appearances", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "trail_id": self.trail_id,
            "heritage_site_id": self.heritage_site_id,
            "heritage_site_name": self.site.name if self.site else None,
            "heritage_site_city": self.site.city if self.site else None,
            "heritage_site_image": self.site.image_url if self.site else None,
            "heritage_site_era": self.site.historical_period if self.site else None,
            "stop_order": self.stop_order,
            "stop_title": self.stop_title,
            "narrative_focus": self.narrative_focus,
            "recommended_time_hours": self.recommended_time_hours,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


class ThenVsNow(db.Model):
    __tablename__ = "then_vs_now_comparisons"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    heritage_site_id = db.Column(db.Integer, db.ForeignKey("heritage_sites.id", ondelete="CASCADE"), nullable=False, index=True)
    
    title = db.Column(db.String(150), nullable=False)
    historical_year = db.Column(db.String(50), nullable=False)  # e.g. "1865 CE Archival Survey", "1905 British Archaeological Record"
    historical_image_url = db.Column(db.String(255), nullable=False)
    historical_image_caption = db.Column(db.String(255), nullable=True)
    
    current_year = db.Column(db.String(50), default="2026 CE Present")
    current_image_url = db.Column(db.String(255), nullable=False)
    current_image_caption = db.Column(db.String(255), nullable=True)
    
    # Categories: Structure, Surroundings, Urbanization, Restoration, Landscape
    comparison_category = db.Column(db.String(80), default="Structure")
    observations_text = db.Column(db.Text, nullable=False)
    source_name = db.Column(db.String(200), default="Archaeological Survey Photographic Archives")
    source_type = db.Column(db.String(50), default="CURATED")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "heritage_site_id": self.heritage_site_id,
            "heritage_site_name": self.heritage_site.name if self.heritage_site else None,
            "title": self.title,
            "historical_year": self.historical_year,
            "historical_image_url": self.historical_image_url,
            "historical_image_caption": self.historical_image_caption,
            "current_year": self.current_year,
            "current_image_url": self.current_image_url,
            "current_image_caption": self.current_image_caption,
            "comparison_category": self.comparison_category,
            "observations_text": self.observations_text,
            "source_name": self.source_name,
            "source_type": self.source_type,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


class CommunityStory(db.Model):
    __tablename__ = "community_stories"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    heritage_site_id = db.Column(db.Integer, db.ForeignKey("heritage_sites.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    
    author_name = db.Column(db.String(100), nullable=False)
    author_role = db.Column(db.String(80), default="Heritage Enthusiast") # Local Resident, Artisan, Historian, Pilgrim, Visitor
    author_email = db.Column(db.String(150), nullable=True)
    
    title = db.Column(db.String(200), nullable=False)
    story_content = db.Column(db.Text, nullable=False)
    story_type = db.Column(db.String(60), default="Memory") # Oral History, Memory, Folk Anecdote, Traditional Practice, Archival Photograph
    historical_period = db.Column(db.String(100), nullable=True) # e.g. "1970s", "Living Memory", "Ancestral Folklore"
    image_url = db.Column(db.String(255), nullable=True)
    
    # Moderation Status: Pending, Verified, Rejected
    status = db.Column(db.String(30), default="Verified", index=True)
    moderation_notes = db.Column(db.Text, nullable=True)
    moderated_by = db.Column(db.String(100), nullable=True)
    moderated_at = db.Column(db.DateTime, nullable=True)
    
    source_type = db.Column(db.String(50), default="COMMUNITY") # COMMUNITY
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "heritage_site_id": self.heritage_site_id,
            "heritage_site_name": self.heritage_site.name if self.heritage_site else None,
            "author_name": self.author_name,
            "author_role": self.author_role,
            "title": self.title,
            "story_content": self.story_content,
            "story_type": self.story_type,
            "historical_period": self.historical_period,
            "image_url": self.image_url,
            "status": self.status,
            "moderation_notes": self.moderation_notes,
            "source_type": self.source_type,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


class HeritageSurrounding(db.Model):
    __tablename__ = "heritage_surroundings"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    heritage_site_id = db.Column(db.Integer, db.ForeignKey("heritage_sites.id", ondelete="CASCADE"), nullable=False, index=True)
    
    factor_type = db.Column(db.String(80), nullable=False) # Urban Development, River Basin, Craft Cluster, Buffer Greenery, Transport Node
    name = db.Column(db.String(150), nullable=False)       # e.g. "Yamuna River Floodplain & Desiccation Zone", "Mehtab Bagh Northern Buffer"
    distance_meters = db.Column(db.Integer, default=150)
    description = db.Column(db.Text, nullable=False)
    impact_nature = db.Column(db.String(50), default="Monitored Concern") # Cultural Asset, Buffer Protection, Monitored Concern, Positive Ecosystem
    status = db.Column(db.String(50), default="Active")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "heritage_site_id": self.heritage_site_id,
            "factor_type": self.factor_type,
            "name": self.name,
            "distance_meters": self.distance_meters,
            "description": self.description,
            "impact_nature": self.impact_nature,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
