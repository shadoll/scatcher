from pydantic import BaseModel
from schema.methods import Methods


class RequestData(BaseModel):
    method: Methods = Methods.GET
    data: dict|None = None
    params: dict = {}
    form: dict|None = None
    url: str
    headers: dict = {}
    cookies: dict = {}
    http_version: str = ""
    time: str
