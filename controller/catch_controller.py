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
            json = None

        try:
            form = await request.form()
        except Exception:
            form = None

        http_version = request.scope.get("http_version")

        last_request = {
            "method": request.method,
            "data": json,
            "params": dict(request.query_params),
            "form": form,
            "url": str(request.url),
            "headers": dict(request.headers),
            "cookies": dict(request.cookies),
            "http_version": http_version,
            "time": datetime.now().isoformat(),
        }
        history = History(namespace)
        history.add(last_request)

        return Answer(status=Status.ok, message="Request was catched.")
