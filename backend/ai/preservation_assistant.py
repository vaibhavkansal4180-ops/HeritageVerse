def generate_site_preservation_brief(site_data: dict) -> dict:
    """
    AI-Assisted Preservation Decision Support Assistant.
    Generates contextual, multi-dimensional risk intelligence, priority reasoning,
    evidence justification, and an actionable on-site inspection checklist for any heritage monument.
    
    IMPORTANT: This is decision support for conservationists and administrators,
    not a generic chat bot. All recommendations are clearly labeled as requiring
    professional on-site verification.
    """
    site_name = site_data.get("name", "Heritage Monument")
    health_score = site_data.get("current_health_score", 80)
    risk_level = site_data.get("risk_level", "Low")
    
    risk_assessment = site_data.get("latest_risk_assessment") or {}
    unresolved_reports = site_data.get("recent_reports") or []
    unresolved_count = len(unresolved_reports)
    alerts = site_data.get("alerts") or []
    active_alerts = [a for a in alerts if a.get("status") in ["Active", "Acknowledged", "Assigned"]]
    
    encroachments = site_data.get("encroachments") or []
    environmental = site_data.get("latest_environmental") or {}
    tourist = site_data.get("latest_tourist_pressure") or {}

    # 1. Identify Top Current Threats
    threats = []
    if risk_assessment.get("structural_risk") in ["High", "Critical"] or any(r.get("severity") in ["High", "Critical"] for r in unresolved_reports):
        threats.append({
            "dimension": "Structural Stability",
            "severity": "HIGH",
            "description": "Masonry stress, joint degradation, or reported stone displacement requiring structural engineering appraisal."
        })

    if encroachments and any(e.get("risk_level") in ["High", "Critical", "Moderate"] for e in encroachments):
        threats.append({
            "dimension": "Regulated Buffer Zone Encroachment",
            "severity": "HIGH",
            "description": f"Detected unauthorized physical development or commercial footprint expansion within the protected boundary."
        })

    if environmental.get("air_quality_aqi", 0) > 150 or environmental.get("exposure_risk_status") in ["High Risk", "Critical Warning"]:
        threats.append({
            "dimension": "Environmental & Atmospheric Corrosion",
            "severity": "MODERATE",
            "description": f"Elevated AQI ({environmental.get('air_quality_aqi', 'High')}) / humidity cycles causing stone surface weathering and gypsum crusting."
        })

    if risk_assessment.get("flood_risk") in ["High", "Critical"]:
        threats.append({
            "dimension": "Hydrological / Flood Inundation",
            "severity": "HIGH",
            "description": "High seasonal flood exposure and rising water table threatening plinth foundation stability."
        })

    if tourist.get("pressure_level") in ["High", "Critical"] or (tourist.get("occupancy_ratio", 0) > 0.85):
        threats.append({
            "dimension": "High Tourist Footfall Stress",
            "severity": "MODERATE",
            "description": f"Daily footfall ({tourist.get('daily_visitors', 0):,} visitors) approaching maximum site carrying capacity threshold ({tourist.get('carrying_capacity', 5000):,})."
        })

    if not threats:
        threats.append({
            "dimension": "Routine Weathering",
            "severity": "LOW",
            "description": "Site condition is stable; ongoing preservation protocols and periodic maintenance are currently effective."
        })

    # 2. Priority Ranking & Rationale
    if health_score < 60 or risk_level == "Critical":
        priority_label = "CRITICAL (Immediate Multi-Agency Intervention)"
        rationale = f"{site_name} exhibits compound vulnerabilities with a degraded Health Score of {health_score}/100 and {len(active_alerts)} active alerts. Multi-hazard structural and environmental pressures exceed standard safety margins."
        first_issue = "Emergency structural stabilization and immediate barrier enforcement on reported breach zones."
    elif health_score < 75 or risk_level == "High":
        priority_label = "HIGH (Action Required within 7 Days)"
        rationale = f"Elevated risk profile driven by {unresolved_count} citizen report(s) and specific encroachment/environmental triggers. Timely mitigation will prevent irreversible structural loss."
        first_issue = "Detailed on-site inspection of reported damage locations and verification of protected zone demarcation."
    elif health_score < 85 or risk_level == "Moderate":
        priority_label = "MODERATE (Scheduled Conservation Audit)"
        rationale = f"Site is in fair operating condition with localized maintenance requirements. Crowd flow and environmental weathering should be actively monitored."
        first_issue = "Sanitation and surface poultice cleaning of exposed stone facades."
    else:
        priority_label = "LOW (Routine Preventative Maintenance)"
        rationale = f"{site_name} maintains a robust preservation health score of {health_score}/100 with no critical threshold breaches detected across monitoring streams."
        first_issue = "Continue quarterly structural baseline surveys and environmental sensor calibration."

    # 3. Evidence Trail
    evidence = []
    if unresolved_reports:
        evidence.append(f"{len(unresolved_reports)} citizen verification report(s) logged, including {unresolved_reports[0].get('issue_type', 'damage')} observation on {unresolved_reports[0].get('incident_date', 'recent dates')}.")
    if encroachments:
        evidence.append(f"Satellite/Drone observation recorded {encroachments[0].get('detected_change', 'unauthorized activity')} with {encroachments[0].get('confidence_pct', 88)}% detection confidence.")
    if environmental.get("air_quality_aqi"):
        evidence.append(f"Micro-climate sensor telemetry: AQI at {environmental.get('air_quality_aqi')} ({environmental.get('aqi_category', 'Moderate')}), Humidity {environmental.get('humidity_pct', 50)}%.")
    if tourist.get("daily_visitors"):
        evidence.append(f"Visitor analytics: {tourist.get('daily_visitors'):,} daily entries against a reference limit of {tourist.get('carrying_capacity'):,}.")

    if not evidence:
        evidence.append("Comprehensive automated baseline records show stable environmental and architectural parameters.")

    # 4. On-Site Inspection Checklist for Field Teams
    checklist = [
        {"item": "Plinth & Foundation Moisture Check", "detail": "Inspect outer plinth for salt efflorescence, rising capillary moisture, and drainage blockage."},
        {"item": "Masonry Joint & Mortar Cohesion", "detail": "Test lime mortar integrity in key archways and decorative cornices using non-destructive acoustic tapping."},
        {"item": "100m Prohibited Zone Verification", "detail": "Survey boundary perimeter pillars to verify zero unauthorized modern construction activity."},
        {"item": "Visitor Pressure Bottleneck Audit", "detail": "Verify crowd control stanchions along narrow internal corridors and sanctum walkways."},
        {"item": "Surface Biological Growth Removal", "detail": "Apply biocidal compress to remove lichen/algal colonies without stone abrasion."}
    ]

    # 5. Concrete Recommended Action Plan
    actions = [
        {
            "timeline": "Immediate (0 - 48 Hours)",
            "action": "Acknowledge active alerts in the Command Center and dispatch local conservation officer for photographic verification."
        },
        {
            "timeline": "Short-Term (1 - 4 Weeks)",
            "action": "Execute targeted restoration on verified damage spots and issue statutory encroachment notices if buffer violations are confirmed."
        },
        {
            "timeline": "Long-Term (1 - 6 Months)",
            "action": "Implement dynamic visitor time-slot ticketing to prevent peak-hour carrying capacity overruns and reinforce perimeter drainage."
        }
    ]

    return {
        "site_id": site_data.get("id"),
        "site_name": site_name,
        "health_score": health_score,
        "risk_level": risk_level,
        "priority_label": priority_label,
        "priority_rationale": rationale,
        "first_issue_to_address": first_issue,
        "top_threats": threats,
        "evidence_trail": evidence,
        "inspection_checklist": checklist,
        "recommended_actions": actions,
        "disclaimer": "AI-assisted recommendation — professional verification required."
    }
