import unittest
from manager.history import History
from schema.methods import Methods
from typing import Any

class TestHistoryManager(unittest.TestCase):
    def setUp(self):
        self.namespace = "test"
        self.request_data: dict[Any, Any] = {
            "data": {},
            "method": Methods.GET,
            "url": "https://example.com",
            "headers": {"Content-Type": "application/json"},
            "time": "2024-01-01 12:00:00",
        }
        self.history = History(namespace=self.namespace)

    def tearDown(self):
        self.history.clear()

    def test_load_empty_history(self):
        self.history.load()
        self.assertEqual(self.history.data, [])

    def test_save_and_load_history(self):
        self.history.add(self.request_data)
        self.history.save()
        self.history.load()
        self.assertEqual(self.history.data, [self.request_data])

    def test_clear_history(self):
        self.history.add(self.request_data)
        self.history.clear()
        self.assertEqual(self.history.data, [])

    def test_get_existing_request(self):
        self.history.add(self.request_data)
        result = self.history.get(0)
        self.assertEqual(result, self.request_data)

    def test_get_non_existing_request(self):
        result = self.history.get(0)
        self.assertIsNone(result)

    def test_get_request_with_index_out_of_range(self):
        self.history.add(self.request_data)
        result = self.history.get(1)
        self.assertIsNone(result)

    def test_last_existing_request(self):
        self.history.add(self.request_data)
        result = self.history.last()
        self.assertEqual(result, self.request_data)

    def test_last_non_existing_request(self):
        result = self.history.last()
        self.assertIsNone(result)

    def test_last_request_with_limit_reached(self):
        for i in range(History.HISTORY_LIMIT + 1):
            self.history.add(self.request_data)
        result = self.history.last()
        self.assertEqual(result, self.request_data)

    def test_add_request(self):
        self.history.clear()
        self.history.add(self.request_data)
        self.assertEqual(self.history.data, [self.request_data])

    def test_add_request_with_limit_reached(self):
        for i in range(History.HISTORY_LIMIT + 1):
            self.history.add(self.request_data)
        self.assertEqual(len(self.history.data), History.HISTORY_LIMIT)

    def test_all_requests(self):
        for i in range(History.HISTORY_LIMIT):
            self.history.add(self.request_data)
        result = self.history.all()
        self.assertEqual(result, [self.request_data for i in range(History.HISTORY_LIMIT)])

    def test_all_requests_empty(self):
        result = self.history.all()
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
