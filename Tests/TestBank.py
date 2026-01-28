import unittest
from unittest.mock import MagicMock
from Core.BankController import BankController


class TestBank(unittest.TestCase):
    def setup(self):
        """
        Set up for testing.
        """
        self.db = MagicMock()
        self.config = {"host": "127.0.0.1", "port": 65525}
        self.controller = BankController(self.config, self.db)

    def test_process_ba_command(self):
        """
        Tests if this command calls the right method.
        """
        self.db.get_bank_amout.return_value = 5000
        response = self.controller.process_command("BA")
        self.assertIn("BA 5000", response)
        self.db.get_bank_amout.assert_called_once()

    def test_help_command(self):
        """
        Tests if help displays right output.
        """
        response = self.controller.process_command("help")
        self.assertIn("Your Options", response)
