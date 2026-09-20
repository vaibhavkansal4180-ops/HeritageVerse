from flask import Blueprint, request, jsonify
from backend.models import (
    db,
    HeritageSite,
    MonumentHistoryEvent,
    HeritageCraft,
    CulturalTradition,
    HeritageTrail,
    TrailStop,
    ThenVsNow,
    CommunityStory,
    HeritageSurrounding
)
from backend.services.health_score_service import HealthScoreService
from backend.services.heritage_doctor_service import HeritageDoctorService
from backend.services.what_if_service import WhatIfSimulationService

discovery_bp = Blueprint("discovery", __name__, url_prefix="/api")

# ==========================================
# 1. FULL HERITAGE PROFILE 2.0
# ==========================================
@discovery_bp.route("/heritage/sites/<int:site_id>/full-profile", methods=["GET"])
def get_full_site_profile(site_id):
    """
    Returns unified 360-degree monument dossier combining:
    - Core details & Architectural classification
    - History & Timeline ledger
    - Living Culture & Crafts
    - Cultural Traditions & Festivals
    - Then vs Now Visual Comparisons
    - Surroundings & Urban Context
    - Community Stories & Oral Histories
    - Real-time Health Score breakdown & Provenance
    - Heritage Doctor Clinical Appraisal
    """
    site = db.session.get(HeritageSite, site_id)
    if not site:
        return jsonify({"error": "Heritage site not found"}), 404

    site_data = site.to_dict(include_details=True)
    health_analysis = HealthScoreService.calculate_health_score(site)
    doctor_appraisal = HeritageDoctorService.diagnose_site(site)

    profile = {
        "site": site_data,
        "health_analysis": health_analysis,
        "heritage_doctor": doctor_appraisal,
        "history_events": [h.to_dict() for h in sorted(site.history_events, key=lambda x: x.year if x.year else 0)],
        "crafts": [c.to_dict() for c in site.crafts],
        "traditions": [t.to_dict() for t in site.traditions],
        "then_vs_now": [tvn.to_dict() for tvn in site.then_vs_now],
        "surroundings": [s.to_dict() for s in site.surroundings],
        "community_stories": [cs.to_dict() for cs in site.community_stories if cs.status == "Verified"],
        "gallery": [img.to_dict() for img in site.images],
        "data_provenance": {
            "official_records": "Archaeological Survey of India & UNESCO World Heritage Centre",
            "condition_telemetry": "HeritageVerse Active Multi-Sensor & Satellite Analysis",
            "cultural_documentation": "National Living Traditions & Crafts Registry",
            "citizen_contributions": f"{len(site.community_stories)} Citizen Oral History Submission(s)"
        }
    }
    return jsonify(profile), 200


# ==========================================
# 2. HISTORICAL STORYTELLING & TIMELINE
# ==========================================
@discovery_bp.route("/heritage/history/<int:site_id>", methods=["GET"])
def get_site_history(site_id):
    site = db.session.get(HeritageSite, site_id)
    if not site:
        return jsonify({"error": "Heritage site not found"}), 404
    
    events = MonumentHistoryEvent.query.filter_by(heritage_site_id=site_id).order_by(MonumentHistoryEvent.year.asc()).all()
    return jsonify({
        "site_id": site.id,
        "site_name": site.name,
        "total_events": len(events),
        "timeline": [e.to_dict() for e in events]
    }), 200


@discovery_bp.route("/heritage/history", methods=["POST"])
def add_history_event():
    data = request.get_json() or {}
    site_id = data.get("heritage_site_id")
    if not site_id or not data.get("title") or not data.get("year_display"):
        return jsonify({"error": "heritage_site_id, title, and year_display are required"}), 400

    site = db.session.get(HeritageSite, site_id)
    if not site:
        return jsonify({"error": "Heritage site not found"}), 404

    event = MonumentHistoryEvent(
        heritage_site_id=site_id,
        year=data.get("year"),
        year_display=data.get("year_display"),
        title=data.get("title"),
        description=data.get("description", ""),
        category=data.get("category", "Historical Event"),
        source_name=data.get("source_name", "Curated Historical Archive"),
        source_url=data.get("source_url"),
        source_type=data.get("source_type", "CURATED"),
        verification_status="VERIFIED"
    )
    db.session.add(event)
    db.session.commit()
    return jsonify({"message": "History event added successfully", "event": event.to_dict()}), 201


# ==========================================
# 3. LIVING CULTURE & ARTISAN CRAFTS
# ==========================================
@discovery_bp.route("/heritage/crafts", methods=["GET"])
def list_crafts():
    site_id = request.args.get("site_id", type=int)
    state_id = request.args.get("state_id", type=int)
    category = request.args.get("category")

    query = HeritageCraft.query
    if site_id:
        query = query.filter_by(heritage_site_id=site_id)
    if state_id:
        query = query.filter_by(state_id=state_id)
    if category:
        query = query.filter(HeritageCraft.category.ilike(f"%{category}%"))

    crafts = query.all()
    return jsonify({
        "total": len(crafts),
        "crafts": [c.to_dict() for c in crafts]
    }), 200


@discovery_bp.route("/heritage/crafts/<int:craft_id>", methods=["GET"])
def get_craft_detail(craft_id):
    craft = db.session.get(HeritageCraft, craft_id)
    if not craft:
        return jsonify({"error": "Heritage craft not found"}), 404
    return jsonify(craft.to_dict()), 200


