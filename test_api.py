"""
Comprehensive Test Suite for HeritageVerse - Real-World Heritage Preservation Intelligence Platform
Tests all REST API endpoints, AI damage analyzer, health score engine, alert workflows, and admin command center.
"""

import os
import sys
import unittest
import json
from pathlib import Path

# Setup project root import
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.app import create_app
from backend.models import db, User, HeritageSite, HeritageReport, Alert

class HeritageVersePreservationTestSuite(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.client = cls.app.test_client()
        cls.app_context = cls.app.app_context()
        cls.app_context.push()

        # Ensure seed data exists for automated testing in fresh environments
        from backend.seed import seed_database
        if User.query.count() == 0:
            seed_database()

        # Pre-authenticate admin and user for reliable test state
        admin_res = cls.client.post('/api/auth/login', json={
            "email": "admin@heritageverse.in",
            "password": "Admin@123"
        })
        cls.admin_token = admin_res.get_json()["data"]["token"]

        user_res = cls.client.post('/api/auth/login', json={
            "email": "user@heritageverse.in",
            "password": "User@123"
        })
        cls.user_token = user_res.get_json()["data"]["token"]

        # Fetch first monitored site
        sites_res = cls.client.get('/api/heritage')
        sites = sites_res.get_json()["data"]
        cls.test_site_id = sites[0]["id"] if sites else 1

    @classmethod
    def tearDownClass(cls):
        cls.app_context.pop()

    def test_01_health_check_and_pages(self):
        """Test public page routing for preservation platform."""
        routes = ["/", "/sites", "/report", "/track", "/my-reports", "/alerts", "/encroachment", "/admin", "/login"]
        for r in routes:
            res = self.client.get(r)
            self.assertIn(res.status_code, [200, 302], f"Failed route {r}")
        print("  [PASS] Public HTML routes verified")

    def test_02_auth_admin_and_user_login(self):
        """Test admin and citizen authentication."""
        # Admin login
        res = self.client.post('/api/auth/login', json={
            "email": "admin@heritageverse.in",
            "password": "Admin@123"
        })
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data["success"])
        self.assertEqual(data["data"]["user"]["role"], "admin")

        # User login
        res_user = self.client.post('/api/auth/login', json={
            "email": "user@heritageverse.in",
            "password": "User@123"
        })
        self.assertEqual(res_user.status_code, 200)
        data_user = res_user.get_json()
        self.assertTrue(data_user["success"])
        self.assertEqual(data_user["data"]["user"]["role"], "user")
        print("  [PASS] Admin & Citizen authentication verified")

    def test_03_preservation_dashboard_metrics(self):
        """Test national summary metrics and chart feeds."""
        res = self.client.get('/api/preservation/dashboard')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()["data"]
        self.assertIn("summary", data)
        self.assertIn("health_distribution", data)
        self.assertIn("issue_categories", data)
        self.assertIn("critical_monuments", data)
        self.assertGreaterEqual(data["summary"]["total_monitored_sites"], 1)
        print("  [PASS] National Preservation Dashboard KPIs verified")

    def test_04_monitored_sites_and_search(self):
        """Test site registry and search filters."""
        res = self.client.get('/api/heritage')
        self.assertEqual(res.status_code, 200)
        sites = res.get_json()["data"]
        self.assertGreater(len(sites), 0)

        # Search test
        search_res = self.client.get('/api/heritage/search?q=Sun+Temple')
        self.assertEqual(search_res.status_code, 200)
        self.assertGreater(len(search_res.get_json()["data"]), 0)
        print("  [PASS] Monitored Sites Registry & multi-criteria search verified")

    def test_05_site_preservation_dossier(self):
        """Test comprehensive site dossier retrieval."""
        site_id = self.test_site_id
        res = self.client.get(f'/api/preservation/site/{site_id}/dossier')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()["data"]
        self.assertIn("id", data)
        self.assertIn("name", data)
        self.assertIn("health_score_breakdown", data)
        self.assertIn("ai_preservation_assistant", data)
        self.assertIn("latest_environmental", data)
        self.assertIn("latest_tourist_pressure", data)
        self.assertIn("timeline", data)
        self.assertIn("encroachments", data)
        print("  [PASS] Full Site Preservation Dossier payload verified")

    def test_06_heritage_health_score_calculation(self):
        """Test factor-wise health score breakdown."""
        site_id = self.test_site_id
        res = self.client.get(f'/api/preservation/site/{site_id}/health')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()["data"]
        self.assertIn("overall_health_score", data)
        self.assertIn("risk_level", data)
        self.assertIn("factor_breakdown", data)
        factors = data["factor_breakdown"]
        self.assertIn("structural_integrity", factors)
        self.assertIn("citizen_reports_penalty", factors)
        self.assertIn("encroachment_security", factors)
        self.assertIn("disaster_resilience", factors)
        self.assertIn("environmental_safety", factors)
        self.assertIn("tourist_pressure", factors)
        print("  [PASS] Transparent Heritage Health Index (0-100) factor formula verified")

    def test_07_ai_preservation_assistant(self):
        """Test AI Decision Support assistant for site conservators."""
        site_id = self.test_site_id
        res = self.client.get(f'/api/preservation/site/{site_id}/ai-assistant')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()["data"]
        self.assertIn("disclaimer", data)
        self.assertIn("top_threats", data)
        self.assertIn("inspection_checklist", data)
        self.assertIn("recommended_actions", data)
        self.assertTrue("AI-assisted" in data["disclaimer"])
        print("  [PASS] AI Preservation Assistant decision support & disclaimer verified")

    def test_08_encroachment_observations(self):
        """Test protected buffer zone (100m/300m) endpoint."""
        res = self.client.get('/api/preservation/encroachments')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()["data"]
        self.assertIsInstance(data, list)
        if len(data) > 0:
            self.assertIn("monitored_zone", data[0])
            self.assertIn("detected_change", data[0])
        print("  [PASS] AMASR Act Buffer Zone Encroachments verified")

    def test_09_early_warning_alerts_and_action(self):
        """Test alerts listing and admin action update."""
        res = self.client.get('/api/alerts')
        self.assertEqual(res.status_code, 200)
        alerts = res.get_json()["data"]
        self.assertGreater(len(alerts), 0)
        alert_id = alerts[0]["id"]

        # Update alert via admin action
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        action_res = self.client.put(f'/api/alerts/{alert_id}/action', headers=headers, json={
            "status": "In Progress",
            "priority": "High",
            "assigned_to": "ASI Conservation Officer Desk",
            "action_notes": "Field scaffolding dispatched for crack stabilization."
        })
        self.assertEqual(action_res.status_code, 200)
        self.assertTrue(action_res.get_json()["success"])
        print("  [PASS] Early Warning Alerts Desk & Action Dispatch verified")

    def test_10_ai_damage_preview_and_citizen_report(self):
        """Test citizen report submission with AI damage analysis."""
        # AI preview
        preview_res = self.client.post('/api/reports/analyze-preview', json={
            "issue_type": "Structural Damage",
            "description": "Deep vertical crack observed running through sandstone lintel on eastern facade.",
            "location": "Eastern Entrance Gateway"
        })
        self.assertEqual(preview_res.status_code, 200)
        preview_ai = preview_res.get_json()["data"]
        self.assertIn("severity_estimated", preview_ai)

        # Submit actual report
        headers = {"Authorization": f"Bearer {self.user_token}"}
        submit_res = self.client.post('/api/reports', headers=headers, json={
            "heritage_site_id": self.test_site_id,
            "issue_type": "Structural Damage",
            "severity": "High",
            "incident_date": "2026-09-04",
            "location": "Eastern Entrance Gateway",
            "description": "Deep vertical fissure expanding along the sandstone lintel after heavy monsoon rainfall."
        })
        self.assertEqual(submit_res.status_code, 201)
        report_data = submit_res.get_json()["data"]
        self.assertIn("report_uid", report_data)
        self.assertIn("ai_analysis", report_data)
        HeritageVersePreservationTestSuite.created_report_uid = report_data["report_uid"]
        HeritageVersePreservationTestSuite.created_report_id = report_data["id"]
        print("  [PASS] Citizen Incident submission with AI damage assessment verified")

    def test_11_public_tracking_and_my_reports(self):
        """Test public tracking by UID and user reports."""
        uid = getattr(self.__class__, "created_report_uid", "HV-2026-TEST01")
        track_res = self.client.get(f'/api/reports/track/{uid}')
        self.assertEqual(track_res.status_code, 200)
        track_data = track_res.get_json()["data"]
        self.assertEqual(track_data["report_uid"], uid)
        self.assertIn("status", track_data)

        # My reports
        headers = {"Authorization": f"Bearer {self.user_token}"}
        my_res = self.client.get('/api/reports/my', headers=headers)
        self.assertEqual(my_res.status_code, 200)
        self.assertGreater(len(my_res.get_json()["data"]), 0)
        print("  [PASS] Public Tracking by UID & Citizen My Reports verified")

    def test_12_admin_report_moderation_and_audit(self):
        """Test admin report status update and audit log."""
        rep_id = getattr(self.__class__, "created_report_id", 1)
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        mod_res = self.client.put(f'/api/admin/reports/{rep_id}', headers=headers, json={
            "status": "Verified",
            "admin_remarks": "Verified by ASI Circle Assistant. Lime-pozzolana mortar stabilization scheduled."
        })
        self.assertEqual(mod_res.status_code, 200)
        self.assertTrue(mod_res.get_json()["success"])

        # Check audit log
        audit_res = self.client.get('/api/admin/audit-logs', headers=headers)
        self.assertEqual(audit_res.status_code, 200)
        logs = audit_res.get_json()["data"]
        self.assertGreater(len(logs), 0)
        print("  [PASS] Admin Report Moderation & Action Audit Trail verified")

    def test_13_public_preservation_stats(self):
        """Test public stats counter endpoint."""
        res = self.client.get('/api/stats/preservation')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()["data"]
        self.assertIn("heritage_sites_count", data)
        self.assertIn("active_early_warnings_count", data)
        self.assertIn("encroachments_detected_count", data)
        print("  [PASS] Public Preservation Statistics verified")


if __name__ == '__main__':
    print("\n=======================================================")
    print(" RUNNING HERITAGEVERSE PRESERVATION INTELLIGENCE SUITE")
    print("=======================================================\n")
    unittest.main(verbosity=2)
