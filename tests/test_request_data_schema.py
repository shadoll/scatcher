import unittest
from schema.request_data import RequestData
from schema.methods import Methods
from typing import Any


class TestRequestDataSchema(unittest.TestCase):
    def setUp(self) -> None:
        self.request_data: dict[Any, Any] = {
            "method": Methods.GET,
            "data": {"key": "value"},
            "params": {"param": "value"},
            "form": {"form": "data"},
            "url": "https://example.com",
            "headers": {"Content-Type": "application/json"},
            "cookies": {"session": "session_id"},
            "http_version": "HTTP/1.1",
            "time": "2024-01-01 12:00:00",
        }
        self.request_data_less: dict[Any, Any] = {
            "method": "GET",
            "data": None,
            "params": {},
            "form": None,
            "url": "https://example.com",
            "headers": {},
            "cookies": {},
            "http_version": "HTTP/1.1",
            "time": "2024-01-01 12:00:00",
        }

    def test_request_data_creation(self):
        request_data = RequestData(**self.request_data)
        self.assertEqual(request_data.data, self.request_data["data"])
        self.assertEqual(request_data.method, Methods.GET)
        self.assertEqual(request_data.url, self.request_data["url"])
        self.assertEqual(request_data.headers, self.request_data["headers"])
        self.assertEqual(request_data.time, self.request_data["time"])
        self.assertEqual(request_data.http_version, "HTTP/1.1")
        self.assertEqual(request_data.cookies, self.request_data["cookies"])
        self.assertEqual(request_data.form, self.request_data["form"])
        self.assertEqual(request_data.params, self.request_data["params"])

    def test_request_data_creation_less_data(self):
        request_data = RequestData(**self.request_data_less)
        self.assertEqual(request_data.data, None)
        self.assertEqual(request_data.method, Methods.GET)
        self.assertEqual(request_data.url, self.request_data_less["url"])
        self.assertEqual(request_data.headers, self.request_data_less["headers"])
        self.assertEqual(request_data.time, self.request_data_less["time"])
        self.assertEqual(request_data.http_version, "HTTP/1.1")
        self.assertEqual(request_data.cookies, self.request_data_less["cookies"])
        self.assertEqual(request_data.form, None)
        self.assertEqual(request_data.params, self.request_data_less["params"])

    def test_request_data_creation_invalid_method(self):
        with self.assertRaises(ValueError):
            RequestData(**{**self.request_data, "method": "INVALID"})
        with self.assertRaises(ValueError):
            RequestData(**{**self.request_data, "method": 123})
        with self.assertRaises(ValueError):
            RequestData(**{**self.request_data, "method": None})

    def test_request_data_creation_invalid_headers(self):
        with self.assertRaises(ValueError):
            RequestData(**{**self.request_data, "headers": "INVALID"})
        with self.assertRaises(ValueError):
            RequestData(**{**self.request_data, "headers": 123})
        with self.assertRaises(ValueError):
            RequestData(**{**self.request_data, "headers": None})


if __name__ == "__main__":
    unittest.main()
