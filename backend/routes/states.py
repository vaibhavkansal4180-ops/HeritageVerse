from flask import Blueprint
from backend.models import State
from backend.utils.response import success_response, error_response

states_bp = Blueprint("states", __name__, url_prefix="/api/states")

@states_bp.route("", methods=["GET"])
def get_all_states():
    """List all states and regions covered under the heritage monitoring network."""
    states = State.query.order_by(State.name.asc()).all()
    return success_response(data=[s.to_dict() for s in states], message=f"Retrieved {len(states)} states")

@states_bp.route("/<int:state_id>", methods=["GET"])
def get_state_by_id(state_id):
    """Get state details and monitored monuments."""
    state = State.query.get_or_404(state_id)
    return success_response(data=state.to_dict(include_sites=True), message=f"Details for {state.name} retrieved")

@states_bp.route("/code/<string:code>", methods=["GET"])
def get_state_by_code(code):
    """Get state by 2-letter state code (e.g. RJ, UP, MH)."""
    state = State.query.filter_by(map_identifier=code.upper()).first()
    if not state:
        return error_response(f"State with code '{code}' not found", status_code=404)
    return success_response(data=state.to_dict(include_sites=True), message=f"Details for {state.name} retrieved")
