import unittest
from solution import ggt


class GgtTest(unittest.TestCase):
    def test_ggt(self):
        self.assertEqual(4, ggt(12, 4))
        self.assertEqual(1, ggt(3, 7))
        self.assertEqual(2, ggt(64, 46))
        self.assertEqual(111, ggt(777, 111))
        self.assertEqual(5, ggt(15, 25))
