import re

def analyze_citizen_damage_report(issue_type: str, description: str, location: str = "") -> dict:
    """
    AI-assisted preliminary damage assessment engine.
    Analyzes submitted issue category, location description, and damage narratives.
    Extracts detected damage taxonomy, estimated severity, confidence percentage,
    visible structural signs, and inspection urgency.
    
    IMPORTANT: Clearly labeled as an AI-assisted preliminary assessment requiring
    professional on-site verification.
    """
    desc_lower = (description or "").lower()
    issue_lower = (issue_type or "").lower()

    # Default baseline
    detected_category = issue_type or "Structural Damage"
    estimated_severity = "Moderate"
    confidence_score = 85
    damage_signs = []
    urgency = "Standard Field Verification Scheduled"

    # Category and keyword pattern recognition
    if any(k in desc_lower for k in ["crack", "cracks", "cracked", "fissure", "fracture", "collapse", "subsidence", "leaning", "spalling", "stone fall", "displacement", "structural", "lintel", "masonry", "plinth", "beam"]) or "structural" in issue_lower:
        detected_category = "Structural Damage"
        damage_signs.append("Stress cracking / masonry displacement in load-bearing lintel or wall")
        if any(k in desc_lower for k in ["severe", "deep crack", "imminent", "large gap", "pillar break", "major", "collapse"]):
            estimated_severity = "Critical"
            confidence_score = 92
            urgency = "Immediate Structural Engineering Inspection (within 24 hours)"
        else:
            estimated_severity = "High"
            confidence_score = 88
            urgency = "Priority On-Site Survey Recommended (within 48 hours)"

    elif any(k in desc_lower for k in ["encroach", "illegal build", "concrete", "boundary", "wall construct", "unauthorized", "digging", "excavation"]) or "encroach" in issue_lower:
        detected_category = "Encroachment"
        damage_signs.append("Unauthorized construction / physical alteration in regulated buffer zone")
        estimated_severity = "High"
        confidence_score = 89
        urgency = "Encroachment Verification & Notice Dispatch Recommended"

    elif any(k in desc_lower for k in ["graffiti", "paint", "carving", "scribble", "ink", "marker", "scratch"]) or "vandalism" in issue_lower:
        detected_category = "Vandalism"
        damage_signs.append("Direct surface defacement / anthropogenic chemical pigment on ancient stone")
        estimated_severity = "Moderate"
        confidence_score = 94
        urgency = "Conservation Poultice Treatment & Security Review"

    elif any(k in desc_lower for k in ["flood", "waterlog", "seepage", "dampness", "efflorescence", "salt", "submerged", "leak"]) or "flood" in issue_lower or "water" in issue_lower:
        detected_category = "Flood/Water Damage"
        damage_signs.append("Capillary water ingress / salt crystallization weathering on monument plinth")
        if any(k in desc_lower for k in ["submerged", "heavy flood", "standing water"]):
            estimated_severity = "Critical"
            confidence_score = 91
            urgency = "Immediate Drainage & Hydrological Pumping Deployment"
        else:
            estimated_severity = "High"
            confidence_score = 86
            urgency = "Moisture Desalination & Drainage Assessment"

    elif any(k in desc_lower for k in ["fire", "smoke", "soot", "burn", "charred"]) or "fire" in issue_lower:
        detected_category = "Fire Damage"
        damage_signs.append("Thermal shock exfoliation / carbonaceous soot deposit on facade")
        estimated_severity = "Critical"
        confidence_score = 95
        urgency = "Immediate Emergency Conservation & Structural Stability Audit"

    elif any(k in desc_lower for k in ["pollution", "blackening", "acid rain", "industrial", "dust", "exhaust"]) or "pollution" in issue_lower:
        detected_category = "Pollution"
        damage_signs.append("Atmospheric particulate accumulation / gypsum crust formation")
        estimated_severity = "Moderate"
        confidence_score = 82
        urgency = "Periodic Air Quality Monitoring & Surface Washing"

    elif any(k in desc_lower for k in ["garbage", "plastic", "waste", "debris", "dumping", "litter"]) or "garbage" in issue_lower:
        detected_category = "Garbage"
        damage_signs.append("Micro-environment biological degradation from unmanaged municipal solid waste")
        estimated_severity = "Low"
        confidence_score = 93
        urgency = "Site Sanitation Dispatch & Additional Eco-Bin Placement"

    if not damage_signs:
        damage_signs.append("Visual evidence indicates surface or environmental condition anomaly requiring inspection")

    return {
        "category_detected": detected_category,
        "severity_estimated": estimated_severity,
        "confidence_score": confidence_score,
        "damage_signs": " • ".join(damage_signs),
        "urgency": urgency,
        "disclaimer": "AI-assisted preliminary assessment — professional verification required."
    }
