from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from backend.models.user import User
from backend.models.state import State
from backend.models.heritage import HeritageSite, HeritageImage
from backend.models.report import HeritageReport, VandalismReport, ReportImage
from backend.models.preservation import (
    RiskAssessment,
    EnvironmentalData,
    TouristPressure,
    EncroachmentObservation,
    ConditionTimeline,
    Alert,
    AdminAction
)

from backend.models.discovery import (
    MonumentHistoryEvent,
    HeritageCraft,
    CulturalTradition,
    HeritageTrail,
    TrailStop,
    ThenVsNow,
    CommunityStory,
    HeritageSurrounding
)

__all__ = [
    "db",
    "User",
    "State",
    "HeritageSite",
    "HeritageImage",
    "HeritageReport",
    "VandalismReport",
    "ReportImage",
    "RiskAssessment",
    "EnvironmentalData",
    "TouristPressure",
    "EncroachmentObservation",
    "ConditionTimeline",
    "Alert",
    "AdminAction",
    "MonumentHistoryEvent",
    "HeritageCraft",
    "CulturalTradition",
    "HeritageTrail",
    "TrailStop",
    "ThenVsNow",
    "CommunityStory",
    "HeritageSurrounding"
]
