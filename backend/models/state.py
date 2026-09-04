from datetime import datetime
from backend.models import db

class State(db.Model):
    __tablename__ = "states"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    map_identifier = db.Column(db.String(10), nullable=False, unique=True, index=True)
    description = db.Column(db.Text, nullable=True)
    history = db.Column(db.Text, nullable=True)
    culture = db.Column(db.Text, nullable=True)
    architecture = db.Column(db.Text, nullable=True)
    traditions = db.Column(db.Text, nullable=True)
    banner_image = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    heritage_sites = db.relationship("HeritageSite", backref="state", lazy=True, cascade="all, delete-orphan")

    def to_dict(self, include_sites=False):
        data = {
            "id": self.id,
            "name": self.name,
            "map_identifier": self.map_identifier,
            "description": self.description,
            "history": self.history,
            "culture": self.culture,
            "architecture": self.architecture,
            "traditions": self.traditions,
            "banner_image": self.banner_image,
            "sites_count": len(self.heritage_sites) if self.heritage_sites else 0,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
        if include_sites:
            data["heritage_sites"] = [site.to_dict() for site in self.heritage_sites]
        return data
