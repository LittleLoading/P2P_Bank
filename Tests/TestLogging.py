import unittest
import json
from Core.Logging import Logging
import os


class TestLogging(unittest.TestCase):
    def test_entry(self):
        """
        Makes test log file and checks the format.
        """
        test_file = "test_log.json"
        Logging.log_file = test_file
        Logging.log("127.0.0.1", "BC", "SUCCESS", "Test message")
        with open(test_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.assertEqual(data[0]["command"], "BC")
            self.assertEqual(data[0]["status"], "SUCCESS")
        if os.path.exists(test_file):
            os.remove(test_file)
        