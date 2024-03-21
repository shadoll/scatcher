import unittest
from controller.base_controller import BaseController

class TestBaseController(unittest.TestCase):
    def setUp(self):
        self.controller = BaseController()

    def test_check_namespace_restricted(self):
        restricted_namespaces = [
            "__history",
            "__last_request",
            "__last",
            "__clear",
            "docs",
            "redoc",
            "api",
        ]
        for namespace in restricted_namespaces:
            result = self.controller.check_namespace(namespace)
            self.assertFalse(result)

    def test_check_namespace_allowed(self):
        allowed_namespaces = [
            "test",
            "example",
            "namespace",
            "custom",
        ]
        for namespace in allowed_namespaces:
            result = self.controller.check_namespace(namespace)
            self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()