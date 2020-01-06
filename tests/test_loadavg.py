import unittest

from collector.loadavg import parseLoad


class Testloadavg(unittest.TestCase):
    def test_loadavg(self):
        load1 = 0.21
        parsed_load1 =  parseLoad(
            "0.21 0.37 0.39 1/719 19737")
        self.assertEqual(load1, parsed_load1)
