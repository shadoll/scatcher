from fastapi import Response, status
from schema.answer import Answer
from schema.request_data import RequestData
from manager.history import History
from controller.base_controller import BaseController
from schema.status import Status


class HistoryController(BaseController):
    async def history(
        self,
        response: Response,
        id: int | None = None,
        namespace: str = "requests",
    ) -> Answer | RequestData | list[RequestData]:
        if not self.check_namespace(namespace=namespace):
            response.status_code = status.HTTP_400_BAD_REQUEST
            return Answer(
                status=Status.error,
                message="Invalid namespace name provided.",
            )

        history = History(namespace=namespace)

        if id is not None:
            item = history.get(id)
            if item is None:
                return Answer(
                    status=Status.error,
                    message="No requests found.",
                )
            return RequestData(**item)
        return [RequestData(**d) for d in history.all()]

    async def last_requests(
        self,
        response: Response,
        namespace: str = "requests",
    ) -> Answer | RequestData:
        if not self.check_namespace(namespace=namespace):
            response.status_code = status.HTTP_400_BAD_REQUEST
            return Answer(
                status=Status.error,
                message="Invalid namespace name provided.",
            )

        last = History(namespace=namespace).last()

        if last is None:
            return Answer(
                status=Status.error,
                message="No requests found.",
            )

        return RequestData(**last)

    async def clear_history(
        self,
        response: Response,
        namespace: str = "requests",
    ) -> Answer:
        if not self.check_namespace(namespace=namespace):
            response.status_code = status.HTTP_400_BAD_REQUEST
            return Answer(
                status=Status.error,
                message="Invalid namespace name provided.",
            )

        History(namespace=namespace).clear()
        return Answer(
            status=Status.success,
            message="History cleared.",
        )
