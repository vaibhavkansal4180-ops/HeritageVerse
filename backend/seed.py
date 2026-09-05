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
    ConditionTimeline, Alert, AdminAction
)

def seed_database(drop_existing=False):
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

        db.session.commit()
        print("✨ Database successfully seeded with Verified Accurate Heritage Imagery & Baseline Telemetry!")

if __name__ == "__main__":
    seed_database()
