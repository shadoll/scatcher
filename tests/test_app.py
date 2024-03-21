import unittest
from fastapi.testclient import TestClient
from app import app
from unittest import IsolatedAsyncioTestCase

client = TestClient(app)


class TestApp(IsolatedAsyncioTestCase):
    def setUp(self):
        self.methods = ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"]
        self.namespace = "test"
        self.namespace_invalid = "api"

    def test_catch_endpoint(self):
        for method in self.methods:
            response = client.request(method, "/")
            self.assertEqual(response.status_code, 200)
            response_namespace = client.request(method, f"/{self.namespace}")
            self.assertEqual(response_namespace.status_code, 200)

    def test_catch_invalid_namespace(self):
        response = client.get("/api")
        self.assertEqual(response.status_code, 400)

    def test_last_requests_endpoint(self):
        response = client.get("/api/__last_request")
        self.assertEqual(response.status_code, 200)

    def test_last_requests_namespace(self):
        response = client.get(f"/api/__last_request/{self.namespace}")
        self.assertEqual(response.status_code, 200)

    def test_last_requests_invalid_namespace(self):
        response = client.get(f"/api/__last_request/{self.namespace_invalid}")
        self.assertEqual(response.status_code, 400)

    def test_last_endpoint(self):
        response = client.get("/api/__last")
        self.assertEqual(response.status_code, 200) # WTF?

    def test_last_namespace(self):
        response = client.get(f"/api/__last/{self.namespace}")
        self.assertEqual(response.status_code, 200)

    def test_history_endpoint(self):
        response = client.get("/api/__history")
        self.assertEqual(response.status_code, 200)

    def test_history_id_endpoint(self):
        response_id = client.get("/api/__history/1")
        self.assertEqual(response_id.status_code, 200)

    def test_history_namespace(self):
        response_namespace = client.get(f"/api/__history/{self.namespace}")
        self.assertEqual(response_namespace.status_code, 200)

    def test_history_namespace_id(self):
        response_namespace_id = client.get(f"/api/__history/{self.namespace}/1")
        self.assertEqual(response_namespace_id.status_code, 200)

    def test_clear_history_endpoint(self):
        response = client.get("/api/__clear")
        self.assertEqual(response.status_code, 200)

    def test_clear_history_namespace(self):
        response = client.get(f"/api/__clear/{self.namespace}")
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
