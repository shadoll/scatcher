from fastapi import FastAPI, Request, Response, status
from schema.answer import Answer
from schema.request_data import RequestData
from controller.history_controller import HistoryController
from controller.catch_controller import CatchController

app = FastAPI()

history_controller = HistoryController()
catch_controller = CatchController()


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
    request: Request,
    response: Response,
    namespace: str = "requests",
) -> Answer:
    return await catch_controller.catch(
        request=request, response=response, namespace=namespace
    )


@app.get("/api/__last_request", status_code=status.HTTP_200_OK)
@app.get("/api/__last}", status_code=status.HTTP_200_OK)
@app.get("/api/__last_request/{namespace}", status_code=status.HTTP_200_OK)
@app.get("/api/__last/{namespace}", status_code=status.HTTP_200_OK)
async def last_requests(
    response: Response,
    namespace: str = "requests",
) -> Answer | RequestData:
    return await history_controller.last_requests(
        response=response, namespace=namespace
    )


@app.get("/api/__history/{id}", status_code=status.HTTP_200_OK)
@app.get("/api/__history", status_code=status.HTTP_200_OK)
@app.get("/api/__history/{namespace}/{id}", status_code=status.HTTP_200_OK)
@app.get("/api/__history/{namespace}", status_code=status.HTTP_200_OK)
async def history(
    response: Response,
    id: int | None = None,
    namespace: str = "requests",
) -> Answer | RequestData | list[RequestData]:
    return await history_controller.history(
        response=response, id=id, namespace=namespace
    )


@app.get("/api/__clear", status_code=status.HTTP_200_OK)
@app.get("/api/__clear/{namespace}", status_code=status.HTTP_200_OK)
async def clear_history(
    response: Response,
    namespace: str = "requests",
) -> Answer:
    return await history_controller.clear_history(
        response=response, namespace=namespace
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
