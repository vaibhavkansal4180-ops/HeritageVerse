#!/usr/bin/env python3
"""
HeritageVerse – Real-World Heritage Preservation Intelligence Platform
One-Click Application Launcher
"""

import os
import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from backend.app import create_app
from backend.models import db, HeritageSite
from backend.seed import seed_database

def main():
    print("=" * 65)
    print(" HERITAGEVERSE - PRESERVATION INTELLIGENCE PLATFORM")
    print(" Pipeline: DETECT -> ANALYSE -> SCORE -> PRIORITIZE -> ALERT -> ACT -> TRACK")
    print("=" * 65)

    app = create_app()

    with app.app_context():
        # Check Database & Seed if empty
        site_count = HeritageSite.query.count()
        if site_count == 0:
            print("\n[Step 1/2] Database is empty. Seeding national monuments and telemetry records...")
            seed_database()
        else:
            print(f"\n[Step 1/2] Database ready with {site_count} monitored heritage sites.")

    # Start Flask Web Server
    port = int(os.getenv("PORT", 5000))
    print(f"\n[Step 2/2] Starting Conservation Intelligence Web Server...")
    print(f"  * Open Platform:   http://localhost:{port}")
    print(f"  * Admin Portal:    admin@heritageverse.in / Admin@123")
    print(f"  * Citizen Portal:  user@heritageverse.in  / User@123")
    print("=" * 65)
    print("Press CTRL+C to stop the server.\n")

    app.run(host="0.0.0.0", port=port, debug=True)

if __name__ == "__main__":
    main()
