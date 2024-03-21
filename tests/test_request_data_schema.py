import unittest
from schema.request_data import RequestData
from schema.methods import Methods


class TestRequestDataSchema(unittest.TestCase):
    def test_request_data_creation(self):
        data = {"key": "value"}
        method = Methods.GET
        url = "https://example.com"
        headers = {"Content-Type": "application/json"}
        time = "2022-01-01 12:00:00"
        request_data = RequestData(data=data, method=method, url=url, headers=headers, time=time)
        self.assertEqual(request_data.data, data)
        self.assertEqual(request_data.method, method)
        self.assertEqual(request_data.url, url)
        self.assertEqual(request_data.headers, headers)
        self.assertEqual(request_data.time, time)


if __name__ == '__main__':
    unittest.main()