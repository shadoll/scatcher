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


if __name__ == "__main__":
    unittest.main()
