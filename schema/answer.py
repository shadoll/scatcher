from pydantic import BaseModel
from schema.status import Status


class Answer(BaseModel):
    status: Status
    message: str
