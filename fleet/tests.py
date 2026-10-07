from unittest.mock import patch

from django.db import DatabaseError
from django.test import Client, TestCase

from .models import Car


class FoundationTests(TestCase):
    def test_catalog_reads_saved_car_and_escapes_html(self):
        Car.objects.create(inventory_code="TEST-001", name="<script>alert(1)</script>")
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "TEST-001")
        self.assertContains(response, "&lt;script&gt;alert(1)&lt;/script&gt;")
        self.assertNotContains(response, "<script>alert(1)</script>")

    def test_health_uses_database(self):
        response = self.client.get("/health/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok", "database": "ok"})

    def test_unavailable_database_has_safe_response(self):
        with patch("fleet.views.connection.cursor", side_effect=DatabaseError("internal-detail")):
            response = self.client.get("/health/")
        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.json(), {"status": "unavailable"})
        self.assertNotContains(response, "internal-detail", status_code=503)

    def test_unknown_path_has_no_debug_traceback(self):
        response = self.client.get("/unknown/")
        self.assertEqual(response.status_code, 404)
        self.assertNotContains(response, "Traceback", status_code=404)

    def test_health_rejects_post_with_csrf_check_and_at_handler(self):
        self.assertEqual(Client(enforce_csrf_checks=True).post("/health/").status_code, 403)
        self.assertEqual(self.client.post("/health/").status_code, 405)
