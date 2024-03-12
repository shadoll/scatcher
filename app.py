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

@app.get("/", status_code=status.HTTP_200_OK)
@app.post("/", status_code=status.HTTP_200_OK)
@app.put("/", status_code=status.HTTP_200_OK)
@app.delete("/", status_code=status.HTTP_200_OK)
@app.patch("/", status_code=status.HTTP_200_OK)
@app.options("/", status_code=status.HTTP_200_OK)
@app.head("/", status_code=status.HTTP_200_OK)
async def webhook_handler(request: Request, response: Response):
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
    store_last_request(last_request)

    response.status_code = status.HTTP_200_OK

    return {"status": "ok", "message": "Request catched."}


@app.get("/api/__help", status_code=status.HTTP_200_OK)
def help():
    return {
        "message": "This is a simple webhook service. It stores the last 10 requests and returns them on demand.",
        "endpoints": {
            "/": "Accepts a webhook request and stores it.",
            "/docs": "Swagger UI for the API.",
            "/redoc": "ReDoc UI for the API.",
            "/api/__last_request": "GET: Returns the last request received.",
            "/api/__history": "GET: Returns the last 10 requests received.",
            "/api/__history/{id}": "GET: Returns the request with the given ID.",
            "/api/__clear": "GET: Clears the request history.",
        },
    }

@app.get("/api/__last_request", status_code=status.HTTP_200_OK)
async def last_requests():
    try:
        with open(HISTORY_FILE, "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []

    return data[-1]


@app.get("/api/__history/{id}", status_code=status.HTTP_200_OK)
@app.get("/api/__history", status_code=status.HTTP_200_OK)
async def history(id: int = None):
    try:
        with open(HISTORY_FILE, "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []

    if id is not None:
        return data[-id]
    return data

@app.get("/api/__clear", status_code=status.HTTP_200_OK)
async def clear_history():
    with open(HISTORY_FILE, "w") as f:
        json.dump([], f)

    return {"status": "ok", "message": "History cleared."}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
