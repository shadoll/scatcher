import unittest
from schema.answer import Answer
from schema.status import Status


class TestAnswerSchema(unittest.TestCase):
    def test_answer_creation(self):
        status = Status.success
        message = "Test message"
        answer = Answer(status=status, message=message)
        self.assertEqual(answer.status, status)
        self.assertEqual(answer.message, message)


if __name__ == '__main__':
    unittest.main()