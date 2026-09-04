from backend.routes.auth import auth_bp
from backend.routes.states import states_bp
from backend.routes.heritage import heritage_bp
from backend.routes.reports import reports_bp
from backend.routes.admin import admin_bp
from backend.routes.stats import stats_bp
from backend.routes.preservation import preservation_bp
from backend.routes.alerts import alerts_bp

__all__ = [
    "auth_bp",
    "states_bp",
    "heritage_bp",
    "reports_bp",
    "admin_bp",
    "stats_bp",
    "preservation_bp",
    "alerts_bp"
]
