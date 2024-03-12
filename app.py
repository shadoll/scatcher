from fastapi import FastAPI, Request, Response, status
from datetime import datetime
import json

app = FastAPI()

HISTORY_LIMIT = 10
HISTORY_FILE = "storage/requests.json"


def store_last_request(last_request, filename=HISTORY_FILE):
    try:
        with open(filename, "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []

    data.append(last_request)

    if len(data) > HISTORY_LIMIT:
        data.pop(0)

    with open(filename, "w") as f:
        json.dump(data, f)


@app.post("/", status_code=status.HTTP_200_OK)
async def webhook_handler(request: Request, response: Response):

    payload = await request.body()

    last_request = {
        "method": request.method,
        "data": payload.decode("utf-8"),
        "headers": dict(request.headers),
        "url": request.url,
        "time": datetime.now().isoformat(),
    }
    store_last_request(last_request)

    response.status_code = status.HTTP_200_OK

    return {"status": "ok"}


@app.get("/__last_request__", status_code=status.HTTP_200_OK)
async def last_requests():
    try:
        with open(HISTORY_FILE, "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []

    return data[-1:]


@app.get("/__history__", status_code=status.HTTP_200_OK)
async def history():
    try:
        with open(HISTORY_FILE, "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []

    return data