# ==========================================
# 4. CULTURAL TRADITIONS & FESTIVALS
# ==========================================
@discovery_bp.route("/heritage/traditions", methods=["GET"])
def list_traditions():
    site_id = request.args.get("site_id", type=int)
    state_id = request.args.get("state_id", type=int)
    tradition_type = request.args.get("type")

    query = CulturalTradition.query
    if site_id:
        query = query.filter_by(heritage_site_id=site_id)
    if state_id:
        query = query.filter_by(state_id=state_id)
    if tradition_type:
        query = query.filter(CulturalTradition.tradition_type.ilike(f"%{tradition_type}%"))

    traditions = query.all()
    return jsonify({
        "total": len(traditions),
        "traditions": [t.to_dict() for t in traditions]
    }), 200


@discovery_bp.route("/heritage/traditions/<int:tradition_id>", methods=["GET"])
def get_tradition_detail(tradition_id):
    tradition = db.session.get(CulturalTradition, tradition_id)
    if not tradition:
        return jsonify({"error": "Cultural tradition not found"}), 404
    return jsonify(tradition.to_dict()), 200


# ==========================================
# 5. HERITAGE TRAILS
# ==========================================
@discovery_bp.route("/heritage/trails", methods=["GET"])
def list_trails():
    theme = request.args.get("theme")
    query = HeritageTrail.query
    if theme:
        query = query.filter(HeritageTrail.theme.ilike(f"%{theme}%"))
    
    trails = query.all()
    return jsonify({
        "total": len(trails),
        "trails": [t.to_dict(include_stops=True) for t in trails]
    }), 200


@discovery_bp.route("/heritage/trails/<identifier>", methods=["GET"])
def get_trail_detail(identifier):
    if identifier.isdigit():
        trail = db.session.get(HeritageTrail, int(identifier))
    else:
        trail = HeritageTrail.query.filter_by(slug=identifier).first()

    if not trail:
        return jsonify({"error": "Heritage trail not found"}), 404
    return jsonify(trail.to_dict(include_stops=True)), 200


# ==========================================
# 6. THEN VS NOW ARCHIVAL COMPARISONS
# ==========================================
@discovery_bp.route("/heritage/then-vs-now", methods=["GET"])
def list_then_vs_now():
    site_id = request.args.get("site_id", type=int)
    query = ThenVsNow.query
    if site_id:
        query = query.filter_by(heritage_site_id=site_id)
    
    comparisons = query.all()
    return jsonify({
        "total": len(comparisons),
        "comparisons": [c.to_dict() for c in comparisons]
    }), 200


# ==========================================
# 7. HERITAGE SURROUNDINGS CONTEXT
# ==========================================
@discovery_bp.route("/heritage/surroundings/<int:site_id>", methods=["GET"])
def get_site_surroundings(site_id):
    surroundings = HeritageSurrounding.query.filter_by(heritage_site_id=site_id).all()
    return jsonify({
        "heritage_site_id": site_id,
        "total": len(surroundings),
        "surroundings": [s.to_dict() for s in surroundings]
    }), 200


# ==========================================
# 8. COMMUNITY STORIES & ORAL HISTORIES
# ==========================================
@discovery_bp.route("/community/stories", methods=["GET"])
def list_community_stories():
    site_id = request.args.get("site_id", type=int)
    story_type = request.args.get("type")
    include_all = request.args.get("all", "").lower() == "true"

    query = CommunityStory.query
    if not include_all:
        query = query.filter_by(status="Verified")

    if site_id:
        query = query.filter_by(heritage_site_id=site_id)
    if story_type:
        query = query.filter(CommunityStory.story_type.ilike(f"%{story_type}%"))

    stories = query.order_by(CommunityStory.created_at.desc()).all()
    return jsonify({
        "total": len(stories),
        "stories": [s.to_dict() for s in stories]
    }), 200


@discovery_bp.route("/community/stories", methods=["POST"])
def submit_community_story():
    data = request.get_json() or {}
    site_id = data.get("heritage_site_id")
    title = data.get("title")
    story_content = data.get("story_content")
    author_name = data.get("author_name")

    if not site_id or not title or not story_content or not author_name:
        return jsonify({"error": "heritage_site_id, title, story_content, and author_name are required"}), 400

    site = db.session.get(HeritageSite, int(site_id))
    if not site:
        return jsonify({"error": "Heritage site not found"}), 404

    story = CommunityStory(
        heritage_site_id=site.id,
        author_name=author_name.strip(),
        author_role=data.get("author_role", "Heritage Enthusiast"),
        author_email=data.get("author_email"),
        title=title.strip(),
        story_content=story_content.strip(),
        story_type=data.get("story_type", "Memory"),
        historical_period=data.get("historical_period", "Living Memory"),
        image_url=data.get("image_url"),
        status="Verified", # Auto-publish verified for immediate exploration & demo
        source_type="COMMUNITY"
    )
    db.session.add(story)
    db.session.commit()

    return jsonify({
        "message": "Thank you for contributing your memory to HeritageVerse! Your story is published.",
        "story": story.to_dict()
    }), 201


@discovery_bp.route("/community/stories/<int:story_id>", methods=["GET"])
def get_community_story(story_id):
    story = db.session.get(CommunityStory, story_id)
    if not story:
        return jsonify({"error": "Community story not found"}), 404
    return jsonify(story.to_dict()), 200
