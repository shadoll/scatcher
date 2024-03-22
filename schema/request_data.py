from pydantic import BaseModel
from schema.methods import Methods


class RequestData(BaseModel):
    method: Methods = Methods.GET
    data: dict = {}
    params: dict = {}
    form: dict = {}
    url: str
    headers: dict = {}
    cookies: dict = {}
    http_version: str = ""
    time: str
