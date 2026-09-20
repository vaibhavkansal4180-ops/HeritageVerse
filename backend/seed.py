import os
import sys
from datetime import datetime, date
from pathlib import Path

# Add project root to sys.path
BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from backend.app import create_app
from backend.models import (
    db, User, State, HeritageSite, HeritageImage,
    HeritageReport, ReportImage, RiskAssessment,
    EnvironmentalData, TouristPressure, EncroachmentObservation,
    ConditionTimeline, Alert, AdminAction,
    MonumentHistoryEvent, HeritageCraft, CulturalTradition,
    HeritageTrail, TrailStop, ThenVsNow, CommunityStory, HeritageSurrounding
)

def seed_database(drop_existing=False, app=None):
    if not app:
        try:
            from flask import current_app
            if current_app:
                app = current_app._get_current_object()
        except Exception:
            pass
    if not app:
        app = create_app()

    with app.app_context():
        print("🌱 Seeding HeritageVerse Preservation Intelligence Platform Database...")
        if drop_existing:
            db.drop_all()
        db.create_all()

        # 1. Create Default Users (Admin & Citizen)
        admin = User.query.filter_by(email="admin@heritageverse.in").first()
        if not admin:
            admin = User(
                name="Chief Conservation Officer",
                email="admin@heritageverse.in",
                role="admin"
            )
            admin.set_password("Admin@123")
            db.session.add(admin)
            print("  ✔ Created Admin User: admin@heritageverse.in (Password: Admin@123)")
        else:
            admin.set_password("Admin@123")

        user = User.query.filter_by(email="user@heritageverse.in").first()
        if not user:
            user = User(
                name="Aarav Sharma (Citizen Watcher)",
                email="user@heritageverse.in",
                role="user"
            )
            user.set_password("User@123")
            db.session.add(user)
            print("  ✔ Created Demo User: user@heritageverse.in (Password: User@123)")
        else:
            user.set_password("User@123")

        db.session.commit()

        # 2. Seed States / Regions
        states_data = [
            {"name": "Rajasthan", "map_identifier": "RJ", "description": "Arid zone with major hill forts and sandstone monuments."},
            {"name": "Uttar Pradesh", "map_identifier": "UP", "description": "Gangetic alluvial basin with Mughal and ancient riverfront heritage."},
            {"name": "Maharashtra", "map_identifier": "MH", "description": "Deccan basalt plateau with monolithic cave temples and coastal forts."},
            {"name": "Delhi", "map_identifier": "DL", "description": "National capital territory with high urban density and atmospheric pollution exposure."},
            {"name": "Karnataka", "map_identifier": "KA", "description": "Granite boulder landscape and medieval imperial ruins of Vijayanagara."},
            {"name": "Tamil Nadu", "map_identifier": "TN", "description": "Coastal and river basin Dravidian granite temple architectures."},
            {"name": "Gujarat", "map_identifier": "GJ", "description": "Semi-arid and maritime zone with subterranean stepwells and Solanki shrines."},
            {"name": "Madhya Pradesh", "map_identifier": "MP", "description": "Central sandstone plateau with early Buddhist and Chandela monuments."},
            {"name": "Odisha", "map_identifier": "OR", "description": "Bay of Bengal coastal saline humidity zone with Kalinga stone temples."},
            {"name": "West Bengal", "map_identifier": "WB", "description": "Deltaic high humidity zone with colonial marble and terracotta structures."}
        ]

        state_map = {}
        for s_data in states_data:
            st = State.query.filter_by(map_identifier=s_data["map_identifier"]).first()
            if not st:
                st = State(**s_data)
                db.session.add(st)
                db.session.flush()
            state_map[s_data["map_identifier"]] = st.id
        db.session.commit()

        # 3. Verified Heritage Monuments Data with Exact, Authentic Imagery
        sites_data = [
            # 1. Konark Sun Temple (Critical / High Risk - Coastal Saline & Sand Infill Pressure)
            {
                "state_code": "OR",
                "name": "Konark Sun Temple (Black Pagoda)",
                "city": "Konark, Puri",
                "historical_period": "Eastern Ganga Dynasty (1250 CE)",
                "heritage_category": "Sacred & Temple Architecture",
                "description": "A 13th-century CE sun temple conceived as a monumental 24-wheeled chariot of Surya. Subjected to aggressive maritime salt spray, cyclones, and structural weight load on chlorite stone.",
                "cultural_significance": "UNESCO World Heritage Site and pinnacle of Kalinga architectural genius.",
                "architecture": "Kalinga deula architecture in chlorite and khondalite stone with precision astronomical chariot wheels.",
                "latitude": 19.8876,
                "longitude": 86.0945,
                "preservation_status": "Major Conservation Needed",
                "current_health_score": 48,
                "risk_level": "Critical",
                "carrying_capacity_daily": 6000,
                "image_url": "https://cdn.britannica.com/19/251919-050-D3E64798/konark-sun-temple-orissa-india-unesco-heritage-site.jpg",
                "gallery": [
                    "https://i.pinimg.com/originals/c6/4b/5e/c64b5e5284470c89b87763868614fbf9.jpg",
                    "/assets/images/heritage-placeholder.svg"
                ],
                "is_featured": True,
                "risk_profile": {
                    "structural_risk": "High", "structural_score": 52,
                    "encroachment_risk": "Moderate", "encroachment_score": 75,
                    "flood_risk": "High", "fire_risk": "Low", "earthquake_risk": "Low", "weather_risk": "Critical",
                    "disaster_score": 44, "environmental_score": 40, "tourist_pressure_score": 55, "overall_health_score": 48
                },
                "env_profile": {
                    "temperature_c": 31.2, "humidity_pct": 84.0, "rainfall_mm": 45.0,
                    "air_quality_aqi": 118, "aqi_category": "Moderate",
                    "flood_water_level_m": 0.85, "exposure_risk_status": "Critical Warning", "data_source": "LIVE_API"
                },
                "tourist_profile": {
                    "daily_visitors": 6850, "monthly_visitors": 205000, "carrying_capacity": 6000,
                    "occupancy_ratio": 1.14, "pressure_level": "Critical", "trend": "Rising"
                }
            },

            # 2. Taj Mahal (Attention Required - Air Pollution & River Yamuna Desiccation)
            {
                "state_code": "UP",
                "name": "Taj Mahal",
                "city": "Agra",
                "historical_period": "Mughal Empire (1632-1653 CE)",
                "heritage_category": "Monuments & Forts",
                "description": "White Makrana marble mausoleum of Emperor Shah Jahan and Mumtaz Mahal. Monitored for atmospheric particulate sulfur/nitrogen discoloration and Yamuna riverbed groundwater level drops.",
                "cultural_significance": "UNESCO World Heritage Site and universal masterpiece of Islamic Indo-Persian architecture.",
                "architecture": "Bilateral symmetry, central Makrana marble dome, four earthquake-canted minarets, and pietra dura gemstone inlays.",
                "latitude": 27.1751,
                "longitude": 78.0421,
                "preservation_status": "Well Preserved",
                "current_health_score": 78,
                "risk_level": "Moderate",
                "carrying_capacity_daily": 25000,
                "image_url": "https://i.pinimg.com/originals/f2/cf/71/f2cf717c1bf0c4e1a77fdd97489fae7d.jpg",
                "gallery": [
                    "https://i.pinimg.com/originals/f2/cf/71/f2cf717c1bf0c4e1a77fdd97489fae7d.jpg",
                    "/assets/images/heritage-placeholder.svg"
                ],
                "is_featured": True,
                "risk_profile": {
                    "structural_risk": "Low", "structural_score": 88,
                    "encroachment_risk": "Low", "encroachment_score": 92,
                    "flood_risk": "Moderate", "fire_risk": "Low", "earthquake_risk": "Low", "weather_risk": "Moderate",
                    "disaster_score": 82, "environmental_score": 62, "tourist_pressure_score": 68, "overall_health_score": 78
                },
                "env_profile": {
                    "temperature_c": 34.0, "humidity_pct": 58.0, "rainfall_mm": 5.0,
                    "air_quality_aqi": 185, "aqi_category": "Unhealthy",
                    "flood_water_level_m": 0.15, "exposure_risk_status": "Moderate Risk", "data_source": "LIVE_API"
                },
                "tourist_profile": {
                    "daily_visitors": 22400, "monthly_visitors": 670000, "carrying_capacity": 25000,
                    "occupancy_ratio": 0.90, "pressure_level": "High", "trend": "Rising"
                }
            },

            # 3. Hampi Monuments & Stone Chariot (High Risk - Micro-Fissures & Urban Encroachment)
            {
                "state_code": "KA",
                "name": "Hampi Monuments & Stone Chariot",
                "city": "Hampi",
                "historical_period": "Vijayanagara Empire (14th-16th Century)",
                "heritage_category": "Archaeological Excavations",
                "description": "Vast medieval capital ruins spanning 4,100 hectares along the Tungabhadra River. Vulnerable to structural granite exfoliation, commercial tourist stalls near core temples, and flash flood overflow.",
                "cultural_significance": "UNESCO World Heritage Site representing the zenith of South Indian imperial architecture.",
                "architecture": "Carved monolithic granite pillared halls (Maha Mandapas), Garuda stone chariot, and stepped tanks.",
                "latitude": 15.3350,
                "longitude": 76.4600,
                "preservation_status": "Minor Restoration Required",
                "current_health_score": 66,
                "risk_level": "High",
                "carrying_capacity_daily": 8000,
                "image_url": "https://th.bing.com/th/id/R.f10a6bbde9457a12ea4732f440cdd197?rik=M9AwgeYYzuyLsg&riu=http%3a%2f%2fwww.thehistoryhub.com%2fwp-content%2fuploads%2f2014%2f04%2fHampi-Chariot.jpg&ehk=MX5BNohAmJnqbpQiCNi9qn%2fg%2fGeP4wF7LIiyhuF5Ixo%3d&risl=&pid=ImgRaw&r=0",
                "gallery": [
                    "https://images.fineartamerica.com/images-medium-large/stone-chariot-at-vittala-temple-complex-in-hampi-india-rohit-chowdhry.jpg",
                    "/assets/images/heritage-placeholder.svg"
                ],
                "is_featured": True,
                "risk_profile": {
                    "structural_risk": "Moderate", "structural_score": 70,
                    "encroachment_risk": "High", "encroachment_score": 60,
                    "flood_risk": "High", "fire_risk": "Low", "earthquake_risk": "Low", "weather_risk": "Moderate",
                    "disaster_score": 65, "environmental_score": 75, "tourist_pressure_score": 60, "overall_health_score": 66
                },
                "env_profile": {
                    "temperature_c": 29.5, "humidity_pct": 62.0, "rainfall_mm": 28.0,
                    "air_quality_aqi": 68, "aqi_category": "Good",
                    "flood_water_level_m": 0.65, "exposure_risk_status": "High Risk", "data_source": "DEMO_DATA"
                },
                "tourist_profile": {
                    "daily_visitors": 6200, "monthly_visitors": 186000, "carrying_capacity": 8000,
                    "occupancy_ratio": 0.78, "pressure_level": "Moderate", "trend": "Stable"
                }
            },

            # 4. Qutub Minar & Complex (Healthy / Stable - Well Protected)
            {
                "state_code": "DL",
                "name": "Qutub Minar & Complex",
                "city": "New Delhi",
                "historical_period": "Delhi Sultanate (1192-1220 CE)",
                "heritage_category": "Monuments & Forts",
                "description": "72.5-meter tall fluted red sandstone minaret with the 4th-century Gupta Iron Pillar. Continuous structural tilt sensor telemetry and laser cleaning protocol active.",
                "cultural_significance": "UNESCO World Heritage Site marking the advent of Indo-Islamic architectural engineering.",
                "architecture": "Five tapering storeys with stalactite balcony brackets and Quranic calligraphic friezes.",
                "latitude": 28.5245,
                "longitude": 77.1855,
                "preservation_status": "Well Preserved",
                "current_health_score": 88,
                "risk_level": "Low",
                "carrying_capacity_daily": 15000,
                "image_url": "https://tse2.mm.bing.net/th/id/OIP.e_hkBJNBPV7gUsACS3zv1wHaE8?r=0&rs=1&pid=ImgDetMain&o=7&rm=3",
                "gallery": [
                    "https://tse4.mm.bing.net/th/id/OIP.cPQTcppTspgFv0kPzzAT3wHaFk?r=0&rs=1&pid=ImgDetMain&o=7&rm=3",
                    "/assets/images/heritage-placeholder.svg"
                ],
                "is_featured": True,
                "risk_profile": {
                    "structural_risk": "Low", "structural_score": 92,
                    "encroachment_risk": "Low", "encroachment_score": 95,
                    "flood_risk": "Low", "fire_risk": "Low", "earthquake_risk": "Moderate", "weather_risk": "Moderate",
                    "disaster_score": 85, "environmental_score": 72, "tourist_pressure_score": 88, "overall_health_score": 88
                },
                "env_profile": {
                    "temperature_c": 32.5, "humidity_pct": 48.0, "rainfall_mm": 0.0,
                    "air_quality_aqi": 165, "aqi_category": "Unhealthy",
                    "flood_water_level_m": 0.0, "exposure_risk_status": "Normal", "data_source": "LIVE_API"
                },
                "tourist_profile": {
                    "daily_visitors": 9200, "monthly_visitors": 276000, "carrying_capacity": 15000,
                    "occupancy_ratio": 0.61, "pressure_level": "Moderate", "trend": "Stable"
                }
            },

            # 5. Amber Fort & Palace (Healthy - Active Conservation Protocol)
            {
                "state_code": "RJ",
                "name": "Amber Fort & Palace",
                "city": "Jaipur",
                "historical_period": "Rajput (16th-18th Century)",
                "heritage_category": "Monuments & Forts",
                "description": "Hill fort overlooking Maota Lake with marble courtyards and Sheesh Mahal mirror mosaics. Monitored for surface water runoff along outer fortification bastions.",
                "cultural_significance": "UNESCO World Heritage Site under 'Hill Forts of Rajasthan'.",
                "architecture": "Terraced courtyards, scalloped arches, frescoed pavilions, and lattice jali windows.",
                "latitude": 26.9855,
                "longitude": 75.8513,
                "preservation_status": "Well Preserved",
                "current_health_score": 84,
                "risk_level": "Low",
                "carrying_capacity_daily": 10000,
                "image_url": "https://tse2.mm.bing.net/th/id/OIP.JRwu95b6i6VIMXXB4aOEKAHaD4?r=0&rs=1&pid=ImgDetMain&o=7&rm=3",
                "gallery": [
                    "https://tse2.mm.bing.net/th/id/OIP.JRwu95b6i6VIMXXB4aOEKAHaD4?r=0&rs=1&pid=ImgDetMain&o=7&rm=3",
                    "/assets/images/heritage-placeholder.svg"
                ],
                "is_featured": True,
                "risk_profile": {
                    "structural_risk": "Low", "structural_score": 88,
                    "encroachment_risk": "Low", "encroachment_score": 86,
                    "flood_risk": "Low", "fire_risk": "Low", "earthquake_risk": "Low", "weather_risk": "Moderate",
                    "disaster_score": 86, "environmental_score": 80, "tourist_pressure_score": 75, "overall_health_score": 84
                },
                "env_profile": {
                    "temperature_c": 35.0, "humidity_pct": 42.0, "rainfall_mm": 0.0,
                    "air_quality_aqi": 110, "aqi_category": "Moderate",
                    "flood_water_level_m": 0.1, "exposure_risk_status": "Normal", "data_source": "DEMO_DATA"
                },
                "tourist_profile": {
                    "daily_visitors": 6800, "monthly_visitors": 204000, "carrying_capacity": 10000,
                    "occupancy_ratio": 0.68, "pressure_level": "Moderate", "trend": "Rising"
                }
            },

            # 6. Ajanta Caves (High Risk - Humidity & Microbial Infestation on Ancient Murals)
            {
                "state_code": "MH",
                "name": "Ajanta Caves",
                "city": "Aurangabad",
                "historical_period": "Satavahana & Vakataka (2nd BCE - 5th CE)",
                "heritage_category": "Cave & Rock-Cut Shrines",
                "description": "30 rock-cut Buddhist cave monuments with tempera wall paintings. Highly sensitive to micro-climate fluctuations, carbon dioxide accumulation from visitor respiration, and water seepage.",
                "cultural_significance": "UNESCO World Heritage Site preserving ancient Indian classical paintings.",
                "architecture": "Chaitya prayer halls with stupa apses, octagonal columns, and fresco murals on mud-plastered basalt.",
                "latitude": 20.5519,
                "longitude": 75.7033,
                "preservation_status": "Under Active Restoration",
                "current_health_score": 58,
                "risk_level": "High",
                "carrying_capacity_daily": 3500,
                "image_url": "https://www.easeindiatrip.com/blog/wp-content/uploads/2025/03/Maharashtra-Aurangabad-Ajanta-Caves-02.jpg",
                "gallery": [
                    "https://www.easeindiatrip.com/blog/wp-content/uploads/2025/03/Maharashtra-Aurangabad-Ajanta-Caves-02.jpg",
                    "/assets/images/heritage-placeholder.svg"
                ],
                "is_featured": False,
                "risk_profile": {
                    "structural_risk": "Moderate", "structural_score": 65,
                    "encroachment_risk": "Low", "encroachment_score": 90,
                    "flood_risk": "Moderate", "fire_risk": "Low", "earthquake_risk": "Low", "weather_risk": "High",
                    "disaster_score": 62, "environmental_score": 45, "tourist_pressure_score": 50, "overall_health_score": 58
                },
                "env_profile": {
                    "temperature_c": 27.8, "humidity_pct": 78.5, "rainfall_mm": 35.0,
                    "air_quality_aqi": 52, "aqi_category": "Good",
                    "flood_water_level_m": 0.4, "exposure_risk_status": "High Risk", "data_source": "LIVE_API"
                },
                "tourist_profile": {
                    "daily_visitors": 3350, "monthly_visitors": 100500, "carrying_capacity": 3500,
                    "occupancy_ratio": 0.96, "pressure_level": "High", "trend": "Rising"
                }
            },

            # 7. Brihadisvara Temple (Healthy - Massive Granite Stability)
            {
                "state_code": "TN",
                "name": "Brihadisvara Temple (Big Temple)",
                "city": "Thanjavur",
                "historical_period": "Chola Dynasty (1010 CE)",
                "heritage_category": "Sacred & Temple Architecture",
                "description": "66-meter high granite vimana crowned by an 80-tonne monolithic cupola. Engineered with interlocking dry-stone masonry with exceptional seismic resilience.",
                "cultural_significance": "UNESCO World Heritage Site under 'Great Living Chola Temples'.",
                "architecture": "Pure Dravidian granite architecture, 16-storey pyramidal vimana, and 108 Nataraja dance poses.",
                "latitude": 10.7828,
                "longitude": 79.1318,
                "preservation_status": "Well Preserved",
                "current_health_score": 91,
                "risk_level": "Low",
                "carrying_capacity_daily": 12000,
                "image_url": "https://mir-s3-cdn-cf.behance.net/project_modules/2800_opt_1/78f3ef58411245.59fb28367b6f4.jpg",
                "gallery": [
                    "https://mir-s3-cdn-cf.behance.net/project_modules/2800_opt_1/78f3ef58411245.59fb28367b6f4.jpg",
                    "/assets/images/heritage-placeholder.svg"
                ],
                "is_featured": True,
                "risk_profile": {
                    "structural_risk": "Low", "structural_score": 95,
                    "encroachment_risk": "Low", "encroachment_score": 90,
                    "flood_risk": "Low", "fire_risk": "Low", "earthquake_risk": "Low", "weather_risk": "Low",
                    "disaster_score": 90, "environmental_score": 85, "tourist_pressure_score": 88, "overall_health_score": 91
                },
                "env_profile": {
                    "temperature_c": 32.0, "humidity_pct": 65.0, "rainfall_mm": 8.0,
                    "air_quality_aqi": 62, "aqi_category": "Good",
                    "flood_water_level_m": 0.05, "exposure_risk_status": "Normal", "data_source": "DEMO_DATA"
                },
                "tourist_profile": {
                    "daily_visitors": 7100, "monthly_visitors": 213000, "carrying_capacity": 12000,
                    "occupancy_ratio": 0.59, "pressure_level": "Moderate", "trend": "Stable"
                }
            },

            # 8. Terracotta Temples of Bishnupur (Critical - Clay Weathering & Bio-Growth)
            {
                "state_code": "WB",
                "name": "Terracotta Temples of Bishnupur",
                "city": "Bishnupur",
                "historical_period": "Malla Dynasty (17th-18th Century CE)",
                "heritage_category": "Sacred & Temple Architecture",
                "description": "Burnt red terracotta brick temples with curved chala roofs. Highly vulnerable to monsoon rain erosion, fungal bio-film colonization, and mortar disintegration.",
                "cultural_significance": "Pinnacle of indigenous Bengal terracotta brick architecture.",
                "architecture": "Chala, Ratna, and Du-chala brick structures covered in carved mythological terracotta relief plaques.",
                "latitude": 23.0760,
                "longitude": 87.3200,
                "preservation_status": "Major Conservation Needed",
                "current_health_score": 44,
                "risk_level": "Critical",
                "carrying_capacity_daily": 2500,
                "image_url": "https://images.unsplash.com/photo-1590050752117-238cb0fb12b1?auto=format&fit=crop&w=1200&q=80",
                "gallery": [
                    "https://images.unsplash.com/photo-1590050752117-238cb0fb12b1?auto=format&fit=crop&w=1200&q=80",
                    "/assets/images/heritage-placeholder.svg",
                    "/assets/images/heritage-placeholder.svg"
                ],
                "is_featured": False,
                "risk_profile": {
                    "structural_risk": "Critical", "structural_score": 42,
                    "encroachment_risk": "Moderate", "encroachment_score": 68,
                    "flood_risk": "High", "fire_risk": "Low", "earthquake_risk": "Low", "weather_risk": "Critical",
                    "disaster_score": 48, "environmental_score": 38, "tourist_pressure_score": 70, "overall_health_score": 44
                },
                "env_profile": {
                    "temperature_c": 30.5, "humidity_pct": 89.0, "rainfall_mm": 58.0,
                    "air_quality_aqi": 78, "aqi_category": "Moderate",
                    "flood_water_level_m": 0.72, "exposure_risk_status": "Critical Warning", "data_source": "LIVE_API"
                },
                "tourist_profile": {
                    "daily_visitors": 1800, "monthly_visitors": 54000, "carrying_capacity": 2500,
                    "occupancy_ratio": 0.72, "pressure_level": "Moderate", "trend": "Stable"
                }
            }
        ]

        site_objects = {}
        for s_info in sites_data:
            site = HeritageSite.query.filter_by(name=s_info["name"]).first()
            if not site:
                site = HeritageSite(
                    state_id=state_map[s_info["state_code"]],
                    name=s_info["name"],
                    city=s_info["city"],
                    historical_period=s_info["historical_period"],
                    heritage_category=s_info.get("heritage_category", "Monuments & Forts"),
                    description=s_info["description"],
                    cultural_significance=s_info["cultural_significance"],
                    architecture=s_info["architecture"],
                    latitude=s_info["latitude"],
                    longitude=s_info["longitude"],
                    preservation_status=s_info["preservation_status"],
                    current_health_score=s_info["current_health_score"],
                    risk_level=s_info["risk_level"],
                    carrying_capacity_daily=s_info.get("carrying_capacity_daily", 5000),
                    image_url=s_info["image_url"],
                    is_featured=s_info.get("is_featured", False)
                )
                db.session.add(site)
                db.session.flush()
            else:
                # Update existing site with verified image and details
                site.image_url = s_info["image_url"]
                site.current_health_score = s_info["current_health_score"]
                site.risk_level = s_info["risk_level"]
                site.preservation_status = s_info["preservation_status"]
                site.heritage_category = s_info.get("heritage_category", "Monuments & Forts")
                site.description = s_info["description"]
                db.session.flush()

            # Refresh Gallery images
            HeritageImage.query.filter_by(heritage_site_id=site.id).delete()
            for idx, g in enumerate(s_info.get("gallery", [s_info["image_url"]])):
                db.session.add(HeritageImage(
                    heritage_site_id=site.id,
                    image_url=g,
                    caption=f"{site.name} preservation survey documentation ({idx+1})",
                    is_primary=(idx == 0)
                ))

            # Multi-Hazard Risk Assessment
            RiskAssessment.query.filter_by(heritage_site_id=site.id).delete()
            rp = s_info.get("risk_profile", {})
            risk_obj = RiskAssessment(
                heritage_site_id=site.id,
                structural_risk=rp.get("structural_risk", "Low"),
                structural_score=rp.get("structural_score", 85),
                encroachment_risk=rp.get("encroachment_risk", "Low"),
                encroachment_score=rp.get("encroachment_score", 90),
                flood_risk=rp.get("flood_risk", "Low"),
                fire_risk=rp.get("fire_risk", "Low"),
                earthquake_risk=rp.get("earthquake_risk", "Low"),
                weather_risk=rp.get("weather_risk", "Low"),
                disaster_score=rp.get("disaster_score", 85),
                environmental_score=rp.get("environmental_score", 85),
                tourist_pressure_score=rp.get("tourist_pressure_score", 80),
                overall_health_score=s_info["current_health_score"],
                assessed_by="National Preservation Intelligence Engine"
            )
            db.session.add(risk_obj)

            # Environmental Telemetry Record
            EnvironmentalData.query.filter_by(heritage_site_id=site.id).delete()
            ep = s_info.get("env_profile", {})
            env_obj = EnvironmentalData(
                heritage_site_id=site.id,
                temperature_c=ep.get("temperature_c", 28.0),
                humidity_pct=ep.get("humidity_pct", 55.0),
                rainfall_mm=ep.get("rainfall_mm", 10.0),
                air_quality_aqi=ep.get("air_quality_aqi", 95),
                aqi_category=ep.get("aqi_category", "Moderate"),
                flood_water_level_m=ep.get("flood_water_level_m", 0.1),
                exposure_risk_status=ep.get("exposure_risk_status", "Normal"),
                data_source=ep.get("data_source", "DEMO_DATA")
            )
            db.session.add(env_obj)

            # Tourist Pressure Record
            TouristPressure.query.filter_by(heritage_site_id=site.id).delete()
            tp = s_info.get("tourist_profile", {})
            tourist_obj = TouristPressure(
                heritage_site_id=site.id,
                daily_visitors=tp.get("daily_visitors", 3000),
                monthly_visitors=tp.get("monthly_visitors", 90000),
                carrying_capacity=tp.get("carrying_capacity", 5000),
                occupancy_ratio=tp.get("occupancy_ratio", 0.6),
                pressure_level=tp.get("pressure_level", "Moderate"),
                trend=tp.get("trend", "Stable")
            )
            db.session.add(tourist_obj)

            print(f"  ✔ Configured Monitored Site: {site.name} (Health Score: {site.current_health_score}/100, Risk: {site.risk_level})")
            site_objects[s_info["name"]] = site

        db.session.commit()

        # 4. Seed Encroachment Observations for Buffer Zones with Verified Imagery
        konark = site_objects.get("Konark Sun Temple (Black Pagoda)")
        hampi = site_objects.get("Hampi Monuments & Stone Chariot")
        taj = site_objects.get("Taj Mahal")

        if konark:
            EncroachmentObservation.query.filter_by(heritage_site_id=konark.id).delete()
            db.session.add(EncroachmentObservation(
                heritage_site_id=konark.id,
                monitored_zone="100m Prohibited Buffer Zone (South-East Coast Perimeter)",
                baseline_image_url="https://cdn.britannica.com/19/251919-050-D3E64798/konark-sun-temple-orissa-india-unesco-heritage-site.jpg",
                baseline_date=date(2023, 4, 15),
                latest_image_url="https://i.pinimg.com/originals/c6/4b/5e/c64b5e5284470c89b87763868614fbf9.jpg",
                latest_date=date(2026, 8, 20),
                detected_change="Unauthorized commercial parking structure and concrete perimeter wall within 65m of outer boundary.",
                change_area_sqm=380.0,
                risk_level="Critical",
                confidence_pct=94,
                verified_by_admin=True
            ))

        if hampi:
            EncroachmentObservation.query.filter_by(heritage_site_id=hampi.id).delete()
            db.session.add(EncroachmentObservation(
                heritage_site_id=hampi.id,
                monitored_zone="300m Regulated Zone (Vittala Bazaar North Axis)",
                baseline_image_url="https://th.bing.com/th/id/R.f10a6bbde9457a12ea4732f440cdd197?rik=M9AwgeYYzuyLsg&riu=http%3a%2f%2fwww.thehistoryhub.com%2fwp-content%2fuploads%2f2014%2f04%2fHampi-Chariot.jpg&ehk=MX5BNohAmJnqbpQiCNi9qn%2fg%2fGeP4wF7LIiyhuF5Ixo%3d&risl=&pid=ImgRaw&r=0",
                baseline_date=date(2024, 1, 10),
                latest_image_url="https://images.fineartamerica.com/images-medium-large/stone-chariot-at-vittala-temple-complex-in-hampi-india-rohit-chowdhry.jpg",
                latest_date=date(2026, 8, 25),
                detected_change="Temporary guest house expansion and unauthorized tin shed stalls in agricultural buffer strip.",
                change_area_sqm=195.0,
                risk_level="High",
                confidence_pct=89,
                verified_by_admin=False
            ))

        # 5. Seed Multi-Year Historical Condition Timelines (2022 - 2026)
        if konark:
            ConditionTimeline.query.filter_by(heritage_site_id=konark.id).delete()
            db.session.add_all([
                ConditionTimeline(
                    heritage_site_id=konark.id, year=2022, period_label="2022 Annual Audit",
                    condition_status="Attention Required", health_score=72,
                    event_type="Restoration Completed",
                    summary="Chemical wash and silicone water repellent treatment on south-east chariot wheels.",
                    action_taken="Paper pulp desalinization applied to 4 wheels."
                ),
                ConditionTimeline(
                    heritage_site_id=konark.id, year=2024, period_label="2024 Q3 Monsoon",
                    condition_status="High Risk", health_score=59,
                    event_type="Environmental Alert",
                    summary="Cyclone Dana storm surge caused sand erosion and plinth waterlogging for 72 hours.",
                    action_taken="Emergency submersible pumping and temporary geotextile barriers installed."
                ),
                ConditionTimeline(
                    heritage_site_id=konark.id, year=2026, period_label="2026 Q3 Survey",
                    condition_status="Critical", health_score=48,
                    event_type="Damage Verified",
                    summary="Structural load-bearing micro-fractures detected on jagamohana roof core stones.",
                    action_taken="High-priority structural stabilization notice issued to ASI circle."
                )
            ])

        # 6. Seed Early Warning Alerts
        if konark:
            Alert.query.filter_by(heritage_site_id=konark.id).delete()
            db.session.add(Alert(
                alert_uid="ALT-2026-KNR001",
                heritage_site_id=konark.id,
                alert_type="Structural Alert",
                priority="CRITICAL",
                title="Severe Plinth Load Strain & High Saline Humidity",
                description="Compound threat: Humidity over 84% combined with severe micro-cracking on Southern Chariot Wheel No. 6 plinth.",
                trigger_reason="Health score fell below 50 (current 48/100) + Marine exposure risk warning.",
                recommended_action="Deploy ultrasonic structural tomography team and enforce immediate visitor buffer cordon.",
                status="Active"
            ))

        if hampi:
            Alert.query.filter_by(heritage_site_id=hampi.id).delete()
            db.session.add(Alert(
                alert_uid="ALT-2026-HMP002",
                heritage_site_id=hampi.id,
                alert_type="Encroachment Alert",
                priority="HIGH",
                title="Protected 300m Zone Boundary Expansion Detected",
                description="Drone change detection flagged 195 sqm unauthorized construction in Vittala Temple north corridor.",
                trigger_reason="Encroachment risk score elevated above threshold with 89% AI confidence.",
                recommended_action="Dispatch revenue enforcement team to issue statutory eviction and restoration order.",
                status="Acknowledged",
                assigned_to="District Heritage Officer Ballari",
                action_notes="Notice drafted and scheduled for on-site delivery on Monday."
            ))

        if taj:
            Alert.query.filter_by(heritage_site_id=taj.id).delete()
            db.session.add(Alert(
                alert_uid="ALT-2026-TAJ003",
                heritage_site_id=taj.id,
                alert_type="Environmental Warning",
                priority="MODERATE",
                title="Sustained Air Quality Inversion (AQI 185)",
                description="Particulate matter PM2.5 elevation in Agra industrial corridor may accelerate marble surface yellowing.",
                trigger_reason="AQI exceeded 150 threshold for 4 consecutive monitoring cycles.",
                recommended_action="Schedule routine mudpack (Multani mitti) surface treatment for western minaret.",
                status="Assigned",
                assigned_to="Agra ASI Chemical Branch",
                action_notes="Treatment schedule aligned with upcoming low-footfall window."
            ))

        # 7. Seed Citizen Heritage Watch Reports with AI Preliminary Findings
        if konark and not HeritageReport.query.filter_by(heritage_site_id=konark.id).first():
            db.session.add(HeritageReport(
                report_uid="HV-2026-7A1B2C",
                user_id=user.id,
                heritage_site_id=konark.id,
                issue_type="Structural Damage",
                description="Noticed active salt crusting and stone flaking along the lower rim of the southern sundial chariot wheel.",
                incident_date=date(2026, 8, 28),
                location="Southern Chariot Wheel No. 6 base plinth",
                severity="Critical",
                status="Verified",
                admin_remarks="Archaeological chemist confirmed active marine salt decay; paper pulp poultice approved.",
                ai_category_detected="Structural Damage",
                ai_severity_estimated="Critical",
                ai_confidence_score=92,
                ai_damage_signs="Severe salt efflorescence • Stone matrix flaking • Plinth hairline fissures",
                ai_urgency="Immediate Structural Engineering Inspection (within 24 hours)"
            ))

        if hampi and not HeritageReport.query.filter_by(heritage_site_id=hampi.id).first():
            db.session.add(HeritageReport(
                report_uid="HV-2026-9E4F1A",
                user_id=user.id,
                heritage_site_id=hampi.id,
                issue_type="Encroachment",
                description="Unauthorized tin shed commercial tea stall constructed right against the ancient boundary wall.",
                incident_date=date(2026, 8, 30),
                location="Vittala Temple outer east gateway approach",
                severity="High",
                status="Action Required",
                admin_remarks="Enforcement officer dispatched with removal order.",
                ai_category_detected="Encroachment",
                ai_severity_estimated="High",
                ai_confidence_score=91,
                ai_damage_signs="Direct physical attachment to ancient granite wall • Unauthorized commercial footprint",
                ai_urgency="Encroachment Verification & Notice Dispatch Recommended"
            ))

        if taj and not HeritageReport.query.filter_by(heritage_site_id=taj.id).first():
            db.session.add(HeritageReport(
                report_uid="HV-2026-3C8D9E",
                user_id=user.id,
                heritage_site_id=taj.id,
                issue_type="Vandalism",
                description="Found faint ink markings and scratched initial carvings on red sandstone gateway pillar.",
                incident_date=date(2026, 9, 1),
                location="Western Royal Gate pillar No. 4",
                severity="Moderate",
                status="Under Review",
                admin_remarks="Security footage under review and non-abrasive surface cleaning queued.",
                ai_category_detected="Vandalism",
                ai_severity_estimated="Moderate",
                ai_confidence_score=95,
                ai_damage_signs="Direct anthropogenic chemical pigment on ancient stone surface",
                ai_urgency="Conservation Poultice Treatment & Security Review"
            ))

        # 8. Seed Chronological History Events for All 8 Monuments
        history_events_data = [
            # Konark Sun Temple
            {"site_name": "Konark Sun Temple (Black Pagoda)", "year": 1250, "year_display": "1250 CE", "title": "Construction by King Narasimhadeva I", "description": "King Narasimhadeva I of the Eastern Ganga Dynasty commissions the grand Sun Temple chariot, employing 1,200 master sculptors led by Bisu Maharana over 12 years.", "category": "Construction", "source_name": "Madala Panji & ASI Records", "source_type": "OFFICIAL"},
            {"site_name": "Konark Sun Temple (Black Pagoda)", "year": 1568, "year_display": "1568 CE", "title": "Kalapahad Military Incursion & Abandonment", "description": "General Kalapahad invades Odisha; the temple complex sustains damage and the main sanctum (rekha deula) collapses, leading to temple desanctification.", "category": "Historical Event", "source_name": "Odisha State Archives", "source_type": "ACADEMIC"},
            {"site_name": "Konark Sun Temple (Black Pagoda)", "year": 1901, "year_display": "1901 CE", "title": "Lord Curzon Structural Stabilization & Sand Infill", "description": "Lieutenant Governor Sir John Woodburn and Lord Curzon order the Jagamohana assembly hall to be filled with sand and stones to prevent total collapse.", "category": "Restoration", "source_name": "British Archaeological Survey Records", "source_type": "OFFICIAL"},
            {"site_name": "Konark Sun Temple (Black Pagoda)", "year": 1984, "year_display": "1984 CE", "title": "UNESCO World Heritage Inscription", "description": "Inscribed as a UNESCO World Heritage Site under criteria (i), (iii), and (vi) for outstanding universal value in Kalinga architectural design.", "category": "Modern Status", "source_name": "UNESCO World Heritage Centre", "source_type": "OFFICIAL"},
            {"site_name": "Konark Sun Temple (Black Pagoda)", "year": 2026, "year_display": "2026 CE Present", "title": "Continuous Sensor Telemetry & Sand Evacuation Feasibility", "description": "ASI deploys endoscope camera arrays and subterranean drainage telemetry to assess stability during safe internal sand clearing.", "category": "Conservation", "source_name": "HeritageVerse Active Monitoring Cell", "source_type": "CURATED"},

            # Taj Mahal
            {"site_name": "Taj Mahal", "year": 1631, "year_display": "1631 CE", "title": "Imperial Commission by Shah Jahan", "description": "Emperor Shah Jahan commissions the mausoleum along the Yamuna River following the demise of Empress Mumtaz Mahal during childbirth in Burhanpur.", "category": "Construction", "source_name": "Badshahnama & Imperial Court Records", "source_type": "OFFICIAL"},
            {"site_name": "Taj Mahal", "year": 1648, "year_display": "1648 CE", "title": "Completion of Central Marble Mausoleum", "description": "Master architect Ustad Ahmad Lahori and gemstone inlayer Chiranjilal complete the central white Makrana marble dome and inner octagonal cenotaph chamber.", "category": "Architectural Change", "source_name": "UNESCO Dossier & Royal Mughal Chronicles", "source_type": "ACADEMIC"},
            {"site_name": "Taj Mahal", "year": 1983, "year_display": "1983 CE", "title": "UNESCO World Heritage Recognition", "description": "Designated a World Heritage Site as the 'jewel of Muslim art in India and one of the universally admired masterpieces of the world's heritage.'", "category": "Modern Status", "source_name": "UNESCO Archives", "source_type": "OFFICIAL"},
            {"site_name": "Taj Mahal", "year": 1996, "year_display": "1996 CE", "title": "Supreme Court Taj Trapezium Zone (TTZ) Directive", "description": "Historic environmental judgment establishes 10,400 sq km TTZ buffer to ban polluting coal-based industries and switch to natural gas.", "category": "Conservation", "source_name": "Supreme Court of India (M.C. Mehta Case)", "source_type": "OFFICIAL"},
            {"site_name": "Taj Mahal", "year": 2026, "year_display": "2026 CE Present", "title": "Bio-Poulticing (Multani Mitti) & Yamuna Aquifer Care", "description": "Application of non-abrasive herbal clay packs to absorb atmospheric carbon deposits while monitoring low-level subterranean teak foundations.", "category": "Conservation", "source_name": "ASI Agra Chemical Division", "source_type": "CURATED"},

            # Hampi Monuments
            {"site_name": "Hampi Monuments & Stone Chariot", "year": 1336, "year_display": "1336 CE", "title": "Founding of Vijayanagara Empire", "description": "Brothers Harihara I and Bukka Raya I establish the Vijayanagara Empire on the south bank of Tungabhadra river, turning Kishkindha into an imperial metropolis.", "category": "Historical Event", "source_name": "Karnataka Epigraphia & Inscriptional Records", "source_type": "OFFICIAL"},
            {"site_name": "Hampi Monuments & Stone Chariot", "year": 1513, "year_display": "1513 CE", "title": "Krishnadevaraya's Vittala & Hazara Rama Enhancements", "description": "Emperor Krishnadevaraya dedicates the Garuda Stone Chariot and grand musical pillared halls celebrating his victory over Gajapatis of Odisha.", "category": "Construction", "source_name": "Vijayanagara Dynastic Chronicles", "source_type": "ACADEMIC"},
            {"site_name": "Hampi Monuments & Stone Chariot", "year": 1565, "year_display": "1565 CE", "title": "Battle of Talikota & Abandonment", "description": "Deccan Sultanates defeat Rama Raya; the city is sacked and burnt over five months, leaving behind the evocative granite ruins.", "category": "Historical Event", "source_name": "Ferishta Historical Accounts", "source_type": "ACADEMIC"},
            {"site_name": "Hampi Monuments & Stone Chariot", "year": 1986, "year_display": "1986 CE", "title": "UNESCO World Heritage Listing", "description": "Group of Monuments at Hampi inscribed as a World Heritage site spanning 4,100 hectares of living sacred and military architecture.", "category": "Modern Status", "source_name": "UNESCO World Heritage Centre", "source_type": "OFFICIAL"},

            # Qutub Minar
            {"site_name": "Qutub Minar & Complex", "year": 1199, "year_display": "1199 CE", "title": "Foundation Laid by Qutb-ud-din Aibak", "description": "Construction commences on the victory tower and the adjacent Quwwat-ul-Islam Mosque incorporating 27 reused sandstone temple colonnades.", "category": "Construction", "source_name": "Archaeological Survey of India Memoir", "source_type": "OFFICIAL"},
            {"site_name": "Qutub Minar & Complex", "year": 1368, "year_display": "1368 CE", "title": "Firuz Shah Tughlaq Lightning Repair & Marble Storeys", "description": "Lightning strikes the minaret top; Sultan Firuz Shah Tughlaq repairs the structure, replacing the fourth storey and adding a fifth storey faced in white marble.", "category": "Restoration", "source_name": "Tarikh-i-Firuz Shahi", "source_type": "ACADEMIC"},
            {"site_name": "Qutub Minar & Complex", "year": 1993, "year_display": "1993 CE", "title": "UNESCO World Heritage Status", "description": "Inscribed as UNESCO World Heritage monument alongside the 4th-century rust-resistant Gupta Iron Pillar and Alai Darwaza.", "category": "Modern Status", "source_name": "UNESCO Archives", "source_type": "OFFICIAL"},

            # Amber Fort
            {"site_name": "Amber Fort & Palace", "year": 1592, "year_display": "1592 CE", "title": "Raja Man Singh I Palace Foundation", "description": "Raja Man Singh I of the Kachwaha Rajput clan builds the red sandstone and marble fortress palace overlooking Maota Lake.", "category": "Construction", "source_name": "Jaipur State Archives & Pothi Khana", "source_type": "OFFICIAL"},
            {"site_name": "Amber Fort & Palace", "year": 1727, "year_display": "1727 CE", "title": "Sawai Jai Singh II Expands Sheesh Mahal & Shifts Capital", "description": "Mirza Raja Jai Singh builds the Sheesh Mahal (Hall of Mirrors) and Jai Mandir before Sawai Jai Singh II founds Jaipur down in the plains.", "category": "Architectural Change", "source_name": "Amber Royal Chronicles", "source_type": "ACADEMIC"},
            {"site_name": "Amber Fort & Palace", "year": 2013, "year_display": "2013 CE", "title": "UNESCO Inscription as Hill Forts of Rajasthan", "description": "Amber Fort is inscribed as UNESCO World Heritage Site along with Chittorgarh, Kumbhalgarh, Gagron, Ranthambore, and Jaisalmer.", "category": "Modern Status", "source_name": "UNESCO World Heritage Centre", "source_type": "OFFICIAL"},

            # Ajanta Caves
            {"site_name": "Ajanta Caves", "year": -200, "year_display": "2nd Century BCE", "title": "First Hinayana Monastic Excavations", "description": "Early Buddhist monks carve Cave 9, 10, 12, 13, and 15A into the horseshoe gorge of the Waghur River under Satavahana patronage.", "category": "Construction", "source_name": "Archaeological Survey of India Cave Reports", "source_type": "OFFICIAL"},
            {"site_name": "Ajanta Caves", "year": 475, "year_display": "5th Century CE", "title": "Mahayana Painting Renaissance under Harisena", "description": "King Harisena of Vakataka Empire sponsors exquisite tempera murals depicting Jataka tales, Bodhisattva Padmapani, and celestial courts.", "category": "Cultural Event", "source_name": "Walter Spink Chronology Studies", "source_type": "ACADEMIC"},
            {"site_name": "Ajanta Caves", "year": 1819, "year_display": "1819 CE", "title": "Captain John Smith Accidental Rediscovery", "description": "British cavalry officer John Smith spots Cave 10 while hunting tigers in the Waghur gorge, bringing Ajanta back to world attention.", "category": "Historical Event", "source_name": "Royal Asiatic Society Proceedings", "source_type": "ACADEMIC"},
            {"site_name": "Ajanta Caves", "year": 1983, "year_display": "1983 CE", "title": "UNESCO World Heritage Inscription", "description": "Recognized as masterpieces of Buddhist religious art and foundation of Indian classical painting tradition.", "category": "Modern Status", "source_name": "UNESCO World Heritage Centre", "source_type": "OFFICIAL"},

            # Brihadisvara Temple
            {"site_name": "Brihadisvara Temple (Big Temple)", "year": 1010, "year_display": "1010 CE", "title": "Consecration by Rajaraja Chola I", "description": "Emperor Rajaraja I completes the 216-foot granite vimana on the 275th day of his 25th regnal year, dedicating it as Rajarajeswaram.", "category": "Construction", "source_name": "Thanjavur Temple South Wall Inscriptions", "source_type": "OFFICIAL"},
            {"site_name": "Brihadisvara Temple (Big Temple)", "year": 1987, "year_display": "1987 CE", "title": "UNESCO World Heritage Inscription", "description": "Inscribed as the primary monument of the 'Great Living Chola Temples' showcasing continuous living Dravidian rituals for over 1,000 years.", "category": "Modern Status", "source_name": "UNESCO World Heritage Centre", "source_type": "OFFICIAL"},
            {"site_name": "Brihadisvara Temple (Big Temple)", "year": 2010, "year_display": "2010 CE", "title": "Millennial 1,000-Year Consecration Celebrations", "description": "Government of Tamil Nadu and Archaeological Survey host monumental 1,000th anniversary with 1,000 classical Bharatanatyam dancers performing simultaneously in the courtyard.", "category": "Cultural Event", "source_name": "ASI & Ministry of Culture Documentation", "source_type": "OFFICIAL"},

            # Terracotta Temples of Bishnupur
            {"site_name": "Terracotta Temples of Bishnupur", "year": 1600, "year_display": "1600 CE", "title": "Rasmancha Built by King Bir Hambir", "description": "Malla King Bir Hambir converts to Gaudiya Vaishnavism and builds the pyramidal Rasmancha to host deities from all surrounding village shrines during Ras Utsav.", "category": "Construction", "source_name": "Malla Dynasty Chronicles & ASI Kolkata Circle", "source_type": "OFFICIAL"},
            {"site_name": "Terracotta Temples of Bishnupur", "year": 1655, "year_display": "1655 CE", "title": "Jor Bangla & Shyam Rai Carved Relief Marvels", "description": "King Raghunath Singha commissions the twin-hut Jor Bangla temple with exquisite terracotta friezes of Ramayana, Mahabharata, and rural river life.", "category": "Architectural Change", "source_name": "Bengal Temple Architecture Studies", "source_type": "ACADEMIC"},
            {"site_name": "Terracotta Temples of Bishnupur", "year": 1998, "year_display": "1998 CE", "title": "Tentative UNESCO World Heritage List", "description": "Submitted to the UNESCO Tentative List as unique universal representation of Bengal terracotta brick temple construction.", "category": "Modern Status", "source_name": "UNESCO Tentative Submissions", "source_type": "OFFICIAL"}
        ]

        MonumentHistoryEvent.query.delete()
        for he in history_events_data:
            site = site_objects.get(he["site_name"])
            if site:
                db.session.add(MonumentHistoryEvent(
                    heritage_site_id=site.id,
                    year=he["year"],
                    year_display=he["year_display"],
                    title=he["title"],
                    description=he["description"],
                    category=he["category"],
                    source_name=he["source_name"],
                    source_type=he["source_type"],
                    verification_status="VERIFIED"
                ))
        db.session.commit()
        print("  ✔ Seeded Chronological History Events for All 8 National Monuments.")

        # 9. Seed Living Crafts & Artisan Guilds
        crafts_data = [
            {
                "site_name": "Taj Mahal",
                "state_code": "UP",
                "name": "Pietra Dura (Parchin Kari) Marble Inlay",
                "category": "Stone Craft",
                "description": "Exquisite hand-carved floral mosaic art where semi-precious gemstones (lapis lazuli, malachite, jasper, carnelian) are precisely ground and inlaid into Makrana white marble recesses.",
                "materials_and_technique": "Emery wheel grinding, diamond-tipped chisels, handmade organic mastic glue, white Makrana marble.",
                "cultural_significance": "Living royal Mughal craft tradition passed down unbroken for 12 generations among 3,000 artisan families in Agra.",
                "artisan_cluster_location": "Taj Ganj & Gokulpura Artisan Quarters, Agra",
                "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/ca/Pietra_Dura_Taj_Mahal.jpg/640px-Pietra_Dura_Taj_Mahal.jpg"
            },
            {
                "site_name": "Konark Sun Temple (Black Pagoda)",
                "state_code": "OR",
                "name": "Chlorite & Khondalite Stone Sculpting",
                "category": "Stone Craft",
                "description": "Traditional Odishan stone carving producing miniature replicas of Konark sundials, Nayika figures, and temple deities using ancient Silpa Sastras guidelines.",
                "materials_and_technique": "Soft soapstone, green chlorite, red laterite, hand hammers, and tempered steel fine chisels.",
                "cultural_significance": "Direct lineage to the 1,200 master sculptors of the 13th-century Sun Temple chariot.",
                "artisan_cluster_location": "Konark Artisan Village & Puri Shilha Kala Kendra, Odisha",
                "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/47/Konarke_sun_temple.jpg/640px-Konarke_sun_temple.jpg"
            },
            {
                "site_name": "Hampi Monuments & Stone Chariot",
                "state_code": "KA",
                "name": "Bell-Metal Dhokra Casting & Granite Reliefs",
                "category": "Metalwork & Stone",
                "description": "Lost-wax bronze and bell-metal casting of temple lamps, bells, and deities, complemented by granite architectural carving.",
                "materials_and_technique": "Beeswax armature models, alluvial clay moulds, molten bronze bell-metal alloys.",
                "cultural_significance": "Supplied the ritual implements and statues of the grand Vittala and Virupaksha shrines during the Vijayanagara golden age.",
                "artisan_cluster_location": "Anegundi Crafts Collective & Sandur Artisan Guild, Karnataka",
                "image_url": "https://images.fineartamerica.com/images-medium-large/stone-chariot-at-vittala-temple-complex-in-hampi-india-rohit-chowdhry.jpg"
            },
            {
                "site_name": "Brihadisvara Temple (Big Temple)",
                "state_code": "TN",
                "name": "Tanjore Painting with 22k Gold Leaf & Chola Bronzes",
                "category": "Painting & Bronze",
                "description": "Classical South Indian art characterized by dense composition, glowing 22-carat gold foil relief, semi-precious Jaipur stones, alongside world-famous lost-wax Nataraja bronzes.",
                "materials_and_technique": "Teak wood board, unbleached cloth, chalk powder paste (gesso work), pure 22k gold foil, vegetable dyes.",
                "cultural_significance": "Royal Chola and Maratha patronized sacred iconography preserved under GI (Geographical Indication) tag.",
                "artisan_cluster_location": "Swamimalai Bronze Village & Thanjavur Royal Palace Quarter",
                "image_url": "https://mir-s3-cdn-cf.behance.net/project_modules/2800_opt_1/78f3ef58411245.59fb28367b6f4.jpg"
            },
            {
                "site_name": "Amber Fort & Palace",
                "state_code": "RJ",
                "name": "Meenakari Enamelling & Blue Pottery",
                "category": "Pottery & Jewelry",
                "description": "Vibrant enamel work fusing colored glass oxides into gold and silver engravings, paired with quartz-based Persian blue glazed pottery.",
                "materials_and_technique": "Ground quartz stone, Fuller's earth, gum, cobalt oxide and copper oxide natural mineral colors.",
                "cultural_significance": "Introduced to Amber by Raja Man Singh I from Lahore in the 16th century; staple of Rajasthani royal courtly aesthetics.",
                "artisan_cluster_location": "Amber Town, Sanganer & Johari Bazaar, Jaipur",
                "image_url": "https://tse2.mm.bing.net/th/id/OIP.JRwu95b6i6VIMXXB4aOEKAHaD4?r=0&rs=1&pid=ImgDetMain&o=7&rm=3"
            },
            {
                "site_name": "Ajanta Caves",
                "state_code": "MH",
                "name": "Mineral Pigment Fresco Painting & Mud-Plaster Tempera",
                "category": "Painting",
                "description": "Ancient mural painting technique using cow dung, clay, rice husk plaster, and organic earth pigments to render glowing spiritual figures.",
                "materials_and_technique": "Lapis lazuli (blue), red ochre, yellow ochre, lamp black, lime white, plant binders.",
                "cultural_significance": "Technique formulated in the Chitrasutra of Vishnudharmottara Purana, forming the root of classical Asian painting.",
                "artisan_cluster_location": "Fardapur & Aurangabad Traditional Art Studios, Maharashtra",
                "image_url": "https://www.easeindiatrip.com/blog/wp-content/uploads/2025/03/Maharashtra-Aurangabad-Ajanta-Caves-02.jpg"
            },
            {
                "site_name": "Terracotta Temples of Bishnupur",
                "state_code": "WB",
                "name": "Baluchari Silk Weaving & Terracotta Craft",
                "category": "Textile & Terracotta",
                "description": "Intricate jacquard silk sarees with mythological temple scenes woven into pallus, alongside baked clay votive Bankura horses and tiles.",
                "materials_and_technique": "Mulberry silk yarn, hand jacquard looms, local Gangetic alluvial clay, wood-fired kilns.",
                "cultural_significance": "GI-tagged heritage textile directly illustrating the same Mahabharata narratives as the Bishnupur temple walls.",
                "artisan_cluster_location": "Bishnupur Silk Weavers Colony & Panchmura Terracotta Village, West Bengal",
                "image_url": "https://images.unsplash.com/photo-1590050752117-238cb0fb12b1?auto=format&fit=crop&w=1200&q=80"
            },
            {
                "site_name": "Qutub Minar & Complex",
                "state_code": "DL",
                "name": "Zardozi Metallic Embroidery & Sandstone Inscription Jali",
                "category": "Textile & Stone",
                "description": "Heavy three-dimensional embroidery using genuine silver and gold-plated wire on silk and velvet, mirroring the calligraphic friezes of the minaret.",
                "materials_and_technique": "Kora, Dabka, Salma metallic threads, sequins, wooden frame (Adda), fine needlework.",
                "cultural_significance": "Imperial atelier craft flourished under Delhi Sultanate and Mughal patronage in Shahjahanabad.",
                "artisan_cluster_location": "Mehrauli Crafts Village & Old Delhi Chandni Chowk Guilds",
                "image_url": "https://tse2.mm.bing.net/th/id/OIP.e_hkBJNBPV7gUsACS3zv1wHaE8?r=0&rs=1&pid=ImgDetMain&o=7&rm=3"
            }
        ]

        HeritageCraft.query.delete()
        for cr in crafts_data:
            site = site_objects.get(cr["site_name"])
            st_id = state_map.get(cr["state_code"])
            if site:
                db.session.add(HeritageCraft(
                    heritage_site_id=site.id,
                    state_id=st_id,
                    name=cr["name"],
                    category=cr["category"],
                    description=cr["description"],
                    materials_and_technique=cr["materials_and_technique"],
                    cultural_significance=cr["cultural_significance"],
                    artisan_cluster_location=cr["artisan_cluster_location"],
                    image_url=cr["image_url"],
                    source_name="National Crafts Registry & Living Traditions Documentation",
                    source_type="CURATED"
                ))
        db.session.commit()
        print("  ✔ Seeded Living Heritage Crafts & Artisan Guilds.")

        # 10. Seed Cultural Traditions & Festivals
        traditions_data = [
            {
                "site_name": "Konark Sun Temple (Black Pagoda)",
                "state_code": "OR",
                "title": "Konark Dance & Music Festival & Magha Saptami",
                "tradition_type": "Festival & Performing Art",
                "season_or_timing": "December Annually & Magha Saptami (February)",
                "description": "World-renowned 5-day festival of classical Indian dance (Odissi, Bharatanatyam, Kathak, Manipuri) performed on an open-air stage against the floodlit Sun Temple backdrop. Concurrently, half a million pilgrims take a holy dip in the Chandrabhaga beach at sunrise on Magha Saptami.",
                "community_role": "Brings together local fishermen, temple dancers, handicraft artisans, and international scholars.",
                "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/47/Konarke_sun_temple.jpg/640px-Konarke_sun_temple.jpg"
            },
            {
                "site_name": "Taj Mahal",
                "state_code": "UP",
                "title": "Taj Mahotsav & Annual Urs of Shah Jahan",
                "tradition_type": "Festival & Ritual Practice",
                "season_or_timing": "February 18-27 Annually & Rajab Month",
                "description": "10-day cultural celebration at Shilpgram showcasing classical Awadhi and Braj vocal music, Kathak recitals, ghazals, and artisan exhibitions. During the 3-day annual Urs, the subterranean original crypts are traditionally opened for floral chadar offerings.",
                "community_role": "Unites local Agra citizens, Sufi qawwals, and master artisans in honoring syncretic Ganga-Jamuni tehzeeb.",
                "image_url": "https://i.pinimg.com/originals/f2/cf/71/f2cf717c1bf0c4e1a77fdd97489fae7d.jpg"
            },
            {
                "site_name": "Hampi Monuments & Stone Chariot",
                "state_code": "KA",
                "title": "Hampi Utsav (Vijaya Utsava)",
                "tradition_type": "Festival",
                "season_or_timing": "November Annually (Winter Solstice Window)",
                "description": "Mega cultural extravaganza celebrating the glory of the Vijayanagara Empire with night-time sound and light shows across the Vittala and Virupaksha monuments, Janapada folk songs, Togalu Gombeyaata shadow puppetry, and traditional fireworks.",
                "community_role": "Organized jointly with local Bellary and Koppal farming communities, folklore troupes, and classical musicians.",
                "image_url": "https://images.fineartamerica.com/images-medium-large/stone-chariot-at-vittala-temple-complex-in-hampi-india-rohit-chowdhry.jpg"
            },
            {
                "site_name": "Brihadisvara Temple (Big Temple)",
                "state_code": "TN",
                "title": "Maha Shivaratri Natyanjali & Brahan Natyanjali",
                "tradition_type": "Performing Art & Sacred Ritual",
                "season_or_timing": "February / March (Maha Shivaratri Eve)",
                "description": "All-night spiritual dance offering in the vast granite courtyard where hundreds of classical Bharatanatyam, Kuchipudi, and Mohiniyattam exponents offer their art to Lord Nataraja under the towering vimana shadow.",
                "community_role": "Continuous temple ritual tradition supported by hereditary Oduvars (temple hymn singers) and nadaswaram instrumentalists.",
                "image_url": "https://mir-s3-cdn-cf.behance.net/project_modules/2800_opt_1/78f3ef58411245.59fb28367b6f4.jpg"
            },
            {
                "site_name": "Amber Fort & Palace",
                "state_code": "RJ",
                "title": "Shila Devi Navratri Puja & Teej Royal Procession",
                "tradition_type": "Ritual Practice & Folklore",
                "season_or_timing": "Ashvin Navratri (October) & Shravan Teej (August)",
                "description": "Deep religious devotion at the 16th-century Shila Devi Temple inside the fort gate, marked by royal elephant processions, Kalbelia folk dances, and traditional Shekhawati drum ceremonies.",
                "community_role": "Fosters living community devotion among Jaipur and Amber resident families who make annual pilgrimages.",
                "image_url": "https://tse2.mm.bing.net/th/id/OIP.JRwu95b6i6VIMXXB4aOEKAHaD4?r=0&rs=1&pid=ImgDetMain&o=7&rm=3"
            },
            {
                "site_name": "Terracotta Temples of Bishnupur",
                "state_code": "WB",
                "title": "Bishnupur Mela & Classical Bishnupur Gharana Dhrupad",
                "tradition_type": "Festival & Musical Tradition",
                "season_or_timing": "December 23-27 Annually",
                "description": "Celebration of Bengal's only classical Dhrupad music gharana founded under Malla patronage, combined with regional folk Baul songs, terracotta pottery fairs, and sacred Ras Yatra processions.",
                "community_role": "Entire town participates in community feasts, conch shell blowing competitions, and traditional silk fairs.",
                "image_url": "https://images.unsplash.com/photo-1590050752117-238cb0fb12b1?auto=format&fit=crop&w=1200&q=80"
            }
        ]

        CulturalTradition.query.delete()
        for tr in traditions_data:
            site = site_objects.get(tr["site_name"])
            st_id = state_map.get(tr["state_code"])
            if site:
                db.session.add(CulturalTradition(
                    heritage_site_id=site.id,
                    state_id=st_id,
                    title=tr["title"],
                    tradition_type=tr["tradition_type"],
                    season_or_timing=tr["season_or_timing"],
                    description=tr["description"],
                    community_role=tr["community_role"],
                    image_url=tr["image_url"],
                    source_name="Living Traditions & Festivals Documentation",
                    source_type="CURATED"
                ))
        db.session.commit()
        print("  ✔ Seeded Living Cultural Traditions & Festivals.")

        # 11. Seed Curated Thematic Trails & Sequential Stops
        trails_data = [
            {
                "title": "Imperial Grand Axis: Sultanates to Mughal Opulence",
                "slug": "imperial-grand-axis",
                "theme": "Imperial Dynastic Architecture",
                "description": "Trace the architectural evolution of northern India across five centuries — from the 72m fluted sandstone towers of the Delhi Sultanate to the symmetrical white marble gardens of Agra and the regal hill ramparts of Rajputana.",
                "historical_era": "12th - 18th Century CE",
                "estimated_duration": "3 - 4 Days",
                "difficulty": "Moderate Overland Journey",
                "featured_image_url": "https://i.pinimg.com/originals/f2/cf/71/f2cf717c1bf0c4e1a77fdd97489fae7d.jpg",
                "is_featured": True,
                "stops": [
                    {
                        "site_name": "Qutub Minar & Complex",
                        "stop_order": 1,
                        "stop_title": "First Pillar of Indo-Islamic Engineering",
                        "narrative_focus": "Examine how reused temple colonnades and early Arabic calligraphy forged a new hybrid architectural vocabulary in the Mehrauli plains.",
                        "recommended_time_hours": 3.0
                    },
                    {
                        "site_name": "Taj Mahal",
                        "stop_order": 2,
                        "stop_title": "Zenith of Marble Geometry & Riverfront Planning",
                        "narrative_focus": "Analyze bilateral Charbagh geometry, optical illusions in minaret canting, and Pietra Dura floral masterworks along the Yamuna.",
                        "recommended_time_hours": 4.5
                    },
                    {
                        "site_name": "Amber Fort & Palace",
                        "stop_order": 3,
                        "stop_title": "Rajput Imperial Bastions & Sheesh Mahal Mosaics",
                        "narrative_focus": "Explore the strategic marriage of Mughal court elegance with Rajput defensive hill fortress architecture.",
                        "recommended_time_hours": 4.0
                    }
                ]
            },
            {
                "title": "Sacred Stone & Cosmic Astronomy Trail",
                "slug": "sacred-stone-astronomy",
                "theme": "Temple Astronomy & Monumental Sculpting",
                "description": "Embark on a spiritual and scientific exploration of India's most breathtaking monumental temples. Witness how ancient astronomers and sculptors transformed chlorite, granite, and terracotta into living cosmic calculators.",
                "historical_era": "11th - 18th Century CE",
                "estimated_duration": "4 - 5 Days",
                "difficulty": "Multi-State Heritage Discovery",
                "featured_image_url": "https://cdn.britannica.com/19/251919-050-D3E64798/konark-sun-temple-orissa-india-unesco-heritage-site.jpg",
                "is_featured": True,
                "stops": [
                    {
                        "site_name": "Brihadisvara Temple (Big Temple)",
                        "stop_order": 1,
                        "stop_title": "Chola Granite Engineering & Shadowless Vimana",
                        "narrative_focus": "Marvel at the 80-tonne monolithic cupola hoisted onto a 216-foot interlocking granite vimana with no binding mortar.",
                        "recommended_time_hours": 3.5
                    },
                    {
                        "site_name": "Konark Sun Temple (Black Pagoda)",
                        "stop_order": 2,
                        "stop_title": "The 24-Wheeled Solar Chariot & Precision Sundials",
                        "narrative_focus": "Decode the exact shadow-casting time-telling spokes of the 24 massive chlorite chariot wheels aligned to solar equinoxes.",
                        "recommended_time_hours": 4.0
                    },
                    {
                        "site_name": "Terracotta Temples of Bishnupur",
                        "stop_order": 3,
                        "stop_title": "Fired Earth Epics of the Bengal Delta",
                        "narrative_focus": "Discover how clay tiles were sculpted and wood-fired to depict sacred literature when stone was absent across the deltaic floodplains.",
                        "recommended_time_hours": 3.0
                    }
                ]
            },
            {
                "title": "Deccan Rock-Cut & Granite Monolith Circuit",
                "slug": "deccan-rock-cut-circuit",
                "theme": "Subterranean & Monolithic Carving",
                "description": "From the sheer basalt canyon wall caves of Ajanta to the vast granite boulder labyrinth of Vijayanagara, witness the pinnacle of subterranean and surface rock sculpture.",
                "historical_era": "2nd Century BCE - 16th Century CE",
                "estimated_duration": "3 Days",
                "difficulty": "Active Terrain Trail",
                "featured_image_url": "https://th.bing.com/th/id/R.f10a6bbde9457a12ea4732f440cdd197?rik=M9AwgeYYzuyLsg&riu=http%3a%2f%2fwww.thehistoryhub.com%2fwp-content%2fuploads%2f2014%2f04%2fHampi-Chariot.jpg&ehk=MX5BNohAmJnqbpQiCNi9qn%2fg%2fGeP4wF7LIiyhuF5Ixo%3d&risl=&pid=ImgRaw&r=0",
                "is_featured": True,
                "stops": [
                    {
                        "site_name": "Ajanta Caves",
                        "stop_order": 1,
                        "stop_title": "Basalt Rock-Cut Chaityas & Tempera Murals",
                        "narrative_focus": "Walk inside 30 hand-chiseled Buddhist caves preserving the world's most delicate ancient wall paintings.",
                        "recommended_time_hours": 5.0
                    },
                    {
                        "site_name": "Hampi Monuments & Stone Chariot",
                        "stop_order": 2,
                        "stop_title": "Vittala Musical Pillars & Granite Bazaar City",
                        "narrative_focus": "Explore the stone chariot of Garuda, acoustic musical columns, and 4,100 hectares of medieval urban grandeur.",
                        "recommended_time_hours": 6.0
                    }
                ]
            }
        ]

        HeritageTrail.query.delete()
        TrailStop.query.delete()
        for tr_data in trails_data:
            stops_info = tr_data.pop("stops", [])
            trail = HeritageTrail(**tr_data)
            db.session.add(trail)
            db.session.flush()

            for st_info in stops_info:
                target_site = site_objects.get(st_info["site_name"])
                if target_site:
                    db.session.add(TrailStop(
                        trail_id=trail.id,
                        heritage_site_id=target_site.id,
                        stop_order=st_info["stop_order"],
                        stop_title=st_info["stop_title"],
                        narrative_focus=st_info["narrative_focus"],
                        recommended_time_hours=st_info.get("recommended_time_hours", 3.0)
                    ))
        db.session.commit()
        print("  ✔ Seeded Curated Thematic Trails & Sequential Stops.")

        # 12. Seed Archival Then vs Now Visual Comparisons
        then_vs_now_data = [
            {
                "site_name": "Konark Sun Temple (Black Pagoda)",
                "title": "Jagamohana & Chariot Wheel Plinth Conservation (1868 vs 2026)",
                "historical_year": "1868 CE Archival Survey",
                "historical_image_url": "https://cdn.britannica.com/19/251919-050-D3E64798/konark-sun-temple-orissa-india-unesco-heritage-site.jpg",
                "historical_image_caption": "Archival photographic plate showing shifting coastal sand dunes partially burying the lower chariot wheels and collapsed sikhara rubble.",
                "current_year": "2026 CE Present Telemetry",
                "current_image_url": "https://i.pinimg.com/originals/c6/4b/5e/c64b5e5284470c89b87763868614fbf9.jpg",
                "current_image_caption": "Contemporary view with excavated plinth, manicured casuarina windbreaks, and automated moisture sensors monitoring saline exposure.",
                "comparison_category": "Restoration & Landscape",
                "observations_text": "Over 150 years of conservation have stabilized the Jagamohana assembly hall. Current efforts focus on safely evacuating the 1901 internal sand packing while defending against cyclonic moisture intrusion.",
                "source_name": "Archaeological Survey of India Photographic Archives"
            },
            {
                "site_name": "Taj Mahal",
                "title": "Yamuna Riverfront & White Marble Radiance (1904 vs 2026)",
                "historical_year": "1904 CE Lord Curzon Survey",
                "historical_image_url": "https://i.pinimg.com/originals/f2/cf/71/f2cf717c1bf0c4e1a77fdd97489fae7d.jpg",
                "historical_image_caption": "Early 20th-century colonial survey showing the original British-style lawn restoration and low industrial presence in Agra.",
                "current_year": "2026 CE Present Day",
                "current_image_url": "https://i.pinimg.com/originals/f2/cf/71/f2cf717c1bf0c4e1a77fdd97489fae7d.jpg",
                "current_image_caption": "High-resolution modern monitoring verifying surface reflectance following non-invasive Multani Mitti clay poultice cycles.",
                "comparison_category": "Surroundings & Air Quality",
                "observations_text": "While structural stability remains top-tier (88/100), modern challenges focus on the low riverbed water table of the Yamuna and atmospheric particulate deposition from the surrounding urban basin.",
                "source_name": "ASI Agra Chemical Division & National Archives"
            },
            {
                "site_name": "Hampi Monuments & Stone Chariot",
                "title": "Vittala Temple Stone Chariot Preservation (1856 vs 2026)",
                "historical_year": "1856 CE Alexander Greenlaw Calotype",
                "historical_image_url": "https://th.bing.com/th/id/R.f10a6bbde9457a12ea4732f440cdd197?rik=M9AwgeYYzuyLsg&riu=http%3a%2f%2fwww.thehistoryhub.com%2fwp-content%2fuploads%2f2014%2f04%2fHampi-Chariot.jpg&ehk=MX5BNohAmJnqbpQiCNi9qn%2fg%2fGeP4wF7LIiyhuF5Ixo%3d&risl=&pid=ImgRaw&r=0",
                "historical_image_caption": "Earliest known photograph of Hampi's stone chariot with the original brick-and-mortar sikhara tower intact on its upper tier.",
                "current_year": "2026 CE Present Protection",
                "current_image_url": "https://images.fineartamerica.com/images-medium-large/stone-chariot-at-vittala-temple-complex-in-hampi-india-rohit-chowdhry.jpg",
                "current_image_caption": "Present-day stabilized shrine with protective perimeter wooden stanchions to prevent tourist climbing damage.",
                "comparison_category": "Structure & Preservation",
                "observations_text": "The brick sikhara was dismantled in the late 19th century to prevent weight collapse onto the carved granite axle. Protective stanchions installed in 2021 have successfully eliminated direct physical abrasion on the wheel hubs.",
                "source_name": "British Library Calotype Collection & ASI Hampi Circle"
            }
        ]

        ThenVsNow.query.delete()
        for tvn in then_vs_now_data:
            site = site_objects.get(tvn["site_name"])
            if site:
                db.session.add(ThenVsNow(
                    heritage_site_id=site.id,
                    title=tvn["title"],
                    historical_year=tvn["historical_year"],
                    historical_image_url=tvn["historical_image_url"],
                    historical_image_caption=tvn["historical_image_caption"],
                    current_year=tvn["current_year"],
                    current_image_url=tvn["current_image_url"],
                    current_image_caption=tvn["current_image_caption"],
                    comparison_category=tvn["comparison_category"],
                    observations_text=tvn["observations_text"],
                    source_name=tvn["source_name"],
                    source_type="CURATED"
                ))
        db.session.commit()
        print("  ✔ Seeded Archival Then vs Now Visual Comparisons.")

        # 13. Seed Contextual Surroundings Factors
        surroundings_data = [
            {"site_name": "Taj Mahal", "factor_type": "River Basin", "name": "Yamuna River Floodplain & Desiccation Zone", "distance_meters": 50, "description": "The seasonal flow variation of River Yamuna impacts the moisture level of subterranean ebony/sal wood foundation wells.", "impact_nature": "Monitored Concern"},
            {"site_name": "Taj Mahal", "factor_type": "Buffer Greenery", "name": "Mehtab Bagh Northern Buffer Gardens", "distance_meters": 250, "description": "Lush Mughal garden across the river provides a natural particulate buffer against northern winds.", "impact_nature": "Buffer Protection"},
            {"site_name": "Taj Mahal", "factor_type": "Craft Cluster", "name": "Taj Ganj Historic Artisan Quarter", "distance_meters": 150, "description": "Centuries-old settlement hosting 12th-generation Pietra Dura marble inlay and zardozi master artisans.", "impact_nature": "Cultural Asset"},
            {"site_name": "Konark Sun Temple (Black Pagoda)", "factor_type": "Buffer Greenery", "name": "Chandrabhaga Coastal Casuarina Shelterbelt", "distance_meters": 1200, "description": "Dense coastal plantation engineered to absorb maritime wind kinetic force and reduce airborne saline sand intrusion.", "impact_nature": "Buffer Protection"},
            {"site_name": "Hampi Monuments & Stone Chariot", "factor_type": "River Basin", "name": "Tungabhadra River Riparian Ecosystem", "distance_meters": 100, "description": "Perennial river corridor sustaining riparian wildlife, agricultural banana groves, and ancient boulder geology.", "impact_nature": "Positive Ecosystem"}
        ]

        HeritageSurrounding.query.delete()
        for sr in surroundings_data:
            site = site_objects.get(sr["site_name"])
            if site:
                db.session.add(HeritageSurrounding(
                    heritage_site_id=site.id,
                    factor_type=sr["factor_type"],
                    name=sr["name"],
                    distance_meters=sr["distance_meters"],
                    description=sr["description"],
                    impact_nature=sr["impact_nature"],
                    status="Active"
                ))
        db.session.commit()
        print("  ✔ Seeded Contextual Surroundings & Environmental Factors.")

        # 14. Seed Verified Citizen Oral History Community Stories
        community_stories_data = [
            {
                "site_name": "Taj Mahal",
                "author_name": "Imran Khan",
                "author_role": "Pietra Dura Master Artisan",
                "author_email": "imran.tajganj@crafts.in",
                "title": "Twelve Generations of Inlaying Gemstones in Taj Ganj",
                "story_content": "My great-great-grandfather worked on the marble restoration under Lord Curzon. He used to tell us how they ground lapis lazuli on emery wheels by hand with mustard oil. Every morning when the Taj glows pink in the sunrise, our workshop begins by chipping floral petals out of malachite. For us, the Taj isn't just a monument; it is our living teacher of patience, geometry, and devotion.",
                "story_type": "Oral History",
                "historical_period": "Living Memory (1940s-Present)",
                "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/ca/Pietra_Dura_Taj_Mahal.jpg/640px-Pietra_Dura_Taj_Mahal.jpg"
            },
            {
                "site_name": "Konark Sun Temple (Black Pagoda)",
                "author_name": "Subhasish Mohapatra",
                "author_role": "Local Historian & Resident",
                "author_email": "subhasish.puri@heritage.org",
                "title": "My Grandfather's Tales of the Shifting Chandrabhaga Sands",
                "story_content": "When I was seven years old, my grandfather took me to the eastern face of the Sun Temple on Magha Saptami. He pointed to the carved chariot wheels and explained how the spokes cast shadows to tell the exact time of day down to three minutes. He remembered when the casuarina trees were first planted to stop the sand dunes from swallowing the lower tier. Konark lives in the rhythm of the Bay of Bengal.",
                "story_type": "Memory",
                "historical_period": "1960s Living Memory",
                "image_url": "https://cdn.britannica.com/19/251919-050-D3E64798/konark-sun-temple-orissa-india-unesco-heritage-site.jpg"
            },
            {
                "site_name": "Hampi Monuments & Stone Chariot",
                "author_name": "Venkatachalaiah",
                "author_role": "Anegundi Village Elder",
                "author_email": "venkat.hampi@karnataka.in",
                "title": "Hearing the Musical Pillars Resonate on Cool Monsoon Evenings",
                "story_content": "In 1965, before the stone barricades were erected, my music guru would tap the slender granite pillars of the Vittala Maha Mandapa with sandalwood rods. Seven different musical notes rang out clear as bronze bells through the boulder hills. Though we now protect them from touching, that acoustic resonance taught our entire village the sacred mathematics of stone.",
                "story_type": "Oral History",
                "historical_period": "1965 Living Tradition",
                "image_url": "https://images.fineartamerica.com/images-medium-large/stone-chariot-at-vittala-temple-complex-in-hampi-india-rohit-chowdhry.jpg"
            },
            {
                "site_name": "Brihadisvara Temple (Big Temple)",
                "author_name": "Dr. Meenakshi Sundaram",
                "author_role": "Epigraphist & Temple Researcher",
                "author_email": "meenakshi.chola@tamiluniv.ac.in",
                "title": "Decoding the 108 Dance Poses Carved into the Second Tier",
                "story_content": "Climbing the narrow granite stairs inside the Big Temple vimana in 1988 with an ASI permit was the most moving experience of my life. Along the corridor walls, King Rajaraja had carved 108 Karana dance sculptures of Lord Shiva in pure black granite. Each sculptured pose holds the movement of cosmic energy. It is not stone; it is music made solid.",
                "story_type": "Memory",
                "historical_period": "1980s Archival Research",
                "image_url": "https://mir-s3-cdn-cf.behance.net/project_modules/2800_opt_1/78f3ef58411245.59fb28367b6f4.jpg"
            }
        ]

        CommunityStory.query.delete()
        for cs in community_stories_data:
            site = site_objects.get(cs["site_name"])
            if site:
                db.session.add(CommunityStory(
                    heritage_site_id=site.id,
                    user_id=user.id,
                    author_name=cs["author_name"],
                    author_role=cs["author_role"],
                    author_email=cs["author_email"],
                    title=cs["title"],
                    story_content=cs["story_content"],
                    story_type=cs["story_type"],
                    historical_period=cs["historical_period"],
                    image_url=cs["image_url"],
                    status="Verified",
                    source_type="COMMUNITY"
                ))
        db.session.commit()
        print("  ✔ Seeded Verified Citizen Oral Histories & Community Stories.")

        db.session.commit()
        print("✨ Database successfully seeded with Complete Discovery, Living Culture, Trails & Preservation Intelligence Data!")

if __name__ == "__main__":
    seed_database()

