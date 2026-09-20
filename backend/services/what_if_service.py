class WhatIfSimulationService:
    """
    Predictive Heritage Scenario Simulation Engine.
    Simulates monument condition deltas under hypothetical environmental,
    visitor, encroachment, and maintenance policy interventions.
    """

    @classmethod
    def simulate_scenario(cls, site, params: dict) -> dict:
        """
        Runs a simulation given baseline site data and user parameter overrides.
        
        Supported parameters in params:
        - tourist_multiplier: float (0.2 to 2.5, default 1.0)
        - aqi: int (10 to 500, default None -> uses current site env AQI)
        - monsoon_severity: str ('normal', 'heavy', 'cyclone_flood', default 'normal')
        - buffer_intrusion: str ('none', 'minor_50m', 'severe_regulated_breach', default 'none')
        - maintenance_regime: str ('optimal', 'regular', 'deferred_1yr', 'deferred_3yr', 'active_restoration', default 'regular')
        - green_buffer_expanded: bool (default False)
        - visitor_timed_entry: bool (default False)
        """
        # Baseline score calculation
        from backend.services.health_score_service import HealthScoreService
        base_breakdown = HealthScoreService.calculate_health_score(site)
        baseline_score = base_breakdown["overall_health_score"]
        baseline_risk = base_breakdown["risk_level"]

        # Parse inputs
        tourist_mult = float(params.get("tourist_multiplier", 1.0))
        aqi = int(params.get("aqi", 0))
        if aqi <= 0:
            env_rec = site.environmental_records[-1] if site.environmental_records else None
            aqi = env_rec.air_quality_aqi if env_rec else 85

        monsoon = str(params.get("monsoon_severity", "normal")).lower()
        buffer_intrusion = str(params.get("buffer_intrusion", "none")).lower()
        maintenance = str(params.get("maintenance_regime", "regular")).lower()
        green_buffer = bool(params.get("green_buffer_expanded", False))
        timed_entry = bool(params.get("visitor_timed_entry", False))

        # Factor Attribution Calculations
        delta_tourist = 0.0
        delta_env = 0.0
        delta_struct = 0.0
        delta_encroach = 0.0
        delta_disaster = 0.0
        interventions = []

        # 1. Tourist Impact
        if timed_entry:
            tourist_mult = min(tourist_mult, 1.0)
            interventions.append("Timed digital ticketing caps peak surge footfall within safe carrying capacity.")
            delta_tourist += 2.0

        if tourist_mult > 1.8:
            delta_tourist -= 7.0
            interventions.append("Surge footfall (>180% capacity) causes rapid micro-abrasion of sandstone flooring and indoor humidity spikes.")
        elif tourist_mult > 1.3:
            delta_tourist -= 4.0
            interventions.append("High visitor density accelerates wear on decorative carvings and stairs.")
        elif tourist_mult < 0.7:
            delta_tourist += 2.5
            interventions.append("Reduced visitor density significantly minimizes micro-climatic thermal shock inside inner sanctums.")

        # 2. AQI & Air Quality Impact
        if green_buffer:
            aqi = max(25, aqi - 45)
            delta_env += 3.0
            interventions.append("Expanding green buffer corridors filters particulate matter and lowers localized ambient surface heat.")

        if aqi > 300:
            delta_env -= 6.5
            interventions.append("Severe particulate pollution (AQI >300) induces chemical sulfation and marble/sandstone yellowing.")
        elif aqi > 200:
            delta_env -= 4.0
            interventions.append("Unhealthy air quality accelerates surface crust formation and acid deposition.")
        elif aqi < 60:
            delta_env += 2.0
            interventions.append("Pristine air quality arrests acid deposition and surface corrosion rates.")

        # 3. Monsoon & Water Ingress / Flooding
        if monsoon == "cyclone_flood":
            delta_disaster -= 10.0
            delta_struct -= 5.0
            interventions.append("Extreme flood / cyclone event threatens plinth drainage inundation, rising damp, and foundation scour.")
        elif monsoon == "heavy":
            delta_disaster -= 4.0
            delta_struct -= 2.0
            interventions.append("Heavy prolonged monsoon increases subterranean capillary moisture migration and algal colonization.")
        else:
            delta_disaster += 1.0

        # 4. Encroachment & Statutory Buffer Zone
        if buffer_intrusion == "severe_regulated_breach":
            delta_encroach -= 9.0
            interventions.append("Unregulated commercial building in 100m Prohibited Area breaches statutory AMASR Act and damages sightlines.")
        elif buffer_intrusion == "minor_50m":
            delta_encroach -= 4.5
            interventions.append("Minor unauthorized stalls/structures in 300m Regulated Zone add vibration, waste, and visual obstruction.")
        else:
            delta_encroach += 1.5

        # 5. Maintenance & Conservation Regime
        if maintenance == "active_restoration":
            delta_struct += 8.0
            interventions.append("Active lime-mortar consolidation and sacrificial poulticing substantially improves structural longevity.")
        elif maintenance == "optimal":
            delta_struct += 4.0
            interventions.append("Proactive quarterly structural telemetry and non-invasive repointing maintains optimal resilience.")
        elif maintenance == "deferred_1yr":
            delta_struct -= 4.0
            interventions.append("Deferring seasonal grouting and micro-crack sealing increases vulnerability to weathering.")
        elif maintenance == "deferred_3yr":
            delta_struct -= 10.0
            interventions.append("Prolonged deferred maintenance (3 years) risks irreversible spalling, stone detachment, and load shift.")

        # Sum of deltas
        total_delta = round(delta_tourist + delta_env + delta_struct + delta_encroach + delta_disaster, 1)
        projected_score = int(round(baseline_score + total_delta))
        projected_score = max(5, min(100, projected_score))

        # Projected Risk Level
        if projected_score >= 85:
            projected_risk = "Low"
            status_summary = "Healthy / Resilient Condition"
        elif projected_score >= 70:
            projected_risk = "Moderate"
            status_summary = "Moderate Vulnerability - Monitor Closely"
        elif projected_score >= 50:
            projected_risk = "High"
            status_summary = "High Risk - Targeted Conservation Required"
        else:
            projected_risk = "Critical"
            status_summary = "Critical Alert - Immediate Preservation Action Required"

        if not interventions:
            interventions.append("Maintain existing baseline monitoring, conservation schedules, and buffer security.")

        return {
            "site_id": site.id,
            "site_name": site.name,
            "provenance": "SIMULATED",
            "disclaimer": "SIMULATED SCENARIO: Preservation projection model for planning and preventative decision-support.",
            "baseline": {
                "health_score": baseline_score,
                "risk_level": baseline_risk
            },
            "projected": {
                "health_score": projected_score,
                "risk_level": projected_risk,
                "status_summary": status_summary
            },
            "score_delta": round(projected_score - baseline_score, 1),
            "risk_transition": f"{baseline_risk} \u2192 {projected_risk}",
            "factor_attribution": {
                "visitor_pressure_shift": round(delta_tourist, 1),
                "environmental_air_shift": round(delta_env, 1),
                "structural_maintenance_shift": round(delta_struct, 1),
                "buffer_encroachment_shift": round(delta_encroach, 1),
                "disaster_weather_shift": round(delta_disaster, 1)
            },
            "scenario_parameters": {
                "tourist_multiplier": tourist_mult,
                "aqi": aqi,
                "monsoon_severity": monsoon,
                "buffer_intrusion": buffer_intrusion,
                "maintenance_regime": maintenance,
                "green_buffer_expanded": green_buffer,
                "visitor_timed_entry": timed_entry
            },
            "recommended_preventative_actions": interventions
        }
