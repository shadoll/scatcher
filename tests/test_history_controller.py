import unittest
from fastapi import Response, status
from schema.answer import Answer
from schema.request_data import RequestData
from manager.history import History
from controller.history_controller import HistoryController
from schema.status import Status
from unittest import IsolatedAsyncioTestCase
from schema.methods import Methods
from typing import Any


class TestHistoryController(IsolatedAsyncioTestCase):
    def setUp(self):
        self.namespace = "test"
        self.namespace_invalid = "api"
        self.request_data: dict[Any, Any] = {
            "data": {},
            "method": Methods.GET,
            "url": "https://example.com",
            "headers": {"Content-Type": "application/json"},
            "time": "2024-01-01 12:00:00",
        }

        self.controller = HistoryController()
        self.history = History(namespace=self.namespace)

    async def test_history_invalid_namespace(self):
        response = Response()
        result = await self.controller.history(
            response=response, namespace=self.namespace_invalid
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            result,
            Answer(status=Status.error, message="Invalid namespace name provided."),
        )

    async def test_history_with_id_existing_request(self):
        self.history.add(self.request_data)
        response = Response()
        result = await self.controller.history(
            response,
            id=0,
            namespace=self.namespace,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(result, RequestData(**self.request_data))

    async def test_history_with_id_non_existing_request(self):
        self.history.clear()
        response = Response()
        result = await self.controller.history(
            response=response,
            id=0,
            namespace=self.namespace,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            result, Answer(status=Status.error, message="No requests found.")
        )

    async def test_history_without_id(self):
        self.history.clear()
        self.history.add(self.request_data)
        response = Response()
        result = await self.controller.history(
            response=response, namespace=self.namespace
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(result, [RequestData(**self.request_data)])

    async def test_history_without_id_no_requests(self):
        self.history.clear()
        response = Response()
        result = await self.controller.history(
            response=response, namespace=self.namespace
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            result, Answer(status=Status.error, message="No requests found.")
        )

    async def test_last_requests_invalid_namespace(self):
        response = Response()
        result = await self.controller.last_requests(
            response, namespace=self.namespace_invalid
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            result,
            Answer(status=Status.error, message="Invalid namespace name provided."),
        )

    async def test_last_requests_existing_request(self):
        self.history.clear()
        self.history.add(self.request_data)
        response = Response()
        result = await self.controller.last_requests(
            response=response, namespace=self.namespace
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(result, RequestData(**self.request_data))

    async def test_last_requests_non_existing_request(self):
        self.history.clear()
        response = Response()
        result = await self.controller.last_requests(
            response=response, namespace=self.namespace
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            result, Answer(status=Status.error, message="No requests found.")
        )

    async def test_clear_history_invalid_namespace(self):
        response = Response()
        result = await self.controller.clear_history(
            response=response, namespace=self.namespace_invalid
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            result,
            Answer(status=Status.error, message="Invalid namespace name provided."),
        )

    async def test_clear_history(self):
        response = Response()
        self.history.add(self.request_data)
        result = await self.controller.clear_history(
            response=response, namespace=self.namespace
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            result, Answer(status=Status.success, message="History cleared.")
        )


if __name__ == "__main__":
    unittest.main()
