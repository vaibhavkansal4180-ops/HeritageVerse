from flask import Blueprint, request
from backend.models import db, HeritageSite, State
from backend.utils.response import success_response, error_response

heritage_bp = Blueprint("heritage", __name__, url_prefix="/api/heritage")

@heritage_bp.route("", methods=["GET"])
def get_all_heritage_sites():
    """
    List all monitored heritage sites with filtering by state, category, risk level, or health score.
    """
    state_id = request.args.get("state_id", type=int)
    category = request.args.get("category")
    risk_level = request.args.get("risk_level")
    is_featured = request.args.get("featured")

    query = HeritageSite.query

    if state_id:
        query = query.filter_by(state_id=state_id)
    if category:
        query = query.filter(HeritageSite.heritage_category.ilike(f"%{category}%"))
    if risk_level:
        query = query.filter_by(risk_level=risk_level)
    if is_featured is not None:
        query = query.filter_by(is_featured=(is_featured.lower() == "true"))

    sites = query.order_by(HeritageSite.name.asc()).all()
    return success_response(
        data=[site.to_dict() for site in sites],
        message=f"Retrieved {len(sites)} monitored heritage sites"
    )


@heritage_bp.route("/search", methods=["GET"])
def search_heritage_sites():
    """
    Full-text search for heritage monuments by name, city, historical era, or category.
    """
    query_str = request.args.get("q", "").strip()
    if not query_str:
        return success_response(data=[], message="No search query provided")

    term = f"%{query_str}%"
    sites = HeritageSite.query.filter(
        (HeritageSite.name.ilike(term)) |
        (HeritageSite.city.ilike(term)) |
        (HeritageSite.historical_period.ilike(term)) |
        (HeritageSite.description.ilike(term)) |
        (HeritageSite.heritage_category.ilike(term))
    ).all()

    return success_response(
        data=[site.to_dict() for site in sites],
        message=f"Found {len(sites)} monuments matching '{query_str}'"
    )


@heritage_bp.route("/<int:site_id>", methods=["GET"])
def get_heritage_site_by_id(site_id):
    """
    Get detailed profile of a monitored heritage site including gallery and recent records.
    """
    site = HeritageSite.query.get_or_404(site_id)
    return success_response(data=site.to_dict(include_details=True), message=f"Details for '{site.name}' retrieved")
