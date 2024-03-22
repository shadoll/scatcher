import json
import os
from schema.methods import Methods

class History:
    HISTORY_LIMIT = 10
    HISTORY_STORAGE = "storage"

    def __init__(self, namespace: str = "requests") -> None:
        self.namespace = namespace
        self.filename = f"{self.HISTORY_STORAGE}/{namespace}.json"
        self.data: list = []
        self.check_directory()

    def check_directory(self) -> None:
        if not os.path.exists(self.HISTORY_STORAGE):
            os.makedirs(self.HISTORY_STORAGE)

    def load(self) -> None:
        try:
            with open(self.filename, "r") as f:
                self.data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.data = []

    def save(self) -> None:
        with open(self.filename, "w") as f:
            json.dump(self.data, f, indent=4)

    def clear(self) -> None:
        self.data = []
        self.save()

    def all(self) -> list | None:
        self.load()
        if len(self.data) == 0:
            return None
        for item in self.data:
            if "method" in item:
                item["method"] = Methods(item["method"])
        return self.data

    def get(self, index: int) -> dict | None:
        self.all()

        return self.data[index] if index < len(self.data) else None

    def last(self) -> dict | None:
        self.all()

        return self.data[-1] if len(self.data) > 0 else None

    def add(self, request_data: dict) -> None:
        self.load()
        self.data.append(request_data)
        if len(self.data) > self.HISTORY_LIMIT:
            self.data.pop(0)
        self.save()
