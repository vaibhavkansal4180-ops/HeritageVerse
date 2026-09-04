# HeritageVerse – National Heritage Preservation Intelligence Platform

A unified national conservation intelligence platform providing real-time risk telemetry, automated damage assessment, and buffer zone protection for monuments across India.

**Preservation Pipeline**: `DETECT → ANALYSE → SCORE → PRIORITIZE → ALERT → ACT → TRACK`

---

## 🏛️ Project Directory Structure

```
C:\Users\Administrator\.gemini\antigravity\scratch\HeritageVerse\
├── backend/
│   ├── ai/
│   │   ├── damage_analyzer.py        # AI preliminary damage analysis
│   │   └── preservation_assistant.py # Decision support assistant
│   ├── models/                       # SQLAlchemy ORM models
│   │   ├── heritage.py
│   │   ├── preservation.py
│   │   ├── report.py
│   │   └── user.py
│   ├── routes/                       # REST API endpoints
│   │   ├── admin.py
│   │   ├── alerts.py
│   │   ├── auth.py
│   │   ├── heritage.py
│   │   ├── preservation.py
│   │   ├── reports.py
│   │   └── stats.py
│   ├── services/                     # Health scoring & alert services
│   ├── app.py                        # Flask application factory
│   └── seed.py                       # Seeding script
├── frontend/
│   ├── css/
│   │   └── style.css                 # Warm Ivory & Deep Forest Green design
│   ├── js/
│   │   ├── admin.js                  # Command Center & Chart.js logic
│   │   ├── api.js                    # REST API client & Toast utility
│   │   ├── auth.js                   # Authentication & navigation controller
│   │   ├── heritage.js               # Sites registry & search controller
│   │   └── reports.js                # Citizen incident submission controller
│   ├── index.html                    # National Intelligence Portal
│   ├── sites.html                    # Monitored Sites Registry
│   ├── site-detail.html              # Site Preservation Dossier
│   ├── report.html                   # Citizen Damage Reporting
│   ├── track.html                    # Public Incident Tracker by UID
│   ├── my-reports.html               # Citizen Watch personal desk
│   ├── encroachment.html             # AMASR Act 100m/300m Buffer Desk
│   ├── alerts.html                   # Early Warning Hazard Alerts Desk
│   ├── admin.html                    # Conservation Command Center
│   └── login.html                    # Portal Authentication
├── database/
│   └── schema.sql                    # Complete MySQL DDL schema
├── test_api.py                       # Automated test suite (13/13 passing)
├── run.py                            # One-click launcher
└── requirements.txt                  # Python dependencies
```

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Seed & Run
```bash
python run.py
```

Open your browser at **`http://localhost:5000`**.

### 3. Demo Credentials
- **Conservation Admin**: `admin@heritageverse.in` / `Admin@123`
- **Citizen Watcher**: `user@heritageverse.in` / `User@123`
- *(One-click auto-fill buttons are provided directly on the Login page)*

---

## 🧪 Running Tests

```bash
python test_api.py
```
