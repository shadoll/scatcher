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

    BLACK_LIST = [
        ".env",
        "favicon.ico",
        "robots.txt",
        "wp-login.php",
        ".DS_Store",
    ]

    def check_namespace(self, namespace: str) -> bool:
        if namespace in self.RESTRICTED_NAMESPACES:
            return False
        if namespace in self.BLACK_LIST:
            return False
        return True
