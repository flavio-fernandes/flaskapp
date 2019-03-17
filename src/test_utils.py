import json
import os
import unittest
from unittest import mock
from unittest.mock import patch, mock_open

import utils
import socket


class TestUtils(unittest.TestCase):
    def test_get_hostname(self):
        self.assertNotEqual(utils.get_hostname(), "")

    def test_get_local_address(self):
        self.assertTrue(socket.inet_aton(utils.get_local_address()))

    def test_get_target(self):
        with patch.dict(os.environ, {'TARGET': 'foo'}):
            self.assertEqual('foo', utils.get_target())

    def test_get_server_hit_count(self):
        hits_before = utils.get_server_hit_count()
        hits_after = utils.get_server_hit_count()
        self.assertGreater(hits_after, hits_before, "Hits should have increased")

    def test_read_config(self):
        mock_app = mock.Mock()
        mock_app.config = {}
        mock_config_file = {"one": "1", "two": "2"}
        with patch('utils.open', mock_open(read_data=json.dumps(mock_config_file))) as m:
            utils.read_config(mock_app)
            self.assertTrue(m.called, "open did not take place")
        self.assertDictEqual(mock_app.config, mock_config_file, "App config does not have expected values")


if __name__ == '__main__':
    unittest.main()
