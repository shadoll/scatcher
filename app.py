import json
import os
from datetime import datetime
from enum import Enum
from fastapi import FastAPI, Request, Response, status
from pydantic import BaseModel

app = FastAPI()

HISTORY_LIMIT = 10
HISTORY_STORAGE = "storage"


class Status(str, Enum):
    ok = "ok"
    error = "error"


class Methods(str, Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"
    OPTIONS = "OPTIONS"
    HEAD = "HEAD"


class Answer(BaseModel):
    status: Status
    message: str


class RequestData(BaseModel):
    data: dict
    method: Methods
    url: str
    headers: dict
    time: str


def store_last_request(request_data, namespace="requests"):

    # Check if the directory exists, if not, create it
    if not os.path.exists(HISTORY_STORAGE):
        os.makedirs(HISTORY_STORAGE)

    filename = f"{HISTORY_STORAGE}/{namespace}.json"

    try:
        with open(filename, "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []

    data.append(request_data)

    if len(data) > HISTORY_LIMIT:
        data.pop(0)

    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

def check_namespace(namespace):
    if namespace == "__history" or namespace == "__last_request" or namespace == "__clear" or namespace == "__help" or namespace == "docs" or namespace == "redoc" or namespace == "api":
        return False
    return True


@app.get("/", status_code=status.HTTP_200_OK)
@app.post("/", status_code=status.HTTP_200_OK)
@app.put("/", status_code=status.HTTP_200_OK)
@app.delete("/", status_code=status.HTTP_200_OK)
@app.patch("/", status_code=status.HTTP_200_OK)
@app.options("/", status_code=status.HTTP_200_OK)
@app.head("/", status_code=status.HTTP_200_OK)
@app.get("/{namespace}", status_code=status.HTTP_200_OK)
@app.post("/{namespace}", status_code=status.HTTP_200_OK)
@app.put("/{namespace}", status_code=status.HTTP_200_OK)
@app.delete("/{namespace}", status_code=status.HTTP_200_OK)
@app.patch("/{namespace}", status_code=status.HTTP_200_OK)
@app.options("/{namespace}", status_code=status.HTTP_200_OK)
@app.head("/{namespace}", status_code=status.HTTP_200_OK)
async def catch(
    request: Request, response: Response, namespace: str = "requests",
) -> Answer:
    if not check_namespace(namespace):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return Answer(status="error", message="Invalid namespace name provided.")
    try:
        json = await request.json()
    except:
        json = {"invalid": "json"}

    last_request = {
        "data": json,
        "method": request.method,
        "url": str(request.url),
        "headers": dict(request.headers),
        "time": datetime.now().isoformat(),
    }
    store_last_request(request_data=last_request, namespace=namespace)

    response.status_code = status.HTTP_200_OK

    return Answer(status="ok", message="Request catched.")


@app.get("/api/__help", status_code=status.HTTP_200_OK)
def help():
    return {
        "message": "This is a simple webhook service. It stores the last 10 requests and returns them on demand.",
        "endpoints": {
            "/": "Accepts a webhook request and stores it.",
            "/{namespace}": "Accepts a webhook request and stores it in the given namespace.",
            "/docs": "Swagger UI for the API.",
            "/redoc": "ReDoc UI for the API.",
            "/api/__last_request": "GET: Returns the last request received.",
            "/api/__last_request/{namespace}": "GET: Returns the last request received for the given namespace.",
            "/api/__history": "GET: Returns the last 10 requests received.",
            "/api/__history/{namespace}": "GET: Returns the last 10 requests received for the given namespace.",
            "/api/__history/{id}": "GET: Returns the request with the given ID.",
            "/api/__history/{namespace}/{id}": "GET: Returns the request with the given ID for the given namespace.",
            "/api/__clear": "GET: Clears the request history.",
            "/api/__clear/{namespace}": "GET: Clears the request history for the given namespace.",
        },
    }


@app.get("/api/__last_request", status_code=status.HTTP_200_OK)
@app.get("/api/__last_request/{namespace}", status_code=status.HTTP_200_OK)
async def last_requests(response: Response, namespace: str = "requests",) -> Answer | RequestData:
    if not check_namespace(namespace):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return Answer(status="error", message="Invalid namespace name provided.")
    filename = f"{HISTORY_STORAGE}/{namespace}.json"
    try:
        with open(filename, "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []

    if len(data) == 0:
        return Answer(status="error", message="No requests found.")

    return RequestData(**data[-1])


@app.get("/api/__history/{id}", status_code=status.HTTP_200_OK)
@app.get("/api/__history", status_code=status.HTTP_200_OK)
@app.get("/api/__history/{namespace}/{id}", status_code=status.HTTP_200_OK)
@app.get("/api/__history/{namespace}", status_code=status.HTTP_200_OK)
async def history(
    response: Response,
    id: int = 0, namespace: str = "requests",
) -> Answer | RequestData | list[RequestData]:
    if not check_namespace(namespace):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return Answer(status="error", message="Invalid namespace name provided.")
    filename = f"{HISTORY_STORAGE}/{namespace}.json"
    try:
        with open(filename, "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []

    if id is not None:
        if len(data) == 0:
            return Answer(status="error", message="No requests found.")
        return RequestData(**data[-id])
    return [RequestData(**d) for d in data]


@app.get("/api/__clear", status_code=status.HTTP_200_OK)
@app.get("/api/__clear/{namespace}", status_code=status.HTTP_200_OK)
async def clear_history(response: Response,
    namespace: str = "requests",) -> Answer:
    if not check_namespace(namespace):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return Answer(status="error", message="Invalid namespace name provided.")
    filename = f"{HISTORY_STORAGE}/{namespace}.json"
    with open(filename, "w") as f:
        json.dump([], f)

    return Answer(status="ok", message="History cleared.")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
