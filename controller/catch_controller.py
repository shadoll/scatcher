from fastapi import Request, Response, status
from schema.answer import Answer
from controller.base_controller import BaseController
from datetime import datetime
from manager.history import History
from schema.status import Status


class CatchController(BaseController):
    async def catch(
        self,
        request: Request,
        response: Response,
        namespace: str = "requests",
    ) -> Answer:
        if not self.check_namespace(namespace):
            response.status_code = status.HTTP_400_BAD_REQUEST
            return Answer(
                status=Status.error, message="Invalid namespace name provided."
            )
        try:
            json = await request.json()
        except Exception:
            json = {"invalid": "json"}

        last_request = {
            "data": json,
            "method": request.method,
            "url": str(request.url),
            "headers": dict(request.headers),
            "time": datetime.now().isoformat(),
        }
        history = History(namespace)
        history.add(last_request)

        return Answer(status=Status.ok, message="Request was catched.")
