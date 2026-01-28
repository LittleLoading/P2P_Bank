import unittest
from unittest.mock import MagicMock
from Core.JsonParser import JsonParser
from tkinter import messagebox


class TestParser(unittest.TestCase):
    def test_config_not_found(self):
        """
        Tests what happens when it cannot find configuration file.
        """
        messagebox.showerror = MagicMock()
        result = JsonParser.get_config("file.json")
        self.assertIsNone(result)
