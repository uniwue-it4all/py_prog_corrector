import unittest
# noinspection PyUnresolvedReferences
from solution import longest_string


class LongestStringTest(unittest.TestCase):
    def test_longest_string(self):
        self.assertEqual(None, longest_string([]))
        self.assertEqual('1', longest_string(['', '1']))
        self.assertEqual('str', longest_string(['str', 'st', 's']))
