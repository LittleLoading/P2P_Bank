import unittest
from Core.Response import Response


class TestBank(unittest.TestCase):
    def test_response_success(self):
        """
        Tests Response class if output matches format when account is created successfully.
        """
        result = Response.success("BC", "127.0.0.1")
        self.assertEqual(result, "BC 127.0.0.1\n")

    def test_response_error(self):
        """
        Tests Response class if error method works with right format.
        """
        result = Response.error("Error")
        self.assertEqual(result, f"ERROR: ")
