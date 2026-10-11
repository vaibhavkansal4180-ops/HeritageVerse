from flask import Blueprint, request
from backend.models import db, HeritageSite, State
from backend.utils.response import success_response, error_response

heritage_bp = Blueprint("heritage", __name__, url_prefix="/api/heritage")

@heritage_bp.route("", methods=["GET"], strict_slashes=False)
@heritage_bp.route("/", methods=["GET"], strict_slashes=False)
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

    from sqlalchemy.orm import joinedload
    sites = query.options(joinedload(HeritageSite.state)).order_by(HeritageSite.id.asc()).all()

    # Deduplicate by normalized monument name ensuring clean unique catalog
    seen_names = set()
    unique_sites = []
    for site in sites:
        norm_name = site.name.strip().lower()
        if norm_name not in seen_names:
            seen_names.add(norm_name)
            unique_sites.append(site)

    # Sort alphabetically by name
    unique_sites.sort(key=lambda s: s.name.lower())

    return success_response(
        data=[site.to_dict() for site in unique_sites],
        message=f"Retrieved {len(unique_sites)} monitored heritage sites"
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
    ).order_by(HeritageSite.id.asc()).all()

    seen_names = set()
    unique_sites = []
    for site in sites:
        norm_name = site.name.strip().lower()
        if norm_name not in seen_names:
            seen_names.add(norm_name)
            unique_sites.append(site)

    return success_response(
        data=[site.to_dict() for site in unique_sites],
        message=f"Found {len(unique_sites)} monuments matching '{query_str}'"
    )


@heritage_bp.route("/<int:site_id>", methods=["GET"])
def get_heritage_site_by_id(site_id):
    """
    Get detailed profile of a monitored heritage site including gallery and recent records.
    """
    site = HeritageSite.query.get_or_404(site_id)
    return success_response(data=site.to_dict(include_details=True), message=f"Details for '{site.name}' retrieved")
