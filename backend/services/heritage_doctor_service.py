from datetime import datetime

class HeritageDoctorService:
    """
    Heritage Doctor: Diagnostic Condition Assessment & Prescription Engine.
    Provides evidence-based clinical diagnostics, pathology identification,
    and structured conservation treatment protocols for heritage monuments.
    """

    @classmethod
    def diagnose_site(cls, site) -> dict:
        from backend.services.health_score_service import HealthScoreService
        health_data = HealthScoreService.calculate_health_score(site)
        score = health_data["overall_health_score"]
        risk_level = health_data["risk_level"]
        breakdown = health_data["factor_breakdown"]

        risk_rec = site.risk_assessments[-1] if site.risk_assessments else None
        env_rec = site.environmental_records[-1] if site.environmental_records else None
        tourist_rec = site.tourist_pressures[-1] if site.tourist_pressures else None
        encroachments = site.encroachments or []
        unresolved_reports = [r for r in site.reports if r.status in ["Submitted", "Under Review", "Verified", "Action Required"]]

        # Grade Assignment
        if score >= 88:
            clinical_grade = "Grade A: Structurally Stable & Well Conserved"
            grade_badge = "GRADE_A"
            urgency = "Standard Scheduled Monitoring"
        elif score >= 75:
            clinical_grade = "Grade B: Monitored Minor Pathologies"
            grade_badge = "GRADE_B"
            urgency = "Preventative Conservation within 6 Months"
        elif score >= 55:
            clinical_grade = "Grade C: Active Deterioration & Pathological Stress"
            grade_badge = "GRADE_C"
            urgency = "Targeted Remedial Action within 60 Days"
        else:
            clinical_grade = "Grade D: Critical Structural Distress & Vulnerability"
            grade_badge = "GRADE_D"
            urgency = "Emergency Intervention Protocol Immediate"

        # Diagnostic Confidence (based on data richness)
        data_points = (1 if risk_rec else 0) + (1 if env_rec else 0) + (1 if tourist_rec else 0) + (1 if len(encroachments) > 0 else 0) + (1 if len(site.timelines) > 0 else 0)
        confidence_pct = min(96, 75 + (data_points * 4))

        # Identified Pathologies & Vulnerabilities
        pathologies = []
        if env_rec and env_rec.air_quality_aqi > 150:
            pathologies.append({
                "pathology": "Atmospheric Particulate Sulfation & Surface Crust",
                "severity": "High" if env_rec.air_quality_aqi > 250 else "Moderate",
                "organ_affected": "Exterior Sandstone/Marble Facade",
                "symptoms": f"Elevated AQI ({env_rec.air_quality_aqi} PM2.5/PM10) depositing acidic particulates and calcium sulfate reaction crusts.",
                "remedy": "Sacrificial Fuller's Earth (Multani Mitti) lime clay poulticing; wash with non-ionic deionized water spray at low bar pressure."
            })

        if env_rec and env_rec.humidity_pct > 70:
            pathologies.append({
                "pathology": "Subterranean Capillary Moisture & Biological Growth",
                "severity": "Moderate",
                "organ_affected": "Plinth Foundation & Lower Masonry",
                "symptoms": f"Ambient humidity at {env_rec.humidity_pct}%; risk of micro-algae, lichen colonization, and salt efflorescence.",
                "remedy": "Biocide treatment with quaternary ammonium compounds; sub-surface French drain restoration around monument perimeter."
            })

        if tourist_rec and tourist_rec.occupancy_ratio > 0.9:
            pathologies.append({
                "pathology": "Micro-Abrasive Friction & Internal Thermal Inversion",
                "severity": "High" if tourist_rec.occupancy_ratio > 1.2 else "Moderate",
                "organ_affected": "Flooring, Plinths, and Sanctum Interiors",
                "symptoms": f"Daily footfall ({tourist_rec.daily_visitors} visitors) nearing or exceeding carrying capacity ({site.carrying_capacity_daily}).",
                "remedy": "Install rubber-cushioned elevated wooden boardwalks; enforce timed slot entries and limit sanctum occupancy to 25 persons."
            })

        if len(encroachments) > 0:
            crit_enc = [e for e in encroachments if e.risk_level in ["Critical", "High"]]
            if crit_enc:
                pathologies.append({
                    "pathology": "Statutory Buffer Zone Encroachment & Vibration Stress",
                    "severity": "Critical",
                    "organ_affected": "100m Prohibited Buffer Zone",
                    "symptoms": f"{len(crit_enc)} unauthorized structure(s) within regulated perimeter generating vehicular vibration and visual clutter.",
                    "remedy": "Issue statutory AMASR Act 1958/2010 Section 20A compliance notice; erect demarcated perimeter heritage boundary bollards."
                })

        if len(unresolved_reports) > 0:
            pathologies.append({
                "pathology": "Unresolved Physical Damage / Vandalism Incidents",
                "severity": "Moderate" if len(unresolved_reports) < 3 else "High",
                "organ_affected": "Superficial Masonry & Public Access Areas",
                "symptoms": f"{len(unresolved_reports)} open citizen incident report(s) awaiting verification or field action.",
                "remedy": "Dispatch local ASI / State conservation team for rapid in-situ photographic documentation and lime repointing."
            })

        if not pathologies:
            pathologies.append({
                "pathology": "Baseline Atmospheric Weathering",
                "severity": "Low",
                "organ_affected": "Exterior Masonry",
                "symptoms": "Normal cyclic seasonal thermal expansion and wind abrasion within acceptable tolerance limits.",
                "remedy": "Continue routine bi-annual condition mapping, photographic monitoring, and non-destructive surface testing."
            })

        # Clinical Treatment Protocol / Prescription
        prescriptions = [
            {
                "phase": "Immediate (0 - 30 Days)",
                "action": "Complete high-resolution non-destructive 3D laser scan and ultrasonic pulse velocity structural testing on all primary load pillars.",
                "responsible": "Superintending Archaeologist & Structural Engineering Cell"
            },
            {
                "phase": "Mid-Term (1 - 6 Months)",
                "action": "Apply breathable lime-mortar pointing with slaked hydraulic lime; clear perimeter stormwater drainage conduits.",
                "responsible": "Conservation Maintenance Division"
            },
            {
                "phase": "Long-Term Policy (6 - 12 Months)",
                "action": "Implement smart carrying capacity turnstiles, integrate continuous environmental sensor nodes, and enforce buffer zone green corridors.",
                "responsible": "Heritage Authority & Municipal Urban Planning Board"
            }
        ]

        # Statutory AMASR Act Compliance Status
        amasr_status = {
            "act_name": "Ancient Monuments and Archaeological Sites and Remains Act (AMASR) 1958 & 2010",
            "prohibited_area_100m": "Strictly Monitored - Zero Commercial Construction Permitted",
            "regulated_area_300m": "Prior Permission from Competent Authority Required for any Alteration",
            "compliance_score": 92 if len(encroachments) == 0 else max(40, 92 - (len(encroachments) * 15)),
            "buffer_integrity": "Protected" if len(encroachments) == 0 else "Active Infringements Under Review"
        }

        return {
            "site_id": site.id,
            "site_name": site.name,
            "city": site.city,
            "state": site.state.name if site.state else "India",
            "clinical_grade": clinical_grade,
            "grade_badge": grade_badge,
            "overall_health_score": score,
            "risk_level": risk_level,
            "urgency_rating": urgency,
            "diagnostic_confidence_percentage": confidence_pct,
            "provenance": "DIAGNOSTIC_EXPLAINABLE",
            "factor_diagnostics": breakdown,
            "identified_pathologies": pathologies,
            "clinical_prescriptions": prescriptions,
            "statutory_compliance": amasr_status,
            "generated_at": datetime.utcnow().isoformat()
        }
