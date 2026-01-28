import unittest
from unittest.mock import MagicMock
from Network.Server import Server


class TestServer(unittest.TestCase):
    def setup(self):
        """
            Set up for testing.
        """
        self.ui = MagicMock()
        self.controller = MagicMock()
        self.server = Server("127.0.0.1", 65525, 20, self.controller, self.ui)

    def test_server_init(self):
        """
        Checks server attribute values.
        """
        self.assertEqual(self.server.host, "127.0.0.1")
        self.assertEqual(self.server.port, 65525)
        self.assertTrue(self.server.running)
