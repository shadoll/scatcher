class BaseController:
    RESTRICTED_NAMESPACES = [
        "__history",
        "__last_request",
        "__last",
        "__clear",
        "docs",
        "redoc",
        "api",
    ]

    def check_namespace(self, namespace: str) -> bool:
        if namespace in self.RESTRICTED_NAMESPACES:
            return False
        return True
