from typing import List, Optional
import unittest


def longest_string(my_list: List[str]) -> Optional[str]:
    longest = None
    for string in my_list:
        if longest is None or len(string) > len(longest):
            longest = string
    return longest


class LongestStringTest(unittest.TestCase):
    def test_longest_string(self):
        self.assertEqual(None, longest_string([]))
        self.assertEqual('1', longest_string(['', '1']))
        self.assertEqual('str', longest_string(['str', 'st', 's']))
