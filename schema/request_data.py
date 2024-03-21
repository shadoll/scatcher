from pydantic import BaseModel
from schema.methods import Methods


class RequestData(BaseModel):
    data: dict
    method: Methods = Methods.GET
    url: str
    headers: dict
    time: str
