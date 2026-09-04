class HealthScoreService:
    """
    Transparent Heritage Health Score Computation Engine (0 - 100).
    
    Formula Breakdown (100 Total Available Points):
      1. Structural Integrity & Masonry Health: 30 Points
      2. Citizen Reports & Unresolved Damage:   20 Points
      3. Encroachment & Buffer Zone Security:   15 Points
      4. Multi-Hazard Disaster Resilience:      15 Points
      5. Environmental & Air Quality Safety:    10 Points
      6. Tourist Footfall & Carrying Capacity:  10 Points
    """

    @classmethod
    def calculate_health_score(cls, site) -> dict:
        risk = site.risk_assessments[-1] if site.risk_assessments else None
        reports = [r for r in site.reports if r.status in ["Submitted", "Under Review", "Verified", "Action Required"]]
        encroachments = site.encroachments or []
        env = site.environmental_records[-1] if site.environmental_records else None
        tourist = site.tourist_pressures[-1] if site.tourist_pressures else None

        # 1. Structural Condition (Max 30 Points)
        struct_base = risk.structural_score if risk else 85
        if site.preservation_status == "Critical":
            struct_base = min(struct_base, 45)
        elif site.preservation_status == "Major Conservation Needed":
            struct_base = min(struct_base, 65)
        elif site.preservation_status == "Minor Restoration Required":
            struct_base = min(struct_base, 80)
        structural_pts = round((struct_base / 100.0) * 30.0, 1)

        # 2. Citizen Reports & Active Damage (Max 20 Points)
        reports_pts = 20.0
        for r in reports:
            if r.severity == "Critical":
                reports_pts -= 7.0
            elif r.severity == "High":
                reports_pts -= 4.0
            elif r.severity == "Moderate":
                reports_pts -= 2.0
            else:
                reports_pts -= 0.5
        reports_pts = max(0.0, round(reports_pts, 1))

        # 3. Encroachment Risk & Buffer Zone (Max 15 Points)
        enc_base = risk.encroachment_score if risk else 90
        for e in encroachments:
            if e.risk_level == "Critical":
                enc_base -= 25
            elif e.risk_level == "High":
                enc_base -= 15
            elif e.risk_level == "Moderate":
                enc_base -= 8
        enc_base = max(0, min(100, enc_base))
        encroachment_pts = round((enc_base / 100.0) * 15.0, 1)

        # 4. Disaster Resilience (Max 15 Points)
        disaster_base = risk.disaster_score if risk else 85
        disaster_pts = round((disaster_base / 100.0) * 15.0, 1)

        # 5. Environmental & Air Quality (Max 10 Points)
        env_pts = 10.0
        if env:
            aqi = env.air_quality_aqi
            if aqi > 250:
                env_pts -= 5.0
            elif aqi > 150:
                env_pts -= 3.0
            elif aqi > 100:
                env_pts -= 1.5
            if env.exposure_risk_status in ["High Risk", "Critical Warning"]:
                env_pts -= 3.0
        env_pts = max(0.0, round(env_pts, 1))

        # 6. Tourist Carrying Capacity (Max 10 Points)
        tourist_pts = 10.0
        if tourist:
            ratio = tourist.occupancy_ratio
            if ratio > 1.2: # Over capacity
                tourist_pts -= 5.0
            elif ratio > 0.9:
                tourist_pts -= 3.0
            elif ratio > 0.75:
                tourist_pts -= 1.5
        tourist_pts = max(0.0, round(tourist_pts, 1))

        # Total Computed Score
        total_score = int(round(structural_pts + reports_pts + encroachment_pts + disaster_pts + env_pts + tourist_pts))
        total_score = max(10, min(100, total_score))

        # Assign Risk Category
        if total_score >= 85:
            risk_level = "Low"
            status_text = "Healthy / Well Preserved"
        elif total_score >= 70:
            risk_level = "Moderate"
            status_text = "Attention Required"
        elif total_score >= 50:
            risk_level = "High"
            status_text = "High Risk / Active Threat"
        else:
            risk_level = "Critical"
            status_text = "Critical Emergency Intervention"

        return {
            "overall_health_score": total_score,
            "risk_level": risk_level,
            "status_text": status_text,
            "factor_breakdown": {
                "structural_integrity": {
                    "points_earned": structural_pts,
                    "max_points": 30.0,
                    "percentage": round((structural_pts / 30.0) * 100, 1),
                    "description": "Architectural masonry, load-bearing stability, and material preservation."
                },
                "citizen_reports_penalty": {
                    "points_earned": reports_pts,
                    "max_points": 20.0,
                    "percentage": round((reports_pts / 20.0) * 100, 1),
                    "description": f"Deductions based on {len(reports)} unresolved citizen incident report(s)."
                },
                "encroachment_security": {
                    "points_earned": encroachment_pts,
                    "max_points": 15.0,
                    "percentage": round((encroachment_pts / 15.0) * 100, 1),
                    "description": "100m/300m protected statutory buffer zone integrity."
                },
                "disaster_resilience": {
                    "points_earned": disaster_pts,
                    "max_points": 15.0,
                    "percentage": round((disaster_pts / 15.0) * 100, 1),
                    "description": "Multi-hazard exposure rating (Flood, Fire, Earthquake, Severe Weather)."
                },
                "environmental_safety": {
                    "points_earned": env_pts,
                    "max_points": 10.0,
                    "percentage": round((env_pts / 10.0) * 100, 1),
                    "description": "Air Quality (AQI), micro-climate humidity, and rain precipitation factors."
                },
                "tourist_pressure": {
                    "points_earned": tourist_pts,
                    "max_points": 10.0,
                    "percentage": round((tourist_pts / 10.0) * 100, 1),
                    "description": "Daily footfall vs monument carrying capacity thresholds."
                }
            }
        }
