import unittest
from unittest.mock import patch, Mock
from io import StringIO
import logging
from simple_switch import SimpleSwitch

class TestSimpleSwitch(unittest.TestCase):
    def setUp(self):
        # יצירת מתג עם Logger מודום
        logger = logging.getLogger(__name__)
        logger_handler = logging.StreamHandler(StringIO())
        logger.addHandler(logger_handler)
        logger.setLevel(logging.INFO)
        self.switch = SimpleSwitch()

    def test_mac_learning(self):
        self.switch.receive_frame("00:1A:2B:3C:4D:5E", "FF:FF:FF:FF:FF:FF", 1, vlan_id=1)
        self.assertEqual(self.switch.mac_table, {1: {"00:1A:2B:3C:4D:5E": 1}})

    @patch('simple_switch.logging.info')
    def test_forwarding_unicast(self, mock_info):
        self.switch.receive_frame("00:1A:2B:3C:4D:5E", "FF:FF:FF:FF:FF:FF", 1, vlan_id=1)
        self.switch.receive_frame("00:5E:6F:7A:8B:9C", "00:1A:2B:3C:4D:5E", 2, vlan_id=1)
        mock_info.assert_called_with("Forwarding frame from port 2 to port 1 (VLAN 1)")

    @patch('simple_switch.logging.info')
    def test_flooding_unknown(self, mock_info):
        self.switch.receive_frame("00:1A:2B:3C:4D:5E", "00:5E:6F:7A:8B:9C", 1, vlan_id=1)
        mock_info.assert_called_with("Flooding frame to all ports except 1 (VLAN 1)")

if __name__ == '__main__':
    unittest.main()