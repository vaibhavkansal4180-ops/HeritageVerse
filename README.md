# HeritageVerse – National Heritage Preservation Intelligence Platform

A unified national conservation intelligence platform providing real-time risk telemetry, automated damage assessment, AMASR Act buffer zone monitoring, and preservation case dossiers for monuments across India.

**Preservation Pipeline**: `DETECT → ANALYSE → SCORE → PRIORITIZE → ALERT → ACT → TRACK`

---

## 🏛️ System Architecture

- **Backend**: Flask 3.x, SQLAlchemy 2.x ORM, Stateless JWT Authentication, Serverless WSGI entrypoint (`api/index.py`).
- **Database**: PostgreSQL (Production recommended via Neon, Supabase, Vercel Postgres, AWS RDS) with transparent offline SQLite fallback.
- **Frontend**: Responsive HTML5, Vanilla JavaScript (ES6+), CSS3 (IVORY & DEEP FOREST GREEN heritage design system), Chart.js telemetry charts.
- **Deployment**: Zero-config GitHub → Vercel serverless deployment (`@vercel/python`) and standard Gunicorn WSGI (`Procfile`).

---

## 📁 Project Directory Structure

```
HeritageVerse/
├── api/
│   └── index.py                      # Vercel Serverless WSGI entrypoint
├── backend/
│   ├── ai/
│   │   ├── damage_analyzer.py        # AI preliminary damage classifier
│   │   └── preservation_assistant.py # Decision support assistant
│   ├── models/                       # SQLAlchemy ORM models
│   │   ├── heritage.py               # HeritageSite, SiteTelemetry, Encroachment
│   │   ├── preservation.py           # PreservationDossier, PreservationIntervention
│   │   ├── report.py                 # CitizenReport, DamageAssessment
│   │   └── user.py                   # User (Admin / Citizen)
│   ├── routes/                       # Modular REST API endpoints
│   │   ├── admin.py                  # Command center operations
│   │   ├── alerts.py                 # Hazard alerts & early warnings
│   │   ├── auth.py                   # Stateless JWT auth & session management
│   │   ├── heritage.py               # Monitored monuments & dossiers
│   │   ├── preservation.py           # Preservation case files & interventions
│   │   ├── reports.py                # Citizen damage reporting & tracking
│   │   └── stats.py                  # National aggregation & telemetry metrics
│   ├── services/                     # Business logic & health scoring
│   ├── app.py                        # Flask Application Factory
│   ├── config.py                     # Environment-driven configuration
│   └── seed.py                       # Monument seeding script
├── frontend/                         # Modern Single-Domain Static UI
│   ├── css/
│   │   └── style.css                 # Heritage design system & responsive layout
│   ├── js/
│   │   ├── admin.js                  # Conservation Command Center logic
│   │   ├── api.js                    # REST API client & Toast notifications
│   │   ├── auth.js                   # Authentication & navigation controller
│   │   ├── heritage.js               # Sites registry & dossier controller
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
│   └── schema.sql                    # SQL DDL reference schema
├── .env.example                      # Environment variables template
├── .gitignore                        # Git exclusion rules
├── Procfile                          # Gunicorn process definition
├── requirements.txt                  # Python dependencies
├── run.py                            # One-click local launcher & WSGI export
├── test_api.py                       # Automated test suite (13/13 passing)
└── vercel.json                       # Vercel serverless build & routing configuration
```

---

## ⚙️ Environment Variables

Create a `.env` file in the root directory (or configure them in your deployment platform):

| Variable | Description | Default / Example |
| :--- | :--- | :--- |
| `DATABASE_URL` | PostgreSQL connection URI *(auto-falls back to SQLite if empty)* | `postgresql://user:pass@host:5432/dbname` |
| `SECRET_KEY` | Secret key for JWT cryptographic signing | `random-64-character-string` |
| `FLASK_ENV` | Environment mode (`production` or `development`) | `production` |
| `DEBUG` | Enable debug mode | `false` |
| `CORS_ORIGINS` | Allowed CORS origins (comma-separated or `*`) | `*` |
| `PORT` | Local server port | `5000` |

---

## 🚀 Deployment Workflows

### 1. Primary Target: GitHub → Vercel Deployment

1. **Push your repository to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "feat: production-ready HeritageVerse deployment"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/HeritageVerse.git
   git push -u origin main
   ```

2. **Deploy on Vercel**:
   - Go to [Vercel Dashboard](https://vercel.com/dashboard) and click **"Add New Project"**.
   - Import your **HeritageVerse** GitHub repository.
   - Leave the Framework Preset as **Other** (Vercel automatically detects `vercel.json` and `@vercel/python`).
   - In **Environment Variables**, add:
     - `DATABASE_URL`: Your managed PostgreSQL database URL (e.g. Neon, Supabase, Vercel Postgres, AWS RDS).
     - `SECRET_KEY`: A secure random string for JWT signing.
     - `FLASK_ENV`: `production`
   - Click **Deploy**.

3. **Database Seeding (One-time setup for new PostgreSQL instances)**:
   You can seed your remote PostgreSQL database from your local machine:
   ```bash
   # Set the remote DATABASE_URL in your terminal
   set DATABASE_URL=postgresql://user:password@host:5432/dbname
   # Run the seed script
   python -m backend.seed
   ```

---

### 2. Secondary Target: Conventional Python Hosting (Gunicorn / Render / Railway / Heroku / VPS)

The project includes a standard `Procfile` configured for Gunicorn:

```bash
# Run with Gunicorn directly:
gunicorn run:app --bind 0.0.0.0:5000 --workers 4
```

On platforms like Render, Heroku, or Railway:
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn run:app`

---

### 3. Local Development

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Launch platform**:
   ```bash
   python run.py
   ```
   *If running for the first time, `run.py` automatically initializes the local SQLite database and seeds all national monument telemetry records.*

3. **Access the application**:
   - Web Platform: **`http://localhost:5000`**
   - **Conservation Admin**: `admin@heritageverse.in` / `Admin@123`
   - **Citizen Watcher**: `user@heritageverse.in` / `User@123`
   *(One-click auto-fill credentials buttons are provided on the login page)*

---

## 🧪 Automated Testing

Run the comprehensive integration test suite verifying all 13 critical subsystems:

```bash
python test_api.py
```

**Verification Coverage**:
- [x] Health & Readiness Check (`/api/health`)
- [x] Citizen Authentication & JWT Token Issuance (`/api/auth/login`)
- [x] Admin Authentication (`/api/auth/login`)
- [x] Monument Listing & Filter Telemetry (`/api/heritage/sites`)
- [x] Individual Monument Dossier (`/api/heritage/sites/<id>`)
- [x] Preservation Case File & Dossier Intelligence (`/api/preservation/dossier/<id>`)
- [x] Buffer Zone & Encroachment Geo-Desk (`/api/heritage/encroachments`)
- [x] Hazard & Early Warning Alerts (`/api/alerts/active`)
- [x] National Aggregate Preservation Metrics (`/api/stats/overview`)
- [x] Citizen Incident Report Submission (`/api/reports/submit`)
- [x] Public Incident Tracking by UID (`/api/reports/track/<uid>`)
- [x] Protected Admin Incident Review (`/api/admin/reports`)
- [x] Preservation Intervention Status Workflow (`/api/preservation/interventions/<id>/status`)
