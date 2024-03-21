from enum import Enum


class Status(str, Enum):
    ok = "ok"
    success = "success"
    error = "error"
